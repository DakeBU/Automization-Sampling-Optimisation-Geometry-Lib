import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.Data.Real.Star
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# The determinant family's single-block precision

Literal equation (4) and the single-block argument of Appendix B.3,
equation (26), in Zhou--Suzuki, arXiv:2610.20492v1.
The full block-diagonal construction and unique minimizer are separate obligations.
-/

open Matrix

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/-- The literal single-block precision in source equation (4). -/
noncomputable def singleBlockPrecision {n : ℕ} (κ : ℝ)
    (O : Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin n) (Fin n) ℝ :=
  ((κ + 1) / 2) • (1 : Matrix (Fin n) (Fin n) ℝ) -
    ((κ - 1) / 4) • ((O : Matrix (Fin n) (Fin n) ℝ) +
      (O : Matrix (Fin n) (Fin n) ℝ).transpose)

/-- Appendix B.3, equation (26), retaining the source's standing n and κ range. -/
theorem singleBlockPrecision_regular {n : ℕ} (_hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    (singleBlockPrecision κ O).IsHermitian ∧
      ∀ v : Fin n → ℝ,
        v ⬝ᵥ v ≤ v ⬝ᵥ (singleBlockPrecision κ O *ᵥ v) ∧
        v ⬝ᵥ (singleBlockPrecision κ O *ᵥ v) ≤ κ * (v ⬝ᵥ v) := by
  constructor
  · rw [Matrix.isHermitian_iff_isSymm]
    unfold Matrix.IsSymm singleBlockPrecision
    simp only [Matrix.transpose_sub, Matrix.transpose_smul, Matrix.transpose_one,
      Matrix.transpose_add, Matrix.transpose_transpose]
    rw [add_comm (O : Matrix (Fin n) (Fin n) ℝ).transpose]
  · intro v
    have horth : (O : Matrix (Fin n) (Fin n) ℝ).transpose *
        (O : Matrix (Fin n) (Fin n) ℝ) = 1 :=
      (Matrix.mem_orthogonalGroup_iff' (Fin n) ℝ).mp O.property
    have hiso : ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) ⬝ᵥ
        ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) = v ⬝ᵥ v := by
      rw [dotProduct_comm, ← Matrix.dotProduct_transpose_mulVec,
        Matrix.mulVec_mulVec, horth, Matrix.one_mulVec]
    have hq : 0 ≤ v ⬝ᵥ v := by
      exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (v i))
    have hcs : (v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)) ^ 2 ≤
        (v ⬝ᵥ v) ^ 2 := by
      have h := Finset.sum_mul_sq_le_sq_mul_sq Finset.univ v
        ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)
      simp only [pow_two] at h ⊢
      change (v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)) *
          (v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)) ≤
        (v ⬝ᵥ v) * (((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) ⬝ᵥ
          ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)) at h
      rw [hiso] at h
      exact h
    have hcross : -(v ⬝ᵥ v) ≤ v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) ∧
        v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) ≤ v ⬝ᵥ v := by
      constructor <;> nlinarith
    have htranspose : v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ v) =
        v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v) :=
      Matrix.dotProduct_transpose_mulVec _ _ _
    have hexpand : v ⬝ᵥ (singleBlockPrecision κ O *ᵥ v) =
        ((κ + 1) / 2) * (v ⬝ᵥ v) -
          ((κ - 1) / 2) * (v ⬝ᵥ ((O : Matrix (Fin n) (Fin n) ℝ) *ᵥ v)) := by
      simp only [singleBlockPrecision, Matrix.sub_mulVec, Matrix.smul_mulVec,
        Matrix.add_mulVec, Matrix.one_mulVec, dotProduct_sub, dotProduct_smul,
        dotProduct_add, htranspose, smul_eq_mul]
      ring
    have hc : 0 ≤ (κ - 1) / 2 := by linarith
    have hlow := mul_le_mul_of_nonneg_left hcross.2 hc
    have hupp := mul_le_mul_of_nonneg_left hcross.1 hc
    rw [hexpand]
    constructor <;> nlinarith

end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
