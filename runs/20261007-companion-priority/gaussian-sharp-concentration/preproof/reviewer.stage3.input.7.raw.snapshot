import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle

import Mathlib.Probability.Distributions.Gaussian.Fernique

open MeasureTheory ProbabilityTheory

open scoped NNReal ENNReal Topology

noncomputable section

def anonymous_statement_type0 {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {L : ℝ≥0} {f : E → ℝ} (hf : LipschitzWith L f) (t : ℝ) : Prop :=
    (∫ x, Real.exp (t * (f x - ∫ z, f z ∂ProbabilityTheory.stdGaussian E))
      ∂ProbabilityTheory.stdGaussian E) ≤ Real.exp ((L : ℝ)^2 * t^2 / 2)

#check @anonymous_statement_type0

def anonymous_statement_type1 {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) : Prop :=
    let F := fun s x => V x + (eta s)⁻¹/2*‖x-y s‖^2
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s + eta s • gradient V (p s) = y s) ∧
      (∀ s z, F s (p s) + (κ⁻¹+(eta s)⁻¹)/2*‖z-p s‖^2 ≤ F s z ∧
        (F s z ≤ F s (p s) ↔ z=p s)) ∧
      (∀ s t, eta s = eta t → ‖p s-p t‖ ≤ ‖y s-y t‖) ∧
      let G := fun q : S × E => gradient V (p q.1+Real.sqrt (eta q.1) • q.2)
      Measurable G ∧
      (∀ s t z w, eta s = eta t →
        ‖G (s,z)-G (t,w)‖ ≤ ‖y s-y t‖+Real.sqrt (eta s)*‖z-w‖) ∧
      ∃ K : ProbabilityTheory.Kernel S E, ProbabilityTheory.IsMarkovKernel K ∧
        (∀ s, K s = (ProbabilityTheory.stdGaussian E).map (fun z => G (s,z))) ∧
        ∀ s, MeasureTheory.Integrable (fun w : E => w) (K s) ∧
          ∀ (a : E) (t : ℝ), MeasureTheory.Integrable
            (fun w => Real.exp (t * inner ℝ a (w - ∫ v, v ∂K s))) (K s) ∧
            (∫ w, Real.exp (t * inner ℝ a (w - ∫ v, v ∂K s)) ∂K s) ≤
              Real.exp (eta s * t^2 * ‖a‖^2 / 2)

#check @anonymous_statement_type1

