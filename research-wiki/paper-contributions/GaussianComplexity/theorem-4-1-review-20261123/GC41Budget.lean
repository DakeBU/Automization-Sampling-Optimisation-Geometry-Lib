import GC41Risk
import GC44Uniform
import GC31ExactSampler

/-! The uniform dimension cutoff, disclosure of the full spectrum and equation (2). -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis

universe u v w
variable {Seed : Type u} {State : Type v} [MeasurableSpace Seed] [MeasurableSpace State]

/-- A probability bound on the actual joint experiment follows from a
representation on any probability space, retaining the hidden orientation. -/
theorem algorithm_pass_of_representation {d q : ℕ} {κ : ℝ} (hκ : 2 ≤ κ)
    (hq : 2*q+1 < d) (ht : queryThreshold 2048 d q ≤ 1/2)
    (ρ : Measure Seed) (alg : Algorithm d Seed State)
    {Ω : Type w} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (pair : Ω → Matrix.orthogonalGroup (Fin d) ℝ × Space d) (g : Ω → Starts d q)
    (hp : MeasurePreserving pair μ (experimentLaw κ q ρ alg))
    (hg : MeasurePreserving g μ (gaussianStarts d q))
    (hmem : ∀ᵐ ω ∂μ, (pair ω).1.val.transpose *ᵥ WithLp.ofLp (pair ω).2 ∈ krylov d q κ (g ω)) :
    (experimentLaw κ q ρ alg).real (jointDetectorEvent d q κ (queryThreshold 2048 d q)) ≤ 1/100 :=
  detector_rare_of_krylov_coupling hκ hq ht
    ((by norm_num : (99/100:ℝ) ≤ 199/200).trans (simultaneous_gram_concentration hq ht))
    μ _ pair g hp hg hmem

/-- Feasible deterministic query caps for a sampler supplied with all eigenvalues
and their multiplicities before the first call. -/
def DisclosedFeasibleBudget (d : ℕ) (κ ε : ℝ) (q : ℕ) : Prop :=
  ∃ (Seed : Type u) (State : Type v) (_ : MeasurableSpace Seed) (_ : MeasurableSpace State)
    (ρ : Measure Seed) (_ : IsProbabilityMeasure ρ) (alg : Polynomial ℝ → Algorithm d Seed State),
    ∀ A : Precision d, Admissible κ A →
      eventTV ((alg A.charpoly).outputLaw ρ q A) (targetLaw A) ≤ ε

def disclosedQueryComplexity (d : ℕ) (κ ε : ℝ) : ℝ≥0∞ :=
  ⨅ t : {q : ℕ // DisclosedFeasibleBudget.{u,v} d κ ε q}, (t.val : ℝ≥0∞)

theorem disclosedQueryComplexity_le (d : ℕ) (κ ε : ℝ) :
    disclosedQueryComplexity.{u,v} d κ ε ≤ gaussianQueryComplexity.{u,v} d κ ε := by
  apply le_iInf
  intro t
  obtain ⟨S,T,mS,mT,ρ,hρ,alg,hacc⟩ := t.property
  exact iInf_le (fun x : {q : ℕ // DisclosedFeasibleBudget.{u,v} d κ ε q} => (x.val : ℝ≥0∞))
    ⟨t.val, S,T,mS,mT,ρ,hρ,(fun _ => alg),hacc⟩

/-- The hard family has one disclosed polynomial. A single dimension cutoff
controls every budget in the testing range, including zero. -/
theorem budget_from_detector {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ ε : ℝ, ε ≤ 1/10 → ∀ q : ℕ,
      ∀ {Seed : Type u} {State : Type v} [MeasurableSpace Seed] [MeasurableSpace State],
      (∀ (ρ : Measure Seed) [IsProbabilityMeasure ρ] (alg : Algorithm d Seed State),
        2*q+1 < d → queryThreshold 2048 d q ≤ 1/2 →
        (experimentLaw κ q ρ alg).real (jointDetectorEvent d q κ (queryThreshold 2048 d q)) ≤ 1/100) →
      ∀ (ρ : Measure Seed) [IsProbabilityMeasure ρ] (algs : Polynomial ℝ → Algorithm d Seed State),
        (∀ A : Precision d, Admissible κ A →
          eventTV ((algs A.charpoly).outputLaw ρ q A) (targetLaw A) ≤ ε) →
        δ/256 * Real.sqrt κ * Real.log (d : ℝ) ≤ (q : ℝ) := by
  obtain ⟨D, hD⟩ := eventual_source_signal 2048 (by norm_num) hδ hδ'
  obtain ⟨P, hP⟩ := eventual_rotated_target_power 2048 (by norm_num) hδ hδ'
  refine ⟨max D P, ?_⟩
  intro d hd κ hκ hcap ε he q Seed State _ _ hrare ρ _ algs hacc
  by_contra! hsmall
  let O₀ : Matrix.orthogonalGroup (Fin d) ℝ := 1
  let p := (hiddenPrecision κ O₀).charpoly
  let alg := algs p
  have hsig := hD d ((le_max_left D P).trans hd) κ hκ hcap q hsmall.le
  obtain ⟨hd2,_,hn,_,_,ht,_⟩ := hsig
  have ha (O : Matrix.orthogonalGroup (Fin d) ℝ) :
      eventTV (alg.outputLaw ρ q (hiddenPrecision κ O)) (targetLaw (hiddenPrecision κ O)) ≤ ε := by
    have hs : (hiddenPrecision κ O).charpoly = p :=
      (hiddenPrecision_charpoly κ O).trans (hiddenPrecision_charpoly κ O₀).symm
    simpa only [hs,alg] using hacc (hiddenPrecision κ O) (admissible_hiddenPrecision hd2 hκ O)
  have hlow := experiment_detector_lower ρ alg ha
    (hP d ((le_max_right D P).trans hd) κ hκ hcap q hsmall.le)
  have hhigh := hrare ρ alg hn ht
  linarith

#print axioms budget_from_detector
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
