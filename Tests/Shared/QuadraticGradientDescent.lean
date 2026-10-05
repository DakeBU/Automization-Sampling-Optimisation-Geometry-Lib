import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent
import Mathlib.Analysis.Matrix.Hermitian

open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent
open scoped RealInnerProductSpace

-- A genuine positive-definite diagonal matrix with distinct endpoint modes 1 and 3.
private noncomputable def diagonalH : EuclideanSpace ℝ (Fin 2) →L[ℝ] EuclideanSpace ℝ (Fin 2) :=
  (Matrix.toEuclideanLin (Matrix.diagonal ![(1 : ℝ), 3])).toContinuousLinearMap

private theorem diagonalH_symmetric : diagonalH.IsSymmetric := by
  exact Matrix.isSymmetric_toEuclideanLin_iff.mpr (Matrix.isHermitian_diagonal _)

private theorem diagonalH_mode (i : Fin 2) :
    diagonalH (EuclideanSpace.basisFun (Fin 2) ℝ i) =
      ![(1 : ℝ), 3] i • EuclideanSpace.basisFun (Fin 2) ℝ i := by
  ext j
  simp [diagonalH, Matrix.toLpLin_apply, EuclideanSpace.basisFun_apply]

-- Balanced step h=1/2, kappa=3: both endpoints attain the factor q^N=(1/2)^N.
-- The high mode changes sign, so absolute values in the general formula matter.
example (N : ℕ) (i : Fin 2) :
    let f := fun z : EuclideanSpace ℝ (Fin 2) => inner ℝ z (diagonalH z) / 2
    ‖(fun z => z - (1/2 : ℝ) • gradient f z)^[N]
      (EuclideanSpace.basisFun (Fin 2) ℝ i)‖ = (1/2 : ℝ)^N := by
  have hr := (quadratic_eigenmode diagonalH diagonalH_symmetric (diagonalH_mode i)
    (1/2 : ℝ) N).2.1
  fin_cases i <;> norm_num at hr ⊢ <;> simpa using hr

-- The same positive quadratic at h=3 grows like 2^N: the identities do not
-- smuggle in stability. Check exact value as well as norm and retain N=0.
example (x : ℝ) (N : ℕ) :
    let f := fun z : ℝ => inner ℝ z z / 2
    ‖(fun z => z - (3 : ℝ) • gradient f z)^[N] x‖ = (2 : ℝ)^N * ‖x‖ ∧
      f ((fun z => z - (3 : ℝ) • gradient f z)^[N] x) = (4 : ℝ)^N * f x := by
  have hr := quadratic_eigenmode (1 : ℝ →L[ℝ] ℝ) (by intro a b; rfl)
    (μ := 1) (x := x) (by simp) 3 N
  have hp : (-2 : ℝ)^(2*N) = (4 : ℝ)^N := by rw [pow_mul]; norm_num
  norm_num [hp] at hr ⊢
  exact ⟨hr.2.1, hr.2.2⟩

-- Operator powers at N=0 and the zero operator for arbitrary steps are retained.
example (h : ℝ) (N : ℕ) (x : ℝ) :
    (fun z => z - h • gradient (fun z : ℝ => inner ℝ z (0 : ℝ) / 2) z)^[N] x = x := by
  simpa using quadratic_gradient_iterate (0 : ℝ →L[ℝ] ℝ) (by intro a b; simp) h N x

#print axioms quadratic_gradient_iterate
#print axioms quadratic_eigenmode
