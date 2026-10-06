import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal
namespace IndependentCenteredPoincareStress
private def V (x : ℝ) : ℝ := x^2/2
private theorem derivatives :
    fderiv ℝ V = (fun x => x • ContinuousLinearMap.id ℝ ℝ) ∧
    ∀ x a : ℝ, fderiv ℝ (fderiv ℝ V) x a a = a^2 := by
  have hd (x : ℝ) : HasDerivAt V x x := by
    convert ((hasDerivAt_id x).pow 2).div_const 2 using 1 <;> first | rfl | (simp [V]; ring)
  have hD : fderiv ℝ V = fun x => x • ContinuousLinearMap.id ℝ ℝ := by
    funext x
    rw [fderiv_eq_smul_deriv, (hd x).deriv]
    rfl
  refine ⟨hD,?_⟩
  intro x a
  rw [hD, fderiv_eq_smul_deriv,
    ((hasDerivAt_id x).smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
  simp
  ring
/-- At the actual eta*beta=1 endpoint, quadratic source scores are constants
in u and their actual reflected-law variance vanishes. No conditional-law or
Poincare certificate is supplied. This independently tests the score sign,
fourfold normalization and zero source coefficient on a nonzero-dimensional law. -/
theorem actual_endpoint_constant_score :
    ∃ S : Kernel ℝ ℝ, IsMarkovKernel S ∧ ∀ y a : ℝ,
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible
        (S y) (fun _ => -(y*a)/2) ∧
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
        (S y) (fun _ => -(y*a)/2) = 0 := by
  have hV : ContDiff ℝ 2 V := by unfold V; fun_prop
  have hh : ∀ x a : ℝ, ((1:NNReal):ℝ)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ V) x a a ∧
      fderiv ℝ (fderiv ℝ V) x a a ≤ ((1:NNReal):ℝ)*‖a‖^2 := by
    intro x a
    rw [derivatives.2]
    simp [Real.norm_eq_abs, sq_abs]
  obtain ⟨R,S,_,hS,_,_,hf⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance.conditional_centered_domain_and_score_variance
      (α:=(1:NNReal)) (β:=(1:NNReal)) (η:=(1:ℝ))
      (by norm_num) (by norm_num) hV hh (by norm_num) (by norm_num)
  refine ⟨S,hS,?_⟩
  intro y a
  obtain ⟨_,_,_,_,D,_,_,_,_,_,ha⟩ := hf y
  have hq : (fun u : ℝ =>
      (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
        (1/(4*(1:ℝ))) • innerSL ℝ (y-u)) a) = (fun _ => -(y*a)/2) := by
    funext u
    simp [derivatives.1, innerSL_apply]
    ring
  have h := ha a
  rw [hq] at h
  norm_num at h
  exact ⟨h.1,le_antisymm h.2
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance_nonneg⟩
#print axioms actual_endpoint_constant_score
end IndependentCenteredPoincareStress
