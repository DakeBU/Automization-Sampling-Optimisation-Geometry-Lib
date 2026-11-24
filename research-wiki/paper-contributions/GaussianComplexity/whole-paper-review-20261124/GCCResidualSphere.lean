import GCCResidualLift
import GCCExposedRank
import GCFinishDirection

/-! Intrinsic uniform sphere law for the frame-coordinate residual direction. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

/-- The old domain as a Euclidean subspace, with the same underlying vectors
as the span of the first columns in the algorithm's raw coordinates. -/
def exposedEuclidean {N : ℕ} (D : O N) (r : ℕ) : Submodule ℝ (E N) :=
  (exposedSpace D r).comap (WithLp.linearEquiv 2 ℝ (Vec N)).toLinearMap

private def matrixIsometry {N : ℕ} (D : O N) : E N ≃ₗᵢ[ℝ] E N :=
  Unitary.linearIsometryEquiv
    (⟨Matrix.toEuclideanCLM (𝕜 := ℝ) D.val,
      Unitary.map_mem (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)) D.property⟩ :
      unitary (E N →L[ℝ] E N))

private theorem split_add {m : ℕ} (r : ℕ) (x y : Vec m) :
    splitVec r 0 (x+y) = splitVec r 0 x + splitVec r 0 y := by
  induction r with
  | zero => rfl
  | succ r ih =>
    funext i
    cases i using Fin.cases with
    | zero => simp [splitVec]
    | succ i => exact congrFun ih i

private theorem split_smul {m : ℕ} (r : ℕ) (s : ℝ) (x : Vec m) :
    splitVec r 0 (s • x) = s • splitVec r 0 x := by
  induction r with
  | zero => rfl
  | succ r ih =>
    funext i
    cases i using Fin.cases with
    | zero => simp [splitVec]
    | succ i => exact congrFun ih i

private theorem sum_tail {m : ℕ} (r : ℕ) (x : Vec m) :
    (∑ i, (splitVec r 0 x i)^2) = ∑ i, (x i)^2 := by
  induction r with
  | zero => rfl
  | succ r ih => exact (Fin.sum_univ_succ (fun i : Fin (m+r+1) => (splitVec (r+1) 0 x i)^2)).trans (by simpa [splitVec,show (fun _ : Fin r => (0:ℝ)) = (0:Vec r) from rfl] using ih)

private def tailIso (m r : ℕ) : E m →ₗᵢ[ℝ] E (m+r) where
  toFun x := WithLp.toLp 2 (splitVec r 0 x.ofLp)
  map_add' x y := congrArg (WithLp.toLp 2) (split_add r x.ofLp y.ofLp)
  map_smul' s x := congrArg (WithLp.toLp 2) (split_smul r s x.ofLp)
  norm_map' x := by
    change ‖WithLp.toLp 2 (splitVec r 0 x.ofLp)‖ = ‖x‖
    have h : ‖WithLp.toLp 2 (splitVec r 0 x.ofLp)‖^2 = ‖x‖^2 := by
      rw [EuclideanSpace.real_norm_sq_eq,EuclideanSpace.real_norm_sq_eq]
      exact sum_tail r x.ofLp
    nlinarith [norm_nonneg (WithLp.toLp 2 (splitVec r 0 x.ofLp)),norm_nonneg x]

private theorem split_orthogonal {m : ℕ} (r : ℕ) (a : Vec r) (c : Vec m) :
    inner ℝ (WithLp.toLp 2 (splitVec r a (0 : Vec m))) (tailIso m r (WithLp.toLp 2 c)) = 0 := by
  change (∑ i, inner ℝ (splitVec r a (0 : Vec m) i) (splitVec r 0 c i)) = 0
  induction r with
  | zero => simp [splitVec]
  | succ r ih =>
    apply (Fin.sum_univ_succ (fun i : Fin (m+r+1) => inner ℝ (splitVec (r+1) a (0 : Vec m) i) (splitVec (r+1) 0 c i))).trans
    simpa [splitVec,show (fun _ : Fin r => (0:ℝ)) = (0:Vec r) from rfl] using ih (fun i => a i.succ)

private def rotatedTail {m : ℕ} (r : ℕ) (D : O (m+r)) : E m →ₗᵢ[ℝ] E (m+r) :=
  (matrixIsometry D).toLinearIsometry.comp (tailIso m r)

