import AutoSamplingTheory.ExampleCases.GaussianComplexity.BlockFamily
import Mathlib.Tactic.NormNum

open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

private noncomputable def mixedBlocks : Fin 2 → orthogonalGroup (Fin 3) ℝ :=
  fun j => if j = 0 then 1 else -1

/- These entry tests distinguish consecutive blocks from an interleaved coordinate
permutation. The last coordinate tests the residual identity block. -/
example : blockPrecision (d := 7) (n := 3) 4 mixedBlocks 0 0 = 1 := by
  change singleBlockPrecision 4 (1 : orthogonalGroup (Fin 3) ℝ) 0 0 = 1
  norm_num [singleBlockPrecision, Matrix.add_apply, Matrix.smul_apply, Matrix.one_apply,
    Matrix.transpose_apply, Matrix.sub_apply, Matrix.ofNat_apply]

example : blockPrecision (d := 7) (n := 3) 4 mixedBlocks 3 3 = 4 := by
  change singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 3) ℝ) 0 0 = 4
  norm_num [singleBlockPrecision, Unitary.coe_neg, Matrix.add_apply, Matrix.smul_apply,
    Matrix.one_apply, Matrix.transpose_apply, Matrix.sub_apply, Matrix.ofNat_apply]

example : blockPrecision (d := 7) (n := 3) 4 mixedBlocks 6 6 = 1 := by
  change (1 : Matrix (Fin 1) (Fin 1) ℝ) 0 0 = 1
  simp

example : blockPrecision (d := 7) (n := 3) 4 mixedBlocks 2 3 = 0 := by
  change (0 : ℝ) = 0
  rfl

/- The endpoint d=k*n has no residual coordinates. -/
example : blockPrecision (d := 6) (n := 3) 4 mixedBlocks 5 5 = 4 := by
  change singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 3) ℝ) 2 2 = 4
  norm_num [singleBlockPrecision, Unitary.coe_neg, Matrix.add_apply, Matrix.smul_apply,
    Matrix.one_apply, Matrix.transpose_apply, Matrix.sub_apply, Matrix.ofNat_apply]

example (x : Fin 7 → ℝ) :
    x ⬝ᵥ x ≤ x ⬝ᵥ (blockPrecision (n := 3) 4 mixedBlocks *ᵥ x) ∧
      x ⬝ᵥ (blockPrecision (n := 3) 4 mixedBlocks *ᵥ x) ≤ 4 * (x ⬝ᵥ x) :=
  (blockPrecision_regular (d := 7) (n := 3) (by decide) (by decide)
    (by norm_num) mixedBlocks).2 x

example (x : Fin 6 → ℝ) :
    (1 / 2 : ℝ) * (x ⬝ᵥ (blockPrecision (n := 3) 4 mixedBlocks *ᵥ x)) = 0 ↔ x = 0 :=
  ((blockPrecision_unique_minimizer (d := 6) (n := 3) (by decide) (by decide)
    (by norm_num) mixedBlocks).2 x).2

#print axioms blockPrecision_regular
#print axioms blockPrecision_unique_minimizer
