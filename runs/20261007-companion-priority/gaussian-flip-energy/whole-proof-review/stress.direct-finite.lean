import Tests.GaussianCompactEntropy
import Tests.GaussianFlipEnergy
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
namespace IndependentGaussianFlipEnergyStress

def probe (x : ℝ) : ℝ := x * smoothUnitCutoff x

theorem probe_C2 : ContDiff ℝ 2 probe := by
  exact contDiff_id.mul (smoothUnitCutoff_contDiff.of_le
    (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤)))

theorem probe_compact : HasCompactSupport probe :=
  smoothUnitCutoff_hasCompactSupport.mul_left

theorem probe_derivative_zero : deriv probe 0 = 1 := by
  have hc : ContDiff ℝ 2 smoothUnitCutoff := smoothUnitCutoff_contDiff.of_le
    (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
  change deriv (fun x : ℝ => x * smoothUnitCutoff x) 0 = 1
  rw [deriv_fun_mul (c := fun x : ℝ => x) (d := smoothUnitCutoff) (x := 0)
    differentiableAt_id (hc.differentiable (by norm_num)).differentiableAt]
  simp [smoothUnitCutoff_eq_one_of_abs_le_one (show |(0 : ℝ)| ≤ 1 by norm_num)]

/-- Actual N0 energy is one even though the actual normalized sign sum is zero. -/
theorem actual_nonzero_N0_energy :
    let μ : Measure (Fin 0 → Bool) :=
      (Fintype.card (Fin 0 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (Fin 0 → Bool) → ℝ := fun ε =>
      (Real.sqrt ((0 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 0, if ε j then (1 : ℝ) else -1
    Integrable (fun ε => (deriv probe (S ε))^2) μ ∧
      (∫ ε, (deriv probe (S ε))^2 ∂μ) = 1 := by
  have h := Tests.GaussianCompactEntropy.zero_count_derivative_domain_and_value
    probe probe_C2 probe_compact
  simpa only [probe_derivative_zero, one_pow] using h


/-- Same signed compact probe: no coordinates at N0, and full N1 flip average4. -/
theorem actual_full_N0_flip_zero :
    let μ : Measure (Fin 0 → Bool) :=
      (Fintype.card (Fin 0 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (Fin 0 → Bool) → ℝ := fun ε =>
      (Real.sqrt ((0 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 0, if ε j then (1 : ℝ) else -1
    Integrable (fun ε => ∑ j : Fin 0,
      (probe (S (Function.update ε j (!ε j))) - probe (S ε))^2) μ ∧
    (∫ ε, (∑ j : Fin 0,
      (probe (S (Function.update ε j (!ε j))) - probe (S ε))^2) ∂μ) = 0 :=
  Tests.GaussianFlipEnergy.zero_count_flip_domain_and_value probe probe_C2 probe_compact

theorem actual_full_N1_flip_average :
    let μ : Measure (Fin 1 → Bool) :=
      (Fintype.card (Fin 1 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let S : (Fin 1 → Bool) → ℝ := fun ε =>
      (Real.sqrt ((1 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 1, if ε j then (1 : ℝ) else -1
    Integrable (fun ε => ∑ j : Fin 1,
      (probe (S (Function.update ε j (!ε j))) - probe (S ε))^2) μ ∧
    (∫ ε, (∑ j : Fin 1,
      (probe (S (Function.update ε j (!ε j))) - probe (S ε))^2) ∂μ) = 4 := by
  dsimp
  let μ : Measure (Fin 1 → Bool) :=
    (Fintype.card (Fin 1 → Bool) : ℝ≥0∞)⁻¹ • Measure.count
  let S : (Fin 1 → Bool) → ℝ := fun ε =>
    (Real.sqrt ((1 : ℕ) : ℝ))⁻¹ * ∑ j : Fin 1, if ε j then (1 : ℝ) else -1
  haveI : IsProbabilityMeasure μ := by
    constructor
    change (((Fintype.card (Fin 1 → Bool) : ℝ≥0∞)⁻¹ • Measure.count) Set.univ) = 1
    rw [Measure.smul_apply, smul_eq_mul]
    rw [Measure.count_apply_finite Set.univ Set.finite_univ]
    simp only [Set.Finite.toFinset_univ, Finset.card_univ]
    exact ENNReal.inv_mul_cancel (by exact_mod_cast Fintype.card_ne_zero) (by simp)
  have hp := AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit probe probe_C2 probe_compact
  refine ⟨hp.2.1 1, ?_⟩
  change (∫ ε : Fin 1 → Bool, (∑ j : Fin 1,
    (probe (S (Function.update ε j (!ε j))) - probe (S ε))^2) ∂μ) = 4
  apply integral_eq_const
  apply Filter.Eventually.of_forall
  intro ε
  cases hε : ε 0 <;>
    norm_num [S, probe, Fin.sum_univ_one, Function.update_self, hε,
      smoothUnitCutoff_eq_one_of_abs_le_one (show |(1 : ℝ)| ≤ 1 by norm_num),
      smoothUnitCutoff_eq_one_of_abs_le_one (show |(-1 : ℝ)| ≤ 1 by norm_num)]


#print axioms actual_nonzero_N0_energy
#print axioms actual_full_N0_flip_zero
#print axioms actual_full_N1_flip_average
end IndependentGaussianFlipEnergyStress
