import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity

/-!
# Quadratic exponential moment of a standard Gaussian

The scalar exponential moment used in Appendix C.2 of arXiv:2610.20492v1.
Multiplying the standard Gaussian density by the exponential changes its
variance from `1` to `3` and introduces the factor `3 ^ (dim / 2)`.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential

open AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity

/-- The quadratic exponential at coefficient `1 / 3` is integrable under the
standard Gaussian. Its exact moment uses half the real dimension, including
odd dimensions and dimension zero. -/
theorem integrable_exp_norm_sq_div_three_and_integral_stdGaussian
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] :
  Integrable (fun x : E => Real.exp (‖x‖ ^ 2 / 3)) (stdGaussian E) ∧
    (∫ x : E, Real.exp (‖x‖ ^ 2 / 3) ∂stdGaussian E) =
      (3 : ℝ) ^ ((Module.finrank ℝ E : ℝ) / 2) := by
  let dimension := Module.finrank ℝ E
  let factor : ℝ := (3 : ℝ) ^ ((dimension : ℝ) / 2)
  let weight (x : E) : ℝ := Real.exp (‖x‖ ^ 2 / 3)
  let density (variance : ℝ) (x : E) : ℝ≥0∞ := ENNReal.ofReal
    (((Real.sqrt (2 * Real.pi * variance))⁻¹) ^ dimension *
      Real.exp (-‖x‖ ^ 2 / (2 * variance)))
  have weight_continuous : Continuous weight := by fun_prop
  have weight_nonneg : ∀ x, 0 ≤ weight x := fun _ => Real.exp_nonneg _
  have density_measurable (variance : ℝ) : Measurable (density variance) := by
    unfold density
    fun_prop
  have standard_density : stdGaussian E = volume.withDensity (density 1) := by
    have scaled := map_sqrt_smul_stdGaussian_eq_withDensity (E := E) 1 zero_lt_one
    have scale_one : (fun x : E => Real.sqrt 1 • x) = id := by
      funext x
      simp
    rw [scale_one, Measure.map_id] at scaled
    exact scaled
  have scaled_density : (stdGaussian E).map (fun x : E => Real.sqrt 3 • x) =
      volume.withDensity (density 3) :=
    map_sqrt_smul_stdGaussian_eq_withDensity (E := E) 3 (by norm_num)
  have scaled_is_probability : IsProbabilityMeasure (volume.withDensity (density 3)) := by
    rw [← scaled_density]
    exact Measure.isProbabilityMeasure_map (by fun_prop)
  have density_mass : (∫⁻ x, density 3 x ∂volume) = 1 := by
    simpa only [withDensity_apply _ MeasurableSet.univ, Measure.restrict_univ] using
      scaled_is_probability.measure_univ
  have factor_nonneg : 0 ≤ factor := by unfold factor; positivity
  have factor_sqrt : factor = Real.sqrt 3 ^ dimension := by
    calc
      factor = (3 : ℝ) ^ ((1 / 2 : ℝ) * (dimension : ℝ)) := by
        unfold factor
        congr 1
        ring
      _ = ((3 : ℝ) ^ (1 / 2 : ℝ)) ^ (dimension : ℝ) :=
        Real.rpow_mul (by norm_num) _ _
      _ = Real.sqrt 3 ^ dimension := by rw [← Real.sqrt_eq_rpow, Real.rpow_natCast]
  have density_factor : factor * ((Real.sqrt (2 * Real.pi * 3))⁻¹) ^ dimension =
      ((Real.sqrt (2 * Real.pi * 1))⁻¹) ^ dimension := by
    rw [factor_sqrt, Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi), ← mul_pow, mul_one]
    congr 1
    field_simp [Real.sqrt_ne_zero'.mpr (by positivity : 0 < 2 * Real.pi),
      Real.sqrt_ne_zero'.mpr (by norm_num : 0 < (3 : ℝ))]
  have weighted_density (x : E) :
      density 1 x * ENNReal.ofReal (weight x) = ENNReal.ofReal factor * density 3 x := by
    dsimp [density, weight]
    rw [← ENNReal.ofReal_mul (by positivity), ← ENNReal.ofReal_mul factor_nonneg]
    congr 1
    rw [mul_assoc, ← Real.exp_add,
      show -‖x‖ ^ 2 / (2 * 1) + ‖x‖ ^ 2 / 3 = -‖x‖ ^ 2 / (2 * 3) by ring,
      ← mul_assoc, density_factor]
  have weighted_mass : (∫⁻ x, ENNReal.ofReal (weight x) ∂stdGaussian E) =
      ENNReal.ofReal factor := by
    calc
      (∫⁻ x, ENNReal.ofReal (weight x) ∂stdGaussian E) =
          ∫⁻ x, density 1 x * ENNReal.ofReal (weight x) ∂volume := by
        rw [standard_density,
          lintegral_withDensity_eq_lintegral_mul volume (density_measurable 1)
            weight_continuous.measurable.ennreal_ofReal]
        rfl
      _ = ∫⁻ x, ENNReal.ofReal factor * density 3 x ∂volume :=
        lintegral_congr weighted_density
      _ = ENNReal.ofReal factor := by
        rw [lintegral_const_mul _ (density_measurable 3), density_mass, mul_one]
  have weight_integrable : Integrable weight (stdGaussian E) := by
    refine ⟨weight_continuous.stronglyMeasurable.aestronglyMeasurable, ?_⟩
    rw [hasFiniteIntegral_iff_ofReal (ae_of_all _ weight_nonneg), weighted_mass]
    exact ENNReal.ofReal_lt_top
  refine ⟨weight_integrable, ?_⟩
  apply (ENNReal.ofReal_eq_ofReal_iff (integral_nonneg weight_nonneg) factor_nonneg).mp
  rw [ofReal_integral_eq_lintegral_ofReal weight_integrable (ae_of_all _ weight_nonneg),
    weighted_mass]

end AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
