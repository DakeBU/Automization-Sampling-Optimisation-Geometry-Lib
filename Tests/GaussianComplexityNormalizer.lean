import AutoSamplingTheory.ExampleCases.GaussianComplexity.Normalizer
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.NormNum.RealSqrt

open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/- The two determinant components and odd/even dimensions exercise the real
square-root branch and the sign in equation (18), at the source endpoint κ=4. -/
example : singleBlockPrecision 4 (1 : orthogonalGroup (Fin 3) ℝ) =
    (1 / 4 : ℝ) •
      ((((Real.sqrt 4 + 1) • (1 : Matrix (Fin 3) (Fin 3) ℝ) -
        (Real.sqrt 4 - 1) • (1 : orthogonalGroup (Fin 3) ℝ).val).transpose) *
       ((Real.sqrt 4 + 1) • (1 : Matrix (Fin 3) (Fin 3) ℝ) -
        (Real.sqrt 4 - 1) • (1 : orthogonalGroup (Fin 3) ℝ).val)) :=
  singleBlockPrecision_factorization (by decide) (by norm_num) 1

private theorem negative_identity_precision (n : ℕ) :
    singleBlockPrecision 4 (-1 : orthogonalGroup (Fin n) ℝ) =
      (4 : ℝ) • (1 : Matrix (Fin n) (Fin n) ℝ) := by
  ext i j
  simp [singleBlockPrecision, Unitary.coe_neg, Matrix.smul_apply, Matrix.one_apply]
  split <;> norm_num

example : Real.sqrt (singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 3) ℝ)).det = 8 := by
  rw [singleBlockPrecision_sqrt_det (by decide) (by norm_num)]
  have hm : ((Real.sqrt (4 : ℝ) + 1) • (1 : Matrix (Fin 3) (Fin 3) ℝ) -
      (Real.sqrt 4 - 1) • (-1 : orthogonalGroup (Fin 3) ℝ).val) =
      (4 : ℝ) • (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
    ext i j
    by_cases hij : i = j <;>
      norm_num [Unitary.coe_neg, Matrix.smul_apply, Matrix.one_apply, hij]
  rw [hm, Matrix.det_smul, Matrix.det_one]
  norm_num

example : (-1 : orthogonalGroup (Fin 3) ℝ).val.det *
    Real.sqrt (singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 3) ℝ)).det = -8 := by
  rw [singleBlockPrecision_signed_sqrt_det (by decide) (by norm_num)]
  have hm : ((Real.sqrt (4 : ℝ) + 1) • (-1 : orthogonalGroup (Fin 3) ℝ).val -
      (Real.sqrt 4 - 1) • (1 : Matrix (Fin 3) (Fin 3) ℝ)) =
      (-4 : ℝ) • (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
    ext i j
    by_cases hij : i = j <;>
      norm_num [Unitary.coe_neg, Matrix.smul_apply, Matrix.one_apply, hij]
  rw [hm, Matrix.det_smul, Matrix.det_one]
  norm_num

example : (-1 : orthogonalGroup (Fin 4) ℝ).val.det *
    Real.sqrt (singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 4) ℝ)).det = 16 := by
  rw [negative_identity_precision, Matrix.det_smul, Matrix.det_one]
  norm_num [Unitary.coe_neg, Matrix.det_neg]

#print axioms singleBlockPrecision_factorization
#print axioms singleBlockPrecision_sqrt_det
#print axioms singleBlockPrecision_signed_sqrt_det
