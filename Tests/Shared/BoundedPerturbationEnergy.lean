import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy
import Mathlib.Analysis.Calculus.Gradient.Basic

open MeasureTheory Filter
open scoped Topology

namespace Tests.Shared.BoundedPerturbationEnergy

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy

-- Exact sealed generic signature; no finite-measure, probability or centering class.
example {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) (f : E → ℝ) (hf : Differentiable ℝ f)
    {M : ℝ} (hbound : ∀ᵐ x ∂mu, |f x| ≤ M)
    (henergy : Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu) :
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      Integrable (fun x => ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu) ∧
    Tendsto (fun e : ℝ =>
      (∫ x, ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, ‖fderiv ℝ f x‖ ^ 2 ∂mu) / 4)) :=
  eventually_integrable_and_tendsto_sqrt_perturbation_energy mu f hf hbound henergy

-- Actual Hilbert gradient-energy consumer via Riesz isometry, not an RN replacement.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) (f : E → ℝ) (hf : Differentiable ℝ f)
    {M : ℝ} (hbound : ∀ᵐ x ∂mu, |f x| ≤ M)
    (henergy : Integrable (fun x => ‖gradient f x‖ ^ 2) mu) :
    (∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      Integrable (fun x => ‖gradient (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu) ∧
    Tendsto (fun e : ℝ =>
      (∫ x, ‖gradient (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2 ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, ‖gradient f x‖ ^ 2 ∂mu) / 4)) := by
  have hnorm (g : E → ℝ) (x : E) : ‖fderiv ℝ g x‖ = ‖gradient g x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  have hi : Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu := by
    simpa only [hnorm] using henergy
  simpa only [hnorm] using
    eventually_integrable_and_tendsto_sqrt_perturbation_energy mu f hf hbound hi

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy.eventually_integrable_and_tendsto_sqrt_perturbation_energy

end Tests.Shared.BoundedPerturbationEnergy
