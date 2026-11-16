import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveDriftIntegral
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoWeightedRiemannSums

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open ProgressiveDriftIntegral ItoWeightedRiemannSums
open AutoSamplingTheory.TechnicalLemmas.Analysis.PrefixIntegral

/-- The initialized progressive drift has its fixed-horizon primitive
representation and continuous finite-variation paths. -/
theorem initialized_drift_progressive_continuous_boundedVariation
    {Ω : Type*} [MeasurableSpace Ω]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} {T : ℝ≥0} (x : Ω → ℝ)
    (hx : StronglyMeasurable[filtration 0] x)
    (b : ℝ≥0 → Ω → ℝ) (hb : IsStronglyProgressive filtration b)
    (hbi : ∀ᵐ ω ∂μ, Integrable (fun s => b s ω) (TimeMeasure.upTo T)) :
    let A := fun t ω => x ω + prefixIntegralProcess b t ω
    IsStronglyProgressive filtration A ∧
      (∀ t ≤ T, ∀ ω, A t ω = x ω + prefixIntegral (fun s => b s ω) T t) ∧
      (∀ᵐ ω ∂μ, ContinuousOn (fun t => A t ω) (Icc 0 T) ∧
        BoundedVariationOn (fun t => A t ω) (Icc 0 T)) := by
  intro A
  have hInitial : StronglyAdapted filtration (fun _ => x) :=
    fun t => hx.mono (filtration.mono (show (0 : ℝ≥0) ≤ t from bot_le))
  have hEq (t : ℝ≥0) (ht : t ≤ T) (ω : Ω) :
      prefixIntegralProcess b t ω = prefixIntegral (fun s => b s ω) T t := by
    rw [prefixIntegralProcess_eq_fixedHorizon b ht, prefixIntegral, min_eq_left ht]
    apply integral_congr_ae
    exact Eventually.of_forall fun s => by
      by_cases hs : s < t
      · simp only [if_pos hs, min_eq_left (hs.le.trans ht)]
      · simp only [if_neg hs]
  have hAeq (t : ℝ≥0) (ht : t ≤ T) (ω : Ω) :
      A t ω = x ω + prefixIntegral (fun s => b s ω) T t :=
    congrArg (x ω + ·) (hEq t ht ω)
  refine ⟨(hInitial.isStronglyProgressive_of_continuous fun _ => continuous_const).add
    (prefixIntegralProcess_stronglyProgressive b hb), hAeq, ?_⟩
  filter_upwards [hbi] with ω hω
  let P := prefixIntegral (fun s => b s ω) T
  have hSame : EqOn (fun t => A t ω) (fun t => x ω + P t) (Icc 0 T) :=
    fun t ht => hAeq t ht.2 ω
  refine ⟨(continuous_const.add (continuous_prefixIntegral hω)).continuousOn.congr hSame, ?_⟩
  unfold BoundedVariationOn
  rw [eVariationOn.congr hSame]
  have hVar : eVariationOn (fun t => x ω + P t) (Icc 0 T) =
      eVariationOn P (Icc 0 T) := by
    unfold eVariationOn
    simp only [edist_dist, Real.dist_eq, add_sub_add_left_eq_sub]
  rw [hVar]
  exact boundedVariationOn_prefixIntegral hω

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoInitializedDrift
