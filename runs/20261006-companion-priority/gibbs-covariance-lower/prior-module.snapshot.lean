import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.Tactic

/-!
# Actual Gibbs gradient second moment

The ideal Gibbs gradient moment consumed by Section 6.3 of Chen, Chewi, Lu
and Zhang, arXiv:2609.06906v1. Genuine C2 Hessian bounds imply all noncompact
weighted integrability facts before full-space directional integration by
parts. A finite orthonormal-basis sum and the actual exponential tilt give
both Gibbs L1 statements, the moment identity, and the beta-times-dimension
bound. No minimizer, weighted-integrability input or moment bound is assumed.

The finite-dimensional real inner-product formulation includes dimension zero.
The explicit alpha<=beta assumption is retained even though its binder is
unused. H denotes the actual standard-orthonormal-basis Hessian diagonal sum;
no separate abstract trace/Laplacian or basis-independence theorem is claimed.
This ideal-law component does not establish approximate/smoothed output
moments, random-history conditioning or summed reference-query cost.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem absorb_quadratic {a r : ℝ} (ha : 0 < a) :
    r^2 * Real.exp (-a*r^2) ≤ (2/a)*Real.exp (-(a/2)*r^2) := by
  have hx : (a/2)*r^2 ≤ Real.exp ((a/2)*r^2) := by
    linarith [Real.add_one_le_exp ((a/2)*r^2)]
  have hm := mul_le_mul_of_nonneg_right hx (Real.exp_nonneg (-a*r^2))
  have he : Real.exp ((a/2)*r^2)*Real.exp (-a*r^2) = Real.exp (-(a/2)*r^2) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [he] at hm
  calc
    r^2 * Real.exp (-a*r^2) ≤ Real.exp (-(a/2)*r^2)/(a/2) :=
      (le_div_iff₀ (by positivity : 0 < a/2)).2 (by nlinarith [hm])
    _ = (2/a)*Real.exp (-(a/2)*r^2) := by ring

private theorem weighted_square (w q : E → ℝ) (hw : Continuous w)
    (hq : Continuous q) {a C A B : ℝ} (ha : 0 < a) (hC : 0 ≤ C)
    (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hweight : ∀ x, Real.exp (w x) ≤ C*Real.exp (-a*‖x‖^2))
    (hgrowth : ∀ x, ‖q x‖ ≤ A+B*‖x‖) :
    Integrable (fun x => Real.exp (w x) * (q x)^2) (volume : Measure E) := by
  have hdom := (Integrability.integrable_exp_neg_mul_norm_sq
      (E := E) (show 0 < a/2 by positivity)).const_mul (C*(2*A^2+4*B^2/a))
  apply hdom.mono' (hw.rexp.mul (hq.pow 2)).aestronglyMeasurable
  filter_upwards with x
  change ‖Real.exp (w x)*(q x)^2‖ ≤ C*(2*A^2+4*B^2/a)*Real.exp (-(a/2)*‖x‖^2)
  simp only [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (Real.exp_nonneg _) (sq_nonneg _))]
  have hs : (q x)^2 ≤ 2*A^2+2*B^2*‖x‖^2 := by
    have hh := (sq_le_sq₀ (norm_nonneg (q x)) (by positivity)).2 (hgrowth x)
    rw [Real.norm_eq_abs,sq_abs] at hh
    nlinarith [sq_nonneg (A-B*‖x‖)]
  have he : Real.exp (-a*‖x‖^2) ≤ Real.exp (-(a/2)*‖x‖^2) := by
    apply Real.exp_le_exp.mpr
    nlinarith [mul_nonneg ha.le (sq_nonneg ‖x‖)]
  calc
    Real.exp (w x)*(q x)^2 ≤ (C*Real.exp (-a*‖x‖^2))*(2*A^2+2*B^2*‖x‖^2) :=
      mul_le_mul (hweight x) hs (sq_nonneg _) (mul_nonneg hC (Real.exp_nonneg _))
    _ = C*(2*A^2*Real.exp (-a*‖x‖^2)+2*B^2*(‖x‖^2*Real.exp (-a*‖x‖^2))) := by ring
    _ ≤ C*(2*A^2*Real.exp (-(a/2)*‖x‖^2)+2*B^2*((2/a)*Real.exp (-(a/2)*‖x‖^2))) := by
      apply mul_le_mul_of_nonneg_left _ hC
      exact add_le_add (mul_le_mul_of_nonneg_left he (by positivity))
        (mul_le_mul_of_nonneg_left (absorb_quadratic (r := ‖x‖) ha) (by positivity))
    _ = C*(2*A^2+4*B^2/a)*Real.exp (-(a/2)*‖x‖^2) := by ring

private theorem weighted_gradient [CompleteSpace E] {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2) :
    Integrable (fun x => Real.exp (-U x)) (volume : Measure E) ∧
    Integrable (fun x => Real.exp (-U x)*‖gradient U x‖^2) (volume : Measure E) ∧
    Integrable (fun x => Real.exp (-U x)*‖gradient U x‖) (volume : Measure E) := by
  have ha : (0 : ℝ) < α := hα
  have hdata := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hU hH (0 : E)
  simp only [NNReal.coe_zero, zero_div, zero_mul, add_zero] at hdata
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hc : Continuous (gradient U) :=
    Calculus.Gradient.continuous_gradient_of_contDiff_one (hU.of_le (by norm_num))
  have hi := StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn ha hd hdata.1
  let g := gradient U (0 : E)
  let b : ℝ := U 0 - ((α : ℝ)/2)⁻¹/2*‖g‖^2
  have hquad (x : E) : (α : ℝ)/4*‖x‖^2+b ≤ U x := by
    have hfirst : U 0 + inner ℝ g x + (α : ℝ)/2*‖x‖^2 ≤ U x := by
      simpa only [g, sub_zero] using
        StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hdata.1
          (fun z _ => (hd z).hasGradientAt) (x := 0) (y := x)
          (Set.mem_univ _) (Set.mem_univ _)
    have hinner := (abs_le.mp (abs_real_inner_le_norm g x)).1
    have hyoung := two_mul_le_add_mul_sq (a := ‖x‖) (b := ‖g‖)
      (show 0 < (α : ℝ)/2 by positivity)
    dsimp only [b]
    nlinarith
  have hgrowth (x : E) : ‖‖gradient U x‖‖ ≤ ‖g‖+(β : ℝ)*‖x‖ := by
    rw [norm_norm]
    have hl := hdata.2.norm_sub_le x 0
    rw [sub_zero] at hl
    calc
      ‖gradient U x‖ ≤ ‖gradient U x-gradient U 0‖+‖gradient U 0‖ := norm_le_norm_sub_add _ _
      _ ≤ ‖g‖+(β : ℝ)*‖x‖ := by dsimp only [g]; linarith
  have hsq := weighted_square (fun x => -U x) (fun x => ‖gradient U x‖)
    hU.continuous.neg hc.norm (a := (α : ℝ)/4) (C := Real.exp (-b))
    (A := ‖g‖) (B := (β : ℝ)) (by positivity) (Real.exp_nonneg _) (norm_nonneg _)
    β.coe_nonneg (fun x => by
      calc
        Real.exp (-U x) ≤ Real.exp (-((α : ℝ)/4*‖x‖^2+b)) :=
          Real.exp_le_exp.mpr (neg_le_neg (hquad x))
        _ = Real.exp (-b)*Real.exp (-((α : ℝ)/4)*‖x‖^2) := by
          rw [← Real.exp_add]
          congr 1
          ring) hgrowth
  refine ⟨hi,hsq,?_⟩
  apply (hi.add hsq).mono' (hU.continuous.neg.rexp.mul hc.norm).aestronglyMeasurable
  filter_upwards with x
  change ‖Real.exp (-U x)*‖gradient U x‖‖ ≤ Real.exp (-U x)+Real.exp (-U x)*‖gradient U x‖^2
  rw [Real.norm_eq_abs, abs_of_nonneg (mul_nonneg (Real.exp_nonneg _) (norm_nonneg _))]
  have hx : ‖gradient U x‖ ≤ 1+‖gradient U x‖^2 := by nlinarith [sq_nonneg (‖gradient U x‖-1)]
  simpa only [mul_add,mul_one] using mul_le_mul_of_nonneg_left hx (Real.exp_nonneg (-U x))

private theorem directional_ibp [CompleteSpace E] {U : E → ℝ} {β : ℝ≥0}
    (hU : ContDiff ℝ 2 U) (v : E) (hv : ‖v‖ = 1)
    (hH : ∀ x, 0 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ β)
    (hi : Integrable (fun x => Real.exp (-U x)) (volume : Measure E))
    (hsq : Integrable (fun x => Real.exp (-U x)*‖gradient U x‖^2) (volume : Measure E))
    (hlin : Integrable (fun x => Real.exp (-U x)*‖gradient U x‖) (volume : Measure E)) :
    Integrable (fun x => Real.exp (-U x)*(fderiv ℝ U x v)^2) (volume : Measure E) ∧
    Integrable (fun x => Real.exp (-U x)*fderiv ℝ (fderiv ℝ U) x v v) (volume : Measure E) ∧
    (∫ x, Real.exp (-U x)*(fderiv ℝ U x v)^2) =
      ∫ x, Real.exp (-U x)*fderiv ℝ (fderiv ℝ U) x v v := by
  let f := fun x => Real.exp (-U x)
  let q := fun x => fderiv ℝ U x v
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hq : ContDiff ℝ 1 q :=
    (hU.fderiv_right (m := 1) (by norm_num)).clm_apply contDiff_const
  have hf : ContDiff ℝ 1 f := (hU.of_le (by norm_num)).neg.exp
  have hqder (x : E) : fderiv ℝ q x v = fderiv ℝ (fderiv ℝ U) x v v := by
    have he := (((hU.fderiv_right (m := 1) (by norm_num)).differentiable_one x).hasFDerivAt).clm_apply
      (hasFDerivAt_const v x)
    rw [show fderiv ℝ q x = _ from he.fderiv]
    simp
  have hfder (x : E) : fderiv ℝ f x v = -f x*q x := by
    rw [show fderiv ℝ f x = _ from (hd x).hasFDerivAt.neg.exp.fderiv]
    simp only [smul_apply,neg_apply,smul_eq_mul,Pi.neg_apply]
    dsimp only [f,q]
    ring
  have hqbound (x : E) : ‖q x‖ ≤ ‖gradient U x‖ := by
    dsimp only [q]
    rw [← inner_gradient_left]
    simpa only [hv,mul_one] using norm_inner_le_norm (gradient U x) v
  have hqq : Integrable (fun x => f x*(q x)^2) (volume : Measure E) := by
    apply hsq.mono' (hf.continuous.mul (hq.continuous.pow 2)).aestronglyMeasurable
    filter_upwards with x
    change ‖f x*(q x)^2‖ ≤ f x*‖gradient U x‖^2
    rw [Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (Real.exp_nonneg _) (sq_nonneg _))]
    apply mul_le_mul_of_nonneg_left _ (Real.exp_nonneg _)
    have hh := (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).2 (hqbound x)
    simpa only [Real.norm_eq_abs,sq_abs] using hh
  have hHc : Continuous (fun x => fderiv ℝ q x v) :=
    (hq.fderiv_right (m := 0) (by norm_num)).continuous.clm_apply continuous_const
  have hqh : Integrable (fun x => f x*fderiv ℝ q x v) (volume : Measure E) := by
    apply (hi.mul_const (β : ℝ)).mono' (hf.continuous.mul hHc).aestronglyMeasurable
    filter_upwards with x
    change ‖f x*fderiv ℝ q x v‖ ≤ f x*(β : ℝ)
    rw [hqder,Real.norm_eq_abs,abs_of_nonneg (mul_nonneg (Real.exp_nonneg _) (hH x).1)]
    exact mul_le_mul_of_nonneg_left (hH x).2 (Real.exp_nonneg _)
  have hq1 : Integrable (fun x => f x*q x) (volume : Measure E) := by
    apply hlin.mono' (hf.continuous.mul hq.continuous).aestronglyMeasurable
    filter_upwards with x
    change ‖f x*q x‖ ≤ f x*‖gradient U x‖
    rw [norm_mul,Real.norm_eq_abs,abs_of_pos (Real.exp_pos _)]
    exact mul_le_mul_of_nonneg_left (hqbound x) (Real.exp_nonneg _)
  have hfq : Integrable (fun x => fderiv ℝ f x v*q x) (volume : Measure E) := by
    convert hqq.neg using 1
    ext x
    change fderiv ℝ f x v*q x = -(f x*(q x)^2)
    rw [hfder]
    ring
  have hidentity := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable hfq hqh hq1
    (fun x _ => hf.differentiable_one x) (fun x _ => hq.differentiable_one x)
  have hHintegral : Integrable (fun x => f x*fderiv ℝ (fderiv ℝ U) x v v) (volume : Measure E) := by
    simpa only [hqder] using hqh
  refine ⟨hqq,hHintegral,?_⟩
  change (∫ x, f x*(q x)^2) = ∫ x, f x*fderiv ℝ (fderiv ℝ U) x v v
  calc
    (∫ x, f x*(q x)^2) = -(∫ x, fderiv ℝ f x v*q x) := by
      rw [← integral_neg]
      apply integral_congr_ae
      filter_upwards with x
      rw [hfder]
      ring
    _ = ∫ x, f x*fderiv ℝ q x v := hidentity.symm
    _ = ∫ x, f x*fderiv ℝ (fderiv ℝ U) x v v := by simp only [hqder]

