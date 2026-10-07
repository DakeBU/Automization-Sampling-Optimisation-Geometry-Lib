import Tests.GaussianCompactEntropy
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff

noncomputable section
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal BigOperators Topology
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
namespace IndependentGaussianCompactEntropyStress

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

#print axioms actual_nonzero_N0_energy
end IndependentGaussianCompactEntropyStress
