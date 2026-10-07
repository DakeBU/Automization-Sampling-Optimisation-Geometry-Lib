import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Probability.Distributions.Gaussian.Multivariate

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace BigOperators

#check (∀
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E]
    (f : E → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f),
    let γ : Measure E := ProbabilityTheory.stdGaussian E
    Integrable (fun x => (f x)^2) γ ∧
    Integrable (fun x => (f x)^2 * Real.log ((f x)^2)) γ ∧
    Integrable (fun x => ‖gradient f x‖^2) γ ∧
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
      2 * ∫ x, ‖gradient f x‖^2 ∂γ)
