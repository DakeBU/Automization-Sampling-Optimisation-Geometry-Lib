import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment
import Mathlib.Analysis.Calculus.LineDeriv.IntegrationByParts
import Mathlib.Tactic

/-!
# Actual Gibbs position moment at a stationary point

A source-backed position-moment component for Lemma 4.2, equation (4.6), of
Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1. The actual normalized Gibbs
measure is constructed from the potential. All required noncompact L1 facts
precede directional integration by parts. Finite orthonormal-basis summation
proves the exact position-gradient identity, then positive curvature gives
the sharp dimension/curvature position moment.

The genuine C2 Hessian contract and supplied actual stationary point are
explicit. General positive lower and finite upper curvature, arbitrary
stationary point, and coordinate-free dimension zero are extensions of the
paper consumer, not a claim of the weakest possible hypotheses. The source
standardized potential has stationary point zero by linear-term cancellation.
Its identification with the affine image of the true RGO still needs the
proximal equation and a separate measure transport proof. Gaussian
transport-Fisher, smoothed-score identification, estimator bias, Picard
accuracy and query costs are not established here.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.GibbsPositionMoment

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [CompleteSpace E]

open AutoSamplingTheory.TechnicalLemmas.Analysis

private theorem stationary_position_integrability {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2)
    (p : E) (hp : gradient U p = 0) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    IsProbabilityMeasure μ ∧
    Integrable (fun x => Real.exp (-U x)) (volume : Measure E) ∧
    Integrable (fun x => ‖x-p‖^2) μ ∧
    Integrable (fun x => ‖x-p‖) μ ∧
    Integrable (fun x => inner ℝ (x-p) (gradient U x)) μ ∧
    (∀ x, (α : ℝ)*‖x-p‖^2 ≤ inner ℝ (x-p) (gradient U x)) := by
  let μ := (volume : Measure E).tilted (fun x => -U x)
  have ha : (0 : ℝ) < α := hα
  have hd : Differentiable ℝ U := hU.differentiable (by norm_num)
  have hc : Continuous (gradient U) :=
    Calculus.Gradient.continuous_gradient_of_contDiff_one (hU.of_le (by norm_num))
  have hdata := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r := 0) hU hH (0 : E)
  simp only [NNReal.coe_zero, zero_div, zero_mul, add_zero] at hdata
  have hg := GibbsGradientMoment.gibbs_gradient_moment hα hαβ hU hH
  have hprob : IsProbabilityMeasure μ := hg.1
  let : IsProbabilityMeasure μ := hprob
  have hgrad : Integrable (fun x => ‖gradient U x‖^2) μ := hg.2.1
  have hweight := StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    ha hd hdata.1
  have hcoercive (x : E) : (α : ℝ)*‖x-p‖^2 ≤ inner ℝ (x-p) (gradient U x) := by
    have hi := StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn
      hdata.1 (fun z _ => (hd z).hasGradientAt) (x := p) (y := x)
      (Set.mem_univ _) (Set.mem_univ _)
    simpa only [hp,sub_zero,real_inner_comm] using hi
  have hbound (x : E) : ‖x-p‖ ≤ ‖gradient U x‖/(α : ℝ) := by
    have hi := (hcoercive x).trans (real_inner_le_norm (x-p) (gradient U x))
    by_cases hz : ‖x-p‖ = 0
    · rw [hz]; positivity
    · have hn : 0 < ‖x-p‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hz)
      apply (le_div_iff₀ ha).2
      have hm : ‖x-p‖*((α : ℝ)*‖x-p‖) ≤ ‖x-p‖*‖gradient U x‖ := by
        nlinarith [hi]
      have hh := le_of_mul_le_mul_left hm hn
      nlinarith [hh]
  have hpos : Integrable (fun x => ‖x-p‖^2) μ := by
    apply (hgrad.div_const ((α : ℝ)^2)).mono'
      (((continuous_id.sub continuous_const).norm.pow 2).aestronglyMeasurable)
    filter_upwards with x
    change ‖‖x-p‖^2‖ ≤ ‖gradient U x‖^2/(α : ℝ)^2
    rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _),← div_pow]
    exact (sq_le_sq₀ (norm_nonneg _) (by positivity)).2 (hbound x)
  have hlin : Integrable (fun x => ‖x-p‖) μ := by
    apply ((integrable_const (1 : ℝ)).add hpos).mono'
      ((continuous_id.sub continuous_const).norm.aestronglyMeasurable)
    filter_upwards with x
    change ‖‖x-p‖‖ ≤ 1+‖x-p‖^2
    rw [norm_norm]
    nlinarith [sq_nonneg (‖x-p‖-1)]
  have hpair : Integrable (fun x => inner ℝ (x-p) (gradient U x)) μ := by
    apply (hpos.add hgrad).mono'
      (((continuous_id.sub continuous_const).inner hc).aestronglyMeasurable)
    filter_upwards with x
    change ‖inner ℝ (x-p) (gradient U x)‖ ≤ ‖x-p‖^2+‖gradient U x‖^2
    have hi : ‖inner ℝ (x-p) (gradient U x)‖ ≤ ‖x-p‖*‖gradient U x‖ := norm_inner_le_norm (x-p) (gradient U x)
    nlinarith [hi,sq_nonneg (‖x-p‖-‖gradient U x‖)]
  exact ⟨hprob,hweight,hpos,hlin,hpair,hcoercive⟩


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


