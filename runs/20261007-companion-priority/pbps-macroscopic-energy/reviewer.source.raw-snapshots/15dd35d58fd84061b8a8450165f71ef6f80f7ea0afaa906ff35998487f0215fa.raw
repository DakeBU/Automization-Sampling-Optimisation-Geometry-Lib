import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy
import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicRepresentative
import AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2

/-!
# The actual macroscopic reflection energy in joint L2

Source: arXiv:2609.06905v1 Appendix B.1-B.9 and C.1 (C.2).
A, B and D below are authored aliases for U_PP, U_QP and U_QQ.
This joins actual conditional variance, L2 block norms and smooth compact
energy. The full rough H1 domain, Gamma and half-turn mixing remain separate.
-/

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy

/-- Genuine joint-L2 classes and block variance for the SAME reflected kernel
whose literal conditional integral has the sharp smooth gradient bound. -/
theorem actual_macroscopic_gradient_energy_blocks
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E,
      (α : ℝ) * ‖a‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x a) a ∧
      (fderiv ℝ (fderiv ℝ V) x a) a ≤ (β : ℝ) * ‖a‖^2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1, p.1 + Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let ν := J.snd
    let Λ := J.map (fun p : E × E => (p.2, (2 : ℝ) • p.1 - p.2))
    let F := fun p : E × E => (p.1, (2 : ℝ) • p.1 - p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x - y)) ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun u => -V ((1/2 : ℝ) • (y+u)) - ‖y-u‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        let A := P * U.toContinuousLinearMap * P
        let B := (1-P) * U.toContinuousLinearMap * P
        let D := (1-P) * U.toContinuousLinearMap * (1-P)
        star B * B = P - A^2 ∧ star B * D = -(A * star B) ∧
        (∀ g : Lp ℝ 2 J, P g = g → ‖B g‖^2 = ‖g‖^2 - ‖A g‖^2) ∧
        ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
          let Tf := fun y => ∫ u, f u ∂S y
          Differentiable ℝ Tf ∧ MemLp f 2 ν ∧ MemLp Tf 2 ν ∧
          MemLp (gradient Tf) 2 ν ∧
          Integrable (fun y =>
            AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
              (S y) f) ν ∧
          ∃ g : Lp ℝ 2 J,
            (g : E × E → ℝ) =ᵐ[J] (fun p => f p.2) ∧ P g = g ∧
            (A g : E × E → ℝ) =ᵐ[J] (fun p => Tf p.2) ∧
            ‖g‖^2 = (∫ y, (f y)^2 ∂ν) ∧
            ‖A g‖^2 = (∫ y, (Tf y)^2 ∂ν) ∧
            (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
              (S y) f ∂ν) = ‖B g‖^2 ∧
            η * (∫ y, ‖gradient Tf y‖^2 ∂ν) ≤
              (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) * ‖B g‖^2 := by
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let ν := J.snd
  let Λ := J.map (fun p : E × E => (p.2,(2:ℝ) • p.1-p.2))
  let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
    (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
      2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
  obtain ⟨hμ,hJ,hν,R,S,hR,hS,hcond,hSR,hSd,henergy⟩ :=
    ConditionalGradientEnergy.reflected_conditional_gradient_energy hα hαβ hV hH hη hβη
  letI : IsProbabilityMeasure μ := hμ
  letI : IsProbabilityMeasure J := hJ
  letI : IsProbabilityMeasure ν := hν
  letI : IsMarkovKernel R := hR
  letI : IsMarkovKernel S := hS
  letI : (J.map Prod.swap).IsCondKernel R := hcond

  -- Transform the actual disintegration, not an independently chosen law.
  let G := fun p : E × E => (p.1,(2:ℝ) • p.2-p.1)
  have hG : Measurable G := by fun_prop
  have hmap : (J.map Prod.swap).fst ⊗ₘ S =
      ((J.map Prod.swap).fst ⊗ₘ R).map G := by
    ext t ht
    rw [Measure.compProd_apply ht, Measure.map_apply hG ht,
      Measure.compProd_apply (hG ht)]
    apply lintegral_congr_ae
    filter_upwards with y
    rw [hSR y, Measure.map_apply (by fun_prop) (measurable_prodMk_left ht)]
    rfl
  have hΛmap : (J.map Prod.swap).map G = Λ := by
    rw [Measure.map_map hG (by fun_prop)]
    rfl
  have hfst : Λ.fst = ν := by
    rw [← hΛmap, Measure.fst_map_prodMk (by fun_prop), Measure.fst_map_swap]
  have hΛcond : Λ.IsCondKernel S := by
    constructor
    rw [hfst, show ν = (J.map Prod.swap).fst from (Measure.fst_map_swap J).symm,
      hmap, Measure.disintegrate (J.map Prod.swap) R, hΛmap]
  letI : Λ.IsCondKernel S := hΛcond

  obtain ⟨S₀,hS₀,hΛ₀,hfst₀,U₀,hU₀,hUi₀,hUs₀,hrep₀⟩ :=
    MacroscopicRepresentative.macroscopic_reflection_smooth_representative hα hV hH hη
  letI : IsMarkovKernel S₀ := hS₀
  letI : Λ.IsCondKernel S₀ := hΛ₀
  have hκ : S =ᵐ[ν] S₀ := by
    have h₁ := eq_condKernel_of_measure_eq_compProd S (Measure.disintegrate Λ S).symm
    have h₀ := eq_condKernel_of_measure_eq_compProd S₀ (Measure.disintegrate Λ S₀).symm
    rw [hfst] at h₁ h₀
    exact h₁.trans h₀.symm
  have hκJ : ∀ᵐ p ∂J, S p.2 = S₀ p.2 :=
    ae_of_ae_map measurable_snd.aemeasurable hκ

  obtain ⟨R₁,hR₁,hRf₁,U,hU,hUi,hUs,hRp,hBB,hBD,hblock⟩ :=
    ReflectionL2.actual_reflection_block_identities μ hη
  have hUU : U₀ = U := by
    apply LinearIsometry.ext
    intro g
    exact Lp.ext ((hU₀ g).trans (hU g).symm)
  refine ⟨hμ,hJ,hν,R,S,hR,hS,hcond,hSR,hSd,hΛcond,hfst,U,hU,hUi,hUs,
    hBB,hBD,hblock,?_⟩
  intro f hf hfc
  let Tf := fun y => ∫ u, f u ∂S y
  obtain ⟨hd,hf2,hTf2,hgrad2,hvarI,hvar,hbound⟩ := henergy f hf hfc
  obtain ⟨g,hg,hPg,hAg,hTf₀2,hscore⟩ := hrep₀ f hf hfc
  rw [hUU] at hAg
  let A := P * U.toContinuousLinearMap * P
  let B := (1-P) * U.toContinuousLinearMap * P
  have hAgS : (A g : E × E → ℝ) =ᵐ[J] (fun p => Tf p.2) := by
    apply hAg.trans
    filter_upwards [hκJ] with p hp
    change (∫ u, f u ∂S₀ p.2) = ∫ u, f u ∂S p.2
    rw [hp]

  -- A joint representative's actual second moment uses the actual snd law.
  have norm_snd (v : Lp ℝ 2 J) (φ : E → ℝ) (hφ : Continuous φ)
      (hv : (v : E × E → ℝ) =ᵐ[J] (fun p => φ p.2)) :
      ‖v‖^2 = ∫ y, (φ y)^2 ∂ν := by
    calc
      ‖v‖^2 = ∫ p, (φ p.2)^2 ∂J := by
        rw [← real_inner_self_eq_norm_sq, L2.inner_def]
        apply integral_congr_ae
        filter_upwards [hv] with p hp
        rw [hp]
        simp [pow_two]
      _ = ∫ y, (φ y)^2 ∂ν :=
        (integral_map measurable_snd.aemeasurable
          (hφ.pow 2).aestronglyMeasurable).symm
  have hgn := norm_snd g f hf.continuous hg
  have hAgn := norm_snd (A g) Tf hd.continuous hAgS
  have hvariance : (∫ y,
      AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
        (S y) f ∂ν) = ‖B g‖^2 := by
    calc
      _ = ‖g‖^2-‖A g‖^2 := by rw [hvar,hgn,hAgn]
      _ = ‖B g‖^2 := (hblock g hPg).symm
  refine ⟨hd,hf2,hTf2,hgrad2,hvarI,g,hg,hPg,hAgS,hgn,hAgn,hvariance,?_⟩
  calc
    η * (∫ y, ‖gradient Tf y‖^2 ∂ν) ≤
        (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) *
          ((∫ y, (f y)^2 ∂ν)-(∫ y, (Tf y)^2 ∂ν)) := hbound
    _ = (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) * ‖B g‖^2 := by
      rw [← hvar,hvariance]

end AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
