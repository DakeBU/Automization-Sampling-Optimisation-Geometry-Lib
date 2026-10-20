import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk

open MeasureTheory
open scoped InnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk

theorem quadratic_feature_probability_segment
    {W H : Type*} [MeasurableSpace W]
    [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
    (μ ν : Measure W) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (feature : W → H) (label : H)
    (hμ : Integrable feature μ) (hν : Integrable feature ν) :
    let curve : ℝ → Measure W := fun t =>
      ENNReal.ofReal (1 - t) • μ + ENNReal.ofReal t • ν
    let mean : Measure W → H := fun law => ∫ w, feature w ∂law
    let risk : Measure W → ℝ := fun law => ‖mean law - label‖ ^ 2
    let potential : W → ℝ := fun w => 2 * ⟪mean μ - label, feature w⟫_ℝ
    (∀ t ∈ Set.Icc (0 : ℝ) 1,
      IsProbabilityMeasure (curve t) ∧ Integrable feature (curve t) ∧
      mean (curve t) = (1 - t) • mean μ + t • mean ν) ∧
    Integrable potential μ ∧ Integrable potential ν ∧
    HasDerivWithinAt (fun t => risk (curve t))
      ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ))
      (Set.Icc (0 : ℝ) 1) 0 ∧
    (risk ν - risk μ - ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) =
      ‖mean ν - mean μ‖ ^ 2) ∧
    (risk μ + ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) ≤ risk ν) := by
  dsimp only
  let curve : ℝ → Measure W := fun t =>
    ENNReal.ofReal (1 - t) • μ + ENNReal.ofReal t • ν
  let mean : Measure W → H := fun law => ∫ w, feature w ∂law
  let risk : Measure W → ℝ := fun law => ‖mean law - label‖ ^ 2
  let potential : W → ℝ := fun w => 2 * ⟪mean μ - label, feature w⟫_ℝ
  change (∀ t ∈ Set.Icc (0 : ℝ) 1,
    IsProbabilityMeasure (curve t) ∧ Integrable feature (curve t) ∧
    mean (curve t) = (1 - t) • mean μ + t • mean ν) ∧
    Integrable potential μ ∧ Integrable potential ν ∧
    HasDerivWithinAt (fun t => risk (curve t))
      ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) (Set.Icc (0 : ℝ) 1) 0 ∧
    (risk ν - risk μ - ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) =
      ‖mean ν - mean μ‖ ^ 2) ∧
    (risk μ + ((∫ w, potential w ∂ν) - (∫ w, potential w ∂μ)) ≤ risk ν)
  have hprops : ∀ t ∈ Set.Icc (0 : ℝ) 1,
      IsProbabilityMeasure (curve t) ∧ Integrable feature (curve t) ∧
      mean (curve t) = (1 - t) • mean μ + t • mean ν := by
    intro t ht
    have hleft : 0 ≤ 1 - t := sub_nonneg.mpr ht.2
    have hμt := hμ.smul_measure (c := ENNReal.ofReal (1 - t)) ENNReal.ofReal_ne_top
    have hνt := hν.smul_measure (c := ENNReal.ofReal t) ENNReal.ofReal_ne_top
    refine ⟨?_, hμt.add_measure hνt, ?_⟩
    · apply isProbabilityMeasure_iff.mpr
      simp only [curve, Measure.add_apply, Measure.smul_apply, measure_univ, smul_eq_mul,
        mul_one]
      rw [← ENNReal.ofReal_add hleft ht.1]
      norm_num
    · dsimp only [mean, curve]
      rw [integral_add_measure hμt hνt, integral_smul_measure, integral_smul_measure,
        ENNReal.toReal_ofReal hleft, ENNReal.toReal_ofReal ht.1]
  have hcalc := AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticFeatureRisk.quadratic_feature_mean_calculus
    μ ν feature label hμ hν
  dsimp only at hcalc
  rcases hcalc with ⟨hpotμ, hpotν, hpair, hbre, hsupport, hderiv⟩
  refine ⟨hprops, hpotμ, hpotν, ?_, hbre, hsupport⟩
  apply hderiv.hasDerivWithinAt.congr_of_mem
  · intro t ht
    change ‖mean (curve t) - label‖ ^ 2 = _
    rw [(hprops t ht).2.2]
    congr 2
    rw [sub_smul, one_smul, smul_sub]
    abel
  · exact ⟨le_rfl, zero_le_one⟩


end AutoSamplingTheory.TechnicalLemmas.Analysis.ProbabilitySegmentRisk
