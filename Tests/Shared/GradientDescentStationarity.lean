import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul

open AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity
open Set
open scoped BigOperators RealInnerProductSpace

-- Actual quadratic gradient, arbitrary positive admissible step, and a nonempty range.
example (h x : ℝ) (hh : 0 < h) (hs : h ≤ 1) {N : ℕ} (hN : 0 < N) :
    ∃ k ∈ Finset.range N,
      ‖gradient (fun t : ℝ => t ^ 2 / 2)
        ((fun t => t - h * gradient (fun t : ℝ => t ^ 2 / 2) t)^[k] x)‖ ≤
      Real.sqrt (x ^ 2 / ((N : ℝ) * h)) := by
  have hg (t : ℝ) : gradient (fun t : ℝ => t ^ 2 / 2) t = t := by
    have hd : HasDerivAt (fun t : ℝ => t ^ 2 / 2) t t := by
      simpa using ((hasDerivAt_id t).pow 2).div_const (2 : ℝ)
    exact hd.hasGradientAt.gradient
  have hr := exists_gradient_descent_norm_le (f := fun t : ℝ => t ^ 2 / 2)
    (β := 1) (h := h) (z := 0)
    (by intro t _; change (0 : ℝ)^2 / 2 ≤ t^2 / 2; nlinarith [sq_nonneg t])
    hh (by simpa using hs)
    (by intro a b; rw [hg]; simp only [Real.inner_apply, Real.norm_eq_abs, sq_abs];
        nlinarith [sq_nonneg (b-a)]) x hN
  have he : 2 * (x ^ 2 / 2 - (0 : ℝ) ^ 2 / 2) = x ^ 2 := by ring
  simpa only [he, smul_eq_mul] using hr

-- A constant objective has beta=0: no reciprocal step restriction is silently added.
-- N=1 includes x0 itself and the zero-gap conclusion is exactly a zero gradient.
example (x : ℝ) : ∃ k ∈ Finset.range 1,
    ‖gradient (fun _ : ℝ => (7 : ℝ))
      ((fun t => t - (2 : ℝ) • gradient (fun _ : ℝ => (7 : ℝ)) t)^[k] x)‖ ≤ 0 := by
  have hr := exists_gradient_descent_norm_le (f := fun _ : ℝ => (7 : ℝ))
    (β := 0) (h := 2) (z := 0)
    (by intro t _; change (7 : ℝ) ≤ 7; rfl) (by norm_num) (by norm_num)
    (by intro a b; simp) x (N := 1) (by norm_num)
  simpa only [sub_self, mul_zero, zero_div, Real.sqrt_zero] using hr

-- Unnormalized accumulation permits h=0 and N=0, unlike the divided statement.
example {f : ℝ → ℝ} {β : ℝ}
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y-x) + β/2 * ‖y-x‖^2)
    (x : ℝ) (N : ℕ) :
    (0 : ℝ) / 2 * ∑ k ∈ Finset.range N,
      ‖gradient f ((fun t => t - (0 : ℝ) • gradient f t)^[k] x)‖^2 ≤
      f x - f ((fun t => t - (0 : ℝ) • gradient f t)^[N] x) :=
  gradient_descent_sum_sq_bound (by norm_num) (by simp) hu x N

#print axioms gradient_descent_sum_sq_bound
#print axioms exists_gradient_descent_norm_le
