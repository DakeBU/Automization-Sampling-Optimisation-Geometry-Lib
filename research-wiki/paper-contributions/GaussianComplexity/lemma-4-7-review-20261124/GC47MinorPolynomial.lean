import GC47Witness
import Mathlib.Algebra.MvPolynomial.Eval

/-! Express the selected maximal Krylov minor as a polynomial in the starts' real coordinates. -/
noncomputable section
open Matrix MvPolynomial
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

def minorPolynomial {d : ℕ} (q : ℕ) (node : Fin d → ℝ) : MvPolynomial (Fin d × Fin (q+1)) ℝ :=
  Matrix.det (Matrix.of (fun i j : Fin (minorSize d q) =>
    C (node (minorRow d q i) ^ (minorColumn d q j).2.val) *
      X (minorRow d q i, (minorColumn d q j).1)))

theorem eval_minorPolynomial {d q : ℕ} (node : Fin d → ℝ) (g : Starts d q) :
    MvPolynomial.eval (fun ia : Fin d × Fin (q+1) => g ia.2 ia.1) (minorPolynomial q node) =
      minorDet node g := by
  unfold minorPolynomial minorDet
  rw [RingHom.map_det]
  congr 1
  ext i j
  simp [monomialMatrix, RingHom.mapMatrix_apply, Matrix.submatrix]

theorem minorPolynomial_ne_zero {d : ℕ} (q : ℕ) (node : Fin d → ℝ)
    (hn : Function.Injective node) : minorPolynomial q node ≠ 0 := by
  intro he
  have h := eval_minorPolynomial node (monomialWitness q node)
  rw [he, map_zero] at h
  exact witness_minor_ne_zero (q := q) node hn h.symm

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
