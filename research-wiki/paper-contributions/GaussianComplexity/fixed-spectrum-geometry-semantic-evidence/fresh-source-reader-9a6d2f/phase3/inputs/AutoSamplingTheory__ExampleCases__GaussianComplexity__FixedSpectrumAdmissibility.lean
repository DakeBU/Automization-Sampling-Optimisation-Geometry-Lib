import Mathlib.Algebra.Order.Star.Real
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Linarith
open Matrix
set_option autoImplicit false
/-!
# Actual cosine-grid precision admissibility

Zhou--Suzuki, arXiv:2610.20492v1, Eq11 and Lemma4.6. The literal
cosine-grid precision is used for every full real orthogonal O, with exactly
source d>=2 and kappa>=2. The two matrix differences are positive semidefinite
in quadratic-form order, and positive definiteness is produced internally.
The source dimension binder is deliberately retained even though the scalar
cosine envelope and matrix bound proof work for every choice of angles.

The actual inverse-precision Gaussian law-density consumer is in the focused
Test and reuses the existing canonical GaussianPrecisionDensity leaf. No
calculus, known-normalizer product, moment/Krylov, algorithm/TV/cost transport
or main-lower-bound completion is asserted by this pointwise matrix result.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
theorem actual_precision_admissible {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    A.PosDef ∧ (A - 1).PosSemidef ∧
      (κ • (1 : Matrix (Fin d) (Fin d) ℝ) - A).PosSemidef := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let U : Matrix (Fin d) (Fin d) ℝ := O
  let L : Matrix (Fin d) (Fin d) ℝ := Matrix.diagonal diagonalValue
  let A : Matrix (Fin d) (Fin d) ℝ := U * L * U.transpose
  change A.PosDef ∧ (A - 1).PosSemidef ∧
    (κ • (1 : Matrix (Fin d) (Fin d) ℝ) - A).PosSemidef
  have hcoef : 0 ≤ (κ - 1) / 2 := by linarith
  have hvalue (i : Fin d) : 1 ≤ diagonalValue i ∧ diagonalValue i ≤ κ := by
    have hlo := mul_le_mul_of_nonneg_left (Real.neg_one_le_cos (θ i)) hcoef
    have hhi := mul_le_mul_of_nonneg_left (Real.cos_le_one (θ i)) hcoef
    dsimp only [diagonalValue]
    constructor <;> nlinarith
  have hO : U * U.transpose = 1 := by
    simpa only [U] using
      (Matrix.mem_orthogonalGroup_iff (n := Fin d) (R := ℝ)).mp O.property
  have hstar : U.conjTranspose = U.transpose := by
    ext i j
    simp
  have hdiaglo : Matrix.diagonal (fun i => diagonalValue i - 1) = L - 1 := by
    ext i j
    by_cases hij : i = j <;> simp [L, hij]
  have hdiaghi : Matrix.diagonal (fun i => κ - diagonalValue i) = κ • 1 - L := by
    ext i j
    by_cases hij : i = j <;>
      simp [L, hij, smul_eq_mul]
  have hlow : (Matrix.diagonal (fun i => diagonalValue i - 1)).PosSemidef :=
    Matrix.PosSemidef.diagonal (fun i => sub_nonneg.mpr (hvalue i).1)
  have hhigh : (Matrix.diagonal (fun i => κ - diagonalValue i)).PosSemidef :=
    Matrix.PosSemidef.diagonal (fun i => sub_nonneg.mpr (hvalue i).2)
  have hloweq : U * Matrix.diagonal (fun i => diagonalValue i - 1) * U.transpose =
      A - 1 := by
    dsimp only [A]
    rw [hdiaglo, Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_one, hO]
  have hhigheq : U * Matrix.diagonal (fun i => κ - diagonalValue i) * U.transpose =
      κ • 1 - A := by
    dsimp only [A]
    rw [hdiaghi, Matrix.mul_sub, Matrix.sub_mul, Matrix.mul_smul,
      Matrix.mul_one, Matrix.smul_mul, hO]
  have hAlo : (A - 1).PosSemidef := by
    rw [← hloweq]
    simpa only [hstar] using hlow.mul_mul_conjTranspose_same U
  have hAhi : (κ • (1 : Matrix (Fin d) (Fin d) ℝ) - A).PosSemidef := by
    rw [← hhigheq]
    simpa only [hstar] using hhigh.mul_mul_conjTranspose_same U
  have hpos := Matrix.PosDef.posSemidef_add hAlo
    (Matrix.PosDef.one : (1 : Matrix (Fin d) (Fin d) ℝ).PosDef)
  exact ⟨by simpa only [sub_add_cancel] using hpos, hAlo, hAhi⟩
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility
