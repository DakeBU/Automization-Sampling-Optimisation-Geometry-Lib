"""Prepare only the prospective fully expanded statement; no proof BODY."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
source = ROOT / "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean"
old = source.read_text(encoding="utf-8")
definitions = old[old.index("    let c :"):old.index("    ∀ y xRef :")]
binders = old[old.index("    {E : Type*}"):old.index("    let c :")]
header = """import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity
import Mathlib.Data.Fin.Tuple.Basic

/-! Prospective statement only: actual one-step complete finite-history extension.
Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1
(A.1),(A.2), one iteration ingredient of (A.7), and Appendix A.2.
The append's negative-time and stopped branches are auxiliary totalizations.
Only the strict finite event 0<wait<d(H_n) is transported.
Ordered-time iteration, final survival, full (A.7) and restart remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_finite_history_extension_statement
""" + binders + definitions + """    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
      let Hist := Fin (n + 1) → Rec
      let HistNext := Fin (n + 2) → Rec
      let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
      let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
      let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
      let append : Hist × ℝ → HistNext := fun p =>
        Fin.snoc p.1 (match p.1 last with
          | Sum.inl a => Sum.inl (a.1 + Real.toNNReal p.2,
              S xRef (Φ y xRef p.2 a.2))
          | Sum.inr _ => Sum.inr ())
      let lift : Hist × ℝ → HistNext × ℝ := fun p => (append p, p.2)
      Measurable Hnext ∧ Measurable append ∧ Measurable lift ∧
      (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), append p j.castSucc = p.1 j) ∧
      (∀ d : Hist → ℝ≥0, Measurable d →
        let μ : Measure Hist := Measure.map H P
        let D : Hist → ℝ → ℝ≥0∞ := fun h s =>
          if 0 < s ∧ s < (d h : ℝ) then density y xRef (h last, s) else 0
        let B : Set (ℕ → ℝ) := {w |
          (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
          waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
            ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
        let X : (ℕ → ℝ) → Hist × ℝ := fun w =>
          (H w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
        let Y : (ℕ → ℝ) → HistNext × ℝ := fun w =>
          (Hnext w, timeObs y xRef (record y xRef z₀ (ε w) n, w n))
        let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
          (fun p => D p.1 p.2)
        MeasurableSet B ∧ Measurable Y ∧
        (∀ w ∈ B, Hnext w = append (X w)) ∧
        Measure.map Y (P.restrict B) = Measure.map lift ν ∧
        Measure.map Hnext (P.restrict B) = Measure.map append ν ∧
        (Measure.map lift ν) Set.univ ≤ 1 ∧
        (∀ F : HistNext × ℝ → ℝ≥0∞, Measurable F →
          Measurable (fun h => ∫⁻ s : ℝ, F (lift (h, s)) * D h s) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
              ∫⁻ h in A, (∫⁻ s : ℝ, F (lift (h, s)) * D h s) ∂μ)))

end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension
"""
target = HERE / "header90.proposed.lean"
assert not target.exists()
target.write_text(header, encoding="utf-8", newline="\n")
def desc(p):
    b = p.read_bytes()
    return {"path": str(p), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
packet = {
    "kind": "preproof prospective source-facing statement; no Seal or proof",
    "header": desc(target),
    "accepted_source_graph": desc(HERE / "source-proof-graph90.accepted-successor.json"),
    "source_adoption": desc(HERE / "root.source90.adoption.json"),
    "unchanged_coverage": desc(HERE / "independent-source-first90/source-coverage90.native.json"),
    "copied_literal_definitions_from": desc(source),
    "candidate_delta": "Derive a Borel full-history append, actual guarded identity, and restricted joint/marginal n+1-history laws by transport of verified89.",
    "mathematical_consumer": "Remaining S87-I5/G86-11 ordered-event density iteration uses the actual full next history, not just its last state.",
    "six_analytic_source_binders": ["hα", "hαβ", "hV", "hH", "hη", "hβη"],
    "no_provider_premise": True,
    "auxiliary_totalizations": "Negative real times use the literal real harmonic flow and toNNReal cumulative increment; stopped records append stopped. Neither is claimed to describe a positive finite actual jump outside B.",
    "edge_cases": ["n=0", "d=0", "unbounded finite-valued Borel d", "null old-history A", "stopped history", "live infinite wait excluded by B", "rank-zero E", "unrealizable complete histories"],
    "excluded": ["unrestricted next-history law", "positive probability normalization", "finite wait guarantee", "ordered absolute-time iteration", "final survival", "full A7", "restart/Markov", "main theorem", "whole-paper or Goal completion"],
    "SAU_claimed": False, "statement_sealed": False, "Lean_BODY_started": False,
    "independent_preproof_header_reviews_required": True
}
(HERE / "header-review90.packet.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(json.dumps({"header": desc(target), "review_packet": desc(HERE / "header-review90.packet.json")}))
