from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "website" / "scripts"))

import lean_tutor  # noqa: E402
import reader_contract_final  # noqa: E402


class LeanTutorPostBuildTests(unittest.TestCase):
    def make_output(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        output = Path(temp.name)
        assets = output / "assets"
        assets.mkdir(parents=True)
        (assets / "lean-tutor.css").write_text(".lean-learning-studio{}\n", encoding="utf-8")
        (assets / "lean-tutor.js").write_text("(() => {})();\n", encoding="utf-8")
        (assets / "module-lean-tutor.js").write_text("(() => {})();\n", encoding="utf-8")
        (assets / "module-lean-tutor.css").write_text(".module-lean-tutor-panel{}\n", encoding="utf-8")

        theorem_dir = output / "theorems"
        theorem_dir.mkdir()
        (theorem_dir / "sample.html").write_text(
            "<html><head></head><body><section class=\"theorem-layout\"><article>"
            "<h2>Plain-English statement</h2><p>sample</p>"
            "<h2>Lean statement</h2><pre><code class=\"language-lean\">theorem sample : True := by trivial</code></pre>"
            "</article></section></body></html>",
            encoding="utf-8",
        )

        declarations = output / "declarations"
        declarations.mkdir()
        (declarations / "index.html").write_text("<html></html>", encoding="utf-8")

        modules = output / "modules"
        modules.mkdir()
        (modules / "sample.html").write_text(
            '<html><head></head><body><div class="declaration-list">'
            '<details class="declaration"><summary><code>Sample.helper</code></summary>'
            '<div class="declaration-content"><pre><code class="language-lean">lemma helper : True := by trivial</code></pre></div>'
            '</details></div></body></html>',
            encoding="utf-8",
        )
        return temp, output

    def test_injects_reading_modes_graph_line_tutor_and_module_tutor(self) -> None:
        temp, output = self.make_output()
        self.addCleanup(temp.cleanup)
        self.assertEqual(lean_tutor.enrich_site(output), 2)
        text = (output / "theorems" / "sample.html").read_text(encoding="utf-8")
        self.assertIn('data-reading-mode="beginner"', text)
        self.assertIn('data-reading-mode="rigorous"', text)
        self.assertIn('data-reading-mode="lean"', text)
        self.assertIn('data-graph-mode="tree"', text)
        self.assertIn('data-graph-mode="network"', text)
        self.assertIn("data-lean-line-tutor", text)
        self.assertIn("lean-tutor.css", text)
        self.assertIn("lean-tutor.js", text)
        module_text = (output / "modules" / "sample.html").read_text(encoding="utf-8")
        self.assertIn("lean-tutor.css", module_text)
        self.assertIn("module-lean-tutor.js", module_text)
        self.assertEqual(lean_tutor.validate_site(output), [])

    def test_enrichment_is_idempotent(self) -> None:
        temp, output = self.make_output()
        self.addCleanup(temp.cleanup)
        lean_tutor.enrich_site(output)
        lean_tutor.enrich_site(output)
        text = (output / "theorems" / "sample.html").read_text(encoding="utf-8")
        self.assertEqual(text.count(lean_tutor.START), 1)
        self.assertEqual(text.count(lean_tutor.END), 1)
        self.assertEqual(text.count("lean-tutor.css"), 1)
        self.assertEqual(text.count("lean-tutor.js"), 1)
        module_text = (output / "modules" / "sample.html").read_text(encoding="utf-8")
        self.assertEqual(module_text.count("lean-tutor.css"), 1)
        self.assertEqual(module_text.count("module-lean-tutor.js"), 1)

    def test_tutor_does_not_choose_language_from_preferences(self) -> None:
        markup = lean_tutor.studio_html()
        self.assertIsNone(lean_tutor.CJK_RE.search(markup))
        self.assertNotIn("data-lean-language-toggle", markup)
        for name in ("lean-tutor.js", "module-lean-tutor.js"):
            script = (ROOT / "website" / "static" / name).read_text(encoding="utf-8")
            self.assertIsNone(lean_tutor.CJK_RE.search(script), name)
            self.assertNotIn("samplinglib-lean-language", script, name)
            self.assertNotIn("navigator.language", script, name)

    def test_public_language_gate_covers_folded_copy_and_accessible_labels(self) -> None:
        check = reader_contract_final.validate_page
        path = Path("sample.html")
        self.assertEqual(check(path, '<html lang="en"><details><summary>Proof</summary>'
                                     '<pre><code>-- 原样源码\n∀ x, x ≤ x</code></pre>'
                                     '</details></html>'), [])
        for markup in (
            '<html><p>Proof</p></html>',
            '<html lang="zh"><p>Proof</p></html>',
            '<html lang="en"><p lang="fr">Proof</p></html>',
            '<html lang="en"><details><summary>证明</summary></details></html>',
            '<html lang="en"><button aria-label="&#35777;&#26126;">Proof</button></html>',
        ):
            with self.subTest(markup=markup):
                self.assertTrue(check(path, markup))


if __name__ == "__main__":
    unittest.main()