private theorem rotatedTail_mem {m : ℕ} (r : ℕ) (D : O (m+r)) (z : E m) :
    rotatedTail r D z ∈ (exposedEuclidean D r)ᗮ := by
  intro y hy
  have hc := (exposedSpace_iff D y.ofLp).mp hy
  let a := exposedCoords m r (act D⁻¹ y.ofLp)
  have hy' : matrixIsometry D (WithLp.toLp 2 (splitVec r a (0 : Vec m))) = y := by
    apply (WithLp.equiv 2 (Vec (m+r))).injective
    change act D (splitVec r a 0) = y.ofLp
    simpa only [a,hc] using query_from_coordinates D y.ofLp
  change inner ℝ y (matrixIsometry D (tailIso m r z)) = 0
  rw [← hy',(matrixIsometry D).inner_map_map]
  exact split_orthogonal r a z.ofLp

private theorem euclidean_finrank {m : ℕ} (r : ℕ) (D : O (m+r)) :
    Module.finrank ℝ (exposedEuclidean D r) = r :=
  ((WithLp.linearEquiv 2 ℝ (Vec (m+r))).ofSubmodule' (exposedSpace D r)).finrank_eq.trans
    (exposedSpace_finrank (⟨r,rfl,D,D⟩ : BlockFrame (m+r) m))

private theorem range_rotatedTail {m : ℕ} (r : ℕ) (D : O (m+r)) :
    LinearMap.range (rotatedTail r D).toLinearMap = (exposedEuclidean D r)ᗮ := by
  apply Submodule.eq_of_le_of_finrank_le
  · rintro _ ⟨z,rfl⟩; exact rotatedTail_mem r D z
  · have h := (exposedEuclidean D r).finrank_add_finrank_orthogonal
    rw [finrank_euclideanSpace_fin,euclidean_finrank] at h
    rw [LinearMap.finrank_range_of_inj (rotatedTail r D).injective,finrank_euclideanSpace_fin]
    omega

private def complementIso {m : ℕ} (r : ℕ) (D : O (m+r)) :
    E m ≃ₗᵢ[ℝ] (exposedEuclidean D r)ᗮ :=
  (rotatedTail r D).equivRange.trans (LinearIsometryEquiv.ofEq _ _ (range_rotatedTail r D))

private theorem complementIso_apply {m : ℕ} (r : ℕ) (D : O (m+r)) (z : E m) :
    ((complementIso r D z : (exposedEuclidean D r)ᗮ) : E (m+r)) = rotatedTail r D z := rfl


private theorem rotate_realizes_isometry {m : ℕ} (u : E m ≃ₗᵢ[ℝ] E m) :
    ∃ D : O m, ∀ z : S m, (rotate D z).val = u z.val := by
  let U := Unitary.linearIsometryEquiv.symm u
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin m)
  let D : O m := ⟨M.symm U.val, Unitary.map_mem M.symm U.property⟩
  refine ⟨D,fun z => ?_⟩
  change M (M.symm U.val) z.val = u z.val
  rw [M.apply_symm_apply]
  rfl

private theorem sphere_map_congr_isometry {m n : ℕ} [NeZero m]
    {X : Type*} [NormedAddCommGroup X] [InnerProductSpace ℝ X] [MeasurableSpace X] [BorelSpace X]
    (i : E m ≃ₗᵢ[ℝ] X) (j : E n ≃ₗᵢ[ℝ] X) :
    (sphereProbability m).map (fun z : S m => i z.val) =
      (sphereProbability n).map (fun z : S n => j z.val) := by
  have he : m=n := by simpa only [finrank_euclideanSpace_fin] using (i.trans j.symm).toLinearEquiv.finrank_eq
  subst n
  obtain ⟨D,hD⟩ := rotate_realizes_isometry (i.trans j.symm)
  have h := measurePreserving_rotate (0 : Fin m) D
  have hm : Measurable (fun z : S m => j z.val) := (j.continuous.comp continuous_subtype_val).measurable
  calc
    _ = (sphereProbability m).map ((fun z : S m => j z.val) ∘ rotate D) := by
      congr 1; funext z
      simp only [Function.comp_apply,hD,LinearIsometryEquiv.trans_apply,j.apply_symm_apply]
    _ = _ := by rw [← Measure.map_map hm h.measurable, h.map_eq]

private theorem lift_isometry {m : ℕ} (r : ℕ) (D : O (m+r)) (z : S m) :
    WithLp.toLp 2 (residualLift D r rfl z) =
      ((complementIso r D z.val : (exposedEuclidean D r)ᗮ) : E (m+r)) := by
  rw [complementIso_apply]
  change WithLp.toLp 2 (encodeResponse D 0 1 z) = _
  simp only [encodeResponse,one_smul]
  rfl

/-- The residual unit vector lies on the unit sphere in the actual ambient complement. -/
theorem residualLift_mem_unit_complement {N m : ℕ} (D : O N) (r : ℕ) (e : m+r=N) (z : S m) :
    WithLp.toLp 2 (residualLift D r e z) ∈ (exposedEuclidean D r)ᗮ ∧
      ‖WithLp.toLp 2 (residualLift D r e z)‖ = 1 := by
  subst N
  rw [lift_isometry]
  exact ⟨(complementIso r D z.val).property,
    ((complementIso r D).norm_map z.val).trans (mem_sphere_zero_iff_norm.mp z.property)⟩

/-- Ambient residual lifts carry normalized coordinate surface measure onto normalized surface
measure of the orthogonal complement, independently of the chosen frame coordinates. -/
theorem measurePreserving_residualLift {N m : ℕ} [NeZero m] (D : O N) (r : ℕ) (e : m+r=N) :
    MeasurePreserving (fun z : S m => WithLp.toLp 2 (residualLift D r e z))
      (sphereProbability m) (complementSphere (exposedEuclidean D r)) := by
  subst N
  let K := exposedEuclidean D r
  let i := complementIso r D
  let j := (stdOrthonormalBasis ℝ Kᗮ).repr.symm
  have hi : Measurable (fun z : S m => i z.val) := (i.continuous.comp continuous_subtype_val).measurable
  have hj : Measurable (fun z : S (Module.finrank ℝ Kᗮ) => j z.val) :=
    (j.continuous.comp continuous_subtype_val).measurable
  have hx : (fun z : S m => WithLp.toLp 2 (residualLift D r rfl z)) =
      (Subtype.val : Kᗮ → E (m+r)) ∘ (fun z : S m => i z.val) := funext (lift_isometry r D)
  rw [hx]
  refine ⟨measurable_subtype_coe.comp hi, ?_⟩
  rw [← Measure.map_map measurable_subtype_coe hi,sphere_map_congr_isometry i j,
    Measure.map_map measurable_subtype_coe hj]
  rfl

#print axioms residualLift_mem_unit_complement
#print axioms measurePreserving_residualLift

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
