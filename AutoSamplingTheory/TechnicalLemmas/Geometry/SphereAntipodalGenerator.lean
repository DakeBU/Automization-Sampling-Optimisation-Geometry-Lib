import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator
import Mathlib.Analysis.Calculus.FDeriv.Equiv

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereAntipodalGenerator

open SphereDiffusionGenerator
open scoped Laplacian

/-- Negation transports the actual first derivative and commutes with the
existing extrinsic sphere expression. These are total-operator identities;
classical generator applications separately supply smooth tests and unit points. -/
theorem sphere_differential_operators_comp_neg
    {I : Type*} [Fintype I] [DecidableEq I]
    (f : EuclideanSpace ℝ I → ℝ) (w : EuclideanSpace ℝ I) :
    (∀ h : EuclideanSpace ℝ I,
      fderiv ℝ (fun x => f (-x)) w h = -fderiv ℝ f (-w) h) ∧
    sphereLaplacian (fun x => f (-x)) w = sphereLaplacian f (-w) := by
  have hD (x : EuclideanSpace ℝ I) :
      fderiv ℝ (fun y => f (-y)) x = -fderiv ℝ f (-x) := by
    simpa only [neg_one_smul] using (fderiv_comp_smul (f := f) (x := x) (-1 : ℝ))
  have hDfun : fderiv ℝ (fun x => f (-x)) = fun x => -fderiv ℝ f (-x) :=
    funext hD
  have hH (x : EuclideanSpace ℝ I) :
      fderiv ℝ (fderiv ℝ (fun y => f (-y))) x = fderiv ℝ (fderiv ℝ f) (-x) := by
    rw [hDfun]
    change fderiv ℝ (-(fun y => fderiv ℝ f (-y))) x = _
    rw [fderiv_neg]
    have ht := fderiv_comp_smul (f := fderiv ℝ f) (x := x) (-1 : ℝ)
    simpa only [neg_one_smul, neg_neg] using congrArg (fun L => -L) ht
  have hLap : (Δ (fun x => f (-x))) w = (Δ f) (-w) := by
    rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis _
        (EuclideanSpace.basisFun I ℝ),
      InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis _
        (EuclideanSpace.basisFun I ℝ)]
    simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one, hH]
  constructor
  · intro h
    simpa only [neg_apply] using congrArg (fun L => L h) (hD w)
  · simp only [sphereLaplacian, hLap, hH, hD, neg_apply,
      map_neg, neg_neg]

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereAntipodalGenerator
