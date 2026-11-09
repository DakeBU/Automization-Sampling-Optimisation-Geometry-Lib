import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev

open MeasureTheory ProbabilityTheory
open scoped ContDiff RealInnerProductSpace

namespace Tests.Shared.CompactLogSobolevPoincare

open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities

-- Real probability measure and real function-form LSI; checks the factor two
-- against the established Gaussian result and obtains genuine admissibility.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) (hs : HasCompactSupport f) :
    Poincare.Admissible (stdGaussian E) f ∧
      Poincare.variance (stdGaussian E) f ≤ Poincare.dirichletEnergy (stdGaussian E) f := by
  have hLSI (v : E → ℝ) (hv : ContDiff ℝ ∞ v) (hsv : HasCompactSupport v) :
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂(stdGaussian E)) -
        (∫ x, (v x)^2 ∂(stdGaussian E)) * Real.log (∫ x, (v x)^2 ∂(stdGaussian E)) ≤
      2 * 1 * ∫ x, ‖gradient v x‖^2 ∂(stdGaussian E) := by
    have h := GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev v
      (hv.of_le (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))) hsv
    simpa only [mul_one] using h.2.2.2
  simpa only [one_mul] using CompactLogSobolevPoincare.variance_le_of_compact_logSobolev
    (stdGaussian E) 1 hLSI f hf hs

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare.variance_le_of_compact_logSobolev

end Tests.Shared.CompactLogSobolevPoincare
