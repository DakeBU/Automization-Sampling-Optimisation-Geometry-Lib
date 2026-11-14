import Mathlib
noncomputable section
open MeasureTheory
open scoped Matrix.Norms.L2Operator
set_option autoImplicit false

def producerProp    {n Ω : Type*} [Fintype n] [DecidableEq n] [MeasurableSpace Ω]
    {μ : Measure Ω} [IsProbabilityMeasure μ]
    (f : Ω → Matrix n n ℝ) (hf : Integrable f μ)
    (hpos : ∀ᵐ ω ∂μ, Matrix.PosSemidef (f ω)) : Prop :=
    Matrix.PosSemidef (∫ ω, f ω ∂μ)

#print producerProp

section
variable {n Ω : Type*} [Fintype n] [DecidableEq n] [MeasurableSpace Ω]
variable {μ : Measure Ω} [IsProbabilityMeasure μ]
#synth NormedRing (Matrix n n ℝ)
#synth NormedSpace ℝ (Matrix n n ℝ)
#synth CompleteSpace (Matrix n n ℝ)
end
