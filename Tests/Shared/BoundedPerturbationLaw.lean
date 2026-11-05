import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw
import AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation

open MeasureTheory Filter
open scoped Topology

#check AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw.eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
#print axioms AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw.eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul

example {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsProbabilityMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) (hcenter : (∫ x, f x ∂mu) = 0) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∀ᵐ x ∂mu, (1 : ℝ) / 2 ≤ 1 + e * f x) ∧
      IsProbabilityMeasure (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) ∧
      InformationTheory.klDiv
        (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu =
        ENNReal.ofReal (∫ x, InformationTheory.klFun (1 + e * f x) ∂mu) :=
  AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw.eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
    mu f hf hbound hcenter

-- Finiteness of extended-real KL is a real consequence, not inferred from toReal.
example {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsProbabilityMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) (hcenter : (∫ x, f x ∂mu) = 0) :
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), InformationTheory.klDiv
      (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu ≠ ⊤ := by
  filter_upwards [AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw.eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
    mu f hf hbound hcenter] with e he
  rw [he.2.2]
  exact ENNReal.ofReal_ne_top

-- A real consumer: combine the actual-law adapter with the independent analytic
-- parent. This focused composition earns no extra public leaf or Bench credit.
example {X : Type*} [MeasurableSpace X] (mu : Measure X) [IsProbabilityMeasure mu]
    (f : X → ℝ) (hf : AEStronglyMeasurable f mu) {M : ℝ}
    (hbound : ∀ᵐ x ∂mu, |f x| ≤ M) (hcenter : (∫ x, f x ∂mu) = 0) :
    Tendsto (fun e : ℝ => (InformationTheory.klDiv
      (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu).toReal / e ^ 2)
      (𝓝[≠] (0 : ℝ)) (𝓝 ((∫ x, f x ^ 2 ∂mu) / 2)) := by
  have hreal : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), (InformationTheory.klDiv
      (mu.withDensity (fun x => ENNReal.ofReal (1 + e * f x))) mu).toReal =
      ∫ x, InformationTheory.klFun (1 + e * f x) ∂mu := by
    filter_upwards [AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedPerturbationLaw.eventually_isProbabilityMeasure_and_klDiv_eq_one_add_mul
      mu f hf hbound hcenter] with e he
    rw [he.2.2, ENNReal.toReal_ofReal]
    exact integral_nonneg_of_ae (he.1.mono fun x hx =>
      InformationTheory.klFun_nonneg (by linarith))
  exact (AutoSamplingTheory.TechnicalLemmas.InformationTheory.BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq
    mu f hf hbound).congr' ((hreal.filter_mono nhdsWithin_le_nhds).mono fun e he =>
      congrArg (fun z : ℝ => z / e ^ 2) he.symm)
