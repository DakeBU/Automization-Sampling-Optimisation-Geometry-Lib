import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov

/-!
# The one-row truncation bound in Appendix C.2

The exact Gaussian moment gives the tail at the source threshold by exponential
Markov. The row dimension is `q + 1`, with no scaling of its Euclidean norm.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.Tests.GaussianComplexityRadialExponential

open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential

/-- Apply the quadratic exponential moment to the source row law and threshold. -/
private theorem actual_source_row_truncation_tail
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let L : ℝ := 2 * ((q + 1 : ℕ) : ℝ) + 3 * Real.log (1000 * (d : ℝ))
  μ {x : E | L < ‖x‖ ^ 2} ≤ ENNReal.ofReal ((1000 * (d : ℝ))⁻¹) := by
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let row_dim : ℝ := (q + 1 : ℕ)
  let scale : ℝ := 1000 * (d : ℝ)
  let L : ℝ := 2 * row_dim + 3 * Real.log scale
  let weight (x : E) : ℝ := Real.exp (‖x‖ ^ 2 / 3)
  change μ {x : E | L < ‖x‖ ^ 2} ≤ ENNReal.ofReal (scale⁻¹)
  have d_pos : 0 < d := by omega
  have d_real_pos : 0 < (d : ℝ) := by exact_mod_cast d_pos
  have scale_pos : 0 < scale := by unfold scale; positivity
  have row_dim_nonneg : 0 ≤ row_dim := by unfold row_dim; positivity
  obtain ⟨weight_integrable, exact_moment⟩ :=
    integrable_exp_norm_sq_div_three_and_integral_stdGaussian (E := E)
  have rank_eq : Module.finrank ℝ E = q + 1 := finrank_euclideanSpace_fin
  rw [rank_eq] at exact_moment
  change (∫ x, weight x ∂μ) = (3 : ℝ) ^ (row_dim / 2) at exact_moment
  have weight_measurable : Measurable (fun x => ENNReal.ofReal (weight x)) := by
    unfold weight
    fun_prop
  have weight_nonneg : 0 ≤ᵐ[μ] weight := ae_of_all _ fun _ => Real.exp_nonneg _

  -- Bound the numerical coefficient of the row dimension in the exponent.
  have log_three_split : Real.log 3 = 2 * Real.log (3 / 2) + Real.log (4 / 3) := by
    calc
      Real.log 3 = Real.log ((3 / 2) * (3 / 2) * (4 / 3)) := by congr 1; norm_num
      _ = _ := by
        rw [Real.log_mul (x := (3 / 2) * (3 / 2)) (y := 4 / 3) (by norm_num) (by norm_num),
          Real.log_mul (x := 3 / 2) (y := 3 / 2) (by norm_num) (by norm_num)]
        ring
  have log_three_lt : Real.log 3 < 4 / 3 := by
    rw [log_three_split]
    linarith [Real.log_lt_sub_one_of_pos (x := 3 / 2) (by norm_num) (by norm_num),
      Real.log_le_sub_one_of_pos (x := 4 / 3) (by norm_num)]
  have log_moment_le : Real.log 3 * (row_dim / 2) ≤ 2 * row_dim / 3 := by
    nlinarith [mul_nonneg row_dim_nonneg (sub_nonneg.mpr log_three_lt.le)]
  have moment_over_threshold : (3 : ℝ) ^ (row_dim / 2) / Real.exp (L / 3) ≤ scale⁻¹ := by
    rw [Real.rpow_def_of_pos (by norm_num : 0 < (3 : ℝ)), ← Real.exp_sub,
      ← Real.exp_log scale_pos, ← Real.exp_neg]
    apply Real.exp_le_exp.mpr
    dsimp [L]
    linarith

  -- The strict bad event lies in the weak threshold event used by Markov.
  calc
    μ {x : E | L < ‖x‖ ^ 2} ≤
        μ {x : E | ENNReal.ofReal (Real.exp (L / 3)) ≤ ENNReal.ofReal (weight x)} := by
      apply measure_mono
      intro x hx
      change L < ‖x‖ ^ 2 at hx
      exact ENNReal.ofReal_le_ofReal (Real.exp_le_exp.mpr
        (div_le_div_of_nonneg_right hx.le (by norm_num)))
    _ ≤ (∫⁻ x, ENNReal.ofReal (weight x) ∂μ) / ENNReal.ofReal (Real.exp (L / 3)) :=
      meas_ge_le_lintegral_div weight_measurable.aemeasurable
        (ne_of_gt (ENNReal.ofReal_pos.mpr (Real.exp_pos _))) ENNReal.ofReal_ne_top
    _ = ENNReal.ofReal ((3 : ℝ) ^ (row_dim / 2) / Real.exp (L / 3)) := by
      rw [← ofReal_integral_eq_lintegral_ofReal weight_integrable weight_nonneg,
        exact_moment, ENNReal.ofReal_div_of_pos (Real.exp_pos _)]
    _ ≤ ENNReal.ofReal (scale⁻¹) := ENNReal.ofReal_le_ofReal moment_over_threshold

end AutoSamplingTheory.Tests.GaussianComplexityRadialExponential
