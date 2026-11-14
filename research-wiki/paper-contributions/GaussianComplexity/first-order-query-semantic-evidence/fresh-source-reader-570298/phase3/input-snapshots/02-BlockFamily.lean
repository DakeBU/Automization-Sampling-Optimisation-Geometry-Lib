import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
import Mathlib.Data.Matrix.Block
import Mathlib.Logic.Equiv.Fin.Basic

/-!
# The determinant family's full block precision

Equation (5) and Lemma 3.4 / Appendix B.3, Lemma B.8, of
Zhou--Suzuki, arXiv:2610.20492v1. Coordinates are consecutive blocks,
followed by the residual identity block. No Gaussian law or oracle lower bound
is supplied by these finite-dimensional matrix statements.
-/

open Matrix
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

private def blockCoordinates (d n : ℕ) :
    ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
  ((Equiv.sumCongr
    ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
    (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
    (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))

/-- Literal equation (5), with contiguous size-n blocks and the residual identity. -/
noncomputable def blockPrecision {d n : ℕ} (κ : ℝ)
    (O : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) : Matrix (Fin d) (Fin d) ℝ :=
  Matrix.reindex (blockCoordinates d n) (blockCoordinates d n)
    (Matrix.fromBlocks (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (O j)))
      0 0 (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ))

/-- Full block spectral regularity in Lemma 3.4 / Lemma B.8. -/
theorem blockPrecision_regular {d n : ℕ} (hn : 3 ≤ n) (_hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (O : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) :
    (blockPrecision κ O).IsHermitian ∧
      ∀ x : Fin d → ℝ,
        x ⬝ᵥ x ≤ x ⬝ᵥ (blockPrecision κ O *ᵥ x) ∧
        x ⬝ᵥ (blockPrecision κ O *ᵥ x) ≤ κ * (x ⬝ᵥ x) := by
  let e := blockCoordinates d n
  let B := Matrix.fromBlocks (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (O j)))
    0 0 (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)
  have hB : B.IsHermitian := by
    apply Matrix.IsHermitian.fromBlocks
    · exact Matrix.isHermitian_blockDiagonal_iff.mpr
        (fun j => (singleBlockPrecision_regular hn hκ (O j)).1)
    · simp
    · exact Matrix.isHermitian_one
  constructor
  · exact hB.reindex e
  · intro x
    let y := x ∘ e
    let v := fun j i => y (Sum.inl (i, j))
    let z := y ∘ Sum.inr
    have hchange (M : Matrix ((Fin n × Fin (d / n)) ⊕ Fin (d % n))
        ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ℝ) :
        x ⬝ᵥ (Matrix.reindex e e M *ᵥ x) = y ⬝ᵥ (M *ᵥ y) := by
      change x ⬝ᵥ (M.submatrix e.symm e.symm *ᵥ x) = _
      rw [Matrix.submatrix_mulVec_equiv]
      exact dotProduct_comp_equiv_symm _ _ e
    have hvec (w : Fin n × Fin (d / n) → ℝ) (i : Fin n) (j : Fin (d / n)) :
        (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (O j)) *ᵥ w) (i, j) =
          (singleBlockPrecision κ (O j) *ᵥ (fun a => w (a, j))) i := by
      simp [Matrix.mulVec, dotProduct, Fintype.sum_prod_type, Matrix.blockDiagonal_apply,
        ite_mul]
    have hnorm : x ⬝ᵥ x = (∑ j, v j ⬝ᵥ v j) + z ⬝ᵥ z := by
      have h := e.sum_comp (fun i => x i * x i)
      change y ⬝ᵥ y = x ⬝ᵥ x at h
      rw [← h, Matrix.dotProduct_block]
      congr 1
      simp only [dotProduct, Fintype.sum_prod_type]
      exact Finset.sum_comm
    have hquad : x ⬝ᵥ (blockPrecision κ O *ᵥ x) =
        (∑ j, v j ⬝ᵥ (singleBlockPrecision κ (O j) *ᵥ v j)) + z ⬝ᵥ z := by
      change x ⬝ᵥ (Matrix.reindex e e B *ᵥ x) = _
      rw [hchange]
      simp only [B, Matrix.fromBlocks_mulVec, Matrix.zero_mulVec, Matrix.one_mulVec,
        add_zero, zero_add]
      rw [Matrix.dotProduct_block]
      congr 1
      simp only [dotProduct, Fintype.sum_prod_type, Function.comp_apply, Sum.elim_inl,
        hvec]
      exact Finset.sum_comm
    have hlo : (∑ j, v j ⬝ᵥ v j) ≤
        ∑ j, v j ⬝ᵥ (singleBlockPrecision κ (O j) *ᵥ v j) :=
      Finset.sum_le_sum (fun j _ => ((singleBlockPrecision_regular hn hκ (O j)).2 (v j)).1)
    have hupp : (∑ j, v j ⬝ᵥ (singleBlockPrecision κ (O j) *ᵥ v j)) ≤
        κ * (∑ j, v j ⬝ᵥ v j) := by
      rw [Finset.mul_sum]
      exact Finset.sum_le_sum (fun j _ =>
        ((singleBlockPrecision_regular hn hκ (O j)).2 (v j)).2)
    have hz : 0 ≤ z ⬝ᵥ z := Finset.sum_nonneg (fun i _ => mul_self_nonneg (z i))
    have htail : z ⬝ᵥ z ≤ κ * (z ⬝ᵥ z) := by
      simpa using mul_le_mul_of_nonneg_right (show (1 : ℝ) ≤ κ by linarith) hz
    rw [hnorm, hquad]
    constructor <;> nlinarith

/-- The actual quadratic potential has minimum zero only at the origin. -/
theorem blockPrecision_unique_minimizer {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (O : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) :
    let f : (Fin d → ℝ) → ℝ := fun x => (1 / 2 : ℝ) * (x ⬝ᵥ (blockPrecision κ O *ᵥ x))
    f 0 = 0 ∧ ∀ x, 0 ≤ f x ∧ (f x = 0 ↔ x = 0) := by
  dsimp
  constructor
  · simp
  intro x
  have hlow := ((blockPrecision_regular hn hnd hκ O).2 x).1
  have hnonneg : 0 ≤ x ⬝ᵥ x :=
    Finset.sum_nonneg (fun i _ => mul_self_nonneg (x i))
  constructor
  · nlinarith
  constructor
  · intro h
    have hzero : x ⬝ᵥ x = 0 := by nlinarith
    ext i
    change x i = 0
    have hi := Finset.single_le_sum (fun j (_ : j ∈ (Finset.univ : Finset (Fin d))) =>
      mul_self_nonneg (x j)) (Finset.mem_univ i)
    change x i * x i ≤ x ⬝ᵥ x at hi
    rw [hzero] at hi
    exact mul_self_eq_zero.mp (le_antisymm hi (mul_self_nonneg (x i)))
  · intro h
    subst x
    simp

end AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
