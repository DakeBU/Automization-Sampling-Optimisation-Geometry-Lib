"""Compiler-snapshot scope and tamper checks; no model scores or untrusted code."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'website/scripts')]
import sog_bench as bench
import sog_bench_compiled_graph as compiled
import sog_bench_reader as reader


class CompiledGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cache=patch.object(bench.astis_site,'_SOURCE_BY_NAME',
            {d.full_name:d for d in bench.astis_site.scan_project_sources()[1]})
        cls.cache.start()
        cls.addClassCleanup(cls.cache.stop)
        cls.spec,cls.core,cls.data=compiled.recorded()
        cls.flow_spec,cls.flow_core,cls.flow_data=compiled.recorded(compiled.FLOW_SPEC,compiled.FLOW_SNAPSHOT)

    def test_selected_compiler_evidence_is_owned_bounded_and_not_full_closure(self):
        self.assertEqual(len(self.data['rows']),15)
        self.assertEqual(len(self.data['provenance']['source_sha256_lf']),6)
        self.assertEqual(self.data['provenance']['core_binding_sha256'],self.core['binding_sha256'])
        self.assertEqual(self.data['graph']['kind'],compiled.KIND)
        self.assertIn('private auxiliaries',self.data['graph']['scope'])
        self.assertIn('No path in an induced slice',self.data['graph']['truth_boundary'])
        self.assertTrue(all(set(row['axioms'])<=compiled.AXIOMS for row in self.data['rows']))
        probe=compiled.probe_source(self.spec)
        self.assertIn('body.getUsedConstants',probe)
        self.assertIn('Lean.collectAxioms',probe)
        self.assertIn('info.type.getUsedConstants',probe)
        self.assertIn('let .thmInfo',probe)
        self.assertNotIn('sorry',probe)
        self.assertNotIn(self.core['lean_task'],probe)

    def test_task_answers_are_computed_from_actual_selected_edges(self):
        rows=compiled.items()
        self.assertEqual([r['id'] for r in rows],['sogb-g004','sogb-g005'])
        expected=[n for n in self.spec['nodes'] if n.endswith('.measurable_quadraticCost')]
        self.assertEqual(rows[0]['answer']['nodes'],expected)
        self.assertEqual(rows[1]['answer']['nodes'],[self.core['declaration']])
        for row in rows:
            self.assertEqual(row['core_id'],self.core['id'])
            self.assertEqual(row['family'],self.core['family'])
            self.assertEqual(row['library_domains'],self.core['library_domains'])
            self.assertIn(row['level'],{'L1','L2'})  # L4 source does not make graph reading L4.
            self.assertFalse(row['answer']['entails_mathematical_necessity'])
            self.assertNotIn('rows',row['context'])
        prompts=bench.curriculum.graph_prompts(rows)
        self.assertTrue(all('answer' not in row and 'reference_status' not in row for row in prompts))
        self.assertEqual(bench.curriculum.grade_graph(rows,[
            {'id':r['id'],'binding_sha256':r['binding_sha256'],'attempt':1,'answer':r['answer']} for r in rows])['points'],2)

    def test_unknown_duplicate_cyclic_and_unapproved_axiom_rows_fail(self):
        variants=[]
        for parents in ([self.data['rows'][0]['id']],['unknown'],[self.data['rows'][1]['id']]*2):
            rows=deepcopy(self.data['rows']);rows[0]['body_parents']=parents;variants.append(rows)
        for axioms in (['sorryAx'],[True],['propext','propext']):
            rows=deepcopy(self.data['rows']);rows[0]['axioms']=axioms;variants.append(rows)
        for profile in (['unknown'],[True],['HasDerivAt','HasDerivAt']):
            rows=deepcopy(self.data['rows']);rows[0]['statement_constants']=profile;variants.append(rows)
        rows=deepcopy(self.data['rows'])
        rows[0]['body_parents']=[rows[1]['id']];rows[1]['body_parents']=[rows[0]['id']]
        variants += [rows,self.data['rows'][:-1],self.data['rows'][:-1]+self.data['rows'][:1]]
        for rows in variants:
            with self.assertRaises(ValueError):
                compiled.canonical_rows(rows,self.spec)

    def test_source_pins_generator_or_core_changes_stale_the_record(self):
        for key in ('context_sha256','core_binding_sha256','generator_sha256_lf',
                    'mathlib_manifest_sha256_lf','toolchain','lakefile_sha256_lf'):
            changed=deepcopy(self.data['provenance']);changed[key]='changed'
            with patch.object(compiled,'inputs',return_value=(self.spec,self.core,changed)):
                with self.assertRaises(ValueError):
                    compiled.recorded()
        original=bench.text_hash
        path=self.spec['source_files'][0]
        with patch.object(bench,'text_hash',side_effect=lambda p:'changed' if p.relative_to(ROOT).as_posix()==path else original(p)):
            with self.assertRaises(ValueError):
                compiled.recorded()

    def test_unrelated_live_proofs_are_not_snapshot_inputs(self):
        original=bench.text_hash
        with patch.object(bench,'text_hash',side_effect=lambda p:'changed' if p.name=='SubgradientMethod.lean' else original(p)):
            self.assertEqual(compiled.recorded()[2],self.data)

    def test_flow_profiles_and_body_paths_are_distinct_compiler_evidence(self):
        rows={r['id']:r for r in self.flow_data['rows']}
        first=next(n for n in rows if n.endswith('.firstOrder_lower_bound_of_strongConvexOn'))
        inner=next(n for n in rows if n.endswith('.gradient_inner_lower_bound_of_strongConvexOn'))
        limit=next(n for n in rows if n.endswith('.firstOrder_geodesicConvexity'))
        flow=self.flow_core['declaration']
        midpoint=next(n for n in rows if n.endswith('.centered_quadratic_lower_bound_of_strongConvexOn_minimizer'))
        self.assertEqual(rows[flow]['body_parents'],[first])
        self.assertEqual(rows[first]['body_parents'],[limit])
        self.assertEqual(rows[midpoint]['body_parents'],[])
        self.assertEqual(rows[first]['statement_constants'],['CompleteSpace','HasGradientAt'])
        self.assertIn('Differentiable',rows[flow]['statement_constants'])
        self.assertNotIn('HasGradientAt',rows[flow]['statement_constants'])
        tasks=compiled.items(compiled.FLOW_SPEC,compiled.FLOW_SNAPSHOT)
        self.assertEqual(tasks[0]['answer']['nodes'],sorted([flow,inner]))
        self.assertEqual(tasks[1]['answer']['nodes'],sorted([first,inner]))
        self.assertIn('not proof of necessary hypotheses',tasks[1]['question'])
        self.assertEqual(tasks[1]['required_statement_constants'],['CompleteSpace','HasGradientAt'])
        self.assertEqual(tasks[1]['family'],self.flow_core['family'])

    def test_all_selected_local_import_branches_are_bound_not_just_the_anchor(self):
        dependency='AutoSamplingTheory/TechnicalLemmas/Geometry/LogConcavity.lean'
        self.assertIn(dependency,self.flow_data['provenance']['local_import_closure_sha256_lf'])
        original=bench.text_hash
        with patch.object(bench,'text_hash',side_effect=lambda p:'changed' if p.relative_to(ROOT).as_posix()==dependency else original(p)):
            with self.assertRaises(ValueError):
                compiled.recorded(compiled.FLOW_SPEC,compiled.FLOW_SNAPSHOT)

    def test_profile_selectors_cannot_inject_or_invent_lean_constants(self):
        for required in (['unknown'],['CompleteSpace; import Anything']):
            changed=deepcopy(self.flow_spec)
            changed['tasks'][1]['required_statement_constants']=required
            with self.assertRaises(ValueError):
                compiled.probe_source(changed)

    def test_unsafe_or_unowned_selectors_are_rejected_before_compiler_execution(self):
        variants=[]
        for path in ('outer_repos/source.lean','../source.lean','research-wiki/retrieval-index/atlas-v1/data.jsonl'):
            spec=deepcopy(self.spec);spec['source_files']=[path];variants.append(spec)
        spec=deepcopy(self.spec);spec['nodes']={'malicious; import Anything':'bad'};variants.append(spec)
        spec=deepcopy(self.spec);spec['core_id']='unknown';variants.append(spec)
        spec=deepcopy(self.spec);spec['source_files']*=2;variants.append(spec)
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'spec.json'
            for spec in variants:
                path.write_bytes(bench.encoded(spec))
                with patch.object(compiled,'SPEC',path),patch('subprocess.run',side_effect=AssertionError('No execution')):
                    with self.assertRaises(ValueError):
                        compiled.inputs()

    def test_resigned_forged_edges_require_real_replay_not_merely_hash_validation(self):
        rows=deepcopy(self.data['rows'])
        cost=next(r for r in rows if r['id'].endswith('.measurable_quadraticCost'))
        mass=next(r['id'] for r in rows if r['id'].endswith('.isProbabilityMeasure_of_isCoupling_left'))
        cost['body_parents']=[mass]  # A known, acyclic but deliberately false edge.
        forged=compiled.snapshot(rows,self.spec,self.data['provenance'])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'snapshot.json';path.write_bytes(bench.encoded(forged))
            with patch.object(compiled,'SNAPSHOT',path):
                self.assertEqual(compiled.recorded()[2],forged)  # Not a signed/fresh compiler attestation.
                with patch.object(compiled,'replay',return_value=self.data),patch.object(sys,'argv',['compiled-graph','check']):
                    with self.assertRaises(ValueError):
                        compiled.main()

    def test_forged_statement_profiles_also_require_real_replay(self):
        rows=deepcopy(self.data['rows'])
        rows[0]['statement_constants']=['HasGradientAt']
        forged=compiled.snapshot(rows,self.spec,self.data['provenance'])
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'snapshot.json';path.write_bytes(bench.encoded(forged))
            with patch.object(compiled,'SNAPSHOT',path):
                self.assertEqual(compiled.recorded()[2],forged)
                with patch.object(compiled,'replay',return_value=self.data),patch.object(sys,'argv',['compiled-graph','check','--slice','transport']):
                    with self.assertRaises(ValueError):
                        compiled.main()

    def test_compiled_figure_uses_readable_labels_and_distinct_edge_semantics(self):
        for row in compiled.items():
            graph=row['context'];figure=reader.import_figure(graph)
            self.assertEqual(figure.count('<rect '),len(graph['nodes']))
            self.assertIn('Solid arrows',figure)
            self.assertNotIn('stroke-dasharray',figure)
            self.assertIn('not full closure',figure)
            for label in graph['node_labels'].values():
                self.assertIn(label,figure)

    def test_unreviewed_graph_variants_are_not_exported_as_admitted_gold(self):
        graphs=bench.curriculum.graph_items()
        draft=deepcopy(graphs[-1]);draft['id']='sogb-g999'
        draft['question']+=' Unreviewed software fixture, not a new dataset task.'
        with tempfile.TemporaryDirectory() as tmp,patch.object(bench.curriculum,'graph_items',return_value=graphs+[draft]):
            out=Path(tmp)/'export';bench.export(out)
            questions=[json.loads(line) for line in (out/'reviewed-graph-questions.jsonl').read_text(encoding='utf-8').splitlines()]
            refs=[json.loads(line) for line in (out/'reviewed-graph-reference.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertCountEqual([row['id'] for row in questions], [row['id'] for row in graphs])
            self.assertCountEqual([row['id'] for row in refs], [row['id'] for row in graphs])
            self.assertNotIn('sogb-g999',{r['id'] for r in questions})
            self.assertTrue(all('answer' not in r for r in questions))


if __name__=='__main__':
    unittest.main()
