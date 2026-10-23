import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereAngularCost
import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient

open MeasureTheory
open scoped InnerProductSpace ENNReal
open AutoSamplingTheory.TechnicalLemmas.Geometry

-- The two-point unit sphere still has finite angular cost pi at antipodes.
example :
    let u : {w : ℝ // ‖w‖ = 1} := ⟨1, by norm_num⟩
    let v : {w : ℝ // ‖w‖ = 1} := ⟨-1, by norm_num⟩
    Real.arccos ⟪u.1,v.1⟫_ℝ = Real.pi ∧
      ‖u.1-v.1‖ ≤ Real.arccos ⟪u.1,v.1⟫_ℝ := by
  dsimp only
  have h := UnitSphereAngularCost.unit_sphere_angular_cost_properties (E := ℝ)
  constructor
  · norm_num [Real.inner_apply]
  · exact (h.2.2.1 ⟨1, by norm_num⟩ ⟨-1, by norm_num⟩).2.2.2.1

-- Real identity features: the derivative hypotheses are supplied, not assumed.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (y : E) (μ : Measure {w : E // ‖w‖ = 1}) [IsProbabilityMeasure μ] (w : E) :
    HasGradientAt (fun z : E => 2 * ⟪(∫ u, u.1 ∂μ)-y,z⟫_ℝ)
      ((2 : ℝ) • ((∫ u, u.1 ∂μ)-y)) w := by
  have h := QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
    (E := E) (H := E) id (fun _ => ContinuousLinearMap.id ℝ E)
    (fun z => hasFDerivAt_id z) 1 0 (by norm_num) (by norm_num)
    (by intro z hz; exact ContinuousLinearMap.norm_id_le) (by intro z u hz hu; simp) y
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ := h
  simpa only [id_eq, ContinuousLinearMap.adjoint_id, ContinuousLinearMap.id_apply] using
    (hpoint μ inferInstance).2.1 w

-- Actual all-coupling law sensitivity, with every analytic premise discharged.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] (y : E) :
    let S := {w : E // ‖w‖ = 1}
    let m : Measure S → E := fun μ => ∫ w, w.1 ∂μ
    let G : Measure S → E → E := fun μ w =>
      (2 : ℝ) • ((m μ-y) - ⟪m μ-y,w⟫_ℝ • w)
    let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
    let Q := fun μ ν => AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
      (fun z => ENNReal.ofReal ((c z)^2)) μ ν
    ∃ C : ℝ, 0 < C ∧ ∀ μ ν : Measure S,
      IsProbabilityMeasure μ → IsProbabilityMeasure ν →
      Q μ ν ≠ ∞ ∧ ∀ w u : S,
        ‖G μ w.1-G ν u.1‖ ≤ C*((Q μ ν ^ (1 / 2 : ℝ)).toReal+c (w,u)) := by
  have h := QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
    (E := E) (H := E) id (fun _ => ContinuousLinearMap.id ℝ E)
    (fun z => hasFDerivAt_id z) 1 0 (by norm_num) (by norm_num)
    (by intro z hz; exact ContinuousLinearMap.norm_id_le) (by intro z u hz hu; simp) y
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ := h
  refine ⟨C₂,hC₂,?_⟩
  simpa only [id_eq, ContinuousLinearMap.adjoint_id, ContinuousLinearMap.id_apply] using hlaw

-- Constant features are allowed with both derivative budgets zero.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (a y : ℝ) (μ : Measure {w : E // ‖w‖ = 1}) [IsProbabilityMeasure μ] (w : E) :
    HasGradientAt (fun _ : E => 2 * ⟪(∫ _ : {w : E // ‖w‖ = 1}, a ∂μ)-y,a⟫_ℝ)
      (0 : E) w := by
  have h := QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
    (E := E) (H := ℝ) (fun _ => a) (fun _ => 0)
    (fun z => hasFDerivAt_const a z) 0 0 (by norm_num) (by norm_num)
    (by intro z hz; simp) (by intro z u hz hu; simp) y
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ := h
  simpa using (hpoint μ inferInstance).2.1 w
