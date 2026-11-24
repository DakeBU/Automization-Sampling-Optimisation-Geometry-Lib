import GCCHaarStateRevelation
import GCCSubspaceImage

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private theorem euclidean_span {N : ℕ} {D D' : O N} {r r' : ℕ} {u : Vec N}
    (he : exposedSpace D' r' = exposedSpace D r ⊔ ℝ ∙ u) :
    exposedEuclidean D' r' = exposedEuclidean D r ⊔ ℝ ∙ (WithLp.toLp 2 u) := by
  let e := (WithLp.linearEquiv 2 ℝ (Vec N)).symm
  have h (A : O N) (s : ℕ) : (exposedSpace A s).map e.toLinearMap = exposedEuclidean A s :=
    Submodule.map_equiv_eq_comap_symm e _
  rw [← h,he,Submodule.map_sup,h,Submodule.map_span,Set.image_singleton]
  rfl

private theorem sends_revealed {N : ℕ} (A : O N) (b : Bool) (x : Vec N) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) A.val (WithLp.toLp 2 (if b then response b A x else x)) =
      WithLp.toLp 2 (if b then x else response b A x) := by
  cases b
  · rfl
  · change WithLp.toLp 2 (act A (act A⁻¹ x)) = WithLp.toLp 2 x
    rw [← act_mul,mul_inv_cancel]
    exact congrArg (WithLp.toLp 2) (Matrix.one_mulVec _)

/-- After observing the actual image or preimage, the remaining law is Haar, and its
domain and range are exactly the old unknown subspaces intersected with the two
new perpendicular hyperplanes. This permits random ranks and determined queries. -/
theorem TaggedState.actual_perpendicular_restriction {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
    {μ : Measure Ω} [IsFiniteMeasure μ] {N : ℕ} {A : Ω → O N} {h : Ω → H}
    {F : H → PublicFrame N} (st : TaggedState μ h A F) (b : Bool) {x : H → Vec N} (hx : Measurable x) :
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
  obtain ⟨after,growth⟩ := st.reveal_ambient b hx
  refine ⟨after,?_⟩
  filter_upwards [st.realizes,after.realizes,growth] with ω ho hn hg
  let G := F (h ω)
  let v := x (h ω)
  let y := response b (A ω) v
  let G' := nextPublic G b v y
  obtain ⟨w,hw⟩ : IsRealized G (A ω) := ho
  obtain ⟨w',hw'⟩ : IsRealized G' (A ω) := hn
  have dom := euclidean_span hg
  have eqv := completion_perpendicular_restriction G.2 G'.2 w w' (hw'.symm.trans hw)
    (WithLp.toLp 2 (if b then y else v)) dom
  dsimp only at eqv
  rw [← hw,sends_revealed] at eqv
  exact eqv

#print axioms TaggedState.actual_perpendicular_restriction
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
