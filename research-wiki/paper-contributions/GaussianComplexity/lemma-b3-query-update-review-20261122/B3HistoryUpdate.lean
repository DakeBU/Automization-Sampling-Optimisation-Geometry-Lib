import Mathlib.Probability.Kernel.Composition.MeasureCompProd

/-!
# Extending the conditional law through one step of a query history

The disintegration step in the proof of Zhou–Suzuki, Lemma B.3
(arXiv:2610.20492v1). Old and new residual laws may both depend on the
old history. A concrete oracle must supply the jointly measurable update
and its one-step conditional product law.
-/

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {H X Y R : Type*}
  [MeasurableSpace H] [MeasurableSpace X] [MeasurableSpace Y] [MeasurableSpace R]

/-- A fiberwise response/residual product, after adjoining the actual response
to the old history, gives the posterior kernel at the new history. -/
theorem extend_history_posterior (ρ : Measure H) [SFinite ρ]
    (old : Kernel H X) (answer : Kernel H Y) (remaining : Kernel H R)
    [IsSFiniteKernel old] [IsSFiniteKernel answer] [IsSFiniteKernel remaining]
    (step : H → X → Y × R) (hm : Measurable (Function.uncurry step))
    (hlaw : ∀ᵐ h ∂ρ, (old h).map (step h) = (answer h).prod (remaining h)) :
    (ρ ⊗ₘ old).map (fun p : H × X =>
      ((p.1, (step p.1 p.2).1), (step p.1 p.2).2)) =
      (ρ ⊗ₘ answer) ⊗ₘ Kernel.prodMkRight Y remaining := by
  let posterior := Kernel.prodMkRight Y remaining
  have hfamily (h : H) : (answer ⊗ₖ posterior) h = (answer h).prod (remaining h) := by
    ext s hs
    rw [Kernel.compProd_apply hs, Measure.prod_apply hs]
    rfl
  let keep := fun p : H × X => (p.1, step p.1 p.2)
  have hk : Measurable keep := measurable_fst.prodMk hm
  have hj : (ρ ⊗ₘ old).map keep = ρ ⊗ₘ (answer ⊗ₖ posterior) := by
    ext s hs
    rw [Measure.map_apply hk hs, Measure.compProd_apply (hk hs), Measure.compProd_apply hs]
    apply lintegral_congr_ae
    filter_upwards [hlaw] with h hh
    rw [hfamily, ← hh, Measure.map_apply hm.of_uncurry_left (measurable_prodMk_left hs)]
    rfl
  calc
    _ = ((ρ ⊗ₘ old).map keep).map MeasurableEquiv.prodAssoc.symm :=
      (Measure.map_map MeasurableEquiv.prodAssoc.symm.measurable hk).symm
    _ = _ := by rw [hj, Measure.compProd_assoc]

#print axioms extend_history_posterior

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
