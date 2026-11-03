"""Paired identities, exact reference extraction, no-answer exports and reader contracts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench as bench
import sog_bench_reader as reader
import sog_bench_graph_review as graph_review


class BenchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_patch = patch.object(bench.astis_site, '_SOURCE_BY_NAME',
            {d.full_name: d for d in bench.astis_site.scan_project_sources()[1]})
        cls.source_patch.start()
        cls.addClassCleanup(cls.source_patch.stop)
        cls.cores = bench.materialize()

    def test_available_views_share_core_family_and_split_without_fake_pairs(self):
        prompts = bench.prompts(self.cores)
        self.assertEqual(len(self.cores), 24)
        self.assertEqual(len(prompts), 35)
        for core in self.cores:
            views = [r for r in prompts if r['id'] == core['id']]
            self.assertEqual({r['track'] for r in views}, set(core['track_levels']))
            for row in views:
                self.assertEqual(row['family'], core['family'])
                self.assertEqual(row['binding_sha256'], core['binding_sha256'])
                self.assertEqual(row['split'], 'public-dev')

    def test_prompt_export_has_no_answers_rubrics_or_reference_proofs(self):
        allowed = {'id', 'family', 'domain', 'library_domains', 'skills', 'title', 'split', 'assumptions', 'binding_sha256', 'track', 'level', 'question'}
        for row in bench.prompts(self.cores):
            self.assertEqual(set(row), allowed)
            self.assertNotIn(':= by\n  intro', row['question'])
        self.assertTrue(all('-- Replace this comment' in r['question']
                            for r in bench.prompts(self.cores) if r['track'] == 'lean'))

    def test_extracts_existing_proof_not_target_import_or_wrapper(self):
        for core in self.cores:
            if not bench.has_lean(core):
                self.assertEqual(core['lean_reference'], '')
                self.assertNotIn('lean', core['track_levels'])
                continue
            reference = core['lean_reference']
            target_module = core['source_file'].removesuffix('.lean').replace('/', '.')
            self.assertNotIn('import ' + target_module + '\n', reference)
            self.assertRegex(reference, r'\bexample\s')
            self.assertNotIn('end AutoSamplingTheory', reference.split('\nexample', 1)[1])
            self.assertNotIn(core['declaration'], reference)
            self.assertNotIn('sorry', reference)
            self.assertEqual(core['source_sha256_lf'], bench.text_hash(ROOT / core['source_file']))
        self.assertIn('ENNReal.tsum_comm', self.cores[0]['lean_reference'])
        self.assertIn('by_cases hq', self.cores[1]['lean_reference'])
        self.assertIn('hV.2', self.cores[2]['lean_reference'])

    def test_binding_changes_with_prose_or_context(self):
        for key in ('question', 'context', 'boundary'):
            changed = deepcopy(bench.load())
            changed['cores'][0][key] += '\nChanged contract.'
            rows = bench.materialize(changed)
            self.assertNotEqual(rows[0]['binding_sha256'], self.cores[0]['binding_sha256'])

    def test_export_determinism_license_and_portable_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'export'
            bench.export(output, self.cores)
            before = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            bench.export(output, self.cores)
            self.assertEqual(before, {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()})
            manifest = json.loads((output / 'manifest.json').read_text())
            self.assertEqual(manifest['qa_views'], 35)
            self.assertEqual(manifest['graph_tasks'], 7)
            self.assertEqual(len(manifest['graph_evidence_kinds']),2)
            self.assertTrue((output/'compiled-transport-graph.json').is_file())
            self.assertTrue((output/'compiled-flow-graph.json').is_file())
            self.assertIn('content-bound', manifest['independent_semantic_review'])
            self.assertEqual(manifest['editorial_accepted_graph_tasks'], graph_review.summary(bench.curriculum.graph_items())['accepted_tasks'])
            self.assertIn('human-attested', manifest['prose_scoring'])
            self.assertTrue((output/'EVALUATION.md').is_file())
            self.assertTrue((output/'examples/prose-run.json').is_file())
            guide = (output/'README.md').read_text(encoding='utf-8')
            self.assertNotIn('](reviews/', guide)
            self.assertIn('/blob/main/benchmarks/samplingoptimisationgeometrybench/reviews/formal-3/README.md', guide)
            self.assertFalse((output/'reviews').exists())  # Historical rejected text is audit-only.
            for name, digest in manifest['files'].items():
                self.assertEqual(digest, bench.sha((output / name).read_bytes()))
            for name in bench.project_licensing.LICENSE_FILES:
                self.assertEqual((output / name).read_bytes(), (ROOT / name).read_bytes())
            one, two = Path(tmp) / 'one.zip', Path(tmp) / 'two.zip'
            bench.archive_bytes(output, one)
            bench.archive_bytes(output, two)
            self.assertEqual(one.read_bytes(), two.read_bytes())
            with zipfile.ZipFile(one) as archive:
                self.assertIn('questions.jsonl', archive.namelist())
                self.assertTrue(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in archive.namelist()))

    def test_absent_and_stale_receipt_do_not_claim_compilation(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(bench, 'RECEIPT', Path(tmp) / 'receipt.json'):
            self.assertFalse(bench.receipt_current(self.cores))

    def test_export_does_not_overwrite_or_bundle_unrelated_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            unrelated = output / 'README.md'
            unrelated.write_text('User work', encoding='utf-8')
            with self.assertRaises(ValueError):
                bench.export(output, self.cores)
            self.assertEqual(unrelated.read_text(), 'User work')

    def test_receipt_requires_exact_source_and_qa_bindings(self):
        aligned = [c for c in self.cores if bench.has_lean(c)]
        receipt = {'schema_version': 1, 'passed': True, 'environment_sha256': 'environment',
                   'environment_scope': 'selected-source-import-closure',
                   'compiler_version': 'Lean (version 4.33.0, test fixture)',
                   'bindings': {c['id']: c['binding_sha256'] for c in aligned},
                   'reference_sha256': {c['id']: bench.sha(c['lean_reference'].encode()) for c in aligned},
                   'commands': [{'returncode': 0}] * (len(aligned) + 2)}
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(bench, 'RECEIPT', Path(tmp) / 'receipt.json'), \
             patch.object(bench, 'environment_digest', return_value='environment'):
            bench.RECEIPT.write_bytes(bench.encoded(receipt))
            self.assertTrue(bench.receipt_current(self.cores))
            receipt['bindings']['sogb-001'] = 'old-question'
            bench.RECEIPT.write_bytes(bench.encoded(receipt))
            self.assertFalse(bench.receipt_current(self.cores))
            bench.RECEIPT.write_text('{"passed": true}', encoding='utf-8')
            self.assertFalse(bench.receipt_current(self.cores))

    def test_review_and_split_cannot_be_promoted_by_editing_badge(self):
        for key, value in (('split', 'heldout'), ('review_status', 'verified')):
            data = bench.load()
            data[key] = value
            with patch.object(bench.Path, 'read_text', return_value=json.dumps(data)):
                with self.assertRaises(ValueError):
                    bench.load()

    def test_reader_is_layered_and_does_not_cross_promote_projects(self):
        text = reader.home(self.cores)
        self.assertIn('natural-language/index.html', text)
        self.assertIn('lean/index.html', text)
        self.assertIn('content-bound AI editorial acceptance', text)
        self.assertNotIn('Quantum', text)
        self.assertIn('evaluation/index.html', text)
        assessment=reader.evaluation_page()
        self.assertIn('not automatically verified mathematics',assessment)
        self.assertNotIn('<details open',assessment)
        for core in self.cores:
            rendered = reader.core_page(core, False, {'decl:' + core['declaration']})
            self.assertIn('Reference mathematical proof', rendered)
            if bench.has_lean(core):
                self.assertIn('Reference Lean and explanation', rendered)
                self.assertIn('data-lean-copy-status', rendered)
                self.assertIn('No current trusted-reference compiler receipt', rendered)
            else:
                self.assertIn('Lean view: not yet aligned', rendered)
                self.assertEqual('data-lean-copy-status' in rendered, bool(core.get('support_source_view')))
            self.assertNotIn('<details open', rendered)
            self.assertIn('focus=decl%3A', rendered)
            fallback = reader.core_page(core, False, set())
            self.assertIn('focus=module%3A', fallback)
            self.assertIn('declaration not yet indexed', fallback)

    def test_display_identity_linebreaks_preserve_source_and_avoid_nested_tex(self):
        source = r'Proof \[a=b,\qquad c=d\] done.'
        rendered = reader.prose(source)
        self.assertIn(r'\begin{gathered}a=b,\\ c=d\end{gathered}', rendered)
        self.assertEqual(source, r'Proof \[a=b,\qquad c=d\] done.')
        for nested in (r'\[\text{a,\qquad b}=c\]', r'\[\begin{aligned}a&=b,\qquad c&=d\end{aligned}\]'):
            self.assertNotIn(r'\begin{gathered}', reader.prose(nested))

    def test_seven_domain_five_level_matrix_does_not_invent_coverage(self):
        graphs = bench.curriculum.graph_items()
        coverage = bench.curriculum.coverage(self.cores, graphs)
        self.assertEqual(len(coverage['cells']), 35)
        self.assertEqual(coverage['unique_mathematical_cores'], 24)
        self.assertTrue(all(c['gap'] for c in coverage['cells'] if c['level'] == 'L5'))
        self.assertTrue(all(c['independently_reviewed'] == 0 for c in coverage['cells']))
        self.assertEqual(coverage['mathematical_editorial_status'], 'pending')
        current = bench.coverage(self.cores, graphs)
        self.assertEqual(current['editorial_accepted_mathematical_cores'], 24)
        self.assertEqual(current['mathematical_editorial_status'], 'complete-for-current-cores')
        self.assertEqual(current['graph_editorial_status'], graph_review.summary(graphs)['editorial_status'])
        self.assertEqual({d for c in self.cores for d in c['library_domains']}, set(bench.curriculum.curriculum()['domains']))
        self.assertNotIn('OpenAI', json.dumps(coverage))
        for domain in bench.curriculum.curriculum()['domains']:
            self.assertTrue(any(domain in c['library_domains'] and c['track_levels'].get('natural-language') == 'L1' for c in self.cores))
            self.assertTrue(any(domain in c['library_domains'] and bench.has_lean(c) for c in self.cores))

    def test_compiler_scope_tracks_real_imports_and_pins_not_unrelated_modules(self):
        selected = [c for c in self.cores if c['id'] == 'sogb-016']
        actual_hash = bench.text_hash
        reads = set()
        def tracked_hash(path):
            reads.add(path.relative_to(ROOT).as_posix())
            return actual_hash(path)
        with patch.object(bench, 'text_hash', side_effect=tracked_hash):
            before = bench.environment_digest(selected)
        self.assertIn('AutoSamplingTheory/TechnicalLemmas/Geometry/SphereRayleigh.lean', reads)
        self.assertIn('AutoSamplingTheory/TechnicalLemmas/Geometry/SphereGradient.lean', reads)
        self.assertNotIn('AutoSamplingTheory/TechnicalLemmas/Analysis/SubgradientMethod.lean', reads)
        for changed in ('AutoSamplingTheory/TechnicalLemmas/Geometry/SphereGradient.lean',
                        'lean-toolchain', 'lake-manifest.json', 'lakefile.lean'):
            def changed_hash(path):
                return 'changed' if path.relative_to(ROOT).as_posix() == changed else actual_hash(path)
            with patch.object(bench, 'text_hash', side_effect=changed_hash):
                self.assertNotEqual(before, bench.environment_digest(selected))

    def test_transport_join_is_actual_multi_module_proof_not_exact_triangle_shortcut(self):
        core=next(c for c in self.cores if c['id']=='sogb-018')
        self.assertEqual(core['track_levels'],{'natural-language':'L4','lean':'L4'})
        self.assertIn('StandardBorelSpace E',core['context'])
        self.assertNotIn('FiniteDimensional',core['context'])
        self.assertEqual(len(core['dependencies']['astis']),8)
        for name in core['dependencies']['astis']:
            self.assertIn(name.rsplit('.',1)[1],core['lean_reference'])
        self.assertNotIn('WassersteinTriangleExact',core['lean_reference'])
        self.assertIn('independent product',core['steps'][-1])
        self.assertIn('not the true Wasserstein inequality',core['steps'][-1])
        self.assertIn('ancestor proofs',core['boundary'])

    def test_subgradient_source_view_preserves_notices_without_inventing_a_lean_task(self):
        by_id={c['id']:c for c in self.cores}
        norm,energy=by_id['sogb-019'],by_id['sogb-020']
        self.assertEqual(norm['family'],energy['family'])
        self.assertEqual(energy['track_levels'],{'natural-language':'L3'})
        self.assertEqual(energy['lean_reference'],'')
        self.assertEqual(energy['support_lean_source'],(ROOT/energy['source_file']).read_text(encoding='utf-8'))
        for credit in ('Hongjia Chen','Chenyi Li','Wanyi He','Zaiwen Wen','Apache 2.0'):
            self.assertIn(credit,norm['lean_reference'])
            self.assertIn(credit,energy['support_lean_source'])
        question=next(r for r in bench.prompts(self.cores) if r['id']==energy['id'])
        self.assertNotIn('support_lean_source',question)
        self.assertNotIn('theorem exists_gap_le',question['question'])
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)
            bench.export(output,self.cores)
            self.assertEqual((output/'lean/sogb-020-support.lean').read_text(encoding='utf-8'),energy['support_lean_source'])
            self.assertFalse((output/'lean/sogb-020-reference.lean').exists())
        self.assertIn('not an aligned QA task',reader.core_page(energy,False))
        self.assertNotIn('Trusted reference compilation recorded',reader.core_page(energy,True))

    def test_new_pairs_have_actual_norm_and_conditional_kernel_targets(self):
        norm,heat=(next(c for c in self.cores if c['id']==identity) for identity in ('sogb-019','sogb-021'))
        self.assertIn("hs (x + g)",norm['lean_reference'])
        self.assertIn('by_cases hg',norm['lean_reference'])
        self.assertIn('fst_compProd_condDistrib_snd_eq_self',heat['lean_reference'])
        self.assertIn('noncomputable def heatBathSnd',heat['context'])
        self.assertNotIn('heatBathSnd_invariant',heat['lean_task'])
        self.assertNotIn('IsProbabilityMeasure',heat['lean_task'])
        self.assertNotIn('StandardBorelSpace α',heat['lean_task'])

    def test_selected_curve_target_keeps_genuine_derivative_and_external_geometry_boundary(self):
        core=next(c for c in self.cores if c['id']=='sogb-022')
        self.assertIn('def IsAlphaGeodesicallyConvex',core['context'])
        self.assertIn('HasDerivAt',core['lean_task'])
        self.assertIn('MetricSpace M',core['lean_task'])
        self.assertNotIn('InnerProductSpace',core['lean_task'])
        self.assertIn('div_le_iff₀',core['lean_reference'])
        self.assertIn('le_of_tendsto_of_tendsto',core['lean_reference'])
        self.assertIn('not certified geometric data',core['boundary'])

    def test_gradient_flow_rate_is_a_real_trajectory_join_not_an_assumed_gap_bound(self):
        core=next(c for c in self.cores if c['id']=='sogb-023')
        self.assertIn('HasDerivWithinAt X (-gradient',core['lean_task'])
        self.assertIn('ContinuousOn X (Icc 0 T)',core['lean_task'])
        self.assertIn('∀ t ∈ Ioc 0 T',core['lean_task'])
        self.assertIn('if α = 0 then',core['lean_task'])
        self.assertIn('[CompleteSpace E]',core['context'])
        self.assertNotIn('FiniteDimensional',core['lean_task'])
        self.assertNotIn('LipschitzWith',core['lean_task'])
        self.assertEqual(core['lean_reference'].count('le_gronwallBound_of_liminf_deriv_right_le'),2)
        self.assertIn('hmono',core['lean_reference'])
        self.assertIn('firstOrder_lower_bound_of_strongConvexOn',core['lean_reference'])
        self.assertEqual(core['family'],next(c for c in self.cores if c['id']=='sogb-022')['family'])

    def test_uncountable_event_audit_does_not_claim_a_formal_counterexample_or_failed_averaging(self):
        core=next(c for c in self.cores if c['id']=='sogb-024')
        self.assertFalse(bench.has_lean(core))
        self.assertEqual(core['track_levels'],{'natural-language':'L3'})
        self.assertIn('∀ᵐ x ∂μ, ∀ s',core['support_lean_source'])
        self.assertIn('Both output measures are μ',core['steps'][4])
        self.assertIn('not countably generated',core['steps'][5])
        self.assertIn('not a formal proof of this QA',core['boundary'])
        self.assertEqual(core['family'],next(c for c in self.cores if c['id']=='sogb-017')['family'])

    def test_plain_exponentials_render_without_nesting_existing_math_or_mutating_gold(self):
        text='Multiply by αe^{αt}>0; X(u)=e^{−u}. Already \\(e^{\\alpha t}\\) and \\[e^{-t}\\].'
        rendered=reader.prose(text)
        self.assertIn(r'\(αe^{αt}\)',rendered)
        self.assertIn(r'\(e^{−u}\)',rendered)
        self.assertIn(r'\(e^{\alpha t}\)',rendered)
        self.assertNotIn(r'\(\(',rendered)
        core=next(c for c in self.cores if c['id']=='sogb-023')
        self.assertIn('αe^{αt}>0',core['steps'][3])
        self.assertEqual(core['binding_sha256'],next(c for c in bench.materialize() if c['id']==core['id'])['binding_sha256'])

    def test_flow_graph_reader_separates_statement_profiles_and_download_provenance(self):
        graphs={g['id']:g for g in bench.curriculum.graph_items()}
        typed=reader.graph_page(graphs['sogb-g007'])
        self.assertIn('data-statement-profiles',typed)
        self.assertIn('not a binder-role analysis',typed)
        self.assertIn('compiled-flow-graph.json',typed)
        self.assertIn('source mathematical proof and optional Lean',typed)
        ordinary=reader.graph_page(graphs['sogb-g004'])
        self.assertNotIn('data-statement-profiles',ordinary)
        self.assertIn('compiled-transport-graph.json',ordinary)

    def test_structural_graph_answers_sources_and_no_gold_in_prompts(self):
        graphs = bench.curriculum.graph_items()
        self.assertEqual(len(graphs), 7)
        self.assertTrue(all(g['family'] == 'pl-gradient-iteration' for g in graphs[:3]))
        self.assertTrue(all(g['family'] == 'coupling-gluing-triangle' for g in graphs[3:5]))
        self.assertTrue(all(g['family'] == 'convex-flow-first-order-rate' for g in graphs[5:]))
        self.assertTrue(all('answer' not in p for p in bench.curriculum.graph_prompts(graphs)))
        self.assertEqual(len(graphs[0]['context']['nodes']), 3)
        self.assertEqual(len(graphs[0]['context']['edges']), 2)
        self.assertEqual(len(graphs[2]['answer']['nodes']), 2)
        for g in graphs:
            self.assertFalse(g['answer']['entails_mathematical_necessity'])
            self.assertNotIn('atlas', json.dumps(g).lower())
            self.assertIn('source_sha256_lf', g['context'])

    def test_graph_grader_rejects_duplicates_stale_context_and_implicit_selection(self):
        graphs = bench.curriculum.graph_items()
        rows = [{'id': g['id'], 'binding_sha256': g['binding_sha256'], 'attempt': 1, 'answer': g['answer']} for g in graphs]
        grade = bench.curriculum.grade_graph(graphs, rows)
        self.assertEqual((grade['points'], grade['max_points']), (len(graphs), len(graphs)))
        missing = bench.curriculum.grade_graph(graphs, rows[:1])
        self.assertEqual((missing['points'], missing['max_points']), (1, len(graphs)))
        for invalid in (rows + rows[:1], [{**rows[0], 'binding_sha256': 'stale'}], [{**rows[0], 'attempt': 2}], [{**rows[0], 'attempt': True}]):
            with self.assertRaises(ValueError):
                bench.curriculum.grade_graph(graphs, invalid)
        wrong_type = deepcopy(rows)
        wrong_type[0]['answer']['entails_mathematical_necessity'] = 'false'
        self.assertFalse(bench.curriculum.grade_graph(graphs, wrong_type)['results'][0]['valid_schema'])

    def test_invalid_or_missing_track_difficulty_is_rejected(self):
        policy = bench.curriculum.curriculum()
        core = deepcopy(self.cores[0])
        core['track_levels'] = {'natural-language': 'L3'}
        with self.assertRaises(ValueError):
            bench.curriculum.classify(core, policy)

    def test_run_provenance_requires_a_real_profile_and_timezone(self):
        metadata = {'run_id': 'software-test-fixture', 'model': 'not-an-evaluated-model', 'model_version': 'fixture',
                    'created_at': '2026-11-03T10:00:00+08:00', 'prompt_profile': 'given-snapshot',
                    'attempt_policy': 'first-attempt', 'tools': [], 'seed': None}
        bench.curriculum.validate_run_metadata(metadata)
        for key, value in (('model_version', ''), ('created_at', '2026-11-03'), ('attempt_policy', 'best-of-10'), ('tools', 'none')):
            with self.assertRaises(ValueError):
                bench.curriculum.validate_run_metadata({**metadata, key: value})

    def test_import_figure_has_one_shared_node_and_no_proof_status_colours(self):
        figure = reader.import_figure(bench.curriculum.graph_items()[0]['context'])
        self.assertEqual(figure.count('<rect '), 3)
        self.assertIn('not theorem implication', figure)
        self.assertIn('stroke-dasharray', figure)
        self.assertNotIn('status-blue', figure)
        import re
        rects = [(float(x), float(y)) for x, y in re.findall(r'<rect x="([\d.]+)" y="([\d.]+)"', figure)]
        for x, y in rects:
            for xx, yy in rects:
                if y == yy and xx > x:
                    self.assertGreaterEqual(xx - x, 250)


if __name__ == '__main__':
    unittest.main()
