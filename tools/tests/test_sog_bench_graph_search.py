"""Controlled search-tool tests; no API calls, model measurements or arbitrary Lean."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_graph_search as search


class GraphSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.item = search.admitted('sogb-g007')

    def exercise(self, *calls, max_lookups=8):
        observed, events = [], []
        source = io.BytesIO(b''.join(call if isinstance(call, bytes) else search.line(call) for call in calls))
        report = search.run_trial(self.item, max_lookups, source, observed.append, events.append)
        return report, observed, events

    def test_prompt_contains_no_snapshot_or_answer_but_lookups_return_local_evidence(self):
        target = self.item['targets'][0]
        _, (prompt, matches, inspected, unknown), _ = self.exercise(
            {'action': 'find', 'query': 'gradient pairing'}, {'action': 'inspect', 'id': target},
            {'action': 'inspect', 'id': '../../operator-task.json'})
        for key in ('context', 'answer', 'edges', 'graph_sha256', 'binding_sha256', 'statement_profiles'):
            self.assertNotIn(key, prompt)
        self.assertEqual(prompt['id'], self.item['id'])
        self.assertEqual(len(matches['matches']), 1)
        self.assertEqual(inspected['parents'], sorted(p for c, p in self.item['context']['edges'] if c == target))
        self.assertEqual(inspected['statement_constants'], self.item['context']['statement_profiles'][target])
        self.assertEqual(unknown, {'kind': 'unknown-node', 'remaining_lookups': 5})
        self.assertNotIn('answer', inspected)

    def test_unreviewed_or_wrong_kind_tasks_are_not_available(self):
        with (patch.object(search.bench.curriculum, 'graph_items', return_value=[self.item]),
              patch.object(search.review, 'summary', return_value={'items': {'sogb-g007': {'editorial': 'stale'}}})):
            with self.assertRaisesRegex(ValueError, 'currently admitted'):
                search.admitted('sogb-g007')
            with self.assertRaisesRegex(ValueError, 'currently admitted'):
                search.admitted('sogb-g999')
        imports = {**self.item, 'context': {**self.item['context'], 'kind': 'source-scanned-module-imports'}}
        with patch.object(search.bench.curriculum, 'graph_items', return_value=[imports]):
            with self.assertRaisesRegex(ValueError, 'compiled-body'):
                search.admitted('sogb-g007')

    def test_real_multihop_and_statement_filter_using_only_tool_outputs(self):
        prompt = search.prompt(self.item, 8)
        observations = {}
        queue = list(prompt['targets'])
        calls = []
        while queue:
            node = queue.pop()
            if node in observations:
                continue
            call = {'action': 'inspect', 'id': node}
            calls.append(call)
            obs = search.lookup(self.item, call)
            observations[node] = obs
            queue.extend(obs['parents'])
        def reaches(node):
            return node == prompt['remove'] or any(reaches(parent) for parent in observations[node]['parents'])
        answer = {'nodes': [node for node in prompt['targets'] if reaches(node) and
                            set(prompt['required_statement_constants']) <= set(observations[node]['statement_constants'])],
                  'entails_mathematical_necessity': False}
        self.assertGreater(len(calls), len(prompt['targets']))
        final = {'action': 'submit', 'answer': answer}
        result, stream, _ = self.exercise(*calls, final)
        self.assertEqual(result['score']['points'], 1)
        self.assertEqual(stream[-1], {'kind': 'final-recorded'})
        self.assertFalse(result['model_measurement'])
        result, _, _ = self.exercise({**final, 'answer': {**answer, 'entails_mathematical_necessity': True}}, final)
        self.assertEqual(result['score']['points'], 0)

    def test_invalid_request_is_bounded_and_does_not_reset_selection(self):
        result, observations, events = self.exercise(
            b'{"action":"find","query":"Convex","query":"Gradient"}\n', b'\xff\n',
            {'action': 'find', 'query': 'kernel'}, {'action': 'submit', 'answer': self.item['answer']}, max_lookups=2)
        self.assertEqual([obs['kind'] for obs in observations[1:]],
                         ['invalid-lookup', 'invalid-lookup', 'lookup-budget-exhausted-no-final'])
        self.assertEqual(len(events), 3)
        self.assertEqual(result['score']['submitted'], 0)
        self.assertEqual(result['score']['max_points'], 1)
        result, _, events = self.exercise(b'x' * (search.MAX_REQUEST + 999))
        self.assertEqual(result['termination'], 'oversized-request-no-final')
        self.assertTrue(events[0]['request_is_oversize_prefix'])
        result, _, _ = self.exercise({'action': 'submit', 'answer': self.item['answer'], 'other': 1},
                                     {'action': 'submit', 'answer': self.item['answer']})
        self.assertEqual(result['score']['submitted'], 1)
        self.assertFalse(result['score']['results'][0]['valid_schema'])
        self.assertEqual(result['score']['points'], 0)

    def test_exact_trace_replays_and_existing_output_cannot_be_reused(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'trial'
            request = search.line({'action': 'inspect', 'id': self.item['targets'][0]})
            report = search.archive(self.item, 8, path, io.BytesIO(request), lambda _: None)
            self.assertEqual(report, search.replay(path, self.item))
            self.assertEqual(report['termination'], 'eof-no-final')
            with self.assertRaises(FileExistsError):
                search.archive(self.item, 8, path, io.BytesIO(request), lambda _: None)
            event_path = path / 'actions.jsonl'
            event = json.loads(event_path.read_bytes())
            event['observation']['parents'] = ['not-a-compiled-parent']
            event_path.write_bytes(search.line(event))
            with self.assertRaisesRegex(ValueError, 'differs from exact replay'):
                search.replay(path, self.item)


if __name__ == '__main__':
    unittest.main()
