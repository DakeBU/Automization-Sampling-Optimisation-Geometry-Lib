import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementJacobianEntropy
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Tactic

/-!
# Spectral assembly for the displacement Jacobian

Chewi's entropy half of Theorem 1.4.5 uses the literal Jacobian

`(1 - t) I + t ∇T`

and the convexity of `- log det`.  `DisplacementJacobianEntropy` already proves
all of the local ingredients needed for a positive-definite matrix: the scalar
log inequality on each positive eigenvalue, determinant invariance under
unitary star-conjugation, and the determinant of the affine segment against a
diagonal matrix.

This module closes the finite-dimensional spectral bookkeeping gap.  It uses
Mathlib's Hermitian spectral theorem to identify the determinant of the literal
affine matrix with the product of the affine eigenvalues, then rewrites the
existing spectrum-level inequality as an inequality for the actual matrix
`det`.

Truth boundary: this is still not the full entropy displacement-convexity
argument in Chewi Theorem 1.4.5.  A Brenier Jacobian is only positive
semidefinite a.e. in general, and the density change-of-variables / endpoint
limit needed for that source theorem remain separate analytic Frontier Cells.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace DisplacementJacobianSpectral

open Real
open scoped BigOperators

noncomputable section

open DisplacementJacobianEntropy

/-- Hermitian spectral diagonalization turns the determinant of the literal
affine matrix `(1-t) I + t A` into the product of the affine eigenvalues.

No positivity hypothesis is needed for this algebraic identity. -/
theorem det_affineIdentity_eq_prod_eigenvalues
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (t : ℝ) :
    Matrix.det ((1 - t) • (1 : Matrix ι ι ℝ) + t • A) =
      ∏ i, ((1 - t) + t * hA.eigenvalues i) := by
  have hspectral :
      A = Unitary.conjStarAlgAut ℝ (Matrix ι ι ℝ) hA.eigenvectorUnitary
        (Matrix.diagonal hA.eigenvalues) := by
    simpa using hA.spectral_theorem
  have haffine0 := congrArg
    (fun B : Matrix ι ι ℝ =>
      (1 - t) • (1 : Matrix ι ι ℝ) + t • B)
    hspectral
  have hmap :
      (1 - t) • (1 : Matrix ι ι ℝ) +
          t • Unitary.conjStarAlgAut ℝ (Matrix ι ι ℝ) hA.eigenvectorUnitary
            (Matrix.diagonal hA.eigenvalues) =
        Unitary.conjStarAlgAut ℝ (Matrix ι ι ℝ) hA.eigenvectorUnitary
          ((1 - t) • (1 : Matrix ι ι ℝ) +
            t • Matrix.diagonal hA.eigenvalues) := by
    rw [map_add, map_smul, map_smul, map_one]
  have haffine :
      (1 - t) • (1 : Matrix ι ι ℝ) + t • A =
        Unitary.conjStarAlgAut ℝ (Matrix ι ι ℝ) hA.eigenvectorUnitary
          ((1 - t) • (1 : Matrix ι ι ℝ) +
            t • Matrix.diagonal hA.eigenvalues) :=
    haffine0.trans hmap
  calc
    Matrix.det ((1 - t) • (1 : Matrix ι ι ℝ) + t • A) =
        Matrix.det
          (Unitary.conjStarAlgAut ℝ (Matrix ι ι ℝ) hA.eigenvectorUnitary
            ((1 - t) • (1 : Matrix ι ι ℝ) +
              t • Matrix.diagonal hA.eigenvalues)) :=
      congrArg Matrix.det haffine
    _ = Matrix.det
        ((1 - t) • (1 : Matrix ι ι ℝ) +
          t • Matrix.diagonal hA.eigenvalues) :=
      det_conjStarAlgAut_eq hA.eigenvectorUnitary _
    _ = ∏ i, ((1 - t) + t * hA.eigenvalues i) :=
      det_affineIdentity_diagonal hA.eigenvalues t

/-- For a positive-definite matrix, the spectrum-level affine log determinant
is exactly the logarithm of the literal affine matrix determinant. -/
theorem spectrumLogDet_affineIdentity_eigenvalues_eq_log_det
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.PosDef) (t : ℝ)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    spectrumLogDet
        (affineIdentitySpectrum t hA.isHermitian.eigenvalues) =
      Real.log
        (Matrix.det ((1 - t) • (1 : Matrix ι ι ℝ) + t • A)) := by
  unfold spectrumLogDet
  rw [det_affineIdentity_eq_prod_eigenvalues A hA.isHermitian t]
  exact
    (Real.log_prod
      (fun i _ =>
        (affineIdentityEigenvalue_pos
          (hA.eigenvalues_pos i) ht0 ht1).ne')).symm

/-- Literal matrix form of the log-determinant concavity along the segment from
`I` to a positive-definite matrix `A`:

` t log det A ≤ log det ((1-t)I+tA) `.

This is the matrix statement used by the smooth positive-definite branch of
the entropy calculation. -/
theorem log_det_affineIdentity_ge
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.PosDef) (t : ℝ)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    t * Real.log A.det ≤
      Real.log (Matrix.det ((1 - t) • (1 : Matrix ι ι ℝ) + t • A)) := by
  have h :=
    spectrumLogDet_affineIdentity_ge
      hA.isHermitian.eigenvalues t
      (fun i => hA.eigenvalues_pos i) ht0 ht1
  rw [spectrumLogDet_eigenvalues_eq_log_det A hA] at h
  rw [spectrumLogDet_affineIdentity_eigenvalues_eq_log_det A hA t ht0 ht1] at h
  exact h

/-- Equivalent entropy-sign orientation of `log_det_affineIdentity_ge`. -/
theorem neg_log_det_affineIdentity_le
    {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.PosDef) (t : ℝ)
    (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    -Real.log (Matrix.det ((1 - t) • (1 : Matrix ι ι ℝ) + t • A)) ≤
      t * (-Real.log A.det) := by
  have h := neg_le_neg (log_det_affineIdentity_ge A hA t ht0 ht1)
  simpa [mul_neg] using h

end

end DisplacementJacobianSpectral
end Measure
end TechnicalLemmas
end AutoSamplingTheory
