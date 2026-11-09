/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels

open MeasureTheory ProbabilityTheory
open scoped BigOperators Classical
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
  AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.RadialLevels

-- The literal field family has its exact marginals and mutual independence.
example (n : ℕ+) (h : ℕ)
    (x : Fin (h + 1) → EuclideanSpace ℝ (Fin n.val)) :
    let L := Fin (h + 1)
    let P := {p : Fin (2 ^ (64 * (h + 1)) + 1) // Even p.val ∧ 4 ≤ p.val}
    let B := L × P
    let C := fun b : B ↦
      ((Fin b.2.val.val × (Σ j : Fin (h - b.1.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)
    let E := fun b : B ↦ EuclideanSpace ℝ (C b)
    let degree := fun p : P ↦
      (⟨p.val.val, p.property.1, p.property.2, Nat.le_of_lt_succ p.val.isLt⟩ :
        {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    let S := fun i : L ↦ ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a := fun (i : L) (p : P) ↦ 1 / ((p.val.val : ℝ) ^ 4 * (S i : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S i)))
    let χ := fun r : ℝ ↦
      expNegInvGlue (r - 13 / 20) /
        (expNegInvGlue (r - 13 / 20) + expNegInvGlue (7 / 10 - r)) *
      (expNegInvGlue (1 - r) /
        (expNegInvGlue (1 - r) + expNegInvGlue (r - 19 / 20)))
    let tail := fun (i : L) (j : Fin (h - i.val + 1)) ↦ x ⟨i.val + j.val, by omega⟩
    let c := fun i : L ↦ ∏ j, χ (‖tail i j‖ / Real.sqrt n.val)
    let field := fun (i : L) (z : (p : P) → E (i, p)) ↦
      if ∃ j, tail i j = 0 then 0 else
        c i * ∑ p : P, angularDegreeComponent n h i (degree p)
          (fun j ↦ NormedSpace.normalize (tail i j)) (z p)
    let Ω := EuclideanSpace ℝ (Σ b : B, C b)
    let H := fun (ξ : Ω) (i : L) ↦ field i
      (fun p ↦ WithLp.toLp 2 (fun k : C (i, p) ↦ ξ ⟨(i, p), k⟩))
    let μ := stdGaussian Ω
    let target := fun i : L ↦
      gaussianReal 0 (((n.val : ℝ) * (c i) ^ 2 * ∑ p : P, (a i p) ^ 2).toNNReal)
    (∀ i : L, HasLaw (fun ξ ↦ H ξ i) (target i) μ) ∧
      iIndepFun (fun i ξ ↦ H ξ i) μ := by
  intro L P B C E degree S a χ tail c field Ω H μ target
  have hJoint : HasLaw H (Measure.pi target) μ := radialLevels_hasLaw n h x
  have hMarginal (i : L) : HasLaw (fun ξ ↦ H ξ i) (target i) μ := by
    have hEval := measurePreserving_eval (μ := target) i
    exact hEval.fun_comp_hasLaw hJoint
  exact ⟨hMarginal, (iIndepFun_iff_hasLaw_pi_pi hMarginal).2 hJoint⟩

#print axioms radialLevels_hasLaw
#check @radialLevels_hasLaw
