"""Paired graph accounting: controlled software tests, not model results."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_graph_suite as suite

g = suite.graph
b = suite.bench
META = {'kind': 'controlled-software-fixture', 'agent': 'test', 'revision': '1',
        'settings': {'no_network': True}}
IDS = ['sogb-g007', 'sogb-g010']


class PairedSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = b.curriculum.graph_items()
        cls.decisions = g.review.summary(cls.items)

    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / 'suite'
        for obj, attr, value in [(b.curriculum, 'graph_items', self.items),
                                 (g.review, 'summary', self.decisions)]:
            context = patch.object(obj, attr, return_value=value)
            context.start()
            self.addCleanup(context.stop)
        self.digest = suite.plan(self.root, IDS, 5, META)

    def run_case(self, identity, profile, *requests):
        stream = io.BytesIO(b''.join(g.line(row) for row in requests))
        outputs = []
        result = suite.record(self.root, self.digest, identity, profile, stream, outputs.append)
        self.assertEqual(outputs[0], (self.root / 'prompts' / identity / (profile + '.json')).read_bytes())
        return result, [json.loads(raw) for raw in outputs]

    def test_common_selection_and_separate_visible_projections(self):
        plan, items = suite.load(self.root, self.digest)
        self.assertEqual(list(items), IDS)
        self.assertEqual(plan['attempt_policy'], 'first-final-no-retries')
        snapshot, lookup = [json.loads(suite.visible_prompt(items[IDS[0]], p, 5)) for p in suite.PROFILES]
        self.assertIn('snapshot', snapshot)
        self.assertNotIn('snapshot', lookup)
        self.assertEqual(snapshot['question'], lookup['question'])
        self.assertEqual(list(snapshot['tools']), ['submit'])
        self.assertEqual(set(lookup['tools']), {'submit', 'find', 'inspect'})
        for prompt in (snapshot, lookup):
            self.assertFalse({'answer', 'binding_sha256', 'operator_task_sha256'} & prompt.keys())

    def test_full_denominator_and_first_final_including_one_arm_only(self):
        item = next(x for x in self.items if x['id'] == IDS[0])
        correct = {'action': 'submit', 'answer': item['answer']}
        bad = {'action': 'submit', 'answer': {**item['answer'], 'entails_mathematical_necessity': True}}
        record, _ = self.run_case(IDS[0], suite.SNAPSHOT, bad, correct)
        self.assertEqual(record['score']['points'], 0)
        with self.assertRaises(FileExistsError):
            self.run_case(IDS[0], suite.SNAPSHOT, correct)
        record, seen = self.run_case(IDS[0], g.PROFILE,
            {'action': 'inspect', 'id': item['targets'][0]}, correct)
        self.assertEqual(seen[1]['kind'], 'node')
        self.assertEqual(record['score']['points'], 1)
        self.run_case(IDS[1], g.PROFILE)  # real EOF; not an unstarted case
        accounting = suite.account(self.root, self.digest)
        self.assertEqual(accounting['selected_per_condition'], 2)
        self.assertEqual(accounting['paired_replayed_ids'], [IDS[0]])
        self.assertEqual([r['points'] for r in accounting['conditions'][suite.SNAPSHOT]['rows']], [0, None])
        self.assertEqual([r['points'] for r in accounting['conditions'][g.PROFILE]['rows']], [1, 0])
        self.assertEqual(accounting['conditions'][g.PROFILE]['rows'][1]['termination'], 'eof-no-final')
        self.assertFalse(accounting['model_measurement_certified'])

    def test_mid_record_failure_does_not_retry_or_become_zero(self):
        class Stopped:
            def readline(self, _):
                raise RuntimeError('simulated disconnected collector')
        with self.assertRaisesRegex(RuntimeError, 'disconnected'):
            suite.record(self.root, self.digest, IDS[0], g.PROFILE, Stopped(), lambda _: None)
        row = suite.account(self.root, self.digest)['conditions'][g.PROFILE]['rows'][0]
        self.assertEqual((row['termination'], row['points']), ('unfinished-archive', None))
        with self.assertRaises(FileExistsError):
            self.run_case(IDS[0], g.PROFILE)

    def test_observation_tamper_fails_even_with_resigned_action_digest(self):
        self.run_case(IDS[0], g.PROFILE, {'action': 'find', 'query': 'gradient'})
        folder = self.root / 'runs' / IDS[0] / g.PROFILE
        event = json.loads((folder / 'actions.jsonl').read_bytes())
        event['observation']['remaining_lookups'] = 0
        fake = g.line(event)
        (folder / 'actions.jsonl').write_bytes(fake)
        report = json.loads((folder / 'result.json').read_bytes())
        (folder / 'result.json').write_bytes(b.encoded({**report, 'actions_sha256': b.sha(fake)}))
        with self.assertRaisesRegex(ValueError, 'differ from replay'):
            suite.account(self.root, self.digest)

    def test_scope_drift_extra_cases_and_budget_fail_closed(self):
        with self.assertRaisesRegex(ValueError, 'digest'):
            suite.account(self.root, '0' * 64)
        with self.assertRaisesRegex(ValueError, 'predeclared'):
            self.run_case('sogb-g008', suite.SNAPSHOT)
        with self.assertRaisesRegex(ValueError, 'at most one'):
            suite.plan(self.root.parent / 'duplicate-family', ['sogb-g006', 'sogb-g007'], 5, META)
        with self.assertRaisesRegex(ValueError, 'compiled-body'):
            suite.plan(self.root.parent / 'imports', ['sogb-g001'], 5, META)
        record, seen = self.run_case(IDS[0], suite.SNAPSHOT, {'action': 'find', 'query': 'gradient'})
        self.assertEqual(record['lookups_used'], 0)
        self.assertEqual(seen[-1]['kind'], 'lookup-budget-exhausted-no-final')
        (self.root / 'runs' / 'sogb-g008').mkdir()
        with self.assertRaisesRegex(ValueError, 'Unexpected task'):
            suite.account(self.root, self.digest)


if __name__ == '__main__':
    unittest.main()
