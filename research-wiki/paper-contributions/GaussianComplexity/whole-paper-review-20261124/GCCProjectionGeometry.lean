import GCCIntrinsicPreimage
import GCCFrameChart

noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private def toIsometry {N : ℕ} (D : O N) : E N ≃ₗᵢ[ℝ] E N :=
  Unitary.linearIsometryEquiv
    (⟨Matrix.toEuclideanCLM (𝕜 := ℝ) D.val,
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)) D.property⟩ :
      unitary (E N →L[ℝ] E N))

private theorem iso_front_iff {N : ℕ} (D : O N) (r : ℕ) (y : E N) :
    toIsometry D y ∈ exposedEuclidean D r ↔ y ∈ front N r := by
  change (∀ i : Fin N, r ≤ i.val → act D⁻¹ (act D y.ofLp) i = 0) ↔ _
  rw [act_inv_act]
  rfl

/-- The first public matrix in the chart is literally the ambient orthogonal projector
onto the exposed domain. -/
theorem frameObservation_projection {N : ℕ} (D R : O N) (r : ℕ) :
    (MeasurableFrames.frameObservation r (D,R)).1 = projectionMatrix (exposedEuclidean D r) := by
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  let K := exposedEuclidean D r
  let L := front N r
  let I := toIsometry D
  have isoP (x : E N) : K.starProjection (I x) = I (L.starProjection x) := by
    apply Submodule.eq_starProjection_of_mem_orthogonal'
      ((iso_front_iff D r _).2 (L.orthogonalProjectionOnto x).property)
      (z := I (Lᗮ.starProjection x))
    · intro y hy
      obtain ⟨v,rfl⟩ := I.surjective y
      rw [I.inner_map_map]
      exact (Lᗮ.orthogonalProjectionOnto x).property v ((iso_front_iff D r v).1 hy)
    · rw [← map_add]; exact congrArg I (L.starProjection_add_starProjection_orthogonal x).symm
  apply M.injective
  change M (D.val * projectionMatrix L * D⁻¹.val) = M (projectionMatrix K)
  rw [map_mul,map_mul]
  change M D.val * M (M.symm L.starProjection) * M D⁻¹.val = M (M.symm K.starProjection)
  rw [M.apply_symm_apply,M.apply_symm_apply]
  ext y : 1
  let z := M D⁻¹.val y
  have hz : I z = y := by
    change WithLp.toLp 2 (act D (act D⁻¹ y.ofLp)) = y
    rw [← act_mul,mul_inv_cancel]
    exact congrArg (WithLp.toLp 2) (Matrix.one_mulVec _)
  change I (L.starProjection z) = K.starProjection y
  rw [← hz,isoP]

private theorem projection_formula {m : ℕ} (r : ℕ) (D : O (m+r)) (x : Vec (m+r)) :
    let K := exposedEuclidean D r
    let p := act D (splitVec r (exposedCoords m r (act D⁻¹ x)) (0 : Vec m))
    K.starProjection (WithLp.toLp 2 x) = WithLp.toLp 2 p ∧
      ‖Kᗮ.starProjection (WithLp.toLp 2 x)‖ = ‖queryComplement (m := m) (r := r) D x‖ := by
  dsimp only
  let p := act D (splitVec r (exposedCoords m r (act D⁻¹ x)) (0 : Vec m))
  let K := exposedEuclidean D r
  have hp : WithLp.toLp 2 p ∈ K := by
    apply (exposedSpace_iff D p).2
    simp only [p,act_inv_act,residualCoords_splitVec]
  cases m with
  | zero =>
    have h : residualCoords 0 r (act D⁻¹ x) = 0 := Subsingleton.elim _ _
    have hx : p = x := by simpa only [p,h] using query_from_coordinates D x
    have hP := K.starProjection_eq_self_iff.mpr hp
    change K.starProjection (WithLp.toLp 2 x) = WithLp.toLp 2 p ∧ _
    rw [← hx]
    refine ⟨hP,?_⟩
    change ‖Kᗮ.starProjection (WithLp.toLp 2 p)‖ = ‖queryComplement (m := 0) (r := r) D p‖
    rw [Submodule.starProjection_orthogonal_val,hP,sub_self,norm_zero]
    exact (norm_eq_zero.mpr (Subsingleton.elim _ _)).symm
  | succ n =>
    let F : BlockFrame (n+1+r) (n+1) := ⟨r,rfl,D,D⟩
    let c := queryComplement (m := n+1) (r := r) D x
    let z := unitOrFirst c
    let v := WithLp.toLp 2 (residualLift D r rfl z)
    have hz := residualLift_mem_unit_complement D r rfl z
    have hr : frameResponse F true x z = x := by
      change act D (splitVec r (exposedCoords (n+1) r (act D⁻¹ x)) (‖c‖ • (unitOrFirst c).val.ofLp)) = x
      rw [scaled_unitOrFirst]
      exact query_from_coordinates D x
    have hsplit : WithLp.toLp 2 x = WithLp.toLp 2 p + ‖c‖ • v := by
      exact congrArg (WithLp.toLp 2) (hr.symm.trans (frameResponse_preimage F x z))
    have hP : K.starProjection (WithLp.toLp 2 x) = WithLp.toLp 2 p :=
      Submodule.eq_starProjection_of_mem_orthogonal' hp (Kᗮ.smul_mem ‖c‖ hz.1) hsplit
    refine ⟨hP,?_⟩
    change ‖Kᗮ.starProjection (WithLp.toLp 2 x)‖ = ‖c‖
    rw [Submodule.starProjection_orthogonal_val,hP,hsplit,add_sub_cancel_left,norm_smul]
    change ‖‖c‖‖ * ‖WithLp.toLp 2 (residualLift D r rfl z)‖ = _
    rw [hz.2,norm_norm,mul_one]

/-- The known preimage in Equation (27) is the true inverse applied to the orthogonal
projection on the known range. Its scale is the norm of the complementary projection. -/
theorem knownPreimage_projection {N m : ℕ} (F : BlockFrame N m) (W : O m) (x : Vec N) :
    let K := exposedEuclidean F.range F.rank
    knownPreimage F x = response true (F.realize W) (K.starProjection (WithLp.toLp 2 x)).ofLp ∧
      ‖frameComplement F true x‖ = ‖Kᗮ.starProjection (WithLp.toLp 2 x)‖ := by
  rcases F with ⟨r,e,D,R⟩; subst N
  have hp := projection_formula r R x
  dsimp only at hp
  change act D (splitVec r (exposedCoords m r (act R⁻¹ x)) (0 : Vec m)) =
    act (framed D R W)⁻¹ (((exposedEuclidean R r).starProjection (WithLp.toLp 2 x)).ofLp) ∧ _
  rw [hp.1]
  exact ⟨(zero_residual_response D R W _).2.symm,hp.2.symm⟩

/-- Ambient Eq. (27) with its literal projector and the actual sampled isometry. -/
theorem HaarState.preimage_projection_decomposition {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
    {μ : Measure Ω} {h : Ω → H} {N m : ℕ} [NeZero m] {A : Ω → O N}
    {F : H → BlockFrame N m} {W : Ω → O m} (state : HaarState μ h A F W) (x : H → Vec N) :
    ∀ᵐ ω ∂μ, let K := exposedEuclidean (F (h ω)).range (F (h ω)).rank
      let v := WithLp.toLp 2 (x (h ω))
      response true (A ω) v.ofLp =
        response true (A ω) (K.starProjection v).ofLp +
          ‖Kᗮ.starProjection v‖ • normalizedPreimage (F (h ω)) (A ω) v.ofLp := by
  filter_upwards [state.preimage_decomposition x,state.reconstruct] with ω he hA
  have hg := knownPreimage_projection (F (h ω)) (W ω) (x (h ω))
  rw [← hA] at hg
  simpa only [hg.1,hg.2] using he

#print axioms frameObservation_projection
#print axioms knownPreimage_projection
#print axioms HaarState.preimage_projection_decomposition
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
