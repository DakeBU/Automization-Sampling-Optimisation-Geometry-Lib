import AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient

open MeasureTheory ProbabilityTheory
open scoped ContDiff NNReal Topology
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean
set_option maxHeartbeats 800000

theorem actual_macroscopic_l2_mean
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
    let Λ := J.map (fun p : E × E => (p.2,(2 : ℝ) • p.1-p.2))
    let F := fun p : E × E => (p.1,(2 : ℝ) • p.1-p.2)
    let P : Lp ℝ 2 J →L[ℝ] Lp ℝ 2 J :=
      (lpMeas ℝ ℝ (MeasurableSpace.comap Prod.snd (inferInstance : MeasurableSpace E))
        2 J).subtypeL ∘L condExpL2 ℝ ℝ measurable_snd.comap_le
    IsProbabilityMeasure μ ∧ IsProbabilityMeasure J ∧ IsProbabilityMeasure ν ∧
    ∃ S : Kernel E E, IsMarkovKernel S ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun x => -V ((1/2 : ℝ) • (y+x)) - ‖y-x‖^2/(8*η))) ∧
      Λ.IsCondKernel S ∧ Λ.fst = ν ∧ Λ.snd = ν ∧
      ∃ U : Lp ℝ 2 J →ₗᵢ[ℝ] Lp ℝ 2 J,
        (∀ g : Lp ℝ 2 J, (U g : E × E → ℝ) =ᵐ[J] g ∘ F) ∧
        Function.Involutive U ∧ IsSelfAdjoint U.toContinuousLinearMap ∧
        ∃ M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J,
          (∀ u : Lp ℝ 2 ν, (M u : E × E → ℝ) =ᵐ[J] u ∘ Prod.snd) ∧
          ∃ T : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν,
            let A := P * U.toContinuousLinearMap * P
            let B := (1-P) * U.toContinuousLinearMap * P
            ∀ u : Lp ℝ 2 ν,
              P (M u) = M u ∧ M (T u) = A (M u) ∧ ‖T u‖ ≤ ‖u‖ ∧
              (T u : E → ℝ) =ᵐ[ν] (fun y => ∫ x, u x ∂S y) ∧
              (∀ᵐ y ∂ν, Integrable (u : E → ℝ) (S y) ∧
                Integrable (fun x => (u x)^2) (S y)) ∧
              Integrable (fun y =>
                AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
                  (S y) (u : E → ℝ)) ν ∧
              (∫ y, AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance
                (S y) (u : E → ℝ) ∂ν) = ‖B (M u)‖^2 ∧
              ‖B (M u)‖^2 = ‖u‖^2-‖T u‖^2