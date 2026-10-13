import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CenteredDomainPoincare
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper

/-!
# Actual centered Poincare for the Gaussian Gibbs marginal

PBPS arXiv:2609.06905v1 Eq2.13, D.6/D.10 and C.3. The positive C2
normalized marginal is derived from the actual Gibbs/Gaussian law. Posterior
covariance upper and the existing exact smoothed Hessian upper producer give
alpha/(1+alpha eta) and beta/(1+beta eta); all moment, partition and law
adapters are internal. Existing original-domain Poincare is consumed on one
genuine smooth-compact gradient closure selected before all centered inputs.
Original C2/two Hessian bounds and positive capped eta remain. Finite Hilbert,
Borel and rank0 are explicit extensions. This does not identify full weighted
H1, macro range, Gamma/inverses, dynamics, mixing, main results or query costs.
-/

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
open Set MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff NNReal Topology
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 1600000

theorem actual_gaussian_marginal_centered_poincare
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2)
    (hη : 0 < η) (hβη : (β : ℝ)*η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    let ν := J.snd
    IsProbabilityMeasure ν ∧
      ∃ G : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν,
        Dense (G.domain : Set (Lp ℝ 2 ν)) ∧ G.IsClosable ∧ G.closure.IsClosed ∧
        (∀ (u : Lp ℝ 2 ν) (v : Lp E 2 ν), (u,v) ∈ G.graph ↔
          ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
            u =ᵐ[ν] φ ∧ v =ᵐ[ν] gradient φ) ∧
        ∀ z : G.closure.domain,
          (∫ x, (z : Lp ℝ 2 ν) x ∂ν) = 0 →
          ((α : ℝ)/(1+(α : ℝ)*η))*‖(z : Lp ℝ 2 ν)‖^2 ≤ ‖G.closure z‖^2 := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := (μ.prod (stdGaussian E)).map
    (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
  let ν := J.snd
  let C := ((Real.sqrt (2*Real.pi*η))⁻¹)^Module.finrank ℝ E
  let A := fun y : E => C*∫ x, Real.exp (-V x-‖y-x‖^2/(2*η)) ∂(volume : Measure E)
  let Vη := fun y : E => -Real.log (A y)
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
  let U := fun y : E => -Real.log (C*∫ x, Real.exp (-‖y-x‖^2/(2*η)) ∂μ)
  let ZV := ∫ x, Real.exp (-V x) ∂(volume : Measure E)
  obtain ⟨hZ,hμ,_hlaw,hIA,hIntA,hTilt,hA,hC2,hshift⟩ :=
    AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedGibbsPotential.smoothed_gibbs_potential
      hα hV (fun x a => (hH x a).1) hη
  letI : IsProbabilityMeasure μ := hμ
  have hpair : Measurable (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) := by fun_prop
  letI : IsProbabilityMeasure J := Measure.isProbabilityMeasure_map hpair.aemeasurable
  letI : IsProbabilityMeasure ν := Measure.isProbabilityMeasure_map measurable_snd.aemeasurable
  have htilt : ν = (volume : Measure E).tilted (fun y => -Vη y) :=
    (Measure.map_map measurable_snd hpair).trans hTilt
  have hC : 0<C := by dsimp only [C]; positivity
  obtain ⟨hRm,_hD,hDD⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_derivatives μ hη hC
  have hi := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    hα (hV.differentiable (by norm_num))
    (AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (fun x a => (hH x a).1))
  have hcov (y : E) : ∀ a : E, covarianceBilin (R y) a a ≤ ‖a‖^2/((α : ℝ)+η⁻¹) := by
    let W := fun x => V x+η⁻¹/2*‖x-y‖^2
    have hW : ContDiff ℝ 2 W := hV.add (contDiff_const.mul ((contDiff_id.sub contDiff_const).norm_sq (𝕜:=ℝ)))
    have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
    have hVdd : Differentiable ℝ (fderiv ℝ V) := (hV.fderiv_right (m:=1) (by norm_num)).differentiable_one
    have hq (x : E) : HasFDerivAt (fun z => η⁻¹/2*‖z-y‖^2)
        (η⁻¹ • innerSL ℝ (x-y)) x := by
      convert (((hasFDerivAt_id x).sub_const y).norm_sq).const_mul (η⁻¹/2)
        using 1 <;> first | rfl | (ext a; simp;ring)
    have hWfd (x : E) : fderiv ℝ W x = fderiv ℝ V x+η⁻¹ • innerSL ℝ (x-y) :=
      ((hVd x).hasFDerivAt.add (hq x)).fderiv
    let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
      {toFun := fun a => innerSL ℝ a
       map_add' := by intros;ext;simp
       map_smul' := by intros;ext;simp
       cont := (innerSL ℝ (E:=E)).continuous}
    have hWdd (x : E) : HasFDerivAt (fderiv ℝ W)
        (fderiv ℝ (fderiv ℝ V) x+η⁻¹ • J) x := by
      rw [show fderiv ℝ W=(fun z => fderiv ℝ V z+η⁻¹ • innerSL ℝ (z-y)) from funext hWfd]
      convert (hVdd x).hasFDerivAt.add ((J.hasFDerivAt.comp x ((hasFDerivAt_id x).sub_const y)).const_smul η⁻¹) using 1 <;> rfl
    have hb (x a : E) : ((α : ℝ)+η⁻¹)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ W) x a a ∧
        fderiv ℝ (fderiv ℝ W) x a a ≤ ((β : ℝ)+η⁻¹)*‖a‖^2 := by
      rw [(hWdd x).fderiv]
      change ((α : ℝ)+η⁻¹)*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ V) x a a+η⁻¹*inner ℝ a a ∧
        fderiv ℝ (fderiv ℝ V) x a a+η⁻¹*inner ℝ a a ≤ ((β : ℝ)+η⁻¹)*‖a‖^2
      rw [real_inner_self_eq_norm_sq]
      constructor <;> nlinarith [(hH x a).1,(hH x a).2]
    have hm : 0<(α : ℝ)+η⁻¹ := add_pos hα (inv_pos.mpr hη)
    have hmM : (α : ℝ)+η⁻¹≤(β : ℝ)+η⁻¹ := by
      simpa only [add_comm] using (add_le_add_right (show (α : ℝ) ≤ (β : ℝ) from hαβ) η⁻¹)
    have hiW := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
      hm (hW.differentiable (by norm_num))
      (AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hW (fun x a => (hb x a).1))
    have hRW : R y=(volume : Measure E).tilted (fun x => -W x) := by
      dsimp only [R,μ]
      rw [tilted_tilted hi]
      congr 1
      funext x
      simp only [Pi.add_apply,W]
      field_simp [hη.ne']
      ring
    have hX : MemLp id 2 ((volume : Measure E).tilted (fun x => -W x)) := hRW ▸ (hRm y).2
    rw [hRW]
    exact AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GibbsLinearCovarianceUpper.gibbs_linear_covariance_upper
      W hW hiW (integral_exp_pos hiW) ((α : ℝ)+η⁻¹) ((β : ℝ)+η⁻¹) hm hmM
      (fun x a => (hb x a).1) (fun x a => (hb x a).2) hX
  have he : U=(fun y => Vη y+Real.log ZV) := funext hshift
  have hd : fderiv ℝ U=fderiv ℝ Vη := by
    rw [he]
    funext y
    exact fderiv_add_const _
  change ∀ y a b, fderiv ℝ (fderiv ℝ U) y a b = _ at hDD
  rw [hd] at hDD
  let m := (α : ℝ)/(1+(α : ℝ)*η)
  let M := (β : ℝ)/(1+(β : ℝ)*η)
  have hden : 0<1+(α : ℝ)*η := by positivity
  have hbden : 0<1+(β : ℝ)*η := by positivity
  have hm : 0<m := div_pos hα hden
  have hmM : m≤M := by
    dsimp only [m,M]
    apply (div_le_div_iff₀ hden hbden).2
    nlinarith [show (α : ℝ) ≤ (β : ℝ) from hαβ]
  have hlower (y a : E) : m*‖a‖^2 ≤ fderiv ℝ (fderiv ℝ Vη) y a a := by
    rw [hDD y a a,real_inner_self_eq_norm_sq]
    have hp : 0<(α : ℝ)+η⁻¹ := add_pos hα (inv_pos.mpr hη)
    calc
      m*‖a‖^2 = ‖a‖^2/η-(‖a‖^2/((α : ℝ)+η⁻¹))/η^2 := by
        dsimp only [m]
        field_simp [hη.ne',hp.ne',hden.ne']
        ring
      _ ≤ ‖a‖^2/η-covarianceBilin (R y) a a/η^2 :=
        sub_le_sub_left (div_le_div_of_nonneg_right (hcov y a) (sq_nonneg η)) _
  have hupper : ∀ y a : E, fderiv ℝ (fderiv ℝ Vη) y a a ≤ M*‖a‖^2 :=
    (AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.SmoothedHessianUpper.smoothed_hessian_upper
      (show 0<α from hα) hαβ hV hH hη).2
  have hI : Integrable (fun y => Real.exp (-Vη y)) (volume : Measure E) := by
    have hexp (y : E) : Real.exp (-Vη y)=A y := by
      dsimp only [Vη];rw [neg_neg,Real.exp_log (hA y)]
    simpa only [hexp] using hIA
  have hZη : 0<∫ y, Real.exp (-Vη y) ∂(volume : Measure E) := integral_exp_pos hI
  obtain ⟨G,hDense,hClose,hClosed,hGraph⟩ :=
    GaussianMarginalGradient.gaussian_marginal_gradient_closable μ hη
  refine ⟨inferInstance,G,hDense,hClose,hClosed,hGraph,?_⟩
  have hPI : ∀ (D : Lp ℝ 2 ν →ₗ.[ℝ] Lp E 2 ν), D.IsClosable →
      (∀ (a : Lp ℝ 2 ν) (F : Lp E 2 ν), (a,F) ∈ D.graph ↔
        ∃ φ : E → ℝ, ContDiff ℝ ∞ φ ∧ HasCompactSupport φ ∧
          a =ᵐ[ν] φ ∧ F =ᵐ[ν] gradient φ) →
      ∀ z : D.closure.domain, (∫ x, (z : Lp ℝ 2 ν) x ∂ν)=0 →
        m*‖(z : Lp ℝ 2 ν)‖^2 ≤ ‖D.closure z‖^2 := by
    rw [htilt]
    exact CenteredDomainPoincare.gibbs_centered_domain_poincare
      Vη hC2 hI hZη m M hm hmM hlower hupper
  exact hPI G hClose hGraph

end
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare
