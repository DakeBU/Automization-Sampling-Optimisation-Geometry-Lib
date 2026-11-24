import GC47Witness
import Mathlib.LinearAlgebra.Matrix.Rank

/-! The dimension of the literal power Krylov span from a nonzero minor. -/
noncomputable section
open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

/-- The eigenvalues on the midpoint grid in equation (11). -/
def gridNode (d : ℕ) (κ : ℝ) (i : Fin d) : ℝ :=
  (κ+1)/2 + (κ-1)/2 * Real.cos (gridAngle d i)

private theorem strictAnti_cos_gridAngle (d : ℕ) :
    StrictAnti (fun i : Fin d => Real.cos (gridAngle d i)) := by
  intro i j hij
  have hd : (0 : ℝ) < d := by exact_mod_cast (Nat.zero_lt_of_lt j.isLt)
  have hij' : (i.val : ℝ) < j.val := by exact_mod_cast hij
  have hj : (j.val : ℝ) + 1 ≤ d := by exact_mod_cast j.isLt
  apply Real.cos_lt_cos_of_nonneg_of_le_pi
  · unfold gridAngle
    positivity
  · unfold gridAngle
    apply (div_le_iff₀ hd).2
    nlinarith [Real.pi_pos, mul_nonneg (sub_nonneg.mpr hj) Real.pi_pos.le]
  · unfold gridAngle
    exact div_lt_div_of_pos_right (mul_lt_mul_of_pos_right (by linarith) Real.pi_pos) hd

theorem gridNode_injective (d : ℕ) {κ : ℝ} (hκ : κ ≠ 1) :
    Function.Injective (gridNode d κ) := by
  intro i j hij
  apply (strictAnti_cos_gridAngle d).injective
  exact mul_left_cancel₀ (show (κ-1)/2 ≠ 0 by exact div_ne_zero (sub_ne_zero.mpr hκ) (by norm_num))
    (add_left_cancel hij)

abbrev generatorMatrix (d q : ℕ) (κ : ℝ) (g : Starts d q) : Matrix (Fin d) (Indices q) ℝ :=
  monomialMatrix (gridNode d κ) g

theorem generatorMatrix_col (d q : ℕ) (κ : ℝ) (g : Starts d q) (a : Indices q) :
    (generatorMatrix d q κ g).col a =
      (diagonalPrecision d κ ^ a.2.val) *ᵥ WithLp.ofLp (g a.1) := by
  ext i
  simp only [diagonalPrecision, Matrix.diagonal_pow, Matrix.mulVec_diagonal]
  rfl

theorem finrank_krylov_eq_rank (d q : ℕ) (κ : ℝ) (g : Starts d q) :
    Module.finrank ℝ (krylov d q κ g) = (generatorMatrix d q κ g).rank := by
  rw [Matrix.rank_eq_finrank_span_cols, krylov, funext (generatorMatrix_col d q κ g)]

theorem finrank_krylov_le (d q : ℕ) (κ : ℝ) (g : Starts d q) :
    Module.finrank ℝ (krylov d q κ g) ≤ min d ((q+1)^2) := by
  rw [finrank_krylov_eq_rank]
  apply le_min
  · simpa using (generatorMatrix d q κ g).rank_le_card_height
  · simpa [Indices, pow_two] using (generatorMatrix d q κ g).rank_le_card_width

theorem finrank_krylov_of_minor {d q : ℕ} {κ : ℝ} (g : Starts d q)
    (row : Fin (min d ((q+1)^2)) → Fin d) (col : Fin (min d ((q+1)^2)) → Indices q)
    (hdet : ((generatorMatrix d q κ g).submatrix row col).det ≠ 0) :
    Module.finrank ℝ (krylov d q κ g) = min d ((q+1)^2) := by
  apply le_antisymm (finrank_krylov_le ..)
  rw [finrank_krylov_eq_rank]
  simpa only [Matrix.rank_of_det_ne_zero hdet, Fintype.card_fin] using
    (generatorMatrix d q κ g).rank_submatrix_le row col

/-- At unit condition number the powers of the precision matrix repeat each start. -/
theorem krylov_one (d q : ℕ) (g : Starts d q) :
    krylov d q 1 g = Submodule.span ℝ (Set.range (fun a => WithLp.ofLp (g a))) := by
  have hD : diagonalPrecision d 1 = 1 := by
    unfold diagonalPrecision
    convert Matrix.diagonal_one (n := Fin d) (α := ℝ) using 1
    norm_num
  rw [krylov, hD]
  congr 1
  ext x
  constructor
  · rintro ⟨a,rfl⟩
    exact ⟨a.1, by simp⟩
  · rintro ⟨a,rfl⟩
    exact ⟨(a,0), by simp⟩

#print axioms gridNode_injective
#print axioms finrank_krylov_of_minor
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
