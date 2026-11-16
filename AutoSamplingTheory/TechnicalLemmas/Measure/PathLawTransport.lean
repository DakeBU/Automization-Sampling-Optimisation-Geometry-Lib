import AutoSamplingTheory.TechnicalLemmas.Measure.Transport
import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw
import Mathlib.Analysis.Real.Sqrt

namespace AutoSamplingTheory.TechnicalLemmas.Measure.PathLawTransport

open Filter MeasureTheory
open scoped ENNReal NNReal Topology
open AutoSamplingTheory.TechnicalLemmas.Measure.Transport
open AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.WeakDiffusionLaw

variable {T Ω E : Type*} [TopologicalSpace T] [FirstCountableTopology T]
  [MeasurableSpace Ω] [TopologicalSpace E] [CompactSpace E] [MeasurableSpace E]
  [OpensMeasurableSpace (E × E)]

/-- Same-sample couplings of two evaluations of a continuous path have
cost tending to zero as the first time approaches the second. -/
theorem tendsto_transportCost_marginal_of_ae_continuous
    (P : ProbabilityMeasure Ω) (X : T → Ω → E) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (c : C(E × E, ℝ≥0)) (hzero : ∀ x : E, c (x, x) = 0) (s : T) :
    Tendsto (fun t => transportCost (fun z => (c z : ℝ≥0∞))
      (P.map (hX t).aemeasurable : Measure E) (P.map (hX s).aemeasurable : Measure E))
      (𝓝 s) (𝓝 0) := by
  let Z (t : T) (ω : Ω) := (X t ω, X s ω)
  have hZ (t : T) : Measurable (Z t) := (hX t).prodMk (hX s)
  have hZpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => Z t ω) :=
    hpaths.mono fun _ hω => hω.prodMk continuous_const
  let γ (t : T) := P.map (hZ t).aemeasurable
  have hγ : Continuous γ := continuous_marginal_law_of_ae_continuous P Z hZ hZpaths
  let C (t : T) := ∫⁻ z, (c z : ℝ≥0∞) ∂(γ t : Measure (E × E))
  have hC : Continuous C := (ProbabilityMeasure.continuous_lintegral_continuousMap c).comp hγ
  have hCs : C s = 0 := by
    dsimp [C, γ]
    have hc : Measurable (fun z : E × E => (c z : ℝ≥0∞)) :=
      measurable_coe_nnreal_ennreal.comp c.continuous.measurable
    rw [lintegral_map hc (hZ s)]
    simp [Z, hzero]
  have hlim : Tendsto C (𝓝 s) (𝓝 0) := hCs ▸ hC.continuousAt
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hlim (fun _ => bot_le) ?_
  intro t
  apply transportCost_le_lintegral_of_isCoupling
  constructor
  · simp only [γ, ProbabilityMeasure.toMeasure_map, Z, Measure.fst_map_prodMk (hX s)]
  · simp only [γ, ProbabilityMeasure.toMeasure_map, Z, Measure.snd_map_prodMk (hX t)]

/-- A transport and pointwise estimate gives joint continuity of a field
along the marginal laws of an almost surely continuous process. -/
theorem continuous_of_path_law_transport_bound
    {F : Type*} [NormedAddCommGroup F]
    (P : ProbabilityMeasure Ω) (X : T → Ω → E) (hX : ∀ t, Measurable (X t))
    (hpaths : ∀ᵐ ω ∂(P : Measure Ω), Continuous (fun t => X t ω))
    (c : C(E × E, ℝ≥0)) (hzero : ∀ x : E, c (x, x) = 0)
    (U : T × E → F) (L : ℝ)
    (hbound : ∀ p q : T × E, ‖U p - U q‖ ≤ L *
      (Real.sqrt (transportCost (fun z => ((c z : ℝ≥0∞) ^ 2))
        (P.map (hX p.1).aemeasurable : Measure E)
        (P.map (hX q.1).aemeasurable : Measure E)).toReal + (c (p.2, q.2) : ℝ))) :
    Continuous U := by
  rw [continuous_iff_continuousAt]
  intro q
  rw [ContinuousAt, tendsto_iff_norm_sub_tendsto_zero]
  let Q (p : T × E) := transportCost (fun z => ((c z : ℝ≥0∞) ^ 2))
    (P.map (hX p.1).aemeasurable : Measure E) (P.map (hX q.1).aemeasurable : Measure E)
  let c₂ : C(E × E, ℝ≥0) := c ^ 2
  have hzero₂ (x : E) : c₂ (x, x) = 0 := by simp [c₂, hzero]
  have hQ : Tendsto Q (𝓝 q) (𝓝 0) := by
    have h := (tendsto_transportCost_marginal_of_ae_continuous P X hX hpaths c₂ hzero₂ q.1).comp
      continuous_fst.continuousAt
    simpa only [Q, c₂, Function.comp_def, ContinuousMap.pow_apply, ENNReal.coe_pow] using h
  have hroot : Tendsto (fun p => Real.sqrt (Q p).toReal) (𝓝 q) (𝓝 0) := by
    simpa only [Function.comp_def, ENNReal.toReal_zero, Real.sqrt_zero] using
      ((ENNReal.tendsto_toReal ENNReal.zero_ne_top).comp hQ).sqrt
  have hc : Continuous (fun p : T × E => (c (p.2, q.2) : ℝ)) :=
    NNReal.continuous_coe.comp (c.continuous.comp (continuous_snd.prodMk continuous_const))
  have hpoint : Tendsto (fun p : T × E => (c (p.2, q.2) : ℝ)) (𝓝 q) (𝓝 0) := by
    simpa only [hzero, NNReal.coe_zero] using (hc.continuousAt (x := q)).tendsto
  have hmajor : Tendsto (fun p => L * (Real.sqrt (Q p).toReal + (c (p.2, q.2) : ℝ)))
      (𝓝 q) (𝓝 0) := by
    simpa only [add_zero, mul_zero] using tendsto_const_nhds.mul (hroot.add hpoint)
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hmajor
    (fun _ => norm_nonneg _) (fun p => hbound p q)

end AutoSamplingTheory.TechnicalLemmas.Measure.PathLawTransport
