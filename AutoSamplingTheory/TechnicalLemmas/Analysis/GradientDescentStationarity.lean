import AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentBasic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Analysis.Real.Sqrt

/-!
# Nonconvex gradient descent and approximate stationarity

Chewi arXiv:2605.07006v1 Theorem 3.7 and its telescoping proof.
The upper model uses the actual gradient; no convexity or PL inequality is assumed.
The normalized conclusion requires positive step and nonempty iteration range.
The supplied global minimizer retains the source's attainment convention.
The algebraic upper-model formulation extends the source's smooth Euclidean setting.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity

open Set
open scoped BigOperators RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Telescoping the actual gradient-step decrease bounds the accumulated squared gradients.
This unnormalized inequality includes zero steps and empty sums. -/
theorem gradient_descent_sum_sq_bound {f : E → ℝ} {β h : ℝ}
    (hh : 0 ≤ h) (hstep : β * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x₀ : E) (N : ℕ) :
    h / 2 * ∑ k ∈ Finset.range N, ‖gradient f ((fun x => x - h • gradient f x)^[k] x₀)‖ ^ 2 ≤
      f x₀ - f ((fun x => x - h • gradient f x)^[N] x₀) := by
  let T : E → E := fun x => x - h • gradient f x
  calc
    h / 2 * ∑ k ∈ Finset.range N, ‖gradient f (T^[k] x₀)‖ ^ 2 =
        ∑ k ∈ Finset.range N, h / 2 * ‖gradient f (T^[k] x₀)‖ ^ 2 := Finset.mul_sum _ _ _
    _ ≤ ∑ k ∈ Finset.range N, (f (T^[k] x₀) - f (T^[k + 1] x₀)) := by
      apply Finset.sum_le_sum
      intro k _
      rw [Function.iterate_succ_apply']
      have hd := GradientDescentBasic.gradient_step_descent_of_quadratic_upper_bound
        hh hstep hu (T^[k] x₀)
      change h / 2 * ‖gradient f (T^[k] x₀)‖ ^ 2 ≤ f (T^[k] x₀) - f (T (T^[k] x₀))
      dsimp [T] at *
      linarith
    _ = f x₀ - f (T^[N] x₀) := by
      simpa using Finset.sum_range_sub' (fun k => f (T^[k] x₀)) N

/-- Among the first `N` actual gradient iterates, one has small gradient norm.
This is a best-iterate guarantee, not a last-iterate or global optimality guarantee. -/
theorem exists_gradient_descent_norm_le {f : E → ℝ} {β h : ℝ} {z : E}
    (hz : IsMinOn f univ z) (hh : 0 < h) (hstep : β * h ≤ 1)
    (hu : ∀ x y, f y ≤ f x + inner ℝ (gradient f x) (y - x) + β / 2 * ‖y - x‖ ^ 2)
    (x₀ : E) {N : ℕ} (hN : 0 < N) :
    ∃ k ∈ Finset.range N,
      ‖gradient f ((fun x => x - h • gradient f x)^[k] x₀)‖ ≤
        Real.sqrt (2 * (f x₀ - f z) / ((N : ℝ) * h)) := by
  let T : E → E := fun x => x - h • gradient f x
  let B : ℝ := 2 * (f x₀ - f z) / ((N : ℝ) * h)
  have hNr : 0 < (N : ℝ) := by exact_mod_cast hN
  have hd := gradient_descent_sum_sq_bound hh.le hstep hu x₀ N
  have hzN : f z ≤ f (T^[N] x₀) := hz (mem_univ _)
  have hsum : (∑ k ∈ Finset.range N, ‖gradient f (T^[k] x₀)‖ ^ 2) ≤
      ∑ _k ∈ Finset.range N, B := by
    have hb : h / 2 * ((N : ℝ) * B) = f x₀ - f z := by
      dsimp [B]
      field_simp
    simp only [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
    apply (mul_le_mul_iff_right₀ (show 0 < h / 2 by positivity)).mp
    change h / 2 * (∑ k ∈ Finset.range N, ‖gradient f (T^[k] x₀)‖ ^ 2) ≤
      h / 2 * ((N : ℝ) * B)
    rw [hb]
    change h / 2 * (∑ k ∈ Finset.range N, ‖gradient f (T^[k] x₀)‖ ^ 2) ≤
      f x₀ - f (T^[N] x₀) at hd
    linarith
  obtain ⟨k, hk, hkle⟩ := Finset.exists_le_of_sum_le ⟨0, Finset.mem_range.mpr hN⟩ hsum
  refine ⟨k, hk, ?_⟩
  exact Real.le_sqrt_of_sq_le hkle

end AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentStationarity
