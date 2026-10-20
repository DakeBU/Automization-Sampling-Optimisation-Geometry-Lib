import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

open MeasureTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

namespace Tests.QuadraticFeatureRisk

noncomputable section

/-- Nondegenerate responses at the same input: response is not a function of input. -/
private def noisyData : Measure (Unit × ℝ) :=
  (2 : ℝ≥0∞)⁻¹ • (Measure.dirac ((), 1) + Measure.dirac ((), 3))

private instance : IsProbabilityMeasure noisyData := by
  constructor
  change (2 : ℝ≥0∞)⁻¹ * ((Measure.dirac ((), (1 : ℝ)) + Measure.dirac ((), 3) : Measure (Unit × ℝ)) Set.univ) = 1
  simp only [Measure.add_apply, measure_univ, one_add_one_eq_two]
  exact ENNReal.inv_mul_cancel (by norm_num) (by norm_num)

private def signFeature (q : Fin 2) (_ : Unit) : ℝ := if q = 0 then 1 else -1

private def empiricalTwo (cfg : Fin 2 → Fin 2) : Measure (Fin 2) :=
  (2 : ℝ≥0∞)⁻¹ • ∑ j, Measure.dirac (cfg j)

private theorem empiricalTwo_integral (cfg : Fin 2 → Fin 2) (g : Fin 2 → ℝ) :
    (∫ q, g q ∂empiricalTwo cfg) = (g (cfg 0) + g (cfg 1)) / 2 := by
  rw [empiricalTwo, integral_smul_measure,
    integral_finsetSum_measure (fun j _ => integrable_dirac (by simp))]
  norm_num [Fin.sum_univ_two, smul_eq_mul]
  ring

private theorem noisyData_integral (g : Unit × ℝ → ℝ) :
    (∫ z, g z ∂noisyData) = (g ((), 1) + g ((), 3)) / 2 := by
  rw [noisyData, integral_smul_measure,
    integral_add_measure (integrable_dirac (by simp)) (integrable_dirac (by simp))]
  norm_num [smul_eq_mul]
  ring

/-- A colliding two-particle law with an actual noisy response gives pairing2,
exact remainder1, and the tight budget4*1²/2²=1. -/
example :
    let rho := empiricalTwo (fun _ => 0)
    let rhoNew := empiricalTwo (Function.update (fun _ => 0) 0 1)
    let predictor : Measure (Fin 2) → Unit → ℝ := fun law x => ∫ q, signFeature q x ∂law
    let risk : Measure (Fin 2) → ℝ := fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂noisyData
    let V : Fin 2 → ℝ := fun q => 2 * ∫ z, (predictor rho z.1 - z.2) * signFeature q z.1 ∂noisyData
    let D := (∫ q, V q ∂rhoNew) - (∫ q, V q ∂rho)
    D = 2 ∧ risk rhoNew - risk rho - D = 1 ∧ risk rhoNew - risk rho - D ≤ 1 := by
  let rho := empiricalTwo (fun _ => 0)
  let rhoNew := empiricalTwo (Function.update (fun _ => 0) 0 1)
  let predictor : Measure (Fin 2) → Unit → ℝ := fun law x => ∫ q, signFeature q x ∂law
  let risk : Measure (Fin 2) → ℝ := fun law => ∫ z, (predictor law z.1 - z.2) ^ 2 ∂noisyData
  let V : Fin 2 → ℝ := fun q => 2 * ∫ z, (predictor rho z.1 - z.2) * signFeature q z.1 ∂noisyData
  let D := (∫ q, V q ∂rhoNew) - (∫ q, V q ∂rho)
  change D = 2 ∧ risk rhoNew - risk rho - D = 1 ∧ risk rhoNew - risk rho - D ≤ 1
  haveI : IsProbabilityMeasure (noisyData.map (Prod.fst : Unit × ℝ → Unit)) :=
    Measure.isProbabilityMeasure_map measurable_fst.aemeasurable
  have hfeature (q : Fin 2) : MemLp (signFeature q) 2 (noisyData.map Prod.fst) := by
    exact memLp_const _
  have hbound (q : Fin 2) : ‖(hfeature q).toLp (signFeature q)‖ ≤ (1 : ℝ) := by
    rw [Lp.norm_toLp]
    change (eLpNorm (fun _ : Unit => (if q = 0 then 1 else -1 : ℝ)) 2
      (noisyData.map Prod.fst)).toReal ≤ 1
    rw [eLpNorm_const' _ (by norm_num) (by norm_num)]
    by_cases hq : q = 0 <;> norm_num [hq]
  have hlabel : MemLp (fun z : Unit × ℝ => z.2) 2 noisyData := by
    apply MemLp.of_bound measurable_snd.aestronglyMeasurable 3
    apply Measure.ae_smul_measure (μ := Measure.dirac ((), (1 : ℝ)) + Measure.dirac ((), 3)) _ (2 : ℝ≥0∞)⁻¹
    norm_num [ae_add_measure_iff]
  have result := joint_empirical_squared_risk_replacement noisyData signFeature 1 (by norm_num)
    hfeature hbound hlabel (N := 2) (by decide) (fun _ => 0) 0 1
  rcases result with ⟨hpositive, hprob, hprobNew, hLoss, hLossNew,
    hV, hVNew, hPair, hRemainder, hNonneg, hBudget⟩
  change risk rhoNew - risk rho - D =
    ∫ x, (predictor rhoNew x - predictor rho x) ^ 2 ∂noisyData.map Prod.fst at hRemainder
  change risk rhoNew - risk rho - D ≤ 4 * (1 : ℝ) ^ 2 / (2 : ℝ) ^ 2 at hBudget
  have hPredOld (x : Unit) : predictor rho x = 1 := by
    norm_num [predictor, rho, empiricalTwo_integral, signFeature]
  have hPredNew (x : Unit) : predictor rhoNew x = 0 := by
    norm_num [predictor, rhoNew, empiricalTwo_integral, signFeature]
  have hMeanSquare : (∫ x, (predictor rhoNew x - predictor rho x) ^ 2
      ∂noisyData.map Prod.fst) = 1 := by
    simp only [hPredOld, hPredNew]
    norm_num
  have hPairValue : D = 2 := by
    norm_num [D, V, predictor, rho, rhoNew, empiricalTwo_integral, noisyData_integral, signFeature]
  refine ⟨hPairValue, hRemainder.trans hMeanSquare, ?_⟩
  norm_num only at hBudget
  exact hBudget

#print axioms empirical_squared_feature_risk_derivatives
#print axioms empirical_squared_risk_eq_L2_norm
#print axioms empirical_law_squared_risk_eq_L2_norm
#print axioms empirical_squared_loss_replacement
#print axioms quadratic_feature_mean_calculus
#print axioms joint_empirical_squared_risk_replacement

end

end Tests.QuadraticFeatureRisk
