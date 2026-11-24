import GCCIntrinsicSupport
import GCCProjectionGeometry

/-! Select compatible frames directly from the two measured observations when
the second agrees almost surely with the sampled orthogonal matrix on the exposed space. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
attribute [local instance] matrixMeasurable matrixBorel matrixSecond

theorem projectionMatrix_injective {N : ℕ} :
    Function.Injective (@projectionMatrix N) := by
  intro V U he
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  have h := M.symm.injective he
  change V.starProjection = U.starProjection at h
  rw [← Submodule.range_starProjection V,← Submodule.range_starProjection U,h]

theorem compatible_at_rank {N : ℕ} (V : Submodule ℝ (E N)) (U : O N) :
    (projectionMatrix V,U.val*projectionMatrix V) ∈
      range (@MeasurableFrames.frameObservation N (Module.finrank ℝ V)) := by
  obtain ⟨p,_,he⟩ := measurable_frames_all_ranks (H := Unit) (fun _ => V) (fun _ => U)
    measurable_const measurable_const
  exact ⟨p (),he ()⟩

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {N : ℕ}
    {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

/-- Given the actual observable data, the state admits an adapted chart, with
its domain subspace and the known action recovered on all sampled histories.
No choice of an ambient extension is needed as input. -/
theorem IntrinsicState.select_chart (V : H → Submodule ℝ (E N)) (T : H → Mat N)
    (st : IntrinsicState μ h A (fun a => (projectionMatrix (V a), T a)))
    (hT : ∀ᵐ ω ∂μ, (A ω).val * projectionMatrix (V (h ω)) = T (h ω)) :
    ∃ F : H → PublicFrame N, TaggedState μ h A F ∧
      (∀ᵐ a ∂μ.map h, observationOf (F a).2 = (projectionMatrix (V a),T a)) ∧
      ∀ᵐ a ∂μ.map h, exposedEuclidean (F a).2.domain (F a).2.rank = V a := by
  classical
  let obs (a : H) := (projectionMatrix (V a),T a)
  have hp : Measurable obs := st.observable
  let k (a : H) : Fin (N+1) := ⟨Module.finrank ℝ (V a),by
    have hh := (V a).finrank_le
    rw [finrank_euclideanSpace_fin] at hh
    omega⟩
  have hk : Measurable k := by
    have hs : Measurable (fun x : ℕ => Fin.ofNat (N+1) x) := Measurable.of_discrete
    convert hs.comp (measurable_finrank V (measurable_fst.comp hp)) using 1
    funext a
    apply Fin.ext
    exact (Nat.mod_eq_of_lt (k a).isLt).symm
  let S (i : Fin (N+1)) := range (@MeasurableFrames.frameObservation N i.val)
  have hs (i) : MeasurableSet (S i) :=
    (isCompact_range (continuous_frameObservation (N := N) (r := i.val))).isClosed.measurableSet
  have branch (i : Fin (N+1)) : ∃ g : H → PublicFrame N, Measurable g ∧
      ∀ a, obs a ∈ S i → observationOf (g a).2 = obs a := by
    let s := obs ⁻¹' S i
    let : MetricSpace (O N × O N) := TopologicalSpace.metrizableSpaceMetric _
    obtain ⟨b,hb,he⟩ := measurable_lift (@MeasurableFrames.frameObservation N i.val) continuous_frameObservation
      (fun a : s => obs a) (hp.comp measurable_subtype_coe) Subtype.property
    let G (a : s) : BlockFrame N (N-i.val) := ⟨i.val,by omega,(b a).1,(b a).2⟩
    let F (a : H) : PublicFrame N := if hc : a ∈ s then ⟨_,G ⟨a,hc⟩⟩ else ⟨N,BlockFrame.initial N⟩
    refine ⟨F,measurable_of_restrict_of_restrict_compl (hp (hs i)) ?_ ?_,?_⟩
    · have eqn : s.domRestrict F = fun a : s => ⟨N-i.val,G a⟩ := funext fun a => dif_pos a.property
      rw [eqn]
      exact (PublicFrame.measurable_tag _).comp (PublicFrame.measurable_blockFrame
        (measurable_fst.comp hb) (measurable_snd.comp hb))
    · have eqn : sᶜ.domRestrict F = fun _ => ⟨N,BlockFrame.initial N⟩ := funext fun a => dif_neg a.property
      rw [eqn]; exact measurable_const
    · intro a ha
      change a ∈ s at ha
      have hf : F a = ⟨N-i.val,G ⟨a,ha⟩⟩ := dif_pos ha
      rw [hf]
      exact he ⟨a,ha⟩
  choose g hg eg using branch
  let F := fun a => g (k a) a
  have hmix : Measurable (fun p : Fin (N+1) × H => g p.1 p.2) := measurable_from_prod_countable_right hg
  have hF : Measurable F := hmix.comp (hk.prodMk measurable_id)
  have hobs : ∀ᵐ a ∂μ.map h, observationOf (F a).2 = obs a := by
    apply (ae_map_iff st.history.aemeasurable
      (measurableSet_eq_fun ((measurable_observationOf N).comp hF) hp)).mpr
    filter_upwards [hT] with ω e
    apply eg
    change (projectionMatrix (V (h ω)),T (h ω)) ∈ _
    rw [← e]
    exact compatible_at_rank (V (h ω)) (A ω)
  refine ⟨F,(intrinsicState_iff_taggedState hF hp hobs).mp st,hobs,?_⟩
  filter_upwards [hobs] with a e
  apply projectionMatrix_injective
  exact (frameObservation_projection (F a).2.domain (F a).2.range (F a).2.rank).symm.trans
    (congrArg Prod.fst e)

#print axioms IntrinsicState.select_chart
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
