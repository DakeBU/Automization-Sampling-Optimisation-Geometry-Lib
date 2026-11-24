import GCCIntrinsicEndpoint
import GCCProjectorUpdate

/-! The exact projector of the updated subspace on every potential history. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond
variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {N : ℕ}
  {μ : Measure Ω} [IsFiniteMeasure μ] {A : Ω → O N} {h : Ω → H}

/-- With an actual forward image or inverse image as the new observation, the
new subspace is the literal source span on every history and its action is
history-measurable and agrees almost surely with the sampled orthogonal matrix. -/
theorem IntrinsicState.exact_update (V : H → Submodule ℝ (E N)) (T : H → Mat N)
    (st : IntrinsicState μ h A (fun a => (projectionMatrix (V a),T a)))
    (known : ∀ᵐ ω ∂μ, (A ω).val * projectionMatrix (V (h ω)) = T (h ω))
    (back : Bool) {x : H → Vec N} (hx : Measurable x) :
    ∃ T' : H × Vec N → Mat N,
      IntrinsicState μ (observedHistory h A back x) A
        (fun p => (projectionMatrix (updatedSubspace V back x p),T' p)) ∧
      ∀ᵐ ω ∂μ, let p := observedHistory h A back x ω
        (A ω).val * projectionMatrix (updatedSubspace V back x p) = T' p := by
  obtain ⟨ob,hs,he⟩ := st.reveal V T known back hx
  have q : Measurable (fun p : H × Vec N => WithLp.toLp 2 (if back then p.2 else x p.1)) := by
    have m : Measurable (fun p : H × Vec N => if back then p.2 else x p.1) := by
      cases back
      · exact hx.comp measurable_fst
      · exact measurable_snd
    exact (PiLp.continuous_toLp 2 (fun _ : Fin N => ℝ)).measurable.comp m
  have hP := measurable_projection_sup_line (fun p : H × Vec N => V p.1)
    ((measurable_fst.comp st.observable).comp measurable_fst) _ q
  have eP : ∀ᵐ p ∂μ.map (observedHistory h A back x),
      (ob p).1 = projectionMatrix (updatedSubspace V back x p) := by
    apply (ae_map_iff hs.history.aemeasurable (measurableSet_eq_fun (measurable_fst.comp hs.observable) hP)).mpr
    filter_upwards [he] with ω e using congrArg Prod.fst e
  refine ⟨fun p => (ob p).2,⟨hs.history,hs.ambient,hP.prodMk (measurable_snd.comp hs.observable),?_⟩,?_⟩
  · filter_upwards [hs.law,eP] with a ha ea
    exact ha.trans (congrArg intrinsicCompletion (Prod.ext ea rfl))
  · filter_upwards [he] with ω e using (congrArg Prod.snd e).symm

#print axioms IntrinsicState.exact_update
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
