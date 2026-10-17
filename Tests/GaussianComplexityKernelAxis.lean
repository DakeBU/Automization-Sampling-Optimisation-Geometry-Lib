import AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic.NormNum

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.KernelAxis

-- This vector distinguishes the Euclidean square norm 9 from the sup-norm square 4.
private def v : EuclideanSpace ℝ (Fin 3) := WithLp.toLp 2 ![1, 2, 2]

example : ‖v‖ ^ 2 = (9 : ℝ) := by
  rw [EuclideanSpace.real_norm_sq_eq]
  norm_num [v, Fin.sum_univ_succ]

example :
    let p : Matrix.orthogonalGroup (Fin 3) ℝ → ℝ := fun O =>
      Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (3 / 2 : ℝ) *
        Real.exp (-(![1, 2, 2] ⬝ᵥ (singleBlockPrecision 4 O *ᵥ ![1, 2, 2])) / 2)
    let r : Matrix.orthogonalGroup (Fin 3) ℝ → ℝ := fun O =>
      Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (3 / 2 : ℝ) *
        Real.exp (-(5 - 3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0) * 9 / 4)
    Integrable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * p O) (orthogonalHaar 3) ∧
    Integrable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * r O) (orthogonalHaar 3) ∧
    (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * p O ∂orthogonalHaar 3) =
    (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * r O ∂orthogonalHaar 3) := by
  have hv : ‖v‖ ^ 2 = (9 : ℝ) := by
    rw [EuclideanSpace.real_norm_sq_eq]
    norm_num [v, Fin.sum_univ_succ]
  have h := signed_kernel_radial (n := 3) (by decide) (κ := 4) (by norm_num) v
  norm_num only [Nat.cast_ofNat, show (4 : ℝ) + 1 = 5 by norm_num,
    show (4 : ℝ) - 1 = 3 by norm_num, hv] at h
  exact h

-- The zero/equal-vector geometry has no division by the norm and preserves genuine L1.
example :
    Integrable (fun O : Matrix.orthogonalGroup (Fin 4) ℝ =>
      (O : Matrix (Fin 4) (Fin 4) ℝ).det *
        (Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (2 : ℝ)))
      (orthogonalHaar 4) := by
  have h := (signed_kernel_radial (n := 4) (by decide) (κ := 4) (by norm_num) 0).2.1
  norm_num only [norm_zero, zero_pow (by decide : 2 ≠ 0), mul_zero, zero_div,
    Real.exp_zero, mul_one, Nat.cast_ofNat, show (4 : ℝ) / 2 = 2 by norm_num] at h
  exact h

#print axioms signed_kernel_radial
