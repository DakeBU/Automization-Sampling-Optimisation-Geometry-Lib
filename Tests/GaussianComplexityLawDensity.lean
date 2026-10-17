import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
import Mathlib.Tactic.NormNum.RealSqrt
import Mathlib.LinearAlgebra.Matrix.Notation

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity

-- The generic theorem includes the empty Euclidean space with unit volume.
example : multivariateGaussian (0 : EuclideanSpace ℝ (Fin 0))
    ((1 : Matrix (Fin 0) (Fin 0) ℝ)⁻¹) = volume := by
  have h := multivariateGaussian_eq_withDensity_of_posDef
    (1 : Matrix (Fin 0) (Fin 0) ℝ) (by simpa using Matrix.PosDef.one (n := Fin 0) (R := ℝ))
  simpa using h

-- A genuinely anisotropic precision: coefficient 2 and real dimension-half 3/2.
example : multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
    ((Matrix.diagonal ![4, 1, 1] : Matrix (Fin 3) (Fin 3) ℝ)⁻¹) =
    (volume : Measure (EuclideanSpace ℝ (Fin 3))).withDensity (fun x =>
      ENNReal.ofReal (2 / (2 * Real.pi) ^ (3 / 2 : ℝ) *
        Real.exp (-(4 * (WithLp.ofLp x 0) ^ 2 + (WithLp.ofLp x 1) ^ 2 +
          (WithLp.ofLp x 2) ^ 2) / 2))) := by
  have hA : (Matrix.diagonal ![4, 1, 1] : Matrix (Fin 3) (Fin 3) ℝ).PosDef := by
    rw [Matrix.posDef_diagonal_iff]
    intro i
    fin_cases i <;> norm_num
  have h := multivariateGaussian_eq_withDensity_of_posDef _ hA
  rw [h]
  apply withDensity_congr_ae
  exact Filter.Eventually.of_forall fun x => by
    have hd : (Matrix.diagonal ![4, 1, 1] : Matrix (Fin 3) (Fin 3) ℝ).det = 4 := by
      norm_num [Matrix.det_diagonal, Fin.prod_univ_succ]
    have hq : (WithLp.ofLp x) ⬝ᵥ
        ((Matrix.diagonal ![4, 1, 1] : Matrix (Fin 3) (Fin 3) ℝ) *ᵥ WithLp.ofLp x) =
        4 * (WithLp.ofLp x 0) ^ 2 + (WithLp.ofLp x 1) ^ 2 + (WithLp.ofLp x 2) ^ 2 := by
      simp [Matrix.mulVec_diagonal, dotProduct, Fin.sum_univ_succ]
      ring
    dsimp only
    rw [hd, hq]
    norm_num

-- The source adapter supplies SPD itself, for every full orthogonal input.
example (O : Matrix.orthogonalGroup (Fin 3) ℝ) :
    IsProbabilityMeasure ((volume : Measure (EuclideanSpace ℝ (Fin 3))).withDensity
      (fun x => ENNReal.ofReal (Real.sqrt (singleBlockPrecision 4 O).det /
        (2 * Real.pi) ^ (3 / 2 : ℝ) * Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision 4 O *ᵥ WithLp.ofLp x)) / 2)))) := by
  have h := gaussian_law_eq_density (n := 3) (by decide) (κ := 4) (by norm_num) O
  norm_num only [Nat.cast_ofNat] at h
  rw [← h]
  infer_instance

#print axioms multivariateGaussian_eq_withDensity_of_posDef
#print axioms gaussian_law_eq_density
