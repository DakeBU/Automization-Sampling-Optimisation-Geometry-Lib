import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2
import Mathlib.MeasureTheory.Integral.Prod

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveCoefficientBounds

open Filter MeasureTheory Set TopologicalSpace
open scoped NNReal ENNReal
open ElementaryItoIntegral ProgressiveL2

/-- A jointly measurable scalar coefficient with a uniform state bound on a
finite time interval gives a progressive coefficient with integrable time
sections and finite product-space moments on that interval. -/
theorem bounded_measurable_coefficient_along_progressive_process
    {Ω S : Type*} [MeasurableSpace Ω] [TopologicalSpace S]
    [PseudoMetrizableSpace S] [MeasurableSpace S] [BorelSpace S]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ]
    (X : ℝ≥0 → Ω → S) (hX : Measurable (Function.uncurry X))
    (hProgressive : IsStronglyProgressive filtration X)
    (c : ℝ≥0 × S → ℝ) (hc : Measurable c) (T : ℝ≥0) (p : ℝ≥0∞)
    (hBound : ∃ C : ℝ, ∀ t ≤ T, ∀ x, ‖c (t, x)‖ ≤ C) :
    let b := fun t ω => c (t, X t ω)
    IsStronglyProgressive filtration b ∧
    (∀ ω, Integrable (fun t => b t ω) (TimeMeasure.upTo T)) ∧
    MemLp (processFunction b) p (processTimeMeasure μ T) := by
  intro b
  obtain ⟨C, hC⟩ := hBound
  have htime : ∀ᵐ t ∂TimeMeasure.upTo T, t ≤ T :=
    (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ ht => ht.2
  refine ⟨?_, ?_, ?_⟩
  · intro t
    let _ : MeasurableSpace Ω := filtration t
    exact (hc.comp
      ((measurable_subtype_coe.comp measurable_fst).prodMk (hProgressive t).measurable)).stronglyMeasurable
  · intro ω
    have hm := hc.comp (measurable_id.prodMk
      (hX.comp (measurable_id.prodMk (measurable_const (a := ω)))))
    exact Integrable.of_bound hm.aestronglyMeasurable C
      (htime.mono fun t ht => hC t ht (X t ω))
  · have hXswap : Measurable (fun z : Ω × ℝ≥0 => X z.2 z.1) :=
      hX.comp (measurable_snd.prodMk measurable_fst)
    have hm := hc.comp (measurable_snd.prodMk hXswap)
    change MemLp (processFunction b) p (μ.prod (TimeMeasure.upTo T))
    exact MemLp.of_bound hm.aestronglyMeasurable C
      ((Measure.quasiMeasurePreserving_snd.ae htime).mono fun z hz => hC z.2 hz (X z.2 z.1))

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveCoefficientBounds
