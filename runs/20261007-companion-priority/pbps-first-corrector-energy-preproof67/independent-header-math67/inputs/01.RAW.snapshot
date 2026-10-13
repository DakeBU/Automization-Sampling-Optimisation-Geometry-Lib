theorem positive_square_commutation
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (G D : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hG : G.IsPositive) (hD : D.IsPositive)
    (hCommute : Commute (G*G) D) : Commute G D
