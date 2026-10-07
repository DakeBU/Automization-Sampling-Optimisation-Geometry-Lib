import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy
namespace Tests.GaussianFlipEnergy

/-- The full flip energy is zero at N=0, even when the derivative observer
at the zero atom is nonzero. Its genuine L1 domain comes from the producer. -/
theorem zero_count_flip_domain_and_value (f : ℝ → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : Measure (Fin 0 → Bool) :=
      (Fintype.card (Fin 0 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (Fin 0 → Bool) → ℝ := fun ε =>
      (Real.sqrt ((0 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 0, if ε j then (1 : ℝ) else -1
    Integrable (fun ε => ∑ j : Fin 0,
      (f (S (Function.update ε j (!ε j))) - f (S ε))^2) μ ∧
      (∫ ε, (∑ j : Fin 0,
        (f (S (Function.update ε j (!ε j))) - f (S ε))^2) ∂μ) = 0 := by
  have h := compact_count_gaussian_flip_energy_limit f hf hs
  exact ⟨h.2.1 0, by simp⟩

/-- At N=1 either Boolean state gives the full squared difference between
the actual two normalized-sum atoms, without an accidental factor one-half. -/
theorem one_count_full_flip_energy (f : ℝ → ℝ) (ε : Fin 1 → Bool) :
    let S : (Fin 1 → Bool) → ℝ := fun η =>
      (Real.sqrt ((1 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 1, if η j then (1 : ℝ) else -1
    (∑ j : Fin 1,
      (f (S (Function.update ε j (!ε j))) - f (S ε))^2) =
      (f 1 - f (-1))^2 := by
  dsimp
  simp only [Nat.cast_one, Real.sqrt_one, inv_one, one_mul, Fin.sum_univ_one,
    Function.update_self]
  cases ε 0 <;> simp <;> ring

#print axioms compact_count_gaussian_flip_energy_limit
#print axioms zero_count_flip_domain_and_value
#print axioms one_count_full_flip_energy

end Tests.GaussianFlipEnergy
