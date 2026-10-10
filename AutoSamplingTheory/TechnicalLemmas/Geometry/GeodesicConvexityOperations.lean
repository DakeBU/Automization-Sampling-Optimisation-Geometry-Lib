import AutoSamplingTheory.TechnicalLemmas.Geometry.GeodesicConvexity
import Mathlib.Tactic

/-!
# Closure operations for selected-geodesic convexity

Chewi's proof of Theorem 1.4.5 splits the KL functional into an energy part and
an entropy part, proves the corresponding geodesic-convexity estimates
separately, and then combines them.  The same algebraic closure principle is
useful in the Riemannian optimization route.

This module proves that closure once for the route-neutral
`GeodesicConvexity.IsAlphaGeodesicallyConvex` interface.  It does **not** claim
Chewi Theorem 1.4.5 itself: the measure-level tasks showing strong geodesic
convexity of the potential energy and displacement convexity of entropy remain
separate analytic Frontier Cells.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Geometry
namespace GeodesicConvexityOperations

open GeodesicConvexity

/-- Geodesic convexity moduli add under pointwise addition of functionals.

For the same selected family of geodesics, an `alpha`-geodesically convex
functional plus a `beta`-geodesically convex functional is
`(alpha + beta)`-geodesically convex. -/
theorem add
    {M : Type*} [MetricSpace M]
    {isGeodesic : (ℝ → M) → Prop}
    {F G : M → ℝ} {alpha beta : ℝ}
    (hF : IsAlphaGeodesicallyConvex isGeodesic F alpha)
    (hG : IsAlphaGeodesicallyConvex isGeodesic G beta) :
    IsAlphaGeodesicallyConvex isGeodesic (fun x => F x + G x) (alpha + beta) := by
  intro path hpath t ht
  have hF' := hF path hpath t ht
  have hG' := hG path hpath t ht
  change F (path t) + G (path t) ≤
    (1 - t) * (F (path 0) + G (path 0)) +
      t * (F (path 1) + G (path 1)) -
        ((alpha + beta) * t * (1 - t) / 2) *
          dist (path 0) (path 1) ^ 2
  calc
    F (path t) + G (path t) ≤
        ((1 - t) * F (path 0) + t * F (path 1) -
          (alpha * t * (1 - t) / 2) * dist (path 0) (path 1) ^ 2) +
        ((1 - t) * G (path 0) + t * G (path 1) -
          (beta * t * (1 - t) / 2) * dist (path 0) (path 1) ^ 2) :=
      add_le_add hF' hG'
    _ = (1 - t) * (F (path 0) + G (path 0)) +
        t * (F (path 1) + G (path 1)) -
          ((alpha + beta) * t * (1 - t) / 2) *
            dist (path 0) (path 1) ^ 2 := by
      ring

/-- A constant functional is zero-geodesically convex for every selected
geodesic family. -/
theorem constant_zero
    {M : Type*} [MetricSpace M]
    {isGeodesic : (ℝ → M) → Prop}
    (c : ℝ) :
    IsAlphaGeodesicallyConvex isGeodesic (fun _ : M => c) 0 := by
  intro path hpath t ht
  dsimp
  nlinarith

/-- Adding a zero-geodesically convex functional preserves an existing
geodesic-convexity modulus. -/
theorem add_zero_right
    {M : Type*} [MetricSpace M]
    {isGeodesic : (ℝ → M) → Prop}
    {F G : M → ℝ} {alpha : ℝ}
    (hF : IsAlphaGeodesicallyConvex isGeodesic F alpha)
    (hG : IsAlphaGeodesicallyConvex isGeodesic G 0) :
    IsAlphaGeodesicallyConvex isGeodesic (fun x => F x + G x) alpha := by
  simpa using add hF hG

/-- Adding a normalization constant does not change the geodesic-convexity
modulus.  This is the small closure used when a source functional is identified
with `energy + entropy + constant`. -/
theorem add_constant_right
    {M : Type*} [MetricSpace M]
    {isGeodesic : (ℝ → M) → Prop}
    {F : M → ℝ} {alpha c : ℝ}
    (hF : IsAlphaGeodesicallyConvex isGeodesic F alpha) :
    IsAlphaGeodesicallyConvex isGeodesic (fun x => F x + c) alpha := by
  have hc : IsAlphaGeodesicallyConvex isGeodesic (fun _ : M => c) 0 :=
    constant_zero (isGeodesic := isGeodesic) c
  simpa using add_zero_right hF hc

end GeodesicConvexityOperations
end Geometry
end TechnicalLemmas
end AutoSamplingTheory
