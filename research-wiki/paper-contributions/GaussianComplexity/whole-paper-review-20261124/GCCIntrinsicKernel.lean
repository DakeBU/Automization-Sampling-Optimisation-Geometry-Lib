import GCCIntrinsicState

/-! The coordinate-free completion is a probability kernel on matrix observations. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond

private theorem measurable_on_cover {ι X Y : Type*} [Countable ι] [MeasurableSpace X]
    [MeasurableSpace Y] (t : ι → Set X) (ht : ∀ i, MeasurableSet (t i))
    (cover : ∀ x, ∃ i, x ∈ t i) {f : X → Y} (hf : ∀ i, Measurable ((t i).domRestrict f)) :
    Measurable f := by
  intro s hs
  have he : f ⁻¹' s = ⋃ i, Subtype.val '' ((t i).domRestrict f ⁻¹' s) := by
    ext x
    constructor
    · intro hx
      obtain ⟨i,hi⟩ := cover x
      exact mem_iUnion.mpr ⟨i,⟨⟨x,hi⟩,hx,rfl⟩⟩
    · intro hx
      obtain ⟨i,z,hz,rfl⟩ := mem_iUnion.mp hx
      exact hz
  rw [he]
  exact MeasurableSet.iUnion (fun i => (ht i).subtype_image (hf i hs))

instance intrinsicCompletion_probability {N : ℕ} (p : Mat N × Mat N) :
    IsProbabilityMeasure (intrinsicCompletion p) := by
  classical
  unfold intrinsicCompletion
  split
  · rename_i h
    let F := Classical.choose h
    let := (orthogonalHaar_spec F.1).1
    exact Measure.isProbabilityMeasure_map F.2.measurable_realize.aemeasurable
  · infer_instance

/-- The section-free law is Borel, including across changes of revealed dimension. -/
theorem measurable_intrinsicCompletion (N : ℕ) : Measurable (@intrinsicCompletion N) := by
  classical
  let S (i : Fin (N+1)) : Set (Mat N × Mat N) := range (@frameObservation N i.val)
  have hs (i) : MeasurableSet (S i) := (isCompact_range (continuous_frameObservation (N := N) (r := i.val))).isClosed.measurableSet
  have hvalid (i : Fin (N+1)) : Measurable ((S i).domRestrict (@intrinsicCompletion N)) := by
    let : MetricSpace (O N × O N) := TopologicalSpace.metrizableSpaceMetric _
    obtain ⟨b,hb,he⟩ := measurable_lift (@frameObservation N i.val) continuous_frameObservation
      ((↑) : S i → Mat N × Mat N) measurable_subtype_coe Subtype.property
    let F (z : S i) : BlockFrame N (N-i.val) := ⟨i.val,by omega,(b z).1,(b z).2⟩
    have hD : Measurable (fun z => (F z).domain) := measurable_fst.comp hb
    have hR : Measurable (fun z => (F z).range) := measurable_snd.comp hb
    let f := fun z => (F z).realize
    have hfn : Measurable (fun p : S i × O (N-i.val) => f p.1 p.2) :=
      measurable_realize_family (hD.comp measurable_fst) (hR.comp measurable_fst) measurable_snd
    let := (orthogonalHaar_spec (N-i.val)).1
    have heq : (S i).domRestrict intrinsicCompletion = kernel (orthogonalHaar (N-i.val)) f := by
      funext z
      change intrinsicCompletion z.val = _
      rw [← he z]
      exact (intrinsicCompletion_eq (F z)).trans (kernel_apply _ _ hfn z).symm
    rw [heq]
    exact Kernel.measurable _
  let t : Option (Fin (N+1)) → Set (Mat N × Mat N)
    | none => (⋃ i, S i)ᶜ
    | some i => S i
  apply measurable_on_cover t
  · intro j
    cases j with
    | none => exact (MeasurableSet.iUnion hs).compl
    | some i => exact hs i
  · intro z
    by_cases hz : z ∈ ⋃ i, S i
    · obtain ⟨i,hi⟩ := mem_iUnion.mp hz
      exact ⟨some i,hi⟩
    · exact ⟨none,hz⟩
  · intro j
    cases j with
    | some i => exact hvalid i
    | none =>
      have hconst : (t none).domRestrict intrinsicCompletion = fun _ => Measure.dirac 1 := by
        funext z
        apply dif_neg
        rintro ⟨F,hF⟩
        obtain ⟨m,r,hr,D,R⟩ := F
        apply z.property
        apply mem_iUnion.mpr
        exact ⟨⟨r,by omega⟩,(D,R),hF⟩
      rw [hconst]
      exact measurable_const

def completionKernel (N : ℕ) : Kernel (Mat N × Mat N) (O N) :=
  ⟨intrinsicCompletion,measurable_intrinsicCompletion N⟩

instance completionKernel_markov (N : ℕ) : IsMarkovKernel (completionKernel N) :=
  ⟨intrinsicCompletion_probability⟩

/-- On every valid matrix observation, the probability kernel gives full measure to
exactly compatible orthogonal extensions. -/
theorem completionKernel_ae_compatible {N m : ℕ} (F : BlockFrame N m) :
    ∀ᵐ A ∂completionKernel N (observationOf F),
      A.val * (observationOf F).1 = (observationOf F).2 := by
  change ∀ᵐ A ∂intrinsicCompletion (observationOf F), _
  rw [intrinsicCompletion_eq]
  have h : MeasurableSet {A : O N | A.val * (observationOf F).1 = (observationOf F).2} :=
    (isClosed_eq (continuous_subtype_val.mul continuous_const) continuous_const).measurableSet
  apply (ae_map_iff F.measurable_realize.aemeasurable h).mpr
  filter_upwards [] with W
  have hr := (mem_range_self W : F.realize W ∈ range F.realize)
  rw [range_realize_eq_compatible] at hr
  exact hr

#print axioms measurable_intrinsicCompletion
#print axioms completionKernel_ae_compatible
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
