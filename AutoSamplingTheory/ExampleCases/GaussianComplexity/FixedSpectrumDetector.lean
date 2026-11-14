import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.Star.UnitaryStarAlgAut
import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Chebyshev.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

open Matrix
set_option autoImplicit false

/-!
# Actual fixed-spectrum matrix-Chebyshev detector

Zhou--Suzuki arXiv:2610.20492v1, Eq11 and Section4.3.
The actual affine normalized precision has the exact first-kind Chebyshev
matrix polynomial given by the same orthogonal conjugate cosine diagonal.
This auxiliary identity holds for all natural frequencies; the source uses
n=2q+1. No Gaussian law, probability, algorithm or query bound is asserted.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector

theorem actual_chebyshev_matrix_cosine {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (n : ℕ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ)) =
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => Real.cos ((n : ℝ) * θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let Λ : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i))
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) * Λ *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let D : Matrix (Fin d) (Fin d) ℝ :=
    Matrix.diagonal (fun i => Real.cos (θ i))
  let B : Matrix (Fin d) (Fin d) ℝ :=
    (κ - 1)⁻¹ • ((2 : ℝ) • A - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))
  let Φ : Matrix (Fin d) (Fin d) ℝ ≃ₐ[ℝ] Matrix (Fin d) (Fin d) ℝ :=
    (Unitary.conjStarAlgAut ℝ (Matrix (Fin d) (Fin d) ℝ) O).toAlgEquiv
  have hΦ (M : Matrix (Fin d) (Fin d) ℝ) :
      Φ M = (O : Matrix (Fin d) (Fin d) ℝ) * M *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose := by
    change (O : Matrix (Fin d) (Fin d) ℝ) * M *
      star (O : Matrix (Fin d) (Fin d) ℝ) = _
    simp only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
  have hnz : κ - 1 ≠ 0 := by linarith
  have hD :
      (κ - 1)⁻¹ • ((2 : ℝ) • Λ - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ)) = D := by
    ext i j
    by_cases hij : i = j
    · subst j
      simp only [Matrix.smul_apply, smul_eq_mul, Matrix.sub_apply, Λ, D,
        Matrix.diagonal_apply_eq, Matrix.one_apply_eq, mul_one]
      field_simp [hnz]
      ring
    · simp [Λ, D, hij]
  have hA : A = Φ Λ := (hΦ Λ).symm
  have hB : B = Φ D := by
    dsimp only [B]
    rw [hA]
    calc
      (κ - 1)⁻¹ • ((2 : ℝ) • Φ Λ - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ)) =
          Φ ((κ - 1)⁻¹ • ((2 : ℝ) • Λ - (κ + 1) • (1 : Matrix (Fin d) (Fin d) ℝ))) := by
        simp only [map_smul, map_sub, map_one]
      _ = Φ D := congrArg Φ hD
  have hdiag : Polynomial.aeval D (Polynomial.Chebyshev.T ℝ (n : ℤ)) =
      Matrix.diagonal (fun i => Real.cos ((n : ℝ) * θ i)) := by
    change Polynomial.aeval ((Matrix.diagonalAlgHom (n := Fin d) (α := ℝ) ℝ) (fun i => Real.cos (θ i)))
      (Polynomial.Chebyshev.T ℝ (n : ℤ)) = _
    rw [Polynomial.aeval_algHom_apply, Polynomial.aeval_pi_apply]
    change Matrix.diagonal (fun i => Polynomial.aeval (Real.cos (θ i))
      (Polynomial.Chebyshev.T ℝ (n : ℤ))) = _
    apply congrArg (Matrix.diagonal : (Fin d → ℝ) → Matrix (Fin d) (Fin d) ℝ)
    funext i
    change (Polynomial.Chebyshev.T ℝ (n : ℤ)).eval (Real.cos (θ i)) = _
    simpa only [Int.cast_natCast] using Polynomial.Chebyshev.T_real_cos (θ i) (n : ℤ)
  change Polynomial.aeval B (Polynomial.Chebyshev.T ℝ (n : ℤ)) = _
  rw [hB, Polynomial.aeval_algHom_apply, hdiag, hΦ]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDetector
