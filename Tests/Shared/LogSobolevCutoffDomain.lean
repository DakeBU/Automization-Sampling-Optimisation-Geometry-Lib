import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Countable

open MeasureTheory
open scoped ContDiff ENNReal
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff

-- Compact smoothness alone is not an integrability condition on an arbitrary
-- Borel measure. This test isolates the convention in the compact LSI premise,
-- not a counterexample to the extension on its genuine integrable domain.
example :
    let μ : Measure ℝ := (⊤ : ℝ≥0∞) • Measure.dirac 0
    let f : ℝ → ℝ := radialSmoothCutoff 1
    ContDiff ℝ ∞ f ∧ HasCompactSupport f ∧
      ¬ Integrable (fun x => f x ^ 2) μ ∧ (∫ x, f x ^ 2 ∂μ) = 0 := by
  let μ : Measure ℝ := (⊤ : ℝ≥0∞) • Measure.dirac 0
  let f : ℝ → ℝ := radialSmoothCutoff 1
  have hzero : f 0 = 1 := radialSmoothCutoff_eq_one_of_norm_le zero_lt_one (by simp)
  have hnot : ¬ Integrable (fun x => f x ^ 2) μ := by
    intro hf
    have hfin := hasFiniteIntegral_iff_enorm.mp hf.hasFiniteIntegral
    dsimp only [μ] at hfin
    rw [lintegral_smul_measure, lintegral_dirac, hzero] at hfin
    simp at hfin
  exact ⟨radialSmoothCutoff_contDiff zero_lt_one, radialSmoothCutoff_hasCompactSupport zero_lt_one,
    hnot, integral_undef hnot⟩
