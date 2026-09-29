from pathlib import Path
import ast
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
BUILD_SITE = ROOT / "website" / "scripts" / "build_site.py"
README = ROOT / "README.md"
CITATION = ROOT / "CITATION.bib"
ASTIS_SITE = ROOT / "tools" / "astis_site.py"

class ProjectAuthorsFooterTests(unittest.TestCase):
    def test_footer_removal_preserves_primary_source_authors(self) -> None:
        tree = ast.parse(BUILD_SITE.read_text(encoding="utf-8"))
        names = {"ORGANIZER_FOOTER_INPUTS", "PROVISIONAL_ORGANIZER_FOOTER"}
        nodes = [n for n in tree.body if
                 (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))
                 or (isinstance(n, ast.FunctionDef) and n.name == "repair_project_author_footer")]
        scope = {"Path": Path}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), "<footer-test>", "exec"), scope)
        source = "<p>Primary source: Sinho Chewi; Fan Chen; Jianfeng Lu; Matthew S. Zhang.</p>"
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            for footer in (*scope["ORGANIZER_FOOTER_INPUTS"], scope["PROVISIONAL_ORGANIZER_FOOTER"]):
                page.write_text(source + footer, encoding="utf-8")
                scope["repair_project_author_footer"](Path(tmp))
                self.assertEqual(page.read_text(encoding="utf-8"), source)

    def test_public_surfaces_do_not_assert_provisional_authorship(self) -> None:
        for path in (README, CITATION, ASTIS_SITE):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("Dake Bu and Ji Cheng", text)
            self.assertNotIn("Dake Bu · Ji Cheng", text)
            self.assertNotIn("Organized by Dake Bu", text)

    def test_readme_keeps_peer_library_table(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn("| Library | Primary source |", readme)
        self.assertIn("| Statistical Optimal Transport |", readme)
        self.assertIn("Sinho Chewi", readme)


if __name__ == "__main__":
    unittest.main()
