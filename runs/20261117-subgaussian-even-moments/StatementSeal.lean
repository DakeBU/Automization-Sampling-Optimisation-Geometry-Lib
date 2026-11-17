import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Series
open MeasureTheory ProbabilityTheory
open scoped BigOperators

-- Generic probability prerequisite; type seals only.
#check (∀ (x : ℝ) (m : ℕ),
  x^(2*m)/(Nat.factorial (2*m) : ℝ) ≤ Real.cosh x)

#check (∀ {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (X : Ω → ℝ) (c : NNReal)
    (hX : HasSubgaussianMGF X c μ) (m : ℕ),
    Integrable (fun ω => |X ω|^(2*m)) μ ∧
    (∫ ω, |X ω|^(2*m) ∂μ) ≤
      (Nat.factorial (2*m) : ℝ)*Real.exp (1/2)*(c : ℝ)^m)
