import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.FDeriv.Comp
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Tactic

/-!
# Algebra and scalar chain rules for gradients

Mathlib's gradient API is intentionally minimal.  Sampling proofs repeatedly
need derived rules for real-valued functions on a real Hilbert space:

* product rule: `grad(fg) = f grad g + g grad f`;
* scalar outer chain rule: `grad(phi ∘ f) = phi'(f) grad f`;
* reciprocal and quotient rules on the nonzero-denominator locus.

This file packages these rules at the `HasGradientAt` level so downstream
proofs can keep differentiability and positivity/nonvanishing hypotheses
explicit.  In particular, the quotient rule is the local calculus leaf needed
for `rho = p / q` in Chewi Theorem 8.3.1.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace Calculus
namespace GradientAlgebra

open InnerProductSpace
open scoped RealInnerProductSpace

noncomputable section

/-- Product rule for gradients of real-valued functions on a real Hilbert
space. -/
theorem HasGradientAt.mul
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f g : E → ℝ} {x gradF gradG : E}
    (hf : HasGradientAt f gradF x) (hg : HasGradientAt g gradG x) :
    HasGradientAt (fun y => f y * g y)
      (f x • gradG + g x • gradF) x := by
  rw [hasGradientAt_iff_hasFDerivAt]
  change HasFDerivAt (f * g)
    ((toDual ℝ E) (f x • gradG + g x • gradF)) x
  simpa only [map_add, map_smul] using hf.hasFDerivAt.mul hg.hasFDerivAt

/-- Scalar outer-function chain rule for gradients. -/
theorem HasGradientAt.comp_real
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} {phi : ℝ → ℝ} {x gradF : E} {phi' : ℝ}
    (hf : HasGradientAt f gradF x)
    (hphi : HasDerivAt phi phi' (f x)) :
    HasGradientAt (fun y => phi (f y)) (phi' • gradF) x := by
  rw [hasGradientAt_iff_hasFDerivAt]
  change HasFDerivAt (phi ∘ f) ((toDual ℝ E) (phi' • gradF)) x
  have hmap :
      (toDual ℝ E) (phi' • gradF) =
        (ContinuousLinearMap.toSpanSingleton ℝ phi').comp ((toDual ℝ E) gradF) := by
    ext v
    simp [InnerProductSpace.toDual_apply_apply, mul_comm]
  rw [hmap]
  exact hphi.hasFDerivAt.comp x hf.hasFDerivAt

/-- Reciprocal rule for gradients on the nonzero locus.

The coefficient is kept in Mathlib's native derivative form
`-(f x ^ 2)⁻¹`; downstream algebra may rewrite it as `-1 / f(x)^2` when
needed. -/
theorem HasGradientAt.inv
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} {x gradF : E}
    (hf : HasGradientAt f gradF x) (hfx : f x ≠ 0) :
    HasGradientAt (fun y => (f y)⁻¹) (-(f x ^ 2)⁻¹ • gradF) x := by
  exact HasGradientAt.comp_real hf (hasDerivAt_inv hfx)

/-- Quotient rule for gradients on the nonzero-denominator locus.

It is stated in the product-with-reciprocal form produced directly by the two
reusable rules above:

`grad(f/g) = f * (-(g^2)⁻¹ grad g) + g⁻¹ grad f`.

This avoids hiding any vector-space normalization inside the calculus theorem;
a later scalar-algebra leaf may rewrite it to the familiar
`(g grad f - f grad g) / g^2` form. -/
theorem HasGradientAt.div
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f g : E → ℝ} {x gradF gradG : E}
    (hf : HasGradientAt f gradF x)
    (hg : HasGradientAt g gradG x)
    (hg0 : g x ≠ 0) :
    HasGradientAt (fun y => f y / g y)
      (f x • (-(g x ^ 2)⁻¹ • gradG) + (g x)⁻¹ • gradF) x := by
  simpa only [div_eq_mul_inv] using
    HasGradientAt.mul hf (HasGradientAt.inv hg hg0)

/-- Total-gradient form of the product rule under pointwise differentiability. -/
theorem gradient_mul_eq_of_differentiableAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f g : E → ℝ} {x : E}
    (hf : DifferentiableAt ℝ f x) (hg : DifferentiableAt ℝ g x) :
    gradient (fun y => f y * g y) x =
      f x • gradient g x + g x • gradient f x := by
  exact (HasGradientAt.mul hf.hasGradientAt hg.hasGradientAt).gradient

/-- Total-gradient form of the scalar chain rule. -/
theorem gradient_comp_real_eq_of_differentiableAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} {phi : ℝ → ℝ} {x : E}
    (hf : DifferentiableAt ℝ f x)
    (hphi : DifferentiableAt ℝ phi (f x)) :
    gradient (fun y => phi (f y)) x =
      deriv phi (f x) • gradient f x := by
  exact (HasGradientAt.comp_real hf.hasGradientAt hphi.hasDerivAt).gradient

/-- Total-gradient reciprocal rule under pointwise differentiability and a
nonzero value. -/
theorem gradient_inv_eq_of_differentiableAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f : E → ℝ} {x : E}
    (hf : DifferentiableAt ℝ f x) (hfx : f x ≠ 0) :
    gradient (fun y => (f y)⁻¹) x =
      (-(f x ^ 2)⁻¹) • gradient f x := by
  exact (HasGradientAt.inv hf.hasGradientAt hfx).gradient

/-- Total-gradient quotient rule under pointwise differentiability and a
nonzero denominator. -/
theorem gradient_div_eq_of_differentiableAt
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    {f g : E → ℝ} {x : E}
    (hf : DifferentiableAt ℝ f x)
    (hg : DifferentiableAt ℝ g x)
    (hg0 : g x ≠ 0) :
    gradient (fun y => f y / g y) x =
      f x • (-(g x ^ 2)⁻¹ • gradient g x) +
        (g x)⁻¹ • gradient f x := by
  exact (HasGradientAt.div hf.hasGradientAt hg.hasGradientAt hg0).gradient

end

end GradientAlgebra
end Calculus
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
