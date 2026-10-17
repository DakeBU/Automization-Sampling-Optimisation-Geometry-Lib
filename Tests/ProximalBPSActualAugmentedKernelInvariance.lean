import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance

/-! Focused statement/axiom regression and projection of derived normalization.
The type permits rank zero; no separate rank-zero specialization is claimed. -/

#check AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance.actual_augmented_kernel_invariant
#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance.actual_augmented_kernel_invariant

open AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAugmentedKernelInvariance
open MeasureTheory ProbabilityTheory
open scoped NNReal

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1)
    (ρ : ℝ) (hρpos : 0 < ρ) (hρlt : ρ < 1) :
    IsProbabilityMeasure ((volume : Measure E).tilted (fun x => -V x)) :=
  (actual_augmented_kernel_invariant hα hαβ hV hH hη hβη ρ hρpos hρlt).1
