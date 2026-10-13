import AutoSamplingTheory.TechnicalLemmas.Geometry.GeodesicConvexity
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.LineDeriv.Basic
import Mathlib.Analysis.Convex.Strong

/-!
# First-order lower bounds for strongly convex functions

This module is a source-neutral shared convex-analysis layer for the front-loaded
Samplinglib textbook spine.  It ports the mathematical content of the pinned
Optlib theorem `Strong_Convex_second_lower` while reusing Samplinglib's already
compiled scalar/geodesic limiting lemma.

The main theorem is consumed by Chewi's Optimization Proposition 1.6, by the
strong-convexity part of Log-Concave Sampling Chapter 2, and by convex-potential
arguments in Statistical Optimal Transport.  Gibbs/log-concavity statements
remain explicit downstream adapters.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Analysis
namespace StrongConvexFirstOrder

open Set
open scoped RealInnerProductSpace

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- A strongly convex function lies above its first-order model by the
quadratic term `m / 2 * ‖y - x‖²`.

This is the ASTIS-owned shared port of Optlib's pinned
`Strong_Convex_second_lower`.  The statement is deliberately domain-local and
uses a supplied Mathlib gradient.  Chewi's whole-space `C¹` formulation is a
downstream specialization, not a silent relabeling of this more general shared
interface.

The proof factors through `Geometry.GeodesicConvexity.firstOrder_geodesicConvexity`:
strong convexity supplies the chord inequality on the affine segment and the
supplied gradient supplies the derivative of that segment at its initial point.
-/
theorem firstOrder_lower_bound_of_strongConvexOn
    {s : Set E} {f : E → ℝ} {m : ℝ} {grad : E → E}
    (hsc : StrongConvexOn s m f)
    (hgrad : ∀ z ∈ s, HasGradientAt f (grad z) z)
    {x y : E} (hx : x ∈ s) (hy : y ∈ s) :
    f y ≥ f x + inner ℝ (grad x) (y - x) + m / 2 * ‖y - x‖ ^ 2 := by
  let path : ℝ → E := fun t => x + t • (y - x)
  let isSelected : (ℝ → E) → Prop := fun q => q = path
  have hpath : isSelected path := rfl
  have hconvex :
      Geometry.GeodesicConvexity.IsAlphaGeodesicallyConvex isSelected f m := by
    intro q hq t ht
    subst q
    have hnonneg_left : 0 ≤ 1 - t := sub_nonneg.mpr ht.2
    have hnonneg_right : 0 ≤ t := ht.1
    have hstrong := hsc.2 hx hy hnonneg_left hnonneg_right (by ring)
    have hpoint : path t = (1 - t) • x + t • y := by
      dsimp only [path]
      rw [smul_sub, sub_smul, one_smul]
      abel
    calc
      f (path t) = f ((1 - t) • x + t • y) := congrArg f hpoint
      _ ≤ (1 - t) * f x + t * f y -
          (1 - t) * t * (m / 2 * ‖x - y‖ ^ 2) := by
        simpa [smul_eq_mul] using hstrong
      _ = (1 - t) * f (path 0) + t * f (path 1) -
          (m * t * (1 - t) / 2) * dist (path 0) (path 1) ^ 2 := by
        simp [path, dist_eq_norm]
        ring
  have hline :
      HasLineDerivAt ℝ f (inner ℝ (grad x) (y - x)) x (y - x) := by
    have h := (hgrad x hx).hasFDerivAt.hasLineDerivAt (y - x)
    simpa [InnerProductSpace.toDual_apply_apply] using h
  have hderiv :
      HasDerivAt (fun t : ℝ => f (path t)) (inner ℝ (grad x) (y - x)) 0 := by
    simpa [HasLineDerivAt, path] using hline
  have hfirst :=
    Geometry.GeodesicConvexity.firstOrder_geodesicConvexity
      hconvex hpath hderiv
  simpa [path, dist_eq_norm, norm_sub_rev] using hfirst

/-- The gradient of a strongly convex function has the corresponding inner-product
lower bound on its domain.

Mathematical provenance: Optlib `Strong_Convex_lower`, commit
`5da27c5f95aa6a8a45b8c14b968ade4c13ff18c3`,
`Optlib/Convex/StronglyConvex.lean` (Apache-2.0; Chenyi Li and Ziyu Wang).
This proof reuses the local first-order bound in both directions, as in Chewi,
arXiv:2605.07006v1, Proposition 1.6, (1.4) implies (1.5).
The domain-local supplied-gradient interface retains arbitrary real `m`;
Chewi's whole-space `C¹`, nonnegative-modulus statement is a specialization.
-/
theorem gradient_inner_lower_bound_of_strongConvexOn
    {s : Set E} {f : E → ℝ} {m : ℝ} {grad : E → E}
    (hsc : StrongConvexOn s m f)
    (hgrad : ∀ z ∈ s, HasGradientAt f (grad z) z)
    {x y : E} (hx : x ∈ s) (hy : y ∈ s) :
    m * ‖y - x‖ ^ 2 ≤ inner ℝ (grad y - grad x) (y - x) := by
  have hxy := firstOrder_lower_bound_of_strongConvexOn hsc hgrad hx hy
  have hyx := firstOrder_lower_bound_of_strongConvexOn hsc hgrad hy hx
  rw [show x - y = -(y - x) by abel, inner_neg_right, norm_neg] at hyx
  rw [inner_sub_left]
  linarith

end

end StrongConvexFirstOrder
end Analysis
end TechnicalLemmas
end AutoSamplingTheory
