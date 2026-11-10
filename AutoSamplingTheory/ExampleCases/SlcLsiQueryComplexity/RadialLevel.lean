/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum
import Mathlib.Analysis.Normed.Module.Normalize
import Mathlib.Analysis.SpecialFunctions.SmoothTransition

open MeasureTheory ProbabilityTheory
open scoped BigOperators Classical
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
open scoped NNReal

/-!
# One-location radial level law

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), Eq. (13)–(16), footnote 2,
and the actual level marginal at the application of Fact 10 in §6.2.
This uses the literal shell factor, not a rescaled approximation.
The location is deterministic; only the joint coefficient vector is sampled.
-/

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel

open AngularDegreeSum

/-- The zero-extended radial level has its exact centered Gaussian law.
This proves the one-point marginal, not the conditional or process law. -/
theorem radialLevel_hasLaw (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (x : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val)) :
    let P := {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let B := Fin (h + 1) × P
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let degree := fun p : P ↦
      (⟨p.val.val, p.property.1, p.property.2, Nat.le_of_lt_succ p.val.isLt⟩ :
        {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a := fun p : P ↦ 1 / ((p.val.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
    let χ := fun r : ℝ ↦
      expNegInvGlue (r - 13 / 20) /
        (expNegInvGlue (r - 13 / 20) + expNegInvGlue (7 / 10 - r)) *
      (expNegInvGlue (1 - r) /
        (expNegInvGlue (1 - r) + expNegInvGlue (r - 19 / 20)))
    let c := ∏ j, χ (‖x j‖ / Real.sqrt n.val)
    let F := fun (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
        (ξ : EuclideanSpace ℝ (Σ b : B, C b)) ↦ ∑ p : P,
      angularDegreeComponent n h i (degree p) u
        (WithLp.toLp 2 (fun c : C (i, p) ↦ ξ ⟨(i, p), c⟩))
    let H := fun ξ ↦ if ∃ j, x j = 0 then 0
      else c * F (fun j ↦ NormedSpace.normalize (x j)) ξ
    HasLaw H (gaussianReal 0 (((n.val : ℝ) * c ^ 2 * ∑ p : P, (a p) ^ 2).toNNReal))
      (stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))) := by
  intro P B C degree S a χ c F H
  let Ω := EuclideanSpace ℝ (Σ b : B, C b)
  let μ : Measure Ω := stdGaussian Ω
  let v : ℝ := ∑ p : P, (a p) ^ 2
  change HasLaw H (gaussianReal 0 (((n.val : ℝ) * c ^ 2 * v).toNNReal)) μ
  by_cases hz : ∃ j, x j = 0
  · obtain ⟨j, hj⟩ := hz
    have hρ : expNegInvGlue (0 - 13 / 20) = 0 :=
      expNegInvGlue.zero_of_nonpos (by norm_num)
    have hχ : χ 0 = 0 := by
      simp only [χ, hρ, zero_div, zero_mul]
    have hc : c = 0 := by
      apply Finset.prod_eq_zero (Finset.mem_univ j)
      simpa only [hj, norm_zero, zero_div] using hχ
    rw [hc]
    simp only [zero_pow (by decide : (2 : ℕ) ≠ 0), mul_zero, zero_mul,
      Real.toNNReal_zero, gaussianReal_zero_var]
    exact hasLaw_dirac_of_ae_eq (Filter.Eventually.of_forall fun _ ↦ if_pos ⟨j, hj⟩)
  · let u := fun j ↦ NormedSpace.normalize (x j)
    have hu (j : Fin (h - i.val + 1)) : ‖u j‖ = 1 :=
      NormedSpace.norm_normalize (fun hj ↦ hz ⟨j, hj⟩)
    have hF : HasLaw (F u) (gaussianReal 0 (((n.val : ℝ) * v).toNNReal)) μ :=
      angularDegreeSum_hasLaw n h i u hu
    have hScaled := gaussianReal_const_mul hF c
    have hH : H = fun ξ ↦ c * F u ξ := funext fun _ ↦ if_neg hz
    have hv : 0 ≤ v := Finset.sum_nonneg fun p _ ↦ sq_nonneg (a p)
    have hn : 0 ≤ (n.val : ℝ) := Nat.cast_nonneg _
    have hVar : NNReal.mk (c ^ 2) (sq_nonneg c) * ((n.val : ℝ) * v).toNNReal =
        ((n.val : ℝ) * c ^ 2 * v).toNNReal := by
      apply NNReal.coe_injective
      rw [NNReal.coe_mul, NNReal.coe_mk,
        Real.coe_toNNReal _ (mul_nonneg hn hv),
        Real.coe_toNNReal _ (mul_nonneg (mul_nonneg hn (sq_nonneg c)) hv)]
      ring
    rw [hH, ← hVar]
    simpa only [mul_zero] using hScaled

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel
