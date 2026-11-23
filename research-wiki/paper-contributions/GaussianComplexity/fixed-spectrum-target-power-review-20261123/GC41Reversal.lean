import GC41Target
import Mathlib.LinearAlgebra.Matrix.Permutation
import Mathlib.Data.Fin.Rev
import Mathlib.Tactic

/-! # Opposite tests for two rotations of the known cosine grid

Reversing the order of the disclosed spectrum preserves its multiset and
negates the cosine detector at every odd frequency. With a nonnegative
threshold the two strict detector events are disjoint.
-/

open Matrix

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

/-- The orthogonal permutation reversing the order of the eigenvectors. -/
def reversal (d : ℕ) : Matrix.orthogonalGroup (Fin d) ℝ :=
  ⟨Fin.revPerm.permMatrix ℝ, (Matrix.mem_orthogonalGroup_iff (Fin d) ℝ).mpr (by
    rw [Matrix.transpose_permMatrix, ← Matrix.permMatrix_mul]
    simp)⟩

private theorem reverse_cosine {d n : ℕ} (hn : Odd n) (i : Fin d) :
    Real.cos ((n : ℝ) * (((i.rev.val : ℝ) + 1/2) * Real.pi / (d : ℝ))) =
      -Real.cos ((n : ℝ) * (((i.val : ℝ) + 1/2) * Real.pi / (d : ℝ))) := by
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by have := i.isLt; omega)
  have hi : i.rev.val + i.val + 1 = d := by dsimp [Fin.rev]; omega
  have hi' : (i.rev.val : ℝ) + (i.val : ℝ) + 1 = (d : ℝ) := by exact_mod_cast hi
  rw [show (n : ℝ) * (((i.rev.val : ℝ) + 1/2) * Real.pi / (d : ℝ)) =
    (n : ℝ) * Real.pi - (n : ℝ) * (((i.val : ℝ) + 1/2) * Real.pi / (d : ℝ)) by
      rw [show (i.rev.val : ℝ) = d - (i.val : ℝ) - 1 by linarith]; field_simp; ring]
  rw [Real.cos_nat_mul_pi_sub, hn.neg_one_pow]; ring

/-- Odd cosine modes change sign under reversal of the Chebyshev grid. -/
theorem reversal_conjugates_odd_cosine {d n : ℕ} (hn : Odd n) :
    let D : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal (fun i : Fin d =>
      Real.cos ((n : ℝ) * (((i.val : ℝ) + 1/2) * Real.pi / (d : ℝ))))
    (reversal d : Matrix (Fin d) (Fin d) ℝ) * D *
      (reversal d : Matrix (Fin d) (Fin d) ℝ).transpose = -D := by
  dsimp only [reversal]
  rw [Matrix.transpose_permMatrix, PEquiv.toMatrix_toPEquiv_mul, PEquiv.mul_toMatrix_toPEquiv]
  ext i j
  by_cases h : i = j
  · subst j
    simpa only [Matrix.submatrix_apply, Equiv.Perm.inv_def, Equiv.symm_symm, Fin.revPerm_apply,
      id_eq, Matrix.neg_apply, Matrix.diagonal_apply_eq] using reverse_cosine hn i
  · simp [Matrix.submatrix_apply, Equiv.Perm.inv_def, h]

/-- At every odd mode an arbitrary sample can pass at most one of the two strict tests. -/
theorem disjoint_reversed_odd_detector_events {d n : ℕ} {κ τ : ℝ}
    (hd : 2 ≤ d) (hκ : 2 ≤ κ) (hn : Odd n) (hτ : 0 ≤ τ) :
    Disjoint (detectorEvent κ n τ (hiddenPrecision κ (1 : Matrix.orthogonalGroup (Fin d) ℝ)))
      (detectorEvent κ n τ (hiddenPrecision κ (reversal d))) := by
  let D : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal (fun i => Real.cos ((n : ℝ) * gridAngle d i))
  let T (A : Matrix (Fin d) (Fin d) ℝ) := Polynomial.aeval
    ((κ-1)⁻¹ • ((2 : ℝ) • A - (κ+1) • (1 : Matrix (Fin d) (Fin d) ℝ)))
    (Polynomial.Chebyshev.T ℝ (n : ℤ))
  have eval (O : Matrix.orthogonalGroup (Fin d) ℝ) :
      T (hiddenPrecision κ O) = O.val * D * O.val.transpose :=
    FixedSpectrumDetector.actual_chebyshev_matrix_cosine hd hκ O n
  have eid : T (hiddenPrecision κ (1 : Matrix.orthogonalGroup (Fin d) ℝ)) = D := by
    simpa using eval 1
  have erev : T (hiddenPrecision κ (reversal d)) = -D :=
    (eval (reversal d)).trans (reversal_conjugates_odd_cosine hn)
  apply Set.disjoint_left.mpr
  intro x h₁ h₂
  change 0 < (-1 : ℝ)^n * (WithLp.ofLp x ⬝ᵥ (T _ *ᵥ WithLp.ofLp x)) - 2*τ*‖x‖^2 at h₁ h₂
  rw [eid] at h₁
  rw [erev, Matrix.neg_mulVec, dotProduct_neg] at h₂
  linarith [mul_nonneg hτ (sq_nonneg ‖x‖)]

/-- For a zero-query test the source uses the first cosine mode. -/
theorem disjoint_reversed_detector_events {d : ℕ} {κ τ : ℝ}
    (hd : 2 ≤ d) (hκ : 2 ≤ κ) (hτ : 0 ≤ τ) :
    Disjoint (detectorEvent κ 1 τ (hiddenPrecision κ (1 : Matrix.orthogonalGroup (Fin d) ℝ)))
      (detectorEvent κ 1 τ (hiddenPrecision κ (reversal d))) :=
  disjoint_reversed_odd_detector_events hd hκ (by decide) hτ

#print axioms disjoint_reversed_detector_events

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
