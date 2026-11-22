import B3HistoryUpdate
import ParameterizedPushforward

/-!
# One response added to a history

On a region of histories with fixed residual dimensions, the observation
may be encoded using the old history. If its pre-encoding law factors from
the remaining blocks, the posterior after the recorded response has the
same residual law. A history-determined response also preserves a possibly
history-dependent residual kernel.
-/

open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {H X Y Z R : Type*}
  [MeasurableSpace H] [MeasurableSpace X] [MeasurableSpace Y]
  [MeasurableSpace Z] [MeasurableSpace R]

/-- Encode the observed direction as the algorithm's response and retain the
actual new residual. The response kernel only uses the observation law and the
public encoding. -/
theorem extend_encoded_response (ρ : Measure H) [SFinite ρ]
    (μ : Measure X) [SFinite μ] (σ : Measure Z) [IsProbabilityMeasure σ]
    (ν : Measure R) [SFinite ν]
    (read : H → X → Z × R) (hm : Measurable (Function.uncurry read))
    (hlaw : ∀ h, μ.map (read h) = σ.prod ν)
    (encode : H → Z → Y) (he : Measurable (Function.uncurry encode)) :
    (ρ.prod μ).map (fun p : H × X =>
      ((p.1, encode p.1 (read p.1 p.2).1), (read p.1 p.2).2)) =
      (ρ ⊗ₘ kernel σ encode).prod ν := by
  let step (h : H) (x : X) := (encode h (read h x).1, (read h x).2)
  have hs : Measurable (Function.uncurry step) :=
    (he.comp (measurable_fst.prodMk hm.fst)).prodMk hm.snd
  let := isMarkovKernel_kernel σ encode he
  have hfiber (h : H) : μ.map (step h) = (kernel σ encode h).prod ν := by
    have henc : Measurable (encode h) := he.of_uncurry_left
    have hp : MeasurePreserving (encode h) σ (σ.map (encode h)) := ⟨henc, rfl⟩
    change μ.map (Prod.map (encode h) id ∘ read h) = _
    rw [← Measure.map_map (henc.prodMap measurable_id) hm.of_uncurry_left, hlaw,
      kernel_apply σ encode he]
    exact (hp.prod (MeasurePreserving.id ν)).map_eq
  have h := extend_history_posterior ρ (Kernel.const H μ) (kernel σ encode)
    (Kernel.const H ν) step hs (ae_of_all _ hfiber)
  change (ρ ⊗ₘ Kernel.const H μ).map _ =
    (ρ ⊗ₘ kernel σ encode) ⊗ₘ (Kernel.const (H × Y) ν) at h
  simpa only [Measure.compProd_const] using h

/-- Appending a history-determined response (including a padding symbol) keeps
every residual coordinate and its posterior. -/
theorem extend_determined_response (ρ : Measure H) [SFinite ρ]
    (old : Kernel H X) [IsSFiniteKernel old] (f : H → Y) (hf : Measurable f) :
    (ρ ⊗ₘ old).map (fun p : H × X => ((p.1, f p.1), p.2)) =
      (ρ ⊗ₘ Kernel.deterministic f hf) ⊗ₘ Kernel.prodMkRight Y old := by
  apply extend_history_posterior ρ old (Kernel.deterministic f hf) old
    (fun h x => (f h, x)) ((hf.comp measurable_fst).prodMk measurable_snd)
  exact ae_of_all _ fun h => by rw [Kernel.deterministic_apply, Measure.dirac_prod]

#print axioms extend_encoded_response
#print axioms extend_determined_response

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
