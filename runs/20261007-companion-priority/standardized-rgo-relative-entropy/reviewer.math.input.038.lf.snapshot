import Mathlib.Analysis.Calculus.Deriv.Slope
import Mathlib.Topology.MetricSpace.Basic

/-!
# Geodesic convexity

The definition is parameterized by the predicate selecting geodesic curves.
This keeps it reusable for Riemannian and Wasserstein spaces while those
spaces retain their own regularity and constant-speed requirements.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Geometry
namespace GeodesicConvexity

open Filter Set
open scoped Topology

/-- Chewi Definition 1.3.26, condition 1: `F` is alpha-geodesically convex
along every selected geodesic, with the source normalization
`alpha * t * (1-t) / 2`. -/
def IsAlphaGeodesicallyConvex
    {M : Type*} [MetricSpace M]
    (isGeodesic : (ℝ → M) → Prop) (F : M → ℝ) (alpha : ℝ) : Prop :=
  ∀ path : ℝ → M, isGeodesic path →
    ∀ t : ℝ, t ∈ Icc (0 : ℝ) 1 →
      F (path t) ≤
        (1 - t) * F (path 0) + t * F (path 1) -
          (alpha * t * (1 - t) / 2) * dist (path 0) (path 1) ^ 2

/-- The chord formulation of geodesic alpha-convexity implies its first-order
form along a differentiable selected geodesic.  The scalar
`gradientPairing` is the derivative of `F` along the path at its initial
point; identifying it with the Riemannian or Wasserstein gradient pairing is
a separate geometric theorem.

This is the one-dimensional limiting argument behind Chewi display
(1.4.7). -/
theorem firstOrder_geodesicConvexity
    {M : Type*} [MetricSpace M]
    {isGeodesic : (ℝ → M) → Prop} {F : M → ℝ} {alpha : ℝ}
    (hconvex : IsAlphaGeodesicallyConvex isGeodesic F alpha)
    {path : ℝ → M} (hpath : isGeodesic path)
    {gradientPairing : ℝ}
    (hderiv : HasDerivAt (fun t => F (path t)) gradientPairing 0) :
    F (path 1) ≥
      F (path 0) + gradientPairing +
        alpha / 2 * dist (path 0) (path 1) ^ 2 := by
  let phi : ℝ → ℝ := fun t => F (path t)
  let upper : ℝ → ℝ := fun t =>
    F (path 1) - F (path 0) -
      alpha * (1 - t) / 2 * dist (path 0) (path 1) ^ 2
  have hslope :
      Tendsto (slope phi 0) (𝓝[>] 0) (𝓝 gradientPairing) := by
    apply hderiv.tendsto_slope.mono_left
    apply nhdsWithin_mono
    intro t ht
    simpa only [mem_compl_iff, mem_singleton_iff] using ne_of_gt ht
  have hupper :
      Tendsto upper (𝓝[>] 0) (𝓝 (upper 0)) := by
    have hcontinuous : ContinuousAt upper 0 := by
      dsimp only [upper]
      fun_prop
    have hfilter : 𝓝[>] (0 : ℝ) ≤ 𝓝 0 := inf_le_left
    exact hcontinuous.tendsto.mono_left hfilter
  have hslope_le : slope phi 0 ≤ᶠ[𝓝[>] 0] upper := by
    filter_upwards [self_mem_nhdsWithin,
      (eventually_lt_nhds zero_lt_one).filter_mono inf_le_left]
      with t ht htle
    have htpos : 0 < t := ht
    have hchord := hconvex path hpath t ⟨htpos.le, htle.le⟩
    have hquotient :
        (F (path t) - F (path 0)) / t ≤ upper t := by
      apply (div_le_iff₀ htpos).2
      dsimp only [upper]
      nlinarith
    rw [div_eq_inv_mul] at hquotient
    simpa [phi, slope, htpos.ne'] using hquotient
  have hfirst := le_of_tendsto_of_tendsto hslope hupper hslope_le
  dsimp only [upper, sub_zero, one_mul] at hfirst
  linarith

end GeodesicConvexity
end Geometry
end TechnicalLemmas
end AutoSamplingTheory
