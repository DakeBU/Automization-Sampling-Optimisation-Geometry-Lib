import AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation
import Mathlib.Tactic.NormNum.RealSqrt

/-! Direct consumers at the source boundary and a non-boundary condition number.
These exercise the literal scalar ratio; no actual TV input is assumed. -/
set_option autoImplicit false
open AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation

example : (1 / 2 : ℝ) * Real.exp (-(15 : ℝ) / 2) ≤ 1 / 126 := by
  have h := explicit_ratio_ge_exponential (n := 3) (κ := 4) (by norm_num) (by norm_num)
  norm_num at h ⊢
  exact h

example : (1 / 2 : ℝ) * Real.exp (-(20 : ℝ) / 3) ≤ 1 / 80 := by
  have h := explicit_ratio_ge_exponential (n := 4) (κ := 9) (by norm_num) (by norm_num)
  norm_num at h ⊢
  exact h

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation.explicit_ratio_ge_exponential
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.NumericSeparation.explicit_ratio_ge_exponential | throwError "Target missing"
  let some body := info.value? (allowOpaque := true) | throwError "Body missing"
  let parents := body.getUsedConstants.filter fun n =>
    n.toString.startsWith "Real.log" || n.toString.startsWith "Real.exp" ||
    n.toString.startsWith "Real.add_one_le_exp" || n.toString.startsWith "div_le_div" ||
    n.toString.startsWith "pow_le_pow"
  logInfo m!"ACTUAL COMPILED PARENTS {parents}"
