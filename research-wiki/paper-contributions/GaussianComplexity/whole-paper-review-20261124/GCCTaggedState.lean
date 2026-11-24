import GCCStateEndpoints
open MeasureTheory ProbabilityTheory Topology TopologicalSpace
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

instance orthogonalPolish (N : ℕ) : PolishSpace (O N) := by
  let := metrizableSpaceMetric (O N)
  infer_instance

variable {Ω H X : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace X]

private theorem restrict_compProd_first (ρ : Measure H) [SFinite ρ] (K : Kernel H X)
    [IsSFiniteKernel K] {s : Set H} (hs : MeasurableSet s) :
    (ρ ⊗ₘ K).restrict (Prod.fst ⁻¹' s) = ρ.restrict s ⊗ₘ K := by
  classical
  ext t ht
  rw [Measure.restrict_apply ht,Measure.compProd_apply (ht.inter (measurable_fst hs)),
    Measure.compProd_apply ht,← lintegral_indicator hs]
  apply lintegral_congr
  intro a
  by_cases ha : a ∈ s
  · have e : (Prod.mk a : X → H × X) ⁻¹' (Prod.fst ⁻¹' s) = Set.univ := by ext x; simp [ha]
    rw [Set.preimage_inter,e,Set.inter_univ,Set.indicator_of_mem ha]
  · have e : (Prod.mk a : X → H × X) ⁻¹' (Prod.fst ⁻¹' s) = ∅ := by ext x; simp [ha]
    rw [Set.preimage_inter,e,Set.inter_empty,measure_empty,Set.indicator_of_notMem ha]

theorem condDistrib_restrict_history [StandardBorelSpace X] [Nonempty X]
    {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {x : Ω → X}
    (hh : Measurable h) (hx : Measurable x) {s : Set H} (hs : MeasurableSet s) :
    condDistrib x h (μ.restrict (h ⁻¹' s)) =ᵐ[(μ.map h).restrict s] condDistrib x h μ := by
  rw [Measure.restrict_map hh hs]
  apply condDistrib_ae_eq_of_measure_eq_compProd h hx.aemeasurable
  have he : h ⁻¹' s = (fun ω => (h ω,x ω)) ⁻¹' (Prod.fst ⁻¹' s) := rfl
  rw [← Measure.restrict_map hh hs, ← restrict_compProd_first _ _ hs,compProd_map_condDistrib hx.aemeasurable,
    he,← Measure.restrict_map (hh.prodMk hx) (measurable_fst hs)]

variable {N m : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

/-- The ambient conditional law for an arbitrary measurable *random* residual
rank. Its right hand side is the uniform completion of the exposed map. -/
structure TaggedState (μ : Measure Ω) [IsFiniteMeasure μ] (h : Ω → H) (A : Ω → O N)
    (F : H → PublicFrame N) : Prop where
  history : Measurable h
  ambient : Measurable A
  frame : Measurable F
  law : ∀ᵐ a ∂μ.map h, condDistrib A h μ a = (orthogonalHaar (F a).1).map (F a).2.realize

theorem TaggedState.restrict_history {F : H → PublicFrame N} (st : TaggedState μ h A F)
    {s : Set H} (hs : MeasurableSet s) : TaggedState (μ.restrict (h ⁻¹' s)) h A F := by
  refine ⟨st.history,st.ambient,st.frame,?_⟩
  rw [← Measure.restrict_map st.history hs]
  exact (condDistrib_restrict_history st.history st.ambient hs).trans (ae_mono Measure.restrict_le_self st.law)

theorem TaggedState.congr_frame {F G : H → PublicFrame N} (st : TaggedState μ h A F)
    (hG : Measurable G) (he : F =ᵐ[μ.map h] G) : TaggedState μ h A G := by
  refine ⟨st.history,st.ambient,hG,?_⟩
  filter_upwards [st.law,he] with a ha ea
  rwa [← ea]

theorem TaggedState.glue {I : Type*} [Countable I]
    {F : H → PublicFrame N} (hh : Measurable h) (hA : Measurable A) (hF : Measurable F)
    (s : I → Set H) (hs : ∀ i, MeasurableSet (s i)) (cover : ∀ a, ∃ i, a ∈ s i)
    (localState : ∀ i, TaggedState (μ.restrict (h ⁻¹' s i)) h A F) :
    TaggedState μ h A F := by
  refine ⟨hh,hA,hF,?_⟩
  have each i : ∀ᵐ a ∂μ.map h, a ∈ s i → condDistrib A h μ a =
      (orthogonalHaar (F a).1).map (F a).2.realize := by
    apply (ae_restrict_iff' (hs i)).mp
    have e := (localState i).law
    rw [← Measure.restrict_map hh (hs i)] at e
    exact (condDistrib_restrict_history hh hA (hs i)).symm.trans e
  filter_upwards [ae_all_iff.mpr each] with a ha
  obtain ⟨i,hi⟩ := cover a
  exact ha i hi

theorem HaarState.tagged {F : H → BlockFrame N m} {W : Ω → O m} (st : HaarState μ h A F W) :
    TaggedState μ h A (fun a => ⟨m,F a⟩) := by
  let := (orthogonalHaar_spec m).1
  have hh : Measurable h := measurable_fst.comp st.law.measurable
  let sim := fun p : H × O m => (F p.1).realize p.2
  have hm : Measurable sim := measurable_realize_family (st.domain.comp measurable_fst) (st.range.comp measurable_fst) measurable_snd
  let f := fun a => (F a).realize
  let := isMarkovKernel_kernel (orthogonalHaar m) f hm
  have joint : μ.map (fun ω => (h ω,A ω)) = (μ.map h) ⊗ₘ kernel (orthogonalHaar m) f := by
    rw [← map_prod_eq_compProd _ _ _ hm,← st.law.map_eq,Measure.map_map (measurable_fst.prodMk hm) st.law.measurable]
    apply Measure.map_congr
    filter_upwards [st.reconstruct] with ω e using Prod.ext rfl e
  refine ⟨hh,st.ambient,(PublicFrame.measurable_tag m).comp (PublicFrame.measurable_blockFrame st.domain st.range),?_⟩
  filter_upwards [condDistrib_ae_eq_of_measure_eq_compProd h st.ambient.aemeasurable joint] with a ha
  exact ha.trans (kernel_apply _ _ hm a)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
