"""Exercise the real reviewed slice and the projection's fail-closed boundary."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sog_bench_lean_retrieval as retrieval


class LeanGraphRetrievalTests(unittest.TestCase):
    def stage(self, core: dict) -> tuple[dict, Path, dict]:
        bench = retrieval.bench
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        stage = Path(tmp.name)
        modules = retrieval.runtime.local_imports(core['imports'])
        files = {}
        for module in modules:
            source = module.replace('.', '/') + '.lean'
            name = 'project/' + source
            path = stage / name
            path.parent.mkdir(parents=True, exist_ok=True)
            data = (retrieval.runtime.ROOT / source).read_bytes()
            path.write_bytes(data)
            files[name] = bench.sha(data)
        desc = {'id': core['id'], 'binding_sha256': core['binding_sha256'],
                'owned_ancestor_modules': modules, 'target_module_absent': True,
                'oracle_included': False, 'files': files}
        (stage / 'stage.json').write_bytes(bench.encoded(desc))
        return {'id': core['id'], 'binding_sha256': core['binding_sha256'],
                'paths': {'stage': str(stage)}}, stage, desc

    def test_projected_real_g010_uses_imported_support_but_not_its_answer_owner(self):
        bench = retrieval.bench
        core = next(c for c in bench.materialize() if c['id'] == 'sogb-046')
        provenance = {'tools': retrieval.TOOLS, 'retrieval_profile': retrieval.RETRIEVAL,
                      'graph_task_id': 'sogb-g010', 'max_graph_lookups': 4}
        manifest, stage, _ = self.stage(core)
        graph, receipt = retrieval.prepare({**manifest, 'provenance': provenance})
        self.assertEqual(set(graph), {'nodes', 'node_labels', 'edges', 'statement_profiles'})
        self.assertEqual(len(graph['nodes']), 4)
        self.assertEqual(len(graph['edges']), 2)
        self.assertNotIn(core['declaration'], str(graph))
        self.assertNotIn('quadratic_gap_lower_bound', str(graph))
        self.assertEqual(receipt['stage_sha256'], bench.sha((stage / 'stage.json').read_bytes()))
        self.assertEqual(receipt['projection_sha256'], bench.sha(bench.encoded(graph)))
        query = retrieval.lookup(graph, {'action': 'find', 'query': 'eigenmode'}, 42)
        self.assertEqual(len(query['matches']), 1)
        node = query['matches'][0]['id']
        self.assertTrue(node.endswith('.quadratic_eigenmode'))
        read = retrieval.lookup(graph, {'action': 'inspect', 'id': node}, 120)
        self.assertTrue(read['parents'][0].endswith('.quadratic_gradient_iterate'))
        self.assertEqual(retrieval.lookup(graph, {'action': 'inspect', 'id': core['declaration']}, 200),
                         {'kind': 'unknown-node'})
        self.assertEqual(retrieval.lookup(graph, {'action': 'find', 'query': 'eigenmode'}, 9000),
                         {'kind': 'invalid-lookup'})

    def test_self_consistent_old_stage_is_rejected_before_retrieval(self):
        bench = retrieval.bench
        core = next(c for c in bench.materialize() if c['id'] == 'sogb-046')
        manifest, stage, desc = self.stage(core)
        name = next(iter(desc['files']))
        raw = (stage / name).read_bytes() + b'\n-- differently versioned ancestor\n'
        (stage / name).write_bytes(raw)
        desc['files'][name] = bench.sha(raw)
        (stage / 'stage.json').write_bytes(bench.encoded(desc))
        with self.assertRaisesRegex(ValueError, 'Staged Lean source differs'):
            retrieval.checked_stage(manifest, core)

    def test_unapproved_inputs_cannot_enlarge_projection(self):
        source = 'AutoSamplingTheory/TechnicalLemmas/Owner.lean'
        core = {'family': 'family-a', 'split': 'public-dev', 'imports': [], 'declaration': 'answer',
                'source_file': source}
        item = {'family': 'family-b', 'split': 'public-dev',
                'context': {'kind': retrieval.search.KIND, 'nodes': ['node'], 'source_sha256_lf': {source: 'hash'}}}
        with self.assertRaisesRegex(ValueError, 'same-family'):
            retrieval.project(core, item, {})
        with self.assertRaisesRegex(ValueError, 'every selected declaration'):
            retrieval.project(core, {**item, 'family': core['family']}, {})
        with patch.object(retrieval.runtime, 'local_imports',
                          return_value=['AutoSamplingTheory.TechnicalLemmas.Owner']):
            with self.assertRaisesRegex(ValueError, 'answer owner'):
                retrieval.project(core, {**item, 'family': core['family']}, {'node': source})

    def test_explicit_provenance_is_bounded(self):
        p = {'tools': retrieval.TOOLS, 'retrieval_profile': retrieval.RETRIEVAL,
             'graph_task_id': 'sogb-g010', 'max_graph_lookups': 4}
        retrieval.validate(p)
        for invalid in ({'max_graph_lookups': True}, {'max_graph_lookups': 17},
                        {'graph_task_id': '../restricted'}, {'tools': ['lean_workspace', 'shell']}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                retrieval.validate({**p, **invalid})
