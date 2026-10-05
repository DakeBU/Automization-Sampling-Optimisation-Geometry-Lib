import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Tactic
open scoped InnerProductSpace
noncomputable section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
-- Select the existing operator-norm structures before elaborating nested CLM types.
local instance : NormedAddCommGroup (E →L[ℝ] ℝ) := ContinuousLinearMap.toNormedAddCommGroup
local instance : NormedSpace ℝ (E →L[ℝ] ℝ) := ContinuousLinearMap.toNormedSpace
#synth NormedSpace ℝ (E →L[ℝ] (E →L[ℝ] ℝ))
#synth NormSMulClass ℝ (E →L[ℝ] (E →L[ℝ] ℝ))
#synth TopologicalSpace.PseudoMetrizableSpace (E →L[ℝ] (E →L[ℝ] ℝ))
example (a : ℝ) (L : E →L[ℝ] (E →L[ℝ] ℝ)) : ‖a • L‖ = ‖a‖ * ‖L‖ := by exact norm_smul a L
example (L T : E →L[ℝ] (E →L[ℝ] ℝ)) : ‖L + T‖ ≤ ‖L‖ + ‖T‖ := by exact norm_add_le L T
example (L : E →L[ℝ] ℝ) : ‖L‖ = @Norm.norm _ (ContinuousLinearMap.hasOpNorm) L := rfl
example (y : E) : HasFDerivAt (fun z : E => innerSL ℝ z) (innerSL ℝ) y := (innerSL ℝ).hasFDerivAt
example (L : E →L[ℝ] (E →L[ℝ] ℝ)) (v : E) : ‖L v‖ ≤ ‖L‖ * ‖v‖ := L.le_opNorm v
example : ‖(innerSL ℝ : E →L[ℝ] (E →L[ℝ] ℝ))‖ ≤ 1 := norm_innerSL_le ℝ

