"""Controlled local-graph transport tests; none are model measurements."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_graph_local as pilot

g, b, suite = pilot.graph, pilot.bench, pilot.suite


def turn(text):
    return {'input_ids': [1], 'output_ids': [2], 'raw_text': text}


class LocalGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = b.curriculum.graph_items()
        cls.decisions = g.review.summary(cls.items)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / 'pilot'
        for obj, name, result in ((b.curriculum, 'graph_items', self.items),
                                  (g.review, 'summary', self.decisions)):
            mock = patch.object(obj, name, return_value=result)
            mock.start()
            self.addCleanup(mock.stop)
        self.digest = pilot.plan(self.root, ['sogb-g007', 'sogb-g010'], 2)

    def record(self, generate):
        with patch.object(pilot.local, 'check_assets'), patch.object(pilot.local, 'CpuModel', return_value=generate):
            return pilot.run(self.root, self.digest, Path('unused-test-assets'))

    def test_first_final_and_fresh_condition_messages(self):
        calls = []
        def generate(messages):
            calls.append(messages)
            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0]['content'], pilot.SYSTEM)
            prompt = json.loads(messages[1]['content'])
            self.assertFalse({'answer', 'operator_task_sha256', 'binding_sha256'} & prompt.keys())
            self.assertEqual('snapshot' in prompt, prompt['profile'] == suite.SNAPSHOT)
            return turn('{"action":"submit","answer":{"nodes":[],"entails_mathematical_necessity":false}}')
        result = self.record(generate)
        self.assertEqual(len(calls), 4)
        self.assertEqual(result, pilot.replay(self.root, self.digest))
        self.assertFalse(result['inference_authenticated'])
        self.assertEqual(result['accounting']['selected_per_condition'], 2)
        with self.assertRaises(FileExistsError):
            self.record(generate)

    def test_lookup_is_chosen_by_model_and_actual_observation_is_forwarded(self):
        def generate(messages):
            prompt = json.loads(messages[1]['content'])
            if prompt['profile'] == g.PROFILE and len(messages) == 2:
                return turn('{"action":"inspect","id":"not-a-node"}')
            if prompt['profile'] == g.PROFILE:
                self.assertEqual(json.loads(messages[-1]['content'])['kind'], 'unknown-node')
            return turn('{"action":"submit","answer":null}')
        result = self.record(generate)
        self.assertEqual(result['model_turns']['sogb-g007/' + g.PROFILE], 2)
        self.assertEqual(result['accounting']['conditions'][g.PROFILE]['rows'][0]['lookups_used'], 1)

    def test_multiple_lines_and_fences_are_not_repaired(self):
        result = self.record(lambda _: turn('```json\n{"action":"submit","answer":null}\n```'))
        self.assertEqual(result, pilot.replay(self.root, self.digest))
        self.assertEqual(set(result['model_turns'].values()), {1})
        rows = result['accounting']['conditions']
        self.assertEqual(rows[suite.SNAPSHOT]['rows'][0]['termination'], 'lookup-budget-exhausted-no-final')
        self.assertEqual(rows[g.PROFILE]['rows'][0]['lookups_used'], 1)

    def test_inference_failure_keeps_unfinished_and_unstarted_null(self):
        def failed(_):
            raise RuntimeError('controlled inference failure')
        with self.assertRaises(OSError):
            self.record(failed)
        accounting = suite.account(self.root / 'suite', self.digest)
        self.assertTrue(all(row['points'] is None for c in accounting['conditions'].values() for row in c['rows']))
        self.assertTrue((self.root / 'model/sogb-g007/given-snapshot/inference-error.json').is_file())
        with self.assertRaises(ValueError):
            pilot.replay(self.root, self.digest)

    def test_replay_rejects_prompt_output_and_extra_record_tampering(self):
        self.record(lambda _: turn('{"action":"submit","answer":null}'))
        file = self.root / 'model/sogb-g007/given-snapshot/0001.json'
        original = file.read_bytes()
        row = json.loads(original)
        row['messages'][1]['content'] = 'invented prompt'
        file.write_bytes(b.encoded(row))
        with self.assertRaisesRegex(ValueError, 'conversation'):
            pilot.replay(self.root, self.digest)
        file.write_bytes(original)
        row = json.loads(original)
        row['turn']['raw_text'] = '{"action":"find","query":"gradient"}'
        file.write_bytes(b.encoded(row))
        with self.assertRaisesRegex(ValueError, 'replay'):
            pilot.replay(self.root, self.digest)
        file.write_bytes(original)
        (file.parent / '0002.json').write_bytes(original)
        with self.assertRaisesRegex(ValueError, 'Unexpected'):
            pilot.replay(self.root, self.digest)

    def test_empty_text_consumes_budget_not_infrastructure_or_retry(self):
        result = self.record(lambda _: turn(''))
        self.assertEqual(result['model_turns']['sogb-g007/' + g.PROFILE], 3)
        self.assertEqual(result['accounting']['conditions'][g.PROFILE]['rows'][0]['points'], 0)

    def test_invalid_tokens_and_plan_drift_fail_closed(self):
        for key, value in (('input_ids', [True]), ('output_ids', []), ('raw_text', 3)):
            row = turn('text')
            row[key] = value
            with self.assertRaises(ValueError):
                pilot.validate_turn(row)
        with self.assertRaisesRegex(ValueError, 'digest'):
            pilot.replay(self.root, '0' * 64)
        with patch.object(pilot, 'SYSTEM', 'changed instruction'):
            with self.assertRaisesRegex(ValueError, 'pin drift'):
                pilot.load(self.root, self.digest)


class RecordedLocalGraphTests(unittest.TestCase):
    def test_actual_archive_and_saved_report_replay_without_inference(self):
        root = Path(__file__).resolve().parents[2] / 'runs/20261117-bench-local-graph-first'
        digest = '0a2abcf1f00e17983683c3f4652d23310011c55f1a4ebdf3ae5e34dbc7d989e0'
        with patch.object(pilot.local, 'CpuModel', side_effect=AssertionError('No model load in replay')):
            report = pilot.replay(root, digest)
        self.assertEqual(report, json.loads((root / 'accounting.json').read_bytes()))
        self.assertEqual(set(report['model_turns'].values()), {1})
        for condition in report['accounting']['conditions'].values():
            self.assertEqual((condition['replayed'], condition['observed_points']), (2, 0))
            self.assertTrue(all(row['valid_final'] is False for row in condition['rows']))
        # Charged malformed lines are not real graph navigation.
        for file in (root / 'suite/runs').glob('*/*/actions.jsonl'):
            for raw in file.read_bytes().splitlines():
                event = json.loads(raw)
                self.assertNotIn(event['observation']['kind'], ('matches', 'node'))


if __name__ == '__main__':
    unittest.main()
