from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website" / "scripts"))

import chewi_source_first_contract as contract
import chewi_source_first_refinement as refinement


class InlineMathRefinementTests(unittest.TestCase):
    def test_known_ascii_assumption_math_is_mathjax(self) -> None:
        self.assertEqual(refinement.mathify("c >= 0"), r"\(c\ge 0\)")
        self.assertEqual(
            refinement.mathify("every path t -> A_t is continuous and nondecreasing"),
            r"every path \(t\mapsto A_t\) is continuous and nondecreasing",
        )
        self.assertEqual(
            refinement.mathify("tau_m <= tau_n"),
            r"\(\tau_m\le\tau_n\)",
        )

    def test_refinement_keeps_audit_packet_out_of_reader_prose(self) -> None:
        refinement.patch(contract)
        source = {
            "source_kind": "Definition 1.1.4",
            "source_summary": "A martingale is adapted and integrable.",
            "source_url": "https://example.com/source.pdf",
            "latex_statement": r"0\le s\le t\Longrightarrow \mathbb E[M_t\mid\mathcal F_s]=M_s",
            "source_assumptions": ["an adapted process"],
            "formal_assumptions": ["Martingale M filtration mu", "s <= t"],
            "rigorous_packet": "INTERNAL AUDIT PROSE t <= T SHOULD NOT APPEAR",
            "lean_declarations": ["AutoSamplingTheory.Example.martingale"],
        }
        card = contract._render_source_card(
            "martingale", source, {}, {}, {}
        )
        self.assertNotIn("INTERNAL AUDIT PROSE", card)
        self.assertIn("Conditions made explicit by ASTIS", card)
        self.assertIn("<code>s &lt;= t</code>", card)

    def test_implicit_assumptions_render_relations_inside_mathjax(self) -> None:
        refinement.patch(contract)
        item = {
            "id": "implicit-1-1-hitting-time-stopping",
            "title": "First hitting time",
            "why_needed": "A stopping-time condition is required.",
            "latex_statement": r"\{\tau_c\le t\}\in\mathcal F_t",
            "assumptions": [
                "every path t -> A_t is continuous and nondecreasing",
                "c >= 0",
            ],
            "lean_declarations": [],
        }
        card = contract._render_implicit_card(item, {})
        self.assertIn(r"\(t\mapsto A_t\)", card)
        self.assertIn(r"\(c\ge 0\)", card)
        self.assertEqual(refinement._scan_visible_math(contract, card), [])


class BlockAwareMathLintTests(unittest.TestCase):
    def test_reports_nearest_source_id_for_raw_math(self) -> None:
        html = (
            '<section class="source-contract-card" data-source-id="definition-1-1-4">'
            '<p>For s &lt;= t, M_t is adapted to F_t.</p>'
            '</section>'
        )
        issues = refinement._scan_visible_math(contract, html)
        self.assertTrue(issues)
        self.assertTrue(all("[definition-1-1-4]" in issue for issue in issues))
        self.assertTrue(any("ASCII relation/operator" in issue for issue in issues))
        self.assertTrue(any("raw subscript notation" in issue for issue in issues))

    def test_mathjax_and_code_are_not_reported_as_raw_math(self) -> None:
        html = (
            '<article id="clean-card">'
            r'<p>For \(0\le s\le t\), the defining identity is '
            r'\(\mathbb E[M_t\mid\mathcal F_s]=M_s\).</p>'
            '<code>M_t &lt;= F_t</code>'
            r'<div class="formula">\[X_t=X_0+B_t\]</div>'
            '</article>'
        )
        self.assertEqual(refinement._scan_visible_math(contract, html), [])

    def test_configured_dollar_math_is_not_raw_prose(self) -> None:
        html = (r'<p>The martingale $M_t$ starts at $M_0=0$.</p>'
                r'<p>$$X_t=X_0+B_t$$</p>')
        self.assertEqual(refinement._scan_visible_math(contract, html), [])

    def test_dollar_math_does_not_hide_raw_or_unmatched_prose(self) -> None:
        for text in (r'$M_t$ but F_t is raw', r'$M_t is unclosed',
                     r'\$M_t \$ is escaped', r'$$M_t is unclosed'):
            with self.subTest(text=text):
                self.assertTrue(refinement._scan_visible_math(contract, '<p>'+text+'</p>'))

    def test_dollar_math_handles_escapes_and_line_breaks(self) -> None:
        for text in (r'$M_t+\$1$', '$M_t\n+N_t$', r'\\$M_t$',
                     r'$$M_t+\$1$$', r'\\$$M_t$$'):
            with self.subTest(text=text):
                self.assertEqual(refinement._scan_visible_math(contract, '<p>'+text+'</p>'), [])
        for text in (r'\$M_t\$', r'\\\$M_t\$', r'\$$M_t\$$',
                     r'$M_t+\$1$ outside F_t', r'$$M_t+\$1$$ outside F_t'):
            with self.subTest(text=text):
                self.assertTrue(refinement._scan_visible_math(contract, '<p>'+text+'</p>'))


if __name__ == "__main__":
    unittest.main()
