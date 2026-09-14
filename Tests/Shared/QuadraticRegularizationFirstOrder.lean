import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Mul

open Set
open AutoSamplingTheory.TechnicalLemmas.Analysis
open scoped NNReal

-- A genuine quadratic and arbitrary precision, including zero. The actual
-- gradient formula supplies the gradient update, while the Lipschitz output
-- certifies its reciprocal step size. No Hessian premise is supplied.
set_option backward.isDefEq.respectTransparency false in
example (δ : ℝ≥0) :
    let W := fun x : ℝ => x^2/2 + (δ : ℝ)/2*‖x-1‖^2
    StrongConvexOn univ (δ : ℝ) W ∧ LipschitzWith (1+δ) (gradient W) ∧
      (1:ℝ) - 1/(1+δ)*gradient W 1 = (δ : ℝ)/(1+δ) := by
  let f := fun x : ℝ => x^2/2
  have hd : Differentiable ℝ f := by fun_prop
  have hg (x : ℝ) : gradient f x = x := by
    have h : HasDerivAt f x x := by
      simpa [f] using ((hasDerivAt_id x).pow 2).div_const (2:ℝ)
    exact h.hasGradientAt.gradient
  have hc : ConvexOn ℝ univ f := by
    refine ⟨convex_univ, ?_⟩
    intro x _ y _ a b ha hb hab
    simp only [f, smul_eq_mul]
    have hnon : 0 ≤ a*b*(x-y)^2 := mul_nonneg (mul_nonneg ha hb) (sq_nonneg _)
    have he : a*x^2/2+b*y^2/2-(a*x+b*y)^2/2 = a*b*(x-y)^2/2 := by
      have hb' : b = 1-a := by linarith
      rw [hb']; ring
    nlinarith
  have hL : LipschitzWith 1 (gradient f) := by
    have he : gradient f = id := funext hg
    rw [he]; exact LipschitzWith.id
  obtain ⟨_,hsc,hform,hsm⟩ :=
    QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness hd hc hL (δ := δ) 1
  refine ⟨hsc,hsm,?_⟩
  rw [hform, hg]
  simp only [sub_self, smul_zero, add_zero]
  have hp : (0:ℝ)<1+δ := by positivity
  field_simp
  ring

-- Source parameter arithmetic is checked in its genuine positive regime.
-- These inequalities alone do not claim oracle complexity.
example {β R ε : ℝ} (hβ : 0 < β) (hR : 0 < R) (hε : 0 < ε)
    (hsmall : ε ≤ β*R^2) :
    let δ := ε/R^2
    0 < δ ∧ δ ≤ β ∧ β+δ ≤ 2*β ∧ (β+δ)/δ ≤ 2*β*R^2/ε := by
  have hR2 : 0 < R^2 := sq_pos_of_pos hR
  have hd : 0 < ε/R^2 := div_pos hε hR2
  have hdb : ε/R^2 ≤ β := (div_le_iff₀ hR2).mpr hsmall
  refine ⟨hd,hdb,by linarith,?_⟩
  apply (div_le_iff₀ hd).mpr
  have he : 2*β*R^2/ε*(ε/R^2) = 2*β := by field_simp
  rw [he]
  linarith

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness
