import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-! The scalar comparison in Proposition B.7, arXiv:2610.20492v1 Eq. (19).
The actual TV first bound and sphere/Poisson evaluation remain separate.
The logarithmic estimate below uses two canonical tangent bounds, an alternative
to the source's integral estimate; it preserves the source's final constant. -/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation
set_option autoImplicit false

theorem explicit_ratio_ge_exponential {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    (1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / Real.sqrt κ) ≤
      (((Real.sqrt κ - 1) / (Real.sqrt κ + 1)) ^ n) /
        (2 + 4 * (n : ℝ) * Real.sqrt κ / (Real.sqrt κ + 1) ^ 2) := by
  let s := Real.sqrt κ
  have hs : (2 : ℝ) ≤ s := Real.le_sqrt_of_sq_le (by nlinarith)
  have hs0 : 0 < s := by linarith
  have hm : 0 < s - 1 := by linarith
  have hp : 0 < s + 1 := by linarith
  have ha : 0 < (s + 1) / s := div_pos hp hs0
  have hb : 0 < s / (s - 1) := div_pos hs0 hm
  have hla : Real.log ((s + 1) / s) ≤ 1 / s := by
    convert Real.log_le_sub_one_of_pos ha using 1; field_simp; ring
  have hlb : Real.log (s / (s - 1)) ≤ 1 / (s - 1) := by
    convert Real.log_le_sub_one_of_pos hb using 1; field_simp; ring
  have hprod : ((s + 1) / s) * (s / (s - 1)) = (s + 1) / (s - 1) := by
    field_simp
  have hfra : 1 / (s - 1) ≤ 2 / s := by
    apply (div_le_div_iff₀ hm hs0).2
    linarith
  have hlog : Real.log ((s + 1) / (s - 1)) ≤ 3 / s := by
    rw [← hprod, Real.log_mul (ne_of_gt ha) (ne_of_gt hb)]
    have hsum : 1 / s + 1 / (s - 1) ≤ 3 / s := by
      convert add_le_add_left hfra (1 / s) using 1 <;> ring
    exact (add_le_add hla hlb).trans hsum
  have hr : 0 < (s - 1) / (s + 1) := div_pos hm hp
  have hlower : -(3 : ℝ) / s ≤ Real.log ((s - 1) / (s + 1)) := by
    rw [Real.log_div (ne_of_gt hm) (ne_of_gt hp)]
    rw [Real.log_div (ne_of_gt hp) (ne_of_gt hm)] at hlog
    simpa only [neg_div, neg_sub] using neg_le_neg hlog
  have hexp : Real.exp (-(3 : ℝ) / s) ≤ (s - 1) / (s + 1) :=
    (Real.le_log_iff_exp_le hr).1 hlower
  have hpower : Real.exp (-(3 * (n : ℝ)) / s) ≤ ((s - 1) / (s + 1)) ^ n := by
    have heq : -(3 * (n : ℝ)) / s = (n : ℝ) * (-(3 : ℝ) / s) := by ring
    rw [heq, Real.exp_nat_mul]
    exact pow_le_pow_left₀ (Real.exp_nonneg _) hexp n
  have hkernel : s / (s + 1) ^ 2 ≤ 1 / s := by
    apply (div_le_div_iff₀ (sq_pos_of_pos hp) hs0).2
    nlinarith
  have hden : 2 + 4 * (n : ℝ) * s / (s + 1) ^ 2 ≤
      2 * Real.exp (2 * (n : ℝ) / s) := by
    have hscale := mul_le_mul_of_nonneg_left hkernel
      (show 0 ≤ 4 * (n : ℝ) by positivity)
    have he := Real.add_one_le_exp (2 * (n : ℝ) / s)
    have hscale' : 4 * (n : ℝ) * s / (s + 1) ^ 2 ≤ 4 * (n : ℝ) / s := by
      simpa only [← mul_div_assoc, mul_one] using hscale
    simp only [div_eq_mul_inv] at hscale' he ⊢
    linarith only [hscale', he]
  have hdenpos : 0 < 2 + 4 * (n : ℝ) * s / (s + 1) ^ 2 := by positivity
  have hquot := div_le_div₀ (pow_nonneg (le_of_lt hr) n)
    hpower hdenpos hden
  have heq : Real.exp (-(3 * (n : ℝ)) / s) /
      (2 * Real.exp (2 * (n : ℝ) / s)) =
      (1 / 2 : ℝ) * Real.exp (-(5 * (n : ℝ)) / s) := by
    rw [mul_comm (2 : ℝ), div_mul_eq_div_div, ← Real.exp_sub]
    have harg : -(3 * (n : ℝ)) / s - 2 * (n : ℝ) / s =
        -(5 * (n : ℝ)) / s := by ring
    rw [harg]
    ring
  rw [heq] at hquot
  exact hquot

end AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation
