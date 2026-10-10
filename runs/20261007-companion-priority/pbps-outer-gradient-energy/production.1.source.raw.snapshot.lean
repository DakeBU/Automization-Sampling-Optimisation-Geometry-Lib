import AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientVariance
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection
import Mathlib.Probability.Kernel.MeasurableIntegral
import Mathlib.Probability.Kernel.Composition.IntegralCompProd
import Mathlib.Analysis.Calculus.FDeriv.Measurable

/-! Actual smooth compact PBPS outer energy formula(C.2), arXiv2609.06905v1.
All probability and analytic domains are derived from genuine laws. Full rough
L²-to-H¹ closure, literal operator adapters, main samplers and costs are separate. -/
set_option autoImplicit false
noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace NNReal ContDiff
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy

private theorem reflected_second_moment
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] (η : ℝ) (hη : 0 < η)
    (R S : Kernel E E) [IsMarkovKernel R] [IsMarkovKernel S]
    (f : E → ℝ) (hf : Continuous f) (M : ℝ) (hM : ∀ u, ‖f u‖ ≤ M) :
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    (J.map Prod.swap).IsCondKernel R →
    (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x-y)) →
    (∫ y, ∫ u, (f u)^2 ∂S y ∂J.snd) = ∫ y, (f y)^2 ∂J.snd := by
  dsimp only
  intro hcond hSR
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let ν := J.snd
  have hΦ : Measurable (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2)) := by fun_prop
  have hJ : IsProbabilityMeasure J := Measure.isProbabilityMeasure_map hΦ.aemeasurable
  letI := hJ
  have hdis : ν ⊗ₘ R = J.map Prod.swap := by
    simpa only [Measure.fst_map_swap] using hcond.disintegrate
  let g : E × E → ℝ := fun p => f ((2 : ℝ) • p.2-p.1)
  have hg : Continuous g := by fun_prop
  have hg2 : MemLp g 2 (ν ⊗ₘ R) := MemLp.of_bound hg.aestronglyMeasurable M
    (Filter.Eventually.of_forall fun p => hM _)
  have hfsq : StronglyMeasurable (fun u => (f u)^2) := (hf.pow 2).stronglyMeasurable
  have href := (GaussianReflection.reflection_preserves_augmentation μ η hη).2
  change (∫ y, ∫ u, (f u)^2 ∂S y ∂ν) = ∫ y, (f y)^2 ∂ν
  calc
    (∫ y, ∫ u, (f u)^2 ∂S y ∂ν) =
        ∫ y, ∫ x, (f ((2 : ℝ) • x-y))^2 ∂R y ∂ν := by
      apply integral_congr_ae
      filter_upwards [] with y
      rw [hSR y]
      exact integral_map_of_stronglyMeasurable (by fun_prop) hfsq
    _ = ∫ p, (g p)^2 ∂(ν ⊗ₘ R) := (Measure.integral_compProd hg2.integrable_sq).symm
    _ = ∫ p, (g p)^2 ∂(J.map Prod.swap) := by rw [hdis]
    _ = ∫ p, (f ((2 : ℝ) • p.1-p.2))^2 ∂J := by
      simpa only [Pi.pow_apply, g, Prod.swap_fst, Prod.swap_snd] using
        (integral_map_of_stronglyMeasurable (μ := J) measurable_swap
          (hg.pow 2).stronglyMeasurable)
    _ = ∫ p, (f p.2)^2 ∂(J.map (fun p => (p.1,(2 : ℝ) • p.1-p.2))) := by
      symm
      exact integral_map_of_stronglyMeasurable (by fun_prop)
        ((hf.comp continuous_snd).pow 2).stronglyMeasurable
    _ = ∫ p, (f p.2)^2 ∂J := by rw [href]
    _ = ∫ y, (f y)^2 ∂ν := by
      symm
      exact integral_map_of_stronglyMeasurable measurable_snd hfsq

theorem reflected_conditional_gradient_energy
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
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2 : ℝ) • x - y)) ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun u => -V ((1/2 : ℝ) • (y+u)) - ‖y-u‖^2/(8*η))) ∧
      ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
        let Tf := fun y => ∫ u, f u ∂S y
        Differentiable ℝ Tf ∧ MemLp f 2 ν ∧ MemLp Tf 2 ν ∧
        MemLp (gradient Tf) 2 ν ∧
        Integrable (fun y =>
          AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
            (S y) f) ν ∧
        (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
          (S y) f ∂ν) = (∫ y, (f y)^2 ∂ν) - (∫ y, (Tf y)^2 ∂ν) ∧
        η * (∫ y, ‖gradient Tf y‖^2 ∂ν) ≤
          (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) *
            ((∫ y, (f y)^2 ∂ν) - (∫ y, (Tf y)^2 ∂ν)) := by
  dsimp only
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    (μ.prod (stdGaussian E))
  let ν := J.snd
  obtain ⟨hZ,hJ,_⟩ := GibbsAugmentation.normalized_augmentation_density
    hα hV (fun x a => (hH x a).1) hη
  have hexp : Integrable (fun x => Real.exp (-V x)) (volume : Measure E) := by
    by_contra hn
    exact (ne_of_gt hZ) (integral_undef hn)
  have hμ : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hexp
  letI := hμ
  letI : IsProbabilityMeasure J := hJ
  have hν : IsProbabilityMeasure ν := inferInstance
  letI := hν
  obtain ⟨R,S,hR,hS,hcond,hSR,hSd,hpoint⟩ :=
    ConditionalGradientVariance.reflected_conditional_gradient_variance hα hαβ hV hH hη hβη
  letI := hR
  letI := hS
  refine ⟨hμ,hJ,hν,R,S,hR,hS,hcond,hSR,hSd,?_⟩
  intro f hf hfc
  let Tf := fun y => ∫ u, f u ∂S y
  obtain ⟨M,hMb⟩ := hf.continuous.norm.bddAbove_range_of_hasCompactSupport hfc.norm
  have hM (u : E) : ‖f u‖ ≤ M := hMb (Set.mem_range_self u)
  have hM0 : 0 ≤ M := (norm_nonneg (f 0)).trans (hM 0)
  have hf2 : MemLp f 2 ν := MemLp.of_bound hf.continuous.aestronglyMeasurable M
    (Filter.Eventually.of_forall hM)
  have hfy2 (y : E) : MemLp f 2 (S y) :=
    MemLp.of_bound hf.continuous.aestronglyMeasurable M (Filter.Eventually.of_forall hM)
  have hTfsm : StronglyMeasurable Tf := hf.continuous.stronglyMeasurable.integral_kernel
  have hTfbound (y : E) : ‖Tf y‖ ≤ M := by
    simpa using norm_integral_le_of_norm_le_const (μ := S y) (Filter.Eventually.of_forall hM)
  have hTf2 : MemLp Tf 2 ν := MemLp.of_bound hTfsm.aestronglyMeasurable M
    (Filter.Eventually.of_forall hTfbound)
  let vf := fun y =>
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance (S y) f
  have hv (y : E) : vf y = (∫ u, (f u)^2 ∂S y)-(Tf y)^2 := by
    dsimp only [vf, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance]
    rw [← variance_eq_integral (hfy2 y).aemeasurable, variance_eq_sub (hfy2 y)]
    rfl
  have hfsqsm : StronglyMeasurable (fun y => ∫ u, (f u)^2 ∂S y) :=
    (hf.continuous.pow 2).stronglyMeasurable.integral_kernel
  have hfsqbound (u : E) : ‖(f u)^2‖ ≤ M^2 := by
    rw [norm_pow]
    exact (sq_le_sq₀ (norm_nonneg _) hM0).mpr (hM u)
  have hfsq1 : MemLp (fun y => ∫ u, (f u)^2 ∂S y) 1 ν :=
    MemLp.of_bound hfsqsm.aestronglyMeasurable (M^2) (Filter.Eventually.of_forall
      fun y => by simpa using (norm_integral_le_of_norm_le_const (μ := S y)
        (Filter.Eventually.of_forall hfsqbound)))
  have hfsqI := hfsq1.integrable le_rfl
  have hvI : Integrable vf ν := (hfsqI.sub hTf2.integrable_sq).congr
    (Filter.Eventually.of_forall fun y => (hv y).symm)
  have hvdef : (∫ y, vf y ∂ν) = (∫ y, (f y)^2 ∂ν)-(∫ y, (Tf y)^2 ∂ν) := by
    rw [integral_congr_ae (Filter.Eventually.of_forall hv), integral_sub hfsqI hTf2.integrable_sq]
    rw [reflected_second_moment μ η hη R S f hf.continuous M hM hcond hSR]
  have hgradsm : StronglyMeasurable (gradient Tf) := by
    exact ((toDual ℝ E).symm.continuous.measurable.comp
      (measurable_fderiv (𝕜 := ℝ) (f := Tf))).stronglyMeasurable
  let C := (1/η-(α : ℝ))^2/(4*((α : ℝ)+1/η))
  have hgradI : Integrable (fun y => ‖gradient Tf y‖^2) ν :=
    (hvI.const_mul C).mono_nonneg (hgradsm.norm.pow 2).aestronglyMeasurable
      (Filter.Eventually.of_forall fun _ => sq_nonneg _)
      (Filter.Eventually.of_forall fun y => (hpoint f hf hfc y).2)
  have hgrad2 : MemLp (gradient Tf) 2 ν :=
    (memLp_two_iff_integrable_sq_norm hgradsm.aestronglyMeasurable).mpr hgradI
  refine ⟨fun y => (hpoint f hf hfc y).1,hf2,hTf2,hgrad2,hvI,hvdef,?_⟩
  have hi : (∫ y, ‖gradient Tf y‖^2 ∂ν) ≤ C*(∫ y, vf y ∂ν) := by
    calc
      (∫ y, ‖gradient Tf y‖^2 ∂ν) ≤ ∫ y, C*vf y ∂ν :=
        integral_mono hgradI (hvI.const_mul C) (fun y => (hpoint f hf hfc y).2)
      _ = C*(∫ y, vf y ∂ν) := integral_const_mul _ _
  have hden : 0 < (α : ℝ)+1/η := by positivity
  have hnewden : 0 < 1+(α : ℝ)*η := by positivity
  have hcoeff : η*C = (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η)) := by
    dsimp only [C]
    field_simp [ne_of_gt hη,ne_of_gt hden,ne_of_gt hnewden]
    <;> ring
  calc
    η*(∫ y, ‖gradient Tf y‖^2 ∂ν) ≤ η*(C*(∫ y, vf y ∂ν)) :=
      mul_le_mul_of_nonneg_left hi hη.le
    _ = (η*C)*(∫ y, vf y ∂ν) := by ring
    _ = (1-(α : ℝ)*η)^2/(4*(1+(α : ℝ)*η))*
        ((∫ y, (f y)^2 ∂ν)-(∫ y, (Tf y)^2 ∂ν)) := by rw [hcoeff,hvdef]

end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalGradientEnergy
