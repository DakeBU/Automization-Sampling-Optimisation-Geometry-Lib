import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
import Mathlib.Analysis.Calculus.Gradient.Basic

open MeasureTheory Filter
open scoped Topology ContDiff

namespace Tests.Shared.CompactGradientSqrtPerturbation

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy

-- Exact sealed signature: no input energy integrability, probability or centering.
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) [IsFiniteMeasure mu] (f : E → ℝ)
    (hf : ContDiff ℝ ∞ f) {M : ℝ} (hbound : ∀ x, |f x| ≤ M)
    (hcompact : HasCompactSupport (fderiv ℝ f)) :
    Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu ∧
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∀ x, 1 / 2 ≤ 1 + e * f x) ∧
      ContDiff ℝ ∞ (fun x => Real.sqrt (1 + e * f x)) ∧
      MemLp (fun x => Real.sqrt (1 + e * f x)) 2 mu ∧
      Integrable (fun x => (Real.sqrt (1 + e * f x)) ^ 2 *
        Real.log ((Real.sqrt (1 + e * f x)) ^ 2)) mu ∧
      Integrable (fun x =>
        ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu :=
  eventually_contDiff_and_integrable_sqrt_perturbation mu f hf hbound hcompact

-- A real consumer of the new original-energy output: discharge the old limit
-- theorem's energy premise, including its Hilbert gradient specialization.
-- This example is NOT a second public leaf, LSI application or RN substitution.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) [IsFiniteMeasure mu] (f : E → ℝ)
    (hf : ContDiff ℝ ∞ f) {M : ℝ} (hbound : ∀ x, |f x| ≤ M)
    (hcompact : HasCompactSupport (gradient f)) :
    Integrable (fun x => ‖gradient f x‖ ^ 2) mu ∧
    Tendsto (fun e : ℝ =>
      (∫ x, ‖gradient (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, ‖gradient f x‖ ^ 2 ∂mu) / 4)) := by
  have hnorm (g : E → ℝ) (x : E) : ‖fderiv ℝ g x‖ = ‖gradient g x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  have hcompactFD : HasCompactSupport (fderiv ℝ f) := by
    simpa only [Function.comp_def, toDual_gradient] using
      hcompact.comp_left (g := fun v : E => (InnerProductSpace.toDual ℝ E) v) (by simp)
  have data := eventually_contDiff_and_integrable_sqrt_perturbation mu f hf hbound hcompactFD
  constructor
  · simpa only [hnorm] using data.1
  · simpa only [hnorm] using
      (eventually_integrable_and_tendsto_sqrt_perturbation_energy mu f
        (hf.differentiable (by simp)) (ae_of_all mu hbound) data.1).2

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation

end Tests.Shared.CompactGradientSqrtPerturbation
