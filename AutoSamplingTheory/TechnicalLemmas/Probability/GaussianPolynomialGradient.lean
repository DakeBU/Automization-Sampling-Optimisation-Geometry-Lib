import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Tactic
open MeasureTheory ProbabilityTheory Filter
open scoped InnerProductSpace ENNReal
noncomputable section
namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient

theorem gaussian_polynomial_joint_potential_projected_gradient_transport_control
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hGaussian : P.map Prod.fst = ProbabilityTheory.stdGaussian E)
    (p : Polynomial ℝ) (hlabel : MemLp (fun z : E × ℝ => z.2) 2 P) :
    let S := {w : E // ‖w‖ = 1}
    let predictor : Measure S → E → ℝ := fun μ x => ∫ w, p.eval ⟪w.1,x⟫_ℝ ∂μ
    let V : Measure S → E → ℝ := fun μ w =>
      2 * ∫ z, (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ ∂P
    let grad : Measure S → E → E := fun μ w => gradient (V μ) w
    let G : Measure S → E → E := fun μ w => grad μ w-⟪grad μ w,w⟫_ℝ • w
    let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
    let Q : Measure S → Measure S → ℝ≥0∞ := fun μ ν =>
      AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
        (fun z => ENNReal.ofReal ((c z)^2)) μ ν
    ∃ C₁ C₂ : ℝ, 0 < C₁ ∧ 0 < C₂ ∧
      (∀ μ : Measure S, IsProbabilityMeasure μ →
        (∀ w : E, Integrable (fun z : E × ℝ =>
            (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ) P ∧
          HasGradientAt (V μ) (grad μ w) w) ∧
        ∀ w : S, ⟪w.1,G μ w.1⟫_ℝ = 0 ∧ ‖G μ w.1‖ ≤ C₁) ∧
      ∀ μ ν : Measure S, IsProbabilityMeasure μ → IsProbabilityMeasure ν →
        Q μ ν ≠ ∞ ∧ ∀ w u : S,
          ‖G μ w.1-G ν u.1‖ ≤
            C₂*((Q μ ν ^ (1 / 2 : ℝ)).toReal+c (w,u)) := by
  classical
  let : CompleteSpace E := FiniteDimensional.complete ℝ E
  dsimp only
  let S := {w : E // ‖w‖ = 1}
  let predictor : Measure S → E → ℝ := fun μ x => ∫ w, p.eval ⟪w.1,x⟫_ℝ ∂μ
  let V : Measure S → E → ℝ := fun μ w =>
    2 * ∫ z, (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ ∂P
  let grad : Measure S → E → E := fun μ w => gradient (V μ) w
  let G : Measure S → E → E := fun μ w => grad μ w-⟪grad μ w,w⟫_ℝ • w
  let c : S × S → ℝ := fun z => Real.arccos ⟪z.1.1,z.2.1⟫_ℝ
  let Q : Measure S → Measure S → ℝ≥0∞ := fun μ ν =>
    AutoSamplingTheory.TechnicalLemmas.Measure.Transport.transportCost
      (fun z => ENNReal.ofReal ((c z)^2)) μ ν
  change ∃ C₁ C₂ : ℝ, 0 < C₁ ∧ 0 < C₂ ∧
      (∀ μ : Measure S, IsProbabilityMeasure μ →
        (∀ w : E, Integrable (fun z : E × ℝ =>
            (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ) P ∧
          HasGradientAt (V μ) (grad μ w) w) ∧
        ∀ w : S, ⟪w.1,G μ w.1⟫_ℝ = 0 ∧ ‖G μ w.1‖ ≤ C₁) ∧
      ∀ μ ν : Measure S, IsProbabilityMeasure μ → IsProbabilityMeasure ν →
        Q μ ν ≠ ∞ ∧ ∀ w u : S,
          ‖G μ w.1-G ν u.1‖ ≤
            C₂*((Q μ ν ^ (1 / 2 : ℝ)).toReal+c (w,u))
  obtain ⟨hf,hdf,D,M₁,M₂,hM₁,hM₂,hD,hF,hB,hL,hrepr⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient.gaussian_polynomial_joint_feature_gradient_representation
      P hGaussian p hlabel
  let F : E → Lp ℝ 2 P := fun w => (hf w).toLp (fun z => p.eval ⟪w,z.1⟫_ℝ)
  let label : Lp ℝ 2 P := hlabel.toLp (fun z : E × ℝ => z.2)
  let mean : Measure S → Lp ℝ 2 P := fun μ => ∫ w : S, F w.1 ∂μ
  have hG (μ : Measure S) (hμ : IsProbabilityMeasure μ) (w : S) :
      G μ w.1 = (2 : ℝ) • ((D w.1).adjoint (mean μ-label) -
        ⟪(D w.1).adjoint (mean μ-label),w.1⟫_ℝ • w.1) := by
    exact (hrepr μ hμ).2.2.2.2.2 w
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
      F D hF M₁ M₂ hM₁.le hM₂.le hB hL label
  refine ⟨C₁,C₂,hC₁,hC₂,?_,?_⟩
  · intro μ hμ
    obtain ⟨_,_,_,_,hgrad,_⟩ := hrepr μ hμ
    refine ⟨?_,?_⟩
    · intro w
      refine ⟨(hgrad w).1,?_⟩
      change HasGradientAt (V μ) (gradient (V μ) w) w
      rw [(hgrad w).2.2]
      exact (hgrad w).2.1
    · intro w
      rw [hG μ hμ w]
      exact (hpoint μ hμ).2.2 w
  · intro μ ν hμ hν
    refine ⟨(hlaw μ ν hμ hν).1,?_⟩
    intro w u
    rw [hG μ hμ w,hG ν hν u]
    exact (hlaw μ ν hμ hν).2 w u

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient
