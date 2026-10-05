"""Reader integrity, not an independent mathematical/source certification."""
import copy
import sys
import unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "website/scripts"), str(ROOT / "tools")]
import proof_readers as reader
import inline_lean
import declaration_lessons as lessons


class ProofReaderTests(unittest.TestCase):
    def setUp(self):
        self.items = reader.load_items()
        names = {n for i in self.items for n in i['declarations'] + i['astis_dependencies']}
        self.data = {'gate': {'passed': True}, 'declarations': [
            {'full_name': n, 'local_status': 'Compiled', 'has_placeholder': False,
             'registry_status': ''} for n in names]}

    def test_all_steps_have_equations_and_lean_correspondence(self):
        self.assertEqual(len(self.items), 3)
        self.assertEqual(sum(len(i['steps']) for i in self.items), 13)
        self.assertEqual(sum(len(i['theorems']) for i in self.items), 5)
        for item in self.items:
            self.assertTrue((ROOT / item['test']).is_file())
            for step in item['steps']:
                self.assertTrue(all(step[k] for k in ('text', 'formula', 'lean')))

    def test_statement_split_respects_defaults_and_comments(self):
        source = 'theorem f (x : Nat := 0) /- := ignored -/ : x = x := by rfl'
        statement, proof = inline_lean.split_statement(source)
        self.assertEqual(statement, 'theorem f (x : Nat := 0) /- := ignored -/ : x = x')
        self.assertEqual(proof, ':= by rfl')

    def test_display_source_drops_only_following_top_level_docstring(self):
        source = 'def f : Nat := 1\n\n/-- Documentation for the next declaration. -/'
        self.assertEqual(inline_lean.display_source(source), 'def f : Nat := 1')
        nested = 'structure R where\n  /-- Documentation for a field. -/\n  n : Nat'
        self.assertEqual(inline_lean.display_source(nested), nested)

    def test_structure_defaults_do_not_truncate_its_specification(self):
        source = 'structure R where\n  n : Nat := 0\n  title : String\n'
        self.assertEqual(inline_lean.split_statement(source), (source, ''))
        self.assertEqual(inline_lean.split_statement('def r : R where\n  n := 1\n  title := "a"')[0], 'def r : R')

    def test_statement_retains_nested_local_definitions(self):
        source = ('theorem local_result : let x := let y := 1; y; '
                  'let z := x + 1; z = 2 := by rfl')
        statement, proof = inline_lean.split_statement(source)
        self.assertTrue(statement.endswith('let z := x + 1; z = 2'))
        self.assertEqual(proof, ':= by rfl')

    def test_local_keywords_inside_names_are_not_definitions(self):
        for name in ('«let»', 'Demo.have'):
            source = f'theorem {name} : True := by trivial'
            self.assertEqual(inline_lean.split_statement(source),
                             (f'theorem {name} : True', ':= by trivial'))
        source = 'theorem f : Demo.have «let» := by assumption'
        self.assertEqual(inline_lean.split_statement(source),
                         ('theorem f : Demo.have «let»', ':= by assumption'))

    def test_unrecognized_local_equations_preserve_complete_source(self):
        source = 'theorem f : let g | 0 => 0 | n+1 => n; g 0 = 0 := by rfl'
        self.assertEqual(inline_lean.split_statement(source), (source, ''))

    def test_recursive_depth_disclosure_keeps_all_conclusions(self):
        source = (ROOT / 'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/RecursiveDepth.lean').read_text(encoding='utf-8')
        source = source[source.index('theorem parameter_control'):]
        statement, proof = inline_lean.split_statement(source)
        self.assertIn('Nat.rec r₀', statement)
        self.assertIn('Antitone (fun n => K (r n))', statement)
        self.assertIn('∀ B : ℝ, 0 < B → ∃ J : ℕ', statement)
        self.assertTrue(statement.endswith('(r J)⁻¹ ≤ B)'))
        self.assertTrue(proof.startswith(':= by\n'))

    def test_every_theorem_requires_separate_statement_and_proof(self):
        items = copy.deepcopy(self.items)
        items[0]['theorems'].pop()
        with patch.object(reader, 'read_json', return_value=items):
            with self.assertRaisesRegex(ValueError, 'every declaration'):
                reader.load_items()

    def test_fisher_source_mismatch_cannot_be_hidden_by_compilation(self):
        ev = reader.evidence(self.items[0], self.data)
        self.assertTrue(ev['compiled'])
        self.assertEqual(ev['source_verdict'], 'domain-mismatch')
        self.assertEqual(ev['source_review'], 'needs-revision')
        self.assertEqual(ev['registry_entries'], 0)

    def test_stale_gate_cannot_be_blue(self):
        self.data['gate']['passed'] = False
        self.assertFalse(reader.evidence(self.items[0], self.data)['compiled'])

    def test_placeholder_cannot_be_blue(self):
        name = self.items[0]['declarations'][0]
        next(d for d in self.data['declarations'] if d['full_name'] == name)['has_placeholder'] = True
        self.assertFalse(reader.evidence(self.items[0], self.data)['compiled'])

    def test_noncompiled_declaration_cannot_be_blue(self):
        name = self.items[0]['declarations'][0]
        next(d for d in self.data['declarations'] if d['full_name'] == name)['local_status'] = 'Partial'
        self.assertFalse(reader.evidence(self.items[0], self.data)['compiled'])

    def test_unknown_decl_is_an_error_not_a_search_fallback(self):
        item = copy.deepcopy(self.items[0])
        item['declarations'].append('Invented.theorem')
        with self.assertRaisesRegex(ValueError, 'unknown declaration'):
            reader.evidence(item, self.data)

    def test_invalid_metadata_is_rejected(self):
        items = copy.deepcopy(self.items)
        items[0]['steps'][0]['formula'] = ''
        with patch.object(reader, 'read_json', return_value=items):
            with self.assertRaisesRegex(ValueError, 'incomplete proof step'):
                reader.load_items()

    def test_mathlib_urls_pin_real_source_files_and_lines(self):
        prefix = 'https://github.com/leanprover-community/mathlib4/blob/'
        for item in self.items:
            for dep in item['mathlib_dependencies']:
                self.assertTrue(dep['url'].startswith(prefix))
                sha, path = dep['url'][len(prefix):].split('/', 1)
                self.assertEqual(sha, 'db584cd6d46c92f209a44c0f1c829460d327499d')
                file, line = path.split('#L')
                local = ROOT / '.lake/packages/mathlib' / file
                if local.exists():
                    source_line = local.read_text(encoding='utf-8').splitlines()[int(line)-1]
                    self.assertIn(dep['name'].rsplit('.', 1)[-1], source_line)

    def test_local_and_external_sources_use_distinct_commit_pins(self):
        check = reader.base.source_commit_link_error
        root = 'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib'
        commit = 'a' * 40
        self.assertIsNone(check(root + '/blob/' + commit + '/A.lean', commit, root))
        self.assertIsNotNone(check(root + '/blob/main/A.lean', commit, root))
        self.assertIsNotNone(check(root + '/blob/' + 'b'*40 + '/A.lean', commit, root))
        external = 'https://github.com/leanprover-community/mathlib4/blob/'
        self.assertIsNone(check(external + 'b'*40 + '/A.lean', commit, root))
        self.assertIsNotNone(check(external + 'master/A.lean', commit, root))


