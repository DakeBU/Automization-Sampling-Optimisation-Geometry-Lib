import Mathlib.Analysis.Convex.Strong
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Quadratic regularization at first-order regularity

Chewi arXiv2605.07006v1 Section4.1 Lemma4.2: the actual regularized objective
is strongly convex and smooth. No C² or Hessian hypothesis is introduced.
This component does not establish oracle complexity or the full reduction.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder
open Set InnerProductSpace
open scoped NNReal

set_option backward.isDefEq.respectTransparency false in
/-- Quadratic regularization of a differentiable convex objective: actual
curvature, gradient and smoothness, including zero regularization. -/
theorem curvature_gradient_and_smoothness
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} (hd : Differentiable ℝ f) (hc : ConvexOn ℝ univ f)
    {β δ : ℝ≥0} (hL : LipschitzWith β (gradient f)) (u : E) :
    let W := fun x => f x + (δ : ℝ)/2*‖x-u‖^2
    Differentiable ℝ W ∧ StrongConvexOn univ (δ : ℝ) W ∧
      (∀ x, gradient W x = gradient f x + (δ : ℝ) • (x-u)) ∧
      LipschitzWith (β+δ) (gradient W) := by
  let W := fun x => f x + (δ : ℝ)/2*‖x-u‖^2
  have hq (x : E) : HasFDerivAt (fun z => (δ : ℝ)/2*‖z-u‖^2)
      ((δ : ℝ) • innerSL ℝ (x-u)) x := by
    convert (((hasFDerivAt_id x).sub_const u).norm_sq).const_mul ((δ : ℝ)/2)
      using 1 <;> first | rfl | (ext v; simp; ring)
  have hWd : Differentiable ℝ W := fun x => ((hd x).hasFDerivAt.add (hq x)).differentiableAt
  have hgrad (x : E) : gradient W x = gradient f x + (δ : ℝ) • (x-u) := by
    have hfd : fderiv ℝ W x = fderiv ℝ f x + (δ : ℝ) • innerSL ℝ (x-u) :=
      ((hd x).hasFDerivAt.add (hq x)).fderiv
    rw [gradient, hfd, map_add, map_smul]
    congr 1
    exact congrArg (fun v : E => (δ : ℝ) • v) ((toDual ℝ E).symm_apply_apply (x-u))
  have hstrong : StrongConvexOn univ (δ : ℝ) W := by
    apply strongConvexOn_iff_convex.mpr
    have ha := (hc.add (((-(δ : ℝ)) • (innerSL ℝ u).toLinearMap).convexOn convex_univ)).add_const
      ((δ : ℝ)/2*‖u‖^2)
    convert! ha using 1
    ext x
    simp [W, norm_sub_sq_real, real_inner_comm]
    ring
  refine ⟨hWd,hstrong,hgrad,?_⟩
  apply LipschitzWith.of_dist_le_mul
  intro x y
  rw [dist_eq_norm, hgrad, hgrad]
  have he : gradient f x + (δ : ℝ) • (x-u) -
      (gradient f y + (δ : ℝ) • (y-u)) =
      (gradient f x-gradient f y) + (δ : ℝ) • (x-y) := by
    simp only [smul_sub]
    abel
  rw [he]
  have hb := hL.dist_le_mul x y
  rw [dist_eq_norm, dist_eq_norm] at hb
  calc
    _ ≤ ‖gradient f x-gradient f y‖ + ‖(δ : ℝ) • (x-y)‖ := norm_add_le _ _
    _ ≤ (β : ℝ)*‖x-y‖ + (δ : ℝ)*‖x-y‖ := by
      rw [norm_smul, Real.norm_eq_abs, abs_of_nonneg δ.coe_nonneg]
      linarith
    _ = ((β+δ : ℝ≥0) : ℝ)*dist x y := by rw [dist_eq_norm]; simp; ring
end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder
