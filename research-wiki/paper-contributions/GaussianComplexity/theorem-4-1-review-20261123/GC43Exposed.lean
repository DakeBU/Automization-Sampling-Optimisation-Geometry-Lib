import GC43FrameGeometry
import Mathlib.Tactic

open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

/-- The first r columns of an ambient orthogonal frame span the exposed space. -/
def exposedSpace {N : ℕ} (D : O N) (r : ℕ) : Submodule ℝ (Vec N) where
  carrier := {x | ∀ i : Fin N, r ≤ i.val → act D⁻¹ x i = 0}
  zero_mem' := by simp [act]
  add_mem' := by
    intro x y hx hy i hi
    simp only [act,Matrix.mulVec_add,Pi.add_apply]
    exact add_eq_zero_iff_eq_neg.mpr (by rw [show D⁻¹.val.mulVec x i = 0 from hx i hi,
      show D⁻¹.val.mulVec y i = 0 from hy i hi, neg_zero])
  smul_mem' := by
    intro s x hx i hi
    change act D⁻¹ (s • x) i = 0
    simp only [act, Matrix.mulVec_smul, Pi.smul_apply, smul_eq_mul]
    rw [show D⁻¹.val.mulVec x i = 0 from hx i hi, mul_zero]

private theorem coords_at (m r : ℕ) (x : Vec (m+r)) (i : Fin m) :
    residualCoords m r x i = x ⟨r+i.val,by omega⟩ := by
  induction r with
  | zero => simp [residualCoords]
  | succ r ih =>
    change residualCoords m r (fun j => x j.succ) i = _
    rw [ih]
    congr 1
    apply Fin.ext
    dsimp
    omega

theorem exposedSpace_iff {m r : ℕ} (D : O (m+r)) (x : Vec (m+r)) :
    x ∈ exposedSpace D r ↔ residualCoords m r (act D⁻¹ x) = 0 := by
  constructor
  · intro hx
    funext i
    rw [coords_at]
    exact hx _ (by dsimp; omega)
  · intro hx i hi
    let j : Fin m := ⟨i.val-r, by omega⟩
    have h := congrFun hx j
    rw [coords_at] at h
    have he : (⟨r+j.val,by omega⟩ : Fin (m+r)) = i := by
      apply Fin.ext; dsimp [j]; omega
    rwa [he] at h

theorem frameComplement_zero_iff {N m : ℕ} (F : BlockFrame N m) (back : Bool) (v : Vec N) :
    frameComplement F back v = 0 ↔ v ∈ exposedSpace (queryFrame back F.domain F.range) F.rank := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  rw [exposedSpace_iff]
  change WithLp.toLp 2 (residualCoords m r (act (queryFrame back D R)⁻¹ v)) = 0 ↔
    residualCoords m r (act (queryFrame back D R)⁻¹ v) = 0
  constructor
  · exact fun h => congrArg WithLp.ofLp h
  · intro h; rw [h]; rfl

theorem exposedSpace_initial (N : ℕ) : exposedSpace (1 : O N) 0 = ⊥ := by
  apply le_antisymm _ bot_le
  intro x hx
  change x = 0
  funext i
  have h := hx i (Nat.zero_le _)
  rw [inv_one] at h
  change ((1 : Matrix (Fin N) (Fin N) ℝ) *ᵥ x) i = 0 at h
  change x i = 0
  simpa only [Matrix.one_mulVec] using h

