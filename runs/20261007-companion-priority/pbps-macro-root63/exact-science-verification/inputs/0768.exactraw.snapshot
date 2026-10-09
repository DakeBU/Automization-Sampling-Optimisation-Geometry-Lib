import AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher

/-!
# True smoothed score and posterior expectation

Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1, Section3.1 and unnumbered
S4.Ex9. The actual everywhere quadratic posterior, rather than a chosen
almost-everywhere conditional representative, supplies the gradient mean.
The source unnormalized convolution potential differs from the normalized
potential by a constant log partition. That constant is retained until
differentiation. All positive eta, the same produced proximal selector, and
the same real affine standardized posterior are used throughout.

This is a mean identity and exact evaluator chain rule. It does not prove
bias(4.2), first(4.6) Wasserstein/Fisher, Gaussian LSI/T2, the full oracle
lemma, any HMC approximation, either main theorem, or expected query costs.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior

open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

omit [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] in
private theorem rho_gradient {V : E → ℝ} (hV : ContDiff ℝ 2 V)
    (p : E) (η : ℝ) (u : E) :
    gradient (fun z => V (p+Real.sqrt η • z)-V p-
      Real.sqrt η*inner ℝ (gradient V p) z) u =
      Real.sqrt η • (gradient V (p+Real.sqrt η • u)-gradient V p) := by
  have hd : Differentiable ℝ V := hV.differentiable (by norm_num)
  have hc := (hd (p+Real.sqrt η • u)).hasFDerivAt.comp u
    ((hasFDerivAt_const p u).add ((hasFDerivAt_id u).const_smul (Real.sqrt η)))
  have hl := ((innerSL ℝ (gradient V p)).hasFDerivAt (x := u)).const_mul (Real.sqrt η)
  have hh := (hc.sub_const (V p)).sub hl
  apply ext_inner_right ℝ
  intro v
  rw [inner_gradient_left]
  rw [show fderiv ℝ (fun z => V (p+Real.sqrt η • z)-V p-
    Real.sqrt η*inner ℝ (gradient V p) z) u = _ from hh.fderiv]
  simp only [sub_apply,ContinuousLinearMap.comp_apply,smul_apply,
    ContinuousLinearMap.id_apply,
    zero_add,innerSL_apply_apply,real_inner_smul_left,inner_sub_left,smul_eq_mul]
  rw [← inner_gradient_left]
  simp only [real_inner_smul_right]
  ring

