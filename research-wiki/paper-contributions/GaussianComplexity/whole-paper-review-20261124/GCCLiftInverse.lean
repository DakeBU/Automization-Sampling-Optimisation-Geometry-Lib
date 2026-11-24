import GCCProjectionGeometry

noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

/-- Reading the coordinates of a lifted residual unit recovers that same sphere point. -/
theorem frameUnit_residualLift {N m : ℕ} [NeZero m] (F : BlockFrame N m) (b : Bool) (z : S m) :
    frameUnit F b (residualLift (queryFrame b F.domain F.range) F.rank F.fits z) = z := by
  rcases F with ⟨r,e,D,R⟩; subst N
  let J := queryFrame b D R
  change unitOrFirst (WithLp.toLp 2 (residualCoords m r
    (act J⁻¹ (act J (splitVec r 0 (1 • z.val.ofLp)))))) = z
  rw [one_smul,act_inv_act,residualCoords_splitVec]
  have hz := mem_sphere_zero_iff_norm.mp z.property
  have hs := scaled_unitOrFirst z.val
  rw [hz,one_smul] at hs
  exact Subtype.ext ((WithLp.equiv 2 (Vec m)).injective hs)

/-- Every unit vector in the actual ambient complement is recovered by lifting the
frame coordinates that the algorithm computes from that vector. -/
theorem residualLift_frameUnit_eq {N m : ℕ} [NeZero m] (F : BlockFrame N m) (b : Bool) (x : Vec N)
    (hx : ‖WithLp.toLp 2 x‖ = 1)
    (hK : WithLp.toLp 2 x ∈ (exposedEuclidean (queryFrame b F.domain F.range) F.rank)ᗮ) :
    residualLift (queryFrame b F.domain F.range) F.rank F.fits (frameUnit F b x) = x := by
  rcases F with ⟨r,e,D,R⟩; subst N
  let J := queryFrame b D R
  let G : BlockFrame (m+r) m := ⟨r,rfl,J,J⟩
  let K := exposedEuclidean J r
  let c := queryComplement (m := m) (r := r) J x
  let z := unitOrFirst c
  have hK' : WithLp.toLp 2 x ∈ Kᗮ := hK
  have h0 : K.starProjection (WithLp.toLp 2 x) = 0 :=
    K.starProjection_apply_eq_zero_iff.mpr hK'
  have hc1 : ‖c‖ = 1 := by
    have h := (knownPreimage_projection G 1 x).2
    change ‖c‖ = ‖Kᗮ.starProjection (WithLp.toLp 2 x)‖ at h
    rwa [Kᗮ.starProjection_eq_self_iff.mpr hK',hx] at h
  have hk : knownPreimage G x = 0 := by
    have h := (knownPreimage_projection G 1 x).1
    change knownPreimage G x = response true _ (K.starProjection (WithLp.toLp 2 x)).ofLp at h
    rw [h0] at h
    exact h.trans (by simp [response,act])
  have hr : frameResponse G true x z = x := by
    change act J (splitVec r (exposedCoords m r (act J⁻¹ x)) (‖c‖ • (unitOrFirst c).val.ofLp)) = x
    rw [scaled_unitOrFirst]
    exact query_from_coordinates J x
  have h := frameResponse_preimage G x z
  change frameResponse G true x z = knownPreimage G x + ‖c‖ • residualLift J r rfl z at h
  rw [hr,hk,hc1,one_smul,zero_add] at h
  exact h.symm

theorem exists_residualLift_eq_of_unit_complement {N m : ℕ} [NeZero m] (F : BlockFrame N m)
    (b : Bool) (x : Vec N) (hx : ‖WithLp.toLp 2 x‖ = 1)
    (hK : WithLp.toLp 2 x ∈ (exposedEuclidean (queryFrame b F.domain F.range) F.rank)ᗮ) :
    ∃ z : S m, residualLift (queryFrame b F.domain F.range) F.rank F.fits z = x :=
  ⟨frameUnit F b x,residualLift_frameUnit_eq F b x hx hK⟩

#print axioms frameUnit_residualLift
#print axioms residualLift_frameUnit_eq
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
