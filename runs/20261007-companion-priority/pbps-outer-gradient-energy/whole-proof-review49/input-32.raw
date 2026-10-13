import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy

namespace Tests.ProximalBPSConditionalGradientEnergy
noncomputable section
set_option autoImplicit false
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped ContDiff RealInnerProductSpace NNReal

-- The exact Gaussian precision step makes the SHARP outer coefficient zero.
-- Consume the actual outer measure/kernel, differentiation and finite domains;
-- zero energy is not the totalized gradient of a nondifferentiable mean.
theorem gaussian_precision_outer_energy
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    let V := fun x : E => (1/2 : ℝ)*‖x‖^2
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+p.2)) (μ.prod (stdGaussian E))
    let ν := J.snd
    IsProbabilityMeasure ν ∧
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x-y)) ∧
      ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
        let Tf := fun y => ∫ u, f u ∂S y
        Differentiable ℝ Tf ∧ MemLp f 2 ν ∧ MemLp Tf 2 ν ∧
        MemLp (gradient Tf) 2 ν ∧
        Integrable (fun y =>
          AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) f) ν ∧
        (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
          (S y) f ∂ν) = (∫ y, (f y)^2 ∂ν)-(∫ y, (Tf y)^2 ∂ν) ∧
        (∫ y, ‖gradient Tf y‖^2 ∂ν) = 0 := by
  dsimp only
  let V := fun x : E => (1/2 : ℝ)*‖x‖^2
  have hV : ContDiff ℝ 2 V := contDiff_const.mul (contDiff_id.norm_sq (𝕜 := ℝ))
  have hfd (x : E) : fderiv ℝ V x = innerSL ℝ x := by
    have h := ((hasFDerivAt_id x).norm_sq).const_mul (1/2 : ℝ)
    convert h.fderiv using 1 <;> first | rfl | (ext v; simp)
  have hH (x a : E) : fderiv ℝ (fderiv ℝ V) x a a = ‖a‖^2 := by
    rw [show fderiv ℝ V = innerSL ℝ from funext hfd]
    rw [(innerSL ℝ (E := E)).hasFDerivAt.fderiv]
    exact real_inner_self_eq_norm_sq a
  obtain ⟨_,_,hν,R,S,hR,hS,hcond,hSR,_,hf⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy.reflected_conditional_gradient_energy
      (V := V) (α := 1) (β := 1) (η := 1) (by norm_num) (by rfl) hV
      (by intro x a; simp only [hH,NNReal.coe_one,one_mul]; exact ⟨le_rfl,le_rfl⟩)
      (by norm_num) (by norm_num)
  simp only [Real.sqrt_one,one_smul] at hν hcond
  refine ⟨hν,R,S,hR,hS,hcond,hSR,?_⟩
  intro f hfc hfs
  obtain ⟨hd,hf2,hTf2,hg2,hvI,hvdef,hb⟩ := hf f hfc hfs
  simp only [Real.sqrt_one,one_smul] at hd hf2 hTf2 hg2 hvI hvdef hb
  refine ⟨hd,hf2,hTf2,hg2,hvI,hvdef,?_⟩
  norm_num at hb
  exact le_antisymm hb (integral_nonneg fun _ => sq_nonneg _)

-- Exercise the same actual variance and energy identities in dimension zero.
theorem rank_zero_actual_outer_energy :
    let E := EuclideanSpace ℝ (Fin 0)
    let V := fun x : E => (1/2 : ℝ)*‖x‖^2
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+p.2)) (μ.prod (stdGaussian E))
    let ν := J.snd
    IsProbabilityMeasure ν ∧
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x-y)) ∧
      ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
        let Tf := fun y => ∫ u, f u ∂S y
        Differentiable ℝ Tf ∧ MemLp f 2 ν ∧ MemLp Tf 2 ν ∧
        MemLp (gradient Tf) 2 ν ∧
        Integrable (fun y =>
          AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) f) ν ∧
        (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
          (S y) f ∂ν) = (∫ y, (f y)^2 ∂ν)-(∫ y, (Tf y)^2 ∂ν) ∧
        (∫ y, ‖gradient Tf y‖^2 ∂ν) = 0 :=
  gaussian_precision_outer_energy (E := EuclideanSpace ℝ (Fin 0))

#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy.reflected_conditional_gradient_energy
#print axioms gaussian_precision_outer_energy
#print axioms rank_zero_actual_outer_energy
end
end Tests.ProximalBPSConditionalGradientEnergy
