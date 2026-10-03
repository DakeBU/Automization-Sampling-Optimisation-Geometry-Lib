import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere

open scoped InnerProductSpace

open AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphere

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {w z : E} (hw : ‖w‖ = 1) (htan : ⟪w, z⟫_ℝ = 0) :
    ‖unitSphereExp w z‖ = 1 :=
  unitSphereExp_norm_eq_one hw htan

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {w z : E} (hw : ‖w‖ = 1) (hz : z ≠ 0) (t : ℝ) :
    ‖(‖z‖ ^ (4 : ℕ) * Real.cos (t * ‖z‖)) • w +
        (‖z‖ ^ (3 : ℕ) * Real.sin (t * ‖z‖)) • z‖ ≤
      2 * ‖z‖ ^ (4 : ℕ) :=
  (unitSphereGeodesic_derivatives_and_bounds hw hz t).2.2.2.2
