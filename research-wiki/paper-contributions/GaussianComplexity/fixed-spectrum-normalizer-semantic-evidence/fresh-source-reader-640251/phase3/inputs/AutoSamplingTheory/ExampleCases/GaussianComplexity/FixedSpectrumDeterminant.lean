import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementJacobianEntropy
import Mathlib.LinearAlgebra.UnitaryGroup
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
open Matrix
open scoped BigOperators
set_option autoImplicit false
/-!
# Actual fixed-spectrum precision determinant

Zhou--Suzuki, arXiv:2610.20492v1 Eq11 and the determinant component of
Appendix C.4. The actual cosine-grid precision has the displayed diagonal
product as determinant, pointwise for every full real orthogonal O, either
determinant sign. Exactly source d>=2 and kappa>=2 are retained; these bounds
are not needed for this algebraic identity but feed the actual Gaussian
consumer through the existing source admissibility producer.

The existing public DisplacementJacobianEntropy.det_conjStarAlgAut_eq is the
canonical conjugation-invariance proof node and is reused literally here.
No duplicate generic invariant or determinant-one premise is introduced.
The focused Test consumes this exact determinant result, existing actual
admissibility and canonical GaussianPrecisionDensity in the same actual
inverse-precision law, exposing the spectrum-only density coefficient while
retaining the actual hidden orientation in the quadratic exponent.

Unweighted Gaussian-integral/known-Z statements, full C.4 calculus/minimizer,
moments/Krylov, true oracle/TV/precision/cost adapters and main bounds remain
separate. This pointwise identity is fixed-spectrum background, not a
determinant-sign lower-bound claim.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant
theorem actual_precision_det {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
    let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
    let diagonalValue : Fin d → ℝ := fun i =>
      (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
    let A : Matrix (Fin d) (Fin d) ℝ :=
      (O : Matrix (Fin d) (Fin d) ℝ) * Matrix.diagonal diagonalValue *
        (O : Matrix (Fin d) (Fin d) ℝ).transpose
    A.det = ∏ i : Fin d, diagonalValue i := by
  classical
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let diagonalValue : Fin d → ℝ := fun i =>
    (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let M : Matrix (Fin d) (Fin d) ℝ := O
  change (M * Matrix.diagonal diagonalValue * M.transpose).det =
    ∏ i : Fin d, diagonalValue i
  have hdet :=
    AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementJacobianEntropy.det_conjStarAlgAut_eq
      (O : unitary (Matrix (Fin d) (Fin d) ℝ)) (Matrix.diagonal diagonalValue)
  rw [Unitary.conjStarAlgAut_apply] at hdet
  change (M * Matrix.diagonal diagonalValue * star M).det =
    (Matrix.diagonal diagonalValue).det at hdet
  have hstar : star M = M.transpose := by
    ext i j
    simp
  rw [hstar, Matrix.det_diagonal] at hdet
  exact hdet
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumDeterminant
