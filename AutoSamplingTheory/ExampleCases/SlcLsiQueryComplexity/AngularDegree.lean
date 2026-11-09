/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.HasLaw
import Mathlib.Data.PNat.Basic

/-!
# The actual Gaussian angular degree component

Zhou–Suzuki, arXiv:2611.05813v1 (CC BY 4.0), Section 4.1.1, Eq. (14)–(15).
Tensor coordinates are indexed by a choice in each repeated tensor slot. This
retains the ordered tensor, its multiplicities and the exact source amplitude.
The law is for deterministic unit directions under one actual standard Gaussian
coefficient block. Joint coefficient independence, degree summation, radial
cutoffs and conditional level iteration are separate obligations.

The isolated identity permits every positive dimension and natural depth; it
does not assert hard-family admissibility outside the source parameter regime.
The literal polynomial extends to arbitrary directions, but its Gaussian law
below uses only the source sphere domain.
-/

open MeasureTheory ProbabilityTheory
open scoped BigOperators

namespace AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree

/-- The literal Eq. (15) degree component, including the Eq. (14) amplitude.
The tensor slots select a copy of `psi`, then a trailing block and repetition.
Only its restriction to unit directions is used by the source-law theorem. -/
noncomputable def angularDegreeComponent (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (p : {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (ξ : EuclideanSpace ℝ
      ((Fin p.val × (Σ j : Fin (h - i.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val)) : ℝ :=
  let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
  let a : ℝ := 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
    Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
  Real.sqrt n.val * a * ∑ c, ξ c * ∏ s, u s.2.1 (c s)

private abbrev TensorSlots (h : ℕ) (i : Fin (h + 1)) (p : ℕ) :=
  Fin p × (Σ j : Fin (h - i.val + 1), Fin ((2 ^ (74 * (h + 1))) ^ j.val))

private noncomputable def tensorFeature (n : ℕ+) (h : ℕ) (i : Fin (h + 1)) (p : ℕ)
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val)) :
    EuclideanSpace ℝ (TensorSlots h i p → Fin n.val) :=
  WithLp.toLp 2 fun c ↦ ∏ s, u s.2.1 (c s)

private theorem tensorFeature_norm_sq (n : ℕ+) (h : ℕ) (i : Fin (h + 1)) (p : ℕ)
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (hu : ∀ j, ‖u j‖ = 1) : ‖tensorFeature n h i p u‖ ^ 2 = 1 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  change (∑ c : TensorSlots h i p → Fin n.val,
    (∏ s : TensorSlots h i p, u s.2.1 (c s)) ^ 2) = 1
  simp_rw [← Finset.prod_pow]
  rw [← Fintype.prod_sum (fun (s : TensorSlots h i p) (k : Fin n.val) ↦
    (u s.2.1 k) ^ 2)]
  simp_rw [← EuclideanSpace.real_norm_sq_eq, hu]
  simp

/-- At fixed unit directions the actual Gaussian tensor polynomial has the
source centered normal law with variance `n * a²`. This proves measurability and
the law; neither a Gaussian-law witness nor tensor normalization is assumed. -/
theorem angularDegreeComponent_hasLaw (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (p : {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (hu : ∀ j, ‖u j‖ = 1) :
    let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a : ℝ := 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
    HasLaw (angularDegreeComponent n h i p u)
      (gaussianReal 0 (((n.val : ℝ) * a ^ 2).toNNReal)) (stdGaussian _) := by
  let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
  let a : ℝ := 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
    Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
  let L : StrongDual ℝ (EuclideanSpace ℝ (TensorSlots h i p.val → Fin n.val)) :=
    (Real.sqrt n.val * a) • innerSL ℝ (tensorFeature n h i p.val u)
  change HasLaw (angularDegreeComponent n h i p u)
    (gaussianReal 0 (((n.val : ℝ) * a ^ 2).toNNReal)) (stdGaussian _)
  have hL : (fun ξ ↦ L ξ) = angularDegreeComponent n h i p u := by
    funext ξ
    change (Real.sqrt n.val * a) * inner ℝ (tensorFeature n h i p.val u) ξ =
      (Real.sqrt n.val * a) * ∑ c, ξ c * ∏ s, u s.2.1 (c s)
    congr 1
  have hnorm : ‖L‖ ^ 2 = (n.val : ℝ) * a ^ 2 := by
    simp only [L, norm_smul, innerSL_apply_norm, mul_pow, Real.norm_eq_abs, sq_abs]
    rw [tensorFeature_norm_sq n h i p.val u hu, mul_one,
      Real.sq_sqrt (Nat.cast_nonneg n.val)]
  rw [← hL]
  refine ⟨L.continuous.aemeasurable, ?_⟩
  rw [IsGaussian.map_eq_gaussianReal, integral_strongDual_stdGaussian,
    variance_dual_stdGaussian, hnorm]

end AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
