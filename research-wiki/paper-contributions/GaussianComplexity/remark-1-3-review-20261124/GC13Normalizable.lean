import GC13Gibbs
import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability

/-! The Hessian lower bound and a global minimizer suffice for the Gibbs
partition function to be positive and finite. -/
noncomputable section
open Matrix MeasureTheory InnerProductSpace
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs
open AutoSamplingTheory.TechnicalLemmas.Analysis
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

set_option backward.isDefEq.respectTransparency false in
/-- Identify the Riesz Hessian of the gradient with the second Fréchet derivative
on a diagonal direction, preserving the strong-convexity constant. -/
theorem strongConvexOn_of_gradient_hessian_lower {d : ℕ} {V : E d → ℝ}
    (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v, ‖v‖^2 ≤ inner ℝ v (fderiv ℝ (gradient V) x v)) :
    StrongConvexOn Set.univ 1 V := by
  let R : (E d →L[ℝ] ℝ) →L[ℝ] E d :=
    { toFun := (toDual ℝ (E d)).symm
      map_add' := (toDual ℝ (E d)).symm.map_add
      map_smul' := by intros; simp
      cont := (toDual ℝ (E d)).symm.continuous }
  apply HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV
  intro x v
  have hg : HasFDerivAt (gradient V) (R.comp (fderiv ℝ (fderiv ℝ V) x)) x :=
    R.hasFDerivAt.comp x (((hV.fderiv_right (m := 1) (by norm_num)).differentiable_one x).hasFDerivAt)
  have h := hH x v
  rw [hg.fderiv, real_inner_comm] at h
  have he : inner ℝ ((R.comp (fderiv ℝ (fderiv ℝ V) x)) v) v =
      (fderiv ℝ (fderiv ℝ V) x v) v := toDual_symm_apply
  simpa only [one_mul,he] using h

/-- Every C² potential in the class has a positive finite partition function
at its known minimizer, so its normalized density defines a probability measure. -/
theorem gibbsMass_of_hessian_lower {d : ℕ} {V : E d → ℝ}
    (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v, ‖v‖^2 ≤ inner ℝ v (fderiv ℝ (gradient V) x v))
    (xstar : E d) (hmin : ∀ x, V xstar ≤ V x) :
    0 < gibbsMass V ∧ gibbsMass V ≠ ∞ := by
  constructor
  · exact pos_iff_ne_zero.mpr (lintegral_gibbsDensityENNReal_ne_zero volume hV.continuous.aemeasurable)
  · exact Integrability.lintegral_gibbsDensityENNReal_ne_top_of_strongConvexOn_minimizer
      zero_lt_one xstar (strongConvexOn_of_gradient_hessian_lower hV hH) (isMinOn_univ_iff.mpr hmin)

#print axioms gibbsMass_of_hessian_lower
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
