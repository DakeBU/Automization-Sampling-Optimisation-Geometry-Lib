/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel

open MeasureTheory ProbabilityTheory
open scoped BigOperators Classical
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
  AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevel

-- The literal field has the stated moments at every deterministic location.
example (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
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
    let μ := stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))
    (∫ ξ, H ξ ∂μ) = 0 ∧ Var[H; μ] = (n.val : ℝ) * c ^ 2 * ∑ p : P, (a p) ^ 2 := by
  intro P B C degree S a χ c F H μ
  have hH : HasLaw H
      (gaussianReal 0 (((n.val : ℝ) * c ^ 2 * ∑ p : P, (a p) ^ 2).toNNReal)) μ :=
    radialLevel_hasLaw n h i x
  constructor
  · rw [hH.integral_eq, integral_id_gaussianReal]
  · rw [hH.variance_eq, variance_id_gaussianReal]
    exact Real.coe_toNNReal _
      (mul_nonneg (mul_nonneg (Nat.cast_nonneg n.val) (sq_nonneg c))
        (Finset.sum_nonneg fun p _ ↦ sq_nonneg (a p)))

#print axioms radialLevel_hasLaw
#check @radialLevel_hasLaw
