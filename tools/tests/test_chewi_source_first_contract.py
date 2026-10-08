from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website" / "scripts"))

import chewi_source_first_contract as contract
import chewi_source_first_refinement as refinement

refinement.patch(contract)


class RawMathGateTests(unittest.TestCase):
    def test_tensor_prose_is_not_an_unrendered_formula(self) -> None:
        for value in ("Its square-root and tensor-slot producers remain open.",
                      "Tensor products encode joint seed coordinates.",
                      "No paper-specific tensor-slot adapter is proved."):
            with self.subTest(value=value):
                self.assertEqual(contract._raw_math_errors(value), [])

    def test_ascii_tensor_infix_still_requires_math_rendering(self) -> None:
        for value in ("The law is mu tensor gamma.", "Use v tensor Z.",
                      "The input is X_1 tensor Y_2."):
            with self.subTest(value=value):
                self.assertIn("raw tensor-product notation", contract._raw_math_errors(value))

    def test_rejects_martingale_ascii_exposition(self) -> None:
        value = (
            "For s <= t, E[M_t | F_s] = M_s almost everywhere, and M_t is measurable "
            "with respect to F_t."
        )
        self.assertTrue(contract._raw_math_errors(value))

    def test_rejects_raw_omega_energy_formula(self) -> None:
        self.assertTrue(
            contract._raw_math_errors(
                "For f(omega,t)=|eta_t(omega)|^2 this is the required energy bridge."
            )
        )

    def test_accepts_plain_mathematical_prose(self) -> None:
        self.assertEqual(
            contract._raw_math_errors(
                "Apply Tonelli's theorem to the nonnegative measurable integrand."
            ),
            [],
        )


class SourceCardContractTests(unittest.TestCase):
    def test_card_order_and_folded_astis_layers(self) -> None:
        source = {
            "source_kind": "Theorem 1.2.3",
            "source_summary": "A source-faithful summary.",
            "page": "book 10 / PDF 22",
            "wording_status": "faithful paraphrase",
            "source_url": "https://example.com/source.pdf#page=22",
            "latex_statement": r"x=y",
            "source_assumptions": ["a source-level assumption"],
            "formal_assumptions": ["FormalPredicate x"],
            "rigorous_packet": "ASTIS makes the omitted regularity condition explicit.",
            "lean_declarations": ["AutoSamplingTheory.Example.theorem"],
            "proof_leaves": [
                {"declarations": ["leaf_one", "leaf_two"]}
            ],
        }
        proof = {
            "source_status": "source_proof",
            "steps": [
                {"formula": r"x=z", "lean": ["leaf_one"]},
                {"formula": r"z=y", "lean": ["leaf_two"]},
            ],
        }
        card = contract._render_source_card(
            "source-id",
            source,
            {},
            {"source-id": proof},
            {},
        )
        statement_at = card.index("source-contract-chewi-statement")
        proof_at = card.index("source-contract-chewi-proof")
        assumptions_at = card.index("source-contract-hidden-assumptions")
        astis_at = card.index("source-contract-astis-latex")
        lean_at = card.index("source-contract-lean")
        self.assertLess(statement_at, proof_at)
        self.assertLess(proof_at, assumptions_at)
        self.assertLess(assumptions_at, astis_at)
        self.assertLess(astis_at, lean_at)
        self.assertNotIn('source-contract-astis-latex" open', card)
        self.assertNotIn('source-contract-lean" open', card)
        self.assertIn("<h3>Statement</h3>", card)
        self.assertIn("<h3>Proof / derivation</h3>", card)
        self.assertNotIn("<h3>Chewi statement</h3>", card)
        self.assertNotIn("<h3>Chewi proof / derivation</h3>", card)
        self.assertIn("ASTIS rigorous LaTeX formalization", card)
        self.assertIn("Lean formalization", card)

    def test_internal_exposition_is_not_rendered(self) -> None:
        source = {
            "source_kind": "Definition 1.1.4",
            "source_summary": "A martingale is an adapted integrable process.",
            "source_url": "https://example.com/source.pdf",
            "latex_statement": r"0\le s\le t\Longrightarrow \mathbb E[M_t\mid\mathcal F_s]=M_s",
            "mathematical_exposition": "For s <= t, E[M_t | F_s] = M_s",
            "astis_exposition": "Internal implementation prose.",
            "source_assumptions": ["an adapted process"],
            "formal_assumptions": ["Martingale M filtration mu"],
            "lean_declarations": ["AutoSamplingTheory.Example.martingale"],
        }
        card = contract._render_source_card(
            "martingale",
            source,
            {},
            {},
            {},
        )
        self.assertNotIn("For s <= t", card)
        self.assertNotIn("Internal implementation prose", card)
        self.assertIn(r"\mathbb E[M_t\mid\mathcal F_s]=M_s", card)


class ImplicitPrerequisiteContractTests(unittest.TestCase):
    def test_every_current_override_is_plain_prose(self) -> None:
        for item_id, proof in contract.IMPLICIT_PROOF_OVERRIDES.items():
            with self.subTest(item_id=item_id):
                self.assertEqual(contract._raw_math_errors(proof), [])


if __name__ == "__main__":
    unittest.main()
