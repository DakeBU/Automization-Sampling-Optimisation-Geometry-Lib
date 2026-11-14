import Mathlib.Analysis.Calculus.Deriv.AffineMap
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Convex.Strong
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# Strong convexity from quantitative gradient monotonicity

Statement provenance: Optlib `Lower_Strong_Convex`, commit
`5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3`,
`Optlib/Convex/StronglyConvex.lean` (Apache-2.0; Chenyi Li and Ziyu Wang).
The proof reuses Mathlib's scalar derivative criterion on an affine segment
after subtracting its quadratic correction. This is a mean-value-theorem route;
Chewi, arXiv:2605.07006v1, Proposition 1.6 (1.5) implies (1.3), instead uses
integration under whole-space C¹ assumptions. No integral proof, Hessian
equivalence or complete textbook proposition is claimed here.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse

open Set
open scoped RealInnerProductSpace

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Quantitative monotonicity of genuine ambient gradients on a convex domain
implies strong convexity, with the same (possibly signed) modulus. -/
theorem strongConvexOn_of_gradient_inner_lower_bound
    {s : Set E} {f : E → ℝ} {m : ℝ} {grad : E → E}
    (hs : Convex ℝ s)
    (hgrad : ∀ z ∈ s, HasGradientAt f (grad z) z)
    (hmono : ∀ x ∈ s, ∀ y ∈ s,
      m * ‖y - x‖ ^ 2 ≤ inner ℝ (grad y - grad x) (y - x)) :
    StrongConvexOn s m f := by
  refine ⟨hs, ?_⟩
  intro x hx y hy a b ha hb hab
  let p : ℝ → E := fun t => x + t • (y - x)
  let q : ℝ → ℝ := fun t => f (p t) - m / 2 * t ^ 2 * ‖y - x‖ ^ 2
  let q' : ℝ → ℝ := fun t => inner ℝ (grad (p t)) (y - x) - m * t * ‖y - x‖ ^ 2
  have hp : ∀ t ∈ Icc (0 : ℝ) 1, p t ∈ s := by
    intro t ht
    exact hs.add_smul_sub_mem hx hy ht
  have hq : ∀ t ∈ Icc (0 : ℝ) 1, HasDerivAt q (q' t) t := by
    intro t ht
    have hline : HasDerivAt (fun u => f (p u))
        (inner ℝ (grad (p t)) (y - x)) t := by
      have hpderiv : HasDerivAt p (y - x) t := by
        simpa [p] using ((hasDerivAt_id t).smul_const (y - x)).const_add x
      convert! (hgrad (p t) (hp t ht)).hasFDerivAt.comp_hasDerivAt t hpderiv using 1
    have hquad := (((hasDerivAt_id t).pow 2).const_mul (m / 2)).mul_const (‖y - x‖ ^ 2)
    convert! hline.sub hquad using 1
    simp only [q', id_eq]
    ring
  have hmon : MonotoneOn q' (Icc (0 : ℝ) 1) := by
    intro u hu v hv huv
    rcases eq_or_lt_of_le huv with rfl | huv
    · exact le_rfl
    have h := hmono (p u) (hp u hu) (p v) (hp v hv)
    have hdis : p v - p u = (v - u) • (y - x) := by
      simp only [p, add_sub_add_left_eq_sub, sub_smul]
    rw [hdis, inner_smul_right, norm_smul, Real.norm_eq_abs, mul_pow, sq_abs] at h
    have hscaled : (v - u) * (m * (v - u) * ‖y - x‖ ^ 2) ≤
        (v - u) * inner ℝ (grad (p v) - grad (p u)) (y - x) := by
      nlinarith [h]
    have hbound := le_of_mul_le_mul_left hscaled (sub_pos.mpr huv)
    rw [inner_sub_left] at hbound
    dsimp [q']
    linarith
  have hconv : ConvexOn ℝ (Icc (0 : ℝ) 1) q := by
    apply MonotoneOn.convexOn_of_deriv (convex_Icc (0 : ℝ) 1)
      (fun t ht => (hq t ht).continuousAt.continuousWithinAt)
      (fun t ht => (hq t (interior_subset ht)).differentiableAt.differentiableWithinAt)
    intro u hu v hv huv
    rw [(hq u (interior_subset hu)).deriv, (hq v (interior_subset hv)).deriv]
    exact hmon (interior_subset hu) (interior_subset hv) huv
  have hchord := hconv.2 (show (0 : ℝ) ∈ Icc 0 1 by norm_num)
    (show (1 : ℝ) ∈ Icc 0 1 by norm_num) ha hb hab
  have hpoint : a • x + b • y = p b := by
    have ha' : a = 1 - b := by linarith
    simp [p, ha', sub_smul, smul_sub]
    abel
  rw [hpoint]
  simp only [smul_eq_mul, mul_zero, mul_one, zero_add] at hchord ⊢
  norm_num [q, p] at hchord
  rw [norm_sub_rev] at hchord
  have ha' : a = 1 - b := by linarith
  rw [ha'] at hchord ⊢
  dsimp [p]
  nlinarith [hchord]

end AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse
