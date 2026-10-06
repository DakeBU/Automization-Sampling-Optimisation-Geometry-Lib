import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactWeakPoissonSobolev

set_option autoImplicit false
noncomputable section
open MeasureTheory InnerProductSpace TemperedDistribution LineDeriv
open scoped ContDiff Topology SchwartzMap LineDeriv
namespace RealGradientLimitPrototype
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

private theorem real_postcomp_derivative (ψ : SchwartzMap E ℝ) (a : E) :
    ∂_{a} (ψ.postcompCLM Complex.ofRealCLM) =
      (∂_{a} ψ).postcompCLM Complex.ofRealCLM := by
  ext x
  simp only [SchwartzMap.lineDerivOp_apply_eq_fderiv, SchwartzMap.postcompCLM_apply]
  change (fderiv ℝ (Complex.ofRealCLM ∘ (ψ : E → ℝ)) x) a =
    Complex.ofRealCLM ((fderiv ℝ (ψ : E → ℝ) x) a)
  exact congrArg (fun L : E →L[ℝ] ℂ => L a)
    ((Complex.ofRealCLM.hasFDerivAt.comp x (ψ.hasFDerivAt x)).fderiv)

theorem identify_real_gradient (v : E → ℝ) (G : E → E)
    (hG : MemLp G 2 volume)
    (vc ga : Lp ℂ 2 (volume : Measure E))
    (hvc : vc =ᵐ[volume] (fun x => (v x : ℂ))) (a : E)
    (hga : Lp.toTemperedDistribution ga = ∂_{a} (Lp.toTemperedDistribution vc))
    (hd : ∀ ψ : E → ℝ, ContDiff ℝ 1 ψ → HasCompactSupport ψ →
      Integrable (fun x => ψ x * inner ℝ (G x) a) volume ∧
      Integrable (fun x => v x * fderiv ℝ ψ x a) volume ∧
      (∫ x, ψ x * inner ℝ (G x) a) = -∫ x, v x * fderiv ℝ ψ x a) :
    (fun x => (ga x).re) =ᵐ[volume] (fun x => inner ℝ (G x) a) := by
  have hreal : MemLp (fun x => (ga x).re) 2 volume :=
    (Lp.memLp ga).continuousLinearMap_comp Complex.reCLM
  have hinner : MemLp (fun x => inner ℝ (G x) a) 2 volume := by
    simpa only [innerSL_apply_apply,real_inner_comm] using
      hG.continuousLinearMap_comp (innerSL ℝ a)
  apply ae_eq_of_integral_contDiff_smul_eq
    (hreal.locallyIntegrable (by norm_num)) (hinner.locallyIntegrable (by norm_num))
  intro φ hφ hc
  let ψ : SchwartzMap E ℝ := hc.toSchwartzMap hφ
  let ψC : SchwartzMap E ℂ := ψ.postcompCLM Complex.ofRealCLM
  have hψ : (ψ : E → ℝ) = φ := rfl
  have hweak := hd φ (contDiff_infty.mp hφ 1) hc
  have hcomplex : Integrable (fun x => ψC x * ga x) volume :=
    (ψC.memLp 2 volume).integrable_mul (Lp.memLp ga)
  have hpair := congrArg (fun T : 𝓢'(E,ℂ) => T ψC) hga
  rw [TemperedDistribution.lineDerivOp_apply_apply,
    Lp.toTemperedDistribution_apply,Lp.toTemperedDistribution_apply] at hpair
  have hder : ∂_{a} ψC = (∂_{a} ψ).postcompCLM Complex.ofRealCLM :=
    real_postcomp_derivative ψ a
  have hright : (∫ x, (-∂_{a} ψC) x • vc x) =
      -((∫ x, v x * fderiv ℝ φ x a : ℝ) : ℂ) := by
    simp only [SchwartzMap.neg_apply,neg_smul,integral_neg]
    congr 1
    calc
      _ = ∫ x, ((∂_{a} ψ) x : ℂ) * (v x : ℂ) := by
        apply integral_congr_ae
        filter_upwards [hvc] with x hx
        simp only [hder,hx,SchwartzMap.postcompCLM_apply,
          Complex.ofRealCLM_apply,smul_eq_mul]
      _ = _ := by
        simp only [SchwartzMap.lineDerivOp_apply_eq_fderiv,hψ,
          ← Complex.ofReal_mul,mul_comm]
        exact integral_ofReal
  rw [hright] at hpair
  have hh := congrArg Complex.re hpair
  rw [show (fun x => ψC x • ga x) = (fun x => ψC x * ga x) from rfl] at hh
  have hre := integral_re hcomplex
  simp only [RCLike.re_to_complex] at hre
  rw [← hre] at hh
  have heq : (∫ x, φ x * (ga x).re) = -∫ x, v x * fderiv ℝ φ x a := by
    simpa only [Complex.ofReal_re,Complex.neg_re,SchwartzMap.postcompCLM_apply,
      Complex.ofRealCLM_apply,Complex.mul_re,Complex.ofReal_im,zero_mul,sub_zero,
      ψC,hψ] using hh
  simpa only [smul_eq_mul] using heq.trans hweak.2.2.symm

#print axioms identify_real_gradient
end RealGradientLimitPrototype
