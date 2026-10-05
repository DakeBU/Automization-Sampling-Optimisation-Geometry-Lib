import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# Gradient-descent logarithmic distance complexity

Chewi arXiv2605.07006v1, the paragraph following Theorem3.3's iterated
contraction bound. Reuse that actual-iterate bound at step beta inverse.
Positive moduli and accuracy are explicit. If the initial distance is zero,
no logarithmic threshold is imposed or interpreted; otherwise its argument
is positive. The natural iteration count may be zero, including when the
initial distance is already within tolerance. C1 Hilbert objectives generalize
the source C2 Euclidean setting. A global minimizer is supplied, not constructed.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity
open Set
open scoped RealInnerProductSpace
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The source logarithmic iteration threshold suffices for distance accuracy;
zero initial distance needs no logarithm or positive iteration count. -/
theorem distance_le_of_log_bound {f : E → ℝ} {α β ε : ℝ}
    (hf : ContDiff ℝ 1 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 < α) (hβ : 0 < β) (hε : 0 < ε)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y-x) + β/2*‖y-x‖^2)
    {xstar : E} (hmin : IsMinOn f univ xstar) (x₀ : E) (N : ℕ)
    (hN : 0 < ‖x₀-xstar‖ → 2 * (β / α) * Real.log (‖x₀-xstar‖ / ε) ≤ (N : ℝ)) :
    ‖(fun x => x - β⁻¹ • gradient f x)^[N] x₀ - xstar‖ ≤ ε := by
  have hi := GradientDescentContraction.gradient_descent_distance_bound hf hsc
    hα.le hβ.le (inv_nonneg.mpr hβ.le) (by simp [ne_of_gt hβ]) hu hmin x₀ N
  have he := hi.1.trans hi.2
  by_cases hR : ‖x₀-xstar‖ = 0
  · simpa [hR] using he.trans (by simpa [hR] using hε.le)
  · have hRp : 0 < ‖x₀-xstar‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hR)
    have ht := mul_le_mul_of_nonneg_left (hN hRp) (div_nonneg hα.le hβ.le)
    have hc : (α / β) * (2 * (β / α) * Real.log (‖x₀-xstar‖ / ε)) =
        2 * Real.log (‖x₀-xstar‖ / ε) := by field_simp
    rw [hc] at ht
    have hl : Real.log (‖x₀-xstar‖ / ε) ≤ α * β⁻¹ * N / 2 := by
      rw [div_eq_mul_inv α β] at ht
      nlinarith [ht]
    have hex := (Real.log_le_iff_le_exp (div_pos hRp hε)).mp hl
    have hb : Real.exp (-(α * β⁻¹ * N) / 2) * ‖x₀-xstar‖ ≤ ε := by
      have hm := mul_le_mul_of_nonneg_left hex (le_of_lt (Real.exp_pos (-(α * β⁻¹ * N) / 2)))
      have hid : Real.exp (-(α * β⁻¹ * N) / 2) * Real.exp (α * β⁻¹ * N / 2) = 1 := by
        rw [← Real.exp_add]; ring_nf; exact Real.exp_zero
      rw [hid] at hm
      have hh := (div_le_iff₀ hε).mp (show (Real.exp (-(α * β⁻¹ * N) / 2) * ‖x₀-xstar‖) / ε ≤ 1 by simpa [mul_div_assoc] using hm)
      simpa using hh
    exact he.trans hb

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity
