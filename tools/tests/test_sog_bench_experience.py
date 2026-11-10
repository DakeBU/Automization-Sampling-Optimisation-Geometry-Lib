"""Reader projections must not rewrite reviewed mathematics or invent graph credit."""
import sys
import unittest
from html import unescape
from pathlib import Path
import re
import io
import json
import zipfile
import hashlib

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import sog_bench_reader as reader
import sog_bench as bench


class ReadableMathTests(unittest.TestCase):
    def test_plain_mathematical_notation_gets_real_tex(self):
        rendered = reader.inline_prose('Let f:ℝᵈ→ℝ be C² and α-convex; αI≼∇²f(z)≼βI. Use T_h(x).')
        self.assertIn(r'\mathbb{R}^{d}\to \mathbb{R}', rendered)
        self.assertIn(r'\nabla ^{2}f(z)', rendered)
        self.assertIn(r'T_{h}(x)', rendered)
        self.assertIn(r'\(α\)</span>-convex', rendered)
        self.assertNotIn(r'\(α-convex', rendered)

    def test_explicit_tex_and_code_are_not_guessed_or_mutated(self):
        for math in (r'\(T_h(x)\)', r'\[\frac{a}{b}\]', '$x_i$', '$$x^2$$'):
            self.assertEqual(reader.inline_prose(math), math)
        self.assertEqual(reader.inline_prose('`T_h(x)`'), '<code>T_h(x)</code>')
        self.assertEqual(reader.inline_prose('https://example.com/C_PI.html'), 'https://example.com/C_PI.html')
        self.assertNotIn('sog-inline-math', reader.inline_prose('public-dev and alpha_beta identifiers'))

    def test_projection_keeps_every_original_math_token(self):
        text = 'C²; α-convex f:ℝᵈ→ℝ, T_h(x)=x−h∇f(x), 0<α≤β; C_PI<=C_LSI.'
        rendered = reader.inline_prose(text)
        restored = re.sub(r'<span class="sog-inline-math" data-math-original="([^"]*)">.*?</span>',
                          lambda m: unescape(m.group(1)), rendered)
        self.assertEqual(unescape(restored), text)

    def test_pushforward_subscripts_and_literal_sets_are_not_tex_syntax_errors(self):
        self.assertIn(r'S\#γ', reader.inline_prose('γ′=S#γ'))
        self.assertIn(r'π_{1}\circ S=π_{2}', reader.inline_prose('π₁∘S=π₂'))
        self.assertIn(r'\{0,1\}^{d}', reader.inline_prose('f:{0,1}ᵈ→ℝ'))

    def test_lean_identifiers_are_code_not_subscripted_mathematics(self):
        self.assertEqual(reader.inline_prose('le_div_iff₀'), '<code>le_div_iff₀</code>')
        self.assertEqual(reader.inline_prose('hX.const_inner'), '<code>hX.const_inner</code>')
        self.assertEqual(reader.inline_prose('l2_edge_triangle'), '<code>l2_edge_triangle</code>')
        self.assertIn('sog-inline-math', reader.inline_prose('C_PI<=C_LSI'))

    def test_differential_notation_is_math_but_named_api_calls_stay_code(self):
        self.assertIn(r'dT_{h}(z(t))/dt=DT_{h}(z(t))v',
                      reader.inline_prose('dT_h(z(t))/dt=DT_h(z(t))v.'))
        self.assertEqual(reader.inline_prose('le_div_iff₀(h)'), '<code>le_div_iff₀(h)</code>')
        self.assertEqual(reader.inline_prose('hX.const_inner(u)'), '<code>hX.const_inner(u)</code>')

    def test_simple_mathematical_equalities_are_not_raw_text_or_cli_options(self):
        for formula in ('x=y', 'z(t)=x+tv', 'M=M(h)', 'q<1', 't=0'):
            self.assertIn('sog-inline-math', reader.inline_prose(formula))
        self.assertNotIn('sog-inline-math', reader.inline_prose('attempt=1 and --track=lean'))

    def test_ambiguous_unbalanced_notation_is_left_literal(self):
        self.assertNotIn('sog-inline-math', reader.inline_prose('∇f(x'))


class NumberedExerciseReaderTests(unittest.TestCase):
    def test_lower_bounds_domain_has_a_real_route_without_fake_task_counts(self):
        with self.subTest('routes'):
            config = reader.bench_portals.configuration()
            sources = [c for c in config['collections'] if 'lower-bounds' in c['domains']]
            self.assertEqual([c['id'] for c in sources], ['sampling', 'optimisation'])
            for collection in sources:
                page = reader.bench_portals.collection_page([], collection)
                self.assertIn('href="../domains/lower-bounds.html"', page)
        page = reader.browse_page([], 'lower-bounds', domain=True)
        self.assertIn('href="../../../lower-bounds/index.html"', page)
        self.assertIn('explicit coverage gap', page)
        self.assertIn('stated oracle model', page)

    def test_single_source_exercise_distinguishes_fixed_task_from_owned_answer(self):
        owned = 'AutoSamplingTheory.TechnicalLemmas.Measure.Example.answer'
        exercise = {'book': {'title': 'Synthetic exercise source', 'pdf_url': 'https://example.invalid/book.pdf',
                             'authors': ['Fixture Author'], 'edition': 'Pinned fixture', 'rights_boundary': 'Example only.'},
                    'number': '6', 'book_page': 44, 'pdf_page': 50, 'wording_status': 'Original restatement.',
                    'source_statement': 'Prove the conclusion.', 'source_assumptions': ['Let the hypotheses hold.'],
                    'parts': [{'id': 'bound', 'label': 'Bound'}],
                    'answer_declarations': [{'declaration': owned, 'supports': ['bound']}],
                    'context_notes': [], 'unformalized_context': ['No optimizer conclusion.']}
        paired = reader.exercise_panel({'textbook_exercise': exercise, 'lean_enabled': True}, False)
        self.assertIn('fixed Lean task covers the mathematical conclusion only', paired)
        self.assertIn('No current aggregate owned-answer build receipt', paired)
        self.assertIn('book.pdf#page=50', paired)
        self.assertNotIn('not a new proof, an equivalent Lean challenge', paired)
        prose = reader.exercise_panel({'textbook_exercise': exercise, 'lean_enabled': False}, True)
        self.assertIn('not a new proof, an equivalent Lean challenge', prose)
        self.assertNotIn('separate fixed Lean task', prose)

    def test_source_only_graph_target_never_counts_as_compiled(self):
        owned = 'AutoSamplingTheory.TechnicalLemmas.Measure.Example.answer'
        key = 'decl:' + owned
        node = {'kind': 'declaration', 'url': 'declarations/answer.html', 'status': 'partial'}
        self.assertTrue(reader.has_exercise_graph_target({key: node}, owned, checked=False))
        self.assertFalse(reader.has_exercise_graph_target({key: node}, owned, checked=True))
        for altered in ({'kind': 'module'}, {'status': 'todo'}, {'url': ''}):
            self.assertFalse(reader.has_exercise_graph_target({key: {**node, **altered}}, owned, checked=False))
        self.assertTrue(reader.has_exercise_graph_target({key: {**node, 'status': 'compiled'}}, owned, checked=True))


class TaskPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cores = bench.materialize()
        cls.graphs = bench.curriculum.graph_items()
        cls.assets = bench.task_assets(cls.cores, cls.graphs)

    def test_every_existing_view_has_an_exact_prompt_and_environment_contract(self):
        rows = json.loads(self.assets['task-index.json'])['tasks']
        expected = bench.prompts(self.cores) + bench.curriculum.graph_prompts(self.graphs)
        self.assertEqual(len(rows), len(expected))
        for row, original in zip(rows, expected):
            self.assertEqual(json.loads(self.assets[row['prompt_file']]), original)
            descriptor = json.loads(self.assets[row['task_file']])
            self.assertFalse(descriptor['hidden_test'])
            self.assertFalse(descriptor['environment']['arbitrary_submission_execution'])
            self.assertEqual(descriptor['environment']['lean_toolchain'], 'leanprover/lean4:v4.33.0')
            self.assertEqual(descriptor['family'], original['family'])
            self.assertEqual(descriptor['split'], 'public-dev')

    def test_agent_archive_contains_neither_gold_nor_expert_anchors(self):
        with zipfile.ZipFile(io.BytesIO(self.assets['agent-tasks.zip'])) as bundle:
            names = set(bundle.namelist())
            self.assertIn('LICENSE', names)
            self.assertIn('task-index.json', names)
            self.assertNotIn('training-pairs.jsonl', names)
            self.assertNotIn('expert-graph-positions.json', names)
            self.assertNotIn('harbor-graph-tasks.zip', names)
            self.assertFalse(any('/oracle/' in n or '/verifier/' in n for n in names))
            self.assertFalse(any('reference.lean' in n or 'reviews/' in n for n in names))
            manifest = json.loads(bundle.read('task-files.sha256.json'))
            self.assertEqual(set(manifest['files']), names - {'task-files.sha256.json'})
            for name, expected in manifest['files'].items():
                self.assertEqual(hashlib.sha256(bundle.read(name)).hexdigest(), expected)

    def test_graph_agent_files_use_only_public_prompt_identity(self):
        index = json.loads(self.assets['task-index.json'])
        self.assertEqual(index['schema_version'], 2)
        graph_rows = {row['id']: row for row in index['tasks'] if row['track'] == 'graph-json'}
        with zipfile.ZipFile(io.BytesIO(self.assets['agent-tasks.zip'])) as bundle:
            for item in self.graphs:
                row = graph_rows[item['id']]
                public = bench.curriculum.graph_prompt(item)['prompt_sha256']
                self.assertEqual(row['prompt_sha256'], public)
                self.assertNotIn('binding_sha256', row)
                prefix = row['prompt_file'].removesuffix('/prompt.json') + '/'
                for name in bundle.namelist():
                    self.assertNotIn(item['binding_sha256'].encode(), bundle.read(name), name)
                for suffix in ('prompt.json', 'response-template.json', 'task.json'):
                    data = json.loads(bundle.read(prefix + suffix))
                    self.assertNotIn('binding_sha256', data)
                    self.assertEqual(data['prompt_sha256'], public)

    def test_lean_descriptor_identifies_the_operator_runtime_not_the_prose_grader(self):
        rows = json.loads(self.assets['task-index.json'])['tasks']
        for row in rows:
            env = json.loads(self.assets[row['task_file']])['environment']
            if row['track'] != 'lean':
                self.assertNotIn('verifier_policy_sha256_lf', env)
                continue
            self.assertIn('operator-provisioned Linux Docker/Landrun', row['verifier'])
            self.assertEqual(env['evaluator_source_sha256_lf'],
                             bench.text_hash(ROOT / 'tools/sog_bench_lean.py'))
            self.assertEqual(env['verifier_policy_sha256_lf'],
                             bench.text_hash(bench.DATA.parent / 'lean-runtime/policy.json'))
            self.assertIs(env['verifier_included'], False)
            self.assertIs(env['hosted_execution'], False)
            instruction = self.assets[row['task_file'].replace('/task.json', '/instruction.md')]
            self.assertIn(b'Never run untrusted Lean on the host', instruction)
            self.assertNotIn(b'not implemented', instruction)

    def test_training_and_expert_data_preserve_original_identity_and_scope(self):
        training = [json.loads(line) for line in self.assets['training-pairs.jsonl'].splitlines()]
        self.assertEqual(len(training), len(bench.prompts(self.cores)))
        for row in training:
            source = next(c for c in self.cores if c['id'] == row['id'])
            self.assertEqual(row['family'], source['family'])
            self.assertEqual(row['split'], source['split'])
            self.assertEqual(row['binding_sha256'], source['binding_sha256'])
            self.assertIn('never an unseen test', row['usage'])
        positions = json.loads(self.assets['expert-graph-positions.json'])
        self.assertEqual(len(positions), len(self.cores))
        self.assertTrue(all(p['anchor_kind'] == 'not-checked' and p['node_id'] is None
                            and p['graph_url'] is None for p in positions))
        self.assertTrue(all(p['declaration'].startswith('AutoSamplingTheory.') for p in positions))
        self.assertTrue(all(p['audience'] == 'expert-review-not-model-input' for p in positions))

    def test_expert_positions_share_the_actual_graph_and_do_not_invent_links(self):
        module_core, exact_core, absent_core = self.cores[:3]
        module = 'module:' + module_core['source_file'].removesuffix('.lean').replace('/', '.')
        exact = 'decl:' + exact_core['declaration']
        assets = bench.task_assets([module_core, exact_core, absent_core], [], graph_ids={module, exact})
        rows = json.loads(assets['expert-graph-positions.json'])
        self.assertEqual([(p['anchor_kind'], p['node_id']) for p in rows],
                         [('owning-module', module), ('declaration', exact), ('not-indexed', None)])
        self.assertIsNone(rows[2]['graph_url'])
        self.assertIn('focus=module%3A', rows[0]['graph_url'])
        self.assertIn('focus=decl%3A', rows[1]['graph_url'])
        self.assertEqual(bench.graph_anchor(module_core['declaration'], module_core['source_file'],
                                           {module, 'decl:' + module_core['declaration']})[0], 'declaration')

    def test_package_bytes_are_repeatable(self):
        self.assertEqual(self.assets, bench.task_assets(self.cores, self.graphs))

    def test_graph_selection_rejects_bad_ids_and_keeps_missing_answers_in_denominator(self):
        identities = [g['id'] for g in self.graphs[:2]]
        selected = bench.selected_graph_tasks(self.graphs, {'task_ids': identities})
        report = bench.curriculum.grade_graph(selected, [])
        self.assertEqual(report['max_points'], 2)
        self.assertEqual(report['points'], 0)
        for invalid in ([], ['unknown'], [identities[0], identities[0]], 'all'):
            with self.assertRaises(ValueError):
                bench.selected_graph_tasks(self.graphs, {'task_ids': invalid})
        self.assertEqual(bench.selected_graph_tasks(self.graphs, {}), self.graphs)


if __name__ == '__main__':
    unittest.main()
