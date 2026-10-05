import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep
import Mathlib.Analysis.Calculus.Deriv.Pow

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep
open Set
open scoped RealInnerProductSpace

-- Genuine unit quadratic: arbitrary nonnegative steps, equal moduli (factor zero),
-- and unequal bounds alpha=1,beta=3 (factor 1/2). The latter envelope is attained.
example (x y h : ℝ) (hh : 0 ≤ h) :
    ‖(y - h * y) - (x - h * x)‖ ≤ |1-h| * ‖y-x‖ ∧
    ‖(y-y)-(x-x)‖ ≤ 0 ∧
    ‖(y-(1/2 : ℝ)*y)-(x-(1/2 : ℝ)*x)‖ ≤ (1/2 : ℝ)*‖y-x‖ ∧
    ∀ t : ℝ, (1/2 : ℝ) ≤ max |1-t| |1-3*t| := by
  let f : ℝ → ℝ := fun t => t^2 / 2
  have hf : ContDiff ℝ 2 f := (contDiff_id.pow 2).div_const 2
  have hg (t : ℝ) : gradient f t = t := by
    have hd : HasDerivAt f t t := by
      simpa [f] using ((hasDerivAt_id t).pow 2).div_const (2 : ℝ)
    exact hd.hasGradientAt.gradient
  have hc : StrongConvexOn univ 1 f := by
    rw [strongConvexOn_iff_convex]
    have he : (fun t : ℝ => f t - (1 : ℝ)/2 * ‖t‖^2) = fun _ => 0 := by
      funext t; simp [f, Real.norm_eq_abs, sq_abs]; ring
    rw [he]
    exact convexOn_const _ convex_univ
  have hu : ∀ a b, f b ≤ f a + inner ℝ (gradient f a) (b-a) + 1/2*‖b-a‖^2 := by
    intro a b; rw [hg]; simp only [f, Real.inner_apply, Real.norm_eq_abs, sq_abs]; nlinarith
  have he := gradient_step_endpoint_bound hf hc hh hu x y
  have hz := (optimal_gradient_step hf hc (by norm_num) (by norm_num : (0:ℝ)<1)
    (by norm_num) hu x y).1
  have hu3 : ∀ a b, f b ≤ f a + inner ℝ (gradient f a) (b-a) + 3/2*‖b-a‖^2 := by
    intro a b; have hh' := hu a b; nlinarith [sq_nonneg ‖b-a‖]
  have ht := optimal_gradient_step hf hc (by norm_num) (by norm_num : (0:ℝ)<3)
    (by norm_num) hu3 x y
  constructor
  · simpa [hg] using he
  constructor
  · simpa [hg] using hz
  constructor
  · norm_num [hg] at ht ⊢; exact ht.1
  · intro t; have ht' := ht.2 t; norm_num at ht'; simpa [mul_comm] using ht'

-- alpha=0 gives nonexpansiveness, not strict contraction; a constant objective
-- makes the norm bound equality and tests the beta>0 but non-sharp smoothness bound.
example (x y : ℝ) : ‖y-x‖ ≤ ‖y-x‖ ∧
    ∀ h : ℝ, (1 : ℝ) ≤ max |1-h*0| |1-h| := by
  have h := optimal_gradient_step (f := fun _ : ℝ => (7 : ℝ)) (α := 0) (β := 1)
    contDiff_const (strongConvexOn_zero.mpr (convexOn_const _ convex_univ))
    (by norm_num) (by norm_num) (by norm_num)
    (by intro a b; simp; positivity) x y
  simpa using h

#print axioms gradient_step_endpoint_bound
#print axioms optimal_gradient_step
