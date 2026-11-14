import Mathlib
noncomputable section
open MeasureTheory
open scoped Matrix.Norms.L2Operator MatrixOrder

-- Post-admission R9 consumer API inspection; no new shared PSD-integral proof.
#check norm_cfc_le
#check cfc_id
#check cfc_le_algebraMap_iff
#check cfc_nonneg_iff
#check Matrix.nonneg_iff_posSemidef
#check Matrix.IsHermitian.isSelfAdjoint
#check integral_const_mul_of_integrable
#check integral_mul_const_of_integrable
#check Integrable.const_mul
#check Integrable.mul_const
#check Matrix.IsHermitian.sub
#check Matrix.posSemidef_conjTranspose_mul_self
#check integral_star

section
variable {n : Type*} [Fintype n] [DecidableEq n]
#synth IsometricContinuousFunctionalCalculus ℝ (Matrix n n ℝ) IsSelfAdjoint
#synth NonnegSpectrumClass ℝ (Matrix n n ℝ)
#synth StarOrderedRing (Matrix n n ℝ)
end
