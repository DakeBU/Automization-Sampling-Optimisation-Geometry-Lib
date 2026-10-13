"""Prospective expanded statement only; no proof or Statement Seal."""
from pathlib import Path
import datetime, hashlib, json

base = Path(__file__).parent
source = Path("AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean")
raw = source.read_bytes()
assert hashlib.sha256(raw).hexdigest() == "6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029"
old = raw.decode("utf-8")
binders = old[old.index("    {E : Type*}"):old.index("    let c :")]
definitions = old[old.index("    let c :"):old.index("    ∀ y xRef :")]
adoption = json.loads((base / "root.source91.adoption.json").read_bytes())
assert adoption["status"] == "SOURCE_GRAPH_AND_BOUNDED_CANDIDATE_ADMITTED_FOR_PROSPECTIVE_HEADER_ONLY"
header = """import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension
import Mathlib.MeasureTheory.Group.Prod

/-! Prospective statement only: actual next absolute event-time density.
Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1
(A.1),(A.2), one ordered-coordinate ingredient of (A.7), and Appendix A.2.
The actual time observer reads the next literal stopped/live record.
Only strict finite events a(H_n)<U<b(H_n) are represented by this density.
The stopped time0 and negative auxiliary flow are totalizations, not events.
Ordered iteration, final survival, full (A.7) and restart remain OPEN. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime
open InnerProductSpace MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal ENNReal Topology Interval
noncomputable section
set_option autoImplicit false

private def actual_absolute_next_event_time_statement
""" + binders + definitions + """    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ,
      let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
      let Hist := Fin (n + 1) → Rec
      let HistNext := Fin (n + 2) → Rec
      let last : Fin (n + 1) := ⟨n, Nat.lt_succ_self n⟩
      let lastNext : Fin (n + 2) := ⟨n + 1, Nat.lt_succ_self (n + 1)⟩
      let H : (ℕ → ℝ) → Hist := history y xRef z₀ n
      let Hnext : (ℕ → ℝ) → HistNext := history y xRef z₀ (n + 1)
      let readTime : Rec → ℝ := fun r => match r with
        | Sum.inl q => (q.1 : ℝ)
        | Sum.inr _ => 0
      let a : Hist → ℝ := fun h => readTime (h last)
      let U : (ℕ → ℝ) → ℝ := fun w => readTime (Hnext w lastNext)
      let appendRel : Hist × ℝ → HistNext := fun p =>
        Fin.snoc p.1 (match p.1 last with
          | Sum.inl q => Sum.inl (q.1 + Real.toNNReal p.2,
              S xRef (Φ y xRef p.2 q.2))
          | Sum.inr _ => Sum.inr ())
      let appendAbs : Hist × ℝ → HistNext := fun p => appendRel (p.1, p.2 - a p.1)
      let liftAbs : Hist × ℝ → HistNext × ℝ := fun p => (appendAbs p, p.2)
      Measurable H ∧ Measurable Hnext ∧ Measurable a ∧ Measurable U ∧
      Measurable appendAbs ∧ Measurable liftAbs ∧
      (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), appendAbs p j.castSucc = p.1 j) ∧
      (∀ b : Hist → ℝ≥0, Measurable b →
        let d : Hist → ℝ≥0 := fun h => Real.toNNReal ((b h : ℝ) - a h)
        let μ : Measure Hist := Measure.map H P
        let D : Hist → ℝ → ℝ≥0∞ := fun h u =>
          if a h < u ∧ u < (b h : ℝ) then density y xRef (h last, u - a h) else 0
        let Brel : Set (ℕ → ℝ) := {w |
          (0 : WithTop ℝ≥0) < waitObs y xRef (record y xRef z₀ (ε w) n, w n) ∧
          waitObs y xRef (record y xRef z₀ (ε w) n, w n) <
            ((d (H w) : ℝ≥0) : WithTop ℝ≥0)}
        let B : Set (ℕ → ℝ) := {w |
          (∃ q, H w last = Sum.inl q) ∧
          (∃ q, Hnext w lastNext = Sum.inl q) ∧
          a (H w) < U w ∧ U w < (b (H w) : ℝ)}
        let X : (ℕ → ℝ) → Hist × ℝ := fun w => (H w, U w)
        let Y : (ℕ → ℝ) → HistNext × ℝ := fun w => (Hnext w, U w)
        let ν : Measure (Hist × ℝ) := (μ.prod (volume : Measure ℝ)).withDensity
          (fun p => D p.1 p.2)
        Measurable (Function.uncurry D) ∧
        (∀ h : Hist, (∫⁻ u : ℝ, D h u) ≤ 1) ∧
        MeasurableSet B ∧ Measurable X ∧ Measurable Y ∧ Brel = B ∧
        (∀ w ∈ B, U w = a (H w) +
          timeObs y xRef (record y xRef z₀ (ε w) n, w n)) ∧
        (∀ w ∈ B, Hnext w = appendAbs (X w)) ∧
        Measure.map X (P.restrict B) = ν ∧
        Measure.map Y (P.restrict B) = Measure.map liftAbs ν ∧
        Measure.map Hnext (P.restrict B) = Measure.map appendAbs ν ∧
        ν Set.univ ≤ 1 ∧
        (∀ G : Hist × ℝ → ℝ≥0∞, Measurable G →
          Measurable (fun h => ∫⁻ u : ℝ, G (h, u) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, G (X w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, G (h, u) * D h u) ∂μ)) ∧
        (∀ F : HistNext × ℝ → ℝ≥0∞, Measurable F →
          Measurable (fun h => ∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∧
          (∀ A : Set Hist, MeasurableSet A →
            (∫⁻ w in B ∩ H ⁻¹' A, F (Y w) ∂P) =
              ∫⁻ h in A, (∫⁻ u : ℝ, F (liftAbs (h, u)) * D h u) ∂μ)))

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime
"""
target = base / "header91.proposed.lean"
assert not target.exists()
target.write_text(header, encoding="utf-8", newline="\n")
def desc(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p).replace("\\", "/"), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
packet = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "kind": "Prospective whole expanded private Prop; no public proof, Seal or SAU claim",
    "header": desc(target), "accepted_source_graph": desc(base / "source-proof-graph91.accepted-successor.json"),
    "source_adoption": desc(base / "root.source91.adoption.json"),
    "coverage": adoption["unchanged_coverage"], "candidate": adoption["unchanged_candidate"],
    "literal_source_model_copied_from": desc(source),
    "target_Lean_module": "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean",
    "target_public_declaration": "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law",
    "source_analytic_binders": ["hα", "hαβ", "hV", "hH", "hη", "hβη"],
    "intended_actual_consumers": ["S91-J: b(h)=T supplies the next strict ordered-simplex coordinate inside A7"],
    "direct_probability_parent_plan": ["ActualFiniteHistoryExtension.actual_finite_history_extension"],
    "optional_direct_density_parent_has_real_facet": "ActualConditionalNextWaitDensity for jointly Borel density and all-history fiber mass, besides its transitive law use through90.",
    "internal_ingredients_not_public_premises": ["history-dependent additive Lebesgue shear and inverse", "strict density change of variable", "actual record time/guard identification", "Borel model/observers/constructors", "subprobability and all-history fiber bounds"],
    "auxiliary_totalizations": "Stopped readTime=0. appendAbs uses raw flow at u-a(h) and cumulative live time T+max(u-T,0); it becomes u only on strict support. No total raw negative-time value is a physical event.",
    "edge_cases": ["n=0", "b=0", "b<a", "b=a", "globally unbounded finite Borel b", "stopped history", "live infinite wait", "rank0/zero rate", "null old-history A", "unrealizable abstract histories"],
    "excluded": ["endpoint no-atom equivalence", "unrestricted next-event normalization", "random stopping/restart", "ordered finite-depth iteration", "final survival/path/count/hazard assembly", "fullA7", "main theorem/composition/whole paper/Goal completion"],
    "no_Lean_BODY": True, "StatementSeal": False, "SAU_claim": False,
    "required_reviews": ["independent whole-header mathematical/typecheck", "independent whole-header primary-source semantic audit"],
}
out = base / "header-review91.packet.json"
assert not out.exists()
out.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(json.dumps({"header": desc(target), "review_packet": desc(out)}))
