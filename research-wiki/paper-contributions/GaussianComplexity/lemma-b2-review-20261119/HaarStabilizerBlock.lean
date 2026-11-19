import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Topology.Algebra.Star.Unitary
import Mathlib.Topology.Instances.Matrix

open Matrix

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock

set_option autoImplicit false

abbrev Square (n : ℕ) := Matrix (Fin n) (Fin n) ℝ
abbrev Orthogonal (n : ℕ) := Matrix.orthogonalGroup (Fin n) ℝ

/-- Insert an initial row and column with diagonal entry one and other entries zero. -/
def blockMatrix {n : ℕ} (A : Square n) : Square (n + 1) :=
  fun i j => Fin.cases (Fin.cases 1 (fun _ => 0) j)
    (fun a => Fin.cases 0 (fun b => A a b) j) i

/-- Extract the lower block, indexed without the initial coordinate. -/
def lowerBlock {n : ℕ} (W : Square (n + 1)) : Square n :=
  W.submatrix Fin.succ Fin.succ

theorem continuous_lowerBlock (n : ℕ) :
    Continuous (lowerBlock (n := n)) :=
  continuous_matrix fun i j => continuous_id.matrix_elem i.succ j.succ

@[simp] private theorem blockMatrix_zero_zero {n : ℕ} (A : Square n) :
    blockMatrix A 0 0 = 1 := rfl

@[simp] private theorem blockMatrix_zero_succ {n : ℕ} (A : Square n) (j : Fin n) :
    blockMatrix A 0 j.succ = 0 := rfl

@[simp] private theorem blockMatrix_succ_zero {n : ℕ} (A : Square n) (i : Fin n) :
    blockMatrix A i.succ 0 = 0 := rfl

@[simp] private theorem blockMatrix_succ_succ {n : ℕ} (A : Square n) (i j : Fin n) :
    blockMatrix A i.succ j.succ = A i j := rfl

private theorem blockMatrix_one (n : ℕ) : blockMatrix (1 : Square n) = 1 := by
  ext i j
  cases i using Fin.cases <;> cases j using Fin.cases <;> simp [Matrix.one_apply]
  exact (Fin.succ_ne_zero _).symm

private theorem blockMatrix_mul {n : ℕ} (A B : Square n) :
    blockMatrix (A * B) = blockMatrix A * blockMatrix B := by
  ext i j
  cases i using Fin.cases <;> cases j using Fin.cases <;>
    simp [Matrix.mul_apply, Fin.sum_univ_succ]

private theorem blockMatrix_transpose {n : ℕ} (A : Square n) :
    blockMatrix A.transpose = (blockMatrix A).transpose := by
  ext i j
  cases i using Fin.cases <;> cases j using Fin.cases <;> rfl

/-- The group homomorphism placing the orthogonal matrix in the lower block. -/
def residualEmbed (n : ℕ) : Orthogonal n →* Orthogonal (n + 1) where
  toFun A := ⟨blockMatrix (A : Square n), by
    apply (Matrix.mem_orthogonalGroup_iff (Fin (n + 1)) ℝ).2
    rw [← blockMatrix_transpose, ← blockMatrix_mul,
      (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).mp A.property, blockMatrix_one]⟩
  map_one' := Subtype.ext (blockMatrix_one n)
  map_mul' A B := Subtype.ext (blockMatrix_mul (A : Square n) (B : Square n))

theorem residualEmbed_val {n : ℕ} (A : Orthogonal n) :
    (residualEmbed n A : Square (n + 1)) = blockMatrix (A : Square n) := rfl

theorem continuous_residualEmbed (n : ℕ) :
    Continuous (residualEmbed n) := by
  have hc : Continuous (fun A : Orthogonal n => blockMatrix (A : Square n)) := by
    apply continuous_matrix
    intro i j
    cases i using Fin.cases <;> cases j using Fin.cases
    · exact continuous_const
    · exact continuous_const
    · exact continuous_const
    · exact continuous_subtype_val.matrix_elem _ _
  exact hc.subtype_mk fun A => (residualEmbed n A).property

