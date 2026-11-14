import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
import AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw
open AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowLaw

private theorem actual_original_all_good_cutoff_probability
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let good : Set Ω := {ω | ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L}
  ENNReal.ofReal (999 / 1000 : ℝ) ≤ μ good := by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun a : Fin (q + 1) => ω a i)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let scale : ℝ := 1000 * (d : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log scale
  let good : Set Ω := {ω | ∀ i : Fin d, ‖row i ω‖ ^ 2 ≤ L}
  let bad : Fin d → Set Ω := fun i => {ω | L < ‖row i ω‖ ^ 2}
  let weight : Fin d → Ω → ℝ := fun i ω => Real.exp (‖row i ω‖ ^ 2 / 3)
  change ENNReal.ofReal (999 / 1000 : ℝ) ≤ μ good
  have d_pos : 0 < d := by omega
  have d_real_pos : 0 < (d : ℝ) := by exact_mod_cast d_pos
  have hd0 : (d : ℝ) ≠ 0 := ne_of_gt d_real_pos
  have scale_pos : 0 < scale := by dsimp [scale]; positivity
  have r_nonneg : 0 ≤ r := by dsimp [r]; positivity
  have row_law := actual_source_row_marginal_law (d := d) (q := q) hq
  change ∀ i : Fin d, MeasurePreserving (row i) μ (stdGaussian E) at row_law
  obtain ⟨canonical_integrable, canonical_mean⟩ :=
    integrable_exp_norm_sq_div_three_and_integral_stdGaussian (E := E)
  rw [show Module.finrank ℝ E = q + 1 from finrank_euclideanSpace_fin] at canonical_mean
  change (∫ x : E, Real.exp (‖x‖ ^ 2 / 3) ∂stdGaussian E) = (3 : ℝ) ^ (r / 2)
    at canonical_mean

  -- Transport both genuine integrability and the exact mean to each actual row.
  have row_moment (i : Fin d) :
      Integrable (weight i) μ ∧ (∫ ω, weight i ω ∂μ) = (3 : ℝ) ^ (r / 2) := by
    have integrable_row : Integrable (weight i) μ :=
      (row_law i).integrable_comp_of_integrable canonical_integrable
    have hmeas : AEStronglyMeasurable (fun x : E => Real.exp (‖x‖ ^ 2 / 3))
        (Measure.map (row i) μ) := by
      rw [(row_law i).map_eq]
      exact canonical_integrable.aestronglyMeasurable
    have transport := integral_map (φ := row i) (μ := μ) (row_law i).aemeasurable hmeas
    rw [(row_law i).map_eq, canonical_mean] at transport
    exact ⟨integrable_row, transport.symm⟩

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
  have moment_over_threshold : (3 : ℝ) ^ (r / 2) / Real.exp (L / 3) ≤ scale⁻¹ := by
    rw [Real.rpow_def_of_pos (by norm_num : 0 < (3 : ℝ)), ← Real.exp_sub,
      ← Real.exp_log scale_pos, ← Real.exp_neg]
    apply Real.exp_le_exp.mpr
    dsimp [L]
    linarith

  -- Exponential Markov is applied on the original column outcome space.
  have row_tail (i : Fin d) : μ (bad i) ≤ ENNReal.ofReal (scale⁻¹) := by
    have weight_measurable : Measurable (fun ω => ENNReal.ofReal (weight i ω)) := by
      have row_measurable := (row_law i).measurable
      dsimp only [weight]
      fun_prop
    have weight_nonneg : 0 ≤ᵐ[μ] weight i :=
      ae_of_all _ (fun _ => Real.exp_nonneg _)
    calc
      μ (bad i) ≤ μ {ω : Ω |
          ENNReal.ofReal (Real.exp (L / 3)) ≤ ENNReal.ofReal (weight i ω)} := by
        apply measure_mono
        intro ω hω
        change L < ‖row i ω‖ ^ 2 at hω
        exact ENNReal.ofReal_le_ofReal (Real.exp_le_exp.mpr
          (div_le_div_of_nonneg_right hω.le (by norm_num)))
      _ ≤ (∫⁻ ω, ENNReal.ofReal (weight i ω) ∂μ) / ENNReal.ofReal (Real.exp (L / 3)) :=
        meas_ge_le_lintegral_div weight_measurable.aemeasurable
          (ne_of_gt (ENNReal.ofReal_pos.mpr (Real.exp_pos _))) ENNReal.ofReal_ne_top
      _ = ENNReal.ofReal ((3 : ℝ) ^ (r / 2) / Real.exp (L / 3)) := by
        rw [← ofReal_integral_eq_lintegral_ofReal (row_moment i).1 weight_nonneg,
          (row_moment i).2, ENNReal.ofReal_div_of_pos (Real.exp_pos _)]
      _ ≤ ENNReal.ofReal (scale⁻¹) := ENNReal.ofReal_le_ofReal moment_over_threshold

  -- Finite subadditivity needs no joint-row independence.
  have good_complement : goodᶜ = ⋃ i : Fin d, bad i := by
    ext ω
    simp [good, bad, not_forall]
  have bad_union_bound : μ goodᶜ ≤ ENNReal.ofReal (1 / 1000 : ℝ) := by
    rw [good_complement]
    calc
      μ (⋃ i : Fin d, bad i) ≤ ∑ i : Fin d, μ (bad i) :=
        measure_iUnion_fintype_le μ bad
      _ ≤ ∑ i : Fin d, ENNReal.ofReal (scale⁻¹) :=
        Finset.sum_le_sum (fun i _ => row_tail i)
      _ = ENNReal.ofReal (∑ _i : Fin d, scale⁻¹) :=
        (ENNReal.ofReal_sum_of_nonneg (fun _ _ => inv_nonneg.mpr scale_pos.le)).symm
      _ = ENNReal.ofReal (1 / 1000 : ℝ) := by
        congr 1
        simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
        dsimp [scale]
        field_simp
  have good_measurable : MeasurableSet good := by
    have each (i : Fin d) : MeasurableSet {ω : Ω | ‖row i ω‖ ^ 2 ≤ L} :=
      measurableSet_le ((row_law i).measurable.norm.pow_const 2) measurable_const
    convert MeasurableSet.iInter each using 1
    ext ω
    simp [good]
  have good_measure : μ good = 1 - μ goodᶜ := by
    simpa only [compl_compl, measure_univ] using
      (measure_compl good_measurable.compl (measure_ne_top μ goodᶜ))
  calc
    ENNReal.ofReal (999 / 1000 : ℝ) = 1 - ENNReal.ofReal (1 / 1000 : ℝ) := by
      rw [← ENNReal.ofReal_one, ← ENNReal.ofReal_sub 1 (by norm_num : (0 : ℝ) ≤ 1 / 1000)]
      norm_num
    _ ≤ 1 - μ goodᶜ := tsub_le_tsub_left bad_union_bound 1
    _ = μ good := good_measure.symm

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceRowLaw
