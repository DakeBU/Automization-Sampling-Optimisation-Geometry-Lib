import GCFinishMatching
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder

/-! The rate comparison following Theorem 1.2. The two precision/reply identities
used in Remark 4.2 have already been verified for the source cosine grid. -/
open Real
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison

theorem hidden_spectrum_upper_rate {d κ ε C : ℝ} (hd : 1 ≤ d) (h : d^(-C) ≤ ε) :
    upperRate d κ ε ≤ (1+C)*(sqrt κ*log d) := by
  have hd' : 0 < d := by linarith
  have he : 0 < ε := (rpow_pos_of_pos hd' _).trans_le h
  have hl := log_le_log (rpow_pos_of_pos hd' _) h
  rw [log_rpow hd'] at hl
  apply (min_le_right _ _).trans
  rw [log_div hd'.ne' he.ne']
  calc
    _ ≤ sqrt κ * ((1+C)*log d) := mul_le_mul_of_nonneg_left (by nlinarith) (sqrt_nonneg _)
    _ = _ := by ring

#print axioms hidden_spectrum_upper_rate
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query
end AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison
