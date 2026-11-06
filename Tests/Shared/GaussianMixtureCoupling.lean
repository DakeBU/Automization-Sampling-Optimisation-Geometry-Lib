import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Measure
open scoped ENNReal

-- The actual plan gives the source upper side through the existing infimum
-- bridge. Neither feasibility nor a bound on the cost is given to the test.
example (m : ℝ) :
    WassersteinSpace.wassersteinDistance
        ((1 / 2 : ℝ≥0∞) • gaussianReal (-m) 1 + (1 / 2 : ℝ≥0∞) • gaussianReal m 1)
        ((1 / 4 : ℝ≥0∞) • gaussianReal (-m) 1 + (3 / 4 : ℝ≥0∞) • gaussianReal m 1) ^ 2
      ≤ ENNReal.ofReal (m ^ 2) := by
  obtain ⟨γ, hγ, hcost⟩ := GaussianMixtureCoupling.exists_gaussian_mixture_coupling_cost m
  exact (WassersteinSpace.wassersteinDistance_sq_le_lintegral_of_isCoupling _ _ γ hγ).trans_eq hcost

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling.exists_gaussian_mixture_coupling_cost