/-- Actual Gibbs normalization, position/pairing integrability, exact
position-gradient moment, and sharp dimension/curvature position bound. -/
theorem gibbs_position_moment {U : E → ℝ} {α β : ℝ≥0}
    (hα : 0 < α) (hαβ : α ≤ β) (hU : ContDiff ℝ 2 U)
    (hH : ∀ x v : E, (α : ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ U) x v v ∧
      fderiv ℝ (fderiv ℝ U) x v v ≤ (β : ℝ)*‖v‖^2)
    (p : E) (hp : gradient U p = 0) :
    let μ := (volume : Measure E).tilted (fun x => -U x)
    IsProbabilityMeasure μ ∧
    Integrable (fun x => Real.exp (-U x)) (volume : Measure E) ∧
    0 < (∫ x, Real.exp (-U x)) ∧
    Integrable (fun x => ‖x-p‖^2) μ ∧
    Integrable (fun x => inner ℝ (x-p) (gradient U x)) μ ∧
    (∫ x, inner ℝ (x-p) (gradient U x) ∂μ) = Module.finrank ℝ E ∧
    (∫ x, ‖x-p‖^2 ∂μ) ≤ (Module.finrank ℝ E : ℝ)/(α : ℝ) := by
  classical
  let μ := (volume : Measure E).tilted (fun x => -U x)
  let b := stdOrthonormalBasis ℝ E
  rcases stationary_position_integrability hα hαβ hU hH p hp with
    ⟨hprob,hw,hpos,hlin,hpair,hcoerce⟩
  have hgrad := (GibbsGradientMoment.gibbs_gradient_moment hα hαβ hU hH).2.1
  have hdir (i) := coordinate_position_ibp hU p (b i) (b.orthonormal.norm_eq_one i)
    hw hpos hlin hgrad
  have hparseval (x : E) :
      (∑ i, inner ℝ (x-p) (b i)*fderiv ℝ U x (b i)) = inner ℝ (x-p) (gradient U x) := by
    simpa [inner_gradient_right] using b.sum_inner_mul_inner (x-p) (gradient U x)
  have heq : (∫ x, Real.exp (-U x)*inner ℝ (x-p) (gradient U x)) =
      (Module.finrank ℝ E : ℝ)*(∫ x, Real.exp (-U x)) := by
    calc
      (∫ x, Real.exp (-U x)*inner ℝ (x-p) (gradient U x)) =
          ∫ x, ∑ i, Real.exp (-U x)*inner ℝ (x-p) (b i)*fderiv ℝ U x (b i) := by
        apply integral_congr_ae
        filter_upwards with x
        rw [← hparseval x,Finset.mul_sum]
        simp only [mul_assoc]
      _ = ∑ i, ∫ x, Real.exp (-U x)*inner ℝ (x-p) (b i)*fderiv ℝ U x (b i) :=
        integral_finsetSum _ (fun i _ => (hdir i).1)
      _ = ∑ _i : Fin (Module.finrank ℝ E), ∫ x, Real.exp (-U x) := by
        apply Finset.sum_congr rfl
        intro i _
        exact (hdir i).2
      _ = (Module.finrank ℝ E : ℝ)*(∫ x, Real.exp (-U x)) := by simp
  have hZ : 0 < (∫ x, Real.exp (-U x)) := integral_exp_pos hw
  have htilt (g : E → ℝ) : (∫ x, g x ∂μ) =
      (∫ x, Real.exp (-U x)*g x)/(∫ x, Real.exp (-U x)) := by
    rw [integral_tilted]
    simp only [smul_eq_mul]
    rw [← integral_div]
    apply integral_congr_ae
    filter_upwards with x
    ring
  have hid : (∫ x, inner ℝ (x-p) (gradient U x) ∂μ) = Module.finrank ℝ E := by
    rw [htilt,heq]
    exact mul_div_cancel_right₀ _ hZ.ne'
  refine ⟨hprob,hw,hZ,hpos,hpair,hid,?_⟩
  have hi := integral_mono (hpos.const_mul (α : ℝ)) hpair hcoerce
  rw [integral_const_mul] at hi
  change (∫ x, inner ℝ (x-p) (gradient U x) ∂μ) = Module.finrank ℝ E at hid
  rw [hid] at hi
  apply (le_div_iff₀ (show (0 : ℝ) < α from hα)).2
  nlinarith [hi]


end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.GibbsPositionMoment
