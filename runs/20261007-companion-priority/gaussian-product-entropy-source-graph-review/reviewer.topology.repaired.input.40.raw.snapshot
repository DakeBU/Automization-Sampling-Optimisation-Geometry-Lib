theorem entropy_ge_integral_log [IsProbabilityMeasure μ]
    (Y : Ω → ℝ) (hY_meas : Measurable Y)
    (hY_nn : 0 ≤ᵐ[μ] Y)
    (hY_int : Integrable Y μ)
    (hY_log_int : Integrable (fun ω => Y ω * Real.log (Y ω)) μ)
    (T : Ω → ℝ) (hT_meas : Measurable T)
    (hT_nn : 0 ≤ᵐ[μ] T)
    (hT_int : Integrable T μ)
    (hT_mean_pos : 0 < ∫ ω, T ω ∂μ) :
    integralYLogT μ Y T ≤ (entropy μ Y : EReal) :=
  dualEntropySetT_le_entropy Y hY_meas hY_nn hY_int hY_log_int
    (integralYLogT μ Y T) ⟨T, hT_meas, hT_nn, hT_int, hT_mean_pos, rfl⟩
