import GC32Indistinguishability
import AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification

/-!
# Determinant-family Gaussian targets and their separation

For Eq. (8) of Zhou–Suzuki, arXiv:2610.20492v1, use exactly the two laws on
precision matrices from the first-order experiment in Eq. (7). The canonical
block-product and affinity results give separation in the original ambient
space, including the residual identity coordinates.
-/

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw
open AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

/-- The source class of real symmetric precision matrices with spectrum in [1, κ],
expressed by its equivalent quadratic-form inequalities. -/
def Admissible {d : ℕ} (κ : ℝ) (A : Precision d) : Prop :=
  A.IsHermitian ∧ ∀ x : Fin d → ℝ, x ⬝ᵥ x ≤ x ⬝ᵥ (A *ᵥ x) ∧
    x ⬝ᵥ (A *ᵥ x) ≤ κ * (x ⬝ᵥ x)

/-- Gaussian target for a fixed precision A. -/
noncomputable def targetLaw {d : ℕ} (A : Precision d) : Measure (E d) :=
  multivariateGaussian (0 : E d) A⁻¹

/-- Averaging this target over the same matrix prior as Eq. (7). -/
noncomputable def averagedTarget (d n : ℕ) (κ b : ℝ) : Measure (E d) :=
  (hardPrior d n κ b).bind targetLaw

/-- Total variation of probability measures in the measurable-event convention
of Section 2. -/
noncomputable def eventTV {α : Type*} [MeasurableSpace α] (μ ν : Measure α) : ℝ :=
  sSup {z : ℝ | ∃ B : Set α, MeasurableSet B ∧ z = |μ.real B - ν.real B|}

instance targetLaw_probability {d : ℕ} (A : Precision d) : IsProbabilityMeasure (targetLaw A) :=
  inferInstanceAs (IsProbabilityMeasure (multivariateGaussian (0 : E d) A⁻¹))

variable {d n : ℕ} {κ b : ℝ}

theorem hardPrior_probability (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (hb : b = 1 ∨ b = -1) :
    IsProbabilityMeasure (hardPrior d n κ b) :=
  (actual_averaged_block_product hn hnd hκ hb).1

theorem hardPrior_posDef (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (hb : b = 1 ∨ b = -1) :
    ∀ᵐ A ∂hardPrior d n κ b, A.PosDef :=
  (actual_averaged_block_product hn hnd hκ hb).2.1

theorem averagedTarget_probability (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (hb : b = 1 ∨ b = -1) :
    IsProbabilityMeasure (averagedTarget d n κ b) :=
  (actual_averaged_block_product hn hnd hκ hb).2.2.2.1

/-- The hard precision prior is concentrated on the admissible class. -/
theorem hardPrior_admissible (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) (b : ℝ) :
    ∀ᵐ A ∂hardPrior d n κ b, Admissible κ A := by
  let f := blockPrecision (d := d) (n := n) κ
  have hr := ae_map_mem_range f (isCompact_range (continuous_blockPrecision d n κ)).isClosed.measurableSet
    (Measure.pi fun _ : Fin (d/n) => componentHaar n b)
  filter_upwards [hr] with A hA
  obtain ⟨W,rfl⟩ := hA
  exact blockPrecision_regular hn hnd hκ W

/-- On any prior supported on positive definite matrices, the actual Gaussian
law is an almost everywhere measurable family. -/
theorem targetLaw_aeMeasurable (D : Measure (Precision d)) (hpos : ∀ᵐ A ∂D, A.PosDef) :
    AEMeasurable targetLaw D := by
  let q (A : Precision d) (x : E d) := Real.sqrt A.det /
    (2 * Real.pi) ^ ((d : ℝ) / 2) *
    Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2)
  let density := fun A : Precision d =>
    (volume : Measure (E d)).withDensity (fun x => ENNReal.ofReal (q A x))
  have hq : Continuous (Function.uncurry q) := by dsimp only [q]; fun_prop
  have hm : Measurable density := measurable_withDensity (ENNReal.measurable_ofReal.comp hq.measurable)
  exact hm.aemeasurable.congr (hpos.mono fun A hA =>
    (multivariateGaussian_eq_withDensity_of_posDef A hA).symm)

/-- Lemma 3.3 on the two ambient averaged Gaussian targets. -/
theorem averaged_target_separation (hn : 3 ≤ n) (hnd : n ≤ d) (hκ : 4 ≤ κ) :
    1 - Real.exp (-(((d/n : ℕ) : ℝ) / 8) * Real.exp (-(10 * (n : ℝ)) / Real.sqrt κ))
      ≤ eventTV (averagedTarget d n κ 1) (averagedTarget d n κ (-1)) :=
  actual_averaged_tv_lower_bound hn hnd hκ

#print axioms averaged_target_separation
#print axioms targetLaw_aeMeasurable

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
