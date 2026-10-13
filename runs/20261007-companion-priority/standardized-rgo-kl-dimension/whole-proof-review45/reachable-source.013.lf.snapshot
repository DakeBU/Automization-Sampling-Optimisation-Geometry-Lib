import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSmoothGradient
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Dynamics.FixedPoints.Basic

/-!
# Gradient descent: contraction and distance rates

Source: Chewi, Lectures on Optimization, arXiv:2605.07006v1, Theorem 3.3.
Compose the squared-distance expansion with Exercise 3.1 cocoercivity and
Proposition 1.6 strong gradient monotonicity. Iteration uses an actual global
minimizer, whose gradient vanishes by Fermat's theorem.

We expose the necessary nonnegative-step condition implicit in the source.
The division-free restriction `β * h ≤ 1` includes zero modulus, and C¹ on a
complete real inner-product space generalizes the section's C² Euclidean
setting. No `α ≤ β` assumption is needed, including on a singleton space:
real square root is total and the squared estimate forces zero distance if its
coefficient is negative. The source's positive-modulus instance has the usual
nonnegative coefficient. Its stray gradient before `y - x` in the middle
proof display is read as the displacement, as in the preceding expansion.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction

open Set
open scoped RealInnerProductSpace Topology

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- One gradient step contracts by `sqrt (1 - α * h)` under the global curvature
and quadratic upper models, with explicit nonnegative step. -/
theorem gradient_step_contraction {f : E → ℝ} {α β h : ℝ}
    (hf : ContDiff ℝ 1 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 ≤ α) (hβ : 0 ≤ β) (hh : 0 ≤ h) (hstep : β * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x y : E) :
    ‖(y - h • gradient f y) - (x - h • gradient f x)‖ ≤
      Real.sqrt (1 - α * h) * ‖y - x‖ := by
  have hc : ConvexOn ℝ univ f := hsc.convexOn (by intro r; positivity)
  have hm := StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
    hsc (fun z _ => (hf.differentiable_one z).hasGradientAt) (mem_univ x) (mem_univ y)
  have hg := ConvexSmoothGradient.gradient_cocoercive hf hc hβ hu x y
  have hp : 0 ≤ inner ℝ (gradient f y - gradient f x) (y - x) :=
    le_trans (mul_nonneg hα (sq_nonneg _)) hm
  have hg' := mul_le_mul_of_nonneg_left hg (sq_nonneg h)
  have hs := mul_le_mul_of_nonneg_left hstep (mul_nonneg hh hp)
  have hm' := mul_le_mul_of_nonneg_left hm hh
  have hv : (y - h • gradient f y) - (x - h • gradient f x) =
      (y - x) - h • (gradient f y - gradient f x) := by rw [smul_sub]; abel
  have hb : ‖(y - h • gradient f y) - (x - h • gradient f x)‖ ^ 2 ≤
      (1 - α * h) * ‖y - x‖ ^ 2 := by
    rw [hv, norm_sub_sq_real, inner_smul_right,
      real_inner_comm (gradient f y - gradient f x), norm_smul,
      Real.norm_eq_abs, mul_pow, sq_abs]
    nlinarith
  simpa only [Real.sqrt_mul' _ (sq_nonneg _), Real.sqrt_sq (norm_nonneg _)] using
    Real.le_sqrt_of_sq_le hb

/-- The actual Nth gradient-descent iterate has geometric, then exponential,
distance control about a supplied global minimizer. -/
theorem gradient_descent_distance_bound {f : E → ℝ} {α β h : ℝ}
    (hf : ContDiff ℝ 1 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 ≤ α) (hβ : 0 ≤ β) (hh : 0 ≤ h) (hstep : β * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    {xstar : E} (hmin : IsMinOn f univ xstar) (x₀ : E) (N : ℕ) :
    ‖(fun x => x - h • gradient f x)^[N] x₀ - xstar‖ ≤
        Real.sqrt (1 - α * h) ^ N * ‖x₀ - xstar‖ ∧
      Real.sqrt (1 - α * h) ^ N * ‖x₀ - xstar‖ ≤
        Real.exp (-(α * h * N) / 2) * ‖x₀ - xstar‖ := by
  let T : E → E := fun x => x - h • gradient f x
  have hg : gradient f xstar = 0 := by
    simp [gradient, (hmin.isLocalMin Filter.univ_mem).fderiv_eq_zero]
  have hfix : Function.IsFixedPt T xstar := by simp [Function.IsFixedPt, T, hg]
  have hl : LipschitzWith (Real.toNNReal (Real.sqrt (1 - α * h))) T := by
    rw [lipschitzWith_iff_norm_sub_le]
    intro x y
    simpa only [Real.coe_toNNReal _ (Real.sqrt_nonneg _)] using
      gradient_step_contraction hf hsc hα hβ hh hstep hu y x
  constructor
  · have hi := (hl.iterate N).dist_le_mul x₀ xstar
    simpa only [dist_eq_norm, (hfix.iterate N).eq, NNReal.coe_pow, Real.coe_toNNReal _ (Real.sqrt_nonneg _), T] using hi
  · have he : Real.sqrt (1 - α * h) ≤ Real.exp (-(α * h) / 2) := by
      apply (Real.sqrt_le_left (Real.exp_nonneg _)).mpr
      have hx := Real.add_one_le_exp (-(α * h))
      rw [pow_two, ← Real.exp_add, show -(α * h) / 2 + -(α * h) / 2 = -(α * h) by ring]
      simpa only [sub_eq_add_neg, add_comm] using hx
    have hp := pow_le_pow_left₀ (Real.sqrt_nonneg _) he N
    have hr := mul_le_mul_of_nonneg_right hp (norm_nonneg (x₀ - xstar))
    rw [← Real.exp_nat_mul, show (N : ℝ) * (-(α * h) / 2) =
      -(α * h * N) / 2 by ring] at hr
    exact hr

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentContraction
