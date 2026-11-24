import GCCTaggedState
open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
variable {Ω H Z X : Type*} [MeasurableSpace Ω] [MeasurableSpace H] [MeasurableSpace Z]
variable {μ : Measure Ω} [IsProbabilityMeasure μ] {h : Ω → H} {z : Ω → Z}
theorem condDistrib_independent_auxiliary [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
    {x : Ω → X} (hh : Measurable h) (hz : Measurable z) (hx : Measurable x)
    (hi : IndepFun (fun ω => (h ω,x ω)) z μ) :
    condDistrib x (fun ω => (h ω,z ω)) μ =ᵐ[μ.map (fun ω => (h ω,z ω))]
      Kernel.prodMkRight Z (condDistrib x h μ) := by
  have ih : IndepFun h z μ := hi.comp measurable_fst measurable_id
  have marg := ih.map_prod_eq_prod_map_map hh.aemeasurable hz.aemeasurable
  let K := condDistrib x h μ
  apply condDistrib_ae_eq_of_measure_eq_compProd (fun ω => (h ω,z ω)) hx.aemeasurable
  rw [marg]
  apply Measure.ext_prod₃'
  intro s t u hs ht hu
  let event := fun ω => ((h ω,z ω),x ω)
  have hm : Measurable event := (hh.prodMk hz).prodMk hx
  rw [Measure.map_apply hm ((hs.prod ht).prod hu),Measure.compProd_apply_prod (hs.prod ht) hu]
  have es : event ⁻¹' ((s ×ˢ t) ×ˢ u) = (fun ω => (h ω,x ω)) ⁻¹' (s ×ˢ u) ∩ z ⁻¹' t := by
    ext ω; change (_ ∧ _) ∧ _ ↔ (_ ∧ _) ∧ _; tauto
  rw [es,hi.measure_inter_preimage_eq_mul _ _ (hs.prod hu) ht,
    ← Measure.map_apply (hh.prodMk hx) (hs.prod hu), ← compProd_map_condDistrib hx.aemeasurable,
    Measure.compProd_apply_prod hs hu,← Measure.map_apply hz ht,← Measure.prod_restrict]
  change _ = ∫⁻ a, K a.1 u ∂((μ.map h).restrict s).prod ((μ.map z).restrict t)
  have hcoef : Measurable (fun p : H × Z => K p.1 u) := (K.measurable_coe hu).comp measurable_fst
  rw [lintegral_prod (fun p : H × Z => K p.1 u) hcoef.aemeasurable]
  simp only [lintegral_const,Measure.restrict_apply_univ]
  exact (lintegral_mul_const _ (K.measurable_coe hu)).symm

theorem TaggedState.auxiliary {N : ℕ} {A : Ω → O N} {F : H → PublicFrame N}
    (st : TaggedState μ h A F) (hz : Measurable z) (hi : IndepFun (fun ω => (h ω,A ω)) z μ) :
    TaggedState μ (fun ω => (h ω,z ω)) A (fun p : H × Z => F p.1) := by
  refine ⟨st.history.prodMk hz,st.ambient,st.frame.comp measurable_fst,?_⟩
  have ih : IndepFun h z μ := hi.comp measurable_fst measurable_id
  let := Measure.isProbabilityMeasure_map hz.aemeasurable (μ := μ)
  have hpair := ih.map_prod_eq_prod_map_map st.history.aemeasurable hz.aemeasurable
  have hold : ∀ᵐ p ∂μ.map (fun ω => (h ω,z ω)),
      condDistrib A h μ p.1 = (orthogonalHaar (F p.1).1).map (F p.1).2.realize := by
    rw [hpair]
    exact (measurePreserving_fst (μ := μ.map h) (ν := μ.map z)).quasiMeasurePreserving.ae st.law
  filter_upwards [condDistrib_independent_auxiliary st.history hz st.ambient hi,hold] with p hp ho
  exact hp.trans ho

#print axioms TaggedState.auxiliary
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
