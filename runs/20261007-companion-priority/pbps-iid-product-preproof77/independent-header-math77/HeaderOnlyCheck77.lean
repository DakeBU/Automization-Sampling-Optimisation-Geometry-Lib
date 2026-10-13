import Mathlib.Probability.Distributions.Exponential
import Mathlib.Probability.Independence.InfinitePi
import Mathlib.Probability.StrongLaw

open MeasureTheory ProbabilityTheory Filter
open scoped Topology BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/-- Prospective concrete countable Exp(1) input laws, not a completed theorem.
Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1 Appendix A.1 Ex9.
The later consumer combines these actual thresholds with the compiled finite
PBPS recursion. No event-time, process, invariance or cost claim is made here.
-/
def unit_exponential_product_statement : Prop :=
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let X : ℕ → (ℕ → ℝ) → ℝ := fun k ω => ω k
  let ε : ℕ → (ℕ → ℝ) → ℝ≥0 := fun k ω => Real.toNNReal (X k ω)
  IsProbabilityMeasure P ∧
  (∀ k : ℕ, Measurable (X k) ∧ Measurable (ε k) ∧
    Measure.map (X k) P = expMeasure (1 : ℝ)) ∧
  iIndepFun X P ∧
  (∀ᵐ ω ∂P, ∀ k : ℕ, 0 < X k ω ∧ (ε k ω : ℝ) = X k ω) ∧
  (∀ᵐ ω ∂P, Tendsto (fun n : ℕ => ∑ k ∈ Finset.range n, (ε k ω : ℝ))
    atTop atTop)

#check unit_exponential_product_statement

end AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct

/- Header/type/API formation only; no proof of the target proposition. -/
#check MeasureTheory.Measure.infinitePi
#check MeasureTheory.Measure.infinitePi_map_eval
#check ProbabilityTheory.iIndepFun_infinitePi
#check ProbabilityTheory.iIndepFun.indepFun
#check ProbabilityTheory.iIndepFun.comp
#check ProbabilityTheory.isProbabilityMeasure_expMeasure
#check ProbabilityTheory.cdf_expMeasure_eq
#check ProbabilityTheory.cdf_eq_real
#check ProbabilityTheory.HasLaw.identDistrib
#check ProbabilityTheory.IdentDistrib.comp
#check ProbabilityTheory.IdentDistrib.integrable_iff
#check ProbabilityTheory.strong_law_ae_real
#check MeasureTheory.ae_all_iff
#check MeasureTheory.integrable_const
#check MeasureTheory.Integrable.indicator
#check MeasureTheory.integral_indicator_one
#check MeasureTheory.measurable_real_toNNReal
#check Real.coe_toNNReal
#check Real.GammaIntegral_convergent
#check Real.integral_rpow_mul_exp_neg_mul_Ioi
#check MeasureTheory.integrable_withDensity_iff_integrable_smul'
#check MeasureTheory.integral_withDensity_eq_integral_toReal_smul
#check Filter.tendsto_atTop_mono
