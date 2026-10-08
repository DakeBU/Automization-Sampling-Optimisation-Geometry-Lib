theorem exists_positive_complex_lift
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ) (hD : D.IsPositive) :
    let ι : Lp ℝ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.ofRealCLM.compLpL 2 μ
    let R : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.reCLM.compLpL 2 μ
    let Q : Lp ℂ 2 μ →L[ℝ] Lp ℝ 2 μ := Complex.imCLM.compLpL 2 μ
    let C : Lp ℂ 2 μ →L[ℝ] Lp ℂ 2 μ := Complex.conjCLE.toContinuousLinearMap.compLpL 2 μ
    (∀ u : Lp ℝ 2 μ, ‖ι u‖ = ‖u‖) ∧
    (∀ g : Lp ℂ 2 μ, C g = g ↔ ∃ u : Lp ℝ 2 μ, ι u = g) ∧
    ∃ Dc : Lp ℂ 2 μ →L[ℂ] Lp ℂ 2 μ,
      Dc.IsPositive ∧
      (∀ g : Lp ℂ 2 μ, Dc g = ι (D (R g)) + Complex.I • ι (D (Q g))) ∧
      (∀ u : Lp ℝ 2 μ, Dc (ι u) = ι (D u)) ∧
      (∀ g : Lp ℂ 2 μ, C (Dc g) = Dc (C g))
