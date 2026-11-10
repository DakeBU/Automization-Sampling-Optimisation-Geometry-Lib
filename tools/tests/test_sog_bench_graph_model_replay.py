"""Test offline reconstruction from controlled transport bytes, not model runs."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools.tests.test_sog_bench_graph_model import Provider, response
import sog_bench_graph_model as model
import sog_bench_graph_model_replay as replay


class GraphModelReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.item = model.graph.admitted('sogb-g007')

    def archive(self, folder, provider=None):
        item = self.item
        if provider is None:
            provider = Provider([response(1, 'graph_submit', item['answer']),
                                 response(2, 'graph_inspect', {'id': item['targets'][0]}),
                                 response(3, 'graph_submit', item['answer'])])
        root = Path(folder) / 'run'
        report = model.run(item, root, model='model-test', expected='snapshot-test', max_lookups=1,
                           max_output_tokens=512, provider=provider)
        return root, report

    def resign(self, root, rel, payload, *, forged_results=None):
        raw = payload if isinstance(payload, bytes) else model.bench.encoded(payload)
        (root / rel).write_bytes(raw)
        report = json.loads((root / 'comparison.json').read_bytes())
        report['files_sha256'][rel] = model.bench.sha(raw)
        if forged_results is not None:
            report['results'] = forged_results
        (root / 'comparison.json').write_bytes(model.bench.encoded(report))

    def test_exact_replay_keeps_readonly_archive_and_does_not_call_provider(self):
        with tempfile.TemporaryDirectory() as folder:
            root, report = self.archive(folder)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.object(model.OpenAIResponses, '__call__', side_effect=AssertionError('Network not allowed')):
                checked = replay.replay(root, self.item)
            self.assertEqual(checked['results'], report['results'])
            self.assertEqual(checked['network_calls'], 0)
            self.assertFalse(checked['model_measurement'])
            self.assertFalse(checked['provenance_authenticated'])
            self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_self_resigned_prompt_continuation_or_observation_fails(self):
        lookup = model.PROFILES[1]
        with tempfile.TemporaryDirectory() as folder:
            root, _ = self.archive(folder)
            rel = f'{lookup}/0002/request.json'
            request = json.loads((root / rel).read_bytes())
            request['input'][-1]['output'] = '{"kind":"forged-observation"}'
            self.resign(root, rel, request)
            with self.assertRaisesRegex(ValueError, 'Archived request.json differs'):
                replay.replay(root, self.item)
        with tempfile.TemporaryDirectory() as folder:
            root, _ = self.archive(folder)
            rel = f'{lookup}/actions.jsonl'
            records = [json.loads(raw) for raw in (root / rel).read_bytes().splitlines()]
            records[0]['observation']['remaining_lookups'] = 2
            self.resign(root, rel, b''.join(model.graph.line(row) for row in records))
            with self.assertRaisesRegex(ValueError, 'Archived actions.jsonl differs'):
                replay.replay(root, self.item)

    def test_self_resigned_report_cannot_change_canonical_score(self):
        with tempfile.TemporaryDirectory() as folder:
            root, report = self.archive(folder)
            report['results'][0]['score']['points'] = 0
            self.resign(root, 'given-snapshot/result.json', report['results'][0], forged_results=report['results'])
            with self.assertRaisesRegex(ValueError, 'Archived result.json differs'):
                replay.replay(root, self.item)

    def test_raw_http_error_is_unscored_but_missing_raw_cannot_be_replayed(self):
        with tempfile.TemporaryDirectory() as folder:
            root, report = self.archive(folder, Provider([(429, {'error': 'fixture'})]))
            checked = replay.replay(root, self.item)
            self.assertEqual(checked['results'], report['results'])
            self.assertIsNone(checked['results'][0]['score'])
            self.assertEqual(checked['results'][1]['api_turns'], 0)

        class NoResponse(Provider):
            def __call__(self, raw):
                raise model.ProviderFailure('fixture transport stopped', 'provider-transport')

        with tempfile.TemporaryDirectory() as folder:
            root, report = self.archive(folder, NoResponse([]))
            self.assertIsNone(report['results'][0]['score'])
            with self.assertRaisesRegex(ValueError, 'missing expected entries'):
                replay.replay(root, self.item)

    def test_model_no_final_keeps_both_selected_denominators(self):
        status, baseline = response(1, 'graph_submit', self.item['answer'])
        baseline['output'] = []
        _, lookup = response(2, 'graph_submit', self.item['answer'])
        lookup.update(status='incomplete', incomplete_details={'reason': 'max_output_tokens'}, output=[])
        with tempfile.TemporaryDirectory() as folder:
            root, report = self.archive(folder, Provider([(status, baseline), (status, lookup)]))
            checked = replay.replay(root, self.item)
            self.assertEqual(checked['results'], report['results'])
            self.assertEqual([row['termination'] for row in checked['results']],
                             ['model-no-single-offered-tool-call', 'model-output-budget'])
            for row in checked['results']:
                self.assertEqual(row['score']['points'], 0)
                self.assertEqual(row['score']['max_points'], 1)
                self.assertEqual(row['score']['submitted'], 0)

    def test_extra_artifacts_and_task_drift_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root, _ = self.archive(folder)
            (root / model.PROFILES[1] / '0003').mkdir()
            with self.assertRaisesRegex(ValueError, 'Unexpected archive entry'):
                replay.replay(root, self.item)
        with tempfile.TemporaryDirectory() as folder:
            root, _ = self.archive(folder)
            with self.assertRaisesRegex(ValueError, 'binding drift'):
                replay.replay(root, {**self.item, 'binding_sha256': '0' * 64})


if __name__ == '__main__':
    unittest.main()
