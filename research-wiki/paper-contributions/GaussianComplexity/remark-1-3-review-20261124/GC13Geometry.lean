import GC33Target

/-! Quadratic members of the potential class in Remark 1.3. -/
noncomputable section
open Matrix InnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

variable {d : ℕ} {κ : ℝ} {A : Precision d}

def quadraticPotential (A : Precision d) (x : E d) : ℝ :=
  inner ℝ x (Matrix.toEuclideanCLM (𝕜 := ℝ) A x) / 2

theorem quadraticPotential_eq_dot (A : Precision d) (x : E d) :
    quadraticPotential A x = WithLp.ofLp x ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2 := by
  rw [quadraticPotential, Matrix.inner_toEuclideanCLM]

theorem quadratic_contDiff (A : Precision d) : ContDiff ℝ 2 (quadraticPotential A) := by
  exact (contDiff_id.inner ℝ (Matrix.toEuclideanCLM (𝕜 := ℝ) A).contDiff).div_const 2

theorem quadratic_hasGradientAt (hA : A.IsHermitian) (x : E d) :
    HasGradientAt (quadraticPotential A) (Matrix.toEuclideanCLM (𝕜 := ℝ) A x) x := by
  let L := Matrix.toEuclideanCLM (𝕜 := ℝ) A
  have hs : L.IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp
      ((show IsSelfAdjoint A from hA).map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)))
  have hraw := ((hasFDerivAt_id x).inner ℝ L.hasFDerivAt).const_mul (1 / 2 : ℝ)
  have hlin : (1 / 2 : ℝ) •
      ((fderivInnerCLM ℝ (x, L x)).comp ((ContinuousLinearMap.id ℝ (E d)).prod L)) =
      toDual ℝ (E d) (L x) := by
    ext v
    change (1 / 2 : ℝ) * (inner ℝ x (L v) + inner ℝ v (L x)) = inner ℝ (L x) v
    rw [← hs.apply_clm x v, (real_inner_comm v (L x)).symm]
    ring
  apply hasGradientAt_iff_hasFDerivAt.mpr
  convert hraw using 1 <;> first | rfl | exact hlin.symm | (ext v; simp only [quadraticPotential, id_eq]; ring)

theorem quadratic_gradient (hA : A.IsHermitian) (x : E d) :
    gradient (quadraticPotential A) x = Matrix.toEuclideanCLM (𝕜 := ℝ) A x :=
  (quadratic_hasGradientAt hA x).gradient

theorem quadratic_hessian (hA : A.IsHermitian) (x : E d) :
    fderiv ℝ (gradient (quadraticPotential A)) x = Matrix.toEuclideanCLM (𝕜 := ℝ) A := by
  rw [funext (quadratic_gradient hA)]
  exact (Matrix.toEuclideanCLM (𝕜 := ℝ) A).fderiv

private theorem dot_self_eq_norm_sq (v : E d) : WithLp.ofLp v ⬝ᵥ WithLp.ofLp v = ‖v‖^2 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  simp [dotProduct, pow_two]

theorem quadratic_hessian_bounds (hA : Admissible κ A) (x v : E d) :
    ‖v‖^2 ≤ inner ℝ v (fderiv ℝ (gradient (quadraticPotential A)) x v) ∧
      inner ℝ v (fderiv ℝ (gradient (quadraticPotential A)) x v) ≤ κ * ‖v‖^2 := by
  rw [quadratic_hessian hA.1, Matrix.inner_toEuclideanCLM, ← dot_self_eq_norm_sq]
  exact hA.2 (WithLp.ofLp v)

theorem quadratic_norm_lower (hA : Admissible κ A) (x : E d) :
    ‖x‖^2 / 2 ≤ quadraticPotential A x := by
  rw [quadraticPotential_eq_dot, ← dot_self_eq_norm_sq]
  exact div_le_div_of_nonneg_right (hA.2 _).1 (by norm_num)

@[simp] theorem quadraticPotential_zero (A : Precision d) : quadraticPotential A 0 = 0 := by
  simp [quadraticPotential]

theorem quadratic_minimizer_zero (hA : Admissible κ A) (x : E d) :
    quadraticPotential A 0 ≤ quadraticPotential A x := by
  rw [quadraticPotential_zero]
  exact (by positivity : 0 ≤ ‖x‖^2 / 2).trans (quadratic_norm_lower hA x)

theorem quadratic_minimizer_unique (hA : Admissible κ A) {x : E d}
    (hx : quadraticPotential A x ≤ quadraticPotential A 0) : x = 0 := by
  rw [quadraticPotential_zero] at hx
  have h := (quadratic_norm_lower hA x).trans hx
  exact norm_eq_zero.mp (by nlinarith [norm_nonneg x])

theorem quadratic_reply_eq_precisionReply (hA : A.IsHermitian) (x : E d) :
    (quadraticPotential A x, gradient (quadraticPotential A) x) = precisionReply A x := by
  rw [quadratic_gradient hA]
  rfl

#print axioms quadratic_hessian_bounds
#print axioms quadratic_minimizer_unique
#print axioms quadratic_reply_eq_precisionReply
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