theorem smoothed_score_posterior
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ η : ℝ} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2) (hη : 0 < η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
    let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
    let Vη := fun y : E => -Real.log (A y)
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    IsProbabilityMeasure μ ∧ ContDiff ℝ 2 Vη ∧
      (∀ y, IsProbabilityMeasure (R y) ∧ MemLp id 2 (R y) ∧
        Integrable (gradient V) (R y) ∧
        gradient Vη y = ∫ x, gradient V x ∂(R y)) ∧
      ∃ p : E → E, Measurable p ∧ (∀ y, p y+η • gradient V (p y)=y) ∧
        let rho := fun y u => V (p y+Real.sqrt η • u)-V (p y)-
          Real.sqrt η*inner ℝ (gradient V (p y)) u
        let r := fun y => (R y).map (fun x => (Real.sqrt η)⁻¹ • (x-p y))
        ∀ y, r y=(volume : Measure E).tilted (fun u => -(‖u‖^2/2+rho y u)) ∧
          IsProbabilityMeasure (r y) ∧ MemLp (gradient (rho y)) 2 (r y) ∧
          gradient Vη y=gradient V (p y)+(Real.sqrt η)⁻¹ • (∫ u, gradient (rho y) u ∂(r y)) ∧
          ∀ z, gradient V (p y+Real.sqrt η • z)=
            gradient V (p y)+(Real.sqrt η)⁻¹ • gradient (rho y) z := by
  have hk : 0 < κ := lt_of_lt_of_le zero_lt_one hκ
  have ha : 0 < κ⁻¹ := inv_pos.mpr hk
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
  let Vη := fun y : E => -Real.log (A y)
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
  let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  obtain ⟨_hZ,hμ,_hlaw,_hI,_hInt,_hTilt,_hA,hC2,hshift⟩ :=
    SmoothedGibbsPotential.smoothed_gibbs_potential ha hV (fun x a => (hH x a).1) hη
  have : IsProbabilityMeasure μ := hμ
  have hC : 0 < C := by dsimp only [C]; positivity
  obtain ⟨hRm,hD,_hDD⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_derivatives μ hη hC
  have hi := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    ha (hV.differentiable (by norm_num))
    (AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (fun x a => (hH x a).1))
  have hshiftfun : U = (fun y => Vη y+Real.log ZV) := funext hshift
  have hDU : fderiv ℝ U = fderiv ℝ Vη := by
    rw [hshiftfun]
    funext y
    exact fderiv_add_const _
  have hscore (y : E) : Integrable (gradient V) (R y) ∧
      gradient Vη y = ∫ x, gradient V x ∂(R y) := by
    let W := fun x => V x+η⁻¹/2*‖x-y‖^2
    have hW : ContDiff ℝ 2 W := hV.add (contDiff_const.mul ((contDiff_id.sub contDiff_const).norm_sq (𝕜 := ℝ)))
    have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
    have hVdd : Differentiable ℝ (fderiv ℝ V) := (hV.fderiv_right (m := 1) (by norm_num)).differentiable_one
    have hq (x : E) : HasFDerivAt (fun z => η⁻¹/2*‖z-y‖^2)
        (η⁻¹ • innerSL ℝ (x-y)) x := by
      convert (((hasFDerivAt_id x).sub_const y).norm_sq).const_mul (η⁻¹/2)
        using 1 <;> first | rfl | (ext a; simp; ring)
    have hWfd (x : E) : fderiv ℝ W x = fderiv ℝ V x+η⁻¹ • innerSL ℝ (x-y) :=
      ((hVd x).hasFDerivAt.add (hq x)).fderiv
    let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
      {toFun := fun a => innerSL ℝ a
       map_add' := by intros; ext; simp
       map_smul' := by intros; ext; simp
       cont := (innerSL ℝ (E := E)).continuous}
    have hWdd (x : E) : HasFDerivAt (fderiv ℝ W)
        (fderiv ℝ (fderiv ℝ V) x+η⁻¹ • J) x := by
      rw [show fderiv ℝ W=(fun z => fderiv ℝ V z+η⁻¹ • innerSL ℝ (z-y)) from funext hWfd]
      convert (hVdd x).hasFDerivAt.add ((J.hasFDerivAt.comp x ((hasFDerivAt_id x).sub_const y)).const_smul η⁻¹) using 1 <;> rfl
    have hb (x a : E) : (κ⁻¹+η⁻¹)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a ∧
        fderiv ℝ (fderiv ℝ W) x a a ≤ (1+η⁻¹)*‖a‖^2 := by
      rw [(hWdd x).fderiv]
      change (κ⁻¹+η⁻¹)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ V) x a a+η⁻¹*inner ℝ a a ∧
        fderiv ℝ (fderiv ℝ V) x a a+η⁻¹*inner ℝ a a ≤ (1+η⁻¹)*‖a‖^2
      rw [real_inner_self_eq_norm_sq]
      constructor <;> nlinarith [(hH x a).1,(hH x a).2]
    have hgradW (x : E) : gradient W x = gradient V x+η⁻¹ • (x-y) := by
      apply ext_inner_right ℝ
      intro a
      rw [inner_gradient_left,hWfd]
      simp only [add_apply,smul_apply,innerSL_apply_apply,inner_add_left,real_inner_smul_left,inner_gradient_left,smul_eq_mul]
    let α : ℝ≥0 := ⟨κ⁻¹+η⁻¹,by positivity⟩
    let β : ℝ≥0 := ⟨1+η⁻¹,by positivity⟩
    have hα : 0 < α := by change 0 < κ⁻¹+η⁻¹; positivity
    have hmean := AutoSamplingTheory.TechnicalLemmas.Analysis.GibbsGradientMean.integrable_gradient_and_integral_eq_zero
      (α := α) (β := β) hα hW hb
    have hRW : R y=(volume : Measure E).tilted (fun x => -W x) := by
      dsimp only [R,μ]
      rw [tilted_tilted hi]
      congr 1
      funext x
      simp only [Pi.add_apply,W]
      field_simp [hη.ne']
      ring
    have : IsProbabilityMeasure (R y) := (hRm y).1
    have hX : Integrable (fun x : E => x) (R y) := (hRm y).2.integrable (by norm_num)
    have hqint : Integrable (fun x => η⁻¹ • (x-y)) (R y) :=
      (hX.sub (integrable_const y)).smul η⁻¹
    have hgw : Integrable (gradient W) (R y) := hRW.symm ▸ hmean.2.1
    have hgv : Integrable (gradient V) (R y) := by
      convert hgw.sub hqint using 1
      funext x
      change gradient V x = gradient W x-η⁻¹ • (x-y)
      rw [hgradW]
      abel
    have hz : (∫ x, gradient V x ∂(R y))+η⁻¹ • ((∫ x, x ∂(R y))-y) = 0 := by
      have he : (∫ x, gradient W x ∂(R y)) = 0 := hRW.symm ▸ hmean.2.2
      simp_rw [hgradW] at he
      rw [integral_add hgv hqint,integral_smul,integral_sub hX (integrable_const y)] at he
      simpa only [integral_const,probReal_univ,one_smul] using he
    have hemean : (∫ x, gradient V x ∂(R y)) = η⁻¹ • (y-∫ x, x ∂(R y)) := by
      calc
        _ = -(η⁻¹ • ((∫ x, x ∂(R y))-y)) := eq_neg_of_add_eq_zero_left hz
        _ = _ := by rw [← smul_neg,neg_sub]
    refine ⟨hgv,?_⟩
    rw [hemean]
    apply ext_inner_right ℝ
    intro v
    rw [inner_gradient_left,← hDU,hD]
    simp only [real_inner_smul_left]
    change inner ℝ (y-∫ x,x ∂(R y)) v/η = η⁻¹*inner ℝ (y-∫ x,x ∂(R y)) v
    ring
  refine ⟨hμ,hC2,(fun y => ⟨(hRm y).1,(hRm y).2,(hscore y).1,(hscore y).2⟩),?_⟩
  obtain ⟨p,hpm,hstat,hstd⟩ :=
    StandardizedRGOPositionFisher.standardized_rgo_position_and_fisher hκ hV hH
      (eta := fun _ : E => η) (y := fun x => x) measurable_const measurable_id (fun _ => hη)
  refine ⟨p,hpm,hstat,?_⟩
  let rho := fun y u => V (p y+Real.sqrt η • u)-V (p y)-
    Real.sqrt η*inner ℝ (gradient V (p y)) u
  let r := fun y => (R y).map (fun x => (Real.sqrt η)⁻¹ • (x-p y))
  change ∀ y, r y=(volume : Measure E).tilted (fun u => -(‖u‖^2/2+rho y u)) ∧
    IsProbabilityMeasure (r y) ∧ MemLp (gradient (rho y)) 2 (r y) ∧
    gradient Vη y=gradient V (p y)+(Real.sqrt η)⁻¹ • (∫ u, gradient (rho y) u ∂(r y)) ∧
    ∀ z, gradient V (p y+Real.sqrt η • z)=
      gradient V (p y)+(Real.sqrt η)⁻¹ • gradient (rho y) z
  intro y
  obtain ⟨_hRp,_hρ,_hQ,_hρ0,_hQ0,_hρH,_hQH,hrlaw,hrp,_hrX,_hrXI,_hrXb,hrρ,_hrρa,_hrρb⟩ := hstd.2 y
  have : IsProbabilityMeasure (r y) := hrp
  have heval (z : E) : gradient V (p y+Real.sqrt η • z) =
      gradient V (p y)+(Real.sqrt η)⁻¹ • gradient (rho y) z := by
    have hρ := rho_gradient hV (p y) η z
    change gradient (rho y) z = _ at hρ
    rw [hρ,smul_smul,inv_mul_cancel₀ (Real.sqrt_pos.mpr hη).ne',one_smul]
    abel
  refine ⟨hrlaw,hrp,hrρ,?_,heval⟩
  have hρint : Integrable (gradient (rho y)) (r y) := hrρ.integrable (by norm_num)
  have hρscaled : Integrable (fun u => (Real.sqrt η)⁻¹ • gradient (rho y) u) (r y) :=
    hρint.smul (Real.sqrt η)⁻¹
  have hconst : Integrable (fun _ : E => gradient V (p y)) (r y) := integrable_const _
  have hFint : Integrable (fun u => gradient V (p y+Real.sqrt η • u)) (r y) := by
    convert hconst.add hρscaled using 1 <;> try rfl
    funext u
    change gradient V (p y+Real.sqrt η • u)=gradient V (p y)+(Real.sqrt η)⁻¹ • gradient (rho y) u
    exact heval u
  have hmap : (∫ u, gradient V (p y+Real.sqrt η • u) ∂(r y)) =
      ∫ x, gradient V x ∂(R y) := by
    rw [show r y=(R y).map (fun x => (Real.sqrt η)⁻¹ • (x-p y)) from rfl,
      integral_map (by fun_prop) hFint.aestronglyMeasurable]
    apply integral_congr_ae
    filter_upwards with x
    congr 1
    rw [smul_smul,mul_inv_cancel₀ (Real.sqrt_pos.mpr hη).ne',one_smul]
    abel
  rw [(hscore y).2,← hmap]
  simp_rw [heval]
  rw [integral_add hconst hρscaled,integral_smul,
    integral_const,probReal_univ,one_smul]

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedScorePosterior
