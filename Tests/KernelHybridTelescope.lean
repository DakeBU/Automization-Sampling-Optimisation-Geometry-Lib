import AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope

open MeasureTheory ProbabilityTheory Set
open scoped ProbabilityTheory

example (a δ : ℕ → ℝ)
    (hstep : ∀ i < 3, |a (i + 1) - a i| ≤ δ i) :
    |a 3 - a 0| ≤ δ 0 + δ 1 + δ 2 := by
  simpa [Finset.sum_range_succ] using
    AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_sub_zero_le_sum_range_of_adjacent
      a δ 3 hstep

#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_real_comp_sub_le_integral_eventBound
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_real_comp_commonSuffix_sub_le_integral_eventBound
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.KernelHybridTelescope.abs_sub_zero_le_sum_range_of_adjacent
