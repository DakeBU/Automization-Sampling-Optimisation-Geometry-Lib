import Mathlib.Geometry.Euclidean.Angle.Unoriented.TriangleInequality
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.Tactic

open scoped InnerProductSpace
namespace AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereAngularCost

private theorem chord_le_angle
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    (u v : E) (hu : ‖u‖ = 1) (hv : ‖v‖ = 1) :
    ‖u-v‖ ≤ InnerProductGeometry.angle u v := by
  let θ := InnerProductGeometry.angle u v
  have hθ : 0 ≤ θ := InnerProductGeometry.angle_nonneg u v
  have hc : Real.cos θ = ⟪u,v⟫_ℝ := by
    simpa [θ,hu,hv] using InnerProductGeometry.cos_angle u v
  have heq : ‖u-v‖^2 = 2-2*Real.cos θ := by
    rw [norm_sub_sq_real,hu,hv,hc]
    ring
  have hh := Real.sin_sq_eq_half_sub (θ/2)
  have htwo : 2*(θ/2) = θ := by ring
  rw [htwo] at hh
  have hs := Real.sin_sq_le_sq (x := θ/2)
  change ‖u-v‖ ≤ θ
  nlinarith [norm_nonneg (u-v)]

theorem unit_sphere_angular_cost_properties
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
    let S := {w : E // ‖w‖ = 1}
    let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
    Continuous c ∧ Measurable c ∧
      (∀ u v : S, 0 ≤ c (u,v) ∧ c (u,v) ≤ Real.pi ∧
        c (u,v) = InnerProductGeometry.angle u.1 v.1 ∧
        ‖u.1-v.1‖ ≤ c (u,v) ∧
        (c (u,v) = 0 ↔ u = v) ∧ c (u,v) = c (v,u)) ∧
      ∀ u v w : S, c (u,w) ≤ c (u,v)+c (v,w) := by
  dsimp only
  letI : SecondCountableTopology E := inferInstance
  have heq (u v : {w : E // ‖w‖ = 1}) :
      Real.arccos ⟪u.1,v.1⟫_ℝ = InnerProductGeometry.angle u.1 v.1 := by
    simp [InnerProductGeometry.angle,u.property,v.property]
  have hc : Continuous (fun z : {w : E // ‖w‖ = 1} × {w : E // ‖w‖ = 1} =>
      Real.arccos ⟪z.1.1,z.2.1⟫_ℝ) := by fun_prop
  refine ⟨hc,hc.measurable,?_,?_⟩
  · intro u v
    have hchord : ‖u.1-v.1‖ ≤ Real.arccos ⟪u.1,v.1⟫_ℝ := by
      rw [heq]
      exact chord_le_angle u.1 v.1 u.property v.property
    refine ⟨Real.arccos_nonneg _,Real.arccos_le_pi _,heq u v,hchord,?_,?_⟩
    · constructor
      · intro hz
        apply Subtype.ext
        apply sub_eq_zero.mp
        apply norm_eq_zero.mp
        exact le_antisymm (by simpa only [hz] using hchord) (norm_nonneg _)
      · rintro rfl
        rw [heq]
        apply InnerProductGeometry.angle_self
        intro hz
        have hh := u.property
        rw [hz,norm_zero] at hh
        norm_num at hh
    · rw [heq,heq,InnerProductGeometry.angle_comm]
  · intro u v w
    rw [heq,heq,heq]
    exact InnerProductGeometry.angle_le_angle_add_angle u.1 v.1 w.1

end AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereAngularCost
