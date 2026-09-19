from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
BUILD_SITE = ROOT / "website" / "scripts" / "build_site.py"
README = ROOT / "README.md"
CITATION = ROOT / "CITATION.bib"
ASTIS_SITE = ROOT / "tools" / "astis_site.py"

class ProjectAuthorsFooterTests(unittest.TestCase):
    def test_no_provisional_project_authors(self) -> None:
        for path in (BUILD_SITE, ASTIS_SITE):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn('Organizer (Authors):', text)
            self.assertNotIn('<p>Organized by ', text)
            self.assertNotIn('CANONICAL_ORGANIZER_FOOTER', text)
            self.assertNotIn('class="organizer-names"', text)

    def test_citation_omits_undecided_authors(self) -> None:
        for path in (README, CITATION):
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, r'(?m)^\s*author\s*=')
            self.assertNotIn('**Project contributors:**', text)

    def test_readme_keeps_peer_library_table(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn("| Library | Primary source |", readme)
        self.assertIn("| Statistical Optimal Transport |", readme)
        self.assertIn("Sinho Chewi", readme)


if __name__ == "__main__":
    unittest.main()
