import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment

/-!
# Mean of the actual Gibbs gradient

Positive lower and finite upper C2 Hessian bounds produce a probability tilt,
Bochner integrability of the gradient, and its zero vector mean. The existing
score-square producer supplies the domain; full-space integration by parts
against the constant function supplies the cancellation. No integrability,
normalizer, boundary-decay, minimizer or mean identity is an input.

The upper bound is widened internally when calling the existing second-moment
provider. This avoids an additional alpha<=beta binder and includes dimension
zero, where the Hessian bounds are vacuous and alpha may exceed beta.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal

theorem integrable_gradient_and_integral_eq_zero
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {U : E → ℝ} {α β : ℝ≥0} (hα : 0 < α) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    IsProbabilityMeasure μ ∧ Integrable (gradient U) μ ∧
      (∫ x, gradient U x ∂μ) = 0 := by
  let μ := (volume : Measure E).tilted (fun x => -U x)
  have hupper : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ ((max α β : ℝ≥0) : ℝ)*‖v‖^2 := by
    intro x v
    refine ⟨(hH x v).1,(hH x v).2.trans ?_⟩
    exact mul_le_mul_of_nonneg_right (by exact_mod_cast le_max_right α β) (sq_nonneg _)
  have hm := GibbsGradientMoment.gibbs_gradient_moment hα (le_max_left α β) hU hupper
  have hμ : IsProbabilityMeasure μ := hm.1
  let : IsProbabilityMeasure μ := hμ
  have hc : Continuous (gradient U) :=
    Calculus.Gradient.continuous_gradient_of_contDiff_one (hU.of_le (by norm_num))
  have hlp : MemLp (gradient U) 2 μ :=
    (memLp_two_iff_integrable_sq_norm hc.aestronglyMeasurable).mpr hm.2.1
  have hg : Integrable (gradient U) μ := hlp.integrable (by norm_num)
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hs := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hU hH (0 : E)
  simp only [NNReal.coe_zero,zero_div,zero_mul,add_zero] at hs
  have hi := StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    (show (0 : ℝ) < α from hα) hd hs.1
  have hweighted : Integrable (fun x => Real.exp (-U x) • gradient U x)
      (volume : Measure E) := (integrable_tilted_iff hi _).mp hg
  refine ⟨hμ,hg,integral_eq_zero_of_forall_integral_inner_eq_zero ℝ _ hg ?_⟩
  intro v
  change (∫ x, inner ℝ v (gradient U x) ∂μ) = 0
  rw [show (fun x => inner ℝ v (gradient U x)) =
      (fun x => inner ℝ (gradient U x) v) by funext x; exact real_inner_comm _ _]
  let f := fun x => Real.exp (-U x)
  have hf : Differentiable ℝ f := hd.neg.exp
  have hfd (x : E) : fderiv ℝ f x v = -f x*inner ℝ (gradient U x) v := by
    rw [show fderiv ℝ f x = _ from (hd x).hasFDerivAt.neg.exp.fderiv]
    simp only [smul_apply,neg_apply,smul_eq_mul,Pi.neg_apply]
    rw [← inner_gradient_left]
    dsimp only [f]
    ring
  have hwv : Integrable (fun x => f x*inner ℝ (gradient U x) v)
      (volume : Measure E) := by
    simpa only [real_inner_smul_left,f] using hweighted.inner_const (𝕜 := ℝ) v
  have hdf : Integrable (fun x => fderiv ℝ f x v*(1 : ℝ))
      (volume : Measure E) := by
    convert hwv.neg using 1
    ext x
    rw [hfd]
    change (-f x*inner ℝ (gradient U x) v)*1 = -(f x*inner ℝ (gradient U x) v)
    ring
  have hb := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable hdf
    (by simp) (by simpa only [mul_one] using hi)
    (fun x _ => hf x) (fun x _ => differentiableAt_const (1 : ℝ))
  have hzero : (∫ x, f x*inner ℝ (gradient U x) v ∂(volume : Measure E)) = 0 := by
    simpa [hfd,neg_mul,integral_neg] using hb.symm
  rw [show μ = (volume : Measure E).tilted (fun x => -U x) from rfl,integral_tilted]
  rw [show (fun x => (Real.exp (-U x)/(∫ z,Real.exp (-U z))) •
      inner ℝ (gradient U x) v) = (fun x => (f x*inner ℝ (gradient U x) v)/
        (∫ z,Real.exp (-U z))) by funext x; simp only [smul_eq_mul,f]; ring]
  rw [integral_div,hzero,zero_div]

end AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean
