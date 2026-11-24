import GCCTaggedLocal
import GCCPublicStep
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
noncomputable section
set_option maxHeartbeats 800000
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
variable {Ω H L : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace L]
  {N m : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

def postFrame (F : H → PublicFrame N) (b : Bool) (x : H → Vec N) (p : H × Vec N) : PublicFrame N :=
  nextPublic (F p.1) b (x p.1) p.2

theorem measurable_postFrame {F : H → PublicFrame N} (hF : Measurable F) (b : Bool) {x : H → Vec N}
    (hx : Measurable x) : Measurable (postFrame F b x) :=
  measurable_nextPublic (hF.comp measurable_fst) b (hx.comp measurable_fst) measurable_snd

omit [IsFiniteMeasure μ] in
theorem ae_post_mem {y : Ω → L} (hh : Measurable h) (hy : Measurable y)
    {s : Set H} (hs : MeasurableSet s) :
    ∀ᵐ p ∂(μ.restrict (h ⁻¹' s)).map (fun ω => (h ω,y ω)), p.1 ∈ s :=
  (ae_map_iff (hh.prodMk hy).aemeasurable (measurable_fst hs)).mpr (ae_restrict_mem (hh hs))

theorem TaggedState.glue_first {I : Type*} [Countable I] {y : Ω → L} {G : H × L → PublicFrame N}
    (hh : Measurable h) (hy : Measurable y) (hA : Measurable A) (hG : Measurable G)
    (s : I → Set H) (hs : ∀ i, MeasurableSet (s i)) (cov : ∀ a, ∃ i, a ∈ s i)
    (st : ∀ i, TaggedState (μ.restrict (h ⁻¹' s i)) (fun ω => (h ω,y ω)) A G) :
    TaggedState μ (fun ω => (h ω,y ω)) A G :=
  TaggedState.glue (hh.prodMk hy) hA hG (fun i => Prod.fst ⁻¹' s i)
    (fun i => measurable_fst (hs i)) (fun p => cov p.1) st

theorem TaggedState.glue_cases {y : Ω → L} {G : H × L → PublicFrame N}
    (hh : Measurable h) (hy : Measurable y) (hA : Measurable A) (hG : Measurable G)
    {s : Set H} (hs : MeasurableSet s)
    (pos : TaggedState (μ.restrict (h ⁻¹' s)) (fun ω => (h ω,y ω)) A G)
    (neg : TaggedState (μ.restrict (h ⁻¹' sᶜ)) (fun ω => (h ω,y ω)) A G) :
    TaggedState μ (fun ω => (h ω,y ω)) A G := by
  apply TaggedState.glue_first hh hy hA hG (fun i : Bool => if i then s else sᶜ)
  · intro i; cases i <;> simp [hs]
  · intro a; by_cases e : a ∈ s
    · exact ⟨true,e⟩
    · exact ⟨false,e⟩
  · intro i; cases i
    · exact neg
    · exact pos

def informativeFrame : {m : ℕ} → (H → BlockFrame N (m+1)) → Bool → (H → Vec N) →
    (H × Vec N) → BlockFrame N m
  | 0,F,b,x => lastFrame F b x
  | _n+1,F,b,x => readFrame F b x

theorem informativeState {F : H → BlockFrame N (m+1)} {W : Ω → O (m+1)}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) b (x (h ω)) ≠ 0) :
    HaarState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A (informativeFrame F b x)
      (fun ω => (reveal (m := m) b (frameUnit (F (h ω)) b (x (h ω))) (W ω)).2) := by
  cases m with
  | zero => exact state.last b hx hc
  | succ n => exact state.informative b hx hc

theorem HaarState.update {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x) :
    TaggedState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A
      (postFrame (fun a => ⟨m,F a⟩) b x) := by
  classical
  let y := fun ω => response b (A ω) (x (h ω))
  let G := postFrame (fun a => ⟨m,F a⟩) b x
  have hh : Measurable h := measurable_fst.comp state.law.measurable
  have hy : Measurable y := (measurable_response b).comp (state.ambient.prodMk (hx.comp hh))
  have hG : Measurable G := measurable_postFrame state.tagged.frame b hx
  cases m with
  | zero => exact (state.exhausted b hx).tagged
  | succ n =>
    let s := {a | frameComplement (F a) b (x a) = 0}
    have hs : MeasurableSet s :=
      (measurable_frameComplement state.domain state.range (measurable_const (a := b)) hx) (measurableSet_singleton 0)
    apply TaggedState.glue_cases hh hy state.ambient hG hs
    · have st := state.restrict_history hs
      have hc : ∀ᵐ ω ∂μ.restrict (h ⁻¹' s), frameComplement (F (h ω)) b (x (h ω)) = 0 :=
        ae_restrict_mem (hh hs)
      apply (st.determined b hx hc).tagged.congr_frame hG
      filter_upwards [ae_post_mem hh hy hs] with p ep
      change frameComplement (F p.1) b (x p.1) = 0 at ep
      cases n <;> simp [G,postFrame,nextPublic,ep]
    · have st := state.restrict_history hs.compl
      have hc : ∀ᵐ ω ∂μ.restrict (h ⁻¹' sᶜ), frameComplement (F (h ω)) b (x (h ω)) ≠ 0 :=
        ae_restrict_mem (hh hs.compl)
      apply (informativeState st b hx hc).tagged.congr_frame hG
      filter_upwards [ae_post_mem hh hy hs.compl] with p ep
      change frameComplement (F p.1) b (x p.1) ≠ 0 at ep
      cases n <;> simp [G,postFrame,nextPublic,ep,informativeFrame,lastFrame,readFrame]

#print axioms HaarState.update
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
