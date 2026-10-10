theorem variance_eq_sub [IsProbabilityMeasure μ] {X : Ω → ℝ} (hX : MemLp X 2 μ) :
    variance X μ = μ[X ^ 2] - μ[X] ^ 2 := by
  rw [← covariance_self hX.aemeasurable, covariance_eq_sub hX hX, pow_two, pow_two]
