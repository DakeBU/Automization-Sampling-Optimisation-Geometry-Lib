import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.LogSobolevCutoff

/-! Noncompact C2 Gaussian function LSI through actual radial cutoff exhaustion.
The three analytic domains are genuine inputs; cutoff limits and the inequality
are internal obligations. Coherent posterior KL/Fisher and Gaussian T2 are separate. -/

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped Topology RealInnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev
open Analysis.Calculus.Cutoff
open LogSobolevCutoff

/-- Genuine noncompact Gaussian function LSI on the C2 analytic domain.
Cutoff mass, entropy and true-gradient energy limits are proved internally;
signed functions, zero mass and rank zero are retained. -/
theorem gaussian_logSobolev_of_contDiff
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (hf : ContDiff ℝ 2 f)
    (hf2 : MemLp f 2 (ProbabilityTheory.stdGaussian E))
    (hgrad2 : MemLp (gradient f) 2 (ProbabilityTheory.stdGaussian E))
    (hentropy : Integrable (fun x => (f x)^2 * Real.log ((f x)^2))
      (ProbabilityTheory.stdGaussian E)) :
    let γ : Measure E := ProbabilityTheory.stdGaussian E
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
      2 * ∫ x, ‖gradient f x‖^2 ∂γ := by
  dsimp only
  let γ := ProbabilityTheory.stdGaussian E
  let fn := fun n : ℕ => fun x : E => radialSmoothCutoff ((n:ℝ)+1) x * f x
  obtain ⟨hm,hp,he⟩ := cutoff_integral_limits γ f hf hf2 hgrad2 hentropy
  have hle (n : ℕ) :
      (∫ x, (fn n x)^2 * Real.log ((fn n x)^2) ∂γ) -
      (∫ x, (fn n x)^2 ∂γ) * Real.log (∫ x, (fn n x)^2 ∂γ) ≤
        2 * ∫ x, ‖gradient (fn n) x‖^2 ∂γ := by
    have hc : ContDiff ℝ 2 (radialSmoothCutoff ((n:ℝ)+1) : E → ℝ) :=
      (radialSmoothCutoff_contDiff (by positivity)).of_le
        (WithTop.coe_le_coe.mpr (le_top : (2 : ℕ∞) ≤ ⊤))
    have hs : HasCompactSupport (fn n) :=
      (radialSmoothCutoff_hasCompactSupport (by positivity)).mul_right
    exact (GaussianCompactHilbertLogSobolev.compact_stdGaussian_logSobolev
      (fn n) (hc.mul hf) hs).2.2.2
  exact le_of_tendsto_of_tendsto
    (hp.sub (Real.continuous_mul_log.continuousAt.tendsto.comp hm))
    (he.const_mul 2) (Eventually.of_forall hle)

end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev
