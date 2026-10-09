import Mathlib.Analysis.InnerProductSpace.Adjoint

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
