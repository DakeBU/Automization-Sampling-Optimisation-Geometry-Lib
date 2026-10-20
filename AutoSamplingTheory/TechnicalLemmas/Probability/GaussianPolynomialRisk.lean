import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
import AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal InnerProductSpace Topology

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRisk

theorem gaussian_polynomial_joint_risk_first_variation
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hGaussian : P.map Prod.fst = ProbabilityTheory.stdGaussian E)
    (p : Polynomial ℝ)
    (hlabel : MemLp (fun z : E × ℝ => z.2) 2 P) :
    let U := {w : E // ‖w‖ = 1}
    let predictor : Measure U → E → ℝ := fun rho x => ∫ w : U, p.eval ⟪w.1,x⟫_ℝ ∂rho
    let risk : Measure U → ℝ := fun rho => ∫ z, (predictor rho z.1 - z.2)^2 ∂P
    let potential : Measure U → U → ℝ := fun rho w =>
      2 * ∫ z, (predictor rho z.1 - z.2) * p.eval ⟪w.1,z.1⟫_ℝ ∂P
    (∀ rho : Measure U, IsProbabilityMeasure rho →
      Integrable (fun z : E × ℝ => (predictor rho z.1 - z.2)^2) P ∧
      ∀ w : U, Integrable (fun z : E × ℝ =>
        (predictor rho z.1 - z.2) * p.eval ⟪w.1,z.1⟫_ℝ) P) ∧
    ∀ rho0 rho1 : Measure U, IsProbabilityMeasure rho0 → IsProbabilityMeasure rho1 →
      let curve : ℝ → Measure U := fun t =>
        ENNReal.ofReal (1-t) • rho0 + ENNReal.ofReal t • rho1
      Integrable (potential rho0) rho0 ∧ Integrable (potential rho0) rho1 ∧
      HasDerivWithinAt (fun t => risk (curve t))
        ((∫ w, potential rho0 w ∂rho1) - (∫ w, potential rho0 w ∂rho0))
        (Set.Icc (0 : ℝ) 1) 0 ∧
      risk rho0 + ((∫ w, potential rho0 w ∂rho1) - (∫ w, potential rho0 w ∂rho0)) ≤
        risk rho1 := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  dsimp only
  let U := {w : E // ‖w‖ = 1}
  let K : U → E → ℝ := fun w x => p.eval ⟪w.1,x⟫_ℝ
  let predictor : Measure U → E → ℝ := fun rho x => ∫ w, K w x ∂rho
  let risk : Measure U → ℝ := fun rho => ∫ z, (predictor rho z.1-z.2)^2 ∂P
  let potential : Measure U → U → ℝ := fun rho w =>
    2 * ∫ z, (predictor rho z.1-z.2) * K w z.1 ∂P
  change (∀ rho : Measure U, IsProbabilityMeasure rho →
    Integrable (fun z : E × ℝ => (predictor rho z.1-z.2)^2) P ∧
      ∀ w : U, Integrable (fun z : E × ℝ => (predictor rho z.1-z.2) * K w z.1) P) ∧
    ∀ rho0 rho1 : Measure U, IsProbabilityMeasure rho0 → IsProbabilityMeasure rho1 →
      let curve : ℝ → Measure U := fun t => ENNReal.ofReal (1-t) • rho0 + ENNReal.ofReal t • rho1
      Integrable (potential rho0) rho0 ∧ Integrable (potential rho0) rho1 ∧
      HasDerivWithinAt (fun t => risk (curve t))
        ((∫ w, potential rho0 w ∂rho1)-(∫ w, potential rho0 w ∂rho0)) (Set.Icc (0 : ℝ) 1) 0 ∧
      risk rho0 + ((∫ w, potential rho0 w ∂rho1)-(∫ w, potential rho0 w ∂rho0)) ≤ risk rho1
  obtain ⟨hf,hcont,havg⟩ := AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging.gaussian_polynomial_parameter_average_L2 (E := E) p
  have hmarg : MeasurePreserving (Prod.fst : E × ℝ → E) P (stdGaussian E) :=
    ⟨measurable_fst,hGaussian⟩
  let T : Lp ℝ 2 (stdGaussian E) →L[ℝ] Lp ℝ 2 P :=
    (Lp.compMeasurePreservingₗᵢ ℝ Prod.fst hmarg).toContinuousLinearMap
  let hfP : ∀ w : U, MemLp (fun z : E × ℝ => K w z.1) 2 P :=
    fun w => (hf w).comp_measurePreserving hmarg
  let feature : U → Lp ℝ 2 P := fun w => (hfP w).toLp (fun z => K w z.1)
  let label : Lp ℝ 2 P := hlabel.toLp (fun z : E × ℝ => z.2)
  let mean : Measure U → Lp ℝ 2 P := fun rho => ∫ w, feature w ∂rho
  have hFint (rho : Measure U) (hrho : IsProbabilityMeasure rho) : Integrable feature rho := by
    have h := T.integrable_comp (havg rho hrho).2.1
    exact h
  have hMeanClass (rho : Measure U) (hrho : IsProbabilityMeasure rho) :
      ∃ hpred : MemLp (fun z : E × ℝ => predictor rho z.1) 2 P,
        hpred.toLp (fun z => predictor rho z.1) = mean rho := by
    obtain ⟨hscalar,hint,hmean,hident⟩ := havg rho hrho
    let hpred : MemLp (fun z : E × ℝ => predictor rho z.1) 2 P :=
      hmean.comp_measurePreserving hmarg
    refine ⟨hpred, ?_⟩
    calc
      hpred.toLp (fun z => predictor rho z.1) = T (hmean.toLp (predictor rho)) := rfl
      _ = T (∫ w, (hf w).toLp (K w) ∂rho) := congrArg T hident
      _ = mean rho := (T.integral_comp_comm hint).symm
  have hMeanAE (rho : Measure U) (hrho : IsProbabilityMeasure rho) :
      (fun z => mean rho z) =ᵐ[P] (fun z : E × ℝ => predictor rho z.1) := by
    obtain ⟨hpred,hident⟩ := hMeanClass rho hrho
    rw [← hident]
    exact hpred.coeFn_toLp
  have hResidual (rho : Measure U) (hrho : IsProbabilityMeasure rho) :
      (fun z => (mean rho-label) z) =ᵐ[P] (fun z : E × ℝ => predictor rho z.1-z.2) := by
    filter_upwards [Lp.coeFn_sub (mean rho) label, hMeanAE rho hrho,hlabel.coeFn_toLp]
      with z hsub hm hy
    simp only [Pi.sub_apply] at hsub
    rw [hsub,hm,hy]
  have hRisk (rho : Measure U) (hrho : IsProbabilityMeasure rho) :
      risk rho = ‖mean rho-label‖^2 := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    apply integral_congr_ae
    filter_upwards [hResidual rho hrho] with z hz
    simp only [risk,Real.inner_apply,hz,pow_two]
  have hPot (rho : Measure U) (hrho : IsProbabilityMeasure rho) :
      potential rho = fun w => 2 * ⟪mean rho-label,feature w⟫_ℝ := by
    funext w
    change 2 * (∫ z, (predictor rho z.1-z.2) * K w z.1 ∂P) = _
    rw [L2.inner_def]
    congr 1
    apply integral_congr_ae
    filter_upwards [hResidual rho hrho,(hfP w).coeFn_toLp] with z hr hw
    change feature w z = K w z.1 at hw
    simp only [Real.inner_apply,hr,hw]
  refine ⟨?_,?_⟩
  · intro rho hrho
    obtain ⟨hpred,hident⟩ := hMeanClass rho hrho
    exact ⟨(hpred.sub hlabel).integrable_sq,fun w =>
      (hpred.sub hlabel).integrable_mul (hfP w)⟩
  · intro rho0 rho1 h0 h1
    letI : IsProbabilityMeasure rho0 := h0
    letI : IsProbabilityMeasure rho1 := h1
    dsimp only
    let curve : ℝ → Measure U := fun t => ENNReal.ofReal (1-t) • rho0 + ENNReal.ofReal t • rho1
    have hc := AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk.quadratic_feature_probability_segment
      rho0 rho1 feature label (hFint rho0 h0) (hFint rho1 h1)
    dsimp only at hc
    rcases hc with ⟨hprops,hpot0,hpot1,hderiv,hbre,hsupport⟩
    rw [hPot rho0 h0]
    refine ⟨hpot0,hpot1,?_,?_⟩
    · apply hderiv.congr_of_mem
      · intro t ht
        exact hRisk (curve t) (hprops t ht).1
      · exact ⟨le_rfl,zero_le_one⟩
    · rw [hRisk rho0 h0,hRisk rho1 h1]
      exact hsupport

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRisk
