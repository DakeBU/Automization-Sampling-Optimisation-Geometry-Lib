import Mathlib.MeasureTheory.Measure.Count
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Probability.ProbabilityMassFunction.Basic

open MeasureTheory
open scoped BigOperators ENNReal
noncomputable section
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy
#check ∀ (a b : ℝ),
    (a ^ 2 * Real.log (a ^ 2) + b ^ 2 * Real.log (b ^ 2)) / 2 -
      ((a ^ 2 + b ^ 2) / 2) * Real.log ((a ^ 2 + b ^ 2) / 2) ≤
    (a - b) ^ 2 / 2
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.TwoPointEntropy

namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev
#check ∀ (n : ℕ) (h : (Fin n → Bool) → ℝ),
    let μ : Measure (Fin n → Bool) :=
      (Fintype.card (Fin n → Bool) : ℝ≥0∞)⁻¹ • Measure.count
    let D := fun ε : Fin n → Bool =>
      ∑ j : Fin n, (h ε - h (Function.update ε j (!ε j))) ^ 2
    IsProbabilityMeasure μ ∧
      Integrable (fun ε => (h ε) ^ 2) μ ∧
      Integrable (fun ε => (h ε) ^ 2 * Real.log ((h ε) ^ 2)) μ ∧
      Integrable D μ ∧
      ((∫ ε, (h ε) ^ 2 * Real.log ((h ε) ^ 2) ∂μ) -
        (∫ ε, (h ε) ^ 2 ∂μ) * Real.log (∫ ε, (h ε) ^ 2 ∂μ) ≤
      (1 / 2 : ℝ) * ∫ ε, D ε ∂μ)
end AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev
