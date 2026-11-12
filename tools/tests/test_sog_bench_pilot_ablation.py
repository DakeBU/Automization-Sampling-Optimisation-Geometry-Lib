"""Check the paired pilot records without loading a model or executing Lean."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench_pilot_ablation as pilot


class DiagnosticAblationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixed = pilot.context()

    def test_exactly_the_diagnostic_text_is_withheld(self):
        views = self.fixed[0]['messages_by_condition']
        status_only, diagnostic = (views[name] for name in pilot.CONDITIONS)
        self.assertEqual(status_only[:-1], diagnostic[:-1])
        before = json.loads(status_only[-1]['content'].splitlines()[1])
        after = json.loads(diagnostic[-1]['content'].splitlines()[1])
        self.assertEqual(before, {**after, 'feedback': {**after['feedback'], 'diagnostic': pilot.WITHHELD}})
        self.assertEqual(after['feedback']['kind'], 'proof-rejected')
        self.assertNotEqual(after['feedback']['diagnostic'], pilot.WITHHELD)

    def test_changed_body_never_inherits_the_archived_native_result(self):
        plan, prefix, archived_final, _ = self.fixed
        b = pilot.bench
        matching_text = archived_final.removeprefix(prefix).decode('utf-8')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw = b.encoded({**plan, 'operator_environment': {'system': 'fixture', 'python': 'fixture'}})
            (root / 'plan.json').write_bytes(raw)
            for condition, body in zip(pilot.CONDITIONS, (matching_text, matching_text + ' changed')):
                turn = {'input_ids': [1], 'output_ids': [2], 'raw_text': body}
                candidate = pilot.candidate(prefix, turn, plan)
                (root / f'{condition}-candidate.lean.txt').write_bytes(candidate)
                (root / f'{condition}-model.json').write_bytes(b.encoded({
                    'plan_sha256': b.sha(raw), 'condition': condition, 'turn': turn,
                    'messages': plan['messages_by_condition'][condition],
                    'candidate_sha256': b.sha(candidate)}))
            result = pilot.summarize(root, self.fixed)
            self.assertIs(result['fresh_native_verification'], False)
            self.assertEqual(result['conditions']['status-only']['reused_archived_score'], 0)
            self.assertIsNone(result['conditions']['diagnostic']['reused_archived_score'])
            self.assertIsNone(result['conditions']['diagnostic']['reused_archived_native_result'])
            self.assertTrue(result['output_token_ids_equal'])
            self.assertFalse(result['proof_bodies_equal'])
            (root / 'diagnostic-candidate.lean.txt').write_bytes(archived_final)
            with self.assertRaisesRegex(ValueError, 'candidate, prompt or plan drift'):
                pilot.summarize(root, self.fixed)

    def test_actual_recorded_generations_replay_without_a_model(self):
        report = pilot.verify(ROOT / 'runs/20261112-bench-lean-diagnostic-ablation')
        status, text = (report['conditions'][name] for name in pilot.CONDITIONS)
        self.assertEqual([status['input_token_count'], text['input_token_count']], [410, 731])
        self.assertEqual([status['output_token_count'], text['output_token_count']], [21, 21])
        self.assertTrue(report['output_token_ids_equal'])
        self.assertTrue(report['proof_bodies_equal'])
        self.assertIs(report['fresh_native_verification'], False)
        self.assertTrue(all(row['matches_archived_native_submission']
                            and row['reused_archived_native_result'] == 'proof-rejected'
                            for row in (status, text)))


if __name__ == '__main__':
    unittest.main()
