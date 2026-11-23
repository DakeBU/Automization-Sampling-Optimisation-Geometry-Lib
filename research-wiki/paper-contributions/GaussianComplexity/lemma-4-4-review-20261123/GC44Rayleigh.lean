import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.InnerProductSpace.Rayleigh
import Mathlib.Tactic

noncomputable section
open Matrix
open scoped Matrix.Norms.L2Operator RealInnerProductSpace
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection

/-- A bound on all real quadratic forms controls the Euclidean operator norm. -/
theorem opNorm_le_of_form {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) {t : ℝ} (ht : 0 ≤ t)
    (hb : ∀ v : ι → ℝ, |v ⬝ᵥ (A *ᵥ v)| ≤ t * ‖WithLp.toLp 2 v‖^2) : ‖A‖ ≤ t := by
  let T := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := ι) A
  have hT : T.IsSymmetric := ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp
    ((show IsSelfAdjoint A from hA).map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := ι)))
  change ‖T‖ ≤ t
  rw [T.norm_eq_iSup_rayleighQuotient hT]
  apply ciSup_le
  intro x
  by_cases hx : x = 0
  · simpa [hx] using ht
  · rw [ContinuousLinearMap.rayleighQuotient, abs_div, abs_sq]
    apply (div_le_iff₀ (sq_pos_of_pos (norm_pos_iff.mpr hx))).mpr
    change abs (inner ℝ (T x) x) ≤ _
    rw [real_inner_comm]
    change |inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := ι) A x)| ≤ _
    rw [Matrix.inner_toEuclideanCLM]
    exact hb (WithLp.ofLp x)

end AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
