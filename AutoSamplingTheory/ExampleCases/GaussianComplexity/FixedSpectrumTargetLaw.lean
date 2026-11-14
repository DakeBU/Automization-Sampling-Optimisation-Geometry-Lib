import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Adjoint

open Matrix MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace
set_option autoImplicit false

/-!
# Actual orthogonal Gaussian target law

Zhou--Suzuki arXiv:2610.20492v1, Section4.2 Lemma4.5 coordinate-law
explanation and AppendixC.3. The actual diagonal inverse-precision Gaussian
pushed by the full real orthogonal matvec is the actual target with covariance
A inverse. This is a fixed-O full-measure identity, not a joint conditional,
Haar/adaptive algorithm, probability, oracle or query-cost assertion.
-/
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw

theorem actual_rotated_gaussian_target {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ) (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let R : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun z => WithLp.toLp 2 ((O : Matrix (Fin d) (Fin d) ℝ) *ᵥ WithLp.ofLp z)
  (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹).map R =
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
:= by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let U : Matrix (Fin d) (Fin d) ℝ := O
  let A : Matrix (Fin d) (Fin d) ℝ := U * Λ * U.transpose
  let μ : Measure E := multivariateGaussian (0 : E) Λ⁻¹
  let ν : Measure E := multivariateGaussian (0 : E) A⁻¹
  let T : E →L[ℝ] E := Matrix.toEuclideanCLM (𝕜 := ℝ) U
  have hApos : A.PosDef :=
    (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible hd hκ O).1
  have hΛpos : Λ.PosDef := by
    have h :=
      (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility.actual_precision_admissible
        hd hκ (1 : Matrix.orthogonalGroup (Fin d) ℝ)).1
    simpa [Λ, θ] using h
  have hOleft : U.transpose * U = 1 :=
    (Matrix.mem_orthogonalGroup_iff' (n := Fin d) (R := ℝ)).mp O.property
  have hOright : U * U.transpose = 1 :=
    (Matrix.mem_orthogonalGroup_iff (n := Fin d) (R := ℝ)).mp O.property
  have hΛunit : IsUnit Λ.det := (Matrix.isUnit_iff_isUnit_det _).mp hΛpos.isUnit
  have hinv : A⁻¹ = U * Λ⁻¹ * U.transpose := by
    apply Matrix.inv_eq_left_inv
    change (U * Λ⁻¹ * U.transpose) * (U * Λ * U.transpose) = 1
    calc
      _ = U * (Λ⁻¹ * (U.transpose * U) * Λ) * U.transpose := by
        simp only [Matrix.mul_assoc]
      _ = U * (Λ⁻¹ * Λ) * U.transpose := by rw [hOleft, Matrix.mul_one]
      _ = 1 := by
        rw [Matrix.nonsing_inv_mul _ hΛunit, Matrix.mul_one]
        exact hOright
  have hstar : T.adjoint = Matrix.toEuclideanCLM (𝕜 := ℝ) U.transpose := by
    change star (Matrix.toEuclideanCLM (𝕜 := ℝ) U) = _
    rw [← map_star]
    simp only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
  have hop : T * Matrix.toEuclideanCLM (𝕜 := ℝ) Λ⁻¹ * T.adjoint =
      Matrix.toEuclideanCLM (𝕜 := ℝ) A⁻¹ := by
    simp only [hinv, map_mul, hstar, T]
  change μ.map T = ν
  apply IsGaussian.ext
  · change (∫ x, x ∂μ.map T) = ∫ x, x ∂ν
    rw [ContinuousLinearMap.integral_id_map IsGaussian.integrable_id]
    change T (∫ x : EuclideanSpace ℝ (Fin d), x ∂multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) Λ⁻¹) =
      ∫ x : EuclideanSpace ℝ (Fin d), x ∂multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    rw [integral_id_multivariateGaussian, integral_id_multivariateGaussian, map_zero]
  · ext x y
    rw [covarianceBilin_map IsGaussian.memLp_two_id T]
    change covarianceBilin (multivariateGaussian (0 : E) Λ⁻¹) (T.adjoint x) (T.adjoint y) =
      covarianceBilin (multivariateGaussian (0 : E) A⁻¹) x y
    rw [covarianceBilin_multivariateGaussian hΛpos.inv.posSemidef,
      covarianceBilin_multivariateGaussian hApos.inv.posSemidef]
    rw [← Matrix.inner_toEuclideanCLM, ← Matrix.inner_toEuclideanCLM,
      ContinuousLinearMap.adjoint_inner_left]
    change inner ℝ x ((T * Matrix.toEuclideanCLM (𝕜 := ℝ) Λ⁻¹ * T.adjoint) y) =
      inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) A⁻¹ y)
    rw [hop]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetLaw
