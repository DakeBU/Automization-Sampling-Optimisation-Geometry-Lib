import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation

open MeasureTheory Filter
open scoped Topology

#check @AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq
#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq

-- The exact finite-measure signature includes a.e. bounds, not pointwise
-- regularity, probability normalization or a supplied integral limit.
example {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsFiniteMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) :
    Tendsto (fun e : ℝ => (∫ x, InformationTheory.klFun (1 + e * f x) ∂mu) / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, f x ^ 2 ∂mu) / 2)) :=
  AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq
    mu f hf hbound
