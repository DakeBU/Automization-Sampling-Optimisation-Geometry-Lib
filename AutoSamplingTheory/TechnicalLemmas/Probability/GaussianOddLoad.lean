/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

/-!
# Exponential comparison for an odd Gaussian load

The symmetry/cosh argument in Zhou–Suzuki, arXiv:2611.05813v1, Section 6.2,
Fact 10 (source CC BY 4.0), generalized to a measurable odd sublinear load.
This is an original implementation using Mathlib's Gaussian MGF. Integrability
is a conclusion, including zero variance. The paper's literal truncated load
and its conditional level-by-level iteration are separate consumers, not proved
by this generic lemma alone.
-/

open MeasureTheory
open scoped NNReal

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad

/-- A measurable odd load with linear absolute bound has a Gaussian exponential
moment no larger than the corresponding linear load. The absolute bound itself
forces `β ≥ 0`; no positive variance or supplied integrability is required. -/
theorem gaussian_odd_load_bound {U : ℝ → ℝ} {β a : ℝ} (v : ℝ≥0)
    (hU : Measurable U) (hodd : Function.Odd U)
    (hbound : ∀ y, |U y| ≤ β * |y|) (ha : a ∈ Set.Icc (0 : ℝ) 1) :
    Integrable (fun y ↦ Real.exp (-a * U y)) (ProbabilityTheory.gaussianReal 0 v) ∧
      (∫ y, Real.exp (-a * U y) ∂ProbabilityTheory.gaussianReal 0 v) ≤
        Real.exp (β ^ 2 * (v : ℝ) / 2) := by
  let μ := ProbabilityTheory.gaussianReal 0 v
  have hβ : 0 ≤ β := by simpa using (abs_nonneg (U 1)).trans (hbound 1)
  have hmag (y : ℝ) : |a * U y| ≤ |β * y| := by
    rw [abs_mul, abs_mul, abs_of_nonneg ha.1, abs_of_nonneg hβ]
    exact (mul_le_of_le_one_left (abs_nonneg _) ha.2).trans (hbound y)
  have hpos : Integrable (fun y ↦ Real.exp (β * y)) μ :=
    ProbabilityTheory.integrable_exp_mul_gaussianReal β
  have hneg : Integrable (fun y ↦ Real.exp (-β * y)) μ :=
    ProbabilityTheory.integrable_exp_mul_gaussianReal (-β)
  have hdom (y : ℝ) : Real.exp |a * U y| ≤ Real.exp (β * y) + Real.exp (-β * y) := by
    apply (Real.exp_le_exp.mpr (hmag y)).trans
    by_cases hy : 0 ≤ β * y
    · rw [abs_of_nonneg hy]
      exact le_add_of_nonneg_right (Real.exp_pos _).le
    · rw [abs_of_neg (lt_of_not_ge hy), neg_mul]
      exact le_add_of_nonneg_left (Real.exp_pos _).le
  have hiPlus : Integrable (fun y ↦ Real.exp (a * U y)) μ :=
    (hpos.add hneg).mono' (by fun_prop) (Filter.Eventually.of_forall fun y ↦ by
      rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
      exact (Real.exp_le_exp.mpr (le_abs_self _)).trans (hdom y))
  have hiMinus : Integrable (fun y ↦ Real.exp (-a * U y)) μ :=
    (hpos.add hneg).mono' (by fun_prop) (Filter.Eventually.of_forall fun y ↦ by
      rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _), neg_mul]
      exact (Real.exp_le_exp.mpr (neg_le_abs _)).trans (hdom y))
  have hsym : (∫ y, Real.exp (a * U y) ∂μ) = ∫ y, Real.exp (-a * U y) ∂μ := by
    have hm : μ.map (fun y ↦ -y) = μ := by
      simp only [μ, ProbabilityTheory.gaussianReal_map_neg, neg_zero]
    calc
      _ = ∫ y, Real.exp (a * U y) ∂μ.map (fun y ↦ -y) := by rw [hm]
      _ = ∫ y, Real.exp (a * U (-y)) ∂μ := integral_map (by fun_prop) (by fun_prop)
      _ = _ := by simp only [hodd _, mul_neg, neg_mul]
  have hiCosh : Integrable (fun y ↦ Real.cosh (a * U y)) μ := by
    simpa only [Real.cosh_eq, neg_mul, Pi.add_apply] using (hiPlus.add hiMinus).div_const 2
  have hiLinear : Integrable (fun y ↦ Real.cosh (β * y)) μ := by
    simpa only [Real.cosh_eq, neg_mul, Pi.add_apply] using (hpos.add hneg).div_const 2
  have hcosh : (∫ y, Real.exp (-a * U y) ∂μ) = ∫ y, Real.cosh (a * U y) ∂μ := by
    simp_rw [Real.cosh_eq, ← neg_mul]
    rw [integral_div, integral_add hiPlus hiMinus, hsym]
    ring
  have hmgf (t : ℝ) : (∫ y, Real.exp (t * y) ∂μ) = Real.exp ((v : ℝ) * t ^ 2 / 2) := by
    simpa only [ProbabilityTheory.mgf, zero_mul, zero_add] using
      congrFun (ProbabilityTheory.mgf_fun_id_gaussianReal (μ := 0) (v := v)) t
  refine ⟨hiMinus, ?_⟩
  calc
    _ = ∫ y, Real.cosh (a * U y) ∂μ := hcosh
    _ ≤ ∫ y, Real.cosh (β * y) ∂μ :=
      integral_mono hiCosh hiLinear (fun y ↦ Real.cosh_le_cosh.mpr (hmag y))
    _ = _ := by
      simp_rw [Real.cosh_eq, ← neg_mul]
      rw [integral_div, integral_add hpos hneg, hmgf β, hmgf (-β)]
      rw [neg_sq, mul_comm (v : ℝ) (β ^ 2)]
      ring

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad
