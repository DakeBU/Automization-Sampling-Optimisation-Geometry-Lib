import GC43Representation
import GC41Minimax

/-! Theorem 4.1 of Zhou and Suzuki, including sampling with a disclosed spectrum. -/
noncomputable section
open MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
universe u v

/-- Uniform in dimension, condition number and total-variation error. Each
algorithm may be selected after learning every eigenvalue with multiplicity. -/
theorem gaussian_query_lower_bound_with_disclosed_spectrum
    {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ ε : ℝ, 0 < ε → ε ≤ 1/10 →
      ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤ disclosedQueryComplexity.{u,v} d κ ε ∧
      ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤ gaussianQueryComplexity.{u,v} d κ ε := by
  refine query_complexities_from_representation ?_ hδ hδ'
  intro d q κ _ hn Seed State _ _ ρ _ alg
  exact actual_output_representation κ hn.le ρ alg

/-- Source statement for the finite, real-valued minimax query complexities,
with and without disclosure. Both are finite by the exact column-query sampler. -/
theorem gaussian_query_lower_bound_real {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ ε : ℝ, 0 < ε → ε ≤ 1/10 →
      δ/256 * Real.sqrt κ * Real.log (d : ℝ) ≤ (disclosedQueryComplexity.{0,0} d κ ε).toReal ∧
      δ/256 * Real.sqrt κ * Real.log (d : ℝ) ≤ (gaussianQueryComplexity.{0,0} d κ ε).toReal := by
  obtain ⟨D,hD⟩ := gaussian_query_lower_bound_with_disclosed_spectrum.{0,0} hδ hδ'
  exact ⟨D,fun d hd κ hk hcap ε he he' => finite_real_bounds he.le (hD d hd κ hk hcap ε he he').1⟩

#print axioms gaussian_query_lower_bound_with_disclosed_spectrum
#print axioms gaussian_query_lower_bound_real
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
