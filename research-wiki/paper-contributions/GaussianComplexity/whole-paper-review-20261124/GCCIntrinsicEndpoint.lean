import GCCIntrinsicSelection
import GCCHaarStateRevelation

/-! A history with known action on a random subspace remains a Haar state after
sampling an independent auxiliary variable or observing an actual image or preimage. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
attribute [local instance] matrixMeasurable matrixBorel matrixSecond

variable {Ω H Z : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace Z]
    {N : ℕ} {h : Ω → H} {A : Ω → O N}

theorem IntrinsicState.auxiliary {μ : Measure Ω} [IsProbabilityMeasure μ]
    {obs : H → Mat N × Mat N} (st : IntrinsicState μ h A obs)
    {z : Ω → Z} (hz : Measurable z) (hi : IndepFun (fun ω => (h ω,A ω)) z μ) :
    IntrinsicState μ (fun ω => (h ω,z ω)) A (fun p : H × Z => obs p.1) := by
  refine ⟨st.history.prodMk hz,st.ambient,st.observable.comp measurable_fst,?_⟩
  have ih : IndepFun h z μ := hi.comp measurable_fst measurable_id
  let := Measure.isProbabilityMeasure_map hz.aemeasurable (μ := μ)
  have hpair := ih.map_prod_eq_prod_map_map st.history.aemeasurable hz.aemeasurable
  have hold : ∀ᵐ p ∂μ.map (fun ω => (h ω,z ω)),
      condDistrib A h μ p.1 = intrinsicCompletion (obs p.1) := by
    rw [hpair]
    exact (measurePreserving_fst (μ := μ.map h) (ν := μ.map z)).quasiMeasurePreserving.ae st.law
  filter_upwards [condDistrib_independent_auxiliary st.history hz st.ambient hi,hold] with p hp ho
  exact hp.trans ho

def observedHistory (h : Ω → H) (A : Ω → O N) (back : Bool) (x : H → Vec N) (ω : Ω) :
    H × Vec N := (h ω,response back (A ω) (x (h ω)))

def updatedSubspace (V : H → Submodule ℝ (E N)) (back : Bool) (x : H → Vec N)
    (p : H × Vec N) : Submodule ℝ (E N) :=
  V p.1 ⊔ ℝ ∙ (WithLp.toLp 2 (if back then p.2 else x p.1))

private theorem euclidean_span_of_raw {D D' : O N} {r r' : ℕ} {u : Vec N}
    (he : exposedSpace D' r' = exposedSpace D r ⊔ ℝ ∙ u) :
    exposedEuclidean D' r' = exposedEuclidean D r ⊔ ℝ ∙ (WithLp.toLp 2 u) := by
  let e := (WithLp.linearEquiv 2 ℝ (Vec N)).symm
  have h (B : O N) (s : ℕ) : (exposedSpace B s).map e.toLinearMap = exposedEuclidean B s :=
    Submodule.map_equiv_eq_comap_symm e _
  rw [← h,he,Submodule.map_sup,h,Submodule.map_span,Set.image_singleton]
  rfl

variable {μ : Measure Ω} [IsFiniteMeasure μ]

/-- Given only the old exposed subspace and its observable partial action,
the two new observable matrices are versions of the projector on the exact
updated span and the sampled rotation restricted to that span. Their conditional
completion law is preserved for forward and inverse queries. -/
theorem IntrinsicState.reveal (V : H → Submodule ℝ (E N)) (T : H → Mat N)
    (st : IntrinsicState μ h A (fun a => (projectionMatrix (V a),T a)))
    (known : ∀ᵐ ω ∂μ, (A ω).val * projectionMatrix (V (h ω)) = T (h ω))
    (back : Bool) {x : H → Vec N} (hx : Measurable x) :
    ∃ obs : H × Vec N → Mat N × Mat N,
      IntrinsicState μ (observedHistory h A back x) A obs ∧
      ∀ᵐ ω ∂μ, let p := observedHistory h A back x ω
        let P := projectionMatrix (updatedSubspace V back x p)
        obs p = (P,(A ω).val*P) := by
  obtain ⟨F,hs,_,hd⟩ := st.select_chart V T known
  have hold := ae_of_ae_map st.history.aemeasurable hd
  obtain ⟨after,span⟩ := hs.reveal_ambient back hx
  let G := postFrame F back x
  let ob := fun p => observationOf (G p).2
  have ho : Measurable ob := (measurable_observationOf N).comp after.frame
  refine ⟨ob,(intrinsicState_iff_taggedState after.frame ho (Filter.Eventually.of_forall fun _ => rfl)).mpr after,?_⟩
  filter_upwards [span,after.ae_mem_range_realize,hold] with ω eSpan eMat eV
  let p := observedHistory h A back x ω
  have eg : exposedEuclidean (G p).2.domain (G p).2.rank = updatedSubspace V back x p := by
    have e := euclidean_span_of_raw eSpan
    exact e.trans (congrArg (fun K : Submodule ℝ (E N) => K ⊔ ℝ ∙
      (WithLp.toLp 2 (if back then p.2 else x p.1))) eV)
  have hP : (ob p).1 = projectionMatrix (updatedSubspace V back x p) :=
    (frameObservation_projection (G p).2.domain (G p).2.range (G p).2.rank).trans
      (congrArg projectionMatrix eg)
  change A ω ∈ range (G p).2.realize at eMat
  rw [range_realize_eq_compatible] at eMat
  change (A ω).val * (ob p).1 = (ob p).2 at eMat
  exact Prod.ext hP (eMat.symm.trans (congrArg ((A ω).val * ·) hP))

#print axioms IntrinsicState.auxiliary
#print axioms IntrinsicState.reveal
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
