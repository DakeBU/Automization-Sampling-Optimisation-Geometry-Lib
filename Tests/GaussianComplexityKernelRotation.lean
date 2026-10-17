import AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelRotation

private def swapFirstTwo : Matrix.orthogonalGroup (Fin 3) ℝ :=
  ⟨!![0, 1, 0; 1, 0, 0; 0, 0, 1], by
    apply (Matrix.mem_orthogonalGroup_iff (Fin 3) ℝ).2
    ext i j
    fin_cases i <;> fin_cases j <;>
      norm_num [Matrix.mul_apply, Fin.sum_univ_succ]⟩

example : (swapFirstTwo : Matrix (Fin 3) (Fin 3) ℝ).det = -1 := by
  norm_num [swapFirstTwo, Matrix.det_fin_three, Matrix.cons_val_two]

-- A determinant-minus-one coordinate swap, rather than a special-orthogonal restriction.
example :
    let p : Matrix.orthogonalGroup (Fin 3) ℝ → (Fin 3 → ℝ) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision 4 O).det /
        (2 * Real.pi) ^ (3 / 2 : ℝ) *
          Real.exp (-(x ⬝ᵥ (singleBlockPrecision 4 O *ᵥ x)) / 2)
    Integrable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * p O ![1, 2, 3]) (orthogonalHaar 3) ∧
    (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * p O ![2, 1, 3] ∂orthogonalHaar 3) =
    (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * p O ![1, 2, 3] ∂orthogonalHaar 3) := by
  have hv : (swapFirstTwo : Matrix (Fin 3) (Fin 3) ℝ) *ᵥ ![1, 2, 3] = ![2, 1, 3] := by
    ext i
    fin_cases i <;> norm_num [swapFirstTwo, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  have h := signed_kernel_rotation_invariant (n := 3) (by decide) (κ := 4) (by norm_num)
  exact ⟨h.1 _, by simpa only [hv, Nat.cast_ofNat] using h.2 swapFirstTwo ![1, 2, 3]⟩

-- The zero vector is in the domain; L1 is a proved output, not a caller premise.
example :
    Integrable (fun O : Matrix.orthogonalGroup (Fin 4) ℝ =>
      (O : Matrix (Fin 4) (Fin 4) ℝ).det *
        (Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (2 : ℝ)))
      (orthogonalHaar 4) := by
  have h := (signed_kernel_rotation_invariant (n := 4) (by decide) (κ := 4) (by norm_num)).1 0
  norm_num only [Matrix.mulVec_zero, dotProduct_zero, neg_zero, zero_div, Real.exp_zero,
    mul_one, Nat.cast_ofNat, show (4 : ℝ) / 2 = 2 by norm_num] at h
  exact h

#print axioms signed_kernel_rotation_invariant
