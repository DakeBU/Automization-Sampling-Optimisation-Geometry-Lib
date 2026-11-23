import GC41Asymptotic

/-! Section 4.3 of Zhou–Suzuki, *On Complexity of Gaussian Sampling*.
The original strict test is evaluated on an actual sample in ambient coordinates.
A single dimension cutoff works for every permitted condition number, mode
determined by the query budget, and orientation of the hidden eigenbasis.
-/

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

theorem eventual_rotated_target_power (C : ℝ) (hC : 0 < C) {δ : ℝ} (hδ : 0 < δ) (hδ' : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ q : ℕ, (q : ℝ) ≤ δ/256 * Real.sqrt κ * Real.log (d : ℝ) →
      ∀ O : Matrix.orthogonalGroup (Fin d) ℝ,
      let A := hiddenPrecision κ O
      (9/10 : ℝ) ≤ (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹).real
        (detectorEvent κ (2*q+1) (queryThreshold C d q) A) := by
  obtain ⟨D, hD⟩ := eventual_diagonal_detector_probability C hC hδ hδ'
  refine ⟨max 2 D, ?_⟩
  intro d hd κ hκ hcap q hq O
  dsimp only
  rw [rotated_detector_probability_eq ((le_max_left 2 D).trans hd) hκ]
  exact hD d ((le_max_right 2 D).trans hd) κ hκ hcap q hq

#print axioms eventual_rotated_target_power

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
