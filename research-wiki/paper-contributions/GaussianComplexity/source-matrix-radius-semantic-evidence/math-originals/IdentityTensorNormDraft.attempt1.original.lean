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

theorem identity_rankone_norm {m n : Type*} [Fintype m] [Fintype n]
    [DecidableEq m] [DecidableEq n] [Nonempty m] (v : n → ℝ) :
    ‖Matrix.kronecker (1 : Matrix m m ℝ) (Matrix.vecMulVec v v)‖ =
      ∑ j : n, (v j) ^ 2 := by
  classical
  let F : Matrix n n ℝ := Matrix.vecMulVec v v
  let K : Matrix (m × n) (m × n) ℝ := Matrix.kronecker (1 : Matrix m m ℝ) F
  let S : ℝ := ∑ j : n, (v j) ^ 2
  change ‖K‖ = S
  have hS : 0 ≤ S := Finset.sum_nonneg (fun _ _ => sq_nonneg _)
  have hF : F * F = S • F := by
    ext j k
    change (∑ a : n, (v j * v a) * (v a * v k)) =
      (∑ a : n, (v a) ^ 2) * (v j * v k)
    rw [Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro a _
    ring
  have hstar : K.conjTranspose = K := by
    dsimp only [K]
    rw [Matrix.conjTranspose_kronecker, Matrix.conjTranspose_one]
    simp [F]
  have hKsq : K * K = S • K := by
    dsimp only [K]
    rw [← Matrix.mul_kronecker_mul, Matrix.one_mul, hF, Matrix.kronecker_smul]
  have hn : S * ‖K‖ = ‖K‖ * ‖K‖ := by
    have h := Matrix.l2_opNorm_conjTranspose_mul_self K
    rw [hstar, hKsq, norm_smul, Real.norm_eq_abs, abs_of_nonneg hS] at h
    exact h
  by_cases hv : v = 0
  · simp [K, F, S, hv]
  · obtain ⟨j, hj⟩ : ∃ j : n, v j ≠ 0 := by
      by_contra! h
      exact hv (funext h)
    let i : m := Classical.choice inferInstance
    have hKne : K ≠ 0 := by
      intro hzero
      have hentry := congrArg
        (fun A : Matrix (m × n) (m × n) ℝ => A (i, j) (i, j)) hzero
      have hsq : v j * v j = 0 := by
        simpa [K, F, Matrix.kronecker, Matrix.vecMulVec] using hentry
      exact (mul_ne_zero hj hj) hsq
    have hnorm : ‖K‖ ≠ 0 := norm_ne_zero_iff.mpr hKne
    have hp : (‖K‖ - S) * ‖K‖ = 0 := by nlinarith [hn]
    rcases mul_eq_zero.mp hp with hs | hz
    · exact sub_eq_zero.mp hs
    · exact (hnorm hz).elim

end RadiusNormDraft
