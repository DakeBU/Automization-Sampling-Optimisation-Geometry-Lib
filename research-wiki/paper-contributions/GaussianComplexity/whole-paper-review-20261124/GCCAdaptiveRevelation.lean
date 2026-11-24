import GCCFixedUpdate
open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
noncomputable section
set_option maxHeartbeats 900000
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {N : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

/-- For any history-dependent rank and any measurable query, revealing the
actual image or preimage preserves the Haar-state conditional distribution.
Neither the rank nor the informative/determined branch needs to be constant. -/
theorem TaggedState.update {F : H → PublicFrame N} (st : TaggedState μ h A F)
    (b : Bool) {x : H → Vec N} (hx : Measurable x) :
    TaggedState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A (postFrame F b x) := by
  let y := fun ω => response b (A ω) (x (h ω))
  have hy : Measurable y := (measurable_response b).comp (st.ambient.prodMk (hx.comp st.history))
  let s := fun i : Fin (N+1) => {a | (F a).1 = i.val}
  have hs (i : Fin (N+1)) : MeasurableSet (s i) :=
    (PublicFrame.measurable_profile.comp st.frame) (measurableSet_singleton i.val)
  apply TaggedState.glue_first st.history hy st.ambient (measurable_postFrame st.frame b hx) s hs
  · intro a
    have e := (F a).2.fits
    exact ⟨⟨(F a).1, by omega⟩,rfl⟩
  · intro i
    have hi : i.val ≤ N := by omega
    let fixed := fun a => atRank i.val hi (F a)
    let tag := fun a => (⟨i.val,fixed a⟩ : PublicFrame N)
    have ht : Measurable tag := (PublicFrame.measurable_tag i.val).comp (measurable_atRank st.frame hi)
    have eqv {a} (ha : a ∈ s i) : tag a = F a := tag_atRank hi ha
    have localState := st.restrict_history (hs i)
    have eqtag : F =ᵐ[(μ.restrict (h ⁻¹' s i)).map h] tag := by
      rw [← Measure.restrict_map st.history (hs i)]
      filter_upwards [ae_restrict_mem (μ := μ.map h) (hs i)] with a ha using (eqv ha).symm
    have localized := (localState.congr_frame ht eqtag).fixed
    apply (localized.update b hx).congr_frame (measurable_postFrame st.frame b hx)
    filter_upwards [ae_post_mem st.history hy (hs i)] with p ep
    exact congrArg (fun f => nextPublic f b (x p.1) p.2) (eqv ep)

#print axioms TaggedState.update
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
