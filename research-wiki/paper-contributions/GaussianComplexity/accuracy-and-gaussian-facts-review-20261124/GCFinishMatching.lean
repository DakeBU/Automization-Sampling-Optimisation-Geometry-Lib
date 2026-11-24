import GCFinishBoundary

/-! The matching regimes following Theorem 1.1, as explicit inequalities
between its lower rate and the polynomial-sampling upper rate. -/
open Real
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison

noncomputable def upperRate (d κ ε : ℝ) := min d (sqrt κ * log (d/ε))

/-- For condition numbers at least the square of the dimension, the lower rate is linear. -/
theorem saturated_rate {d κ ε : ℝ} (hd : 0 < d) (hk : d ≤ sqrt κ) (he : 0 < ε) (he' : ε ≤ 1) :
    d/2 ≤ lowerRate d κ ε := by
  let s := sqrt κ
  have hs : 0 < s := hd.trans_le hk
  have hx : 0 < d/s := div_pos hd hs
  have hx' : d/s ≤ 1 := (div_le_one hs).2 hk
  have hlog := Real.one_sub_inv_le_log_of_pos (show 0 < 1+d/s by positivity)
  have hhalf : (d/s)/2 ≤ 1-(1+d/s)⁻¹ := by
    rw [le_sub_iff_add_le, add_comm]
    rw [← le_sub_iff_add_le, inv_eq_one_div]
    apply (div_le_iff₀ (by positivity)).2
    nlinarith [mul_nonneg hx.le (sub_nonneg.mpr hx')]
  have hcomp : 1+d/s ≤ 1+d/(s*ε) := by
    gcongr
    exact mul_le_of_le_one_right hs.le he'
  change d/2 ≤ min d (s * _)
  refine le_min (by linarith) ?_
  calc
    d/2 = s*((d/s)/2) := by field_simp
    _ ≤ s*log (1+d/s) := mul_le_mul_of_nonneg_left (hhalf.trans hlog) hs.le
    _ ≤ _ := mul_le_mul_of_nonneg_left (log_le_log (by positivity) hcomp) hs.le

private theorem compare_logs {d κ ε c : ℝ} (hd : 0 ≤ d) (hc : 0 ≤ c) (hc' : c ≤ 1)
    (h : c*log (d/ε) ≤ log (1+d/(sqrt κ*ε))) :
    c*upperRate d κ ε ≤ lowerRate d κ ε := by
  rw [upperRate,lowerRate]
  refine le_min ?_ ?_
  · exact (mul_le_mul_of_nonneg_left (min_le_left _ _) hc).trans (mul_le_of_le_one_left hd hc')
  · calc
      _ ≤ c*(sqrt κ * log (d/ε)) := mul_le_mul_of_nonneg_left (min_le_right _ _) hc
      _ = sqrt κ*(c*log (d/ε)) := by ring
      _ ≤ _ := mul_le_mul_of_nonneg_left h (sqrt_nonneg _)

/-- Under κ ≤ d^(2-δ), the upper and lower rates match with factor δ/2. -/
theorem polynomial_condition_matching {d κ ε δ : ℝ} (hd : 1 ≤ d) (hk : 0 < κ)
    (he : 0 < ε) (he' : ε ≤ 1) (hδ : 0 < δ) (hδ' : δ < 2) (hcap : κ ≤ d^(2-δ)) :
    (δ/2)*upperRate d κ ε ≤ lowerRate d κ ε := by
  have hd0 : 0 < d := by linarith
  have hs := sqrt_pos.mpr hk
  have hlogk := log_le_log hk hcap
  rw [log_rpow hd0] at hlogk
  have hlogs := log_sqrt hk.le
  have hloge := log_nonpos he.le he'
  apply compare_logs hd0.le (by linarith) (by linarith)
  have hpos : 0 < d/(sqrt κ*ε) := by positivity
  apply le_trans _ (log_le_log hpos (show d/(sqrt κ*ε) ≤ 1+d/(sqrt κ*ε) by linarith))
  rw [log_div hd0.ne' (mul_ne_zero hs.ne' he.ne'), log_mul hs.ne' he.ne', log_div hd0.ne' he.ne']
  nlinarith [mul_nonneg (sub_nonneg.mpr hδ'.le) (neg_nonneg.mpr hloge)]

/-- Polynomial accuracy ε ≤ d^(-c) at every condition number. -/
theorem polynomial_accuracy_matching {d κ ε c : ℝ} (hd : 1 ≤ d) (hk : 0 < κ)
    (he : 0 < ε) (hc : 0 < c) (hcap : ε ≤ d^(-c)) :
    min (1/2) (c/(1+c))*upperRate d κ ε ≤ lowerRate d κ ε := by
  have hd0 : 0 < d := by linarith
  have hs := sqrt_pos.mpr hk
  have hloge := log_le_log he hcap
  rw [log_rpow hd0] at hloge
  have hld := log_nonneg hd
  have he' : ε ≤ 1 := (Real.log_le_iff_le_exp he).mp (by nlinarith [mul_nonneg hc.le hld]) |>.trans_eq Real.exp_zero
  have hc0 : 0 ≤ min (1/2 : ℝ) (c/(1+c)) := le_min (by norm_num) (by positivity)
  have hc1 := min_le_left (1/2 : ℝ) (c/(1+c))
  by_cases hsat : d ≤ sqrt κ
  · apply le_trans _ (saturated_rate hd0 hsat he he')
    calc
      _ ≤ min (1/2 : ℝ) (c/(1+c))*d := mul_le_mul_of_nonneg_left (min_le_left _ _) hc0
      _ ≤ d/2 := by nlinarith [mul_le_mul_of_nonneg_right hc1 hd0.le]
  · apply compare_logs hd0.le hc0 (by linarith)
    have hfrac : 1/ε ≤ d/(sqrt κ*ε) := by
      apply (div_le_div_iff₀ he (by positivity)).2
      nlinarith [mul_le_mul_of_nonneg_right (le_of_not_ge hsat) he.le]
    have hlog : log (1/ε) ≤ log (1+d/(sqrt κ*ε)) :=
      log_le_log (by positivity) (by linarith)
    apply le_trans _ hlog
    rw [show 1/ε = ε⁻¹ from one_div _,log_inv,log_div hd0.ne' he.ne']
    have hle : 0 ≤ log d-log ε := by nlinarith [log_nonpos he.le he']
    apply le_trans (mul_le_mul_of_nonneg_right (min_le_right _ _) hle)
    rw [div_mul_eq_mul_div, div_le_iff₀ (by positivity)]
    nlinarith

#print axioms saturated_rate
#print axioms polynomial_condition_matching
#print axioms polynomial_accuracy_matching
end AutoSamplingTheory.ExampleCases.GaussianComplexity.RateComparison
