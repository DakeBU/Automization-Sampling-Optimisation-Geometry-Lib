theorem exists_positive_real_square_root
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    ∃ Γ : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ,
      Γ.IsPositive ∧ Γ*Γ = D ∧
      ∀ u : Lp ℝ 2 μ, ‖Γ u‖^2 = inner ℝ (D u) u
