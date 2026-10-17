"""Paper-first presentation preserves the canonical mathematical content."""
import copy
import sys
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

    def test_home_puts_four_links_before_closed_cross_library_pointer(self):
        text = reader.overview_main([], [], {}, {})
        self.assertEqual(text.count('data-paper-id='), 4)
        self.assertLess(text.index('id="sampling-papers"'),
                        text.index('id="cross-library-state-preparation"'))
        self.assertIn('<details class="sw-secondary-reading" id="cross-library-state-preparation">', text)
        self.assertNotIn('rceil', text)
        self.assertNotIn('\r', text)
        self.assertIn('not completed paper proofs', text)

    def test_sidebar_has_four_direct_papers_and_closed_settings(self):
        text = math_render.sidebar_directory('example-cases/samplewiki.html', [])
        self.assertEqual(text.count('data-paper-directory="true"'), 1)
        for row in navigation.priority_cases():
            self.assertIn(row['slug'] + '.html', text)
        self.assertNotIn('<details class="sw-setting-directory" open', text)

    def test_directory_injection_is_idempotent(self):
        original = '<aside><details class="book-nav"><summary>Books</summary></details></aside>'
        once = navigation.inject_paper_directory(original, 'example-cases/samplewiki.html')
        self.assertEqual(navigation.inject_paper_directory(once, 'example-cases/samplewiki.html'), once)

    def test_late_companion_shell_without_book_directory(self):
        original = '<aside><section class="sidebar-group sidebar-libraries">Libraries</section></aside>'
        text = navigation.inject_paper_directory(original, 'example-cases/samplewiki/companions/test.html')
        self.assertLess(text.index('data-paper-directory'), text.index('sidebar-libraries'))

    def test_checked_work_is_folded_without_dropping_source_card(self):
        item = {'title': 'An exact source statement', 'bindings': [{'declaration': 'Test.exact'}]}
        with patch.object(publication_reader.publication, 'inputs', return_value={}), \
             patch.object(publication_reader.publication, 'verified_binding', return_value=True), \
             patch.object(publication_reader, 'source_card', return_value='<section>EXACT-PROOF-AND-LEAN</section>'):
            text = publication_reader.companion_publication_block([item], 'example-cases/samplewiki/companions/test.html')
        self.assertEqual(text.count('id="paper-lean-progress"'), 1)
        self.assertIn('<details class="paper-verified-index">', text)
        self.assertIn('<details class="paper-verified-unit">', text)
        self.assertIn('EXACT-PROOF-AND-LEAN', text)
        self.assertIn('Read focused proof', text)
        self.assertIn('1 independently reviewed', text)
        self.assertIn('not completed paper results', text)
        self.assertNotIn('<details open', text)


if __name__ == '__main__':
    unittest.main()
