import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy
namespace Tests.GaussianCompactEntropy

/-- The zero-mass entropy case is admitted without a positivity hypothesis. -/
theorem zero_mass_entropy_limit :
    Tendsto (fun _ : ℕ => (0 : ℝ) - 0 * Real.log 0) atTop (𝓝 0) := by
  have h := compact_count_gaussian_entropy_limits (fun _ : ℝ => 0)
    contDiff_const (by simp [HasCompactSupport])
  simpa using h.2.2.2.2.2.2.2

/-- At N=0 the actual derivative observer is evaluated at the zero atom;
its value is not forced to vanish. The domain is supplied by the new producer. -/
theorem zero_count_derivative_domain_and_value (f : ℝ → ℝ)
    (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let μ : Measure (Fin 0 → Bool) :=
      (Fintype.card (Fin 0 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (Fin 0 → Bool) → ℝ := fun ε =>
      (Real.sqrt ((0 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 0, if ε j then (1 : ℝ) else -1
    Integrable (fun ε => (deriv f (S ε))^2) μ ∧
      (∫ ε, (deriv f (S ε))^2 ∂μ) = (deriv f 0)^2 := by
  have h := compact_count_gaussian_entropy_limits f hf hs
  refine ⟨(h.2.2.2.1 0).2.2, ?_⟩
  rcases AutoSamplingTheory.TechnicalLemmas.Probability.BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian
    with ⟨laws, hlaws, hzero, _⟩
  have hm : Measurable (fun ε : Fin 0 → Bool =>
      (Real.sqrt ((0 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 0, if ε j then (1 : ℝ) else -1) :=
    measurable_of_finite _
  have hd : Continuous (fun x => (deriv f x)^2) :=
    (hf.continuous_deriv (by norm_num)).pow 2
  have hI := integral_map_of_stronglyMeasurable (μ :=
      (Fintype.card (Fin 0 → Bool) : ℝ≥0∞)⁻¹ • Measure.count)
    hm hd.stronglyMeasurable
  rw [← hlaws 0, hzero] at hI
  simpa using hI.symm

#print axioms compact_count_gaussian_entropy_limits
#print axioms zero_mass_entropy_limit
#print axioms zero_count_derivative_domain_and_value

end Tests.GaussianCompactEntropy
