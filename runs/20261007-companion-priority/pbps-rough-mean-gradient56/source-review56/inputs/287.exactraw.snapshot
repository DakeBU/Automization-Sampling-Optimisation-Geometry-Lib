
variable {E : Type*} [MeasurableSpace E] [NormedAddCommGroup E]
  [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Variance written as the integral of the squared centered observable.

Admissibility is deliberately separate because the Bochner integral is
totalized outside its integrable domain. -/
noncomputable def variance (μ : Measure E) (f : E → ℝ) : ℝ :=
  ∫ x, (f x - ∫ y, f y ∂μ) ^ 2 ∂μ
