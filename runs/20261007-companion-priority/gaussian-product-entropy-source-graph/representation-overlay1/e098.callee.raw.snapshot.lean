lemma integralYLogT_of_pos_on_Y (Y T : Ω → ℝ)
    (hT_pos_on_Y : ∀ᵐ ω ∂μ, 0 < Y ω → 0 < T ω) :
    integralYLogT μ Y T =
      ((∫ ω, Y ω * (Real.log (T ω) - Real.log (∫ ω', T ω' ∂μ)) ∂μ) : ℝ) := by
  simp only [integralYLogT, if_pos hT_pos_on_Y]
