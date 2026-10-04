import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereSecondOrder

open scoped InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere
open AutoSamplingTheory.TechnicalLemmas.Geometry.SphereSecondOrder

example {f : ℝ → ℝ} {x : ℝ} (hmin : IsLocalMin f x)
    (hc : ContinuousAt f x) :
    0 ≤ deriv (deriv f) x :=
  hmin.deriv_deriv_nonneg_of_continuousAt hc

example {f : ℝ → ℝ} {x : ℝ} (hmax : IsLocalMax f x)
    (hc : ContinuousAt f x) :
    deriv (deriv f) x ≤ 0 :=
  hmax.deriv_deriv_nonpos_of_continuousAt hc

example {ι E : Type*} [Fintype ι]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {f : E → ℝ} {w : E}
    (directions : ι → E) (diagonal : ι → ℝ) (laplacian : ℝ)
    (hw : ‖w‖ = 1) (htangent : ∀ i, ⟪w, directions i⟫_ℝ = 0)
    (hmin : IsMinOn f (Metric.sphere (0 : E) 1) w)
    (hcontinuous : ∀ i, ContinuousAt
      (fun t : ℝ => f (unitSphereExp w (t • directions i))) 0)
    (hdiagonal : ∀ i, diagonal i =
      deriv (deriv (fun t : ℝ =>
        f (unitSphereExp w (t • directions i)))) 0)
    (htrace : laplacian = ∑ i, diagonal i) :
    0 ≤ laplacian :=
  unitSphere_isMinOn_laplacian_nonneg directions diagonal laplacian
    hw htangent hmin hcontinuous hdiagonal htrace

example {ι E : Type*} [Fintype ι]
    [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {f : E → ℝ} {w : E}
    (directions : ι → E) (diagonal : ι → ℝ) (laplacian : ℝ)
    (hw : ‖w‖ = 1) (htangent : ∀ i, ⟪w, directions i⟫_ℝ = 0)
    (hmax : IsMaxOn f (Metric.sphere (0 : E) 1) w)
    (hcontinuous : ∀ i, ContinuousAt
      (fun t : ℝ => f (unitSphereExp w (t • directions i))) 0)
    (hdiagonal : ∀ i, diagonal i =
      deriv (deriv (fun t : ℝ =>
        f (unitSphereExp w (t • directions i)))) 0)
    (htrace : laplacian = ∑ i, diagonal i) :
    laplacian ≤ 0 :=
  unitSphere_isMaxOn_laplacian_nonpos directions diagonal laplacian
    hw htangent hmax hcontinuous hdiagonal htrace
