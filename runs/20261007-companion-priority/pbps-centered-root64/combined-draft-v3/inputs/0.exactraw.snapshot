theorem positive_square_order
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (A B : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ)
    (hA : A.IsPositive) (hB : B.IsPositive)
    (hSquareOrder : (B*B-A*A).IsPositive) :
    (B-A).IsPositive
