"""Trusted contract fixtures: no provider calls and no execution of submitted Lean."""
from __future__ import annotations

import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_lean_model as model

workspace = model.workspace
runtime = model.runtime
MODEL = 'explicit-unit-fixture-not-a-real-model'
TOKENS = 512


def provenance():
    return {'kind': 'declared-model-run', 'provider': 'openai', 'model': MODEL,
        'model_version': MODEL, 'retrieval_profile': 'provided-prompt-template-only',
        'tools': ['lean_workspace'], 'decoding': {'max_output_tokens': TOKENS}, 'seed': None}


def response(action='submit', source='unit fixture; never executed', identity='one'):
    return {'id': 'response-' + identity, 'model': MODEL, 'status': 'completed',
        'output': [{'type': 'reasoning', 'id': 'reasoning-' + identity, 'encrypted_content': 'opaque-fixture'},
            {'type': 'function_call', 'name': 'lean_workspace', 'call_id': 'call-' + identity,
             'arguments': json.dumps({'action': action, 'source': source})}],
        'usage': {'output_tokens': 1}}


class FixtureProvider:
    kind = 'controlled-unit-fixture-not-an-api-or-model'

    def __init__(self, *replies):
        self.replies = iter(replies); self.requests = []

    def __call__(self, request):
        self.requests.append(json.loads(request))
        reply = next(self.replies)
        if isinstance(reply, BaseException):
            raise reply
        return (reply if isinstance(reply, bytes) else runtime.bench.encoded(reply)), {
            'http_status': 200, 'request_id': 'unit-fixture'}


class ModelBridgeTests(unittest.TestCase):
    def make_workspace(self, root, max_checks=1, identity='sogb-001'):
        task = root / 'task'; stage = root / 'stage'; prepared = root / 'runtime'
        (task / 'agent').mkdir(parents=True); stage.mkdir(); prepared.mkdir()
        (task / 'agent/prompt.json').write_bytes(b'{"question":"prompt only"}')
        (task / 'agent/Solution.lean.txt').write_bytes(b'fixed target; no gold')
        (task / 'oracle').mkdir(); (task / 'oracle/gold.txt').write_bytes(b'PRIVATE GOLD MUST NOT ENTER MODEL INPUT')
        (task / 'operator.json').write_bytes(runtime.bench.encoded({'files': {
            'agent/' + p.name: runtime.bench.sha(p.read_bytes()) for p in (task / 'agent').iterdir()}}))
        (stage / 'stage.json').write_bytes(runtime.bench.encoded({'id': identity, 'binding_sha256': 'fixture'}))
        (prepared / 'preparation.json').write_bytes(b'{}')
        directory = root / 'workspace'
        with patch.object(workspace.sys, 'platform', 'linux'), patch.object(workspace.shutil, 'which', return_value='docker'), \
                patch.object(runtime, 'checked_packet', return_value={'id': identity, 'binding_sha256': 'fixture'}), \
                patch.object(runtime, 'check_runtime'):
            workspace.start(task=task, stage=stage, prepared=prepared, output=directory,
                provenance=provenance(), max_checks=max_checks)
        return directory

    def make_suite(self, root):
        tasks=root/'packets';stages=root/'stages';prepared=root/'prepared';prepared.mkdir()
        (prepared/'preparation.json').write_bytes(b'{}')
        for identity in ('sogb-001','sogb-002'):
            item=root/identity;item.mkdir();self.make_workspace(item,identity=identity)
            shutil.copytree(item/'task',tasks/identity);shutil.copytree(item/'stage',stages/identity)
        with patch.object(workspace.sys,'platform','linux'),patch.object(workspace.shutil,'which',return_value='docker'), \
                patch.object(runtime,'checked_packet',side_effect=lambda p:{'id':p.name,'binding_sha256':'fixture',
                    'family':'controlled-interface-fixture','split':'public-dev'}),patch.object(runtime,'check_runtime'):
            workspace.start_suite(tasks=tasks,stages=stages,prepared=prepared,output=root/'suite',
                task_ids=['sogb-001','sogb-002'],provenance=provenance(),max_checks=1)
        return root/'suite'

    @staticmethod
    def fake_verifier(**kwargs):
        output = kwargs['output']; output.mkdir()
        report = {'kind': 'accepted', 'model_measurement': False, 'scope': 'unexecuted trusted unit fixture'}
        workspace.write_new(output / 'result.json', report)
        (output / 'compiler-diagnostic.bin').write_bytes(b'Unexecuted verifier fixture, not Lean feedback')
        return report

    def run_fixture(self, directory, output, provider):
        with patch.object(runtime, 'checked_packet'), \
                patch.object(runtime, 'run_submission', side_effect=self.fake_verifier):
            return model.run(directory, output, model=MODEL, max_output_tokens=TOKENS, provider=provider)

    def test_check_then_final_replays_all_items_and_only_agent_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            provider = FixtureProvider(response('check', identity='check'), response(identity='final'))
            output = root / 'transcript'; result = self.run_fixture(directory, output, provider)
            self.assertEqual(result['stop'], 'first-final-submitted')
            self.assertTrue(result['final_accepted']); self.assertEqual(result['denominator'], 1)
            self.assertFalse(result['model_measurement']); self.assertFalse(result['provenance_authenticated'])
            self.assertEqual(len(provider.requests), 2)
            first = provider.requests[0]
            self.assertFalse(first['store']); self.assertFalse(first['parallel_tool_calls'])
            self.assertFalse(first['stream']); self.assertEqual(first['max_output_tokens'], TOKENS)
            self.assertNotIn('PRIVATE GOLD', json.dumps(provider.requests))
            self.assertNotIn(str(root), json.dumps(provider.requests))
            self.assertEqual([t['name'] for t in first['tools']], ['lean_workspace'])
            self.assertTrue(any(i.get('encrypted_content') == 'opaque-fixture' for i in provider.requests[1]['input']))
            self.assertTrue(any(i.get('type') == 'function_call_output' and i['call_id'] == 'call-check'
                for i in provider.requests[1]['input']))
            for path, digest in result['files_sha256'].items():
                self.assertEqual(runtime.bench.sha((output / path).read_bytes()), digest)
            with self.assertRaises(ValueError):
                self.run_fixture(directory, root / 'retry', FixtureProvider(response()))

    def test_model_source_is_only_verifier_data_and_invalid_final_stays_selected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            with patch.object(runtime, 'checked_packet'), patch.object(runtime, 'run_submission') as native:
                result = model.run(directory, root / 'transcript', model=MODEL,
                    max_output_tokens=TOKENS, provider=FixtureProvider(response(source='x' * 65537)))
            native.assert_not_called()
            self.assertEqual(result['final_outcome'], 'invalid-submission')
            self.assertEqual(result['denominator'], 1)
            self.assertEqual(workspace.history(directory)[1][0]['action'], 'submit')

    def test_unknown_multiple_duplicate_or_incomplete_provider_calls_do_not_execute(self):
        variants = []
        bad = response(); bad['output'][-1]['name'] = 'shell'; variants.append(bad)
        bad = response(); bad['output'].append(bad['output'][-1]); variants.append(bad)
        bad = response(); bad['output'][-1]['arguments'] = '{"action":"check","action":"submit","source":"x"}'; variants.append(bad)
        bad = response(); bad['output'][-1]['arguments'] = '{"action":"submit","source":"x","command":"never run"}'; variants.append(bad)
        for reply in variants:
            with self.subTest(reply=reply), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); directory = self.make_workspace(root)
                with patch.object(runtime, 'checked_packet'), patch.object(runtime, 'run_submission') as native:
                    result = model.run(directory, root / 'transcript', model=MODEL,
                        max_output_tokens=TOKENS, provider=FixtureProvider(reply))
                native.assert_not_called()
                self.assertEqual(result['final_outcome'], 'no-final-submission')
                self.assertEqual(result['denominator'], 1)

    def test_provider_failure_is_recorded_once_without_automatic_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            provider = FixtureProvider(model.ProviderFailure('provider-transport-error-no-automatic-retry','provider-transport'))
            result = self.run_fixture(directory, root / 'transcript', provider)
            self.assertEqual(len(provider.requests), 1)
            self.assertEqual(result['final_outcome'], 'infrastructure-error')
            self.assertIn('no-automatic-retry', result['stop'])
            self.assertTrue((root / 'transcript/0001/started.json').exists())
            self.assertTrue((directory / 'external-run.json').exists())
            self.assertEqual(json.loads((directory/'external-end.json').read_bytes())['reason'],'provider-transport')

    def test_interruption_before_first_tool_permanently_reserves_model_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            with self.assertRaises(KeyboardInterrupt):
                self.run_fixture(directory, root / 'transcript', FixtureProvider(KeyboardInterrupt()))
            self.assertTrue((directory / 'external-run.json').exists())
            self.assertTrue((root / 'transcript/0001/finished.json').exists())
            with self.assertRaisesRegex(ValueError, 'reserved'):
                self.run_fixture(directory, root / 'retry', FixtureProvider(response()))
            self.assertEqual(workspace.close(directory)['final_outcome'], 'infrastructure-error')

    def test_no_final_after_successful_check_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            no_final = {'id': 'no-final', 'model':MODEL, 'status': 'completed', 'output': []}
            result = self.run_fixture(directory, root / 'transcript', FixtureProvider(response('check'), no_final))
            self.assertEqual(result['final_outcome'], 'no-final-submission')
            self.assertFalse(result['final_accepted'])
            self.assertEqual(workspace.history(directory)[1][0]['result']['kind'], 'accepted')

    def test_provider_envelope_identity_and_budget_classification_order(self):
        cases=[]
        bad=response();bad['status']='incomplete';cases.append((bad,'infrastructure-error','provider-protocol'))
        bad=response();bad['output'].append({'type':'web_search_call'});cases.append((bad,'infrastructure-error','provider-protocol'))
        bad=response();bad['status']='failed';bad['error']={'code':'server_error'};cases.append((bad,'infrastructure-error','provider-protocol'))
        budget=response();budget['status']='incomplete';budget['incomplete_details']={'reason':'max_output_tokens'}
        cases.append((budget,'no-final-submission','model-output-budget'))
        wrong=json.loads(json.dumps(budget));wrong['model']='wrong';cases.append((wrong,'infrastructure-error','provider-identity'))
        malformed=json.loads(json.dumps(budget));malformed['output']=None;cases.append((malformed,'infrastructure-error','provider-protocol'))
        for reply,outcome,reason in cases:
            with self.subTest(reason=reason),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);directory=self.make_workspace(root)
                result=self.run_fixture(directory,root/'transcript',FixtureProvider(reply))
                self.assertEqual(result['final_outcome'],outcome)
                self.assertEqual(json.loads((directory/'external-end.json').read_bytes())['reason'],reason)

    def test_real_model_bridge_to_suite_accounting_keeps_infrastructure_unscored(self):
        class HTTPErrorProvider(FixtureProvider):
            def __call__(self,request):
                raw,receipt=super().__call__(request);receipt['http_status']=503;return raw,receipt
        for case in ('transport','http','check-infrastructure','model-no-final'):
            with self.subTest(case=case),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=self.make_suite(root);child=suite/'tasks/sogb-001'
                if case=='transport':provider=FixtureProvider(model.ProviderFailure('unit-transport','provider-transport'))
                elif case=='http':provider=HTTPErrorProvider({'error':{'code':'unexecuted-server-fixture'}})
                elif case=='check-infrastructure':provider=FixtureProvider(response('check'))
                else:
                    reply=response();reply['output']=[];provider=FixtureProvider(reply)
                if case=='check-infrastructure':
                    def infrastructure(**kwargs):
                        out=kwargs['output'];out.mkdir();report={'kind':'infrastructure-error','model_measurement':False}
                        workspace.write_new(out/'result.json',report);return report
                    with patch.object(runtime,'checked_packet'),patch.object(runtime,'run_submission',side_effect=infrastructure):
                        model.run(child,root/'transcript',model=MODEL,max_output_tokens=TOKENS,provider=provider)
                else:self.run_fixture(child,root/'transcript',provider)
                rolled=workspace.suite_status(suite,finish=True)
                expected='no-final-submission' if case=='model-no-final' else 'infrastructure-error'
                self.assertEqual(rolled['denominator'],2)
                self.assertEqual(rolled['results'][0]['outcome'],expected)
                self.assertEqual(rolled['results'][1]['outcome'],'no-final-submission')

    def test_protocol_metadata_and_agent_file_drift_fail_before_network(self):
        for field in ('tools', 'decoding', 'retrieval_profile', 'seed', 'agent'):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); directory = self.make_workspace(root)
                if field == 'agent':
                    (directory / 'agent/Solution.lean.txt').write_bytes(b'drift')
                else:
                    path = directory / 'session.json'; manifest = json.loads(path.read_bytes())
                    manifest['provenance'][field] = 'mismatched'
                    path.write_bytes(runtime.bench.encoded(manifest))
                provider = FixtureProvider(response())
                with self.assertRaises(ValueError):
                    self.run_fixture(directory, root / 'transcript', provider)
                self.assertEqual(provider.requests, [])

    def test_missing_or_wrong_returned_model_never_dispatches_a_tool(self):
        for returned in (None, '', 'not-the-frozen-version'):
            with self.subTest(returned=returned), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp); directory = self.make_workspace(root)
                reply = response(); reply['model'] = returned
                with patch.object(runtime, 'checked_packet'), patch.object(runtime, 'run_submission') as native:
                    result = model.run(directory, root / 'transcript', model=MODEL,
                        max_output_tokens=TOKENS, provider=FixtureProvider(reply))
                native.assert_not_called()
                self.assertIn('provider-model-identity', result['stop'])
                record = json.loads((root / 'transcript/0001/finished.json').read_bytes())
                self.assertEqual(record['provider_model'], returned)
                self.assertEqual(record['usage'], reply['usage'])

    def test_expected_snapshot_is_explicit_even_when_request_uses_an_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            path = directory / 'session.json'; manifest = json.loads(path.read_bytes())
            manifest['provenance']['model_version'] = 'explicit-returned-fixture-snapshot'
            path.write_bytes(runtime.bench.encoded(manifest))
            reply = response(); reply['model'] = 'explicit-returned-fixture-snapshot'
            result = self.run_fixture(directory, root / 'transcript', FixtureProvider(reply))
            self.assertTrue(result['final_accepted'])
            selection = json.loads((root / 'transcript/selection.json').read_bytes())
            self.assertEqual(selection['identity_policy'], 'exact-declared-provider-model-version')
            self.assertEqual(selection['expected_returned_model'], reply['model'])

    def test_repeated_response_identity_with_distinct_calls_stops_before_second_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); directory = self.make_workspace(root)
            first = response('check', identity='first'); second = response(identity='second')
            second['id'] = first['id']
            result = self.run_fixture(directory, root / 'transcript', FixtureProvider(first, second))
            self.assertEqual(result['stop'], 'repeated-provider-response-identity')
            self.assertEqual(len(workspace.history(directory)[1]), 1)
            self.assertEqual(result['final_outcome'], 'infrastructure-error')

    def test_transport_has_fixed_endpoint_no_redirect_or_secret_archive(self):
        secret = 'unit-only-secret-not-a-real-key'
        transport = model.OpenAIResponses(secret)
        self.assertIsNone(model.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://elsewhere.invalid'))
        class Reply(io.BytesIO):
            code = 200
            headers = {'x-request-id': 'fixture-request', 'date': 'fixture'}
        seen = []
        def open_fake(request, timeout):
            seen.append(request)
            return Reply(runtime.bench.encoded(response()))
        with patch.object(transport._opener, 'open', side_effect=open_fake):
            raw, receipt = transport(b'{"unit":"not sent"}')
        self.assertEqual(seen[0].full_url, model.ENDPOINT)
        self.assertEqual(seen[0].get_header('Authorization'), 'Bearer ' + secret)
        self.assertNotIn(secret, raw.decode()); self.assertNotIn(secret, json.dumps(receipt))
        for body in (secret.encode(), b'x' * (model.WIRE_BYTES + 1)):
            with self.subTest(size=len(body)), patch.object(transport._opener, 'open', return_value=Reply(body)):
                with self.assertRaises(model.ProviderFailure) as error:
                    transport(b'{}')
                self.assertNotIn(secret, str(error.exception))

    def test_replayed_call_id_precedes_malformed_argument_classification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory=self.make_workspace(root)
            first=response('check',identity='first');second=response(identity='second')
            second['output'][-1]['call_id']=first['output'][-1]['call_id']
            second['output'][-1]['arguments']='not JSON'
            result=self.run_fixture(directory,root/'transcript',FixtureProvider(first,second))
            self.assertEqual(result['stop'],'repeated-provider-call-identity')
            self.assertEqual(result['final_outcome'],'infrastructure-error')
            self.assertEqual(len(workspace.history(directory)[1]),1)
            end=json.loads((directory/'external-end.json').read_bytes())
            self.assertEqual(end['disposition'],'infrastructure-error');self.assertEqual(end['reason'],'provider-identity')


if __name__ == '__main__':
    unittest.main()
