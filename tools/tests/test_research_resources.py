"""External inventory completeness, honest status and existing-reader reuse."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import research_resources as intake
import resource_library as reader


class ResourceTests(unittest.TestCase):
    def test_complete_pinned_inventory(self):
        data = intake.load()
        self.assertEqual([len(s['items']) for s in data['forum']['sections']], [9, 1, 1, 12, 67, 43])
        self.assertEqual(len(data['optlib']['modules']), 41)
        self.assertEqual(len(data['optlib']['readme_resources']), 35)
        self.assertEqual(data['optlib']['toolchain'], 'leanprover/lean4:v4.13.0')

    def test_external_items_cannot_be_promoted_by_catalog(self):
        data = deepcopy(intake.load())
        data['forum']['sections'][0]['items'][0]['status'] = 'compiled'
        with self.assertRaisesRegex(ValueError, 'local Lean credit'):
            intake.validate(data)

    def test_all_existing_library_paths_match_canonical_coverage(self):
        guide = reader.guides()
        canonical = json.loads((ROOT / 'research-wiki/openai-math-textbook-coverage.json').read_text(encoding='utf-8'))
        self.assertEqual({l['index_path'] for l in canonical['libraries']}, {l['path'] for l in guide['libraries'].values()})
        self.assertEqual({key for s in guide['subjects'] for key in s['libraries']}, set(guide['libraries']))

    def test_parser_ignores_navigation_and_preserves_math(self):
        html = '<a href="https://ignored.test">Nav</a><time datetime="2026-10-30"></time>'
        for section in intake.ALLOWED:
            html += f'<section class="resource-section" aria-labelledby="{section}"><h2><span>{section}</span></h2><ol><li><a href="https://example.test/{section}">Rate $O(1/T)$ &amp; proof</a> (Oct 3, 2026)</li></ol></section>'
        data = intake.parse_forum(html.encode())
        self.assertEqual(len(data['sections']), 6)
        self.assertEqual(data['sections'][0]['items'][0]['title'], 'Rate $O(1/T)$ & proof')
        self.assertEqual(data['sections'][0]['items'][0]['listed_date'], '2026-10-03')
        self.assertIn(r'\(O(1/T)\)', reader.render_entries(data['sections'][0]['items']))
        with self.assertRaisesRegex(ValueError, 'structure changed'):
            intake.parse_forum(b'<main>No recognized resource sections</main>')

    def test_urls_are_escaped_and_no_fake_blue(self):
        rows = [{'title': '<script> $x^2$', 'url': 'https://example.test/?a=1&b=2', 'status': 'external-reference'}]
        text = reader.render_entries(rows)
        self.assertNotIn('<script>', text)
        self.assertIn('a=1&amp;b=2', text)
        self.assertNotIn('status-blue', text)

    def test_optlib_matches_are_existing_lessons_not_copied_proofs(self):
        matches = reader.existing_optlib_matches()
        self.assertGreater(len(matches), 0)
        text = reader.optlib_page(reader.guides(), intake.load())
        for unit in matches:
            self.assertIn(unit['page'], text)
        self.assertIn('not necessarily a code port', text)
        self.assertNotIn('language-lean', text)

    def test_geometry_discovery_does_not_claim_semantic_review(self):
        data = intake.load()
        rows = reader.discover_geometry(data)
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(r['status'] == 'external-reference' for r in rows))
        guide = next(s for s in reader.guides()['subjects'] if s['id'] == 'geometry')
        self.assertIn('Title-based suggestions', reader.subject_page(guide, reader.guides(), data))


if __name__ == '__main__':
    unittest.main()
