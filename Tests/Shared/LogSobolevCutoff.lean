import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation

open MeasureTheory Filter
open scoped Topology ContDiff

namespace Tests.Shared.LogSobolevCutoff

open AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation

-- The canonical limits retain arbitrary measure and infinite-dimensional
-- complete Hilbert scope; finite dimension is not smuggled into extraction.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [MeasurableSpace E] [BorelSpace E] (μ : Measure E) (f : E → ℝ)
    (hf : ContDiff ℝ 2 f) (hf2 : MemLp f 2 μ) (hgrad2 : MemLp (gradient f) 2 μ)
    (hp : Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) μ) :
    let fn := fun n : ℕ => fun x : E => radialSmoothCutoff ((n:ℝ)+1) x * f x
    Tendsto (fun n => ∫ x, (fn n x)^2 ∂μ) atTop (𝓝 (∫ x, (f x)^2 ∂μ)) ∧
    Tendsto (fun n => ∫ x, (fn n x)^2 * Real.log ((fn n x)^2) ∂μ)
      atTop (𝓝 (∫ x, (f x)^2 * Real.log ((f x)^2) ∂μ)) ∧
    Tendsto (fun n => ∫ x, ‖gradient (fn n) x‖^2 ∂μ)
      atTop (𝓝 (∫ x, ‖gradient f x‖^2 ∂μ)) :=
  cutoff_integral_limits μ f hf hf2 hgrad2 hp

-- An actual consumer: produce the square-root analytic domain and the
-- genuine gradient-L2 handoff internally, then use only compact-smooth LSI.
-- This is a focused test, not another public leaf or the full Exercise1.7.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsFiniteMeasure μ] (C : ℝ)
    (hLSI : ∀ (v : E → ℝ), ContDiff ℝ ∞ v → HasCompactSupport v →
      (∫ x, (v x)^2 * Real.log ((v x)^2) ∂μ) -
        (∫ x, (v x)^2 ∂μ) * Real.log (∫ x, (v x)^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient v x‖^2 ∂μ)
    (f : E → ℝ) (hf : ContDiff ℝ ∞ f) {M : ℝ} (hbound : ∀ x, |f x| ≤ M)
    (hcompact : HasCompactSupport (gradient f)) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∫ x, (Real.sqrt (1+e*f x))^2 * Real.log ((Real.sqrt (1+e*f x))^2) ∂μ) -
        (∫ x, (Real.sqrt (1+e*f x))^2 ∂μ) *
          Real.log (∫ x, (Real.sqrt (1+e*f x))^2 ∂μ) ≤
      2 * C * ∫ x, ‖gradient (fun y => Real.sqrt (1+e*f y)) x‖^2 ∂μ := by
  have hnorm (g : E → ℝ) (x : E) : ‖fderiv ℝ g x‖ = ‖gradient g x‖ := by
    rw [← toDual_gradient]
    exact (InnerProductSpace.toDual ℝ E).norm_map _
  have hcompactFD : HasCompactSupport (fderiv ℝ f) := by
    simpa only [Function.comp_def, toDual_gradient] using
      hcompact.comp_left (g := fun v : E => (InnerProductSpace.toDual ℝ E) v) (by simp)
  obtain ⟨_, hdata⟩ := eventually_contDiff_and_integrable_sqrt_perturbation
    μ f hf hbound hcompactFD
  filter_upwards [hdata] with e he
  rcases he with ⟨_, hsmooth, htwo, hentropy, henergy⟩
  have hmeas : AEStronglyMeasurable (gradient (fun y => Real.sqrt (1+e*f y))) μ :=
    (AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one
      (hsmooth.of_le (by norm_num))).aestronglyMeasurable
  have hgradEnergy : Integrable
      (fun x => ‖gradient (fun y => Real.sqrt (1+e*f y)) x‖^2) μ := by
    simpa only [hnorm] using henergy
  have hgradTwo := (memLp_two_iff_integrable_sq_norm hmeas).mpr hgradEnergy
  exact logSobolev_of_compact_test μ C hLSI (fun y => Real.sqrt (1+e*f y))
    hsmooth htwo hgradTwo hentropy

#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff.cutoff_integral_limits
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff.logSobolev_of_compact_test

end Tests.Shared.LogSobolevCutoff
