import GC43Exposed

noncomputable section
open Matrix MeasureTheory Module
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

private theorem split_prefix_add {m : ℕ} (r : ℕ) (a b : Vec r) :
    splitVec r (a+b) (0 : Vec m) = splitVec r a 0 + splitVec r b 0 := by
  induction r with
  | zero => simp [splitVec]
  | succ r ih =>
    funext i
    cases i using Fin.cases
    · simp [splitVec]
    · rename_i j
      exact congrFun (ih (fun j => a j.succ) (fun j => b j.succ)) j

private theorem split_prefix_smul {m : ℕ} (r : ℕ) (s : ℝ) (a : Vec r) :
    splitVec r (s • a) (0 : Vec m) = s • splitVec r a 0 := by
  induction r with
  | zero => simp [splitVec]
  | succ r ih =>
    funext i
    cases i using Fin.cases
    · simp [splitVec]
    · rename_i j
      exact congrFun (ih (fun j => a j.succ)) j

private theorem prefix_retract {m : ℕ} (r : ℕ) (a : Vec r) :
    exposedCoords m r (splitVec r a 0) = a := by
  induction r with
  | zero => exact funext (fun i => i.elim0)
  | succ r ih =>
    funext i
    cases i using Fin.cases
    · rfl
    · rename_i j
      exact congrFun (ih (fun j => a j.succ)) j

theorem exposedSpace_finrank {N m : ℕ} (F : BlockFrame N m) :
    finrank ℝ (exposedSpace F.domain F.rank) = F.rank := by
  rcases F with ⟨r,e,D,R⟩; subst N
  let L : Vec r →ₗ[ℝ] Vec (m+r) := {
    toFun := fun a => act D (splitVec r a 0)
    map_add' := fun a b => by rw [split_prefix_add]; exact Matrix.mulVec_add _ _ _
    map_smul' := fun s a => by rw [split_prefix_smul]; exact Matrix.mulVec_smul _ _ _ }
  have hinj : Function.Injective L := by
    intro a b hab
    change act D _ = act D _ at hab
    have h := congrArg (fun x => exposedCoords m r (act D⁻¹ x)) hab
    simpa only [act_inv_act,prefix_retract] using h
  have he : exposedSpace D r = LinearMap.range L := by
    ext x
    rw [exposedSpace_iff, LinearMap.mem_range]
    constructor
    · intro h
      refine ⟨exposedCoords m r (act D⁻¹ x),?_⟩
      simpa only [L, LinearMap.coe_mk, AddHom.coe_mk, h] using query_from_coordinates D x
    · rintro ⟨a,rfl⟩
      change residualCoords m r (act D⁻¹ (act D (splitVec r a 0))) = 0
      rw [act_inv_act,residualCoords_splitVec]
  change finrank ℝ (exposedSpace D r) = r
  rw [he,LinearMap.finrank_range_of_inj hinj, Module.finrank_pi, Fintype.card_fin]

/-- The updated domain is exactly the span in parts (ii) and (iii) of Fact C.3. -/
theorem frameAfter_exposed_eq {N n : ℕ} (F : BlockFrame N (n+2)) (Q : S (n+2) → O (n+2))
    (hfirst : ∀ z, (Q z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = WithLp.ofLp z.val)
    (b : Bool) (v : Vec N) (z : S (n+2)) (hc : frameComplement F b v ≠ 0) :
    exposedSpace (frameAfter F Q b v z).domain (frameAfter F Q b v z).rank =
      exposedSpace F.domain F.rank ⊔ Submodule.span ℝ {if b then frameResponse F b v z else v} := by
  classical
  let y := if b then frameResponse F b v z else v
  apply Submodule.eq_of_le_of_finrank_le (frameAfter_exposed_le F Q hfirst b v z hc)
  have h := Submodule.finrank_add_le_finrank_add_finrank (exposedSpace F.domain F.rank) (Submodule.span ℝ {y})
  have hs : finrank ℝ (Submodule.span ℝ {y}) ≤ 1 := le_trans (finrank_span_le_card {y}) (by simp)
  rw [exposedSpace_finrank F] at h
  rw [exposedSpace_finrank]
  exact h.trans (Nat.add_le_add_left hs _)

#print axioms frameAfter_exposed_eq
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
