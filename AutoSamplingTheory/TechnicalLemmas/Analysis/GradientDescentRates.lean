import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentValue

/-!
# Normalized gradient-descent function-value rates

Chewi arXiv2605.07006v1 Theorem3.4 (3.2) and its convex specialization.
The descent and weighted recurrence are reused unchanged. Existing compiled
consumer algebra is promoted to public interfaces; the inverse-power equality
is proved only where its base is strictly positive. The rational strong rate
also covers the zero base. Positive step and iteration count are explicit.
C1 Hilbert objectives and arbitrary comparators generalize the source setting.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates
open Set Finset GradientDescentValue
open scoped RealInnerProductSpace
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Convex function-value rate at every positive iteration, for any comparator. -/
theorem convex_value_le {f : E → ℝ} {β h : ℝ} (hf : ContDiff ℝ 1 f)
    (hc : ConvexOn ℝ univ f) (hh : 0 < h) (hstep : β * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x₀ z : E) {N : ℕ} (hN : 0 < N) :
    f ((fun x => x - h • gradient f x)^[N] x₀) - f z ≤ ‖x₀ - z‖ ^ 2 / (2 * h * N) := by
  have he := gradient_descent_weighted_value_bound hf
    (strongConvexOn_zero.mpr hc) hh.le hstep (by norm_num : (0 : ℝ) * h ≤ 1) hu x₀ z N
  simp only [zero_mul, sub_zero, one_pow, sum_const, card_range, nsmul_eq_mul,
    mul_one, one_mul] at he
  apply (le_div_iff₀ (by positivity : 0 < 2 * h * (N : ℝ))).mpr
  nlinarith [he]

/-- Strongly convex rational rate, and exact inverse-power form on its positive-base domain. -/
theorem strongly_convex_value_le {f : E → ℝ} {α β h : ℝ} (hf : ContDiff ℝ 1 f)
    (hsc : StrongConvexOn univ α f) (hα : 0 < α) (hh : 0 < h) (hstep : β * h ≤ 1)
    (hcoeff : α * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x₀ z : E) {N : ℕ} (hN : 0 < N) :
    f ((fun x => x - h • gradient f x)^[N] x₀) - f z ≤
      α * (1 - α * h) ^ N * ‖x₀ - z‖ ^ 2 / (2 * (1 - (1 - α * h) ^ N)) ∧
    (α * h < 1 → f ((fun x => x - h • gradient f x)^[N] x₀) - f z ≤
      α / (2 * ((1 - α * h) ^ (-(N : ℤ)) - 1)) * ‖x₀ - z‖ ^ 2) := by
  have hq : 0 ≤ 1 - α * h := by linarith
  have hqlt : 1 - α * h < 1 := by nlinarith
  have he := gradient_descent_weighted_value_bound hf hsc hh.le hstep (by linarith) hu x₀ z N
  have hs := geom_sum_mul_neg (1 - α * h) N
  have hp : (1 - α * h) ^ N < 1 := pow_lt_one₀ hq hqlt (Nat.ne_of_gt hN)
  have hr : f ((fun x => x - h • gradient f x)^[N] x₀) - f z ≤
      α * (1 - α * h) ^ N * ‖x₀ - z‖ ^ 2 / (2 * (1 - (1 - α * h) ^ N)) := by
    apply (le_div_iff₀ (by positivity : 0 < 2 * (1 - (1 - α * h) ^ N))).mpr
    have hem := mul_le_mul_of_nonneg_left he hα.le
    have hid : α * (2 * h * ∑ k ∈ range N, (1 - α * h) ^ k) =
        2 * (1 - (1 - α * h) ^ N) := by nlinarith [hs]
    rw [← mul_assoc, hid] at hem
    nlinarith [hem]
  refine ⟨hr, ?_⟩
  intro hstrict
  have hqp : 0 < (1 - α * h) ^ N := pow_pos (by linarith) N
  have heq : α * (1 - α * h) ^ N * ‖x₀ - z‖ ^ 2 /
      (2 * (1 - (1 - α * h) ^ N)) =
      α / (2 * ((1 - α * h) ^ (-(N : ℤ)) - 1)) * ‖x₀ - z‖ ^ 2 := by
    rw [zpow_neg, zpow_natCast]
    field_simp
  rwa [heq] at hr

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentRates
