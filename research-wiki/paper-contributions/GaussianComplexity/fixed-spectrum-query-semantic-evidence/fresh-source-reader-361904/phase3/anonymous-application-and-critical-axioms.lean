import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine
import Lean.Util.FoldConsts
open Matrix
set_option autoImplicit false
example :
∀ {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ),
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let query : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun η x => WithLp.toLp 2 (A η *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      query κ x = (κ - 1) • query 2 x - (κ - 2) • x ∧
      query 2 x = (κ - 1)⁻¹ • (query κ x + (κ - 2) • x)
 := by
  exact @AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query

#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query
#print Matrix.mem_orthogonalGroup_iff
#print Matrix.mem_orthogonalGroup_iff'
#print WithLp.ofLp_injective
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine.actual_affine_precision_query | throwError "Missing producer"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing proof"
  logInfo m!"PRODUCER TYPE {info.type}"
  let used := proof.getUsedConstants
  let parents := used.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL ASTIS PARENTS {parents}"
  logInfo m!"ACTUAL ALL USED CONSTANTS {used}"
  if used.any (fun n => n == `sorryAx) then throwError "sorryAx used"
  if !parents.isEmpty then throwError "Unexpected ASTIS parents"
