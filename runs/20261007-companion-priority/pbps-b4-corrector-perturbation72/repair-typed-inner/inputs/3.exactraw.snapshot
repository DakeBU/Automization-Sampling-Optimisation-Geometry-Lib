import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic.Linarith

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation
noncomputable section
open scoped RealInnerProductSpace
set_option autoImplicit false

theorem quadratic_corrector_perturbation
    {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℝ H]
    [CompleteSpace H]
    (A G Inv : H →L[ℝ] H)
    (hA : IsSelfAdjoint A) (hG : IsSelfAdjoint G)
    (hInv : IsSelfAdjoint Inv) (hAInv : Commute A Inv)
    (hInvG : Inv * G = 1) (hGInv : G * Inv = 1)
    (hSquares : A * A + G * G = 1)
    (u v r : H) :
    let C : H → H → ℝ := fun u v =>
      (‖u‖^2 - ‖v‖^2)/2 - inner ℝ (A (Inv u)) v
    C (u + G r) (v - A r) - C u v =
      inner ℝ u (Inv r) + ‖r‖^2/2
 := by
  dsimp only
  have hIG (x : H) : Inv (G x)=x := by
    have h := congrArg (fun L : H →L[ℝ] H => L x) hInvG
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hSq (x : H) : A (A x)+G (G x)=x := by
    have h := congrArg (fun L : H →L[ℝ] H => L x) hSquares
    simpa only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply] using h
  have hEnergy (x : H) : ‖A x‖^2+‖G x‖^2=‖x‖^2 := by
    have h := congrArg (fun z : H => inner ℝ z x) (hSq x)
    rw [inner_add_left,hA.isSymmetric (A x) x,hG.isSymmetric (G x) x] at h
    simpa only [real_inner_self_eq_norm_sq] using h
  have hLinear (x : H) : Inv (A (A x))+G x=Inv x := by
    calc
      Inv (A (A x))+G x=Inv (A (A x))+Inv (G (G x)) := by rw [hIG]
      _ = Inv (A (A x)+G (G x)) := by rw [map_add]
      _ = Inv x := congrArg Inv (hSq x)
  have hMixed : inner ℝ (A (Inv u)) (A r)+inner ℝ u (G r)=inner ℝ u (Inv r) := by
    rw [hA.isSymmetric (Inv u) (A r),hInv.isSymmetric u (A (A r)),
      ← inner_add_right,hLinear r]
  rw [norm_add_sq_real,norm_sub_sq_real]
  simp only [map_add,hIG,inner_add_left,inner_sub_right,real_inner_self_eq_norm_sq]
  rw [real_inner_comm v (A r)]
  nlinarith only [hEnergy r,hMixed]

end
end AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.quadratic_corrector_perturbation
