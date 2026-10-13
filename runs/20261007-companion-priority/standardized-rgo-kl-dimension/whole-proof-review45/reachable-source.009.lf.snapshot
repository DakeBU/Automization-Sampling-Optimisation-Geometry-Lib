import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-!
# Convex smooth functions: Bregman gap, cocoercivity and Lipschitz gradient

Source: Chewi, Lectures on Optimization, arXiv:2605.07006v1, Exercise 3.1,
equations (3.4)–(3.5). The argument subtracts the tangent plane, applies the
quadratic upper model at a gradient step, exchanges endpoints, and uses
Cauchy–Schwarz. We express the tilted-function calculation directly through
the existing convex first-order lower bound.

Related external mathematics: Optlib commit
5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3, Function/Lsmooth.lean,
`convex_to_lower` and `lower_to_lipschitz` (Apache-2.0).
No external Lean module is imported. The complete real inner-product space
generalizes the source's Euclidean space. The reciprocal step requires positive
modulus; a positive relaxation and limit retain zero modulus in the scaled
cocoercivity and Lipschitz conclusions. No second derivative is assumed.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient

open Set Filter
open scoped RealInnerProductSpace Topology

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- The positive-modulus Bregman gap controls the squared gradient difference.
Dividing by `2 * β > 0` recovers the source's reciprocal formula (3.4). -/
theorem gradient_gap_sq_le_bregman {f : E → ℝ} {β : ℝ}
    (hf : ContDiff ℝ 1 f) (hc : ConvexOn ℝ univ f) (hβ : 0 < β)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x y : E) :
    ‖gradient f y - gradient f x‖ ^ 2 ≤
      2 * β * (f y - f x - inner ℝ (gradient f x) (y - x)) := by
  let d := gradient f y - gradient f x
  let z := y - β⁻¹ • d
  have hl := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn
    (strongConvexOn_zero.mpr hc)
    (fun w _ => (hf.differentiable_one w).hasGradientAt) (mem_univ x) (mem_univ z)
  simp only [zero_div, zero_mul, add_zero] at hl
  have hh := hu y z
  have hzx : z - x = (y - x) - β⁻¹ • d := by dsimp [z]; abel
  rw [hzx, inner_sub_right, inner_smul_right] at hl
  have hzy : z - y = -(β⁻¹ • d) := by dsimp [z]; abel
  rw [hzy, inner_neg_right, inner_smul_right, norm_neg, norm_smul,
    Real.norm_eq_abs, mul_pow, sq_abs] at hh
  have hd : inner ℝ (gradient f y) d - inner ℝ (gradient f x) d = ‖d‖ ^ 2 := by
    rw [← inner_sub_left]
    exact real_inner_self_eq_norm_sq d
  have h := le_trans hl hh
  have hb : β ≠ 0 := ne_of_gt hβ
  apply (mul_le_mul_iff_right₀ (inv_pos.mpr hβ)).mp
  field_simp [hb] at h ⊢
  nlinarith

/-- Convex gradients are cocoercive in the division-free normalization.
The zero-modulus case follows by relaxing the upper model to `β + ε` and
letting positive `ε` tend to zero, without assigning meaning to a zero denominator. -/
theorem gradient_cocoercive {f : E → ℝ} {β : ℝ}
    (hf : ContDiff ℝ 1 f) (hc : ConvexOn ℝ univ f) (hβ : 0 ≤ β)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x y : E) :
    ‖gradient f y - gradient f x‖ ^ 2 ≤
      β * inner ℝ (gradient f y - gradient f x) (y - x) := by
  have he (ε : ℝ) (hε : 0 < ε) :
      ‖gradient f y - gradient f x‖ ^ 2 ≤
        (β + ε) * inner ℝ (gradient f y - gradient f x) (y - x) := by
    have hu' (a b : E) : f b ≤ f a + inner ℝ (gradient f a) (b - a) +
        (β + ε) / 2 * ‖b - a‖ ^ 2 := by
      have := hu a b
      nlinarith [sq_nonneg ‖b - a‖]
    have hxy := gradient_gap_sq_le_bregman hf hc (add_pos_of_nonneg_of_pos hβ hε) hu' x y
    have hyx := gradient_gap_sq_le_bregman hf hc (add_pos_of_nonneg_of_pos hβ hε) hu' y x
    rw [norm_sub_rev (gradient f x), show x - y = -(y - x) by abel, inner_neg_right] at hyx
    rw [inner_sub_left]
    nlinarith
  have ht : Tendsto (fun ε : ℝ => (β + ε) *
      inner ℝ (gradient f y - gradient f x) (y - x)) (𝓝[>] 0)
      (𝓝 (β * inner ℝ (gradient f y - gradient f x) (y - x))) := by
    simpa using (tendsto_const_nhds.add (tendsto_id.mono_left nhdsWithin_le_nhds :
      Tendsto (fun ε : ℝ => ε) (𝓝[>] 0) (𝓝 0))).mul tendsto_const_nhds
  apply ge_of_tendsto ht
  filter_upwards [self_mem_nhdsWithin] with ε hε
  exact he ε hε

/-- A C¹ convex function with the global quadratic upper model has a
`β`-Lipschitz gradient, including `β = 0`. -/
theorem gradient_lipschitz {f : E → ℝ} {β : NNReal}
    (hf : ContDiff ℝ 1 f) (hc : ConvexOn ℝ univ f)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + (β : ℝ) / 2 * ‖y - x‖ ^ 2) :
    LipschitzWith β (gradient f) := by
  rw [lipschitzWith_iff_norm_sub_le]
  intro x y
  have h := gradient_cocoercive hf hc β.coe_nonneg hu y x
  have hs := mul_le_mul_of_nonneg_left
    (real_inner_le_norm (gradient f x - gradient f y) (x - y)) β.coe_nonneg
  by_cases hz : ‖gradient f x - gradient f y‖ = 0
  · rw [hz]
    positivity
  · apply (mul_le_mul_iff_left₀ (lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz))).mp
    nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient
