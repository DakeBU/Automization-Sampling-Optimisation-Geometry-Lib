"""External lifecycle/rollup fixtures; no API calls or submitted Lean execution."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import sog_bench_lean_workspace as workspace
from tools.tests import test_sog_bench_lean as fixtures

runtime=workspace.runtime
META={'client':'trusted-unit-fixture','client_source_sha256_lf':'a'*64,'selection_sha256':'b'*64}


class ExternalRunTests(unittest.TestCase):
    def create(self, root):
        return fixtures.LeanWorkspaceTests().create(root)

    def reserve(self,directory):
        return workspace.reserve_external_run(directory,dict(META))

    def evidence(self,directory,path,disposition='infrastructure-error',reason='provider-http'):
        value={'schema_version':1,'kind':'external-client-termination-evidence',
            'session_sha256':runtime.bench.sha((directory/'session.json').read_bytes()),
            'reservation_sha256':runtime.bench.sha((directory/'external-run.json').read_bytes()),
            'selection_sha256':META['selection_sha256'],'client_source_sha256_lf':META['client_source_sha256_lf'],
            'disposition':disposition,'reason':reason,'client_stop':'unexecuted-unit-fixture','facts':{'fixture':True}}
        path.write_bytes(runtime.bench.encoded(value));return value

    def finish(self,directory,path,disposition='infrastructure-error',reason='provider-http'):
        self.evidence(directory,path,disposition,reason)
        return workspace.finish_external_run(directory,disposition=disposition,reason=reason,evidence=path)

    @staticmethod
    def verifier(kind):
        def verify(**kwargs):
            output=kwargs['output'];output.mkdir()
            result={'kind':kind,'model_measurement':False,'scope':'unexecuted trusted fixture'}
            if kind=='resource-limit':result['interruption']='wall-time'
            workspace.write_new(output/'result.json',result)
            return result
        return verify

    def test_infrastructure_copy_is_real_bounded_evidence_and_final_cannot_be_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory=self.create(root);self.reserve(directory)
            source=root/'stop.json';end=self.finish(directory,source)
            self.assertEqual((directory/'external-evidence.json').read_bytes(),source.read_bytes())
            self.assertEqual(end['evidence_sha256'],runtime.bench.sha(source.read_bytes()))
            with self.assertRaises(ValueError):workspace.act(directory,{'action':'submit','source':'never run'})
            result=workspace.close(directory)
            self.assertEqual(result['final_outcome'],'infrastructure-error');self.assertEqual(result['denominator'],1)

    def test_all_genuine_final_outcomes_survive_later_external_failure(self):
        for kind in ('accepted','proof-rejected','resource-limit','invalid-submission','infrastructure-error'):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);directory=self.create(root);self.reserve(directory)
                with patch.object(runtime,'run_submission',side_effect=self.verifier(kind)):
                    workspace.act(directory,{'action':'submit','source':'unexecuted unit fixture'})
                self.finish(directory,root/'stop.json')
                result=workspace.close(directory)
                self.assertEqual(result['final_outcome'],kind);self.assertEqual(result['final_submissions'],1)
                self.assertFalse(result['interrupted'])
                with self.assertRaises(ValueError):workspace.act(directory,{'action':'submit','source':'replacement'})

    def test_result_without_final_observation_is_interrupted_but_earlier_loss_fails_closed(self):
        for earlier in (False,True):
            with self.subTest(earlier=earlier),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);directory=self.create(root);self.reserve(directory)
                with patch.object(runtime,'run_submission',side_effect=self.verifier('accepted')):
                    if earlier:workspace.act(directory,{'action':'check','source':'unexecuted check'})
                    workspace.act(directory,{'action':'submit','source':'unexecuted final'})
                (directory/'actions/0001/observation.json').unlink()
                if earlier:
                    with self.assertRaisesRegex(ValueError,'nonterminal'):workspace.close(directory)
                else:self.assertEqual(workspace.close(directory)['final_outcome'],'infrastructure-error')

    def test_two_child_rollup_separates_infrastructure_without_dropping_unattempted_target(self):
        for reason,disposition,expected in [('provider-http','infrastructure-error','infrastructure-error'),
                ('provider-transport','infrastructure-error','infrastructure-error'),
                ('verifier-infrastructure','infrastructure-error','infrastructure-error'),
                ('model-protocol-error','completed','no-final-submission')]:
            with self.subTest(reason=reason),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                child=suite/'tasks/sogb-001';self.reserve(child)
                self.finish(child,root/'stop.json',disposition,reason)
                self.assertEqual(workspace.suite_status(suite)['outcome_counts'],{'unfinished':2})
                result=workspace.suite_status(suite,finish=True)
                self.assertEqual(result['denominator'],2)
                self.assertEqual(result['results'][0]['outcome'],expected)
                self.assertEqual(result['results'][1]['outcome'],'no-final-submission')

    def test_unended_partial_collection_is_only_infrastructure_after_explicit_close(self):
        for partial in (False,True):
            with self.subTest(partial=partial),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                child=suite/'tasks/sogb-001';self.reserve(child)
                if partial:(child/'external-evidence.json').write_bytes(b'{partial evidence')
                self.assertEqual(workspace.suite_status(suite)['outcome_counts'],{'unfinished':2})
                result=workspace.suite_status(suite,finish=True)
                self.assertEqual(result['outcome_counts'],{'infrastructure-error':1,'no-final-submission':1})
                completion=json.loads((child/'completion.json').read_bytes())
                self.assertTrue(completion['interrupted']);self.assertIsNone(completion['external_end_sha256'])
                if partial:
                    (child/'external-evidence.json').write_bytes(b'changed partial')
                    with self.assertRaises(ValueError):workspace.suite_status(suite)

    def test_evidence_binding_schema_and_nonfinite_fail_before_copy(self):
        fields=['session_sha256','reservation_sha256','selection_sha256','client_source_sha256_lf',
            'disposition','reason','schema_version','kind','client_stop','facts']
        for field in fields+['nonfinite','duplicate','too-large']:
            with self.subTest(field=field),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);directory=self.create(root);self.reserve(directory);path=root/'stop.json'
                item=self.evidence(directory,path)
                if field=='nonfinite':path.write_bytes(b'{"schema_version":NaN}')
                elif field=='duplicate':path.write_bytes(b'{"kind":"x","kind":"y"}')
                elif field=='too-large':path.write_bytes(b'x'*(workspace.REQUEST_BYTES+1))
                else:
                    item[field]=True if field=='schema_version' else '' if field=='client_stop' else 'wrong'
                    path.write_bytes(runtime.bench.encoded(item))
                with self.assertRaises(ValueError):
                    workspace.finish_external_run(directory,disposition='infrastructure-error',reason='provider-http',evidence=path)
                self.assertFalse((directory/'external-evidence.json').exists())

    def test_missing_or_drifted_canonical_evidence_end_and_completion_fail_rollup(self):
        for change in ('missing','evidence','end-count','reservation','completion'):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                child=suite/'tasks/sogb-001';self.reserve(child);self.finish(child,root/'stop.json')
                workspace.suite_status(suite,finish=True)
                if change=='missing':(child/'external-evidence.json').unlink()
                else:
                    filename={'evidence':'external-evidence.json','end-count':'external-end.json',
                        'reservation':'external-run.json','completion':'completion.json'}[change]
                    path=child/filename;item=json.loads(path.read_bytes())
                    if change=='end-count':item['event_count']=False
                    elif change=='evidence':item['facts']={'changed':True}
                    elif change=='reservation':item['metadata']['selection_sha256']='c'*64
                    else:item['external_run_sha256']=None
                    path.write_bytes(runtime.bench.encoded(item))
                with self.assertRaises(ValueError):workspace.suite_status(suite)

    def test_duplicate_reservation_end_and_partial_copy_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory=self.create(root);self.reserve(directory)
            with self.assertRaises(ValueError):self.reserve(directory)
            self.finish(directory,root/'stop.json')
            old=(directory/'external-evidence.json').read_bytes()
            with self.assertRaises(ValueError):self.finish(directory,root/'other.json')
            self.assertEqual((directory/'external-evidence.json').read_bytes(),old)

    def test_entire_lifecycle_loss_cannot_downgrade_managed_completion_to_legacy(self):
        for final in (False,True):
            for sealed in (False,True):
                with self.subTest(final=final,sealed=sealed),tempfile.TemporaryDirectory() as tmp:
                    root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                    child=suite/'tasks/sogb-001';self.reserve(child)
                    if final:
                        with patch.object(runtime,'run_submission',side_effect=self.verifier('accepted')):
                            workspace.act(child,{'action':'submit','source':'unexecuted fixture'})
                    self.finish(child,root/'stop.json','completed','final-submitted' if final else 'model-no-final')
                    workspace.close(child)
                    if sealed:workspace.suite_status(suite,finish=True)
                    for name in ('external-run.json','external-end.json','external-evidence.json'):(child/name).unlink()
                    with self.assertRaises(ValueError):workspace.suite_status(suite)

    def test_nullable_managed_completion_fields_cannot_disappear(self):
        for field in ('external_end_sha256','external_evidence_sha256'):
            with self.subTest(field=field),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                child=suite/'tasks/sogb-001';self.reserve(child);workspace.close(child)
                path=child/'completion.json';item=json.loads(path.read_bytes())
                self.assertIsNone(item.pop(field));path.write_bytes(runtime.bench.encoded(item))
                with self.assertRaises(ValueError):workspace.suite_status(suite)

    def test_readonly_status_validates_ended_and_orphan_evidence_without_closing(self):
        for change in ('missing','corrupt','orphan'):
            with self.subTest(change=change),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);suite=fixtures.LeanWorkspaceTests().create_suite(root)
                child=suite/'tasks/sogb-001';self.reserve(child);self.finish(child,root/'stop.json')
                if change=='missing':(child/'external-evidence.json').unlink()
                elif change=='corrupt':(child/'external-evidence.json').write_bytes(b'corrupt')
                else:(child/'external-run.json').unlink()
                with self.assertRaises(ValueError):workspace.suite_status(suite)
                self.assertFalse((child/'completion.json').exists())

    def test_completed_reason_cannot_fabricate_or_hide_final(self):
        for final in (False,True):
            with self.subTest(final=final),tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);directory=self.create(root);self.reserve(directory)
                if final:
                    with patch.object(runtime,'run_submission',side_effect=self.verifier('proof-rejected')):
                        workspace.act(directory,{'action':'submit','source':'unexecuted fixture'})
                reason='model-no-final' if final else 'final-submitted'
                with self.assertRaises(ValueError):self.finish(directory,root/'stop.json','completed',reason)

    @unittest.skipIf(sys.platform=='win32','POSIX evidence-link fixture; Linux CI exercises it')
    def test_symbolic_evidence_is_rejected_without_reading_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);directory=self.create(root);self.reserve(directory)
            target=root/'target.json';self.evidence(directory,target)
            link=root/'link.json';link.symlink_to(target)
            with self.assertRaises(ValueError):
                workspace.finish_external_run(directory,disposition='infrastructure-error',reason='provider-http',evidence=link)


if __name__=='__main__':unittest.main()
