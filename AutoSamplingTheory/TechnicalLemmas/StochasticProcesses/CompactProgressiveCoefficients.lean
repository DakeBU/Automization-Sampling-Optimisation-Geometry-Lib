import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2
import Mathlib.MeasureTheory.Integral.Prod

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactProgressiveCoefficients

open Filter MeasureTheory Set TopologicalSpace
open scoped NNReal ENNReal
open ElementaryItoIntegral ProgressiveL2

/-- A continuous scalar coefficient evaluated on a compact-state progressive
process is progressive and has finite horizon integrability. -/
theorem continuous_coefficient_along_compact_process
    {Ω S : Type*} [MeasurableSpace Ω] [TopologicalSpace S] [CompactSpace S]
    [PseudoMetrizableSpace S] [SecondCountableTopology S] [MeasurableSpace S] [BorelSpace S]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ]
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (c : ℝ≥0 × S → ℝ) (hc : Continuous c) (T : ℝ≥0) (p : ℝ≥0∞) :
    let b := fun t ω => c (t, X t ω)
    IsStronglyProgressive filtration b ∧
    (∀ ω, Integrable (fun t => b t ω) (TimeMeasure.upTo T)) ∧
    MemLp (processFunction b) p (processTimeMeasure μ T) := by
  intro b
  have hcompact : IsCompact (Icc (0 : ℝ≥0) T ×ˢ (univ : Set S)) :=
    isCompact_Icc.prod isCompact_univ
  obtain ⟨C, hC⟩ := hcompact.bddAbove_image hc.norm.continuousOn
  have hbound (t : ℝ≥0) (ht : t ≤ T) (ω : Ω) : ‖b t ω‖ ≤ C :=
    hC ⟨(t, X t ω), ⟨⟨bot_le, ht⟩, mem_univ _⟩, rfl⟩
  have htime : ∀ᵐ t ∂TimeMeasure.upTo T, t ≤ T :=
    (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ ht => ht.2
  refine ⟨?_, ?_, ?_⟩
  · intro t
    let _ : MeasurableSpace Ω := filtration t
    exact (hc.measurable.comp
      ((measurable_subtype_coe.comp measurable_fst).prodMk (hProgressive t).measurable)).stronglyMeasurable
  · intro ω
    have hm := hc.measurable.comp (measurable_id.prodMk
      (hX.comp (measurable_id.prodMk (measurable_const (a := ω)))))
    exact Integrable.of_bound hm.aestronglyMeasurable C
      (htime.mono fun t ht => hbound t ht ω)
  · have hXswap : Measurable (fun z : Ω × ℝ≥0 => X z.2 z.1) :=
      hX.comp (measurable_snd.prodMk measurable_fst)
    have hm := hc.measurable.comp (measurable_snd.prodMk hXswap)
    change MemLp (processFunction b) p (μ.prod (TimeMeasure.upTo T))
    exact MemLp.of_bound hm.aestronglyMeasurable C
      ((Measure.quasiMeasurePreserving_snd.ae htime).mono fun z hz => hbound z.2 hz z.1)

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CompactProgressiveCoefficients
