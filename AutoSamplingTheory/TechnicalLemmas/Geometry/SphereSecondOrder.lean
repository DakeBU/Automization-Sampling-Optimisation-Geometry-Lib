import Mathlib.Analysis.Calculus.DerivativeTest
import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere

/-!
# Second-order necessary conditions on the unit sphere

This module proves the non-strict second-order condition at a local extremum
and applies it to exponential-map curves on the unit sphere.  The results are
model-independent prerequisites for Riemannian optimization and parabolic
maximum-principle arguments.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereSecondOrder

open Filter Set
open scoped InnerProductSpace Topology

noncomputable section

/-- At a local minimum of a continuous real function, the second derivative,
when represented by `deriv (deriv f)`, cannot be negative.  This complements
Mathlib's sufficient strict second-derivative test with the necessary
non-strict direction. -/
theorem IsLocalMin.deriv_deriv_nonneg_of_continuousAt
    {f : ℝ → ℝ} {x : ℝ} (hmin : IsLocalMin f x)
    (hc : ContinuousAt f x) :
    0 ≤ deriv (deriv f) x := by
  by_contra hnonneg
  have hneg : deriv (deriv f) x < 0 := lt_of_not_ge hnonneg
  have hmax : IsLocalMax f x :=
    isLocalMax_of_deriv_deriv_neg hneg hmin.deriv_eq_zero hc
  have hconst : f =ᶠ[𝓝 x] fun _ : ℝ => f x := by
    filter_upwards [hmin, hmax] with y hymin hymax
    exact le_antisymm hymax hymin
  have hderiv : deriv f =ᶠ[𝓝 x] fun _ : ℝ => 0 := by
    simpa using hconst.deriv
  have hzero : deriv (deriv f) x = 0 := by
    calc
      deriv (deriv f) x = deriv (fun _ : ℝ => 0) x := hderiv.deriv_eq
      _ = 0 := by simp
  linarith

/-- At a local maximum of a continuous real function, the second derivative,
when represented by `deriv (deriv f)`, is nonpositive. -/
theorem IsLocalMax.deriv_deriv_nonpos_of_continuousAt
    {f : ℝ → ℝ} {x : ℝ} (hmax : IsLocalMax f x)
    (hc : ContinuousAt f x) :
    deriv (deriv f) x ≤ 0 := by
  by_contra hnonpos
  have hpos : 0 < deriv (deriv f) x := lt_of_not_ge hnonpos
  have hmin : IsLocalMin f x :=
    isLocalMin_of_deriv_deriv_pos hpos hmax.deriv_eq_zero hc
  have hconst : f =ᶠ[𝓝 x] fun _ : ℝ => f x := by
    filter_upwards [hmin, hmax] with y hymin hymax
    exact le_antisymm hymax hymin
  have hderiv : deriv f =ᶠ[𝓝 x] fun _ : ℝ => 0 := by
    simpa using hconst.deriv
  have hzero : deriv (deriv f) x = 0 := by
    calc
      deriv (deriv f) x = deriv (fun _ : ℝ => 0) x := hderiv.deriv_eq
      _ = 0 := by simp
  linarith

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

open AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere

/-- Restricting a function with a global minimum on the unit sphere to any
tangent exponential-map curve gives a local minimum at time zero. -/
private theorem unitSphere_isMinOn_expCurve_isLocalMin
    {f : E → ℝ} {w z : E}
    (hw : ‖w‖ = 1) (hz : ⟪w, z⟫_ℝ = 0)
    (hmin : IsMinOn f (Metric.sphere (0 : E) 1) w) :
    IsLocalMin (fun t : ℝ => f (unitSphereExp w (t • z))) 0 := by
  filter_upwards [] with t
  have htan : ⟪w, t • z⟫_ℝ = 0 := by
    simp [real_inner_smul_right, hz]
  have hmem : unitSphereExp w (t • z) ∈ Metric.sphere (0 : E) 1 := by
    rw [Metric.mem_sphere]
    simpa [dist_eq_norm] using unitSphereExp_norm_eq_one hw htan
  simpa [unitSphereExp] using hmin hmem

/-- Restricting a function with a global maximum on the unit sphere to any
tangent exponential-map curve gives a local maximum at time zero. -/
private theorem unitSphere_isMaxOn_expCurve_isLocalMax
    {f : E → ℝ} {w z : E}
    (hw : ‖w‖ = 1) (hz : ⟪w, z⟫_ℝ = 0)
    (hmax : IsMaxOn f (Metric.sphere (0 : E) 1) w) :
    IsLocalMax (fun t : ℝ => f (unitSphereExp w (t • z))) 0 := by
  filter_upwards [] with t
  have htan : ⟪w, t • z⟫_ℝ = 0 := by
    simp [real_inner_smul_right, hz]
  have hmem : unitSphereExp w (t • z) ∈ Metric.sphere (0 : E) 1 := by
    rw [Metric.mem_sphere]
    simpa [dist_eq_norm] using unitSphereExp_norm_eq_one hw htan
  simpa [unitSphereExp] using hmax hmem

/-- The directional second derivative along every tangent exponential-map
curve is nonnegative at a global minimum on the unit sphere. -/
private theorem unitSphere_isMinOn_expCurve_deriv_deriv_nonneg
    {f : E → ℝ} {w z : E}
    (hw : ‖w‖ = 1) (hz : ⟪w, z⟫_ℝ = 0)
    (hmin : IsMinOn f (Metric.sphere (0 : E) 1) w)
    (hc : ContinuousAt (fun t : ℝ => f (unitSphereExp w (t • z))) 0) :
    0 ≤ deriv (deriv (fun t : ℝ => f (unitSphereExp w (t • z)))) 0 := by
  exact IsLocalMin.deriv_deriv_nonneg_of_continuousAt
    (unitSphere_isMinOn_expCurve_isLocalMin hw hz hmin) hc

/-- The directional second derivative along every tangent exponential-map
curve is nonpositive at a global maximum on the unit sphere. -/
private theorem unitSphere_isMaxOn_expCurve_deriv_deriv_nonpos
    {f : E → ℝ} {w z : E}
    (hw : ‖w‖ = 1) (hz : ⟪w, z⟫_ℝ = 0)
    (hmax : IsMaxOn f (Metric.sphere (0 : E) 1) w)
    (hc : ContinuousAt (fun t : ℝ => f (unitSphereExp w (t • z))) 0) :
    deriv (deriv (fun t : ℝ => f (unitSphereExp w (t • z)))) 0 ≤ 0 := by
  exact IsLocalMax.deriv_deriv_nonpos_of_continuousAt
    (unitSphere_isMaxOn_expCurve_isLocalMax hw hz hmax) hc

/-- A trace written as a finite sum of exponential-curve second derivatives is
nonnegative at a global minimum on the unit sphere. -/
theorem unitSphere_isMinOn_laplacian_nonneg
    {ι : Type*} [Fintype ι] {f : E → ℝ} {w : E}
    (directions : ι → E) (diagonal : ι → ℝ) (laplacian : ℝ)
    (hw : ‖w‖ = 1)
    (htangent : ∀ i, ⟪w, directions i⟫_ℝ = 0)
    (hmin : IsMinOn f (Metric.sphere (0 : E) 1) w)
    (hcontinuous : ∀ i, ContinuousAt
      (fun t : ℝ => f (unitSphereExp w (t • directions i))) 0)
    (hdiagonal : ∀ i, diagonal i =
      deriv (deriv (fun t : ℝ =>
        f (unitSphereExp w (t • directions i)))) 0)
    (htrace : laplacian = ∑ i, diagonal i) :
    0 ≤ laplacian := by
  rw [htrace]
  exact Finset.sum_nonneg fun i _ => by
    rw [hdiagonal i]
    exact unitSphere_isMinOn_expCurve_deriv_deriv_nonneg
      hw (htangent i) hmin (hcontinuous i)

/-- A trace written as a finite sum of exponential-curve second derivatives is
nonpositive at a global maximum on the unit sphere. -/
theorem unitSphere_isMaxOn_laplacian_nonpos
    {ι : Type*} [Fintype ι] {f : E → ℝ} {w : E}
    (directions : ι → E) (diagonal : ι → ℝ) (laplacian : ℝ)
    (hw : ‖w‖ = 1)
    (htangent : ∀ i, ⟪w, directions i⟫_ℝ = 0)
    (hmax : IsMaxOn f (Metric.sphere (0 : E) 1) w)
    (hcontinuous : ∀ i, ContinuousAt
      (fun t : ℝ => f (unitSphereExp w (t • directions i))) 0)
    (hdiagonal : ∀ i, diagonal i =
      deriv (deriv (fun t : ℝ =>
        f (unitSphereExp w (t • directions i)))) 0)
    (htrace : laplacian = ∑ i, diagonal i) :
    laplacian ≤ 0 := by
  rw [htrace]
  exact Finset.sum_nonpos fun i _ => by
    rw [hdiagonal i]
    exact unitSphere_isMaxOn_expCurve_deriv_deriv_nonpos
      hw (htangent i) hmax (hcontinuous i)

end

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereSecondOrder
