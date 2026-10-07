import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy

namespace Tests.ProximalBPSGaussianReflectedMean
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 800000
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal
open AutoSamplingTheory.ExampleCases.ProximalBPS
open AutoSamplingTheory.TechnicalLemmas.Measure
open AutoSamplingTheory.TechnicalLemmas.Probability

-- Source Gibbs probability is produced internally by the actual PBPS result.
-- Use its SAME mu/J and an everywhere specified conditional kernel, then
-- consume the new analytic result for its actual reflected integral.
-- The source-volume S_y identity and full rough B.13 remain separate.
theorem actual_pbps_reflected_kernel_mean
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x a : E,
      (α : ℝ) * ‖a‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x a) a ∧
      (fderiv ℝ (fderiv ℝ V) x a) a ≤ (β : ℝ) * ‖a‖^2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := (μ.prod (stdGaussian E)).map
      (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
    ∃ R : Kernel E E, IsMarkovKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
      (J.map Prod.swap).IsCondKernel R ∧
      ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
        ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂((R y).map
          (fun x : E => (2:ℝ) • x-y))) := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  have hactual := MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks
    hα hαβ hV hH hη hβη
  have : IsProbabilityMeasure μ := hactual.1
  obtain ⟨R,hR,hfiber,hcond⟩ := GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  refine ⟨R,hR,hfiber,hcond,?_⟩
  intro f hf hc
  simp_rw [hfiber]
  exact GaussianReflectedMean.gaussian_reflected_mean_c1 μ hη (contDiff_infty.mp hf 1) hc

-- No centering or positive-dimensional premise: the actual posterior and its
-- reflection on rank zero give the NONCENTERED constant observer real mean1.
theorem rank_zero_noncentered_mean :
    let E := EuclideanSpace ℝ (Fin 0)
    let μ := stdGaussian E
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*(1:ℝ)))
    let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
    ContDiff ℝ 1 (fun y : E => ∫ u, (1:ℝ) ∂S y) ∧
      (∀ y, (∫ u, (1:ℝ) ∂S y) = 1) ∧
      (∀ y, fderiv ℝ (fun z : E => ∫ u, (1:ℝ) ∂S z) y = 0) := by
  let E := EuclideanSpace ℝ (Fin 0)
  let μ := stdGaussian E
  let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*(1:ℝ)))
  let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
  have hc : HasCompactSupport (fun _ : E => (1:ℝ)) := (isClosed_tsupport _).isCompact
  have hreg := GaussianReflectedMean.gaussian_reflected_mean_c1 μ
    (η := 1) (by norm_num) (f := fun _ => 1) contDiff_const hc
  obtain ⟨Rk,hRk,hfiber,_⟩ := GaussianConditionalKernel.exists_tilted_isCondKernel μ
    (η := 1) (by norm_num)
  have hmean (y : E) : (∫ u, (1:ℝ) ∂S y) = 1 := by
    have : IsMarkovKernel Rk := hRk
    have hprob : IsProbabilityMeasure (R y) := by
      rw [show R y = Rk y from (hfiber y).symm]
      infer_instance
    have : IsProbabilityMeasure (R y) := hprob
    have : IsProbabilityMeasure (S y) := Measure.isProbabilityMeasure_map (by fun_prop)
    simp
  refine ⟨hreg,hmean,?_⟩
  have he : (fun z : E => ∫ u, (1:ℝ) ∂S z) = fun _ => (1:ℝ) := funext hmean
  intro y
  rw [he,fderiv_const_apply]

#print axioms GaussianReflectedMean.gaussian_reflected_mean_c1
#print axioms actual_pbps_reflected_kernel_mean
#print axioms rank_zero_noncentered_mean

end
end Tests.ProximalBPSGaussianReflectedMean
