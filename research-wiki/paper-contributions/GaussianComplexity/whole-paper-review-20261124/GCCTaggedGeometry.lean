import GCCTaggedLocal
import GCCProjectionGeometry
import GCCSpanAll
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {N : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

def IsRealized (G : PublicFrame N) (A : O N) : Prop := ∃ w, A = G.2.realize w

set_option maxHeartbeats 900000 in
theorem TaggedState.realizes {G : H → PublicFrame N} (st : TaggedState μ h A G) :
    ∀ᵐ ω ∂μ, IsRealized (G (h ω)) (A ω) := by
  let s := fun i : Fin (N+1) => {a | (G a).1 = i.val}
  have hs (i : Fin (N+1)) : MeasurableSet (s i) :=
    (PublicFrame.measurable_profile.comp st.frame) (measurableSet_singleton i.val)
  have each (i : Fin (N+1)) : ∀ᵐ ω ∂μ, h ω ∈ s i → IsRealized (G (h ω)) (A ω) := by
    apply (ae_restrict_iff' (st.history (hs i))).mp
    have hi : i.val ≤ N := by omega
    let F := fun a => atRank i.val hi (G a)
    let tag := fun a => (⟨i.val,F a⟩ : PublicFrame N)
    have ht : Measurable tag := (PublicFrame.measurable_tag i.val).comp (measurable_atRank st.frame hi)
    have eqv {a} (ha : a ∈ s i) : tag a = G a := tag_atRank hi ha
    have eqtag : G =ᵐ[(μ.restrict (h ⁻¹' s i)).map h] tag := by
      rw [← Measure.restrict_map st.history (hs i)]
      filter_upwards [ae_restrict_mem (μ := μ.map h) (hs i)] with a ha using (eqv ha).symm
    have localized := ((st.restrict_history (hs i)).congr_frame ht eqtag).fixed
    filter_upwards [localized.reconstruct,ae_restrict_mem (μ := μ) (st.history (hs i))] with ω e hw
    rw [← eqv hw]
    exact ⟨_,e⟩
  filter_upwards [ae_all_iff.mpr each] with ω e
  have fit := (G (h ω)).2.fits
  exact e ⟨(G (h ω)).1,by omega⟩ rfl

/-- At every random residual rank, the new exposed subspace is the exact
linear span of the old exposed domain and the processed source vector. -/
theorem TaggedState.exposed_update {F : H → PublicFrame N} (st : TaggedState μ h A F)
    (b : Bool) (v : H → Vec N) : ∀ᵐ ω ∂μ,
    let G := F (h ω)
    let y := response b (A ω) (v (h ω))
    let G' := nextPublic G b (v (h ω)) y
    exposedSpace G'.2.domain G'.2.rank = exposedSpace G.2.domain G.2.rank ⊔
      Submodule.span ℝ {if b then y else v (h ω)} := by
  filter_upwards [st.realizes] with ω hw
  obtain ⟨w,e⟩ := hw
  rw [e]
  exact nextPublic_exposed_eq _ w b _

def physicalComponent (G : PublicFrame N) (x : Vec N) : E N :=
  (exposedEuclidean G.2.range G.2.rank)ᗮ.starProjection (WithLp.toLp 2 x)

def physicalDirection (G : PublicFrame N) (A : O N) (x : Vec N) : E N :=
  ‖physicalComponent G x‖⁻¹ • WithLp.toLp 2 (response true A (physicalComponent G x).ofLp)

theorem direction_projection (G : PublicFrame N) (w : O G.1) (x : Vec N) :
    WithLp.toLp 2 (normalizedPreimage G.2 (G.2.realize w) x) = physicalDirection G (G.2.realize w) x := by
  let K := exposedEuclidean G.2.range G.2.rank
  let t := WithLp.toLp 2 x
  have hg := knownPreimage_projection G.2 w x
  have hs := K.starProjection_add_starProjection_orthogonal t
  have he : x - (K.starProjection t).ofLp = (Kᗮ.starProjection t).ofLp := by
    apply sub_eq_iff_eq_add.mpr
    have e : (K.starProjection t).ofLp + (Kᗮ.starProjection t).ofLp = x := congrArg WithLp.ofLp hs
    rw [add_comm]; exact e.symm
  apply WithLp.ofLp_injective
  change ‖frameComplement G.2 true x‖⁻¹ •
    (response true (G.2.realize w) x - knownPreimage G.2 x) =
      ‖Kᗮ.starProjection t‖⁻¹ • response true (G.2.realize w) (Kᗮ.starProjection t).ofLp
  rw [hg.1,hg.2]
  apply congrArg (fun a : Vec N => ‖Kᗮ.starProjection t‖⁻¹ • a)
  let M := ((G.2.realize w)⁻¹ : O N).val
  change M *ᵥ x - M *ᵥ (K.starProjection t).ofLp = M *ᵥ (Kᗮ.starProjection t).ofLp
  rw [← Matrix.mulVec_sub,he]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
