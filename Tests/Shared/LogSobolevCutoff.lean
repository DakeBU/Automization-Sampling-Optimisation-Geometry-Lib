import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation

open MeasureTheory Filter
open scoped Topology ContDiff RealInnerProductSpace

namespace Tests.Shared.LogSobolevCutoff

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff

-- The source's actual square-root test need not be compactly supported.
-- No gradient-integrability hypothesis for that test is supplied by the caller.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsFiniteMeasure μ] (C : ℝ)
    (hLSI : ∀ (v : E → ℝ), ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) {M : ℝ} (hbound : ∀ x, |f x| ≤ M)
    (hcompact : HasCompactSupport (fderiv ℝ f)) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      let u := fun x => Real.sqrt (1 + e * f x)
      (∫ x, (u x)^2 * Real.log ((u x)^2) ∂μ) -
        (∫ x, (u x)^2 ∂μ) * Real.log (∫ x, (u x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient u x‖^2 ∂μ := by
  filter_upwards [(eventually_contDiff_and_integrable_sqrt_perturbation
    μ f hf hbound hcompact).2] with e he
  dsimp only
  obtain ⟨_, hu, hu2, hentropy, henergy⟩ := he
  let u := fun x => Real.sqrt (1 + e * f x)
  change Integrable (fun x => ‖fderiv ℝ u x‖ ^ 2) μ at henergy
  have hnorm (x : E) : ‖fderiv ℝ u x‖ = ‖gradient u x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  have hgrad : MemLp (gradient u) 2 μ :=
    (memLp_two_iff_integrable_sq_norm
      (continuous_gradient_of_contDiff_one (hu.of_le (by simp))).aestronglyMeasurable).mpr
      (by simpa only [hnorm] using henergy)
  exact logSobolev_of_compact_smooth_tests μ C hLSI u hu hu2 hgrad hentropy

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff.cutoff_integral_limits
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff.logSobolev_of_compact_smooth_tests

end Tests.Shared.LogSobolevCutoff
