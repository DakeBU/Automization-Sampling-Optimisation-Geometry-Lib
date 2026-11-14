import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Tactic

/-!
# Gaussian fourth moment

The one scalar moment needed for the Brownian quadratic-variation `L2` estimate:

`E[X^4] = 3 v^2` for `X ~ N(0,v)`.

This is proved from Mathlib's Gaussian moment-generating function and
`iteratedDeriv_mgf_zero`, following the same route used by Mathlib to prove the
Gaussian variance formula.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace GaussianFourthMoment

open MeasureTheory ProbabilityTheory Real
open scoped NNReal ProbabilityTheory

/-- Fourth moment of a centered real Gaussian with variance `v`. -/
theorem integral_pow_four_gaussianReal_zero (v : ℝ≥0) :
    ∫ x : ℝ, x ^ 4 ∂(gaussianReal 0 v) = 3 * (v : ℝ) ^ 2 := by
  calc
    ∫ x : ℝ, x ^ 4 ∂(gaussianReal 0 v) =
        iteratedDeriv 4 (mgf (fun x : ℝ => x) (gaussianReal 0 v)) 0 := by
      rw [iteratedDeriv_mgf_zero] <;> simp
    _ = 3 * (v : ℝ) ^ 2 := by
      rw [mgf_fun_id_gaussianReal, iteratedDeriv_succ, iteratedDeriv_succ,
        iteratedDeriv_succ, iteratedDeriv_one]
      simp only [zero_mul, zero_add]
      let g : ℝ → ℝ := fun t => rexp ((v : ℝ) * t ^ 2 / 2)
      let g₁ : ℝ → ℝ := fun t => (v : ℝ) * t * rexp ((v : ℝ) * t ^ 2 / 2)
      let g₂ : ℝ → ℝ := fun t =>
        ((v : ℝ) + (v : ℝ) ^ 2 * t ^ 2) * rexp ((v : ℝ) * t ^ 2 / 2)
      let g₃ : ℝ → ℝ := fun t =>
        (3 * (v : ℝ) ^ 2 * t + (v : ℝ) ^ 3 * t ^ 3) *
          rexp ((v : ℝ) * t ^ 2 / 2)
      have hg₁ : deriv g = g₁ := by
        funext t
        dsimp [g, g₁]
        rw [_root_.deriv_exp (by fun_prop)]
        simp only [deriv_div_const, differentiableAt_const, differentiableAt_fun_id,
          Nat.cast_ofNat, DifferentiableAt.fun_pow, deriv_fun_mul, deriv_const', zero_mul,
          deriv_fun_pow, Nat.add_one_sub_one, pow_one, deriv_id'', mul_one, zero_add]
        ring
      have hg₂ : deriv g₁ = g₂ := by
        funext t
        dsimp [g₁, g₂]
        rw [deriv_fun_mul (by fun_prop) (by fun_prop),
          deriv_fun_mul (by fun_prop) (by fun_prop),
          _root_.deriv_exp (by fun_prop)]
        simp only [deriv_div_const, differentiableAt_const, differentiableAt_fun_id,
          Nat.cast_ofNat, DifferentiableAt.fun_pow, deriv_fun_mul, deriv_const', zero_mul,
          deriv_fun_pow, Nat.add_one_sub_one, pow_one, deriv_id'', mul_one, zero_add]
        ring
      have hg₃ : deriv g₂ = g₃ := by
        funext t
        dsimp [g₂, g₃]
        rw [deriv_fun_mul (by fun_prop) (by fun_prop),
          deriv_fun_add (by fun_prop) (by fun_prop),
          deriv_fun_mul (by fun_prop) (by fun_prop),
          _root_.deriv_exp (by fun_prop)]
        simp only [deriv_div_const, differentiableAt_const, differentiableAt_fun_id,
          Nat.cast_ofNat, DifferentiableAt.fun_pow, deriv_fun_mul, deriv_const', zero_mul,
          deriv_fun_pow, Nat.add_one_sub_one, pow_one, deriv_id'', mul_one, zero_add]
        ring
      have hg₄ : deriv g₃ = fun t =>
          (3 * (v : ℝ) ^ 2 + 6 * (v : ℝ) ^ 3 * t ^ 2 +
            (v : ℝ) ^ 4 * t ^ 4) * rexp ((v : ℝ) * t ^ 2 / 2) := by
        funext t
        dsimp [g₃]
        rw [deriv_fun_mul (by fun_prop) (by fun_prop),
          deriv_fun_add (by fun_prop) (by fun_prop),
          deriv_fun_mul (by fun_prop) (by fun_prop),
          deriv_fun_mul (by fun_prop) (by fun_prop),
          _root_.deriv_exp (by fun_prop)]
        simp only [deriv_div_const, differentiableAt_const, differentiableAt_fun_id,
          Nat.cast_ofNat, DifferentiableAt.fun_pow, deriv_fun_mul, deriv_const', zero_mul,
          deriv_fun_pow, Nat.add_one_sub_one, pow_one, deriv_id'', mul_one, zero_add,
          deriv_fun_add]
        ring
      change deriv (deriv (deriv (deriv g))) 0 = 3 * (v : ℝ) ^ 2
      rw [hg₁, hg₂, hg₃, hg₄]
      simp

end GaussianFourthMoment
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
