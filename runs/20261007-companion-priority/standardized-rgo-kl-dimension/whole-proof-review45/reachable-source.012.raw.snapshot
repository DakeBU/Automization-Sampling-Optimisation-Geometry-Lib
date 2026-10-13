import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Probability.Moments.CovarianceBilin
import Mathlib.Tactic

/-!
# Actual Gibbs gradient moment and covariance lower bound

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
The covariance extension derives position L2 by strong gradient monotonicity,
then proves centered linear-score IBP and the covariance lower bound beta^-1
in every direction. It is the linear-observable Cramer-Rao corollary, with
full-space integrability proved rather than a well-behaved premise.
No general nonlinear Cramer-Rao or Brascamp-Lieb inequality is claimed.
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

private theorem gibbs_position_l2 [CompleteSpace E] {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    IsProbabilityMeasure μ ∧ MemLp (fun x : E => x) 2 μ := by
  let μ := (volume : Measure E).tilted (fun x => -U x)
  have hg := gibbs_gradient_moment hα hαβ hU hH
  have : IsProbabilityMeasure μ := hg.1
  have hgrad : Integrable (fun x => ‖gradient U x‖^2) μ := hg.2.1
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hdata := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hU hH (0 : E)
  simp only [NNReal.coe_zero,zero_div,zero_mul,add_zero] at hdata
  have ha : (0:ℝ) < α := hα
  have hbound (x : E) : ‖x‖ ≤ (‖gradient U x‖+‖gradient U (0:E)‖)/(α:ℝ) := by
    have hi := StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
      hdata.1 (fun z _ => (hd z).hasGradientAt) (x := 0) (y := x)
      (Set.mem_univ _) (Set.mem_univ _)
    simp only [sub_zero,real_inner_comm] at hi
    have hb := norm_sub_le (gradient U x) (gradient U (0:E))
    have hc := (hi.trans (real_inner_le_norm x (gradient U x-gradient U (0:E)))).trans
      (mul_le_mul_of_nonneg_left hb (norm_nonneg _))
    by_cases hz : ‖x‖=0
    · rw [hz]; positivity
    · have hn : 0<‖x‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
      apply (le_div_iff₀ ha).2
      have hh : ‖x‖*((α:ℝ)*‖x‖) ≤ ‖x‖*(‖gradient U x‖+‖gradient U (0:E)‖) := by nlinarith [hc]
      have ht := le_of_mul_le_mul_left hh hn
      nlinarith [ht]
  have hpos : Integrable (fun x : E => ‖x‖^2) μ := by
    apply ((hgrad.add (integrable_const (‖gradient U (0:E)‖^2))).const_mul (2/(α:ℝ)^2)).mono'
      (continuous_id.norm.pow 2).aestronglyMeasurable
    filter_upwards with x
    change ‖‖x‖^2‖ ≤ 2/(α:ℝ)^2*(‖gradient U x‖^2+‖gradient U (0:E)‖^2)
    rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)]
    have hs := (sq_le_sq₀ (norm_nonneg _) (by positivity)).2 (hbound x)
    have ht : (‖gradient U x‖+‖gradient U (0:E)‖)^2 ≤ 2*(‖gradient U x‖^2+‖gradient U (0:E)‖^2) := by
      nlinarith [sq_nonneg (‖gradient U x‖-‖gradient U (0:E)‖)]
    rw [div_pow] at hs
    have hh := (div_le_div_iff_of_pos_right (sq_pos_of_pos ha)).2 ht
    calc
      ‖x‖^2 ≤ (‖gradient U x‖+‖gradient U (0:E)‖)^2/(α:ℝ)^2 := hs
      _ ≤ 2*(‖gradient U x‖^2+‖gradient U (0:E)‖^2)/(α:ℝ)^2 := hh
      _ = _ := by ring
  exact ⟨inferInstance, (memLp_two_iff_integrable_sq_norm continuous_id.aestronglyMeasurable).2 hpos⟩

