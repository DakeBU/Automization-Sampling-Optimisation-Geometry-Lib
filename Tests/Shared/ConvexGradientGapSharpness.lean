import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexGradientGapSharpness
import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentValue

open Set Finset InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis

#print axioms ConvexGradientGapSharpness.quadratic_gap_lower_bound

-- Compose the actual witness with the existing general upper-rate theorem.
-- Both sides refer to the same function and the same gradient iterates.
example {β : ℝ} (hβ : 0 < β) {N : ℕ} (hN : 0 < N) :
    let f : ℝ → ℝ := fun x => (β / (2 * ((N : ℝ) + 1))) * x ^ 2 / 2
    let z := (fun x => x - (1 / β) * gradient f x)^[N] 1
    β / (16 * ((N : ℝ) + 1)) ≤ f z - f 0 ∧ f z - f 0 ≤ β / (2 * N) := by
  obtain ⟨hm, hf, hc, hu, _, _, hl⟩ := ConvexGradientGapSharpness.quadratic_gap_lower_bound hβ N
  refine ⟨hl, ?_⟩
  have he := GradientDescentValue.gradient_descent_weighted_value_bound
    (hf.of_le (by norm_num : (1 : WithTop ℕ∞) ≤ 2)) (hc.mono hm.le)
    (by positivity : (0 : ℝ) ≤ 1 / β)
    (by simp [ne_of_gt hβ] : β * (1 / β) ≤ 1)
    (by norm_num : (0 : ℝ) * (1 / β) ≤ 1) hu 1 0 N
  simp only [zero_mul, sub_zero, one_pow, sum_const, card_range, nsmul_eq_mul,
    mul_one, smul_eq_mul, norm_one] at he
  have hNr : 0 < (N : ℝ) := by exact_mod_cast hN
  apply (le_div_iff₀ (by positivity : (0 : ℝ) < 2 * N)).mpr
  have hh := mul_le_mul_of_nonneg_left he hβ.le
  have hs : β * (2 * (1 / β) * (N : ℝ)) = 2 * N := by field_simp
  rw [← mul_assoc, hs, mul_one] at hh
  convert hh using 1; ring

-- The horizon-zero extension is finite and preserves the genuine initial gap.
example {β : ℝ} (hβ : 0 < β) :
    let f : ℝ → ℝ := fun x => (β / 2) * x ^ 2 / 2
    f ((fun x => x - (1 / β) * gradient f x)^[0] 1) - f 0 = β / 4 := by
  have h := (ConvexGradientGapSharpness.quadratic_gap_lower_bound hβ 0).2.2.2.2.2.1
  norm_num at h ⊢
  nlinarith [h]

-- Concrete positive horizon: mu=1, beta=4, one real gradient step gives gap9/32.
example :
    let f : ℝ → ℝ := fun x => x ^ 2 / 2
    f ((fun x => x - (1 / 4 : ℝ) * gradient f x)^[1] 1) - f 0 = 9 / 32 := by
  have h := (ConvexGradientGapSharpness.quadratic_gap_lower_bound (by norm_num : (0 : ℝ) < 4) 1).2.2.2.2.2.1
  norm_num at h ⊢
  exact h
