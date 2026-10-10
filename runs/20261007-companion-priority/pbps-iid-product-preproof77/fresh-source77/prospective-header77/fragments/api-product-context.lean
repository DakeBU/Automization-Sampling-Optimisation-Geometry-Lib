namespace MeasureTheory

section Preliminaries

variable {ι : Type*} {X : ι → Type*} {mX : ∀ i, MeasurableSpace (X i)}
variable (μ : (i : ι) → Measure (X i)) [hμ : ∀ i, IsProbabilityMeasure (μ i)]
