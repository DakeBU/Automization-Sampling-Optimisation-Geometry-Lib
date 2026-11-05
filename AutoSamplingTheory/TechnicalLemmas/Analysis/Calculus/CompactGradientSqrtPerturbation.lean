/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Samplinglib contributors
-/
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.BoundedPerturbationEnergy
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.Analysis.SpecialFunctions.Log.NegMulLog

/-!
# Smooth square-root perturbations with finite analytic integrals

Produce the actual analytic inputs used by the noncompact test in Chewi,
*Log-Concave Sampling* (August20 2026), Exercise1.7 (printed43/PDF55).
The bound is global, unlike the a.e. bound in the generic energy-limit theorem:
it gives everywhere positivity and genuine `C^infinity` regularity. Compactness
is imposed on the derivative, not on the function after centering.

No LSI-domain extension, probability/KL/Fisher identification or Poincare
conclusion is asserted. The future exercise must derive this source test class
from its actual input and separately justify compact cutoff/LSI application.
-/

set_option autoImplicit false

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation

open MeasureTheory Filter
open scoped Topology ContDiff

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- A bounded smooth function with compact derivative support produces finite
square-root perturbation integrals on a finite measure. All integrability,
including the original energy, is derived rather than supplied as a premise.

The conclusion includes zero and both signs of sufficiently small parameters.
The square root is globally smooth, but generally not compactly supported; this
does not authorize applying a compact-test logarithmic Sobolev inequality.
-/
theorem eventually_contDiff_and_integrable_sqrt_perturbation
    [MeasurableSpace E] [OpensMeasurableSpace E]
    (mu : Measure E) [IsFiniteMeasure mu] (f : E → ℝ)
    (hf : ContDiff ℝ ∞ f) {M : ℝ} (hbound : ∀ x, |f x| ≤ M)
    (hcompact : HasCompactSupport (fderiv ℝ f)) :
    Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu ∧
    ∀ᶠ e : ℝ in 𝓝 (0 : ℝ),
      (∀ x, 1 / 2 ≤ 1 + e * f x) ∧
      ContDiff ℝ ∞ (fun x => Real.sqrt (1 + e * f x)) ∧
      MemLp (fun x => Real.sqrt (1 + e * f x)) 2 mu ∧
      Integrable (fun x => (Real.sqrt (1 + e * f x)) ^ 2 *
        Real.log ((Real.sqrt (1 + e * f x)) ^ 2)) mu ∧
      Integrable (fun x =>
        ‖fderiv ℝ (fun y => Real.sqrt (1 + e * f y)) x‖ ^ 2) mu := by
  have hfd : Continuous (fderiv ℝ f) := hf.continuous_fderiv (by simp)
  have hcH : HasCompactSupport (fun x => ‖fderiv ℝ f x‖ ^ 2) :=
    hcompact.comp_left (g := fun A : E →L[ℝ] ℝ => ‖A‖ ^ 2) (by simp)
  have hH : Integrable (fun x => ‖fderiv ℝ f x‖ ^ 2) mu :=
    (hfd.norm.pow 2).integrable_of_hasCompactSupport hcH
  have henergy :=
    (BoundedPerturbationEnergy.eventually_integrable_and_tendsto_sqrt_perturbation_energy
      mu f (hf.differentiable (by simp)) (ae_of_all mu hbound) hH).1
  have hsmall : ∀ᶠ e : ℝ in 𝓝 (0 : ℝ), |e| * |M| < 1 / 2 :=
    (isOpen_lt (continuous_abs.mul continuous_const) continuous_const).mem_nhds (by norm_num)
  obtain ⟨C, hC⟩ := isCompact_Icc.exists_bound_of_continuousOn
    (Real.continuous_mul_log.continuousOn :
      ContinuousOn (fun q : ℝ => q * Real.log q) (Set.Icc (1 / 2 : ℝ) (3 / 2)))
  refine ⟨hH, ?_⟩
  filter_upwards [hsmall, henergy] with e he hE
  have hinterval (x : E) : 1 + e * f x ∈ Set.Icc (1 / 2 : ℝ) (3 / 2) := by
    have hb : |e * f x| < 1 / 2 := by
      rw [abs_mul]
      exact (mul_le_mul_of_nonneg_left ((hbound x).trans (le_abs_self M))
        (abs_nonneg e)).trans_lt he
    constructor <;> linarith [neg_abs_le (e * f x), le_abs_self (e * f x)]
  have hpos (x : E) : 0 < 1 + e * f x := by linarith [(hinterval x).1]
  have hu : ContDiff ℝ ∞ (fun x => Real.sqrt (1 + e * f x)) :=
    (contDiff_const.add (contDiff_const.mul hf)).sqrt (fun x => ne_of_gt (hpos x))
  have hu2 : MemLp (fun x => Real.sqrt (1 + e * f x)) 2 mu := by
    apply MemLp.of_bound hu.continuous.aestronglyMeasurable 2
    filter_upwards with x
    rw [Real.norm_eq_abs, abs_of_nonneg (Real.sqrt_nonneg _)]
    exact (Real.sqrt_le_iff).2 ⟨by norm_num, by linarith [(hinterval x).2]⟩
  have hlog : Integrable (fun x => (Real.sqrt (1 + e * f x)) ^ 2 *
      Real.log ((Real.sqrt (1 + e * f x)) ^ 2)) mu := by
    refine (integrable_const C).mono' ?_ ?_
    · exact (Real.continuous_mul_log.comp (hu.continuous.pow 2)).aestronglyMeasurable
    · filter_upwards with x
      rw [Real.sq_sqrt (hpos x).le]
      exact hC _ (hinterval x)
  exact ⟨fun x => (hinterval x).1, hu, hu2, hlog, hE⟩

end AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.CompactGradientSqrtPerturbation
