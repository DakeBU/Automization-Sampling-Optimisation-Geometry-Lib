import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
import AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open MeasureTheory ProbabilityTheory
open scoped InnerProductSpace ENNReal

noncomputable section
namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient

theorem gaussian_polynomial_joint_feature_gradient_representation
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hGaussian : P.map Prod.fst = ProbabilityTheory.stdGaussian E)
    (p : Polynomial ℝ) (hlabel : MemLp (fun z : E × ℝ => z.2) 2 P) :
    let S := {w : E // ‖w‖ = 1}
    let f : E → E × ℝ → ℝ := fun w z => p.eval ⟪w,z.1⟫_ℝ
    let df : E → E → E × ℝ → ℝ := fun w v z =>
      p.derivative.eval ⟪w,z.1⟫_ℝ * ⟪v,z.1⟫_ℝ
    let predictor : Measure S → E → ℝ := fun ρ x =>
      ∫ w : S, p.eval ⟪w.1,x⟫_ℝ ∂ρ
    let V : Measure S → E → ℝ := fun ρ w =>
      2 * ∫ z : E × ℝ, (predictor ρ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ ∂P
    ∃ hf : ∀ w : E, MemLp (f w) 2 P,
    ∃ hdf : ∀ w v : E, MemLp (df w v) 2 P,
    ∃ D : E → E →L[ℝ] Lp ℝ 2 P,
    ∃ M₁ M₂ : ℝ,
      let F : E → Lp ℝ 2 P := fun w => (hf w).toLp (f w)
      let label : Lp ℝ 2 P := hlabel.toLp (fun z : E × ℝ => z.2)
      let K : S → Lp ℝ 2 P := fun w => F w.1
      let mean : Measure S → Lp ℝ 2 P := fun ρ => ∫ w : S, K w ∂ρ
      let G : Measure S → E → E := fun ρ w =>
        gradient (V ρ) w-⟪gradient (V ρ) w,w⟫_ℝ • w
      0 < M₁ ∧ 0 < M₂ ∧
      (∀ w v : E, D w v = (hdf w v).toLp (df w v)) ∧
      (∀ w : E, HasFDerivAt F (D w) w) ∧
      (∀ w : E, ‖w‖ ≤ 1 → ‖D w‖ ≤ M₁) ∧
      (∀ w u : E, ‖w‖ ≤ 1 → ‖u‖ ≤ 1 →
        ‖D w-D u‖ ≤ M₂*‖w-u‖) ∧
      ∀ ρ : Measure S, IsProbabilityMeasure ρ →
        (∀ x : E, Integrable (fun w : S => p.eval ⟪w.1,x⟫_ℝ) ρ) ∧
        Integrable K ρ ∧
        (∃ hpred : MemLp (fun z : E × ℝ => predictor ρ z.1) 2 P,
          hpred.toLp (fun z : E × ℝ => predictor ρ z.1) = mean ρ) ∧
        (V ρ = fun w : E => 2 * ⟪mean ρ-label,F w⟫_ℝ) ∧
        (∀ w : E,
          Integrable (fun z : E × ℝ =>
            (predictor ρ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ) P ∧
          HasGradientAt (V ρ) ((2 : ℝ) • (D w).adjoint (mean ρ-label)) w ∧
          gradient (V ρ) w = (2 : ℝ) • (D w).adjoint (mean ρ-label)) ∧
        ∀ w : S,
          G ρ w.1 = (2 : ℝ) • ((D w.1).adjoint (mean ρ-label) -
            ⟪(D w.1).adjoint (mean ρ-label),w.1⟫_ℝ • w.1) := by
  classical
  let : CompleteSpace E := FiniteDimensional.complete ℝ E
  dsimp only
  let S := {w : E // ‖w‖ = 1}
  let predictor : Measure S → E → ℝ := fun μ x => ∫ w, p.eval ⟪w.1,x⟫_ℝ ∂μ
  let V : Measure S → E → ℝ := fun μ w =>
    2 * ∫ z, (predictor μ z.1-z.2)*p.eval ⟪w,z.1⟫_ℝ ∂P
  obtain ⟨hf,hdf,D,hD,hDiff,M₁,M₂,hM₁,hM₂,hBound,hLip⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialDifferentiation.actual_gaussian_polynomial_ridge_L2_derivative_bounds (E := E) p
  have hmarg : MeasurePreserving (Prod.fst : E × ℝ → E) P (stdGaussian E) :=
    ⟨measurable_fst,hGaussian⟩
  let J : Lp ℝ 2 (stdGaussian E) →ₗᵢ[ℝ] Lp ℝ 2 P :=
    Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hmarg
  let T : Lp ℝ 2 (stdGaussian E) →L[ℝ] Lp ℝ 2 P := J.toContinuousLinearMap
  let hfP : ∀ w : E, MemLp (fun z : E × ℝ => p.eval ⟪w,z.1⟫_ℝ) 2 P :=
    fun w => (hf w).comp_measurePreserving hmarg
  let hdfP : ∀ w v : E,
      MemLp (fun z : E × ℝ => p.derivative.eval ⟪w,z.1⟫_ℝ * ⟪v,z.1⟫_ℝ) 2 P :=
    fun w v => (hdf w v).comp_measurePreserving hmarg
  let F : E → Lp ℝ 2 P := fun w => (hfP w).toLp (fun z => p.eval ⟪w,z.1⟫_ℝ)
  let DP : E → E →L[ℝ] Lp ℝ 2 P := fun w => T.comp (D w)
  have hDP (w v : E) : DP w v =
      (hdfP w v).toLp (fun z => p.derivative.eval ⟪w,z.1⟫_ℝ * ⟪v,z.1⟫_ℝ) := by
    change T (D w v) = _
    rw [hD w v]
    rfl
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
  obtain ⟨hfS,hcont,havg⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging.gaussian_polynomial_parameter_average_L2 (E := E) p
  have hKint (μ : Measure S) (hμ : IsProbabilityMeasure μ) : Integrable K μ := by
    exact T.integrable_comp (havg μ hμ).2.1
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
  have hTangent :=
    AutoSamplingTheory.TechnicalLemmas.Geometry.QuadraticFeatureTangentGradient.quadratic_feature_potential_tangent_gradient
      F DP hFP M₁ M₂ hM₁.le hM₂.le hPB hPL
  have hGrad (μ : Measure S) (hμ : IsProbabilityMeasure μ) (w : E) :
      HasGradientAt (V μ) ((2 : ℝ) • (DP w).adjoint (mean μ-label)) w := by
    rw [hPot μ hμ,hasGradientAt_iff_hasFDerivAt]
    have he : InnerProductSpace.toDual ℝ E ((2 : ℝ) • (DP w).adjoint (mean μ-label)) =
        (2 : ℝ) • innerSL ℝ ((DP w).adjoint (mean μ-label)) := by
      ext v
      simp [InnerProductSpace.toDual_apply_apply,innerSL_apply_apply]
    rw [he]
    exact hTangent.1 (mean μ-label) w
  refine ⟨hfP,hdfP,DP,M₁,M₂,hM₁,hM₂,hDP,hFP,hPB,hPL,?_⟩
  intro μ hμ
  refine ⟨(havg μ hμ).1,hKint μ hμ,hMeanClass μ hμ,hPot μ hμ,?_,?_⟩
  · intro w
    obtain ⟨hpred,hident⟩ := hMeanClass μ hμ
    exact ⟨(hpred.sub hlabel).integrable_mul (hfP w),hGrad μ hμ w,(hGrad μ hμ w).gradient⟩
  · intro w
    change gradient (V μ) w.1 - ⟪gradient (V μ) w.1,w.1⟫_ℝ • w.1 = _
    rw [(hGrad μ hμ w.1).gradient]
    simp only [smul_sub,real_inner_smul_left,smul_smul]
    rfl

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialFeatureGradient
