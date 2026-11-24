import GCCAdaptiveRevelation
import GCCTaggedAuxiliary
import GCCTaggedGeometry
import GCCTaggedDirection
/-! Arbitrary adaptive Haar state updates, the actual ambient returned vectors
and the uniform conditional law of the normalized preimage in Fact C.3. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {N : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

theorem physical_preimage_eq (G : PublicFrame N) (a : O N) (x : Vec N) :
    let K := exposedEuclidean G.2.range G.2.rank
    response true a x = response true a (K.starProjection (WithLp.toLp 2 x)).ofLp +
      ‖physicalComponent G x‖ • (physicalDirection G a x).ofLp := by
  let K := exposedEuclidean G.2.range G.2.rank
  let u := K.starProjection (WithLp.toLp 2 x)
  let v := physicalComponent G x
  have sum : u.ofLp + v.ofLp = x := congrArg WithLp.ofLp (K.starProjection_add_starProjection_orthogonal (WithLp.toLp 2 x))
  have scale : ‖v‖ • (‖v‖⁻¹ • response true a v.ofLp) = response true a v.ofLp := by
    by_cases e : v = 0
    · simp [e,response,act]
    · simp [smul_smul,e]
  change a⁻¹.val *ᵥ x = a⁻¹.val *ᵥ u.ofLp + ‖v‖ • (‖v‖⁻¹ • response true a v.ofLp)
  rw [scale]
  exact (congrArg (a⁻¹.val.mulVec) sum.symm).trans (Matrix.mulVec_add _ _ _)

theorem TaggedState.physical_preimage_uniform {G : H → PublicFrame N} (st : TaggedState μ h A G)
    {v : H → Vec N} (hv : Measurable v) :
    ∀ᵐ a ∂μ.map h, physicalComponent (G a) (v a) ≠ 0 →
      condDistrib (fun ω => physicalDirection (G (h ω)) (A ω) (v (h ω))) h μ a =
        complementSphere (exposedEuclidean (G a).2.domain (G a).2.rank) := by
  have e : (fun ω => direction (G (h ω)) (A ω) (v (h ω))) =ᵐ[μ]
      (fun ω => physicalDirection (G (h ω)) (A ω) (v (h ω))) := by
    filter_upwards [st.realizes] with ω hw
    obtain ⟨w,ew⟩ := hw
    rw [ew]
    exact direction_projection (G (h ω)) w (v (h ω))
  have same := condDistrib_congr (mβ := inferInstance) (X := h) e Filter.EventuallyEq.rfl
  filter_upwards [st.preimage_uniform_complement hv] with a law
  intro ne
  rw [← same]
  apply law
  have size : residualSize (G a) (v a) = ‖physicalComponent (G a) (v a)‖ :=
    (knownPreimage_projection (G a).2 1 (v a)).2
  rw [size]; exact norm_ne_zero_iff.mpr ne

/-- One physical revelation in both senses for a random residual dimension.
The returned vector is the only new element of the old history. -/
theorem TaggedState.reveal_ambient {F : H → PublicFrame N} (st : TaggedState μ h A F)
    (b : Bool) {v : H → Vec N} (hv : Measurable v) :
    TaggedState μ (fun ω => (h ω,response b (A ω) (v (h ω)))) A (postFrame F b v) ∧
    (∀ᵐ ω ∂μ, let G := F (h ω)
      let y := response b (A ω) (v (h ω))
      let G' := nextPublic G b (v (h ω)) y
      exposedSpace G'.2.domain G'.2.rank = exposedSpace G.2.domain G.2.rank ⊔
        Submodule.span ℝ {if b then y else v (h ω)}) :=
  ⟨st.update b hv,st.exposed_update b v⟩

#print axioms TaggedState.auxiliary
#print axioms TaggedState.reveal_ambient
#print axioms TaggedState.physical_preimage_uniform
#print axioms physical_preimage_eq

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
