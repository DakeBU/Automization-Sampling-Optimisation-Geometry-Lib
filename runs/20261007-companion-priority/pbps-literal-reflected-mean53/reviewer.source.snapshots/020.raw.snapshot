import AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean
import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel

namespace Tests.ProximalBPSReflectedMeanRegularity
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 800000
open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal
open AutoSamplingTheory.ExampleCases.ProximalBPS
open AutoSamplingTheory.TechnicalLemmas.Probability

-- Actual source Gibbs law/augmentation and all original Hessian/step premises.
-- The genuine conditional R and the literal source-volume S share the same mu/J;
-- the new integration identifies every S fiber, its probability and source mean.
-- No transition-process, rough domain or expected-query-cost claim is made.
theorem actual_pbps_source_reflected_mean
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
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    ∃ R : Kernel E E, IsMarkovKernel R ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, R y = μ.tilted (fun x => -‖x-y‖^2/(2*η))) ∧
      ∀ f : E → ℝ, ContDiff ℝ ∞ f → HasCompactSupport f →
        (∀ y, S y = (R y).map (fun x : E => (2:ℝ) • x-y)) ∧
        (∀ y, IsProbabilityMeasure (S y)) ∧
        ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y) := by
  let μ := (volume : Measure E).tilted (fun x => -V x)
  let S := fun y : E => (volume : Measure E).tilted
    (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
  have hactual := MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks
    hα hαβ hV hH hη hβη
  have : IsProbabilityMeasure μ := hactual.1
  obtain ⟨R,hR,hfiber,hcond⟩ := GaussianConditionalKernel.exists_tilted_isCondKernel μ hη
  refine ⟨R,hR,hcond,hfiber,?_⟩
  intro f hf hc
  have hnew := LiteralReflectedMean.reflected_gibbs_mean_c1
    hα hV (fun x v => (hH x v).1) hη (contDiff_infty.mp hf 1) hc
  have hS (y : E) : S y = (R y).map (fun x : E => (2:ℝ) • x-y) := by
    rw [hfiber y]
    exact hnew.1 y
  refine ⟨hS,?_,hnew.2⟩
  intro y
  rw [hS y]
  exact Measure.isProbabilityMeasure_map (by fun_prop)

-- Genuine normalized source-volume law in dimension zero, arbitrary signed
-- observer allowed: constant1 has actual mean1 and true derivative0, no centering.
theorem rank_zero_source_noncentered_mean :
    let E := EuclideanSpace ℝ (Fin 0)
    let S := fun y : E => (volume : Measure E).tilted
      (fun u => -(0:ℝ) - ‖y-u‖^2/(8*(1:ℝ)))
    ContDiff ℝ 1 (fun y : E => ∫ u, (1:ℝ) ∂S y) ∧
      (∀ y, (∫ u, (1:ℝ) ∂S y) = 1) ∧
      (∀ y, fderiv ℝ (fun z : E => ∫ u, (1:ℝ) ∂S z) y = 0) := by
  let E := EuclideanSpace ℝ (Fin 0)
  let μ := (volume : Measure E).tilted (fun _ => -(0:ℝ))
  let S := fun y : E => (volume : Measure E).tilted
    (fun u => -(0:ℝ) - ‖y-u‖^2/(8*(1:ℝ)))
  have hH (x v : E) : (1:ℝ)*‖v‖^2 ≤
      (fderiv ℝ (fderiv ℝ (fun _ : E => (0:ℝ))) x v) v := by
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  have hc : HasCompactSupport (fun _ : E => (1:ℝ)) := (isClosed_tsupport _).isCompact
  have hnew := LiteralReflectedMean.reflected_gibbs_mean_c1
    (α := 1) (η := 1) (V := fun _ : E => 0) (by norm_num) contDiff_const hH
    (by norm_num) (f := fun _ => 1) contDiff_const hc
  have hG := GibbsAugmentation.normalized_augmentation_density
    (α := 1) (η := 1) (V := fun _ : E => 0) (by norm_num) contDiff_const hH (by norm_num)
  have hI : Integrable (fun _ : E => Real.exp (-(0:ℝ))) (volume : Measure E) :=
    Integrable.of_integral_ne_zero hG.1.ne'
  have : IsProbabilityMeasure μ := isProbabilityMeasure_tilted hI
  obtain ⟨R,hR,hfiber,_⟩ := GaussianConditionalKernel.exists_tilted_isCondKernel μ
    (η := 1) (by norm_num)
  have hmean (y : E) : (∫ u, (1:ℝ) ∂S y) = 1 := by
    have hS : S y = (R y).map (fun x : E => (2:ℝ) • x-y) := by
      rw [hfiber y]
      exact hnew.1 y
    have : IsProbabilityMeasure (S y) := by
      rw [hS]
      exact Measure.isProbabilityMeasure_map (by fun_prop)
    simp
  refine ⟨hnew.2,hmean,?_⟩
  have he : (fun y : E => ∫ u, (1:ℝ) ∂S y) = fun _ => (1:ℝ) := funext hmean
  intro y
  rw [he,fderiv_const_apply]

#print axioms LiteralReflectedMean.reflected_gibbs_mean_c1
#print axioms actual_pbps_source_reflected_mean
#print axioms rank_zero_source_noncentered_mean

end
end Tests.ProximalBPSReflectedMeanRegularity
