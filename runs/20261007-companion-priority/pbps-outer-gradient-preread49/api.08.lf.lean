theorem evariance_eq_lintegral_ofReal :
    evariance X μ = ∫⁻ ω, ENNReal.ofReal ((X ω - μ[X]) ^ 2) ∂μ := by
  simp [evariance, ← enorm_pow, Real.enorm_of_nonneg (sq_nonneg _)]

lemma variance_eq_integral (hX : AEMeasurable X μ) : Var[X; μ] = ∫ ω, (X ω - μ[X]) ^ 2 ∂μ := by
  simp [variance, evariance, toReal_enorm, ← integral_toReal ((hX.sub_const _).enorm.pow_const _) <|
