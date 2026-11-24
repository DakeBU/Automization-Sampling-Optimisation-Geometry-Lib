import GCCIntrinsicSupport

/-! Conditional law of the restriction to the unexposed domain in Definition C.2. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory Set
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

attribute [local instance] matrixMeasurable matrixBorel matrixSecond
local instance matrixPolish (N : ℕ) : PolishSpace (Mat N) :=
  inferInstanceAs (PolishSpace (Fin N → Fin N → ℝ))

variable {Ω H X Y : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  [MeasurableSpace X] [MeasurableSpace Y] [StandardBorelSpace X] [Nonempty X]
  [StandardBorelSpace Y] [Nonempty Y] {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H}

/-- An observable transformation of a conditional random variable can use both
the conditioning history and the variable's value. -/
theorem condDistrib_history_map {x : Ω → X} (hh : Measurable h) (hx : Measurable x)
    (f : H × X → Y) (hf : Measurable f) :
    ∀ᵐ a ∂μ.map h, condDistrib (fun ω => f (h ω,x ω)) h μ a =
      (condDistrib x h μ a).map (fun u => f (a,u)) := by
  let κ := condDistrib x h μ
  let η := (Kernel.id ×ₖ κ).map f
  let hm : IsMarkovKernel η := Kernel.IsMarkovKernel.map _ hf
  have hslic (a : H) : Measurable (fun u => f (a,u)) := hf.comp measurable_prodMk_left
  have hη (a : H) : η a = (κ a).map (fun u => f (a,u)) := by
    ext s hs
    rw [show η a = _ from Kernel.map_apply _ hf a,Measure.map_apply hf hs,
      Kernel.id_prod_apply' _ _ (hf hs),Measure.map_apply (hslic a) hs]
    rfl
  let t : H × X → H × Y := fun p => (p.1,f p)
  have ht : Measurable t := measurable_fst.prodMk hf
  have hu := hh.prodMk hx
  have hj : μ.map (fun ω => (h ω,f (h ω,x ω))) = μ.map h ⊗ₘ η := by
    change μ.map (t ∘ (fun ω => (h ω,x ω))) = _
    rw [← Measure.map_map ht hu,← compProd_map_condDistrib hx.aemeasurable]
    ext s hs
    rw [Measure.map_apply ht hs,Measure.compProd_apply (ht hs),Measure.compProd_apply hs]
    apply lintegral_congr
    intro a
    rw [hη, Measure.map_apply (hslic a) (measurable_prodMk_left hs)]
    rfl
  have he := condDistrib_ae_eq_of_measure_eq_compProd h (hf.comp hu).aemeasurable hj
  filter_upwards [he] with a ha using ha.trans (hη a)

variable {N : ℕ} {A : Ω → O N} {obs : H → Mat N × Mat N}

/-- The matrix of the actual restriction to the unknown subspace, extended by zero
on the observed subspace. Here p.1 is the observed projector. -/
def restrictionMatrix {N : ℕ} (p : Mat N × Mat N) (U : O N) : Mat N := U.val * (1-p.1)

private theorem recover_matrix {p : Mat N × Mat N} {U : O N} (compatible : U.val*p.1 = p.2) :
    restrictionMatrix p U + p.2 = U.val := by
  rw [restrictionMatrix,mul_sub,mul_one,← compatible,sub_add_cancel]

private theorem determines_completion (p : Mat N × Mat N) {ν η : Measure (O N)}
    (hν : ∀ᵐ U ∂ν, U.val*p.1 = p.2) (hη : ∀ᵐ U ∂η, U.val*p.1 = p.2)
    (he : ν.map (restrictionMatrix p) = η.map (restrictionMatrix p)) : ν = η := by
  have hf : Measurable (restrictionMatrix p) := continuous_subtype_val.measurable.mul measurable_const
  have ha : Measurable (fun K : Mat N => K+p.2) := measurable_id.add_const _
  have e (γ : Measure (O N)) (hg : ∀ᵐ U ∂γ, U.val*p.1 = p.2) :
      (γ.map (restrictionMatrix p)).map (fun K => K+p.2) = γ.map Subtype.val := by
    rw [Measure.map_map ha hf]
    apply Measure.map_congr
    filter_upwards [hg] with U hU using recover_matrix hU
  have hsub : MeasurableEmbedding (Subtype.val : O N → Mat N) :=
    continuous_subtype_val.measurable.measurableEmbedding Subtype.val_injective
  apply hsub.map_injective
  rw [← e ν hν,← e η hη,he]

/-- Under the observed constraint T=AP, the intrinsic Haar state is equivalent to
the source's conditional law of the restriction A restricted to the complementary
subspace. The restriction is encoded as the ordinary matrix A(1-P). -/
theorem intrinsicState_iff_restriction_law (hh : Measurable h) (hA : Measurable A)
    (ho : Measurable obs)
    (realizable : ∀ᵐ a ∂μ.map h, ∃ F : PublicFrame N, observationOf F.2 = obs a)
    (known : ∀ᵐ ω ∂μ, (A ω).val * (obs (h ω)).1 = (obs (h ω)).2) :
    IntrinsicState μ h A obs ↔
      (∀ᵐ a ∂μ.map h, condDistrib (fun ω => restrictionMatrix (obs (h ω)) (A ω)) h μ a =
        (intrinsicCompletion (obs a)).map (restrictionMatrix (obs a))) := by
  let f (p : H × O N) := restrictionMatrix (obs p.1) p.2
  have hf : Measurable f := (continuous_subtype_val.measurable.comp measurable_snd).mul
    (measurable_const.sub (measurable_fst.comp (ho.comp measurable_fst)))
  have hm := condDistrib_history_map (μ := μ) hh hA f hf
  constructor
  · intro st
    filter_upwards [hm,st.law] with a e hs
    exact e.trans (congrArg (Measure.map (restrictionMatrix (obs a))) hs)
  · intro hr
    refine ⟨hh,hA,ho,?_⟩
    let valid (p : H × O N) := p.2.val * (obs p.1).1 = (obs p.1).2
    have hv : MeasurableSet {p | valid p} := measurableSet_eq_fun
      ((continuous_subtype_val.measurable.comp measurable_snd).mul
        (measurable_fst.comp (ho.comp measurable_fst))) (measurable_snd.comp (ho.comp measurable_fst))
    have hp : ∀ᵐ p ∂μ.map h ⊗ₘ condDistrib A h μ, valid p := by
      rw [compProd_map_condDistrib hA.aemeasurable]
      exact (ae_map_iff (hh.prodMk hA).aemeasurable hv).mpr known
    filter_upwards [Measure.ae_ae_of_ae_compProd hp,realizable,hm,hr] with a ha hac he hr'
    obtain ⟨F,hF⟩ := hac
    have hw := completionKernel_ae_compatible F.2
    change ∀ᵐ U ∂intrinsicCompletion (observationOf F.2), U.val*(observationOf F.2).1 = (observationOf F.2).2 at hw
    rw [hF] at hw
    exact determines_completion (obs a) ha hw (he.symm.trans hr')

#print axioms intrinsicState_iff_restriction_law
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
