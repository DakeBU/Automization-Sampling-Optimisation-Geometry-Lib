/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum

open MeasureTheory ProbabilityTheory
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
  AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegreeSum

-- Exercise the actual source sum and its exact first and second centered moments.
example (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (hu : ∀ j, ‖u j‖ = 1) :
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
    let F := fun (ξ : EuclideanSpace ℝ (Σ b : B, C b)) ↦ ∑ p : P,
      angularDegreeComponent n h i (degree p) u
        (WithLp.toLp 2 (fun c : C (i, p) ↦ ξ ⟨(i, p), c⟩))
    let μ := stdGaussian (EuclideanSpace ℝ (Σ b : B, C b))
    (∫ ξ, F ξ ∂μ) = 0 ∧ Var[F; μ] = (n.val : ℝ) * ∑ p : P, (a p) ^ 2 := by
  intro P B C degree S a F μ
  have h : HasLaw F (gaussianReal 0 (((n.val : ℝ) * ∑ p : P, (a p) ^ 2).toNNReal)) μ :=
    angularDegreeSum_hasLaw n h i u hu
  constructor
  · rw [h.integral_eq, integral_id_gaussianReal]
  · rw [h.variance_eq, variance_id_gaussianReal]
    exact Real.coe_toNNReal _ (mul_nonneg (Nat.cast_nonneg n.val)
      (Finset.sum_nonneg fun p _ ↦ sq_nonneg (a p)))

#print axioms angularDegreeSum_hasLaw
#check @angularDegreeSum_hasLaw
