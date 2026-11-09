import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureCoupling
import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzLower
import Mathlib.MeasureTheory.Function.L2Space

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Measure
open scoped ENNReal

-- Statistical Optimal Transport, Exercise 6: both inequalities for the
-- actual two mixtures. The test supplies neither moment nor mean hypotheses.
example (m : ℝ) (hm : 0 < m) :
    let μ := (1 / 2 : ℝ≥0∞) • gaussianReal (-m) 1 + (1 / 2 : ℝ≥0∞) • gaussianReal m 1
    let ν := (1 / 4 : ℝ≥0∞) • gaussianReal (-m) 1 + (3 / 4 : ℝ≥0∞) • gaussianReal m 1
    ENNReal.ofReal (m / 2) ≤ WassersteinSpace.wassersteinDistance μ ν ∧
      WassersteinSpace.wassersteinDistance μ ν ≤ ENNReal.ofReal m := by
  intro μ ν
  have hhalf : (1 / 2 : ℝ≥0∞) + 1 / 2 = 1 := by
    rw [ENNReal.div_add_div_same, show (1 : ℝ≥0∞) + 1 = 2 by norm_num,
      ENNReal.div_self (by norm_num) (by simp)]
  have hquarter : (1 / 4 : ℝ≥0∞) + 3 / 4 = 1 := by
    rw [ENNReal.div_add_div_same, show (1 : ℝ≥0∞) + 3 = 4 by norm_num,
      ENNReal.div_self (by norm_num) (by simp)]
  have probability (a b : ℝ≥0∞) (hab : a + b = 1) :
      IsProbabilityMeasure (a • gaussianReal (-m) 1 + b • gaussianReal m 1) := by
    refine ⟨?_⟩
    simpa only [Measure.add_apply, Measure.smul_apply, smul_eq_mul, measure_univ, mul_one] using hab
  let : IsProbabilityMeasure μ := probability _ _ hhalf
  let : IsProbabilityMeasure ν := probability _ _ hquarter
  have hthree : (3 / 4 : ℝ≥0∞) ≠ ∞ := ENNReal.div_ne_top (by norm_num) (by norm_num)
  have g₂ (a : ℝ) : Integrable (fun x : ℝ => x ^ 2) (gaussianReal a 1) :=
    (memLp_id_gaussianReal' (μ := a) (v := 1) 2 (by simp)).integrable_sq
  have moment (a b : ℝ≥0∞) (ha : a ≠ ∞) (hb : b ≠ ∞) :
      MemLp (id : ℝ → ℝ) 2 (a • gaussianReal (-m) 1 + b • gaussianReal m 1) := by
    apply (memLp_two_iff_integrable_sq measurable_id.aestronglyMeasurable).2
    exact ((g₂ (-m)).smul_measure ha).add_measure ((g₂ m).smul_measure hb)
  have g₁ (a : ℝ) : Integrable (fun x : ℝ => x) (gaussianReal a 1) :=
    (memLp_id_gaussianReal' (μ := a) (v := 1) 2 (by simp)).integrable (by norm_num)
  have mean (a b : ℝ≥0∞) (ha : a ≠ ∞) (hb : b ≠ ∞) :
      (∫ x : ℝ, x ∂(a • gaussianReal (-m) 1 + b • gaussianReal m 1)) =
        a.toReal * (-m) + b.toReal * m := by
    rw [integral_add_measure ((g₁ (-m)).smul_measure ha) ((g₁ m).smul_measure hb),
      integral_smul_measure, integral_smul_measure, integral_id_gaussianReal,
      integral_id_gaussianReal, smul_eq_mul, smul_eq_mul]
  have hμmean : (∫ x : ℝ, x ∂μ) = 0 := by
    dsimp [μ]
    rw [mean _ _ (by simp) (by simp)]
    simp only [ENNReal.toReal_div, ENNReal.toReal_one, ENNReal.toReal_ofNat]
    ring
  have hνmean : (∫ x : ℝ, x ∂ν) = m / 2 := by
    dsimp [ν]
    rw [mean _ _ (by simp) hthree]
    simp only [ENNReal.toReal_div, ENNReal.toReal_one, ENNReal.toReal_ofNat]
    ring
  constructor
  · have hneg : LipschitzWith 1 (fun x : ℝ => -x) := LipschitzWith.mk_one fun x y => by
      simpa only [Real.dist_eq, neg_sub_neg, abs_sub_comm] using
        (le_refl |x - y|)
    have h := WassersteinLipschitzLower.expectation_sub_le_linearCost_and_le_wassersteinDistance
      μ ν (moment _ _ (by simp) (by simp)) (moment _ _ (by simp) hthree) _ hneg
    have hbound := h.1.trans h.2
    change ENNReal.ofReal ((∫ x : ℝ, -x ∂μ) - (∫ x : ℝ, -x ∂ν)) ≤ _ at hbound
    simpa only [integral_neg (fun x : ℝ => x), hμmean, hνmean, neg_zero, zero_sub,
      neg_neg] using hbound
  · obtain ⟨γ, hγ, hcost⟩ := GaussianMixtureCoupling.exists_gaussian_mixture_coupling_cost m
    have hs : WassersteinSpace.wassersteinDistance μ ν ^ 2 ≤ ENNReal.ofReal (m ^ 2) :=
      (WassersteinSpace.wassersteinDistance_sq_le_lintegral_of_isCoupling μ ν γ hγ).trans_eq hcost
    apply (ENNReal.rpow_le_rpow_iff (z := 2) (by norm_num)).1
    rwa [ENNReal.rpow_two, ENNReal.rpow_two, ← ENNReal.ofReal_pow hm.le]

#print axioms AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzLower.expectation_sub_le_linearCost_and_le_wassersteinDistance
