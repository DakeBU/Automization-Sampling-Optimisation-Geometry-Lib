import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient
import AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport
import AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereAngularCost
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.MeasureTheory.Function.StronglyMeasurable.Basic
import Mathlib.Tactic

open MeasureTheory
open scoped InnerProductSpace ENNReal
namespace AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient
theorem quadratic_feature_law_gradient_angular_transport_control
    {E H : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (F : E → H) (D : E → E →L[ℝ] H)
    (hF : ∀ w, HasFDerivAt F (D w) w)
    (M₁ M₂ : ℝ) (hM₁ : 0 ≤ M₁) (hM₂ : 0 ≤ M₂)
    (hBound : ∀ w : E, ‖w‖ ≤ 1 → ‖D w‖ ≤ M₁)
    (hLip : ∀ w u : E, ‖w‖ ≤ 1 → ‖u‖ ≤ 1 → ‖D w-D u‖ ≤ M₂*‖w-u‖)
    (y : H) :
    let S := {w : E // ‖w‖ = 1}
    let K : S → H := fun w => F w.1
    let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
    let m : Measure S → H := fun μ => ∫ w, K w ∂μ
    let V : Measure S → E → ℝ := fun μ w => 2 * ⟪m μ-y,F w⟫_ℝ
    let G : Measure S → E → E := fun μ w =>
      (2 : ℝ) • ((D w).adjoint (m μ-y) - ⟪(D w).adjoint (m μ-y),w⟫_ℝ • w)
    let Q : Measure S → Measure S → ℝ≥0∞ := fun μ ν =>
      AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
        (fun z => ENNReal.ofReal ((c z)^2)) μ ν
    ∃ C₁ C₂ : ℝ, 0 < C₁ ∧ 0 < C₂ ∧
      (∀ μ : Measure S, IsProbabilityMeasure μ →
        Integrable K μ ∧
        (∀ w : E, HasGradientAt (V μ) ((2 : ℝ) • (D w).adjoint (m μ-y)) w) ∧
        ∀ w : S, ⟪w.1,G μ w.1⟫_ℝ = 0 ∧ ‖G μ w.1‖ ≤ C₁) ∧
      ∀ μ ν : Measure S, IsProbabilityMeasure μ → IsProbabilityMeasure ν →
        Q μ ν ≠ ∞ ∧ ∀ w u : S,
          ‖G μ w.1-G ν u.1‖ ≤
            C₂ * ((Q μ ν ^ (1 / 2 : ℝ)).toReal + c (w,u)) := by
  let : SecondCountableTopology E := inferInstance
  let S := {w : E // ‖w‖ = 1}
  let K : S → H := fun w => F w.1
  let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
  let m : Measure S → H := fun μ => ∫ w, K w ∂μ
  let V : Measure S → E → ℝ := fun μ w => 2 * ⟪m μ-y,F w⟫_ℝ
  let G : Measure S → E → E := fun μ w =>
    (2 : ℝ) • ((D w).adjoint (m μ-y) - ⟪(D w).adjoint (m μ-y),w⟫_ℝ • w)
  let Q : Measure S → Measure S → ℝ≥0∞ := fun μ ν =>
    AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
      (fun z => ENNReal.ofReal ((c z)^2)) μ ν
  change ∃ C₁ C₂ : ℝ, 0 < C₁ ∧ 0 < C₂ ∧
    (∀ μ : Measure S, IsProbabilityMeasure μ →
      Integrable K μ ∧
      (∀ w : E, HasGradientAt (V μ) ((2 : ℝ) • (D w).adjoint (m μ-y)) w) ∧
      ∀ w : S, ⟪w.1,G μ w.1⟫_ℝ = 0 ∧ ‖G μ w.1‖ ≤ C₁) ∧
    ∀ μ ν : Measure S, IsProbabilityMeasure μ → IsProbabilityMeasure ν →
      Q μ ν ≠ ∞ ∧ ∀ w u : S,
        ‖G μ w.1-G ν u.1‖ ≤ C₂ * ((Q μ ν ^ (1 / 2 : ℝ)).toReal + c (w,u))
  have hFc : Continuous F := continuous_iff_continuousAt.mpr fun w => (hF w).continuousAt
  have hKsm : StronglyMeasurable K := (hFc.comp continuous_subtype_val).stronglyMeasurable
  have hChord (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) :
      ‖F w-F u‖ ≤ M₁*‖w-u‖ := by
    apply (convex_closedBall (0 : E) 1).norm_image_sub_le_of_norm_hasFDerivWithin_le
      (fun z _ => (hF z).hasFDerivWithinAt) ?_
      (by simpa [Metric.mem_closedBall,dist_zero_right] using hu)
      (by simpa [Metric.mem_closedBall,dist_zero_right] using hw)
    intro z hz
    exact hBound z (by simpa [Metric.mem_closedBall,dist_zero_right] using hz)
  let B := ‖F (0:E)‖+M₁+1
  have hB : 0 ≤ B := by dsimp [B]; positivity
  have hKb (w : S) : ‖K w‖ ≤ B := by
    have hb := hChord w.1 0 w.property.le (by simp)
    have hn := norm_add_le (F w.1-F 0) (F 0)
    rw [sub_add_cancel] at hn
    simp only [sub_zero,w.property,mul_one] at hb
    change ‖F w.1‖ ≤ B
    dsimp [B]
    linarith
  have hAng := AutoSamplingTheory.TechnicalLemmas.Geometry.UnitSphereAngularCost.unit_sphere_angular_cost_properties (E := E)
  change Continuous c ∧ Measurable c ∧
    (∀ u v : S, 0 ≤ c (u,v) ∧ c (u,v) ≤ Real.pi ∧
      c (u,v) = InnerProductGeometry.angle u.1 v.1 ∧ ‖u.1-v.1‖ ≤ c (u,v) ∧
      (c (u,v) = 0 ↔ u = v) ∧ c (u,v) = c (v,u)) ∧
    ∀ u v w : S, c (u,w) ≤ c (u,v)+c (v,w) at hAng
  have hc0 (z : S × S) : 0 ≤ c z := (hAng.2.2.1 z.1 z.2).1
  have hcB (z : S × S) : c z ≤ Real.pi := (hAng.2.2.1 z.1 z.2).2.1
  have hKlip (w u : S) : ‖K w-K u‖ ≤ M₁*c (w,u) :=
    (hChord w.1 u.1 w.property.le u.property.le).trans
      (mul_le_mul_of_nonneg_left (hAng.2.2.1 w u).2.2.2.1 hM₁)
  have hMean (μ ν : Measure S) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν] :=
    AutoSamplingTheory.TechnicalLemmas.Measure.BochnerMeanTransport.bounded_bochner_mean_quadratic_transport_control
      K hKsm B Real.pi M₁ hB Real.pi_pos.le hM₁ hKb c hAng.2.1 hc0 hcB hKlip μ ν
  have hTangent :=
    AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient.quadratic_feature_potential_tangent_gradient
      F D hF M₁ M₂ hM₁ hM₂ hBound hLip
  let R₀ := B+‖y‖
  have hR₀ : 0 ≤ R₀ := add_nonneg hB (norm_nonneg y)
  have hResidual (μ : Measure S) [IsProbabilityMeasure μ] : ‖m μ-y‖ ≤ R₀ :=
    ((hMean μ μ).2.2.2.2 y).1
  have hGrad (μ : Measure S) (w : E) :
      HasGradientAt (V μ) ((2 : ℝ) • (D w).adjoint (m μ-y)) w := by
    rw [hasGradientAt_iff_hasFDerivAt]
    have he : InnerProductSpace.toDual ℝ E ((2 : ℝ) • (D w).adjoint (m μ-y)) =
        (2 : ℝ) • innerSL ℝ ((D w).adjoint (m μ-y)) := by
      ext v
      simp [InnerProductSpace.toDual_apply_apply,innerSL_apply_apply]
    rw [he]
    exact hTangent.1 (m μ-y) w
  let A := 2*M₁^2
  let B₂ := 2*(M₂+2*M₁)*R₀
  have hA : 0 ≤ A := by dsimp [A]; positivity
  have hB₂ : 0 ≤ B₂ := by dsimp [B₂]; positivity
  refine ⟨2*M₁*R₀+1,A+B₂+1,by positivity,by positivity,?_,?_⟩
  · intro μ hμ
    let : IsProbabilityMeasure μ := hμ
    refine ⟨(hMean μ μ).1,hGrad μ,?_⟩
    intro w
    have ht := hTangent.2.1 (m μ-y) w.1 w.property
    refine ⟨ht.1,?_⟩
    exact ht.2.2.trans ((mul_le_mul_of_nonneg_left (hResidual μ) (by positivity)).trans (by linarith))
  · intro μ ν hμ hν
    let : IsProbabilityMeasure μ := hμ
    let : IsProbabilityMeasure ν := hν
    refine ⟨(hMean μ ν).2.2.1,?_⟩
    intro w u
    have hm : ‖(m μ-y)-(m ν-y)‖ ≤ M₁*(Q μ ν ^ (1 / 2 : ℝ)).toReal := by
      simpa only [sub_sub_sub_cancel_right] using (hMean μ ν).2.2.2.1
    have hr := hResidual ν
    have ht := hTangent.2.2 (m μ-y) (m ν-y) w.1 u.1 w.property u.property
    have hpoint := (hAng.2.2.1 w u).2.2.2.1
    have ht' : ‖G μ w.1-G ν u.1‖ ≤
        A*(Q μ ν ^ (1 / 2 : ℝ)).toReal+B₂*c (w,u) := by
      calc
        _ ≤ 2*M₁*‖(m μ-y)-(m ν-y)‖+
            2*(M₂+2*M₁)*‖m ν-y‖*‖w.1-u.1‖ := ht
        _ ≤ 2*M₁*(M₁*(Q μ ν ^ (1 / 2 : ℝ)).toReal)+
            2*(M₂+2*M₁)*R₀*c (w,u) := by
          gcongr
        _ = _ := by dsimp [A,B₂]; ring
    apply ht'.trans
    have hs : 0 ≤ (Q μ ν ^ (1 / 2 : ℝ)).toReal := ENNReal.toReal_nonneg
    have hc := hc0 (w,u)
    nlinarith [mul_nonneg hA hc,mul_nonneg hB₂ hs]

end AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient
