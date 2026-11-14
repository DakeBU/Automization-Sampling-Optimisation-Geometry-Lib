import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment
import Mathlib.Analysis.SpecialFunctions.ImproperIntegrals
import Mathlib.MeasureTheory.Integral.Layercake
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov

/-!
# The truncated radial first moment of one Gaussian row

Appendix C.2 of arXiv:2610.20492v1 integrates the shifted tail of the squared
norm of one standard Gaussian row. The Gaussian expectation and the real
level integral use their respective measures.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRadialMoment

open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment

/-- The strict truncated moment at the source threshold is the boundary term
plus the integral of the shifted tail, with the source upper bound. -/
theorem actual_standard_row_tail_first_moment
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let L : ℝ := 2 * ((q + 1 : ℕ) : ℝ) + 3 * Real.log (1000 * (d : ℝ))
  let badMoment : E → ℝ := Set.indicator {x : E | L < R x} R
  let tail : ℝ → ℝ := fun s => (μ {x : E | L + s < R x}).toReal
  Integrable badMoment μ ∧ IntegrableOn tail (Set.Ioi (0 : ℝ)) (volume : Measure ℝ) ∧
    (∫ x, badMoment x ∂μ) = L * tail 0 + (∫ s in Set.Ioi (0 : ℝ), tail s ∂volume) ∧
    (∫ x, badMoment x ∂μ) ≤ (L + 3) / (1000 * (d : ℝ)) := by
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let μ : Measure E := stdGaussian E
  let R : E → ℝ := fun x => ‖x‖ ^ 2
  let r : ℝ := (q + 1 : ℕ)
  let scale : ℝ := 1000 * (d : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log scale
  let bad : Set E := {x | L < R x}
  let badMoment : E → ℝ := bad.indicator R
  let tail (s : ℝ) : ℝ := (μ {x : E | L + s < R x}).toReal
  let envelope (s : ℝ) : ℝ := Real.exp (-(1 / 3 : ℝ) * s) / scale
  change Integrable badMoment μ ∧ IntegrableOn tail (Set.Ioi (0 : ℝ)) volume ∧
    (∫ x, badMoment x ∂μ) = L * tail 0 + (∫ s in Set.Ioi (0 : ℝ), tail s ∂volume) ∧
    (∫ x, badMoment x ∂μ) ≤ (L + 3) / scale
  have d_ge_one : (1 : ℝ) ≤ (d : ℝ) := by
    exact_mod_cast (show 1 ≤ d by omega)
  have scale_ge_one : 1 ≤ scale := by unfold scale; linarith
  have scale_pos : 0 < scale := zero_lt_one.trans_le scale_ge_one
  have r_nonneg : 0 ≤ r := by unfold r; positivity
  have cutoff_nonneg : 0 ≤ L := by
    unfold L
    linarith [Real.log_nonneg scale_ge_one]
  have radius_nonneg (x : E) : 0 ≤ R x := sq_nonneg _
  have radius_measurable : Measurable R := by unfold R; fun_prop
  have radius_integrable : Integrable R μ :=
    (integrable_norm_sq_and_integral_stdGaussian (E := E)).1
  have bad_measurable : MeasurableSet bad := measurableSet_lt measurable_const radius_measurable
  have bad_moment_integrable : Integrable badMoment μ := radius_integrable.indicator bad_measurable

  -- The exact exponential moment bounds each shifted tail.
  let weight (x : E) : ℝ := Real.exp (R x / 3)
  obtain ⟨weight_integrable, exact_moment⟩ :=
    integrable_exp_norm_sq_div_three_and_integral_stdGaussian (E := E)
  rw [show Module.finrank ℝ E = q + 1 from finrank_euclideanSpace_fin] at exact_moment
  change (∫ x, weight x ∂μ) = (3 : ℝ) ^ (r / 2) at exact_moment
  have weight_measurable : Measurable (fun x => ENNReal.ofReal (weight x)) := by
    unfold weight R
    fun_prop
  have weight_nonneg : 0 ≤ᵐ[μ] weight := ae_of_all _ fun _ => Real.exp_nonneg _
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
  have log_moment_le : Real.log 3 * (r / 2) ≤ 2 * r / 3 := by
    nlinarith [mul_nonneg r_nonneg (sub_nonneg.mpr log_three_lt.le)]
  have moment_ratio_le (s : ℝ) : (3 : ℝ) ^ (r / 2) / Real.exp ((L + s) / 3) ≤ envelope s := by
    rw [Real.rpow_def_of_pos (by norm_num : 0 < (3 : ℝ)), ← Real.exp_sub]
    calc
      _ ≤ Real.exp (-(1 / 3 : ℝ) * s - Real.log scale) := by
        apply Real.exp_le_exp.mpr
        unfold L
        linarith
      _ = envelope s := by rw [Real.exp_sub, Real.exp_log scale_pos]
  have tail_bound (s : ℝ) : tail s ≤ envelope s := by
    have bound : μ {x : E | L + s < R x} ≤ ENNReal.ofReal (envelope s) := by
      calc
        μ {x : E | L + s < R x} ≤
            μ {x : E | ENNReal.ofReal (Real.exp ((L + s) / 3)) ≤ ENNReal.ofReal (weight x)} := by
          apply measure_mono
          intro x hx
          change L + s < R x at hx
          exact ENNReal.ofReal_le_ofReal (Real.exp_le_exp.mpr
            (div_le_div_of_nonneg_right hx.le (by norm_num)))
        _ ≤ (∫⁻ x, ENNReal.ofReal (weight x) ∂μ) / ENNReal.ofReal (Real.exp ((L + s) / 3)) :=
          meas_ge_le_lintegral_div weight_measurable.aemeasurable
            (ne_of_gt (ENNReal.ofReal_pos.mpr (Real.exp_pos _))) ENNReal.ofReal_ne_top
        _ = ENNReal.ofReal ((3 : ℝ) ^ (r / 2) / Real.exp ((L + s) / 3)) := by
          rw [← ofReal_integral_eq_lintegral_ofReal weight_integrable weight_nonneg,
            exact_moment, ENNReal.ofReal_div_of_pos (Real.exp_pos _)]
        _ ≤ ENNReal.ofReal (envelope s) := ENNReal.ofReal_le_ofReal (moment_ratio_le s)
    have real_bound := (ENNReal.toReal_le_toReal (measure_ne_top μ _) ENNReal.ofReal_ne_top).2 bound
    have envelope_nonneg : 0 ≤ envelope s := by unfold envelope; positivity
    simpa only [tail, ENNReal.toReal_ofReal envelope_nonneg] using real_bound
  have measure_antitone : Antitone (fun s : ℝ => μ {x : E | L + s < R x}) := by
    intro s t hst
    apply measure_mono
    intro x hx
    change L + t < R x at hx
    change L + s < R x
    linarith
  have tail_measurable : Measurable tail := measure_antitone.measurable.ennreal_toReal
  have envelope_integrable : IntegrableOn envelope (Set.Ioi (0 : ℝ)) volume :=
    (integrableOn_exp_mul_Ioi (a := -(1 / 3 : ℝ)) (by norm_num) 0).div_const scale
  have tail_integrable : IntegrableOn tail (Set.Ioi (0 : ℝ)) volume :=
    envelope_integrable.mono_nonneg tail_measurable.aestronglyMeasurable
      (ae_of_all _ fun _ => ENNReal.toReal_nonneg) (ae_of_all _ tail_bound)

  -- Separate the mass at the threshold from the positive excess.
  let excess (x : E) : ℝ := max (R x - L) 0
  have excess_nonneg (x : E) : 0 ≤ excess x := le_max_right _ _
  have excess_integrable : Integrable excess μ :=
    radius_integrable.mono_nonneg (by unfold excess R; fun_prop) (ae_of_all _ excess_nonneg)
      (ae_of_all _ fun x => max_le (sub_le_self _ cutoff_nonneg) (radius_nonneg x))
  have excess_levels (s : ℝ) (hs : 0 < s) :
      {x : E | s < excess x} = {x : E | L + s < R x} := by
    ext x
    change s < max (R x - L) 0 ↔ L + s < R x
    rw [lt_max_iff, or_iff_left (not_lt_of_ge hs.le)]
    constructor <;> intro h <;> linarith
  have excess_integral : (∫ x, excess x ∂μ) = ∫ s in Set.Ioi (0 : ℝ), tail s ∂volume := by
    rw [excess_integrable.integral_eq_integral_meas_lt (ae_of_all _ excess_nonneg)]
    apply setIntegral_congr_fun measurableSet_Ioi
    intro s hs
    change (μ {x : E | s < excess x}).toReal = (μ {x : E | L + s < R x}).toReal
    rw [excess_levels s hs]
  let boundaryTerm : E → ℝ := bad.indicator (fun _ => L)
  have boundary_integrable : Integrable boundaryTerm μ := (integrable_const L).indicator bad_measurable
  have boundary_integral : (∫ x, boundaryTerm x ∂μ) = L * tail 0 := by
    unfold boundaryTerm
    rw [integral_indicator bad_measurable, setIntegral_const]
    change (μ bad).toReal * L = L * (μ {x : E | L + 0 < R x}).toReal
    simp only [bad, add_zero, mul_comm]
  have split : badMoment = fun x => boundaryTerm x + excess x := by
    funext x
    by_cases hx : L < R x
    · have nonneg : 0 ≤ R x - L := sub_nonneg.mpr hx.le
      simp only [badMoment, boundaryTerm, bad, Set.indicator, Set.mem_ofPred_eq, hx, if_true,
        excess, max_eq_left nonneg]
      ring
    · have nonpos : R x - L ≤ 0 := sub_nonpos.mpr (le_of_not_gt hx)
      simp only [badMoment, boundaryTerm, bad, Set.indicator, Set.mem_ofPred_eq, hx, if_false,
        excess, max_eq_right nonpos, add_zero]
  have moment_identity : (∫ x, badMoment x ∂μ) =
      L * tail 0 + (∫ s in Set.Ioi (0 : ℝ), tail s ∂volume) := by
    rw [split, integral_add boundary_integrable excess_integrable, boundary_integral, excess_integral]

  -- Integrate the exponential envelope and use the tail at shift zero.
  have envelope_integral : (∫ s in Set.Ioi (0 : ℝ), envelope s ∂volume) = 3 / scale := by
    unfold envelope
    rw [integral_div, integral_exp_mul_Ioi (a := -(1 / 3 : ℝ)) (by norm_num) 0]
    norm_num
  have tail_integral_le : (∫ s in Set.Ioi (0 : ℝ), tail s ∂volume) ≤ 3 / scale := by
    rw [← envelope_integral]
    exact integral_mono_ae tail_integrable envelope_integrable (ae_of_all _ tail_bound)
  have tail_zero_le : tail 0 ≤ 1 / scale := by simpa [envelope] using tail_bound 0
  refine ⟨bad_moment_integrable, tail_integrable, moment_identity, ?_⟩
  calc
    _ = L * tail 0 + (∫ s in Set.Ioi (0 : ℝ), tail s ∂volume) := moment_identity
    _ ≤ L * (1 / scale) + 3 / scale :=
      add_le_add (mul_le_mul_of_nonneg_left tail_zero_le cutoff_nonneg) tail_integral_le
    _ = (L + 3) / scale := by ring

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRadialMoment
