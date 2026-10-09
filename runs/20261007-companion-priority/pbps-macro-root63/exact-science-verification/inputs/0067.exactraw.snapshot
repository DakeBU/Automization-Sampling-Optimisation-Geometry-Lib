import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.MeasureTheory.Measure.Count
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.Deriv.Support
open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal Topology BigOperators
noncomputable section
#check (∀ (f : ℝ → ℝ), ContDiff ℝ 2 f → HasCompactSupport f →
    let γ : Measure ℝ := gaussianReal 0 1
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
    2 * ∫ x, (deriv f x)^2 ∂γ
 : Prop)
