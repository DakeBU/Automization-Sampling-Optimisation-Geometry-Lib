
@[expose] public section

open MeasureTheory Set Filter MeasurableSpace ProbabilityTheory
open scoped ENNReal MeasureTheory Topology

variable {α β Ω : Type*} {mα : MeasurableSpace α} {mβ : MeasurableSpace β} {mΩ : MeasurableSpace Ω}

/-!
### Disintegration of measures

This section provides a predicate for a kernel to disintegrate a measure.
-/

namespace MeasureTheory.Measure
variable (ρ : Measure (α × Ω)) (ρCond : Kernel α Ω)

/-- A kernel `ρCond` is a conditional kernel for a measure `ρ` if it disintegrates it in the sense
that `ρ.fst ⊗ₘ ρCond = ρ`. -/
class IsCondKernel : Prop where
  disintegrate : ρ.fst ⊗ₘ ρCond = ρ
