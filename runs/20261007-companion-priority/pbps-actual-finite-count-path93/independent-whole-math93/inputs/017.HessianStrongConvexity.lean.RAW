import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Convex.Strong
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Tactic.Module

/-!
# Strong convexity from a genuine Hessian lower bound

Restrict a C² real potential to an affine line and subtract the scalar
quadratic prescribed by its Hessian lower bound. The scalar second-derivative
convexity criterion then gives exactly Mathlib's strong-convexity convention.

This is the shared analytic prerequisite for the Hessian assumptions in
Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1 and arXiv:2609.06906v1,
Introduction (1.1). It is not a smoothness, normalization or sampler theorem.
The normed-space statement needs neither finite dimension nor positive modulus.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity

set_option backward.isDefEq.respectTransparency false in
/-- An everywhere C² potential whose genuine second Fréchet derivative is
bounded below on diagonal directions is strongly convex with the same modulus.
The `ContDiff` hypothesis prevents totalized derivatives from serving as
unsupported differentiability witnesses. -/
theorem strongConvexOn_univ_of_fderiv2_lower
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {V : E → ℝ} {α : ℝ}
    (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, α * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v) :
    StrongConvexOn (Set.univ : Set E) α V := by
  have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
  have hVdd : Differentiable ℝ (fderiv ℝ V) :=
    (hV.fderiv_right (m := 1) (by norm_num)).differentiable_one
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ a b ha hb hab
  let v : E := y - x
  let c : ℝ := α * ‖v‖ ^ 2
  let q : ℝ → ℝ := fun t => V (x + t • v) - c / 2 * t ^ 2
  let q' : ℝ → ℝ := fun t => fderiv ℝ V (x + t • v) v - c * t
  let q'' : ℝ → ℝ := fun t =>
    (fderiv ℝ (fderiv ℝ V) (x + t • v) v) v - c
  have hline (t : ℝ) : HasDerivAt (fun s : ℝ => x + s • v) v t := by
    simpa using ((hasDerivAt_id t).smul_const v).const_add x
  have hq' (t : ℝ) : HasDerivAt q (q' t) t := by
    have hquadratic : HasDerivAt (fun s : ℝ => c / 2 * s ^ 2) (c * t) t := by
      convert ((hasDerivAt_id t).pow 2).const_mul (c / 2) using 1 <;>
        first | rfl | (norm_num [id_eq]; ring)
    convert ((hVd _).hasFDerivAt.comp_hasDerivAt t (hline t)).sub hquadratic
      using 1 <;> rfl
  have hq'' (t : ℝ) : HasDerivAt q' (q'' t) t := by
    have hfirst := ((hVdd _).hasFDerivAt.comp_hasDerivAt t (hline t)).clm_apply
      (hasDerivAt_const t v)
    convert hfirst.sub ((hasDerivAt_id t).const_mul c) using 1 <;>
      first | rfl | simp [q'', ContinuousLinearMap.map_zero]
  have hconv : ConvexOn ℝ Set.univ q :=
    convexOn_of_hasDerivWithinAt2_nonneg convex_univ
      (fun t _ => (hq' t).continuousAt.continuousWithinAt)
      (fun t _ => (hq' t).hasDerivWithinAt)
      (fun t _ => (hq'' t).hasDerivWithinAt)
      (fun t _ => sub_nonneg.mpr (hH (x + t • v) v))
  have hchord := hconv.2 (x := 0) (Set.mem_univ _) (y := 1) (Set.mem_univ _)
    ha hb hab
  have hxy : x + b • v = a • x + b • y := by
    dsimp only [v]
    rw [show a = 1 - b by linarith]
    module
  have hend : x + v = y := by simp [v]
  simp only [q, smul_eq_mul, mul_zero, mul_one, zero_add, zero_smul, add_zero,
    one_pow, one_smul] at hchord
  norm_num only [zero_pow, mul_zero, sub_zero] at hchord
  rw [hxy, hend] at hchord
  have hnorm : ‖v‖ ^ 2 = ‖x - y‖ ^ 2 := by
    dsimp only [v]
    rw [norm_sub_rev]
  change V (a • x + b • y) ≤ a * V x + b * V y - a * b * (α / 2 * ‖x - y‖ ^ 2)
  dsimp only [c] at hchord
  rw [hnorm] at hchord
  rw [show a = 1 - b by linarith] at hchord ⊢
  nlinarith

end AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
