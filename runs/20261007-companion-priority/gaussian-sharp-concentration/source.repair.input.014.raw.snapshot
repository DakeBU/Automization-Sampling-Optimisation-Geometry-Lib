import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Analysis.InnerProductSpace.PiL2

noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential

namespace Tests.GaussianLipschitzExponential

-- A nonlinear unbounded observable, with a negative signed parameter.
theorem nonlinear_negative_parameter :
    Integrable (fun x : ℝ => Real.exp ((-3)*(‖x‖-∫ z : ℝ, ‖z‖ ∂stdGaussian ℝ)))
      (stdGaussian ℝ) := by
  have hf : LipschitzWith 1 (fun x : ℝ => ‖x‖) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    simpa only [dist_eq_norm, Real.norm_eq_abs, NNReal.coe_one, one_mul] using
      abs_norm_sub_norm_le x y
  exact (integrable_and_integrable_exp_centered_of_lipschitz
    (μ := stdGaussian ℝ) hf).2 (-3)

-- Zero direction is retained, with no positive Lipschitz constant assumption.
theorem zero_lipschitz_constant (c t : ℝ) :
    Integrable (fun x : ℝ => Real.exp (t*((fun _ : ℝ => c) x-
      ∫ z : ℝ, (fun _ : ℝ => c) z ∂stdGaussian ℝ))) (stdGaussian ℝ) := by
  have hf : LipschitzWith 0 (fun _ : ℝ => c) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    simp
  exact (integrable_and_integrable_exp_centered_of_lipschitz
    (μ := stdGaussian ℝ) hf).2 t

-- Degenerate zero-dimensional standard Gaussian, arbitrary signed parameter.
abbrev E0 := EuclideanSpace ℝ (Fin 0)
theorem zero_dimension (t : ℝ) :
    Integrable (fun x : E0 => Real.exp (t*(‖x‖-∫ z : E0, ‖z‖ ∂stdGaussian E0)))
      (stdGaussian E0) := by
  have hf : LipschitzWith 0 (fun x : E0 => ‖x‖) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    have hxy : x=y := Subsingleton.elim _ _
    simp [hxy]
  exact (integrable_and_integrable_exp_centered_of_lipschitz
    (μ := stdGaussian E0) hf).2 t

#print axioms integrable_and_integrable_exp_centered_of_lipschitz
#print axioms nonlinear_negative_parameter
#print axioms zero_lipschitz_constant
#print axioms zero_dimension

-- This unbounded observable is not C1 at zero; the sharp theorem must remove
-- its internal differentiability restriction, including for negative t.
theorem nonlinear_sharp_negative_parameter :
    (∫ x : ℝ, Real.exp ((-3) * (‖x‖ - ∫ z : ℝ, ‖z‖ ∂stdGaussian ℝ)) ∂stdGaussian ℝ) ≤
      Real.exp (9 / 2) := by
  have h := integral_exp_centered_le_stdGaussian_of_lipschitz
    (lipschitzWith_one_norm : LipschitzWith 1 (norm : ℝ → ℝ)) (-3)
  norm_num at h ⊢
  exact h

theorem sharp_zero_lipschitz_constant (c t : ℝ) :
    (∫ x : ℝ, Real.exp (t * (c - ∫ z : ℝ, (fun _ : ℝ => c) z ∂stdGaussian ℝ))
      ∂stdGaussian ℝ) ≤ 1 := by
  have hf : LipschitzWith 0 (fun _ : ℝ => c) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    simp
  simpa using integral_exp_centered_le_stdGaussian_of_lipschitz hf t

-- Positive stated Lipschitz constant on zero dimension exercises the separate
-- degenerate-space branch, rather than only the zero-constant branch.
theorem sharp_zero_dimension (t : ℝ) :
    (∫ x : E0, Real.exp (t * (‖x‖ - ∫ z : E0, ‖z‖ ∂stdGaussian E0)) ∂stdGaussian E0) ≤
      Real.exp (t^2 / 2) := by
  simpa only [NNReal.coe_one, one_pow, one_mul] using
    integral_exp_centered_le_stdGaussian_of_lipschitz
      (lipschitzWith_one_norm : LipschitzWith 1 (norm : E0 → ℝ)) t

#print axioms integral_exp_centered_le_stdGaussian_of_lipschitz
#print axioms nonlinear_sharp_negative_parameter
#print axioms sharp_zero_lipschitz_constant
#print axioms sharp_zero_dimension
end Tests.GaussianLipschitzExponential
end
