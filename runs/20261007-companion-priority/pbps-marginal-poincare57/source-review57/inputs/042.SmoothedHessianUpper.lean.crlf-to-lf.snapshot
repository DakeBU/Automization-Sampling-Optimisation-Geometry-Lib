import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment
import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential

/-!
# Actual smoothed Hessian upper bound

SPHMC arXiv:2609.06906v1 Section4.1 Lemma4.1, Cramer-Rao half.
The genuine quadratic posterior has Hessian between alpha+eta^-1 and
beta+eta^-1. Its derived covariance lower bound and the true Gaussian
posterior Hessian identity imply the source UNNORMALIZED V_eta has Hessian
at most beta/(1+beta eta). This gives exactly (1+eta)^-1 for source beta=1.
Generic alpha/beta and every eta>0 are explicit extensions of the source.
No moment, normalizer, derivative or covariance estimate is an input.
Brascamp-Lieb/Hessian lower, full Lemma4.1, higher regularity, numerical
accuracy/history/expected work and both complete main/composition remain open.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper

open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal
noncomputable section
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] [CompleteSpace E]

/-- Cramer-Rao half of SPHMC Lemma4.1 for the actual RGO posterior and
source unnormalized smoothed potential. Generic alpha/beta and all eta>0
are explicit generalizations; covariance upper/Hessian lower is separate. -/
theorem smoothed_hessian_upper {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0<α) (hαβ : α≤β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (α:ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ (β:ℝ)*‖v‖^2) (hη : 0<η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
    let Vη := fun y => -Real.log (A y)
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    (∀ y v, ‖v‖^2/((β:ℝ)+η⁻¹) ≤ covarianceBilin (R y) v v) ∧
      ∀ y v, fderiv ℝ (fderiv ℝ Vη) y v v ≤ ((β:ℝ)/(1+(β:ℝ)*η))*‖v‖^2 := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
  let r : ℝ≥0 := ⟨η⁻¹,(inv_pos.mpr hη).le⟩
  have hr : (r:ℝ)=η⁻¹ := rfl
  have ha : (0:ℝ)<α := hα
  have h0 := AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
    (r:=0) hV hH (0:E)
  simp only [NNReal.coe_zero,zero_div,zero_mul,add_zero] at h0
  have hi := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    ha (hV.differentiable (by norm_num)) h0.1
  have hR (y : E) : ∀ v : E, ‖v‖^2/((β:ℝ)+η⁻¹) ≤ covarianceBilin (R y) v v := by
    let W := fun x => V x+(r:ℝ)/2*‖x-y‖^2
    have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
    have hVdd : Differentiable ℝ (fderiv ℝ V) := (hV.fderiv_right (m:=1) (by norm_num)).differentiable_one
    have hW : ContDiff ℝ 2 W := hV.add (contDiff_const.mul ((contDiff_id.sub contDiff_const).norm_sq (𝕜:=ℝ)))
    have hq (x : E) : HasFDerivAt (fun z => (r:ℝ)/2*‖z-y‖^2)
        ((r:ℝ) • innerSL ℝ (x-y)) x := by
      convert (((hasFDerivAt_id x).sub_const y).norm_sq).const_mul ((r:ℝ)/2)
        using 1 <;> first | rfl | (ext v; simp;ring)
    have hWfd (x : E) : fderiv ℝ W x = fderiv ℝ V x+(r:ℝ) • innerSL ℝ (x-y) :=
      ((hVd x).hasFDerivAt.add (hq x)).fderiv
    let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
      {toFun := fun v => innerSL ℝ v
       map_add' := by intros;ext;simp
       map_smul' := by intros;ext;simp
       cont := (innerSL ℝ (E:=E)).continuous}
    have hWdd (x : E) : HasFDerivAt (fderiv ℝ W)
        (fderiv ℝ (fderiv ℝ V) x+(r:ℝ) • J) x := by
      rw [show fderiv ℝ W=(fun z => fderiv ℝ V z+(r:ℝ) • innerSL ℝ (z-y)) from funext hWfd]
      convert (hVdd x).hasFDerivAt.add ((J.hasFDerivAt.comp x ((hasFDerivAt_id x).sub_const y)).const_smul (r:ℝ)) using 1 <;> rfl
    have hb (x v : E) : ((α+r:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ W) x v v ∧
        fderiv ℝ (fderiv ℝ W) x v v ≤ ((β+r:ℝ≥0):ℝ)*‖v‖^2 := by
      rw [(hWdd x).fderiv]
      change ((α:ℝ)+r)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v+(r:ℝ)*inner ℝ v v ∧
        fderiv ℝ (fderiv ℝ V) x v v+(r:ℝ)*inner ℝ v v ≤ ((β:ℝ)+r)*‖v‖^2
      rw [real_inner_self_eq_norm_sq]
      constructor <;> nlinarith [(hH x v).1,(hH x v).2]
    have hc := AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMoment.gibbs_covariance_lower
      (show 0<α+r from by positivity) (show α+r≤β+r from by simpa only [add_comm] using (add_le_add_right hαβ r)) hW hb
    have hRW : R y=(volume : Measure E).tilted (fun x => -W x) := by
      dsimp only [R,μ]
      rw [tilted_tilted hi]
      congr 1
      funext x
      simp only [Pi.add_apply,W]
      rw [hr]
      field_simp [hη.ne']
      ring
    rw [hRW]
    simpa only [NNReal.coe_add,hr] using hc.2.2
  refine ⟨hR,?_⟩
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
  let Vη := fun y => -Real.log (A y)
  let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  obtain ⟨_hZ,hμ,_hlaw,_hI,_hInt,_hTilt,_hA,_hC2,hshift⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential.smoothed_gibbs_potential
      ha hV (fun x v => (hH x v).1) hη
  have : IsProbabilityMeasure μ := hμ
  have hC : 0<C := by dsimp only [C]; positivity
  obtain ⟨_hRm,_hD,hDD⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_derivatives μ hη hC
  have he : U=(fun y => Vη y+Real.log ZV) := funext hshift
  have hd : fderiv ℝ U=fderiv ℝ Vη := by
    rw [he]
    funext y
    exact fderiv_add_const _
  change ∀ y v w, fderiv ℝ (fderiv ℝ U) y v w = _ at hDD
  rw [hd] at hDD
  intro y v
  rw [hDD y v v,real_inner_self_eq_norm_sq]
  have hden : 0<(β:ℝ)+η⁻¹ := add_pos_of_nonneg_of_pos β.coe_nonneg (inv_pos.mpr hη)
  have hbden : 0<1+(β:ℝ)*η := by positivity
  calc
    ‖v‖^2/η-covarianceBilin (R y) v v/η^2 ≤
        ‖v‖^2/η-(‖v‖^2/((β:ℝ)+η⁻¹))/η^2 :=
      sub_le_sub_left (div_le_div_of_nonneg_right (hR y v) (sq_nonneg η)) _
    _ = ((β:ℝ)/(1+(β:ℝ)*η))*‖v‖^2 := by
      field_simp [hη.ne',hden.ne',hbden.ne']
      ring

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper
