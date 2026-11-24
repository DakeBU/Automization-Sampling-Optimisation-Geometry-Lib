import GCCActualRestriction
import GCCTwoSubspaces
import GCCHaarImage

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private def unitComponent {N : ℕ} (G : PublicFrame N) (b : Bool) (x : Vec N) : E N :=
  (exposedEuclidean (queryFrame b G.2.domain G.2.range) G.2.rank)ᗮ.starProjection (WithLp.toLp 2 x)

private def unitDirection {N : ℕ} (G : PublicFrame N) (b : Bool) (A : O N) (x : Vec N) : E N :=
  ‖unitComponent G b x‖⁻¹ • WithLp.toLp 2 (response b A (unitComponent G b x).ofLp)

/-- Both parts of Fact C.1 for the actual image or preimage of an observable unit
vector. The conditional distribution is the ambient uniform sphere on the opposite
space. Given the old history and that actual answer, the remaining isometry is Haar
between the old spaces intersected with the two perpendicular hyperplanes. Here the
common dimension of the two spaces may vary with history. -/
theorem TaggedState.unit_revelation {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
    {μ : Measure Ω} [IsFiniteMeasure μ] {N : ℕ} {A : Ω → O N} {h : Ω → H}
    {F : H → PublicFrame N} (st : TaggedState μ h A F) (b : Bool) {x : H → Vec N}
    (hx : Measurable x) (hu : ∀ᵐ a ∂μ.map h, ‖WithLp.toLp 2 (x a)‖ = 1 ∧
      WithLp.toLp 2 (x a) ∈ (exposedEuclidean (queryFrame b (F a).2.domain (F a).2.range) (F a).2.rank)ᗮ) :
    (∀ᵐ a ∂μ.map h, condDistrib (fun ω => WithLp.toLp 2 (response b (A ω) (x (h ω)))) h μ a =
      complementSphere (exposedEuclidean (queryFrame (!b) (F a).2.domain (F a).2.range) (F a).2.rank)) ∧
    TaggedState μ (fun ω => (h ω,response b (A ω) (x (h ω)))) A (postFrame F b x) ∧
    (∀ᵐ ω ∂μ, let G := F (h ω)
      let y := response b (A ω) (x (h ω))
      let G' := nextPublic G b (x (h ω)) y
      let u := WithLp.toLp 2 (if b then y else x (h ω))
      let v := WithLp.toLp 2 (if b then x (h ω) else y)
      (exposedEuclidean G'.2.domain G'.2.rank)ᗮ =
        (exposedEuclidean G.2.domain G.2.rank)ᗮ ⊓ (ℝ ∙ u)ᗮ ∧
      (exposedEuclidean G'.2.range G'.2.rank)ᗮ =
        (exposedEuclidean G.2.range G.2.rank)ᗮ ⊓ (ℝ ∙ v)ᗮ) := by
  refine ⟨?_,st.actual_perpendicular_restriction b hx⟩
  have hc : ∀ᵐ a ∂μ.map h, unitComponent (F a) b (x a) = WithLp.toLp 2 (x a) := by
    filter_upwards [hu] with a ha
    exact Submodule.starProjection_eq_self_iff.mpr ha.2
  have hh : Measurable h := st.history
  have es : (fun ω => unitDirection (F (h ω)) b (A ω) (x (h ω))) =ᵐ[μ]
      fun ω => WithLp.toLp 2 (response b (A ω) (x (h ω))) := by
    filter_upwards [ae_of_ae_map hh.aemeasurable hc,ae_of_ae_map hh.aemeasurable hu] with ω e c
    simp only [unitDirection,e,c.1,inv_one,one_smul,WithLp.ofLp_toLp]
  have eqv := condDistrib_congr (mβ := inferInstance) (X := h) es Filter.EventuallyEq.rfl
  have both : ∀ᵐ a ∂μ.map h, unitComponent (F a) b (x a) ≠ 0 →
      condDistrib (fun ω => unitDirection (F (h ω)) b (A ω) (x (h ω))) h μ a =
        complementSphere (exposedEuclidean (queryFrame (!b) (F a).2.domain (F a).2.range) (F a).2.rank) := by
    cases b
    · exact st.physical_image_uniform hx
    · exact st.physical_preimage_uniform hx
  filter_upwards [hc,hu,both] with a e ha law
  rw [← eqv]
  apply law
  rw [e]
  intro ez
  exact one_ne_zero (ha.1.symm.trans (norm_eq_zero.mpr ez))

#print axioms TaggedState.unit_revelation
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
