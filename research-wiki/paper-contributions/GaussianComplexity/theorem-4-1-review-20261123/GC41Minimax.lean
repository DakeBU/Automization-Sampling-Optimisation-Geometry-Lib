import GC41Budget
import GC43Extension

/-! From the representation of the actual adaptive output to both minimax complexities. -/
noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
universe u v

theorem query_complexities_from_representation
    (rep : ∀ {d q : ℕ} {κ : ℝ}, 2 ≤ κ → 2*q+1 < d →
      ∀ {Seed : Type u} {State : Type v} [MeasurableSpace Seed] [MeasurableSpace State]
        (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State),
          HasKrylovRepresentation (q := q) κ (experimentLaw κ q ρ alg))
    {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ ε : ℝ, 0 < ε → ε ≤ 1/10 →
      ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤ disclosedQueryComplexity.{u,v} d κ ε ∧
      ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤ gaussianQueryComplexity.{u,v} d κ ε := by
  obtain ⟨D,hD⟩ := budget_from_detector.{u,v} hδ hδ'
  refine ⟨D, ?_⟩
  intro d hd κ hκ hcap ε _ he
  suffices hb : ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤
      disclosedQueryComplexity.{u,v} d κ ε from ⟨hb, hb.trans (disclosedQueryComplexity_le ..)⟩
  apply le_iInf
  intro t
  obtain ⟨Seed,State,mS,mT,ρ,hρ,algs,ha⟩ := t.property
  refine ENNReal.ofReal_le_natCast.mpr (hD d hd κ hκ hcap ε he t.val ?_ ρ algs ha)
  intro σ _ alg hn ht
  obtain ⟨M,hM,hp,hg,hm⟩ := rep hκ hn σ alg
  exact algorithm_pass_of_representation hκ hn ht σ alg M Prod.fst Prod.snd hp hg hm

/-- The column-query sampler witnesses finiteness in the canonical universe. -/
theorem finite_real_bounds {d : ℕ} {κ ε L : ℝ} (he : 0 ≤ ε)
    (h : ENNReal.ofReal L ≤ disclosedQueryComplexity.{0,0} d κ ε) :
    L ≤ (disclosedQueryComplexity.{0,0} d κ ε).toReal ∧
    L ≤ (gaussianQueryComplexity.{0,0} d κ ε).toReal := by
  have hle := disclosedQueryComplexity_le.{0,0} d κ ε
  have hu := (gaussian_query_complexity_le_dimension d κ he).trans_lt (ENNReal.natCast_lt_top d)
  have hl := ENNReal.toReal_mono (hle.trans_lt hu).ne h
  rw [ENNReal.toReal_ofReal'] at hl
  have hb := (le_max_left _ _).trans hl
  exact ⟨hb, hb.trans (ENNReal.toReal_mono hu.ne hle)⟩

#print axioms query_complexities_from_representation
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
