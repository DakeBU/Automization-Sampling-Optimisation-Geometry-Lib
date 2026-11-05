import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev

open MeasureTheory ProbabilityTheory
open scoped ContDiff RealInnerProductSpace

namespace Tests.Shared.CompactLogSobolevPoincare

open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities

-- A consumer with a genuine input LSI, not an assumed final PI.
-- No zero-mean hypothesis is imposed on the observable.
example (g : ℝ → ℝ) (hg : ContDiff ℝ ∞ g) (hs : HasCompactSupport g) :
    (∫ x, (g x - ∫ y, g y ∂stdGaussian ℝ)^2 ∂stdGaussian ℝ) ≤
      ∫ x, ‖gradient g x‖^2 ∂stdGaussian ℝ := by
  have h := CompactLogSobolevPoincare.poincare_of_compact_logSobolev
    (stdGaussian ℝ) 1 (by norm_num) (fun v hv hc => by
      simpa using (GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev
        v (hv.of_le (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))) hc).2.2.2) g hg hs
  simpa only [one_mul] using h

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactLogSobolevPoincare.poincare_of_compact_logSobolev

end Tests.Shared.CompactLogSobolevPoincare
