import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.LinearMap

noncomputable section
open scoped BigOperators Matrix.Norms.L2Operator
set_option autoImplicit false

namespace RadiusNormDraft

theorem matrix_outer_norm {n : Type*} [Fintype n] [DecidableEq n]
    (u : EuclideanSpace ℝ n) :
    ‖Matrix.vecMulVec u.ofLp u.ofLp‖ = ‖u‖ ^ 2 := by
  have he : Matrix.toEuclideanLin.symm
      (InnerProductSpace.rankOne ℝ u u : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n) =
      Matrix.vecMulVec u.ofLp u.ofLp := by
    simpa only [star_trivial] using InnerProductSpace.symm_toEuclideanLin_rankOne u u
  have hl : Matrix.toEuclideanLin (Matrix.vecMulVec u.ofLp u.ofLp) =
      (InnerProductSpace.rankOne ℝ u u : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n) := by
    rw [← he, LinearEquiv.apply_symm_apply]
  have hc : Matrix.toEuclideanCLM (n := n) (𝕜 := ℝ) (Matrix.vecMulVec u.ofLp u.ofLp) =
      InnerProductSpace.rankOne ℝ u u := by
    apply ContinuousLinearMap.ext
    intro x
    exact congrArg (fun f : EuclideanSpace ℝ n →ₗ[ℝ] EuclideanSpace ℝ n => f x) hl
  rw [Matrix.cstar_norm_def, hc, InnerProductSpace.norm_rankOne, ← pow_two]

theorem rankone_tensor_norm {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n]
    (u : EuclideanSpace ℝ m) (v : EuclideanSpace ℝ n) :
    ‖Matrix.kronecker (Matrix.vecMulVec u.ofLp u.ofLp)
        (Matrix.vecMulVec v.ofLp v.ofLp)‖ = ‖u‖ ^ 2 * ‖v‖ ^ 2 := by
  let z : EuclideanSpace ℝ (m × n) := WithLp.toLp 2 (fun ij => u ij.1 * v ij.2)
  have hz : Matrix.kronecker (Matrix.vecMulVec u.ofLp u.ofLp)
      (Matrix.vecMulVec v.ofLp v.ofLp) = Matrix.vecMulVec z.ofLp z.ofLp := by
    ext i j
    dsimp [Matrix.kronecker, Matrix.kroneckerMap, Matrix.vecMulVec, z]
    ring
  rw [hz, matrix_outer_norm, EuclideanSpace.norm_sq_eq, EuclideanSpace.norm_sq_eq,
    EuclideanSpace.norm_sq_eq, Fintype.sum_prod_type]
  simp only [z, Real.norm_eq_abs, sq_abs, mul_pow]
  rw [Finset.sum_mul_sum]

end RadiusNormDraft
