import GCFinishMatching
import GC31LowerBound

/-! Numerical comparison of the lower rates of Theorems 3.1 and 4.1 on their
common parameter range. -/
open Real
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison

/-- The comparison holds already for every real dimension d ≥ 1. -/
theorem hidden_eigenbasis_rate_le_lowerRate {d κ ε δ : ℝ}
    (hd : 1 ≤ d) (hk : 0 < κ) (he : 0 < ε) (he' : ε ≤ 1)
    (hδ : δ < 1) (hcap : κ ≤ d ^ (1-δ)) :
    δ * sqrt κ * log d ≤ lowerRate d κ ε := by
  have hd0 : 0 < d := by linarith
  have hs := sqrt_pos.mpr hk
  have hld := log_nonneg hd
  have hκlog := log_le_log hk hcap
  rw [log_rpow hd0] at hκlog
  have hlog : δ * log d ≤ log (d/sqrt κ) := by
    rw [log_div hd0.ne' hs.ne', log_sqrt hk.le]
    nlinarith [mul_nonneg (sub_nonneg.mpr hδ.le) hld]
  have hfrac : 0 < d/sqrt κ := div_pos hd0 hs
  rw [lowerRate,show δ * sqrt κ * log d = sqrt κ * (δ * log d) by ring]
  apply le_min
  · have h := hlog.trans ((log_le_sub_one_of_pos hfrac).trans (by linarith : d/sqrt κ - 1 ≤ d/sqrt κ))
    calc
      _ ≤ sqrt κ * (d/sqrt κ) := mul_le_mul_of_nonneg_left h hs.le
      _ = d := by field_simp
  · apply mul_le_mul_of_nonneg_left _ hs.le
    apply hlog.trans (log_le_log hfrac _)
    have h := div_le_div_of_nonneg_left hd0.le (mul_pos hs he) (mul_le_of_le_one_right hs.le he')
    linarith

universe u v

/-- Equation (3) alone gives the numerical hidden-eigenbasis rate for the
ordinary minimax query complexity wherever the two parameter ranges overlap. -/
theorem gaussian_complexity_overlap {d : ℕ} {κ ε δ : ℝ}
    (hd : 1 ≤ d) (hk : 4 ≤ κ) (he : 0 < ε) (he' : ε ≤ 1/16)
    (hδ : δ < 1) (hcap : κ ≤ (d : ℝ) ^ (1-δ)) :
    ENNReal.ofReal ((δ/256) * sqrt κ * log d) ≤
      FirstOrderIndistinguishability.gaussianQueryComplexity.{u,v} d κ ε := by
  apply le_trans _ (FirstOrderIndistinguishability.gaussian_query_complexity_lower_bound hd hk he he')
  apply ENNReal.ofReal_le_ofReal
  have h := hidden_eigenbasis_rate_le_lowerRate (by exact_mod_cast hd) (by linarith : 0 < κ) he
    (by linarith) hδ hcap
  change _ ≤ (1/256 : ℝ) * lowerRate d κ ε
  linarith

#print axioms hidden_eigenbasis_rate_le_lowerRate
#print axioms gaussian_complexity_overlap
end AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison
