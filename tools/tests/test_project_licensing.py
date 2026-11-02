"""Exact license distribution, narrow third-party scope and portable reuse."""
import hashlib
import io
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'website/scripts')]
import project_licensing as licensing
import project_news as news


class ProjectLicensingTests(unittest.TestCase):
    def test_news_history_is_uncapped_and_uses_the_readme(self):
        source = '## News\n\n' + '\n'.join(f'- **2026-10-{n:02d}:** Update {n}.' for n in range(20, 0, -1)) + '\n\n## Later\n'
        rendered = news.render(source, 'https://github.com/example/repo')
        self.assertEqual(rendered.count('<li>'), 20)
        self.assertIn('2026-10-01', rendered)
        history = dict(news.rows((ROOT / 'README.md').read_text(encoding='utf-8')))
        self.assertIn('2026-08-29', history)
        self.assertIn('2026-07-17', history)

    def test_full_license_is_unmodified_official_apache_text(self):
        self.assertEqual(hashlib.sha256((ROOT / 'LICENSE').read_bytes()).hexdigest(),
            'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30')

    def test_footer_is_relative_idempotent_and_preserves_attribution(self):
        text = '<footer>Original attribution</footer>'
        once = licensing.footer_link(text, 'textbook/chapter-01/section.html')
        self.assertIn('../../licensing/index.html', once)
        self.assertIn('Original attribution', once)
        self.assertEqual(licensing.footer_link(once, 'textbook/chapter-01/section.html'), once)
        self.assertEqual(licensing.footer_link('<main>source export</main>', 'source.html'), '<main>source export</main>')

    def test_bundles_carry_all_exact_notices(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w') as archive:
            licensing.add_to_archive(archive)
        with zipfile.ZipFile(buf) as archive:
            for name in licensing.LICENSE_FILES:
                self.assertEqual(archive.read(name), (ROOT / name).read_bytes())

    def test_site_copies_license_and_clearly_excludes_external_material(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch.object(licensing.astis_site, 'page', side_effect=lambda title, rel, body: '<main>'+body+'</main><footer>Authors</footer>'), \
             patch.object(licensing.source_lineage, 'canonical_shell', side_effect=lambda text, rel, output: text):
            output = Path(tmp)
            (output / 'index.html').write_text('<main>Home</main><footer>Authors</footer>', encoding='utf-8')
            licensing.enrich_site(output)
            self.assertEqual(licensing.validate_site(output), [])
            text = (output / licensing.PAGE).read_text(encoding='utf-8')
            self.assertIn('933dd38de9423d2967bc36b501b3a2006343000d', text)
            self.assertIn('ATLAS-derived', text)
            self.assertIn('do not extend to unrelated original Samplinglib code', text)
            self.assertIn('does not grant permission to republish', text)
            (output / 'licensing/LICENSE').write_text('stale', encoding='utf-8')
            self.assertTrue(licensing.validate_site(output))


if __name__ == '__main__':
    unittest.main()
