import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Data.Matrix.Diagonal
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
open Matrix
/-!
# Actual same-rotation fixed-spectrum precision replies

Zhou--Suzuki arXiv:2610.20492v1, Section4.1 Equation11 and Remark4.2.
The two precision matrices use the literal cosine grid and the SAME hidden
orthogonal rotation. One exact precision-matvec reply reconstructs the other
at the same actual point in either direction. The number2 here is the
reference condition number, not a call count or inverse-covariance oracle.
All scalar/diagonal/orthogonal/conjugation/matvec and nonzero-reciprocal bridges
are proved internally. No supplied affine identity or reply-correctness premise.
Gaussian target/covariance/TV transport, operational adaptive/cost/precision
adapters, spectral/PosDef/normalizer background and both main lower bounds
remain separate.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine
set_option autoImplicit false
theorem actual_affine_precision_query {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let A : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
      (O : Matrix (Fin d) (Fin d) ℝ) *
        Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    let query : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
      fun η x => WithLp.toLp 2 (A η *ᵥ WithLp.ofLp x)
    ∀ x : EuclideanSpace ℝ (Fin d),
      query κ x = (κ - 1) • query 2 x - (κ - 2) • x ∧
      query 2 x = (κ - 1)⁻¹ • (query κ x + (κ - 2) • x) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : ℝ → Matrix (Fin d) (Fin d) ℝ := fun η =>
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (η + 1) / 2 + (η - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let query : ℝ → EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun η x => WithLp.toLp 2 (A η *ᵥ WithLp.ofLp x)
  -- Align the zero-based indices with the literal one-based source grid.
  have hdpos : (0 : ℝ) < (d : ℝ) := by
    exact_mod_cast (lt_of_lt_of_le (by decide : (0 : ℕ) < 2) hd)
  have hd0 : (d : ℝ) ≠ 0 := ne_of_gt hdpos
  have hindex (i : Fin d) : θ i =
      (((i.val : ℝ) + 1 - 1 / 2) * Real.pi) / (d : ℝ) := by
    dsimp only [θ]
    field_simp [hd0]; ring
  -- Lift the actual entrywise identity through the diagonal and same O.
  have hscalar (i : Fin d) :
      (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i) =
      (κ - 1) * ((2 + 1) / 2 + (2 - 1) / 2 * Real.cos (θ i)) - (κ - 2) := by
    simp only [hindex i]
    ring
  have hdiag :
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) =
      (κ - 1) • Matrix.diagonal (fun i => (2 + 1) / 2 + (2 - 1) / 2 * Real.cos (θ i)) -
        (κ - 2) • (1 : Matrix (Fin d) (Fin d) ℝ) := by
    ext i j
    by_cases hij : i = j
    · subst j
      simpa [Matrix.diagonal_apply, Matrix.one_apply] using hscalar i
    · simp [hij]
  -- Full orthogonal membership supplies the actual right identity.
  have hO : (O : Matrix (Fin d) (Fin d) ℝ) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose = 1 :=
    (Matrix.mem_orthogonalGroup_iff (n := Fin d) (R := ℝ)).mp O.property
  have hmatrix : A κ = (κ - 1) • A 2 - (κ - 2) • 1 := by
    dsimp only [A]
    rw [hdiag, Matrix.mul_sub, Matrix.sub_mul]
    simp only [Matrix.mul_smul, Matrix.smul_mul, Matrix.mul_one, hO]
  -- Reverse conversion uses a genuinely nonzero known scalar.
  have hnz : κ - 1 ≠ 0 := by linarith
  intro x
  have hforward : query κ x = (κ - 1) • query 2 x - (κ - 2) • x := by
    apply WithLp.ofLp_injective 2
    change A κ *ᵥ WithLp.ofLp x =
      (κ - 1) • (A 2 *ᵥ WithLp.ofLp x) - (κ - 2) • WithLp.ofLp x
    rw [hmatrix]
    simp only [Matrix.sub_mulVec, Matrix.smul_mulVec, Matrix.one_mulVec]
  refine ⟨hforward, ?_⟩
  change query 2 x = (κ - 1)⁻¹ • (query κ x + (κ - 2) • x)
  rw [hforward, sub_add_cancel, smul_smul, inv_mul_cancel₀ hnz, one_smul]
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine
