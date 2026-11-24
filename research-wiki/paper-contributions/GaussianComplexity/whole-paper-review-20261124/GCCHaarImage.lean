import GCCHaarStateRevelation

/-! Transposing an arbitrary-history Haar state interchanges its known domain
and range. The new physical direction of an image revelation is uniformly
distributed on the actual unexposed range, even for changing ranks. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {N m : ℕ}

def swapFrame (F : BlockFrame N m) : BlockFrame N m := ⟨F.rank,F.fits,F.range,F.domain⟩

def swapPublic (G : PublicFrame N) : PublicFrame N := ⟨G.1,swapFrame G.2⟩

theorem measurable_swapPublic : Measurable (@swapPublic N) := by
  apply PublicFrame.measurable_of_fibers
  intro m
  apply (PublicFrame.measurable_tag m).comp
  exact PublicFrame.measurable_blockFrame (F := swapFrame) PublicFrame.measurable_range_fixed PublicFrame.measurable_domain_fixed

theorem inverse_realize (F : BlockFrame N m) (w : O m) : (F.realize w)⁻¹ = (swapFrame F).realize w⁻¹ := by
  rcases F with ⟨r,e,D,R⟩; subst N
  change (R * prefixEmbed m r w * D⁻¹)⁻¹ = D * prefixEmbed m r w⁻¹ * R⁻¹
  rw [map_inv]; group

theorem measurePreserving_full_inverse (m : ℕ) : MeasurePreserving (Inv.inv : O m → O m)
    (orthogonalHaar m) (orthogonalHaar m) := by
  refine ⟨measurable_inv,?_⟩
  rw [haar_as_components,Measure.map_smul,Measure.map_add _ _ measurable_inv,
    componentHaar_map_inv,componentHaar_map_inv]

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

theorem TaggedState.inverse {G : H → PublicFrame N} (st : TaggedState μ h A G) :
    TaggedState μ h (fun ω => (A ω)⁻¹) (fun a => swapPublic (G a)) := by
  refine ⟨st.history,st.ambient.inv,measurable_swapPublic.comp st.frame,?_⟩
  have hi : Measurable (Inv.inv : O N → O N) := measurable_inv
  have he := condDistrib_comp (mβ := inferInstance) (μ := μ) h st.ambient.aemeasurable hi
  filter_upwards [he,st.law] with a ha old
  let F := (G a).2
  change condDistrib (Inv.inv ∘ A) h μ a = (orthogonalHaar (G a).1).map (swapFrame F).realize
  rw [ha,Kernel.map_apply _ hi,old,Measure.map_map hi F.measurable_realize]
  have ee : (Inv.inv : O N → O N) ∘ F.realize = (swapFrame F).realize ∘ Inv.inv := funext (inverse_realize F)
  rw [ee,← Measure.map_map (swapFrame F).measurable_realize measurable_inv,(measurePreserving_full_inverse _).map_eq]

/-- Orthogonal component of the query on the unexposed domain before a forward revelation. -/
def imageComponent (G : PublicFrame N) (x : Vec N) : E N :=
  (exposedEuclidean G.2.domain G.2.rank)ᗮ.starProjection (WithLp.toLp 2 x)

/-- The actual unknown part of the forward response, normalized to have unit
length on its nonzero branch and equal to zero on the remaining histories. -/
def physicalImageDirection (G : PublicFrame N) (a : O N) (x : Vec N) : E N :=
  ‖imageComponent G x‖⁻¹ • WithLp.toLp 2 (response false a (imageComponent G x).ofLp)

theorem TaggedState.physical_image_uniform {G : H → PublicFrame N} (st : TaggedState μ h A G)
    {v : H → Vec N} (hv : Measurable v) :
    ∀ᵐ a ∂μ.map h, imageComponent (G a) (v a) ≠ 0 →
      condDistrib (fun ω => physicalImageDirection (G (h ω)) (A ω) (v (h ω))) h μ a =
        complementSphere (exposedEuclidean (G a).2.range (G a).2.rank) := by
  simpa only [physicalDirection,physicalImageDirection,physicalComponent,imageComponent,
    swapPublic,swapFrame,response,inv_inv,if_true,if_false,Bool.false_eq_true] using
    st.inverse.physical_preimage_uniform hv

#print axioms TaggedState.inverse
#print axioms TaggedState.physical_image_uniform
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