private theorem tail_extend {m r : ℕ} (D : O ((m+1)+r)) (U : O (m+1))
    (x : Vec ((m+1)+r)) (hx : x ∈ exposedSpace (extendFrame D U) (r+1)) :
    ∃ t : ℝ, residualCoords (m+1) r (act D⁻¹ x) = t • (U.val *ᵥ Pi.single 0 1) := by
  let F := extendFrame D U
  let y := act F⁻¹ x
  let a := exposedCoords (m+1) r y
  let c := residualCoords (m+1) r y
  have hc : c = c 0 • Pi.single (0 : Fin (m+1)) 1 := by
    funext i
    by_cases h : i = 0
    · subst i; simp
    · change residualCoords (m+1) r y i = _
      rw [coords_at]
      have hn : i.val ≠ 0 := by simpa using h
      have ht := hx (⟨r+i.val,by omega⟩ : Fin ((m+1)+r)) (by dsimp; omega)
      change y ⟨r+i.val,by omega⟩ = 0 at ht
      simp [ht,Pi.single_eq_of_ne h]
  have hx' : act D⁻¹ x = splitVec r a (act U c) := by
    have h : act F (splitVec r a c) = x := query_from_coordinates F x
    calc
      _ = act D⁻¹ (act F (splitVec r a c)) := by rw [h]
      _ = act (prefixEmbed (m+1) r U) (splitVec r a c) := by
        rw [← act_mul]; simp [F,extendFrame]
      _ = _ := act_prefixEmbed r U a c
  refine ⟨c 0, ?_⟩
  rw [hx',residualCoords_splitVec]
  calc
    _ = act U (c 0 • Pi.single (0 : Fin (m+1)) 1) := congrArg (act U) hc
    _ = _ := Matrix.mulVec_smul _ _ _


private theorem space_extend_le {m r : ℕ} (D : O ((m+1)+r)) (U : O (m+1))
    (y : Vec ((m+1)+r)) {s : ℝ} (hs : s ≠ 0)
    (hy : residualCoords (m+1) r (act D⁻¹ y) = s • (U.val *ᵥ Pi.single 0 1)) :
    exposedSpace (extendFrame D U) (r+1) ≤ exposedSpace D r ⊔ Submodule.span ℝ {y} := by
  intro x hx
  obtain ⟨t,ht⟩ := tail_extend D U x hx
  let k := t/s
  have he : x-k • y ∈ exposedSpace D r := by
    rw [exposedSpace_iff]
    funext i
    rw [coords_at]
    have hy' := congrFun hy i
    have hx' := congrFun ht i
    rw [coords_at] at hx' hy'
    change (D⁻¹.val *ᵥ (x-k • y)) _ = 0
    rw [Matrix.mulVec_sub, Matrix.mulVec_smul,Pi.sub_apply,Pi.smul_apply,smul_eq_mul]
    change (act D⁻¹ x) _ - k * (act D⁻¹ y) _ = 0
    rw [hx',hy']
    simp only [Pi.smul_apply, smul_eq_mul]
    dsimp [k]; field_simp; ring
  exact Submodule.mem_sup.mpr ⟨_,he,_,Submodule.smul_mem _ k (Submodule.subset_span (Set.mem_singleton y)),
    sub_add_cancel _ _⟩

theorem frameAfter_exposed_le {N n : ℕ} (F : BlockFrame N (n+2)) (Q : S (n+2) → O (n+2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (back : Bool) (v : Vec N) (z : S (n+2)) (hc : frameComplement F back v ≠ 0) :
    exposedSpace (frameAfter F Q back v z).domain (frameAfter F Q back v z).rank ≤
      exposedSpace F.domain F.rank ⊔ Submodule.span ℝ {if back then frameResponse F back v z else v} := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  cases back
  · let c := queryComplement (m := n+2) (r := r) D v
    change c ≠ 0 at hc
    change exposedSpace (extendFrame D (Q (unitOrFirst c))) (r+1) ≤
      exposedSpace D r ⊔ Submodule.span ℝ {v}
    apply space_extend_le D _ v (norm_ne_zero_iff.mpr hc)
    rw [hfirst,scaled_unitOrFirst]
    rfl
  · let c := queryComplement (m := n+2) (r := r) R v
    change c ≠ 0 at hc
    let a := exposedCoords (n+2) r (act R⁻¹ v)
    change exposedSpace (extendFrame D (Q z)) (r+1) ≤
      exposedSpace D r ⊔ Submodule.span ℝ {encodeResponse D a ‖c‖ z}
    apply space_extend_le D _ _ (norm_ne_zero_iff.mpr hc)
    rw [hfirst]
    simp only [encodeResponse,act_inv_act,residualCoords_splitVec]

#print axioms frameAfter_exposed_le

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
