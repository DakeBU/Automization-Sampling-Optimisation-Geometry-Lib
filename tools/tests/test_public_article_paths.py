"""Public prose removes legacy and configured machine roots without rewriting audits."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import astis

class PublicArticlePathsTests(unittest.TestCase):
    def test_legacy_posix_and_windows_paths(self):
        for value in ('/home/example_owner/project/paper/main.tex',
                      '/Users/example_owner/project/main.tex',
                      '/workspace/repos/example/main.tex',
                      r'D:\Users\example_owner\Desktop\paper.tex',
                      'E:/Users/example_owner/project/main.tex'):
            with self.subTest(value=value):
                output = astis.public_article_text('Source: ' + value)
                self.assertNotIn('example_owner', output)
                self.assertNotIn(value, output)
                self.assertIn('[local source', output)

    def test_environment_configured_source_root(self):
        root = Path.cwd() / 'special_source_root'
        with patch.object(astis, 'SALD_ROOT', root):
            self.assertNotIn('special_source_root', astis.public_article_text(str(root) + '/main.tex'))

    def test_quoted_paths_with_spaces(self):
        for value in ('"/home/Example Owner/project/paper.tex"',
                      r'`D:\Users\Example Owner\Desktop\paper.tex`'):
            output = astis.public_article_text('Source: ' + value)
            self.assertNotIn('Example', output)
            self.assertNotIn('Owner', output)

    def test_relative_or_empty_root_does_not_replace_dots(self):
        value = 'https://example.org/article.pdf and 3.14'
        with patch.object(astis, 'SALD_ROOT', Path('.')):
            self.assertEqual(astis.public_article_text(value), value)

    def test_public_urls_and_relative_code_paths_survive(self):
        value = 'https://example.org/home/article.pdf AutoSamplingTheory/Probability.lean'
        self.assertEqual(astis.public_article_text(value), value)

if __name__ == '__main__':
    unittest.main()
