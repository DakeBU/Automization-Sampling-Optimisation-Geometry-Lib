/-
Copyright (c) 2024 Hongjia Chen, Chenyi Li, Wanyi He, Zaiwen Wen. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors of the upstream mathematical development: Hongjia Chen, Chenyi Li, Wanyi He, Zaiwen Wen
Modified for Samplinglib: native Lean 4.33.0 statements and proofs; reuse SupportsAt,
unbundle algorithm inputs and expose the weighted telescope and a finite index witness.
-/
import AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSubgradient
import Mathlib.Topology.MetricSpace.Lipschitz
import Mathlib.Data.Finset.Max
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

/-!
# Nonsmooth subgradient method

Native port of the norm bound and finite-horizon convergence argument in Optlib
`5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3`,
`Optlib/Algorithm/SubgradientMethod.lean:80–118,137–232` (Apache-2.0).

The existing `ConvexSubgradient.SupportsAt` relation is exactly the global
subgradient inequality. No duplicate predicate or upstream algorithm class is
introduced. Lipschitz growth bounds supplied subgradients, the actual update
telescopes squared distances, and a finite minimizer index supplies the best
iterate bound. Completeness, differentiability and existence of a minimizer are
not needed. This does not construct subgradients or a measurable/random oracle.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.SubgradientMethod

open ConvexSubgradient Finset
open scoped NNReal RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Global Lipschitz growth controls every supplied supporting vector.
This is consumed inside the subgradient telescope, not supplied as an extra premise. -/
theorem norm_le_of_supportsAt {f : E → ℝ} {G : ℝ≥0} {x g : E}
    (hf : LipschitzWith G f) (hs : SupportsAt f x g) : ‖g‖ ≤ (G : ℝ) := by
  have hs' := hs (x + g)
  change f x + inner ℝ g (x + g - x) ≤ f (x + g) at hs'
  rw [add_sub_cancel_left, real_inner_self_eq_norm_sq] at hs'
  have hl : f (x + g) - f x ≤ (G : ℝ) * ‖g‖ := by
    calc
      f (x + g) - f x ≤ |f (x + g) - f x| := le_abs_self _
      _ ≤ (G : ℝ) * ‖g‖ := by
        simpa [Real.dist_eq, dist_eq_norm] using hf.dist_le_mul (x + g) x
  by_cases hg : ‖g‖ = 0
  · simp [hg]
  · have hp : 0 < ‖g‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hg)
    nlinarith

/-- The actual subgradient recurrence controls the finite weighted objective gaps,
retaining the terminal squared distance. Zero steps and the empty horizon are allowed. -/
theorem sum_weighted_gap_le {f : E → ℝ} {G : ℝ≥0} {x g : ℕ → E} {a : ℕ → ℝ}
    (hf : LipschitzWith G f) (ha : ∀ k, 0 ≤ a k)
    (hs : ∀ k, SupportsAt f (x k) (g k))
    (hx : ∀ k, x (k + 1) = x k - a k • g k) (z : E) (N : ℕ) :
    2 * (∑ k ∈ Finset.range N, a k * (f (x k) - f z)) ≤
      ‖x 0 - z‖ ^ 2 + (G : ℝ) ^ 2 * (∑ k ∈ Finset.range N, (a k) ^ 2) - ‖x N - z‖ ^ 2 := by
  have hstep (k : ℕ) :
      2 * a k * (f (x k) - f z) ≤
        ‖x k - z‖ ^ 2 - ‖x (k + 1) - z‖ ^ 2 + (G : ℝ) ^ 2 * (a k) ^ 2 := by
    have hs' := hs k z
    change f (x k) + inner ℝ (g k) (z - x k) ≤ f z at hs'
    have hpair : f (x k) - f z ≤ inner ℝ (g k) (x k - z) := by
      rw [inner_sub_right] at hs' ⊢
      linarith
    have hg := norm_le_of_supportsAt hf (hs k)
    have hgsq : ‖g k‖ ^ 2 ≤ (G : ℝ) ^ 2 :=
      pow_le_pow_left₀ (norm_nonneg _) hg 2
    have hnorm : ‖x (k + 1) - z‖ ^ 2 =
        ‖x k - z‖ ^ 2 - 2 * a k * inner ℝ (g k) (x k - z) + (a k) ^ 2 * ‖g k‖ ^ 2 := by
      rw [hx k, sub_right_comm, norm_sub_sq_real, inner_smul_right,
        norm_smul, Real.norm_eq_abs, mul_pow, sq_abs, real_inner_comm (x k - z)]
      ring
    have hp := mul_le_mul_of_nonneg_left hpair (mul_nonneg (by norm_num : (0 : ℝ) ≤ 2) (ha k))
    have hn := mul_le_mul_of_nonneg_left hgsq (sq_nonneg (a k))
    nlinarith
  induction N with
  | zero => simp
  | succ N ih =>
      rw [Finset.sum_range_succ, Finset.sum_range_succ]
      nlinarith [hstep N]

/-- A positive finite run contains an iterate satisfying the normalized Optlib
subgradient bound, relative to any comparator (not necessarily a minimizer). -/
theorem exists_gap_le {f : E → ℝ} {G : ℝ≥0} {x g : ℕ → E} {a : ℕ → ℝ}
    (hf : LipschitzWith G f) (ha : ∀ k, 0 < a k)
    (hs : ∀ k, SupportsAt f (x k) (g k))
    (hx : ∀ k, x (k + 1) = x k - a k • g k) (z : E) {N : ℕ} (hN : 0 < N) :
    ∃ i < N, f (x i) - f z ≤
      (‖x 0 - z‖ ^ 2 + (G : ℝ) ^ 2 * (∑ k ∈ Finset.range N, (a k) ^ 2)) /
        (2 * ∑ k ∈ Finset.range N, a k) := by
  have hne : (Finset.range N).Nonempty := ⟨0, Finset.mem_range.mpr hN⟩
  obtain ⟨i, hi, hmin⟩ := Finset.exists_min_image (Finset.range N) (fun k => f (x k)) hne
  refine ⟨i, Finset.mem_range.mp hi, ?_⟩
  have hsumpos : 0 < ∑ k ∈ Finset.range N, a k :=
    Finset.sum_pos (fun k _ => ha k) hne
  have hlower : (∑ k ∈ Finset.range N, a k) * (f (x i) - f z) ≤
      ∑ k ∈ Finset.range N, a k * (f (x k) - f z) := by
    rw [Finset.sum_mul]
    exact Finset.sum_le_sum fun k hk =>
      mul_le_mul_of_nonneg_left (sub_le_sub_right (hmin k hk) _) (ha k).le
  have he := sum_weighted_gap_le hf (fun k => (ha k).le) hs hx z N
  apply (le_div_iff₀ (mul_pos (by norm_num : (0 : ℝ) < 2) hsumpos)).mpr
  nlinarith [sq_nonneg ‖x N - z‖]

end AutoSamplingTheory.TechnicalLemmas.Analysis.SubgradientMethod