theorem residualEmbed_fixes {n : ℕ} (A : Orthogonal n) :
    (residualEmbed n A : Square (n + 1)) *ᵥ Pi.single (0 : Fin (n + 1)) (1 : ℝ) =
      Pi.single (0 : Fin (n + 1)) (1 : ℝ) := by
  rw [residualEmbed_val, Matrix.mulVec_single_one]
  funext i
  cases i using Fin.cases <;> simp [Matrix.col_apply]

theorem det_residualEmbed {n : ℕ} (A : Orthogonal n) :
    (residualEmbed n A : Square (n + 1)).det = (A : Square n).det := by
  rw [residualEmbed_val, Matrix.det_succ_row_zero, Fin.sum_univ_succ]
  have hminor : (blockMatrix (A : Square n)).submatrix Fin.succ
      Fin.succ = (A : Square n) := rfl
  simp [hminor]

theorem lowerBlock_residualEmbed {n : ℕ} (A : Orthogonal n) :
    lowerBlock (residualEmbed n A : Square (n + 1)) = (A : Square n) := rfl

private theorem blockMatrix_lowerBlock_of_fixes {n : ℕ} (W : Orthogonal (n + 1))
    (hW : (W : Square (n + 1)) *ᵥ Pi.single (0 : Fin (n + 1)) (1 : ℝ) =
      Pi.single (0 : Fin (n + 1)) (1 : ℝ)) :
    blockMatrix (lowerBlock (W : Square (n + 1))) = (W : Square (n + 1)) := by
  have hWT :
      (W : Square (n + 1)).transpose *ᵥ Pi.single (0 : Fin (n + 1)) (1 : ℝ) =
        Pi.single (0 : Fin (n + 1)) (1 : ℝ) := by
    conv_lhs => rw [← hW]
    rw [Matrix.mulVec_mulVec,
      (Matrix.mem_orthogonalGroup_iff' (Fin (n + 1)) ℝ).mp W.property, Matrix.one_mulVec]
  rw [Matrix.mulVec_single_one] at hW hWT
  ext i j
  cases i using Fin.cases <;> cases j using Fin.cases
  · simpa [Matrix.col_apply] using (congrFun hW (0 : Fin (n + 1))).symm
  · rename_i j
    simpa [Matrix.col_apply] using (congrFun hWT j.succ).symm
  · rename_i i
    simpa [Matrix.col_apply] using (congrFun hW i.succ).symm
  · rfl

theorem lowerBlock_mem_orthogonal_of_fixes {n : ℕ} (W : Orthogonal (n + 1))
    (hW : (W : Square (n + 1)) *ᵥ Pi.single (0 : Fin (n + 1)) (1 : ℝ) =
      Pi.single (0 : Fin (n + 1)) (1 : ℝ)) :
    lowerBlock (W : Square (n + 1)) ∈ Orthogonal n := by
  apply (Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).2
  have hb := blockMatrix_lowerBlock_of_fixes W hW
  have horth := (Matrix.mem_orthogonalGroup_iff (Fin (n + 1)) ℝ).mp W.property
  have h : blockMatrix (lowerBlock (W : Square (n + 1)) *
      (lowerBlock (W : Square (n + 1))).transpose) = blockMatrix (1 : Square n) := by
    rw [blockMatrix_mul, blockMatrix_transpose, hb, horth, blockMatrix_one]
  exact congrArg lowerBlock h

theorem residualEmbed_lowerBlock_of_fixes {n : ℕ} (W : Orthogonal (n + 1))
    (hW : (W : Square (n + 1)) *ᵥ Pi.single (0 : Fin (n + 1)) (1 : ℝ) =
      Pi.single (0 : Fin (n + 1)) (1 : ℝ)) :
    residualEmbed n ⟨lowerBlock (W : Square (n + 1)),
      lowerBlock_mem_orthogonal_of_fixes W hW⟩ = W :=
  Subtype.ext (blockMatrix_lowerBlock_of_fixes W hW)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
