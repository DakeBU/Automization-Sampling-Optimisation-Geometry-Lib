import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.Symmetric
import Mathlib.LinearAlgebra.Eigenspace.Basic

/-!
# Exact gradient descent on a quadratic objective

Chewi arXiv:2605.07006v1 Exercise3.3. Symmetry gives the actual gradient of
`f(x)=⟪x,Hx⟫/2`; the iteration is then a power of `I-hH`. A supplied eigenmode
has an exact trajectory, norm and objective value. The symmetric Hilbert and
arbitrary-step identities extend the positive-definite Euclidean source; they
do not assert spectral endpoint existence or convergence for every step.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent

open InnerProductSpace
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

set_option backward.isDefEq.respectTransparency false in
/-- Actual quadratic-gradient iterates equal the powers of the linear update. -/
theorem quadratic_gradient_iterate (H : E →L[ℝ] E) (hH : H.IsSymmetric)
    (h : ℝ) (N : ℕ) (x : E) :
    let f := fun z : E => inner ℝ z (H z) / 2
    (fun z => z - h • gradient f z)^[N] x = ((1 - h • H) ^ N) x := by
  let f := fun z : E => inner ℝ z (H z) / 2
  have hg (z : E) : gradient f z = H z := by
    have hraw := ((hasFDerivAt_id z).inner ℝ H.hasFDerivAt).const_mul (1 / 2 : ℝ)
    have hlin : (1 / 2 : ℝ) •
        ((fderivInnerCLM ℝ (z, H z)).comp ((ContinuousLinearMap.id ℝ E).prod H)) =
        toDual ℝ E (H z) := by
      ext v
      change (1 / 2 : ℝ) * (inner ℝ z (H v) + inner ℝ v (H z)) = inner ℝ (H z) v
      rw [← hH.apply_clm z v, (real_inner_comm v (H z)).symm]
      ring
    have hd : HasFDerivAt f (toDual ℝ E (H z)) z := by
      convert hraw using 1 <;> first | rfl | exact hlin.symm | (ext v; simp only [f, id_eq]; ring)
    exact (hasGradientAt_iff_hasFDerivAt.mpr hd).gradient
  change (fun z => z - h • gradient f z)^[N] x = _
  simp_rw [hg]
  exact congrFun (FunLike.coe_pow_eq_iterate (1 - h • H) N).symm x

/-- A supplied eigenmode gives exact iterates, distances to zero and quadratic values.
No existence of an eigenvector or stability of the chosen step is assumed. -/
theorem quadratic_eigenmode (H : E →L[ℝ] E) (hH : H.IsSymmetric)
    {μ : ℝ} {x : E} (hx : H x = μ • x) (h : ℝ) (N : ℕ) :
    let f := fun z : E => inner ℝ z (H z) / 2
    let z := (fun y => y - h • gradient f y)^[N] x
    z = (1 - h * μ) ^ N • x ∧
      ‖z‖ = |1 - h * μ| ^ N * ‖x‖ ∧
      f z = (1 - h * μ) ^ (2 * N) * f x := by
  let f := fun z : E => inner ℝ z (H z) / 2
  let A : E →L[ℝ] E := 1 - h • H
  have hAx : A x = (1 - h * μ) • x := by
    simp only [A, sub_apply, one_apply_eq_self,
      smul_apply, hx, smul_smul, sub_smul, one_smul]
  have hp : (A ^ N) x = (1 - h * μ) ^ N • x := by
    by_cases hz : x = 0
    · simp [hz]
    · have he : Module.End.HasEigenvector A.toLinearMap (1 - h * μ) x :=
        ⟨Module.End.mem_eigenspace_iff.mpr hAx, hz⟩
      have ht := congrArg (fun K : E →ₗ[ℝ] E => K x) (ContinuousLinearMap.toLinearMap_pow A N)
      convert ht.trans (he.pow_apply N) using 1; rfl
  have hi := (quadratic_gradient_iterate H hH h N x).trans hp
  change _ = _ ∧ _ = _ ∧ f _ = _ * f x
  rw [hi]
  refine ⟨rfl, ?_, ?_⟩
  · simp [norm_smul, Real.norm_eq_abs]
  · simp only [f, map_smul, inner_smul_left, inner_smul_right, RCLike.conj_to_real]
    rw [Nat.mul_comm 2 N, pow_mul]
    ring

end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent
