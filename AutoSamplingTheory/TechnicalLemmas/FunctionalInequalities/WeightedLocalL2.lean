import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar

/-!
# Local square integrability of Gibbs L2 representatives

An elementary analytic prerequisite for arXiv:2609.06905v1 Appendix C.1:
continuous positive Gibbs weights allow local unweighted L2 control. This is
not elliptic regularity, a domain characterization, or a Poincare inequality.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedLocalL2

open MeasureTheory

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- A Gibbs L2 representative has locally integrable squared norm for volume,
and is L2 on each compact volume restriction. Only continuity of the potential
is required; the target needs no scalar structure or completeness. -/
theorem lp_locallyMemLp_volume {F : Type*} [NormedAddCommGroup F]
    (W : E → ℝ) (hW : Continuous W)
    (hI : Integrable (fun x => Real.exp (-W x)))
    (a : Lp F 2 ((volume : Measure E).tilted (fun x => -W x))) :
    LocallyIntegrable (fun x => ‖a x‖ ^ 2) (volume : Measure E) ∧
      ∀ K : Set E, IsCompact K → MemLp (fun x => a x) 2 (volume.restrict K) := by
  have hs := (memLp_two_iff_integrable_sq_norm (Lp.memLp a).aestronglyMeasurable).mp
    (Lp.memLp a)
  have hw : Integrable (fun x => Real.exp (-W x) * ‖a x‖ ^ 2) := by
    simpa only [smul_eq_mul] using (integrable_tilted_iff hI _).mp hs
  have hl : LocallyIntegrable (fun x => ‖a x‖ ^ 2) (volume : Measure E) := by
    have h := hw.locallyIntegrable.continuous_mul (Real.continuous_exp.comp hW)
    simpa only [Function.comp_apply, ← mul_assoc, ← Real.exp_add, add_neg_cancel,
      Real.exp_zero, one_mul]
      using h
  refine ⟨hl, ?_⟩
  intro K hK
  have hm : AEStronglyMeasurable (fun x => a x) (volume : Measure E) :=
    (Lp.memLp a).aestronglyMeasurable.mono_ac (absolutelyContinuous_tilted hI)
  exact (memLp_two_iff_integrable_sq_norm hm.restrict).mpr
    (hl.integrableOn_isCompact hK)

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedLocalL2
