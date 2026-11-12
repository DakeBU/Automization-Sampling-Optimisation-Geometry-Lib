"""Paired identities, exact reference extraction, no-answer exports and reader contracts."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench as bench
import sog_bench_reader as reader
import sog_bench_graph_review as graph_review
import sog_bench_exercises as exercises


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
        declared = bench.load()['cores']
        self.assertEqual([c['id'] for c in self.cores], [c['id'] for c in declared])
        self.assertCountEqual([(r['id'], r['track']) for r in prompts],
                              [(c['id'], track) for c in declared for track in c['track_levels']])
        for core in self.cores:
            views = [r for r in prompts if r['id'] == core['id']]
            self.assertEqual({r['track'] for r in views}, set(core['track_levels']))
            for row in views:
                self.assertEqual(row['family'], core['family'])
                self.assertEqual(row['binding_sha256'], core['binding_sha256'])
                self.assertEqual(row['split'], 'public-dev')

    def test_prompt_export_has_no_answers_rubrics_or_reference_proofs(self):
        allowed = {'id', 'family', 'domain', 'library_domains', 'skills', 'title', 'split', 'assumptions', 'binding_sha256', 'track', 'level', 'question'}
        exercise_ids = {core['id'] for core in self.cores if core.get('textbook_exercise')}
        for row in bench.prompts(self.cores):
            self.assertEqual(set(row), allowed | ({'exercise_source'} if row['id'] in exercise_ids else set()))
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

    def test_assigned_proof_preserves_a_term_but_rejects_unassigned_declarations(self):
        signature, proof = bench.assigned_theorem(SimpleNamespace(kind='theorem',
            source_text='theorem finite_balance : True :=\n  True.intro'))
        self.assertEqual(signature, 'theorem finite_balance : True')
        self.assertEqual(proof, ':=\n  True.intro')
        for kind, source in (('theorem', 'theorem t : True'),
                             ('theorem', 'theorem t : True := /- no proof -/'),
                             ('def', 'def x : Nat := 1')):
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'explicit assigned proof'):
                bench.assigned_theorem(SimpleNamespace(kind=kind, source_text=source))

    def test_same_file_reference_helper_is_not_in_the_learner_task(self):
        data = bench.load()
        module = 'AutoSamplingTheory.TechnicalLemmas.Probability.KernelMixture'
        helper = module + '.finiteMixture_apply'
        raw = {**data['cores'][0], 'id': 'sogb-helper-fixture', 'context': '',
               'declaration': module + '.finiteMixture_invariant',
               'source_file': module.replace('.', '/') + '.lean', 'reference_helpers': [helper]}
        core = bench.materialize({**data, 'cores': [raw]})[0]
        self.assertIn('private theorem finiteMixture_apply', core['lean_reference'])
        self.assertIn('Kernel.withDensity_apply', core['lean_reference'])
        self.assertNotIn('finiteMixture_apply', core['lean_task'])
        self.assertNotIn('import ' + module, core['lean_reference'])
        for prompt in bench.prompts([core]):
            self.assertNotIn('reference_helpers', prompt)
            self.assertNotIn('finiteMixture_apply', prompt['question'])
        import sog_bench_lean
        runtime = sog_bench_lean.packet(core)
        self.assertIn(b'private theorem finiteMixture_apply', runtime['oracle/Solution.lean.txt'])
        for name in ('agent/prompt.json', 'agent/Solution.lean.txt', 'verifier/Challenge.lean'):
            self.assertNotIn(b'finiteMixture_apply', runtime[name])
        for invalid in ([], [helper, helper], [raw['declaration']], [data['cores'][0]['declaration']],
                        [module + '.finiteMixture'], [module + '.finiteMixture_isMarkovKernel', helper]):
            with self.assertRaises(ValueError):
                bench.materialize({**data, 'cores': [{**raw, 'reference_helpers': invalid}]})
        with self.assertRaises(ValueError):
            bench.materialize({**data, 'cores': [{**raw, 'lean_enabled': False}]})

    def test_lower_bounds_numbered_answer_does_not_create_a_lean_task(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-049')
        self.assertEqual(core['family'], 'chewi-opt-v1-exercise-4-1')
        self.assertEqual((core['textbook_exercise']['book_page'],
                          core['textbook_exercise']['pdf_page']), (28, 28))
        self.assertEqual(set(core['track_levels']), {'natural-language'})
        self.assertEqual(core['lean_task'], '')
        self.assertEqual(core['lean_reference'], '')
        self.assertIn('theorem exercise_4_1', core['support_lean_source'])
        self.assertEqual({a['declaration'] for a in core['textbook_exercise']['answer_declarations']},
                         {core['declaration']})
        panel = reader.exercise_panel(core, checked=False)
        self.assertEqual(panel.count(f'title="{core["declaration"]}"'), 1)
        self.assertIn('One owned Lean answer covers the listed parts', panel)
        for part in core['textbook_exercise']['parts']:
            self.assertIn(part['label'], panel)
        rendered = reader.prose(core['steps'][0])
        self.assertIn(r'\begin{aligned}&amp;f(y+h)-f(y)-\langle\nabla f(y),h\rangle', rendered)
        self.assertIn(r'\\&amp;=\frac{\beta}{8}', rendered)
        self.assertIn(r'\\&amp;\le\frac{\beta}{2}\|h\|^2.\end{aligned}', rendered)
        prompts = bench.prompts([core])
        self.assertEqual([p['track'] for p in prompts], ['natural-language'])
        self.assertNotIn('answer_declarations', prompts[0]['exercise_source'])
        self.assertNotIn('support_lean_source', prompts[0])
        self.assertNotIn('theorem exercise_4_1', prompts[0]['question'])

        catalog = bench.load()
        raw = next(row for row in catalog['cores'] if row['id'] == core['id'])
        for invalid in ({**raw, 'textbook_exercise_id': ''},
                        {**raw, 'support_source_view': False},
                        {**raw, 'lean_enabled': True, 'support_source_view': False},
                        {**raw, 'source_file': raw['source_file'].replace('LowerBounds', 'Other')},
                        {**raw, 'source_file': raw['source_file'].replace('LowerBounds', 'LowerBounds/..')},
                        {**raw, 'source_file': 'research-wiki/retrieval-index/atlas-v1/input.lean'}):
            with self.subTest(invalid=invalid['source_file']), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'cores.json'
                path.write_bytes(bench.encoded({**catalog, 'cores': [invalid]}))
                with patch.object(bench, 'DATA', path), self.assertRaises(ValueError):
                    bench.load()
        for invalid in ({**raw, 'textbook_exercise_id': ''},
                        {**raw, 'family': 'different-source-family'},
                        {**raw, 'lean_enabled': True, 'support_source_view': False}):
            with self.assertRaises(ValueError):
                bench.materialize({**catalog, 'cores': [invalid]})

    def test_original_example_allowlist_is_reference_only(self):
        source = 'AutoSamplingTheory/ExampleCases/DiscreteSampling/OrderedHeatBath.lean'
        decl = 'AutoSamplingTheory.ExampleCases.DiscreteSampling.OrderedHeatBath.ordered_heat_bath_invariant_not_reversible'
        catalog = bench.load()
        raw = {**catalog['cores'][0], 'source_file': source, 'declaration': decl,
               'lean_enabled': False, 'support_source_view': True,
               'track_levels': {'natural-language': 'L3'}}
        core = bench.materialize({**catalog, 'cores': [raw]})[0]
        self.assertEqual(core['lean_task'], '')
        self.assertEqual(core['lean_reference'], '')
        self.assertIn('theorem ordered_heat_bath_invariant_not_reversible', core['support_lean_source'])
        prompt, = bench.prompts([core])
        self.assertEqual(prompt['track'], 'natural-language')
        self.assertNotIn('support_lean_source', prompt)
        self.assertNotIn(decl, prompt['question'])
        page = reader.core_page(core, checked=False, graph_ids={'decl:' + decl},
                                structural=[], review_row={'editorial': 'pending'})
        self.assertIn('Owned Lean example · no fixed reconstruction challenge', page)
        self.assertIn('The owned declaration proves the concrete witness.', page)
        self.assertIn('&amp;view=lean&amp;q=' + decl, page)
        self.assertNotIn('Download task template', page)
        for invalid in ({**raw, 'source_file': source.replace('OrderedHeatBath', 'Other')},
                        {**raw, 'declaration': decl + '_other'},
                        {**raw, 'support_source_view': False},
                        {**raw, 'lean_enabled': True},
                        {**raw, 'track_levels': {'natural-language': 'L3', 'lean': 'L3'}},
                        {**raw, 'textbook_exercise_id': 'fake'}):
            with self.assertRaises(ValueError):
                bench.materialize({**catalog, 'cores': [invalid]})
        with self.assertRaises(ValueError):
            bench.materialize({**catalog, 'split': 'heldout', 'cores': [raw]})

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
            self.assertEqual(manifest['qa_views'], sum(len(c['track_levels']) for c in self.cores))
            self.assertEqual(manifest['numbered_textbook_exercises'],
                             len({c['textbook_exercise_id'] for c in self.cores if c.get('textbook_exercise')}))
            self.assertEqual(manifest['graph_tasks'], len(bench.curriculum.graph_items()))
            self.assertEqual(len(manifest['graph_evidence_kinds']),2)
            self.assertTrue((output/'compiled-transport-graph.json').is_file())
            self.assertTrue((output/'compiled-flow-graph.json').is_file())
            self.assertTrue((output/'compiled-exercise17-graph.json').is_file())
            self.assertIn('content-bound', manifest['independent_semantic_review'])
            self.assertEqual(manifest['editorial_accepted_graph_tasks'], graph_review.summary(bench.curriculum.graph_items())['accepted_tasks'])
            self.assertIn('human-attested', manifest['prose_scoring'])
            self.assertTrue((output/'EVALUATION.md').is_file())
            self.assertEqual((output/'FAMILY_ISOLATION.md').read_bytes(), (bench.DATA.parent/'FAMILY_ISOLATION.md').read_bytes())
            self.assertIn('](FAMILY_ISOLATION.md)', (output/'EVALUATION.md').read_text(encoding='utf-8'))
            self.assertIn('href="../downloads/FAMILY_ISOLATION.md"', reader.evaluation_guide())
            self.assertTrue((output/'TEXTBOOK_EXERCISES.md').is_file())
            self.assertIn('source intake is not QA admission', manifest['textbook_exercise_programme'])
            intake = (output/'TEXTBOOK_EXERCISES.md').read_text(encoding='utf-8')
            self.assertIn('Intake itself is not admission', intake)
            self.assertIn('9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b', intake)
            self.assertTrue((output/'examples/prose-run.json').is_file())
            guide = (output/'README.md').read_text(encoding='utf-8')
            self.assertNotIn('](reviews/', guide)
            self.assertIn('/blob/main/benchmarks/samplingoptimisationgeometrybench/reviews/formal-3/README.md', guide)
            ecosystem = (output/'ECOSYSTEM.md').read_text(encoding='utf-8')
            for text in (guide, ecosystem):
                self.assertNotIn('](lean-runtime/', text)
                self.assertIn('/blob/main/benchmarks/samplingoptimisationgeometrybench/lean-runtime/WORKSPACE.md', text)
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
        answers = exercises.answers(self.cores)
        receipt = {'schema_version': 1, 'passed': True, 'environment_sha256': 'environment',
                   'environment_scope': 'selected-source-import-closure',
                   'compiler_version': 'Lean (version 4.33.0, test fixture)',
                   'bindings': {c['id']: c['binding_sha256'] for c in aligned},
                   'reference_sha256': {c['id']: bench.sha(c['lean_reference'].encode()) for c in aligned},
                   'commands': [{'returncode': 0}] * (len(aligned) + 2 + bool(answers)),
                   'exercise_answer_declarations': sorted(answers),
                   'exercise_answer_axioms': {n: ['propext', 'Classical.choice', 'Quot.sound'] for n in answers}}
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(bench, 'RECEIPT', Path(tmp) / 'receipt.json'), \
             patch.object(bench, 'environment_digest', return_value='environment'):
            bench.RECEIPT.write_bytes(bench.encoded(receipt))
            self.assertTrue(bench.receipt_current(self.cores))
            bad = deepcopy(receipt)
            bad['exercise_answer_axioms'][sorted(answers)[0]] = ['sorryAx']
            bench.RECEIPT.write_bytes(bench.encoded(bad))
            self.assertFalse(bench.receipt_current(self.cores))
            bad = deepcopy(receipt)
            del bad['exercise_answer_declarations']
            bench.RECEIPT.write_bytes(bench.encoded(bad))
            self.assertFalse(bench.receipt_current(self.cores))
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
                if bench.ORIGINAL_EXAMPLE_ANSWERS.get(core['source_file']) == core['declaration']:
                    self.assertIn('The owned declaration proves the concrete witness.', rendered)
                    self.assertNotIn('Download task template', rendered)
                else:
                    self.assertIn('Owned Lean core answers' if core.get('textbook_exercise')
                                  else 'Lean view: not yet aligned', rendered)
                self.assertEqual('data-lean-copy-status' in rendered, bool(core.get('support_source_view')))
            self.assertNotIn('<details open', rendered)
            self.assertIn('focus=decl%3A', rendered)
            module = 'module:' + core['source_file'].removesuffix('.lean').replace('/', '.')
            fallback = reader.core_page(core, False, {module})
            self.assertIn('focus=module%3A', fallback)
            self.assertIn('declaration not yet indexed', fallback)
            unindexed = reader.core_page(core, False, set())
            self.assertIn('Not indexed in Lean Graph', unindexed)
            self.assertNotIn('focus=module%3A', unindexed)

    def test_display_identity_linebreaks_preserve_source_and_avoid_nested_tex(self):
        source = r'Proof \[a=b,\qquad c=d\] done.'
        rendered = reader.prose(source)
        self.assertIn(r'\begin{gathered}a=b,\\ c=d\end{gathered}', rendered)
        self.assertEqual(source, r'Proof \[a=b,\qquad c=d\] done.')
        wrapped = "\\[a=b,\n  \\qquad c=d\n    -e\\]"
        self.assertIn(r'\begin{gathered}a=b,\\ c=d\\    -e\end{gathered}', reader.prose(wrapped))
        for nested in (r'\[\text{a,\qquad b}=c\]', r'\[\begin{aligned}a&=b,\qquad c&=d\end{aligned}\]',
                       r'\[f(a,\qquad b)=c\]', "\\[a=(b\n  -c)\\]", "\\[a=\\|b\n  -c\\|\\]",
                       "\\[a=\\left|b\n  -c\\right|\\]", "\\[a \\le\n  -c\\]", r'\[a=b,\qquad \]'):
            self.assertNotIn(r'\begin{gathered}', reader.prose(nested))

    def test_stopped_work_display_wraps_without_changing_the_bound_text(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-035')
        before = bench.encoded(core)
        assumption = next(a for a in core['assumptions'] if r'\eta_t(h)' in a)
        estimate = next(s for s in core['steps'] if r'\left|\mathbb E_Q W' in s)
        self.assertIn(r'\begin{aligned}&amp;\eta_t(h)\\&amp;=\sum',
                      reader.prose(assumption, paragraph=False))
        self.assertIn(r'\right|\\&amp;=\left|', reader.prose(estimate))
        self.assertEqual(bench.encoded(core), before)

    def test_common_kernel_reference_retains_credit_but_not_answer_in_prompt(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-037')
        self.assertEqual(core['family'], 'adaptive-hybrid-cost-boundary')
        self.assertEqual(core['track_levels'], {'natural-language': 'L3', 'lean': 'L3'})
        reference = core['lean_reference']
        self.assertIn('Copyright (c) 2023 Kalle Kytölä.', reference)
        self.assertIn('Mathlib/MeasureTheory/Measure/LevyProkhorovMetric.lean', reference)
        self.assertIn('integral_eq_integral_Ioc_meas_le', reference)
        for row in bench.prompts([core]):
            self.assertNotIn('have htail', row['question'])
            self.assertNotIn('integral_eq_integral_Ioc_meas_le', row['question'])
        step = next(s for s in core['steps'] if r'\begin{aligned}D_T' in s)
        self.assertIn(r'\\ &amp;\le\delta', reader.prose(step))
        round_dir = bench.DATA.parent / 'reviews/formal-13'
        with patch.object(bench, 'RECEIPT', round_dir / 'trusted-reference-receipt.json'):
            self.assertTrue(bench.receipt_current([core]))

    def test_eight_domain_five_level_matrix_does_not_invent_coverage(self):
        graphs = bench.curriculum.graph_items()
        coverage = bench.curriculum.coverage(self.cores, graphs)
        self.assertEqual(len(coverage['cells']), 40)
        lower = [c for c in coverage['cells'] if c['domain'] == 'lower-bounds']
        self.assertEqual({c['level'] for c in lower}, {'L1', 'L2', 'L3', 'L4', 'L5'})
        self.assertTrue(all(c['gap'] and not any(c['draft_views'].values()) for c in lower if c['level'] not in {'L2', 'L3'}))
        self.assertEqual(next(c['draft_views'] for c in lower if c['level'] == 'L2'),
                         {'natural-language': 0, 'lean': 0, 'graph-json': 1})
        self.assertEqual(next(c['draft_views'] for c in lower if c['level'] == 'L3'),
                         {'natural-language': 4, 'lean': 2, 'graph-json': 0})
        self.assertEqual(coverage['unique_mathematical_cores'], len(bench.load()['cores']))
        self.assertEqual({c['domain'] for c in coverage['cells'] if c['level'] == 'L5' and not c['gap']},
                         {'samplewiki', 'mcmc'})
        self.assertEqual([c['id'] for c in self.cores if c['track_levels'].get('natural-language') == 'L5'],
                         ['sogb-035'])
        self.assertFalse(any(c['track_levels'].get('lean') == 'L5' for c in self.cores))
        self.assertTrue(all(c['independently_reviewed'] == 0 for c in coverage['cells']))
        self.assertEqual(coverage['mathematical_editorial_status'], 'pending')
        current = bench.coverage(self.cores, graphs)
        self.assertEqual(current['editorial_accepted_mathematical_cores'], len(self.cores))
        self.assertEqual(current['mathematical_editorial_status'], 'complete-for-current-cores')
        self.assertEqual(current['graph_editorial_status'], graph_review.summary(graphs)['editorial_status'])
        self.assertEqual(graph_review.summary(graphs)['accepted_tasks'], len(graphs))
        authored_domains = set(bench.curriculum.curriculum()['domains'])
        self.assertEqual({d for c in self.cores for d in c['library_domains']}, authored_domains)
        self.assertNotIn('OpenAI', json.dumps(coverage))
        for domain in authored_domains:
            if domain != 'lower-bounds':
                self.assertTrue(any(domain in c['library_domains'] and c['track_levels'].get('natural-language') == 'L1' for c in self.cores))
            self.assertTrue(any(domain in c['library_domains'] and bench.has_lean(c) for c in self.cores))

    def test_lower_bounds_pair_is_an_exact_reviewed_fixed_step_component(self):
        item = next(c for c in self.cores if c['id'] == 'sogb-046')
        self.assertEqual((item['id'], item['family']), ('sogb-046', 'chewi-opt-v1-exercise-3-3'))
        self.assertEqual(item['track_levels'], {'natural-language': 'L3', 'lean': 'L3'})
        self.assertNotIn('textbook_exercise', item)  # Not coverage of every source part.
        self.assertNotIn(item['source_file'].removesuffix('.lean').replace('/', '.'), item['imports'])
        self.assertIn('does not give a lower bound for adaptive', item['rubric'][3]['criterion'])
        self.assertNotIn('tight', item['rubric'][3]['criterion'])
        review_row = bench.editorial_review(self.cores)['items'][item['id']]
        self.assertEqual((review_row['editorial'], review_row['formal_alignment']),
                         ('accepted-after-repair', 'conclusion-only'))
        self.assertTrue(review_row['prior_review_report_sha256'])
        self.assertIn('never include in canonical exports yet.', item['boundary'])
        self.assertNotIn('canonical exports', bench.mathematical_scope(item))
        self.assertIn('oracle-complexity lower bound', bench.mathematical_scope(item))
        graph, = [g for g in bench.curriculum.graph_items() if g['core_id'] == item['id']]
        self.assertEqual((graph['id'], graph['family'], graph['split'], graph['level']),
                         ('sogb-g010', item['family'], item['split'], 'L2'))

    def test_horizon_gap_is_a_separate_reviewed_component_of_the_same_family(self):
        import sog_bench_lean as runtime
        by_id = {c['id']: c for c in self.cores}
        distance, gap = by_id['sogb-046'], by_id['sogb-047']
        self.assertEqual((gap['family'], gap['split']), (distance['family'], distance['split']))
        self.assertNotEqual(gap['declaration'], distance['declaration'])
        self.assertNotIn('textbook_exercise', gap)
        self.assertEqual(gap['track_levels'], {'natural-language': 'L3', 'lean': 'L3'})
        self.assertNotIn(gap['source_file'].removesuffix('.lean').replace('/', '.'),
                         runtime.local_imports(gap['imports']))
        self.assertIn('one_add_mul_sub_le_pow', gap['lean_reference'])
        self.assertNotIn('one_add_mul_sub_le_pow', gap['lean_task'])
        self.assertIn('norm, or energy argument', gap['rubric'][1]['criterion'])
        row = bench.editorial_review(self.cores)['items'][gap['id']]
        self.assertEqual((row['editorial'], row['formal_alignment']),
                         ('accepted-after-repair', 'conclusion-only'))
        graph = next(g for g in bench.curriculum.graph_items() if g['id'] == 'sogb-g010')
        self.assertEqual(graph['core_id'], distance['id'])
        self.assertIn(gap['declaration'], graph['context']['nodes'])
        self.assertIn('sogb-g010.html', reader.core_page(gap, False, structural=[graph], review_row=row))
        self.assertIn('sogb-047.html', reader.graph_page(graph))

    def test_single_query_lower_bound_is_only_aligned_to_natural_language(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-048')
        self.assertEqual(core['track_levels'], {'natural-language': 'L3'})
        self.assertFalse(bench.has_lean(core))
        self.assertNotIn('textbook_exercise', core)
        self.assertTrue(core['support_source_view'])
        self.assertTrue(core['declaration'].endswith(
            '.QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness'))
        self.assertNotIn(core['id'], {g['core_id'] for g in bench.curriculum.graph_items()})
        row = bench.editorial_review(self.cores)['items'][core['id']]
        self.assertEqual((row['editorial'], row['formal_alignment'], row['issues']),
                         ('accepted', 'no-aligned-view', []))

    def test_product_coupling_is_an_original_foundation_view_of_a_public_family(self):
        by_id = {c['id']: c for c in self.cores}
        core = by_id['sogb-041']
        self.assertEqual(core['track_levels'], {'natural-language': 'L2', 'lean': 'L1'})
        self.assertEqual(core['family'], by_id['sogb-012']['family'])
        self.assertEqual(core['family'], by_id['sogb-015']['family'])
        self.assertFalse(bench.has_lean(by_id['sogb-012']))
        self.assertNotIn('textbook_exercise', core)
        self.assertTrue(core['declaration'].endswith('.Transport.isCoupling_prod'))
        self.assertIn('MeasureTheory.SFinite', core['dependencies']['mathlib'])
        self.assertIn('constructor <;> simp', core['lean_reference'])
        self.assertNotIn('constructor <;> simp', core['lean_task'])

    def test_fisher_pairing_keeps_the_domain_and_hides_answer_helpers(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-042')
        self.assertEqual(core['track_levels'], {'natural-language': 'L4', 'lean': 'L4'})
        self.assertEqual(set(core['library_domains']), {'log-concave-sampling', 'statistical-optimal-transport'})
        self.assertNotIn('textbook_exercise', core)
        self.assertIn('SmoothFiniteScoreDomain', core['lean_task'])
        self.assertIn('IsQuadraticOptimalCoupling', core['lean_task'])
        self.assertNotIn(core['source_file'].removesuffix('.lean').replace('/', '.'), core['imports'])
        self.assertIn('memLp_score_and_displacement', core['lean_reference'])
        self.assertNotIn('memLp_score_and_displacement', core['lean_task'])

    def test_random_scan_term_proof_preserves_family_and_operator_boundary(self):
        import sog_bench_lean as runtime
        by_id = {c['id']: c for c in self.cores}
        narrow, full = by_id['sogb-006'], by_id['sogb-043']
        self.assertFalse(bench.has_lean(narrow))
        self.assertEqual((full['family'], full['split']), (narrow['family'], narrow['split']))
        self.assertEqual(full['track_levels'], {'natural-language': 'L3', 'lean': 'L3'})
        owner = full['source_file'].removesuffix('.lean').replace('/', '.')
        self.assertNotIn(owner, runtime.local_imports(full['imports']))
        pack = runtime.packet(full)
        self.assertIn(b'private theorem singleton_balance', pack['oracle/Solution.lean.txt'])
        self.assertIn(b':=\n  KernelReversibility.isReversible_of_singleton_balance', pack['oracle/Solution.lean.txt'])
        for path in ('agent/prompt.json', 'agent/Solution.lean.txt', 'verifier/Challenge.lean'):
            self.assertNotIn(b'singleton_balance', pack[path])

    def test_retained_kernel_keeps_sfinite_and_ae_fiber_boundary(self):
        import sog_bench_lean as runtime
        by_id = {c['id']: c for c in self.cores}
        base, lift = by_id['sogb-021'], by_id['sogb-044']
        self.assertEqual((lift['family'], lift['split']), (base['family'], base['split']))
        self.assertEqual(lift['track_levels'], {'natural-language': 'L4', 'lean': 'L4'})
        self.assertEqual(set(lift['library_domains']), {'mcmc', 'samplewiki'})
        self.assertFalse(runtime.local_imports(lift['imports']))
        for binder in ('[SFinite μ]', '[IsSFiniteKernel R]', '[IsSFiniteKernel F]', '∀ᵐ a ∂μ'):
            self.assertIn(binder, lift['lean_task'])
        self.assertNotIn('IsMarkovKernel', lift['lean_task'])
        self.assertNotIn('IsProbabilityMeasure', lift['lean_task'])
        pack = runtime.packet(lift)
        self.assertIn(b'private theorem retained_flux', pack['oracle/Solution.lean.txt'])
        for path in ('agent/prompt.json', 'agent/Solution.lean.txt', 'verifier/Challenge.lean'):
            self.assertNotIn(b'retained_flux', pack[path])

    def test_positive_fiber_reconstructs_finite_target_conditioning(self):
        import sog_bench_lean as runtime
        by_id = {c['id']: c for c in self.cores}
        scan, fiber = by_id['sogb-043'], by_id['sogb-045']
        self.assertEqual((fiber['family'], fiber['split']), (scan['family'], scan['split']))
        self.assertEqual(fiber['track_levels'], {'natural-language': 'L4', 'lean': 'L4'})
        for binder in ('[IsFiniteMeasure μ]', '[StandardBorelSpace (X i)]',
                       '[Nonempty (X i)]', '[MeasurableSingletonClass', '≠ 0'):
            self.assertIn(binder, fiber['lean_task'])
        self.assertNotIn('IsProbabilityMeasure', fiber['lean_task'])
        owner = fiber['source_file'].removesuffix('.lean').replace('/', '.')
        self.assertNotIn(owner, runtime.local_imports(fiber['imports']))
        pack = runtime.packet(fiber)
        self.assertIn(b'condDistrib_apply_of_ne_zero', pack['oracle/Solution.lean.txt'])
        for path in ('agent/prompt.json', 'agent/Solution.lean.txt', 'verifier/Challenge.lean'):
            self.assertNotIn(b'heatBath_eq_cond', pack[path])
        graph = next(item for item in bench.curriculum.graph_items() if item['id'] == 'sogb-g009')
        self.assertIn(fiber['declaration'], graph['context']['nodes'])
        self.assertIn('sogb-045.html', reader.graph_page(graph))
        self.assertNotEqual(graph['core_id'], fiber['id'])
        self.assertIn('sogb-g009.html', reader.core_page(fiber, False, structural=[graph]))

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

    def test_posterior_covariance_pair_and_weak_convex_transfer_have_distinct_formal_scopes(self):
        paired = next(c for c in self.cores if c['id'] == 'sogb-025')
        audit = next(c for c in self.cores if c['id'] == 'sogb-026')
        self.assertEqual(paired['family'], audit['family'])
        self.assertTrue(bench.has_lean(paired))
        self.assertFalse(bench.has_lean(audit))
        self.assertIn('(hX : MemLp id 2', paired['lean_task'])
        self.assertIn('(hupper :', paired['lean_task'])
        self.assertIn('GibbsC1Poincare.gibbs_c1_variance_poincare', paired['lean_reference'])
        self.assertIn('covarianceBilin_self', paired['lean_reference'])
        page = reader.core_page(audit, checked=False)
        self.assertIn('Additional source-bound support', page)
        for support in audit['supporting_declarations']:
            self.assertIn(support['source_sha256_lf'], page)
            self.assertIn(support['declaration'], page)
        self.assertIn('Lean view: not yet aligned', page)
        self.assertNotIn('Show fixed Lean task', page)
        self.assertIn('not full QA certification', page)

    def test_bernoulli_induction_is_not_a_fake_final_wrapper_task(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-027')
        self.assertFalse(bench.has_lean(core))
        self.assertEqual(core['track_levels'], {'natural-language': 'L3'})
        self.assertIn('private theorem entropy_bound', core['support_lean_source'])
        self.assertIn('private theorem rms_contraction', core['support_lean_source'])
        self.assertIn('Copyright (c) 2026 Yuanhe Zhang', core['support_lean_source'])
        self.assertIn('d0f506f0a695018265dccb33bcb05e2f5ca1c876', core['support_lean_source'])
        self.assertIn('conditional mean M is identically zero', core['steps'][7])
        self.assertIn('not divided by n', ' '.join(core['assumptions']))
        self.assertNotIn('entropy_chain', ' '.join(core['dependencies']['astis']))

    def test_gaussian_limit_pair_has_no_opaque_limit_premises_or_noncompact_credit(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-028')
        finite = next(c for c in self.cores if c['id'] == 'sogb-027')
        target = core['lean_task'].split('\nexample', 1)[1]
        self.assertEqual(core['family'], finite['family'])
        self.assertEqual(core['track_levels'], {'natural-language': 'L4', 'lean': 'L3'})
        self.assertIn('ContDiff ℝ 2 f', target)
        self.assertIn('HasCompactSupport f', target)
        self.assertNotIn('Integrable', target)
        self.assertNotIn('Tendsto', target)
        self.assertIn('le_of_tendsto_of_tendsto tEnt tHalf', core['lean_reference'])
        self.assertIn('BernoulliLogSobolev.bernoulli_function_logSobolev', core['lean_reference'])
        self.assertIn('sub_sq_comm', core['lean_reference'])
        self.assertIn(r'\frac{16BK}{\sqrt m}', ' '.join(core['steps']))
        self.assertIn('No full noncompact', core['boundary'])
        self.assertEqual(len(core['supporting_declarations']), 4)

    def test_real_textbook_exercise_intake_has_actual_existing_source_targets_not_qa_credit(self):
        source = json.loads((ROOT/'website/content/publications/optimisation.json').read_text(encoding='utf-8'))
        item = next(row for row in source['items'] if row['id'] == 'chewi-opt-v1-exercise-3-2')
        self.assertEqual(item['source']['edition'], 'arXiv:2605.07006v1')
        self.assertIn('Exercise3.2', item['source']['anchor'])
        for short in ('gradient_step_endpoint_bound', 'optimal_gradient_step'):
            name = 'AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.' + short
            self.assertFalse(bench.astis_site._SOURCE_BY_NAME[name].has_placeholder)
        page = reader.home(self.cores)
        self.assertIn('Numbered textbook exercises and our reference solutions', page)
        self.assertIn('downloads/TEXTBOOK_EXERCISES.md', page)
        self.assertIn('Intake itself is not admission', page)
        self.assertIn('chapter-03.html#chewi-opt-v1-exercise-3-2', page)
        self.assertIn('Exercise 3.2', next(c['title'] for c in self.cores if c['id'] == 'sogb-029'))

    def test_statot_numbered_exercise_preserves_the_two_actual_bounds(self):
        import sog_bench_formal_review as formal
        core = next(c for c in self.cores if c['id'] == 'sogb-031')
        ex = core['textbook_exercise']
        self.assertEqual((ex['number'], ex['book_page'], ex['pdf_page']), ('6', 44, 50))
        self.assertEqual(len(ex['parts']), 2)
        self.assertTrue(bench.has_lean(core))
        self.assertNotIn(core['source_file'].removesuffix('.lean').replace('/', '.'), core['imports'])
        row = formal.statuses(self.cores)[core['id']]
        self.assertEqual((row['editorial'], row['formal_alignment']), ('accepted', 'conclusion-only'))
        with self.assertRaisesRegex(ValueError, 'every source part'):
            formal.require_full_exercise_review(core, {})

    def test_numbered_exercise_has_exact_source_parts_and_only_bibliography_in_prompts(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-029')
        ex = core['textbook_exercise']
        self.assertEqual(ex['number'], '3.2')
        self.assertEqual((ex['book_page'], ex['pdf_page']), (23, 23))
        self.assertEqual({p['id'] for p in ex['parts']},
                         {'hessian-segment-bound', 'balanced-minimax-step'})
        self.assertEqual({s for d in ex['answer_declarations'] for s in d['supports']},
                         {p['id'] for p in ex['parts']})
        self.assertFalse(bench.has_lean(core))
        prompt = bench.prompts([core])[0]['exercise_source']
        self.assertEqual(prompt['exercise'], '3.2')
        self.assertNotIn('answer_declarations', prompt)
        self.assertNotIn('assumption_deltas', prompt)
        self.assertNotIn(core['declaration'], json.dumps(prompt))
        self.assertEqual(core['family'], ex['id'])
        self.assertTrue(all(d in bench.astis_site._SOURCE_BY_NAME for d in core['dependencies']['astis']))

    def test_multipage_exercise_links_all_three_owned_answers_without_prompt_leakage(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-030')
        ex = core['textbook_exercise']
        prompt = bench.prompts([core])[0]['exercise_source']
        self.assertEqual((prompt['pdf_page'], prompt['pdf_page_end']), (22, 23))
        self.assertEqual((prompt['book_page'], prompt['book_page_end']), (22, 23))
        self.assertEqual({p['id'] for p in ex['parts']},
                         {'bregman-positive-domain', 'scaled-cocoercivity', 'gradient-lipschitz'})
        names = {d['declaration'] for d in ex['answer_declarations']}
        self.assertEqual(len(names), 3)
        self.assertFalse(bench.has_lean(core))
        panel = reader.exercise_panel(core, False)
        self.assertIn('printed pp. 22–23 / PDF pp. 22–23', panel)
        self.assertIn('2605.07006v1#page=22', panel)
        self.assertIn('2605.07006v1#page=23', panel)
        for name in names:
            self.assertIn('?focus=decl%3A' + name, panel)
            self.assertNotIn(name, json.dumps(prompt))
        self.assertEqual(exercises.probe([core]).count('#print axioms '), 3)

    def test_long_trial_step_equality_aligns_without_changing_gold(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-030')
        step = core['steps'][1]
        rendered = reader.prose(step)
        self.assertIn(r'\begin{aligned}', rendered)
        self.assertIn(r'\\&amp;=F_x(y)-\frac{\|d\|^2}{2\beta}', rendered)
        self.assertNotIn(r'\begin{aligned}', step)
        for tex in (r'A\le B+\frac{1234567890}{1234567890}+(X=Y)',
                    r'A\le B+\frac{1234567890}{1234567890}+L:=X'):
            self.assertNotIn(r'\begin{aligned}', reader.prose(r'\[' + tex + 'a'*90 + r'\]'))

    def test_multipage_exercise_rejects_incomplete_reversed_or_untyped_ranges(self):
        known = bench.astis_site._SOURCE_BY_NAME
        original = json.loads(exercises.DATA.read_text(encoding='utf-8'))
        for edit in ({'pdf_page_end': 22}, {'pdf_page_end': 150}, {'book_page_end': True},
                     {'book_page_end': '23'}, {'pdf_page_end': None}):
            data = deepcopy(original)
            row = next(r for r in data['exercises'] if r['id'] == 'chewi-opt-v1-exercise-3-1')
            for key, value in edit.items():
                if value is None:
                    del row[key]
                else:
                    row[key] = value
            with self.assertRaises(ValueError):
                exercises.resolve(row['id'], known, data)

    def test_numbered_source_resolver_rejects_relabelling_missing_parts_and_fake_declarations(self):
        original = json.loads(exercises.DATA.read_text(encoding='utf-8'))
        known = bench.astis_site._SOURCE_BY_NAME
        for key, value in (('number', '3.3'), ('pdf_page', 150),
                           ('book_page', True), ('publication_file', '../elsewhere.json')):
            data = deepcopy(original)
            data['exercises'][0][key] = value
            with self.assertRaises(ValueError):
                exercises.resolve('chewi-opt-v1-exercise-3-2', known, data)
        data = deepcopy(original)
        data['books']['chewi-optimization-v1']['pdf_url'] = 'https://arxiv.org/pdf/2605.07006v2'
        with self.assertRaises(ValueError):
            exercises.resolve('chewi-opt-v1-exercise-3-2', known, data)
        with self.assertRaises(ValueError):
            exercises.resolve('not-a-real-exercise', known)
        with self.assertRaises(ValueError):
            exercises.resolve('chewi-opt-v1-exercise-3-2', {}, original)
        path = ROOT / original['exercises'][0]['publication_file']
        pub = json.loads(path.read_text(encoding='utf-8'))
        selected = next(p for p in pub['items'] if p['id'] == 'chewi-opt-v1-exercise-3-2')
        selected['bindings'] = selected['bindings'][:1]
        actual_read = Path.read_text
        with patch.object(Path, 'read_text', lambda p, *a, **kw:
                          bench.encoded(pub).decode() if p == path else actual_read(p, *a, **kw)):
            with self.assertRaises(ValueError):
                exercises.resolve('chewi-opt-v1-exercise-3-2', known, original)

    def test_owned_answer_probe_checks_named_compiled_modules_not_a_reconstruction_target(self):
        core = next(c for c in self.cores if c['id'] == 'sogb-029')
        names = sorted(exercises.answers([core]))
        probe = exercises.probe([core])
        self.assertEqual(probe.count('#print axioms '), 2)
        self.assertIn('import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep', probe)
        self.assertNotIn('example', probe)
        output = '\n'.join("'" + n + "' depends on axioms: [propext, Classical.choice, Quot.sound]" for n in names)
        self.assertEqual(set(exercises.checked_axioms(output, names)), set(names))
        with self.assertRaises(ValueError):
            exercises.checked_axioms(output.replace('Quot.sound', 'sorryAx'), names)
        with self.assertRaises(ValueError):
            exercises.checked_axioms('', names)

    def test_exercise_1_7_preserves_distinct_targets_and_one_public_family(self):
        import sog_bench_lean as runtime

        cores = [c for c in self.cores if c['id'] in {'sogb-039', 'sogb-040'}]
        self.assertEqual([c['id'] for c in cores], ['sogb-039', 'sogb-040'])
        self.assertEqual({c['family'] for c in cores}, {'chewi-lcs-2026-08-20-exercise-1-7'})
        self.assertEqual({c['split'] for c in cores}, {'public-dev'})
        exercise = cores[0]['textbook_exercise']
        self.assertEqual(exercise, cores[1]['textbook_exercise'])
        self.assertEqual((exercise['book_page'], exercise['pdf_page']), (43, 55))
        self.assertNotIn('source_assumptions', exercise)
        owners = {c['source_file'].removesuffix('.lean').replace('/', '.') for c in cores}
        self.assertEqual(len(owners), 2)
        for core, level in zip(cores, ('L4', 'L3'), strict=True):
            self.assertEqual(core['track_levels'], {'natural-language': level, 'lean': level})
            self.assertFalse(owners.intersection(runtime.local_imports(core['imports'])))
            packet = runtime.packet(core)
            descriptor = json.loads(packet['operator.json'])
            self.assertEqual(descriptor['binding_sha256'], core['binding_sha256'])
            self.assertNotIn('source_components', json.loads(packet['agent/prompt.json']))
            self.assertTrue(all(c['declaration'].encode() not in packet['agent/Solution.lean.txt'] for c in cores))
        self.assertNotEqual(*(exercises.question_component(exercise, c['declaration']) for c in cores))

    def test_exercise_sources_allow_hash_pinned_primary_books_not_only_arxiv(self):
        data = json.loads(exercises.DATA.read_text(encoding='utf-8'))
        book = data['books']['chewi-optimization-v1']
        book['edition'] = 'dated-primary-source-test-fixture'
        book['pdf_url'] = 'https://chewisinho.github.io/main.pdf'
        del book['html_url']
        path = ROOT / data['exercises'][0]['publication_file']
        pub = json.loads(path.read_text(encoding='utf-8'))
        selected = next(p for p in pub['items'] if p['id'] == 'chewi-opt-v1-exercise-3-2')
        selected['source']['edition'] = book['edition']
        selected['source']['anchor'] = 'Exercise 3.2. Source punctuation fixture.'
        actual_read = Path.read_text
        with patch.object(Path, 'read_text', lambda p, *a, **kw:
                          bench.encoded(pub).decode() if p == path else actual_read(p, *a, **kw)):
            resolved = exercises.resolve('chewi-opt-v1-exercise-3-2', bench.astis_site._SOURCE_BY_NAME, data)
            self.assertEqual(resolved['book']['pdf_url'], book['pdf_url'])
        for url in ('javascript:bad', 'https://user:secret@example.org/book.pdf', 'https://example.org/ bad'):
            self.assertFalse(exercises.primary_url(url))

    def _component_exercise_fixture(self):
        data = json.loads(exercises.DATA.read_text(encoding='utf-8'))
        row = data['exercises'][0]
        book = data['books'][row['book_id']]
        existing = json.loads((ROOT / row.pop('publication_file')).read_text(encoding='utf-8'))
        original = next(item for item in existing['items'] if item['id'] == row['id'])
        docs, refs = {}, []
        for i, binding in enumerate(original['bindings'], 1):
            rel = f'website/content/publications/exercise-component-fixture-{i}.json'
            ident = f'exercise-component-fixture-{i}'
            item = {**deepcopy(original), 'id': ident, 'title': f'Component {i}',
                    'statement': f'Statement belonging only to component {i}.',
                    'assumptions': [f'Assumptions belonging only to component {i}.'],
                    'obligations': [{'id': 'shared-part-label', 'label': f'Represented part {i}'}],
                    'bindings': [{**deepcopy(binding), 'role': 'proof-edge', 'supports': ['shared-part-label']}]}
            item['source'].update(url=book['pdf_url'] + '#page=23', pdf_sha256=book['pdf_sha256'])
            docs[ROOT / rel] = {'schema_version': 1, 'items': [item]}
            refs.append({'publication_file': rel, 'item_id': ident})
        self.assertEqual(len(refs), 2)
        row['publication_components'] = refs
        return data, row['id'], docs

    def _resolve_component_fixture(self, data, identity, docs):
        original = Path.read_text
        with patch.object(Path, 'read_text', lambda p, *a, **kw:
                          bench.encoded(docs[p]).decode() if p in docs else original(p, *a, **kw)):
            return exercises.resolve(identity, bench.astis_site._SOURCE_BY_NAME, data)

    def test_distinct_numbered_exercise_components_keep_separate_scope_and_prompt_only_source(self):
        data, identity, docs = self._component_exercise_fixture()
        result = self._resolve_component_fixture(data, identity, docs)
        self.assertNotIn('source_assumptions', result)
        self.assertNotIn('source_statement', result)
        self.assertEqual([a['component_id'] for a in result['answer_declarations']],
                         [c['item_id'] for c in result['source_components']])
        ids = [part['id'] for part in result['parts']]
        self.assertEqual(len(set(ids)), 2)
        self.assertEqual([a['supports'][0] for a in result['answer_declarations']], ids)
        html = reader.exercise_panel({'textbook_exercise': result,
                                      'declaration': result['answer_declarations'][1]['declaration']}, False)
        self.assertIn('Represented source parts and exact Lean scope', html)
        self.assertNotIn('all requested parts', html)
        self.assertLess(html.index('<summary>Component 2</summary>'), html.index('<summary>Component 1</summary>'))
        self.assertEqual(html.count('Source component for this question'), 1)
        for i, answer in enumerate(result['answer_declarations'], 1):
            self.assertIn(f'<summary>Component {i}</summary>', html)
            self.assertIn(f'Assumptions belonging only to component {i}.', html)
            self.assertIn('focus=decl%3A' + answer['declaration'], html)
        prompt = json.dumps(exercises.source_prompt(result))
        self.assertIn('3.2', prompt)
        for secret in ('source_components', 'exercise-component-fixture-', 'Assumptions belonging',
                       'answer_declarations', *(a['declaration'] for a in result['answer_declarations'])):
            self.assertNotIn(secret, prompt)
        changed = deepcopy(docs)
        next(iter(changed.values()))['items'][0]['statement'] += ' Revised wording.'
        revised = self._resolve_component_fixture(data, identity, changed)
        self.assertNotEqual(result['source_entry_sha256'], revised['source_entry_sha256'])
        self.assertEqual(exercises.compile_contexts([{'textbook_exercise': result}]),
                         exercises.compile_contexts([{'textbook_exercise': revised}]))

    def test_component_acceptance_does_not_spread_to_other_parts(self):
        data, identity, docs = self._component_exercise_fixture()
        exercise = self._resolve_component_fixture(data, identity, docs)
        cores = [{'id': f'sogb-fixture-{i}', 'textbook_exercise': exercise, 'declaration': row['declaration'],
                  'track_levels': {'natural-language': 'L3'}} for i, row in enumerate(exercise['answer_declarations'])]
        reviews = {c['id']: {'editorial': state} for c, state in zip(cores, ['accepted', 'stale'], strict=True)}
        rows = exercises.projection(cores, reviews, compiled=False)
        first, second = (c['item_id'] for c in exercise['source_components'])
        self.assertEqual(rows[0]['represented_components_with_accepted_qa'], [first])
        self.assertEqual([q['component_id'] for q in rows[0]['questions']], [first, second])
        self.assertFalse(rows[0]['owned_answer_build_recorded'])
        with patch.object(bench, 'editorial_review', return_value={'items': reviews}):
            html = reader.exercise_index(cores, False)
        self.assertIn('1 of 2 represented source components', html)
        self.assertIn('>Component 2</a> · stale', html)
        with self.assertRaisesRegex(ValueError, 'exactly one owned answer anchor'):
            exercises.projection([{**cores[0], 'declaration': 'Unowned'}], reviews, compiled=False)

    def test_numbered_exercise_components_refuse_ambiguous_scope_or_unbound_sources(self):
        data, identity, docs = self._component_exercise_fixture()
        for defect in ('both-mappings', 'duplicate-component', 'outside-path', 'missing-file',
                       'missing-boundary', 'wrong-pdf', 'wrong-url', 'wrong-page', 'wrong-exercise', 'missing-part',
                       'prerequisite-only', 'duplicate-answer'):
            with self.subTest(defect=defect):
                changed, files = deepcopy(data), deepcopy(docs)
                row = changed['exercises'][0]
                first, second = [p['items'][0] for p in files.values()]
                if defect == 'both-mappings':
                    row['publication_file'] = 'website/content/publications/optimisation.json'
                elif defect == 'duplicate-component':
                    row['publication_components'][1] = row['publication_components'][0]
                elif defect == 'outside-path':
                    row['publication_components'][0]['publication_file'] = '../elsewhere.json'
                elif defect == 'missing-file':
                    row['publication_components'][0]['publication_file'] = 'website/content/publications/not-present.json'
                elif defect == 'missing-boundary':
                    row['unformalized_context'] = []
                elif defect == 'wrong-pdf':
                    first['source']['pdf_sha256'] = '0' * 64
                elif defect == 'wrong-url':
                    first['source']['url'] = 'https://example.org/another-book.pdf'
                elif defect == 'wrong-page':
                    first['source']['url'] = first['source']['url'].replace('#page=23', '#page=24')
                elif defect == 'wrong-exercise':
                    first['source']['anchor'] = 'Exercise 3.3'
                elif defect == 'missing-part':
                    first['obligations'].append({'id': 'unmapped', 'label': 'Unmapped conclusion'})
                elif defect == 'prerequisite-only':
                    first['bindings'][0]['role'] = 'prerequisite'
                elif defect == 'duplicate-answer':
                    first['bindings'][0]['declaration'] = second['bindings'][0]['declaration']
                with self.assertRaises(ValueError):
                    self._resolve_component_fixture(changed, identity, files)

    def test_exercise_prose_changes_do_not_recompile_unchanged_owned_answers(self):
        data = deepcopy(bench.load())
        identity = 'sogb-030'
        next(c for c in data['cores'] if c['id'] == identity)['question'] += ' Extra unaudited clause.'
        changed = bench.materialize(data)
        self.assertNotEqual(next(c for c in changed if c['id'] == identity)['binding_sha256'],
                            next(c for c in self.cores if c['id'] == identity)['binding_sha256'])
        self.assertEqual(bench.environment_digest(changed), bench.environment_digest(self.cores))
        self.assertEqual(exercises.compile_contexts(changed), exercises.compile_contexts(self.cores))

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
        self.assertTrue(all(g['family'] == 'pl-gradient-iteration' for g in graphs[:3]))
        self.assertTrue(all(g['family'] == 'coupling-gluing-triangle' for g in graphs[3:5]))
        self.assertTrue(all(g['family'] == 'convex-flow-first-order-rate' for g in graphs[5:7]))
        self.assertTrue(all(not {'answer', 'binding_sha256'} & p.keys()
                            for p in bench.curriculum.graph_prompts(graphs)))
        self.assertEqual(len(graphs[0]['context']['nodes']), 3)
        self.assertEqual(len(graphs[0]['context']['edges']), 2)
        self.assertEqual(len(graphs[2]['answer']['nodes']), 2)
        for g in graphs:
            self.assertFalse(g['answer']['entails_mathematical_necessity'])
            self.assertNotIn('atlas', json.dumps(g).lower())
            self.assertIn('source_sha256_lf', g['context'])

    def test_public_graph_fingerprint_is_independent_of_the_answer(self):
        graphs = bench.curriculum.graph_items()
        for item in graphs:
            public = bench.curriculum.graph_prompt(item)
            visible = {k: v for k, v in public.items() if k != 'prompt_sha256'}
            self.assertEqual(public['prompt_sha256'], bench.curriculum.digest(visible))
            self.assertEqual(item['binding_sha256'], bench.curriculum.digest(
                {'prompt': visible, 'answer': item['answer']}))
            different = {**item['answer'],
                         'entails_mathematical_necessity': not item['answer']['entails_mathematical_necessity']}
            alternate = {**item, 'answer': different, 'binding_sha256': bench.curriculum.digest(
                {'prompt': visible, 'answer': different})}
            self.assertNotEqual(item['binding_sha256'], alternate['binding_sha256'])
            self.assertEqual(bench.curriculum.graph_prompt(alternate), public)
            self.assertNotEqual(bench.curriculum.graph_prompt({**item, 'question': item['question'] + ' Change.'}),
                                public)

    def test_graph_capture_translates_only_the_exact_public_prompt(self):
        item = bench.curriculum.graph_items()[0]
        row = {'id': item['id'], 'attempt': 1, 'answer': item['answer'],
               'prompt_sha256': bench.curriculum.graph_prompt(item)['prompt_sha256']}
        original = deepcopy(row)
        legacy = {k: v for k, v in row.items() if k != 'prompt_sha256'} | {'binding_sha256': item['binding_sha256']}
        canonical = bench.curriculum.bind_graph_submissions([item], [row])
        self.assertEqual(canonical, [legacy])
        self.assertEqual(row, original)
        self.assertEqual(bench.curriculum.grade_graph([item], canonical)['points'], 1)
        self.assertEqual(bench.curriculum.bind_graph_submissions([item], [legacy], allow_legacy=True), [legacy])
        for bad in (legacy, {**row, 'prompt_sha256': item['binding_sha256']},
                    {**row, 'binding_sha256': item['binding_sha256']}, {**row, 'id': []}):
            with self.assertRaises(ValueError):
                bench.curriculum.bind_graph_submissions([item], [bad])

    def test_offline_graph_parser_never_collapses_ambiguous_attempts(self):
        self.assertEqual(bench.curriculum.parse_graph_record('{"attempt":1}'), {'attempt': 1})
        for raw in ('{"attempt":2,"attempt":1}', '{"answer":{"nodes":[],"nodes":["other"]}}',
                    '{"attempt":NaN}', '{"attempt":Infinity}', '{}{}', '[]'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                bench.curriculum.parse_graph_record(raw)

    def test_exercise17_graph_explains_indirect_path_in_reference_not_prompt(self):
        graph = next(g for g in bench.curriculum.graph_items() if g['id'] == 'sogb-g008')
        core = next(c for c in self.cores if c['id'] == 'sogb-039')
        self.assertEqual(graph['family'], core['family'])
        self.assertEqual(graph['answer']['nodes'], [core['declaration']])
        self.assertNotIn([core['declaration'], graph['remove']], graph['context']['edges'])
        page = reader.graph_page(graph)
        self.assertIn('compiled-exercise17-graph.json', page)
        self.assertIn('sogb-040.html', page)
        self.assertIn('Compact Euclidean Poincaré conclusion → Compact-test LSI extension → Three cutoff limits', page)
        self.assertIn('Shared immediate proof-body parent(s): Compensated entropy integral limit', page)
        self.assertNotIn('Selected path:', json.dumps(bench.curriculum.graph_prompts([graph])))

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


class AuthoredProseRenderingTests(unittest.TestCase):
    def test_presence_gate_checks_authored_words_not_hidden_code_or_raw_typography(self):
        import declaration_lessons as lessons
        raw = 'Assume `x <= M` and actual integrability.'
        expected = lessons._canonical_prose(raw)
        self.assertIn(expected, lessons._authored_prose_text('<p>' + lessons.inline_text(raw) + '</p>'))
        self.assertNotIn(expected, lessons._authored_prose_text('<pre>' + raw + '</pre><script>' + raw + '</script>'))
        self.assertNotIn(expected, lessons._authored_prose_text('<p>Assume x ≤ M.</p>'))

    def test_prose_relations_render_but_literal_code_is_preserved(self):
        import declaration_lessons
        rendered = declaration_lessons.inline_text('u>=0, x <= M, a -> b, x!=y; `x <= M -> True`')
        self.assertIn('u≥0, x ≤ M, a → b, x≠y;', rendered)
        self.assertIn('<code>x &lt;= M -&gt; True</code>', rendered)
        assumptions = declaration_lessons.prose_list(['x <= M', '`x <= M`'])
        self.assertIn('<li>x ≤ M</li>', assumptions)
        self.assertIn('<li><code>x &lt;= M</code></li>', assumptions)
        # Preserve legacy structured convention records as data, not prose.
        structured = {'notation': 'x <= M'}
        self.assertIn(declaration_lessons.base.esc(structured), declaration_lessons.prose_list([structured]))

    def test_existing_tex_and_html_escaping_are_preserved(self):
        import declaration_lessons
        rendered = declaration_lessons.inline_text(r'\(\texttt{a->b}\) and \[x<=y\] $x>=y$ $$a->b$$ <script>')
        self.assertIn(r'\(\texttt{a-&gt;b}\)', rendered)
        self.assertIn(r'\[x&lt;=y\]', rendered)
        self.assertIn('$x&gt;=y$', rendered)
        self.assertIn('$$a-&gt;b$$', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertNotIn('<script>', rendered)


class SiteWorkflowPinTests(unittest.TestCase):
    def test_pinned_playwright_has_a_supported_fixed_browser_runner(self):
        workflow = (ROOT / '.github/workflows/blueprint-site.yml').read_text(encoding='utf-8')
        job = workflow.split('\n  website:\n', 1)[1].split('\n  deploy:', 1)[0]
        self.assertIn('runs-on: ubuntu-24.04', job)
        self.assertIn('playwright==1.57.0', job)
        self.assertIn('playwright install --with-deps chromium', job)
        self.assertNotIn('runs-on: ubuntu-latest', job)


if __name__ == '__main__':
    unittest.main()