private theorem coordinate_position_ibp {U : E → ℝ} (hU : ContDiff ℝ 2 U)
    (p v : E) (hv : ‖v‖ = 1)
    (hw : Integrable (fun x => Real.exp (-U x)) (volume : Measure E))
    (hpos : Integrable (fun x => ‖x-p‖^2) ((volume : Measure E).tilted (fun x => -U x)))
    (hlin : Integrable (fun x => ‖x-p‖) ((volume : Measure E).tilted (fun x => -U x)))
    (hgrad : Integrable (fun x => ‖gradient U x‖^2) ((volume : Measure E).tilted (fun x => -U x))) :
    Integrable (fun x => Real.exp (-U x)*inner ℝ (x-p) v*fderiv ℝ U x v)
      (volume : Measure E) ∧
    (∫ x, Real.exp (-U x)*inner ℝ (x-p) v*fderiv ℝ U x v) =
      ∫ x, Real.exp (-U x) := by
  let f := fun x => Real.exp (-U x)
  let q := fun x => inner ℝ (x-p) v
  let a := fun x => fderiv ℝ U x v
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hf : ContDiff ℝ 1 f := (hU.of_le (by norm_num)).neg.exp
  have hq : ContDiff ℝ 1 q := (contDiff_id.sub contDiff_const).inner ℝ contDiff_const
  have hac : Continuous a :=
    (hU.fderiv_right (m := 1) (by norm_num)).continuous.clm_apply continuous_const
  have hqder (x : E) : fderiv ℝ q x v = 1 := by
    have he := ((hasFDerivAt_id x).sub_const p).inner ℝ (hasFDerivAt_const v x)
    rw [show fderiv ℝ q x = _ from he.fderiv]
    simp [hv]
  have hfder (x : E) : fderiv ℝ f x v = -f x*a x := by
    rw [show fderiv ℝ f x = _ from (hd x).hasFDerivAt.neg.exp.fderiv]
    simp only [smul_apply,neg_apply,smul_eq_mul,Pi.neg_apply]
    dsimp only [f,a]
    ring
  have hqbound (x : E) : ‖q x‖ ≤ ‖x-p‖ := by
    dsimp only [q]
    simpa only [hv,mul_one] using norm_inner_le_norm (x-p) v
  have habound (x : E) : ‖a x‖ ≤ ‖gradient U x‖ := by
    dsimp only [a]
    rw [← inner_gradient_left]
    simpa only [hv,mul_one] using norm_inner_le_norm (gradient U x) v
  have hqμ : Integrable q ((volume : Measure E).tilted (fun x => -U x)) := by
    apply hlin.mono' hq.continuous.aestronglyMeasurable
    filter_upwards with x
    exact hqbound x
  have hqaμ : Integrable (fun x => q x*a x)
      ((volume : Measure E).tilted (fun x => -U x)) := by
    apply (hpos.add hgrad).mono' (hq.continuous.mul hac).aestronglyMeasurable
    filter_upwards with x
    change ‖q x*a x‖ ≤ ‖x-p‖^2+‖gradient U x‖^2
    rw [norm_mul]
    have hi := mul_le_mul (hqbound x) (habound x) (norm_nonneg _) (norm_nonneg _)
    nlinarith [hi,sq_nonneg (‖x-p‖-‖gradient U x‖)]
  have hfq : Integrable (fun x => f x*q x) (volume : Measure E) := by
    simpa only [smul_eq_mul] using (integrable_tilted_iff hw q).1 hqμ
  have hfqa : Integrable (fun x => f x*q x*a x) (volume : Measure E) := by
    simpa only [smul_eq_mul,mul_assoc] using
      (integrable_tilted_iff hw (fun x => q x*a x)).1 hqaμ
  have hf'q : Integrable (fun x => fderiv ℝ f x v*q x) (volume : Measure E) := by
    convert hfqa.neg using 1
    ext x
    change fderiv ℝ f x v*q x = -(f x*q x*a x)
    rw [hfder]
    ring
  have hfq' : Integrable (fun x => f x*fderiv ℝ q x v) (volume : Measure E) := by
    simpa only [hqder,mul_one] using hw
  have hid := integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable hf'q hfq' hfq
    (fun x _ => hf.differentiable_one x) (fun x _ => hq.differentiable_one x)
  refine ⟨hfqa,?_⟩
  change (∫ x, f x*q x*a x) = ∫ x, f x
  calc
    (∫ x, f x*q x*a x) = -(∫ x, fderiv ℝ f x v*q x) := by
      rw [← integral_neg]
      apply integral_congr_ae
      filter_upwards with x
      rw [hfder]
      ring
    _ = ∫ x, f x*fderiv ℝ q x v := hid.symm
    _ = ∫ x, f x := by simp only [hqder,mul_one]



set_option maxHeartbeats 800000 in
private theorem gibbs_covariance_unit [CompleteSpace E] {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2)
    (v : E) (hv : ‖v‖=1) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    (β:ℝ)⁻¹ ≤ ProbabilityTheory.covarianceBilin μ v v := by
  let μ := (volume : Measure E).tilted (fun x => -U x)
  change (β:ℝ)⁻¹ ≤ ProbabilityTheory.covarianceBilin μ v v
  have hpos := gibbs_position_l2 hα hαβ hU hH
  have : IsProbabilityMeasure μ := hpos.1
  have hLp : MemLp id 2 μ := hpos.2
  let p := ∫ x, x ∂μ
  let q := fun x => inner ℝ (x-p) v
  let a := fun x => fderiv ℝ U x v
  have hw := weighted_gradient hα hU hH
  have hg := gibbs_gradient_moment hα hαβ hU hH
  have hgrad : Integrable (fun x => ‖gradient U x‖^2) μ := hg.2.1
  have hLpc : MemLp (fun x : E => x-p) 2 μ := hLp.sub (memLp_const p)
  have hsq : Integrable (fun x : E => ‖x-p‖^2) μ :=
    (memLp_two_iff_integrable_sq_norm hLpc.aestronglyMeasurable).1 hLpc
  have hlin : Integrable (fun x : E => ‖x-p‖) μ := (hLpc.integrable (by norm_num)).norm
  have hpair := coordinate_position_ibp hU p v hv hw.1 hsq hlin hgrad
  have hdiag (x : E) : 0 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ β := by
    have hh := hH x v
    rw [hv,one_pow,mul_one,mul_one] at hh
    exact ⟨(NNReal.coe_nonneg α).trans hh.1,hh.2⟩
  have hs := directional_ibp hU v hv hdiag hw.1 hw.2.1 hw.2.2
  have htilt (f : E → ℝ) : (∫ x, f x ∂μ) =
      (∫ x, Real.exp (-U x)*f x)/(∫ x, Real.exp (-U x)) := by
    rw [integral_tilted]
    simp only [smul_eq_mul]
    rw [← integral_div]
    apply integral_congr_ae
    filter_upwards with x
    ring
  have hZ := integral_exp_pos hw.1
  have ha2 : Integrable (fun x => (a x)^2) μ := by
    apply (integrable_tilted_iff hw.1 _).2
    simpa only [smul_eq_mul,a] using hs.1
  have hqa : Integrable (fun x => q x*a x) μ := by
    apply (integrable_tilted_iff hw.1 _).2
    simpa only [smul_eq_mul,mul_assoc,q,a] using hpair.1
  have hpairmean : (∫ x, q x*a x ∂μ)=1 := by
    rw [htilt]
    simp only [q,a,← mul_assoc]
    change (∫ x, Real.exp (-U x)*inner ℝ (x-p) v*fderiv ℝ U x v)/_ = 1
    rw [hpair.2,div_self hZ.ne']
  have hscore : (∫ x, (a x)^2 ∂μ) ≤ (β:ℝ) := by
    rw [htilt]
    change (∫ x, Real.exp (-U x)*(fderiv ℝ U x v)^2)/_ ≤ (β:ℝ)
    rw [hs.2.2]
    apply (div_le_iff₀ hZ).2
    have hm := integral_mono hs.2.1 (hw.1.mul_const (β:ℝ))
      (fun x => mul_le_mul_of_nonneg_left (hdiag x).2 (Real.exp_nonneg _))
    calc
      (∫ x, Real.exp (-U x)*fderiv ℝ (fderiv ℝ U) x v v) ≤
          ∫ x, Real.exp (-U x)*(β:ℝ) := hm
      _ = (β:ℝ)*(∫ x, Real.exp (-U x)) := by rw [integral_mul_const];ring
  have hqLp : MemLp q 2 μ := hLpc.inner_const (𝕜:=ℝ) v
  have hq2 := (memLp_two_iff_integrable_sq hqLp.aestronglyMeasurable).1 hqLp
  have hb : (0:ℝ)<β := lt_of_lt_of_le hα hαβ
  have hnonneg : 0 ≤ ∫ x, (a x-(β:ℝ)*q x)^2 ∂μ := integral_nonneg (fun x => sq_nonneg _)
  have hexp : (∫ x, (a x-(β:ℝ)*q x)^2 ∂μ) =
      (∫ x, (a x)^2 ∂μ)-2*(β:ℝ)*(∫ x, q x*a x ∂μ)+(β:ℝ)^2*(∫ x, (q x)^2 ∂μ) := by
    have hid : (fun x => (a x-(β:ℝ)*q x)^2) =
        (fun x => (a x)^2-2*(β:ℝ)*(q x*a x)+(β:ℝ)^2*(q x)^2) := by funext x;ring
    have hiqa : Integrable (fun x => (2*(β:ℝ))*(q x*a x)) μ :=
      hqa.const_mul (2*(β:ℝ))
    have hiq2 : Integrable (fun x => (β:ℝ)^2*(q x)^2) μ :=
      hq2.const_mul ((β:ℝ)^2)
    have hsum := integral_add (ha2.sub hiqa) hiq2
    have hsub := integral_sub ha2 hiqa
    rw [hid]
    calc
      (∫ x, (a x)^2-2*(β:ℝ)*(q x*a x)+(β:ℝ)^2*(q x)^2 ∂μ) =
          (∫ x, (a x)^2-2*(β:ℝ)*(q x*a x) ∂μ)+
          (∫ x, (β:ℝ)^2*(q x)^2 ∂μ) := by
        simpa only [Pi.sub_apply] using hsum
      _ = _ := by
        rw [hsub]
        rw [integral_const_mul (2*(β:ℝ)),integral_const_mul ((β:ℝ)^2)]
  rw [hexp,hpairmean] at hnonneg
  have hcov : ProbabilityTheory.covarianceBilin μ v v = ∫ x, (q x)^2 ∂μ := by
    rw [ProbabilityTheory.covarianceBilin_apply hLp]
    apply integral_congr_ae
    filter_upwards with x
    simp only [q,p,real_inner_comm,Function.id_def,pow_two]
  rw [hcov]
  rw [← one_div]
  apply (div_le_iff₀ hb).2
  have hprod : (β:ℝ)^2*(∫ x, (q x)^2 ∂μ) ≥ (β:ℝ) := by nlinarith [hscore,hnonneg]
  have hh : (β:ℝ)*1 ≤ (β:ℝ)*((β:ℝ)*(∫ x, (q x)^2 ∂μ)) := by nlinarith [hprod]
  have ht := le_of_mul_le_mul_left hh hb
  nlinarith [ht]


/-- Actual Gibbs covariance lower bound in every direction, with probability
and position L2 derived from genuine Hessian bounds. No Fisher-information,
score-pairing, moment or covariance certificate is supplied. -/
theorem gibbs_covariance_lower [CompleteSpace E] {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    IsProbabilityMeasure μ ∧ MemLp id 2 μ ∧
      ∀ v : E, ‖v‖^2/(β:ℝ) ≤ ProbabilityTheory.covarianceBilin μ v v := by
  let μ := (volume : Measure E).tilted (fun x => -U x)
  have hp := gibbs_position_l2 hα hαβ hU hH
  refine ⟨hp.1,hp.2,?_⟩
  intro v
  by_cases hvzero : v=0
  · subst v
    simp
  · have hn : ‖v‖≠0 := norm_ne_zero_iff.mpr hvzero
    let u := ‖v‖⁻¹ • v
    have hu : ‖u‖=1 := by
      dsimp only [u]
      rw [norm_smul,Real.norm_eq_abs,abs_inv,abs_of_nonneg (norm_nonneg v),inv_mul_cancel₀ hn]
    have hv : ‖v‖ • u = v := by
      dsimp only [u]
      rw [smul_smul,mul_inv_cancel₀ hn,one_smul]
    have hc := gibbs_covariance_unit hα hαβ hU hH u hu
    have hscale : ProbabilityTheory.covarianceBilin μ v v =
        ‖v‖^2*ProbabilityTheory.covarianceBilin μ u u := by
      calc
        ProbabilityTheory.covarianceBilin μ v v =
            ProbabilityTheory.covarianceBilin μ (‖v‖ • u) (‖v‖ • u) := by rw [hv]
        _ = _ := by
          simp only [map_smul,smul_apply,smul_eq_mul]
          ring
    rw [hscale,div_eq_mul_inv]
    exact mul_le_mul_of_nonneg_left hc (sq_nonneg _)


end AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment
