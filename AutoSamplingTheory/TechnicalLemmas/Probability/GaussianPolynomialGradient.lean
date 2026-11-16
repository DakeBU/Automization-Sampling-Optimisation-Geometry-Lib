import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
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
  obtain ⟨hf,hdf,D,hD,hDiff,M₁,M₂,hM₁,hM₂,hBound,hLip⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation.actual_gaussian_polynomial_ridge_L2_derivative_bounds (E := E) p
  have hmarg : MeasurePreserving (Prod.fst : E × ℝ → E) P (stdGaussian E) :=
    ⟨measurable_fst,hGaussian⟩
  let J : Lp ℝ 2 (stdGaussian E) →ₗᵢ[ℝ] Lp ℝ 2 P :=
    Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hmarg
  let T : Lp ℝ 2 (stdGaussian E) →L[ℝ] Lp ℝ 2 P := J.toContinuousLinearMap
  let hfP : ∀ w : E, MemLp (fun z : E × ℝ => p.eval ⟪w,z.1⟫_ℝ) 2 P :=
    fun w => (hf w).comp_measurePreserving hmarg
  let F : E → Lp ℝ 2 P := fun w => (hfP w).toLp (fun z => p.eval ⟪w,z.1⟫_ℝ)
  let DP : E → E →L[ℝ] Lp ℝ 2 P := fun w => T.comp (D w)
  have hFeq (w : E) : F w = T ((hf w).toLp (fun x => p.eval ⟪w,x⟫_ℝ)) := rfl
  have hFP (w : E) : HasFDerivAt F (DP w) w := by
    have he : F = fun u => T ((hf u).toLp (fun x => p.eval ⟪u,x⟫_ℝ)) := funext hFeq
    rw [he]
    exact T.hasFDerivAt.comp w (hDiff w)
  have hPB (w : E) (hw : ‖w‖ ≤ 1) : ‖DP w‖ ≤ M₁ := by
    apply ContinuousLinearMap.opNorm_le_bound _ hM₁.le
    intro v
    change ‖J (D w v)‖ ≤ M₁*‖v‖
    rw [J.norm_map]
    exact ((D w).le_opNorm v).trans (mul_le_mul_of_nonneg_right (hBound w hw) (norm_nonneg v))
  have hPL (w u : E) (hw : ‖w‖ ≤ 1) (hu : ‖u‖ ≤ 1) :
      ‖DP w-DP u‖ ≤ M₂*‖w-u‖ := by
    apply ContinuousLinearMap.opNorm_le_bound _ (mul_nonneg hM₂.le (norm_nonneg _))
    intro v
    change ‖T (D w v)-T (D u v)‖ ≤ (M₂*‖w-u‖)*‖v‖
    rw [← map_sub]
    change ‖J ((D w-D u) v)‖ ≤ (M₂*‖w-u‖)*‖v‖
    rw [J.norm_map]
    exact ((D w-D u).le_opNorm v).trans
      (mul_le_mul_of_nonneg_right (hLip u w hu hw) (norm_nonneg v))
  let label : Lp ℝ 2 P := hlabel.toLp (fun z : E × ℝ => z.2)
  let K : S → Lp ℝ 2 P := fun w => F w.1
  let mean : Measure S → Lp ℝ 2 P := fun μ => ∫ w, K w ∂μ
  obtain ⟨C₁,C₂,hC₁,hC₂,hpoint,hlaw⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureLawGradient.quadratic_feature_law_gradient_angular_transport_control
      F DP hFP M₁ M₂ hM₁.le hM₂.le hPB hPL label
  obtain ⟨hfS,hcont,havg⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging.gaussian_polynomial_parameter_average_L2 (E := E) p
  have hMeanClass (μ : Measure S) (hμ : IsProbabilityMeasure μ) :
      ∃ hpred : MemLp (fun z : E × ℝ => predictor μ z.1) 2 P,
        hpred.toLp (fun z => predictor μ z.1) = mean μ := by
    obtain ⟨hscalar,hint,hmean,hident⟩ := havg μ hμ
    let hpred : MemLp (fun z : E × ℝ => predictor μ z.1) 2 P :=
      hmean.comp_measurePreserving hmarg
    refine ⟨hpred,?_⟩
    calc
      hpred.toLp (fun z => predictor μ z.1) = T (hmean.toLp (predictor μ)) := rfl
      _ = T (∫ w, (hfS w).toLp (fun x => p.eval ⟪w.1,x⟫_ℝ) ∂μ) := congrArg T hident
      _ = mean μ := (T.integral_comp_comm hint).symm
  have hMeanAE (μ : Measure S) (hμ : IsProbabilityMeasure μ) :
      (fun z => mean μ z) =ᵐ[P] (fun z : E × ℝ => predictor μ z.1) := by
    obtain ⟨hpred,hident⟩ := hMeanClass μ hμ
    rw [← hident]
    exact hpred.coeFn_toLp
  have hResidual (μ : Measure S) (hμ : IsProbabilityMeasure μ) :
      (fun z => (mean μ-label) z) =ᵐ[P] (fun z : E × ℝ => predictor μ z.1-z.2) := by
    filter_upwards [Lp.coeFn_sub (mean μ) label,hMeanAE μ hμ,hlabel.coeFn_toLp]
      with z hs hm hy
    simp only [Pi.sub_apply] at hs
    rw [hs,hm,hy]
  have hPot (μ : Measure S) (hμ : IsProbabilityMeasure μ) :
      V μ = fun w => 2 * ⟪mean μ-label,F w⟫_ℝ := by
    funext w
    change 2 * (∫ z, (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ ∂P) = _
    rw [L2.inner_def]
    congr 1
    apply integral_congr_ae
    filter_upwards [hResidual μ hμ,(hfP w).coeFn_toLp] with z hr hw
    change F w z = p.eval ⟪w,z.1⟫_ℝ at hw
    simp only [Real.inner_apply,hr,hw]
  have hGrad (μ : Measure S) (hμ : IsProbabilityMeasure μ) (w : E) :
      HasGradientAt (V μ) ((2 : ℝ) • (DP w).adjoint (mean μ-label)) w := by
    rw [hPot μ hμ]
    exact (hpoint μ hμ).2.1 w
  have hG (μ : Measure S) (hμ : IsProbabilityMeasure μ) (w : E) :
      G μ w = (2 : ℝ) • ((DP w).adjoint (mean μ-label) -
        ⟪(DP w).adjoint (mean μ-label),w⟫_ℝ • w) := by
    dsimp only [G,grad]
    rw [(hGrad μ hμ w).gradient]
    simp only [smul_sub,real_inner_smul_left,smul_smul]
  refine ⟨C₁,C₂,hC₁,hC₂,?_,?_⟩
  · intro μ hμ
    refine ⟨?_,?_⟩
    · intro w
      obtain ⟨hpred,hident⟩ := hMeanClass μ hμ
      refine ⟨(hpred.sub hlabel).integrable_mul (hfP w),?_⟩
      change HasGradientAt (V μ) (gradient (V μ) w) w
      rw [(hGrad μ hμ w).gradient]
      exact hGrad μ hμ w
    · intro w
      rw [hG μ hμ w.1]
      exact (hpoint μ hμ).2.2 w
  · intro μ ν hμ hν
    refine ⟨(hlaw μ ν hμ hν).1,?_⟩
    intro w u
    rw [hG μ hμ w.1,hG ν hν u.1]
    exact (hlaw μ ν hμ hν).2 w u

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialGradient
