import GCCIntrinsicKernel

/-! An observed partial isometry constrains the actual global rotation. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond

theorem measurable_observationOf (N : ℕ) :
    Measurable (fun p : PublicFrame N => observationOf p.2) := by
  apply PublicFrame.measurable_of_fibers
  intro m
  have he : (fun F : BlockFrame N m => observationOf F) =
      fun F => frameObservation (N-m) (F.domain,F.range) := by
    funext F
    have h := F.fits
    have er : F.rank = N-m := by omega
    simp [observationOf,er]
  rw [he]
  exact continuous_frameObservation.measurable.comp
    (PublicFrame.measurable_domain_fixed.prodMk PublicFrame.measurable_range_fixed)

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] {N : ℕ}
  {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N} {F : H → PublicFrame N}

theorem TaggedState.ae_mem_range_realize (st : TaggedState μ h A F) :
    ∀ᵐ ω ∂μ, A ω ∈ range (F (h ω)).2.realize := by
  let ob := fun a => observationOf (F a).2
  have ho : Measurable ob := (measurable_observationOf N).comp st.frame
  let valid (p : H × O N) := p.2.val * (ob p.1).1 = (ob p.1).2
  have hv : MeasurableSet {p | valid p} :=
    measurableSet_eq_fun ((continuous_subtype_val.measurable.comp measurable_snd).mul
      (measurable_fst.comp (ho.comp measurable_fst))) (measurable_snd.comp (ho.comp measurable_fst))
  have hc : ∀ᵐ a ∂μ.map h, ∀ᵐ U ∂condDistrib A h μ a, valid (a,U) := by
    filter_upwards [st.law] with a ha
    rw [ha]
    have hh := completionKernel_ae_compatible (F a).2
    change ∀ᵐ U ∂intrinsicCompletion (observationOf (F a).2), _ at hh
    rwa [intrinsicCompletion_eq] at hh
  have hpair : ∀ᵐ p ∂(μ.map h ⊗ₘ condDistrib A h μ), valid p :=
    Measure.ae_compProd_of_ae_ae hv hc
  rw [compProd_map_condDistrib st.ambient.aemeasurable] at hpair
  filter_upwards [(ae_map_iff (st.history.prodMk st.ambient).aemeasurable hv).mp hpair] with ω hω
  rw [range_realize_eq_compatible]
  exact hω

/-- With no exposed subspace the intrinsic kernel returns the full group Haar law. -/
theorem completion_initial (N : ℕ) :
    completionKernel N (observationOf (BlockFrame.initial N)) = orthogonalHaar N := by
  change intrinsicCompletion _ = _
  rw [intrinsicCompletion_eq,completionInFrame]
  convert Measure.map_id (μ := orthogonalHaar N) using 1
  exact congrArg (fun f => (orthogonalHaar N).map f) (funext (BlockFrame.initial_realize N))

/-- At full exposure there is a unique ambient orthogonal extension. -/
theorem completion_full {N : ℕ} (F : BlockFrame N 0) :
    completionKernel N (observationOf F) = Measure.dirac (F.realize 1) := by
  change intrinsicCompletion _ = _
  rw [intrinsicCompletion_eq,completionInFrame,orthogonalHaar_zero,
    Measure.map_dirac' F.measurable_realize]

#print axioms TaggedState.ae_mem_range_realize
#print axioms completion_full
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
