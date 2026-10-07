theorem compact_gaussian_logSobolev
    (f : ℝ → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure ℝ := gaussianReal 0 1
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
    2 * ∫ x, (deriv f x)^2 ∂γ := by
  dsimp only
  let μ : (n : ℕ) → Measure (Fin n → Bool) := fun n =>
    (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count
  let S : (n : ℕ) → (Fin n → Bool) → ℝ := fun n ε =>
    (Real.sqrt (n : ℝ))⁻¹ * ∑ j : Fin n, if ε j then (1 : ℝ) else -1
  rcases GaussianCompactEntropy.compact_count_gaussian_entropy_limits f hf hs
    with ⟨_, _, _, _, _, _, _, tEnt⟩
  rcases GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit f hf hs
    with ⟨_, _, tEnergy⟩
  change Tendsto (fun n : ℕ =>
    (∫ ε, (f (S (n+1) ε))^2 * Real.log ((f (S (n+1) ε))^2) ∂μ (n+1)) -
      (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1)) *
        Real.log (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1))) atTop
    (𝓝 ((∫ x, (f x)^2 * Real.log ((f x)^2) ∂gaussianReal 0 1) -
      (∫ x, (f x)^2 ∂gaussianReal 0 1) *
        Real.log (∫ x, (f x)^2 ∂gaussianReal 0 1))) at tEnt
  change Tendsto (fun n : ℕ => ∫ ε : Fin (n+1) → Bool,
    (∑ j : Fin (n+1),
      (f (S (n+1) (Function.update ε j (!ε j))) - f (S (n+1) ε))^2)
      ∂μ (n+1)) atTop (𝓝 (4 * ∫ x, (deriv f x)^2 ∂gaussianReal 0 1)) at tEnergy
  have tHalf : Tendsto (fun n : ℕ => (1/2 : ℝ) *
      ∫ ε : Fin (n+1) → Bool, (∑ j : Fin (n+1),
        (f (S (n+1) (Function.update ε j (!ε j))) - f (S (n+1) ε))^2)
        ∂μ (n+1)) atTop (𝓝 (2 * ∫ x, (deriv f x)^2 ∂gaussianReal 0 1)) := by
    have heq : (1/2 : ℝ) * (4 * ∫ x, (deriv f x)^2 ∂gaussianReal 0 1) =
        2 * ∫ x, (deriv f x)^2 ∂gaussianReal 0 1 := by ring
    simpa only [heq] using tEnergy.const_mul (1/2 : ℝ)
  apply le_of_tendsto_of_tendsto tEnt tHalf
  exact Eventually.of_forall fun n => by
    have hn := (BernoulliLogSobolev.bernoulli_function_logSobolev (n+1)
      (fun ε => f (S (n+1) ε))).2.2.2.2
    change ((∫ ε, (f (S (n+1) ε))^2 * Real.log ((f (S (n+1) ε))^2) ∂μ (n+1)) -
      (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1)) *
        Real.log (∫ ε, (f (S (n+1) ε))^2 ∂μ (n+1))) ≤
      (1/2 : ℝ) * ∫ ε : Fin (n+1) → Bool, (∑ j : Fin (n+1),
        (f (S (n+1) ε) - f (S (n+1) (Function.update ε j (!ε j))))^2)
        ∂μ (n+1) at hn
    simpa only [sub_sq_comm] using hn

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev