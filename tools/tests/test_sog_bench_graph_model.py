"""Fixture transport only; never call a model or claim a score from these tests."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_graph_model as model


class Provider:
    kind = 'controlled-responses-fixture'

    def __init__(self, replies):
        self.replies = iter(replies)
        self.requests = []

    def __call__(self, raw):
        self.requests.append(json.loads(raw))
        status, response = next(self.replies)
        return model.bench.encoded(response), {'http_status': status, 'request_id': 'fixture-request'}


def response(i, name, args, *, returned='snapshot-test'):
    return (200, {'id': f'resp_{i}', 'model': returned, 'status': 'completed', 'usage': {'output_tokens': 10},
                  'output': [{'type': 'reasoning', 'id': f'rs_{i}', 'encrypted_content': f'fixture_{i}'},
                             {'type': 'function_call', 'call_id': f'call_{i}', 'name': name,
                              'arguments': args if isinstance(args, str) else json.dumps(args)}]})


class GraphModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.item = model.graph.admitted('sogb-g007')

    def run_at(self, root, provider, max_lookups=1):
        return model.run(self.item, root, model='model-test', expected='snapshot-test', max_lookups=max_lookups,
                         max_output_tokens=512, provider=provider)

    def test_pair_freezes_profiles_and_uses_same_scorer_in_fresh_contexts(self):
        item = self.item
        provider = Provider([response(1, 'graph_submit', item['answer']),
                             response(2, 'graph_inspect', {'id': item['targets'][0]}),
                             response(3, 'graph_submit', item['answer'])])
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'run'
            report = self.run_at(root, provider)
            baseline, lookup = report['results']
            self.assertEqual(baseline['score'], lookup['score'])
            self.assertEqual([r['api_turns'] for r in report['results']], [1, 2])
            self.assertFalse(report['model_measurement'])
            self.assertEqual(report['family'], item['family'])
            a, b, c = provider.requests
            self.assertEqual(len(a['input']), len(b['input']))
            self.assertEqual(len(b['input']), 1)
            p0, p1 = [json.loads(r['input'][0]['content']) for r in (a, b)]
            self.assertEqual(p0['question'], p1['question'])
            self.assertEqual(p0['evidence'], p1['evidence'])
            self.assertIn('snapshot', p0)
            self.assertNotIn('snapshot', p1)
            self.assertNotIn('answer', p0)
            self.assertNotIn('answer', p1)
            self.assertEqual([t['name'] for t in a['tools']], ['graph_submit'])
            self.assertEqual(c['input'][1]['encrypted_content'], 'fixture_2')
            feedback = c['input'][-1]
            self.assertEqual(feedback['call_id'], 'call_2')
            self.assertEqual(json.loads(feedback['output'])['remaining_lookups'], 0)
            self.assertNotIn('score', feedback['output'])
            self.assertEqual({r['parallel_tool_calls'] for r in provider.requests}, {False})
            self.assertEqual({r['store'] for r in provider.requests}, {False})
            for path, digest in report['files_sha256'].items():
                self.assertEqual(model.bench.sha((root / path).read_bytes()), digest)
            with self.assertRaises(FileExistsError):
                self.run_at(root, provider)

    def test_infrastructure_never_becomes_zero_or_a_retry(self):
        for reply, reason in [((429, {'error': 'fixture HTTP failure'}), 'provider-http'),
                              (response(1, 'graph_submit', self.item['answer'], returned='different'),
                               'provider-identity')]:
            with self.subTest(reason=reason), tempfile.TemporaryDirectory() as folder:
                provider = Provider([reply])
                root = Path(folder) / 'run'
                first, second = self.run_at(root, provider)['results']
                self.assertEqual(len(provider.requests), 1)
                self.assertEqual(first['termination'], reason)
                self.assertEqual(second['termination'], 'not-run-after-infrastructure-error')
                self.assertIsNone(first['score'])
                self.assertIsNone(second['score'])
                self.assertEqual(first['selected_denominator'], 1)
                self.assertTrue((root / 'given-snapshot/0001/response.json').is_file())

    def test_bad_finals_stay_final_and_overbudget_lookup_keeps_missing_answer(self):
        provider = Provider([response(1, 'graph_submit', {'nodes': ['x' * 10000]}),
                             response(2, 'graph_find', {'unexpected': 'malformed lookup'}),
                             response(3, 'graph_find', {'query': 'Gradient'})])
        with tempfile.TemporaryDirectory() as folder:
            first, second = self.run_at(Path(folder) / 'run', provider)['results']
            self.assertEqual(first['termination'], 'first-final')
            self.assertEqual(first['score']['submitted'], 1)
            self.assertEqual(first['score']['points'], 0)
            self.assertEqual(second['termination'], 'lookup-budget-exhausted-no-final')
            self.assertEqual(second['score']['submitted'], 0)
            self.assertEqual(second['score']['max_points'], 1)
            obs = json.loads(provider.requests[2]['input'][-1]['output'])
            self.assertEqual(obs['kind'], 'invalid-lookup')
            self.assertEqual(len(provider.requests), 3)


if __name__ == '__main__':
    unittest.main()
