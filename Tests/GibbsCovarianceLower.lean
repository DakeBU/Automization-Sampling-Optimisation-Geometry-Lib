import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

noncomputable section
set_option backward.isDefEq.respectTransparency false
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal
open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper
namespace Tests.GibbsCovarianceLower

private def potential (x : ℝ) : ℝ := (3/8)*x^2 + (1/8)*Real.sin x
private theorem potential_curvature :
    ∀ z v : ℝ, (1/(2*(1:ℝ)))*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ potential) z v) v ∧
      (fderiv ℝ (fderiv ℝ potential) z v) v ≤ ‖v‖^2 := by
  have hder (z : ℝ) : HasDerivAt potential ((3/4)*z+(1/8)*Real.cos z) z := by
    convert (((hasDerivAt_id z).pow 2).const_mul (3/8)).add
      ((Real.hasDerivAt_sin z).const_mul (1/8)) using 1 <;> first | rfl | (simp [potential, Pi.add_apply, mul_comm]; ring)
  have hD : fderiv ℝ potential = fun z =>
      ((3/4)*z+(1/8)*Real.cos z) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv, (hder z).deriv]
    simp
  have hDD (z v : ℝ) : (fderiv ℝ (fderiv ℝ potential) z v) v =
      ((3/4)-(1/8)*Real.sin z)*v^2 := by
    have hd : HasDerivAt (fun w : ℝ => (3/4)*w+(1/8)*Real.cos w)
        ((3/4)-(1/8)*Real.sin z) z := by
      convert ((hasDerivAt_id z).const_mul (3/4)).add
        ((Real.hasDerivAt_cos z).const_mul (1/8)) using 1 <;> (try dsimp only [id]) <;> first | rfl | ring
    rw [hD, fderiv_eq_smul_deriv,
      (hd.smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
    simp
    ring
  intro z v
  rw [hDD]
  simp only [Real.norm_eq_abs, sq_abs]
  constructor <;> nlinarith [Real.sin_le_one z, Real.neg_one_le_sin z, sq_nonneg v]



-- Nonquadratic actual source potential: the posterior and convolution are
-- definitions, never inputs certifying covariance or smoothed curvature.
theorem actual_nonconstant_source {η : ℝ} (hη : 0<η) :
    let μ := (volume : Measure ℝ).tilted (fun x => -potential x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ ℝ
    let A := fun y : ℝ => C*∫ x, Real.exp (-potential x-‖y-x‖^2/(2*η)) ∂(volume : Measure ℝ)
    let R := fun y : ℝ => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    (∀ y v, ‖v‖^2/(1+η⁻¹) ≤ covarianceBilin (R y) v v) ∧
      ∀ y v, fderiv ℝ (fderiv ℝ (fun y => -Real.log (A y))) y v v ≤ (1/(1+η))*‖v‖^2 := by
  have hf : ContDiff ℝ 2 potential := by unfold potential;fun_prop
  have hh : ∀ x v : ℝ, ((1/2:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ potential) x v v ∧
      fderiv ℝ (fderiv ℝ potential) x v v ≤ ((1:ℝ≥0):ℝ)*‖v‖^2 := by
    intro x v
    simpa using potential_curvature x v
  simpa using smoothed_hessian_upper (by norm_num : (0:ℝ≥0)<1/2)
    (by norm_num : (1/2:ℝ≥0)≤1) hf hh hη

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment.gibbs_gradient_moment
#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment.gibbs_covariance_lower
#print axioms smoothed_hessian_upper
#print axioms actual_nonconstant_source
end Tests.GibbsCovarianceLower
