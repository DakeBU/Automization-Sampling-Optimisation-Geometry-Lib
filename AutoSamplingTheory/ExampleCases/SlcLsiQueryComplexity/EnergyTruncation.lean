/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Probability.HasLaw
import Mathlib.Data.PNat.Basic

/-!
# The literal energy truncation and its Gaussian bound

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), footnote 3, Eq. (17), and Fact 10.
The definition uses the source's rho quotient, not an abstract odd load. Its
positive parameter types exclude off-source zero-denominator defaults. The
proof identifies the integrand with the existing canonical cutoff and derives
all hypotheses of the Gaussian comparison internally. This does not construct
the recursive amplitudes, coefficient fields, or conditional iteration of
Lemma 6.2, nor prove the main sampling query lower bounds.
-/

open MeasureTheory
open scoped NNReal
open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Cutoff
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.EnergyTruncation

/-- The literal source energy truncation on positive source parameters.
`expNegInvGlue` is rho and the interval integral is oriented. -/
noncomputable def energyTruncation (n : ℕ+) (β lam : {r : ℝ // 0 < r}) (y : ℝ) : ℝ :=
  (n : ℝ) * (β : ℝ) ^ 2 / (lam : ℝ) *
    ∫ s in (0 : ℝ)..((lam : ℝ) * y / ((n : ℝ) * (β : ℝ))),
      expNegInvGlue (2 - |s|) /
        (expNegInvGlue (2 - |s|) + expNegInvGlue (|s| - 1))

private theorem kernel_eq_cutoff (s : ℝ) :
    expNegInvGlue (2 - |s|) /
      (expNegInvGlue (2 - |s|) + expNegInvGlue (|s| - 1)) = smoothUnitCutoff s := by
  have harg : 1 - (2 - |s|) = |s| - 1 := by ring
  have hden : 0 < expNegInvGlue (2 - |s|) + expNegInvGlue (|s| - 1) := by
    simpa only [harg] using Real.smoothTransition.pos_denom (2 - |s|)
  rw [div_eq_iff hden.ne', smoothUnitCutoff_eq_smoothTransition,
    Real.smoothTransition, harg, div_mul_cancel₀ _ hden.ne']

private theorem primitive_continuous :
    Continuous (fun t : ℝ ↦ ∫ s in (0 : ℝ)..t, smoothUnitCutoff s) :=
  (intervalIntegral.differentiable_integral_of_continuous
    smoothUnitCutoff_contDiff.continuous).continuous

private theorem primitive_odd (t : ℝ) :
    (∫ s in (0 : ℝ)..(-t), smoothUnitCutoff s) =
      -(∫ s in (0 : ℝ)..t, smoothUnitCutoff s) := by
  have heven (s : ℝ) : smoothUnitCutoff (-s) = smoothUnitCutoff s := by
    simp only [smoothUnitCutoff_eq_smoothTransition, abs_neg]
  have h := intervalIntegral.integral_comp_neg (f := smoothUnitCutoff) (a := 0) (b := t)
  simp only [heven, neg_zero] at h
  rw [intervalIntegral.integral_symm, ← h]

private theorem primitive_abs_le (t : ℝ) :
    |∫ s in (0 : ℝ)..t, smoothUnitCutoff s| ≤ |t| := by
  have h := intervalIntegral.norm_integral_le_of_norm_le_const
    (a := 0) (b := t) (C := 1) (f := smoothUnitCutoff) (fun s _ ↦ by
      rw [Real.norm_eq_abs, abs_of_nonneg (smoothUnitCutoff_mem_Icc s).1]
      exact (smoothUnitCutoff_mem_Icc s).2)
  simpa only [Real.norm_eq_abs, sub_zero, one_mul] using h

private theorem load_eq (n : ℕ+) (β lam : {r : ℝ // 0 < r}) (y : ℝ) :
    energyTruncation n β lam y = (n : ℝ) * (β : ℝ) ^ 2 / (lam : ℝ) *
      ∫ s in (0 : ℝ)..((lam : ℝ) * y / ((n : ℝ) * (β : ℝ))), smoothUnitCutoff s := by
  simp only [energyTruncation, kernel_eq_cutoff]

private theorem load_continuous (n : ℕ+) (β lam : {r : ℝ // 0 < r}) :
    Continuous (energyTruncation n β lam) := by
  simp_rw [show energyTruncation n β lam = fun y ↦ (n : ℝ) * (β : ℝ) ^ 2 / (lam : ℝ) *
      ∫ s in (0 : ℝ)..((lam : ℝ) * y / ((n : ℝ) * (β : ℝ))), smoothUnitCutoff s
    from funext (load_eq n β lam)]
  exact continuous_const.mul (primitive_continuous.comp (by fun_prop))

private theorem load_odd (n : ℕ+) (β lam : {r : ℝ // 0 < r}) :
    Function.Odd (energyTruncation n β lam) := by
  intro y
  simp only [load_eq, mul_neg, neg_div, primitive_odd, mul_neg]

private theorem load_abs_le (n : ℕ+) (β lam : {r : ℝ // 0 < r}) (y : ℝ) :
    |energyTruncation n β lam y| ≤ (β : ℝ) * |y| := by
  have hn : (0 : ℝ) < n := by exact_mod_cast n.pos
  have hβ : (0 : ℝ) < β := β.property
  have hlam : (0 : ℝ) < lam := lam.property
  rw [load_eq, abs_mul, abs_of_pos (div_pos (mul_pos hn (sq_pos_of_pos hβ)) hlam)]
  calc
    _ ≤ (n : ℝ) * (β : ℝ) ^ 2 / (lam : ℝ) *
        |(lam : ℝ) * y / ((n : ℝ) * (β : ℝ))| :=
      mul_le_mul_of_nonneg_left (primitive_abs_le _) (by positivity)
    _ = (β : ℝ) * |y| := by
      rw [abs_div, abs_mul, abs_mul, abs_of_pos hn, abs_of_pos hβ, abs_of_pos hlam]
      field_simp

/-- Fact 10 for the literal source load, including exponential integrability and
arbitrary underlying probability space. Zero Gaussian variance is allowed. -/
theorem energyTruncation_gaussian_bound {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) (n : ℕ+) (β lam : {r : ℝ // 0 < r}) {Y : Ω → ℝ}
    (v : ℝ≥0) (hY : ProbabilityTheory.HasLaw Y (ProbabilityTheory.gaussianReal 0 v) P)
    {a : ℝ} (ha : a ∈ Set.Icc (0 : ℝ) 1) :
    Integrable (fun ω ↦ Real.exp (-a * energyTruncation n β lam (Y ω))) P ∧
      (∫ ω, Real.exp (-a * energyTruncation n β lam (Y ω)) ∂P) ≤
        Real.exp ((β : ℝ) ^ 2 * ProbabilityTheory.variance Y P / 2) := by
  obtain ⟨hint, hbound⟩ := gaussian_odd_load_bound (β := (β : ℝ)) v
    (load_continuous n β lam).measurable (load_odd n β lam) (load_abs_le n β lam) ha
  have hi : Integrable (fun ω ↦ Real.exp (-a * energyTruncation n β lam (Y ω))) P := by
    have hm : Integrable (fun y ↦ Real.exp (-a * energyTruncation n β lam y)) (P.map Y) := by
      rwa [hY.map_eq]
    exact hm.comp_aemeasurable hY.aemeasurable
  refine ⟨hi, ?_⟩
  have heq := hY.integral_comp hint.aestronglyMeasurable
  have hv : ProbabilityTheory.variance Y P = (v : ℝ) := by
    rw [hY.variance_eq, ProbabilityTheory.variance_id_gaussianReal]
  simpa only [Function.comp_def, hv] using heq.trans_le hbound

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.EnergyTruncation
