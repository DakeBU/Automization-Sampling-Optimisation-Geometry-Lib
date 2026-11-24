import GCCRevelationLaw
import GC43FrameMeasurable

/-! Haar states and their forward/inverse ambient observations. Frames and query
vectors are arbitrary measurable functions of the pre-existing history. -/
noncomputable section
set_option maxHeartbeats 1000000
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H Z : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace Z]
  {N m n : ℕ}

/-- Frame coordinates of Definition C.2. Its public frames describe the exposed
subspace and the already known isometry. Realizing the remaining conditional
Haar isometry reconstructs the original ambient matrix almost surely. -/
structure HaarState (μ : Measure Ω) (h : Ω → H) (A : Ω → O N)
    (F : H → BlockFrame N m) (W : Ω → O m) : Prop where
  domain : Measurable (fun a => (F a).domain)
  range : Measurable (fun a => (F a).range)
  ambient : Measurable A
  law : LawGiven μ h W (orthogonalHaar m)
  reconstruct : ∀ᵐ ω ∂μ, A ω = (F (h ω)).realize (W ω)

theorem HaarState.restrict_history {μ : Measure Ω} [IsFiniteMeasure μ]
    {h : Ω → H} {A : Ω → O N} {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) {s : Set H} (hs : MeasurableSet s) :
    HaarState (μ.restrict (h ⁻¹' s)) h A F W := by
  let := (orthogonalHaar_spec m).1
  exact ⟨state.domain,state.range,state.ambient,state.law.restrict_history hs,
    ae_mono Measure.restrict_le_self state.reconstruct⟩

theorem HaarState.independent_auxiliary {μ : Measure Ω} [IsProbabilityMeasure μ]
    {h : Ω → H} {A : Ω → O N} {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) {z : Ω → Z} (hz : Measurable z)
    (hi : IndepFun (fun ω => (h ω,W ω)) z μ) :
    HaarState μ (fun ω => (h ω,z ω)) A (fun p : H × Z => F p.1) W := by
  let := (orthogonalHaar_spec m).1
  exact ⟨state.domain.comp measurable_fst,state.range.comp measurable_fst,state.ambient,
    state.law.independent_auxiliary hz hi,state.reconstruct⟩

def response (b : Bool) (A : O N) (x : Vec N) : Vec N :=
  act (if b then A⁻¹ else A) x

theorem measurable_response (b : Bool) :
    Measurable (fun p : O N × Vec N => response b p.1 p.2) := by
  cases b
  · exact (continuous_act _).measurable
  · exact (continuous_act _).measurable.comp (measurable_fst.inv.prodMk measurable_snd)

def readFrame (F : H → BlockFrame N (n+2)) (b : Bool) (x : H → Vec N)
    (p : H × Vec N) : BlockFrame N (n+1) :=
  frameAfter (F p.1) (sectionQ n) b (x p.1) (frameUnit (F p.1) (!b) p.2)

theorem measurable_readFrame {F : H → BlockFrame N (n+2)} (b : Bool) {x : H → Vec N}
    (hD : Measurable fun a => (F a).domain) (hR : Measurable fun a => (F a).range)
    (hx : Measurable x) : Measurable (fun p => (readFrame F b x p).domain) ∧
      Measurable (fun p => (readFrame F b x p).range) :=
  measurable_frameAfter _ (sectionQ_meas n) (hD.comp measurable_fst) (hR.comp measurable_fst)
    measurable_const (hx.comp measurable_fst) (measurable_frameUnit (hD.comp measurable_fst)
      (hR.comp measurable_fst) measurable_const measurable_snd)

/-- On the informative stratum the new frame reads the actual ambient answer.
Its law conditions on precisely that answer and the old history. -/
theorem HaarState.informative {μ : Measure Ω} [IsFiniteMeasure μ]
    {h : Ω → H} {A : Ω → O N} {F : H → BlockFrame N (n+2)} {W : Ω → O (n+2)}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) b (x (h ω)) ≠ 0) :
    let history := fun ω => (h ω,response b (A ω) (x (h ω)))
    let p := fun ω => reveal (m := n+1) b (frameUnit (F (h ω)) b (x (h ω))) (W ω)
    HaarState μ history A (readFrame F b x) (fun ω => (p ω).2) := by
  let := (orthogonalHaar_spec (n+1)).1
  let u := fun a => frameUnit (F a) b (x a)
  let p := fun ω => reveal (m := n+1) b (u (h ω)) (W ω)
  let y := fun ω => response b (A ω) (x (h ω))
  let enc := fun q : H × S (n+2) => (q.1,frameResponse (F q.1) b (x q.1) q.2)
  have hu : Measurable u := measurable_frameUnit state.domain state.range measurable_const hx
  have hh : Measurable h := measurable_fst.comp state.law.measurable
  have hW : Measurable W := measurable_snd.comp state.law.measurable
  have hinput : Measurable (fun ω => (u (h ω), W ω)) := (hu.comp hh).prodMk hW
  let rd : S (n+2) × O (n+2) → S (n+2) × O (n+1) :=
    fun q => reveal (m := n+1) b q.1 q.2
  have hrd : Measurable rd := measurable_reveal (m := n+1) b
  have hp : Measurable p := by
    change Measurable (rd ∘ (fun ω => (u (h ω), W ω)))
    exact hrd.comp hinput
  have hy : Measurable y := (measurable_response b).comp (state.ambient.prodMk (hx.comp hh))
  have he : Measurable enc := measurable_fst.prodMk (measurable_frameResponse
    (state.domain.comp measurable_fst) (state.range.comp measurable_fst) measurable_const
    (hx.comp measurable_fst) measurable_snd)
  have hobs (ω) : (p ω).1 = frameObservation (F (h ω)) b (x (h ω)) (W ω) :=
    reveal_direction (m := n+1) b (u (h ω)) (W ω)
  have hresp : ∀ᵐ ω ∂μ, y ω = frameResponse (F (h ω)) b (x (h ω)) (p ω).1 := by
    filter_upwards [state.reconstruct] with ω hω
    dsimp [y,response]
    rw [hω,hobs]
    cases b
    · exact frameAnswer_eq (F (h ω)) false (x (h ω)) (W ω)
    · exact frameAnswer_eq (F (h ω)) true (x (h ω)) (W ω)
  have hF := measurable_readFrame b state.domain state.range hx
  refine ⟨hF.1,hF.2,state.ambient,?_,?_⟩
  · have prior := (conditional_haar_revelation state.law b u hu).2.map_history he
    apply prior.congr_ae (hh.prodMk hy) hp.snd _ (Filter.EventuallyEq.rfl)
    filter_upwards [hresp] with ω heq using Prod.ext rfl heq.symm
  · filter_upwards [state.reconstruct,hresp,hc] with ω hω hyω hcω
    change A ω = (frameAfter (F (h ω)) (sectionQ n) b (x (h ω))
      (frameUnit (F (h ω)) (!b) (y ω))).realize (p ω).2
    rw [hyω]
    change A ω = (frameAfter _ _ _ _ (unitOrFirst (frameComplement _ _ _))).realize _
    rw [recovered_observation _ _ _ _ hcω,hω]
    exact frame_reconstruct (F (h ω)) (sectionQ n) (sectionQ_col n) b (x (h ω)) (W ω)

