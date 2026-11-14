import Mathlib
set_option autoImplicit false
open scoped Matrix.Norms.L2Operator
universe u
#check @NormedSpace.exp
#check @Matrix.PosSemidef
section
variable {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
#synth Algebra ℚ (Matrix ι ι ℝ)
#synth NormedRing (Matrix ι ι ℝ)
#synth CompleteSpace (Matrix ι ι ℝ)
end
