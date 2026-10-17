"""Paper-first presentation preserves the canonical mathematical content."""
import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import samplewiki_navigation as navigation
import samplewiki_reader_contract as reader
import samplewiki_math_render as math_render
import publication_reader


class PaperNavigationTests(unittest.TestCase):
    def test_priority_is_projected_from_execution_not_case_order(self):
        model = navigation.load_model()
        rows = navigation.priority_cases(model)
        self.assertEqual([r['slug'] for r in rows], [
            'proximal-bouncy-particle', 'smoothed-picard-hmc',
            'gaussian-cloud-picard-hmc', 'midpoint-langevin'])
        reordered = copy.deepcopy(model)
        reordered['cases'].reverse()
        self.assertEqual(navigation.priority_cases(reordered), rows)
        self.assertEqual(len(model['cases']), 5)  # Other projects are retained.

    def test_home_has_one_sampling_research_directory(self):
        text = reader.overview_main([], [], {}, {})
        self.assertEqual(text.count('data-paper-id='), 5)
        self.assertIn('id="research-cases"', text)
        self.assertIn('Gaussian Sampling Complexity', text)
        self.assertIn('module-autosamplingtheory-examplecases-gaussiancomplexity-gaussianexpectation.html', text)
        for old_level in ('Sampling papers', 'Companion-paper frontiers', 'Open frontier',
                          'cross-library-state-preparation', 'Schrödinger', 'QuantumComputinglib'):
            self.assertNotIn(old_level, text)
        self.assertNotIn('rceil', text)
        self.assertNotIn('\r', text)
        self.assertIn('not completed paper proofs', text)

    def test_sidebar_has_all_research_cases_without_an_extra_taxonomy(self):
        text = math_render.sidebar_directory('example-cases/samplewiki.html', [])
        self.assertEqual(text.count('data-paper-directory="true"'), 1)
        for row in navigation.research_cases():
            self.assertIn(row['slug'] + '.html', text)
        self.assertIn('<h2>SampleWiki</h2>', text)
        self.assertNotIn('Sampling papers', text)
        self.assertNotIn('Open frontier', text)
        self.assertNotIn('SampleWiki contents', text)
        self.assertNotIn('<details class="sw-setting-directory" open', text)

    def test_scheduling_priority_does_not_hide_other_projects(self):
        model = navigation.load_model()
        self.assertEqual(len(navigation.priority_cases(model)), 4)
        self.assertEqual({r['id'] for r in navigation.research_cases(model)},
                         {r['id'] for r in model['cases']})

    def test_old_frontier_is_only_a_compatibility_entry(self):
        text = reader.frontier_main([], {}, {})
        self.assertIn('unified research directory', text)
        self.assertNotIn('<h1>Sampling frontier</h1>', text)

    def test_existing_lesson_links_back_to_its_samplewiki_result(self):
        model = navigation.load_model()
        row = next(r for r in model['cases'] if r['id'] == 'ASTIS-SW-GAUSSIAN-COMPLEXITY-2026')
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / row['reader_links'][0]['path']
            target.parent.mkdir(parents=True)
            original = '<main id="content"><h1>Exact lesson</h1><div>UNCHANGED-PROOF</div></main>'
            target.write_text(original, encoding='utf-8')
            navigation.attach_research_context(Path(tmp), model)
            once = target.read_text(encoding='utf-8')
            self.assertIn('gaussian-sampling-complexity.html', once)
            self.assertIn('>SampleWiki</a>', once)
            self.assertIn('UNCHANGED-PROOF', once)
            navigation.attach_research_context(Path(tmp), model)
            self.assertEqual(target.read_text(encoding='utf-8'), once)

    def test_research_context_cannot_write_outside_the_site(self):
        model = navigation.load_model()
        row = next(r for r in model['cases'] if r['id'] == 'ASTIS-SW-GAUSSIAN-COMPLEXITY-2026')
        row['reader_links'][0]['path'] = '../outside.html'
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'inside generated site'):
                navigation.attach_research_context(Path(tmp), model)

    def test_directory_injection_is_idempotent(self):
        original = '<aside><details class="book-nav"><summary>Books</summary></details></aside>'
        once = navigation.inject_paper_directory(original, 'example-cases/samplewiki.html')
        self.assertEqual(navigation.inject_paper_directory(once, 'example-cases/samplewiki.html'), once)

    def test_late_companion_shell_without_book_directory(self):
        original = '<aside><section class="sidebar-group sidebar-libraries">Libraries</section></aside>'
        text = navigation.inject_paper_directory(original, 'example-cases/samplewiki/companions/test.html')
        self.assertLess(text.index('data-paper-directory'), text.index('sidebar-libraries'))

    def test_checked_work_links_full_source_proof_without_loading_it_in_the_index(self):
        item = {'id': 'test-source', 'title': 'An exact source statement', 'bindings': [{'declaration': 'Test.exact'}]}
        data = {'lessons': {'Test.exact': {'title': 'Exact mathematical proof'}}}
        with patch.object(publication_reader.publication, 'inputs', return_value=data), \
             patch.object(publication_reader.publication, 'verified_binding', return_value=True), \
             patch.object(publication_reader, 'source_card', return_value='<section>EXACT-PROOF-AND-LEAN</section>'):
            text = publication_reader.companion_publication_block([item], 'example-cases/samplewiki/companions/test.html')
        self.assertEqual(text.count('id="paper-lean-progress"'), 1)
        self.assertIn('<details class="paper-verified-index">', text)
        self.assertIn('<details class="paper-verified-unit"', text)
        self.assertNotIn('EXACT-PROOF-AND-LEAN', text)
        self.assertIn('proofs/source-test-source.html', text)
        self.assertIn('Read full statement and proof', text)
        self.assertIn('data-proof-declaration="Test.exact"', text)
        self.assertIn('1 independently reviewed', text)
        self.assertIn('not completed paper results', text)
        self.assertNotIn('<details open', text)


if __name__ == '__main__':
    unittest.main()