/-- When the residual component vanishes the whole old matrix conditional law
is retained, even after the actual ambient answer is added to the history. -/
theorem HaarState.determined {μ : Measure Ω} [IsFiniteMeasure μ] [NeZero m]
    {h : Ω → H} {A : Ω → O N} {F : H → BlockFrame N m} {W : Ω → O m}
    (state : HaarState μ h A F W) (b : Bool) {x : H → Vec N} (hx : Measurable x)
    (hc : ∀ᵐ ω ∂μ, frameComplement (F (h ω)) b (x (h ω)) = 0) :
    HaarState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A
      (fun p : H × Vec N => F p.1) W := by
  let := (orthogonalHaar_spec m).1
  let enc := fun a => (a,frameResponse (F a) b (x a) (coordinatePoint 0))
  have he : Measurable enc := measurable_id.prodMk (measurable_frameResponse state.domain state.range
    measurable_const hx measurable_const)
  have hh : Measurable h := measurable_fst.comp state.law.measurable
  refine ⟨state.domain.comp measurable_fst,state.range.comp measurable_fst,state.ambient,?_,state.reconstruct⟩
  apply (state.law.map_history he).congr_ae (hh.prodMk ((measurable_response b).comp
    (state.ambient.prodMk (hx.comp hh)))) (measurable_snd.comp state.law.measurable) _ Filter.EventuallyEq.rfl
  filter_upwards [hc,state.reconstruct] with ω hcω hω
  refine Prod.ext ?_ ?_
  · rfl
  change frameResponse (F (h ω)) b (x (h ω)) (coordinatePoint 0) = response b (A ω) (x (h ω))
  rw [hω,frameResponse_zero _ _ _ hcω _ (frameObservation (F (h ω)) b (x (h ω)) (W ω))]
  cases b
  · exact (frameAnswer_eq (F (h ω)) false (x (h ω)) (W ω)).symm
  · exact (frameAnswer_eq (F (h ω)) true (x (h ω)) (W ω)).symm

#print axioms HaarState.informative
#print axioms HaarState.determined
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
