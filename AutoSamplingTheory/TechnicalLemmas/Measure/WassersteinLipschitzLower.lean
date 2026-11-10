import AutoSamplingTheory.TechnicalLemmas.Measure.CouplingQuadraticIntegrability
import AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinSpace
import Mathlib.MeasureTheory.Integral.MeanInequalities

namespace AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzLower

open MeasureTheory
open scoped ENNReal

/-- The real P₂ lower comparison in Statistical Optimal Transport §1.8,
Exercise 6. The linear-cost infimum is the literal Kantorovich cost for
absolute displacement; only the one-sided Lipschitz inequality is claimed. -/
theorem expectation_sub_le_linearCost_and_le_wassersteinDistance
    (μ ν : Measure ℝ) [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (hμ : MemLp (id : ℝ → ℝ) 2 μ) (hν : MemLp (id : ℝ → ℝ) 2 ν)
    (f : ℝ → ℝ) (hf : LipschitzWith 1 f) :
    let W₁ := Transport.transportCost (fun z : ℝ × ℝ => ENNReal.ofReal |z.1 - z.2|) μ ν
    ENNReal.ofReal ((∫ x, f x ∂μ) - ∫ y, f y ∂ν) ≤ W₁ ∧
      W₁ ≤ WassersteinSpace.wassersteinDistance μ ν := by
  let c : ℝ × ℝ → ℝ≥0∞ := fun z => ENNReal.ofReal |z.1 - z.2|
  change ENNReal.ofReal ((∫ x, f x ∂μ) - ∫ y, f y ∂ν) ≤
    Transport.transportCost c μ ν ∧
    Transport.transportCost c μ ν ≤ WassersteinSpace.wassersteinDistance μ ν
  constructor
  · have hf_int (ρ : Measure ℝ) [IsProbabilityMeasure ρ]
        (hρ : MemLp (id : ℝ → ℝ) 2 ρ) : Integrable f ρ := by
      let g : ℝ → ℝ := fun x => f x - f 0
      have hg : LipschitzWith 1 g := LipschitzWith.mk_one fun x y => by
        have heq : g x - g y = f x - f y := by dsimp [g]; ring
        simpa only [Real.dist_eq, heq, NNReal.coe_one, one_mul] using hf.dist_le_mul x y
      have hg₂ : MemLp g 2 ρ := hg.comp_memLp (by simp [g]) hρ
      have hadd : g + (fun _ : ℝ => f 0) = f := by
        funext x
        exact sub_add_cancel (f x) (f 0)
      rw [← hadd]
      exact (hg₂.integrable (by norm_num : (1 : ℝ≥0∞) ≤ 2)).add (integrable_const (f 0))
    rw [Transport.transportCost_eq_sInf]
    apply le_sInf
    rintro _ ⟨γ, hγ, rfl⟩
    have hp₁ := CouplingQuadraticIntegrability.measurePreserving_fst_of_isCoupling hγ
    have hp₂ := CouplingQuadraticIntegrability.measurePreserving_snd_of_isCoupling hγ
    have h₁ : Integrable (fun z : ℝ × ℝ => f z.1) γ :=
      hp₁.integrable_comp_of_integrable (hf_int μ hμ)
    have h₂ : Integrable (fun z : ℝ × ℝ => f z.2) γ :=
      hp₂.integrable_comp_of_integrable (hf_int ν hν)
    have he₁ : (∫ z : ℝ × ℝ, f z.1 ∂γ) = ∫ x, f x ∂μ := by
      rw [← hp₁.map_eq, integral_map measurable_fst.aemeasurable hf.continuous.aestronglyMeasurable]
    have he₂ : (∫ z : ℝ × ℝ, f z.2 ∂γ) = ∫ y, f y ∂ν := by
      rw [← hp₂.map_eq, integral_map measurable_snd.aemeasurable hf.continuous.aestronglyMeasurable]
    rw [← he₁, ← he₂, ← integral_sub h₁ h₂]
    calc
      _ ≤ ENNReal.ofReal (∫ z : ℝ × ℝ, ‖f z.1 - f z.2‖ ∂γ) := by
        apply ENNReal.ofReal_le_ofReal
        exact (le_abs_self _).trans (by simpa only [Real.norm_eq_abs] using
          norm_integral_le_integral_norm (μ := γ) (fun z : ℝ × ℝ => f z.1 - f z.2))
      _ = ∫⁻ z : ℝ × ℝ, ‖f z.1 - f z.2‖ₑ ∂γ :=
        ofReal_integral_norm_eq_lintegral_enorm (h₁.sub h₂)
      _ ≤ _ := lintegral_mono fun z => by
        rw [Real.enorm_eq_ofReal_abs]
        apply ENNReal.ofReal_le_ofReal
        simpa only [c, Real.dist_eq, NNReal.coe_one, one_mul] using hf.dist_le_mul z.1 z.2
  · by_contra! h
    obtain ⟨γ, hγ, hlt⟩ :=
      WassersteinSpace.exists_isCoupling_sqrt_lintegral_lt_of_wassersteinDistance_lt μ ν h
    let : IsProbabilityMeasure γ := Transport.isProbabilityMeasure_of_isCoupling_left hγ
    have hc : Measurable c := by dsimp [c]; fun_prop
    have hq (z : ℝ × ℝ) : c z ^ (2 : ℝ) = WassersteinSpace.quadraticCost z := by
      rw [ENNReal.rpow_two]
      change ENNReal.ofReal |z.1 - z.2| ^ 2 = ENNReal.ofReal (‖z.1 - z.2‖ ^ 2)
      rw [Real.norm_eq_abs, ENNReal.ofReal_pow (abs_nonneg _)]
    have hCS : (∫⁻ z, c z ∂γ) ≤
        (∫⁻ z, WassersteinSpace.quadraticCost z ∂γ) ^ (1 / 2 : ℝ) := by
      simpa only [Pi.mul_apply, Pi.one_apply, mul_one, ENNReal.one_rpow, lintegral_const,
        measure_univ, hq] using
        ENNReal.lintegral_mul_le_Lp_mul_Lq γ Real.HolderConjugate.two_two
          (f := c) (g := 1) hc.aemeasurable aemeasurable_const
    exact (not_lt_of_ge
      ((Transport.transportCost_le_lintegral_of_isCoupling c μ ν γ hγ).trans hCS)) hlt

end AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzLower
