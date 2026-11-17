import AutoSamplingTheory.TechnicalLemmas.Probability.SubgaussianEvenMoments

open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.SubgaussianEvenMoments

-- Actual bounded-observable producer; no assumed moments of the centered variable.
example {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (X : Ω → ℝ) {a b : ℝ}
    (hX : AEMeasurable X μ) (hbound : ∀ᵐ ω ∂μ, X ω ∈ Set.Icc a b) (m : ℕ) :
    Integrable (fun ω => |X ω-(∫ ω, X ω ∂μ)|^(2*m)) μ ∧
    (∫ ω, |X ω-(∫ ω, X ω ∂μ)|^(2*m) ∂μ) ≤
      (Nat.factorial (2*m) : ℝ)*Real.exp (1/2)*
        (((‖b-a‖₊/2)^2 : NNReal) : ℝ)^m :=
  integrable_even_moment_le_of_hasSubgaussianMGF μ _ _
    (hasSubgaussianMGF_of_mem_Icc hX hbound) m

-- Actual independence-to-sum MGF producer, followed by the moment consumer.
example {Ω ι : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : ι → Ω → ℝ) (c : ι → NNReal) (s : Finset ι)
    (hindep : iIndepFun X μ)
    (hX : ∀ i ∈ s, HasSubgaussianMGF (X i) (c i) μ) (m : ℕ) :
    Integrable (fun ω => |∑ i ∈ s, X i ω|^(2*m)) μ ∧
    (∫ ω, |∑ i ∈ s, X i ω|^(2*m) ∂μ) ≤
      (Nat.factorial (2*m) : ℝ)*Real.exp (1/2)*((∑ i ∈ s, c i : NNReal) : ℝ)^m :=
  integrable_even_moment_le_of_hasSubgaussianMGF μ _ _
    (HasSubgaussianMGF.sum_of_iIndepFun hindep hX) m

#print axioms integrable_even_moment_le_of_hasSubgaussianMGF
