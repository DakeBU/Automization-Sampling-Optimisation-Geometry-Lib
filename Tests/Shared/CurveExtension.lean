import AutoSamplingTheory.TechnicalLemmas.Geometry.CurveExtension
import Mathlib.Analysis.Calculus.Deriv.Prod
import Mathlib.Analysis.Calculus.Deriv.Pow

noncomputable section

namespace AutoSamplingTheory.Tests.Shared.CurveExtension

open Filter Set
open scoped Topology
open TechnicalLemmas.Geometry.CurveExtension

-- Two extensions of the same parabola objective have different ambient
-- derivatives, but agree on its actual, nonconstant tangent velocities.
example (t₀ : ℝ) :
    fderiv ℝ (fun p : ℝ × ℝ => p.2) (t₀, t₀ ^ 2) (1, 2 * t₀) =
      fderiv ℝ (fun p : ℝ × ℝ => p.1 ^ 2) (t₀, t₀ ^ 2) (1, 2 * t₀) := by
  have hc : HasDerivAt (fun t : ℝ => (t, t ^ 2)) (1, 2 * t₀) t₀ := by
    simpa using (hasDerivAt_id t₀).prodMk ((hasDerivAt_id t₀).pow 2)
  apply fderiv_eq_on_curve_velocity (s := {p : ℝ × ℝ | p.2 = p.1 ^ 2})
    (c := fun t : ℝ => (t, t ^ 2)) differentiableAt_snd
    (differentiableAt_fst.pow 2) hc
  · exact Filter.Eventually.of_forall (fun _ => rfl)
  · filter_upwards [self_mem_nhdsWithin] with p hp
    exact hp

#print axioms TechnicalLemmas.Geometry.CurveExtension.fderiv_eq_on_curve_velocity

end AutoSamplingTheory.Tests.Shared.CurveExtension
