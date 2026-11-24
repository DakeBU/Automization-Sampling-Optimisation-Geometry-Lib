import GCCAmbientState
import GCCLastCoordinate
import GC3Unframe

noncomputable section
set_option maxHeartbeats 700000
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H Z : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace Z]
  {N m : ℕ} {μ : Measure Ω} {h : Ω → H} {A : Ω → O N}

theorem HaarState.auxiliary [IsProbabilityMeasure μ] {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) {z : Ω → Z} (hz : Measurable z)
    (hi : IndepFun (fun ω => (h ω,A ω)) z μ) :
    HaarState μ (fun ω => (h ω,z ω)) A (fun p : H × Z => F p.1) W := by
  let read := fun p : H × O N => (p.1, readResidualAt m ⟨m,F p.1⟩ p.2)
  have ht : Measurable (fun a => (⟨m,F a⟩ : PublicFrame N)) :=
    (PublicFrame.measurable_tag m).comp (PublicFrame.measurable_blockFrame state.domain state.range)
  let tag := fun p : H × O N => (⟨m,F p.1⟩ : PublicFrame N)
  let args := fun p : H × O N => (tag p,p.2)
  have htag : Measurable tag := ht.comp measurable_fst
  have hargs : Measurable args := htag.prodMk measurable_snd
  let unframe := Function.uncurry (@readResidualAt N m)
  have hf : Measurable unframe := measurable_readResidualAt m
  have hv : Measurable (unframe ∘ args) := hf.comp hargs
  have hm : Measurable read := measurable_fst.prodMk hv
  apply state.independent_auxiliary hz
  apply (hi.comp hm measurable_id).congr _ (Filter.EventuallyEq.rfl)
  filter_upwards [state.reconstruct] with ω e
  change (h ω,readResidualAt m ⟨m,F (h ω)⟩ (A ω)) = _
  rw [e,readResidualAt_realize]

theorem HaarState.response_eq [NeZero m] {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) (b : Bool) (x : H → Vec N) :
    ∀ᵐ ω ∂μ, response b (A ω) (x (h ω)) =
      frameResponse (F (h ω)) b (x (h ω)) (frameObservation (F (h ω)) b (x (h ω)) (W ω)) := by
  filter_upwards [state.reconstruct] with ω e
  rw [e]
  cases b
  · exact frameAnswer_eq (F (h ω)) false (x (h ω)) (W ω)
  · exact frameAnswer_eq (F (h ω)) true (x (h ω)) (W ω)

def lastFrame (F : H → BlockFrame N 1) (b : Bool) (x : H → Vec N)
    (p : H × Vec N) : BlockFrame N 0 :=
  fullFrame ((F p.1).realize (lastDecode (frameUnit (F p.1) b (x p.1)) (frameUnit (F p.1) (!b) p.2)))

/-- The final nonzero revelation, whether an image or a preimage, leaves a
zero-dimensional Haar residual. The new frame uses only the recorded answer. -/
theorem HaarState.last [IsFiniteMeasure μ] {F : H → BlockFrame N 1} {W : Ω → O 1}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) b (x (h ω)) ≠ 0) :
    HaarState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A (lastFrame F b x)
      (fun _ => (1 : O 0)) := by
  have hh : Measurable h := measurable_fst.comp state.law.measurable
  have hy := (measurable_response (N := N) b).comp (state.ambient.prodMk (hx.comp hh))
  have hD : Measurable (fun p : H × Vec N => (F p.1).domain) := state.domain.comp measurable_fst
  have hR : Measurable (fun p : H × Vec N => (F p.1).range) := state.range.comp measurable_fst
  have hu : Measurable (fun p : H × Vec N => frameUnit (F p.1) b (x p.1)) :=
    measurable_frameUnit hD hR measurable_const (hx.comp measurable_fst)
  have hz : Measurable (fun p : H × Vec N => frameUnit (F p.1) (!b) p.2) :=
    measurable_frameUnit hD hR measurable_const measurable_snd
  exact {
    domain := measurable_const
    range := measurable_realize_family hD hR (measurable_lastDecode.comp (hu.prodMk hz))
    ambient := state.ambient
    law := zero_law μ (hh.prodMk hy)
    reconstruct := by
      filter_upwards [state.reconstruct, state.response_eq b x, hc] with ω hA hy hcω
      change A ω = (fullFrame ((F (h ω)).realize (lastDecode _
        (unitOrFirst (frameComplement (F (h ω)) (!b) (response b (A ω) (x (h ω)))))))).realize 1
      rw [fullFrame_realize,hy,recovered_observation _ _ _ _ hcω]
      exact hA.trans (congrArg (F (h ω)).realize (lastDecode_reveal b _ (W ω)).symm) }

/-- If the domain was already fully exposed, every further response retains
the same conditional state. -/
theorem HaarState.exhausted [IsFiniteMeasure μ] {F : H → BlockFrame N 0} {W : Ω → O 0}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x) :
    HaarState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A
      (fun p : H × Vec N => F p.1) W := by
  let : Subsingleton (O 0) := ⟨fun _ _ => Subtype.ext (funext fun i => i.elim0)⟩
  have hh : Measurable h := measurable_fst.comp state.law.measurable
  have hW : Measurable W := measurable_snd.comp state.law.measurable
  have hm := hh.prodMk ((measurable_response (N := N) b).comp (state.ambient.prodMk (hx.comp hh)))
  exact ⟨state.domain.comp measurable_fst,state.range.comp measurable_fst,state.ambient,
    (zero_law μ hm).congr_ae hm hW Filter.EventuallyEq.rfl (ae_of_all _ fun _ => Subsingleton.elim _ _),
    state.reconstruct⟩

#print axioms HaarState.last
#print axioms HaarState.auxiliary
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