class DeclarationLessonTests(unittest.TestCase):
    def test_structure_accessors_are_not_invented_theorem_leaves(self):
        known = {'A.Domain': SimpleNamespace(kind='structure', source_text='structure Domain : Prop where\n  integrable : P\n')}
        projection = {'structure': 'A.Domain', 'field': 'integrable', 'role': 'Read the supplied premise.'}
        lessons.validate_projection(projection, known)
        with self.assertRaisesRegex(ValueError, 'Unknown structure field'):
            lessons.validate_projection({**projection, 'field': 'invented'}, known)
        with self.assertRaisesRegex(ValueError, 'Unknown projection structure'):
            lessons.validate_projection({**projection, 'structure': 'A.Unknown'}, known)

    def test_case_sensitive_lean_names_cannot_overwrite_each_other(self):
        self.assertNotEqual(lessons.lesson_path('A.DvVariationalFormulaInterface'), lessons.lesson_path('A.dvVariationalFormulaInterface'))
        self.assertNotEqual(lessons.lesson_path('A.foo'), lessons.lesson_path("A.foo'"))
        self.assertLess(len(lessons.lesson_path('A.' + 'x'*400).rsplit('/', 1)[-1]), 200)

    def test_authored_schema_requires_real_steps_not_just_source(self):
        units = lessons.load_units()
        self.assertGreaterEqual(len(units), 17)
        for unit in units:
            self.assertNotEqual(unit['lean_statement'], unit.get('source_text'))
            self.assertFalse(unit['lean_proof'].lstrip().startswith('by\n'))
            self.assertTrue(all(s['formula'] and s['text'] and s['lean'] for s in unit['steps']))
        self.assertEqual(len({lessons.lesson_path(u['declaration']) for u in units}), len(units))

    def test_local_sources_are_portable_and_browser_readable(self):
        href = lessons.source_link({'path': 'AutoSamplingTheory/Probability.lean', 'line': 7}, 'lessons/test.html')
        self.assertEqual(href, '../data/lesson-sources/AutoSamplingTheory/Probability.lean.html#L7')
        for raw in ('../outside', '/etc/passwd', 'D:/private/source.lean'):
            with self.assertRaises(ValueError):
                lessons.source_link({'path': raw}, 'lessons/test.html')
        with self.assertRaises(ValueError):
            lessons.source_link({'url': 'file:///private'}, 'lessons/test.html')

    def test_mathlib_sources_follow_lockfile_not_astis_commit(self):
        href = lessons.source_link({'path': '.lake/packages/mathlib/Mathlib/Probability/Kernel/Invariance.lean', 'line': 50}, 'lessons/test.html')
        self.assertIn('/blob/' + lessons.mathlib_pin() + '/Mathlib/', href)
        self.assertTrue(href.endswith('#L50'))

    def test_coverage_includes_definitions_but_never_claims_notes_are_complete(self):
        data = {'teaching_declarations': [{'declaration': 'A.noted'}], 'declarations': [
            {'full_name': name, 'kind': kind, 'module': module, 'local_status': 'Compiled', 'page': 'modules/a.html'}
            for name, kind, module in [('A.noted', 'theorem', 'A'), ('A.contract', 'def', 'A'), ('Tests.t', 'theorem', 'Tests.A')]]}
        rows = lessons.coverage(data, [])
        self.assertEqual(len(rows), 2)
        self.assertEqual([r['exposition'] for r in rows], ['existing-notes', 'needed'])
        self.assertEqual(rows[1]['kind'], 'def')

    def test_balanced_math_block_does_not_consume_neighbor_proof(self):
        value = '<div class="statement"><div>nested</div></div><div class="proof">proof</div>'
        a, b = inline_lean.block_bounds(value, 'statement')
        self.assertEqual(value[a:b], '<div class="statement"><div>nested</div></div>')

    def test_inline_code_escapes_once_without_eating_tex(self):
        self.assertEqual(lessons.inline_text('Use `x < y` and \\(x\\).'), 'Use <code>x &lt; y</code> and \\(x\\).')

    def test_reviewed_measure_boundaries_survive_import(self):
        units = {u['declaration'].rsplit('.', 1)[-1]: u for u in lessons.load_units()}
        statement = units['fst_compProd_condDistrib_snd_eq_self']['lean_statement']
        self.assertIn('general finite', statement)
        self.assertIn('measurable kernel', statement)
        step = units['heatBathSnd_invariant']['steps'][2]['text']
        self.assertIn('compProd_eq_comp_prod', step)
        self.assertIn('s-finite', step)


if __name__ == '__main__':
    unittest.main()