/-- Probability, actual Gibbs L1, the score-square/diagonal-Hessian identity,
and its sharp curvature-dimension upper bound for the normalized Gibbs law. -/
theorem gibbs_gradient_moment [CompleteSpace E] {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (_hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    let H := fun x => ∑ i, fderiv ℝ (fderiv ℝ U) x
      ((stdOrthonormalBasis ℝ E) i) ((stdOrthonormalBasis ℝ E) i)
    IsProbabilityMeasure μ ∧ Integrable (fun x => ‖gradient U x‖^2) μ ∧
      Integrable H μ ∧ (∫ x, ‖gradient U x‖^2 ∂μ) = (∫ x, H x ∂μ) ∧
      (∫ x, ‖gradient U x‖^2 ∂μ) ≤ (β : ℝ)*Module.finrank ℝ E := by
  classical
  let μ := (volume : Measure E).tilted (fun x => -U x)
  let b := stdOrthonormalBasis ℝ E
  let H := fun x => ∑ i, fderiv ℝ (fderiv ℝ U) x (b i) (b i)
  have hw := weighted_gradient hα hU hH
  have hunit (i) : ‖b i‖ = 1 := b.orthonormal.norm_eq_one i
  have hdiag (x : E) (i) : 0 ≤ fderiv ℝ (fderiv ℝ U) x (b i) (b i) ∧
      fderiv ℝ (fderiv ℝ U) x (b i) (b i) ≤ β := by
    have hh := hH x (b i)
    rw [hunit,one_pow,mul_one,mul_one] at hh
    exact ⟨(NNReal.coe_nonneg α).trans hh.1,hh.2⟩
  have hdir (i) := directional_ibp hU (b i) (hunit i) (fun x => hdiag x i)
    hw.1 hw.2.1 hw.2.2
  have hHi : Integrable (fun x => Real.exp (-U x)*H x) (volume : Measure E) := by
    have hi := integrable_finsetSum Finset.univ (fun i _ => (hdir i).2.1)
    simpa only [H,Finset.mul_sum] using hi
  have hparseval (x : E) : (∑ i, (fderiv ℝ U x (b i))^2) = ‖gradient U x‖^2 := by
    simpa only [inner_gradient_left,Real.norm_eq_abs,sq_abs] using
      b.sum_sq_norm_inner_left (gradient U x)
  have heq : (∫ x, Real.exp (-U x)*‖gradient U x‖^2) = ∫ x, Real.exp (-U x)*H x := by
    calc
      (∫ x, Real.exp (-U x)*‖gradient U x‖^2) =
          ∫ x, ∑ i, Real.exp (-U x)*(fderiv ℝ U x (b i))^2 := by
        simp only [← Finset.mul_sum,hparseval]
      _ = ∑ i, ∫ x, Real.exp (-U x)*(fderiv ℝ U x (b i))^2 :=
        integral_finsetSum _ (fun i _ => (hdir i).1)
      _ = ∑ i, ∫ x, Real.exp (-U x)*fderiv ℝ (fderiv ℝ U) x (b i) (b i) := by
        apply Finset.sum_congr rfl
        intro i _
        exact (hdir i).2.2
      _ = ∫ x, ∑ i, Real.exp (-U x)*fderiv ℝ (fderiv ℝ U) x (b i) (b i) :=
        (integral_finsetSum _ (fun i _ => (hdir i).2.1)).symm
      _ = ∫ x, Real.exp (-U x)*H x := by simp only [H,Finset.mul_sum]
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hw.1
  have hgμ : Integrable (fun x => ‖gradient U x‖^2) μ := by
    apply (integrable_tilted_iff hw.1 _).2
    simpa only [smul_eq_mul] using hw.2.1
  have hHμ : Integrable H μ := by
    apply (integrable_tilted_iff hw.1 _).2
    simpa only [smul_eq_mul] using hHi
  have htilt (g : E → ℝ) : (∫ x, g x ∂μ) =
      (∫ x, Real.exp (-U x)*g x)/(∫ x, Real.exp (-U x)) := by
    rw [integral_tilted]
    simp only [smul_eq_mul]
    rw [← integral_div]
    apply integral_congr_ae
    filter_upwards with x
    ring
  have heqμ : (∫ x, ‖gradient U x‖^2 ∂μ) = ∫ x, H x ∂μ := by
    rw [htilt,htilt,heq]
  refine ⟨inferInstance,hgμ,hHμ,heqμ,?_⟩
  change (∫ x, ‖gradient U x‖^2 ∂μ) ≤ (β : ℝ)*Module.finrank ℝ E
  rw [heqμ]
  have hbound (x : E) : H x ≤ (β : ℝ)*Module.finrank ℝ E := by
    calc
      H x ≤ ∑ _i : Fin (Module.finrank ℝ E), (β : ℝ) :=
        Finset.sum_le_sum (fun i _ => (hdiag x i).2)
      _ = (β : ℝ)*Module.finrank ℝ E := by simp [mul_comm]
  simpa only [integral_const,probReal_univ,one_smul] using
    integral_mono hHμ (integrable_const ((β : ℝ)*Module.finrank ℝ E)) hbound

end AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment
