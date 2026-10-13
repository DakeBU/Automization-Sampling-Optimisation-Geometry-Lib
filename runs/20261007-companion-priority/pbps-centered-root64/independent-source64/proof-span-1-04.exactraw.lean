  have hOrder : (Γ-γ • Q).IsPositive :=
    AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order
      ν (γ • Q) Γ (hQpos.smul_of_nonneg hγ.le) hΓ hSquare
