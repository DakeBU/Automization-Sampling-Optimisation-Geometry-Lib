import GCCCompletionLaw
import GCCTaggedLocal

/-! Observable projector and partial-map formulation of a Haar state. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

local instance matrixMeasurable (N : ℕ) : MeasurableSpace (Mat N) := borel _
local instance matrixBorel (N : ℕ) : BorelSpace (Mat N) := ⟨rfl⟩
local instance matrixSecond (N : ℕ) : SecondCountableTopology (Mat N) :=
  inferInstanceAs (SecondCountableTopology (Fin N → Fin N → ℝ))

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {N m : ℕ}
  {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}
  {obs : H → Mat N × Mat N}

/-- The defining conditional isometry law is a property of two history-observable matrices.
The first matrix is an orthogonal projection and the second is the known partial action. -/
structure IntrinsicState (μ : Measure Ω) [IsFiniteMeasure μ] (h : Ω → H) (A : Ω → O N)
    (obs : H → Mat N × Mat N) : Prop where
  history : Measurable h
  ambient : Measurable A
  observable : Measurable obs
  law : ∀ᵐ a ∂μ.map h, condDistrib A h μ a = intrinsicCompletion (obs a)

theorem intrinsicState_iff_taggedState {F : H → PublicFrame N}
    (hF : Measurable F) (hp : Measurable obs)
    (he : ∀ᵐ a ∂μ.map h, observationOf (F a).2 = obs a) :
    IntrinsicState μ h A obs ↔ TaggedState μ h A F := by
  constructor
  · intro st
    refine ⟨st.history,st.ambient,hF,?_⟩
    filter_upwards [st.law,he] with a ha ea
    rw [ha,← ea,intrinsicCompletion_eq]
    rfl
  · intro st
    refine ⟨st.history,st.ambient,hp,?_⟩
    filter_upwards [st.law,he] with a ha ea
    rw [← ea,intrinsicCompletion_eq]
    exact ha

/-- In every history-measurable fixed-rank chart, reading the actual ambient matrix gives
a residual Haar matrix independent of the history, and realizes the ambient matrix again. -/
theorem IntrinsicState.readResidual {F : H → BlockFrame N m} (st : IntrinsicState μ h A obs)
    (hf : Measurable F) (he : ∀ᵐ a ∂μ.map h, observationOf (F a) = obs a) :
    HaarState μ h A F (fun ω => readResidualAt m ⟨m,F (h ω)⟩ (A ω)) :=
  ((intrinsicState_iff_taggedState (F := fun a => ⟨m,F a⟩)
    ((PublicFrame.measurable_tag m).comp hf) st.observable he).mp st).fixed

/-- The frames and their random ranks are jointly observable from the two source matrices. -/
theorem measurable_public_chart (V : H → Submodule ℝ (E N)) (B : H → O N)
    (hP : Measurable (fun a => projectionMatrix (V a)))
    (hT : Measurable (fun a => (B a).val * projectionMatrix (V a))) :
    ∃ F : H → PublicFrame N, Measurable F ∧ ∀ a,
      (F a).2.rank = Module.finrank ℝ (V a) ∧
      observationOf (F a).2 = (projectionMatrix (V a),(B a).val * projectionMatrix (V a)) := by
  obtain ⟨p,hp,ep⟩ := measurable_frames_all_ranks V B hP hT
  let k (a : H) : Fin (N+1) := ⟨Module.finrank ℝ (V a),by
    have hh := (V a).finrank_le
    rw [finrank_euclideanSpace_fin] at hh
    omega⟩
  have hk : Measurable k := by
    have hs : Measurable (fun x : ℕ => Fin.ofNat (N+1) x) := Measurable.of_discrete
    convert hs.comp (measurable_finrank V hP) using 1
    funext a
    apply Fin.ext
    exact (Nat.mod_eq_of_lt (k a).isLt).symm
  let mk (i : Fin (N+1)) (a : H) : PublicFrame N :=
    ⟨N-i.val,⟨i.val,by omega,(p a).1,(p a).2⟩⟩
  have hi (i : Fin (N+1)) : Measurable (mk i) :=
    (PublicFrame.measurable_tag _).comp
      (PublicFrame.measurable_blockFrame (measurable_fst.comp hp) (measurable_snd.comp hp))
  have hm : Measurable (fun b : Fin (N+1) × H => mk b.1 b.2) :=
    measurable_from_prod_countable_right hi
  exact ⟨fun a => mk (k a) a,hm.comp (hk.prodMk measurable_id),fun a => ⟨rfl,ep a⟩⟩

/-- For the coordinate-free conditional law in Definition C.2, a history-measurable
variable-rank Haar state exists with precisely the given exposed map. -/
theorem IntrinsicState.exists_taggedState (V : H → Submodule ℝ (E N)) (B : H → O N)
    (st : IntrinsicState μ h A (fun a => (projectionMatrix (V a),(B a).val * projectionMatrix (V a)))) :
    ∃ F : H → PublicFrame N, TaggedState μ h A F ∧ ∀ a,
      (F a).2.rank = Module.finrank ℝ (V a) ∧
      observationOf (F a).2 = (projectionMatrix (V a),(B a).val * projectionMatrix (V a)) := by
  obtain ⟨F,hF,he⟩ := measurable_public_chart V B (measurable_fst.comp st.observable)
    (measurable_snd.comp st.observable)
  exact ⟨F,(intrinsicState_iff_taggedState hF st.observable (ae_of_all _ fun a => (he a).2)).mp st,he⟩

#print axioms IntrinsicState.readResidual
#print axioms IntrinsicState.exists_taggedState
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
