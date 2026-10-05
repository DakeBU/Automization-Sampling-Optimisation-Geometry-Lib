import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.ContDiff.Operations
import Mathlib.Algebra.Order.Floor.Semiring

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity
open Set
open scoped RealInnerProductSpace

-- Actual nontrivial quadratic iteration with alpha1,beta2 and step1/2.
-- Nat ceiling gives an integer budget; zero initial distance needs no logarithm;
-- an already accurate initial point allows N0.
example (x ε : ℝ) (hε : 0 < ε) :
    ‖(fun t : ℝ => t - (1/2 : ℝ)*t)^[⌈4 * Real.log (‖x‖ / ε)⌉₊] x‖ ≤ ε ∧
    (∀ N : ℕ, ‖(fun t : ℝ => t - (1/2 : ℝ)*t)^[N] 0‖ ≤ ε) ∧
    (‖x‖ ≤ ε → ‖(fun t : ℝ => t - (1/2 : ℝ)*t)^[0] x‖ ≤ ε) := by
  let f : ℝ → ℝ := fun t => t^2/2
  have hf : ContDiff ℝ 1 f := (contDiff_id.pow 2).div_const 2
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
  have hu : ∀ a b, f b ≤ f a + inner ℝ (gradient f a) (b-a) + 2/2*‖b-a‖^2 := by
    intro a b; rw [hg]; simp only [f, Real.inner_apply, Real.norm_eq_abs, sq_abs]; nlinarith [sq_nonneg (b-a)]
  have hm : IsMinOn f univ 0 := by intro t _; simp [f]; positivity
  have bound := distance_le_of_log_bound hf hc (by norm_num : (0:ℝ)<1)
    (by norm_num : (0:ℝ)<2) hε hu hm
  constructor
  · have hr := bound x ⌈4 * Real.log (‖x‖ / ε)⌉₊ (by
      intro _; simpa only [sub_zero, div_one, show (2:ℝ)*2=4 by norm_num] using Nat.le_ceil (4 * Real.log (‖x‖ / ε)))
    simpa [hg] using hr
  constructor
  · intro N
    have hr := bound 0 N (by simp)
    simpa [hg] using hr
  · intro hx
    have hl := Real.log_nonpos (div_nonneg (norm_nonneg x) hε.le)
      ((div_le_one hε).mpr hx)
    have hr := bound x 0 (by intro _; simpa only [sub_zero, div_one, Nat.cast_zero, show (2:ℝ)*2=4 by norm_num] using mul_nonpos_of_nonneg_of_nonpos (by norm_num : (0:ℝ)≤4) hl)
    simpa [hg] using hr

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentComplexity.distance_le_of_log_bound
