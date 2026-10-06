import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean
import Mathlib.Analysis.InnerProductSpace.PiL2

noncomputable section
open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal
open AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean
namespace Tests.GibbsGradientMean

private def shifted (x : ℝ) : ℝ := (x-7)^2/2

private theorem shifted_gradient : gradient shifted = fun x => x-7 := by
  funext x
  have h : HasDerivAt shifted (x-7) x := by
    convert (((hasDerivAt_id x).sub_const 7).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  exact h.hasGradientAt.gradient

private theorem shifted_curvature (x v : ℝ) :
    fderiv ℝ (fderiv ℝ shifted) x v v = ‖v‖^2 := by
  have hd (z : ℝ) : HasDerivAt shifted (z-7) z := by
    convert (((hasDerivAt_id z).sub_const 7).pow 2).div_const 2 using 1 <;>
      first | rfl | (simp only [id_eq]; ring)
  have hf : fderiv ℝ shifted = fun z => (z-7) • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    rw [fderiv_eq_smul_deriv,(hd z).deriv]
    simp
  have hh : deriv (fun z : ℝ => (z-7) • ContinuousLinearMap.id ℝ ℝ) x =
      ContinuousLinearMap.id ℝ ℝ := by
    simpa only [one_smul,id_eq] using
      (((hasDerivAt_id x).sub_const 7).smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv
  rw [hf,fderiv_eq_smul_deriv,hh]
  simp [Real.norm_eq_abs,pow_two]

-- Actual unbounded, noncentered Gibbs observable: the result yields EX=7.
theorem translated_gibbs_mean :
    let μ := (volume : Measure ℝ).tilted (fun x => -(x-7)^2/2)
    IsProbabilityMeasure μ ∧ Integrable id μ ∧ (∫ x,x ∂μ)=7 := by
  have hH : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)*‖v‖^2 ≤
      fderiv ℝ (fderiv ℝ shifted) x v v ∧
      fderiv ℝ (fderiv ℝ shifted) x v v ≤ ((1 : ℝ≥0) : ℝ)*‖v‖^2 := by
    intro x v; rw [shifted_curvature]; norm_num
  obtain ⟨hp,hg,hm⟩ := integrable_gradient_and_integral_eq_zero
    (by norm_num : (0 : ℝ≥0)<1) (by unfold shifted; fun_prop) hH
  let μ := (volume : Measure ℝ).tilted (fun x => -(x-7)^2/2)
  have hp' : IsProbabilityMeasure μ := by simpa only [μ,shifted,neg_div] using hp
  have : IsProbabilityMeasure μ := hp'
  have hg' : Integrable (fun x : ℝ => x-7) μ := by
    simpa only [μ,shifted_gradient,shifted,neg_div] using hg
  have hx : Integrable (fun x : ℝ => x) μ := by
    convert hg'.add (integrable_const (7 : ℝ)) using 1 <;> try rfl
    funext x; change x=(x-7)+7; ring
  refine ⟨hp',hx,?_⟩
  have hm' : (∫ x,x-7 ∂μ)=0 := by simpa only [μ,shifted_gradient,shifted,neg_div] using hm
  rw [integral_sub hx (integrable_const _),integral_const,probReal_univ,one_smul] at hm'
  linarith

abbrev E0 := EuclideanSpace ℝ (Fin 0)
-- Alpha exceeds beta. A convenience alpha<=beta binder would reject this case.
theorem zero_dimension_reversed_bounds :
    let μ := (volume : Measure E0).tilted (fun _ => (-7 : ℝ))
    IsProbabilityMeasure μ ∧ Integrable (gradient (fun _ : E0 => (7 : ℝ))) μ ∧
      (∫ x,gradient (fun _ : E0 => (7 : ℝ)) x ∂μ)=0 := by
  apply integrable_gradient_and_integral_eq_zero (α := 1) (β := 0) (by norm_num) contDiff_const
  intro x v
  have hv : v=0 := Subsingleton.elim _ _
  simp [hv]

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean.integrable_gradient_and_integral_eq_zero
#print axioms translated_gibbs_mean
#print axioms zero_dimension_reversed_bounds

end Tests.GibbsGradientMean
