import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
import Mathlib.Tactic.NormNum

open Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/- The identity and negative identity attain opposite spectral endpoints.
These checks distinguish O(n) from SO(n) and exercise the source n=3, κ=4 endpoint. -/
example (v : Fin 3 → ℝ) :
    v ⬝ᵥ v ≤ v ⬝ᵥ (singleBlockPrecision 4 (1 : orthogonalGroup (Fin 3) ℝ) *ᵥ v) ∧
    v ⬝ᵥ (singleBlockPrecision 4 (1 : orthogonalGroup (Fin 3) ℝ) *ᵥ v) ≤
      4 * (v ⬝ᵥ v) :=
  (singleBlockPrecision_regular (by decide) (by norm_num) 1).2 v

example : singleBlockPrecision 4 (1 : orthogonalGroup (Fin 3) ℝ) = 1 := by
  ext i j
  simp [singleBlockPrecision, Matrix.smul_apply, Matrix.one_apply]
  split <;> norm_num

example : singleBlockPrecision 4 (-1 : orthogonalGroup (Fin 3) ℝ) =
    (4 : ℝ) • (1 : Matrix (Fin 3) (Fin 3) ℝ) := by
  ext i j
  simp [singleBlockPrecision, Unitary.coe_neg, Matrix.smul_apply, Matrix.one_apply]
  split <;> norm_num

#print axioms singleBlockPrecision_regular
