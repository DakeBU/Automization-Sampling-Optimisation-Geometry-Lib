import AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt
import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation
import Mathlib.Tactic.NormNum.RealSqrt

set_option autoImplicit false
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/-! Exact source-boundary and internal parameter instances plus an actual
Gaussian-integrability consumer at the selected positive tilt. -/
example : (0 : ℝ) < 25 / 48 := by
  have h := (selected_tilt (n := 3) (κ := 4) (by norm_num) (by norm_num)).2.2.1
  convert h using 1 <;> norm_num

example (u : ℝ) : (9 : ℝ) + 1 + 4 * (13 / 24) - (9 - 1) * u =
    (32 / 3) * (1 + (3 / 8) ^ 2 - 2 * (3 / 8) * u) := by
  have h := ((selected_tilt (n := 4) (κ := 9) (by norm_num) (by norm_num)).2.2.2.2.2 u).1
  norm_num at h ⊢
  exact h

example {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin n) ℝ) :
    let ℓ : ℝ := (4 * (n : ℝ) * Real.sqrt κ + (Real.sqrt κ - 1) ^ 2) /
      (8 * (n : ℝ) * ((n : ℝ) - 1))
    Integrable (fun x : EuclideanSpace ℝ (Fin n) => Real.exp (-ℓ * ‖x‖ ^ 2))
      (multivariateGaussian (0 : EuclideanSpace ℝ (Fin n)) (singleBlockPrecision κ O)⁻¹) := by
  have hℓ := (selected_tilt hn hκ).2.2.1
  exact ((AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation.actual_gaussian_transform
    hn hκ (le_of_lt hℓ)).1 O).1

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt.selected_tilt
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.SelectedTilt.selected_tilt | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun n =>
    n.toString.startsWith "Real." || n.toString.startsWith "div_" ||
    n.toString.startsWith "mul_pos" || n.toString.startsWith "one_div"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
