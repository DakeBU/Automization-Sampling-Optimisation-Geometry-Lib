import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
import Mathlib.MeasureTheory.Integral.Bochner.Set
/-!
# Actual mixture test expectations and their signed gap

Zhou--Suzuki arXiv:2610.20492v1 Appendix B.2.2 radial test and half-mass
expectation identity before Eq20, with Section3.1 actual single-block mixtures.
The source omits measure/test interchange bookkeeping; it is supplied here.
Both actual Bochner transports and the exact factor2 gap are proved internally.
The source H is represented by the existing actual Gaussian expectation; its
density identification and Eq21 value are separate existing results. No TV,
product, oracle or main lower bound is asserted here.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
theorem actual_mixture_expectation_gap {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) {ℓ : ℝ} (hℓ : 0 ≤ ℓ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    let f : Matrix.orthogonalGroup (Fin n) ℝ → ℝ := fun O => ∫ x, t x ∂γ O
    Integrable t (νpos.bind γ) ∧ Integrable t (νneg.bind γ) ∧
      Integrable f νpos ∧ Integrable f νneg ∧
      (∫ x, t x ∂νpos.bind γ) = (∫ O, f O ∂νpos) ∧
      (∫ x, t x ∂νneg.bind γ) = (∫ O, f O ∂νneg) ∧
      ((∫ x, t x ∂νpos.bind γ) - (∫ x, t x ∂νneg.bind γ)) =
        2 * (∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
          (O : Matrix (Fin n) (Fin n) ℝ).det * f O ∂μ) := by
  classical
  dsimp only
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let E := EuclideanSpace ℝ (Fin n)
  let μ := orthogonalHaar n
  let Cpos : Set G := {O | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let Cneg : Set G := {O | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let νpos := (2 : ℝ≥0∞) • μ.restrict Cpos
  let νneg := (2 : ℝ≥0∞) • μ.restrict Cneg
  let γ : G → Measure E := fun O => multivariateGaussian (0 : E)
    (singleBlockPrecision κ O)⁻¹
  let t : E → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
  let f : G → ℝ := fun O => ∫ x, t x ∂γ O
  have hlaws := actual_mixture_laws hn hκ
  have hγ : Measurable γ := hlaws.1
  let : IsProbabilityMeasure (νpos.bind γ) := hlaws.2.1
  let : IsProbabilityMeasure (νneg.bind γ) := hlaws.2.2.1
  have hpriors := component_probabilities (lt_of_lt_of_le (by decide : 0 < 3) hn)
  let : IsProbabilityMeasure νpos := hpriors.2.2.1
  let : IsProbabilityMeasure νneg := hpriors.2.2.2
  let : IsProbabilityMeasure μ := (orthogonalHaar_spec n).1
  have hγprob (O : G) : IsProbabilityMeasure (γ O) := by
    dsimp [γ]
    infer_instance
  have htc : Continuous t := by dsimp [t, E]; fun_prop
  have htnn (x : E) : 0 ≤ t x := (Real.exp_pos _).le
  have htb (x : E) : ‖t x‖ ≤ 1 := by
    dsimp [t]
    rw [abs_of_pos (Real.exp_pos _)]
    apply Real.exp_le_one_iff.mpr
    exact mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hℓ) (sq_nonneg _)
  have htL (ρ : Measure E) [IsProbabilityMeasure ρ] : Integrable t ρ :=
    (integrable_const (1 : ℝ)).mono' htc.aestronglyMeasurable
      (Filter.Eventually.of_forall htb)
  let q : G → ℝ≥0∞ := fun O => ∫⁻ x, ENNReal.ofReal (t x) ∂γ O
  have hqm : Measurable q :=
    (Measure.measurable_lintegral (ENNReal.measurable_ofReal.comp htc.measurable)).comp hγ
  have hqle (O : G) : q O ≤ 1 := by
    let := hγprob O
    calc
      q O ≤ ∫⁻ x, (1 : ℝ≥0∞) ∂γ O := by
        apply lintegral_mono
        intro x
        have htupper : t x ≤ 1 :=
          (le_abs_self (t x)).trans (by simpa only [Real.norm_eq_abs] using htb x)
        simpa using ENNReal.ofReal_le_ofReal htupper
      _ = 1 := by simp
  have hqfin (O : G) : q O < ⊤ := (hqle O).trans_lt (by simp)
  have hfq (O : G) : f O = (q O).toReal :=
    integral_eq_lintegral_of_nonneg_ae (Filter.Eventually.of_forall htnn)
      htc.aestronglyMeasurable
  have hfm : Measurable f := by
    have heq : f = fun O => (q O).toReal := funext hfq
    rw [heq]
    exact ENNReal.measurable_toReal.comp hqm
  have hfb (O : G) : ‖f O‖ ≤ 1 := by
    let := hγprob O
    simpa only [f, probReal_univ, mul_one] using
      (norm_integral_le_of_norm_le_const (Filter.Eventually.of_forall htb) :
        ‖∫ x, t x ∂γ O‖ ≤ (1 : ℝ) * (γ O).real Set.univ)
  have hfL (ρ : Measure G) [IsProbabilityMeasure ρ] : Integrable f ρ :=
    (integrable_const (1 : ℝ)).mono' hfm.aestronglyMeasurable
      (Filter.Eventually.of_forall hfb)
  have htrans (ν : Measure G) [IsProbabilityMeasure ν] :
      (∫ x, t x ∂ν.bind γ) = ∫ O, f O ∂ν := by
    have htm : AEMeasurable (fun x => ENNReal.ofReal (t x)) (ν.bind γ) :=
      (ENNReal.measurable_ofReal.comp htc.measurable).aemeasurable
    rw [integral_eq_lintegral_of_nonneg_ae (Filter.Eventually.of_forall htnn)
      htc.aestronglyMeasurable, Measure.lintegral_bind hγ.aemeasurable htm]
    have heq : f = fun O => (q O).toReal := funext hfq
    rw [heq]
    exact (integral_toReal hqm.aemeasurable (Filter.Eventually.of_forall hqfin)).symm
  have hcont : Continuous (fun O : G => (O : Matrix (Fin n) (Fin n) ℝ).det) := by
    fun_prop
  have hpos : MeasurableSet Cpos := (isClosed_eq hcont continuous_const).measurableSet
  have hneg : MeasurableSet Cneg := (isClosed_eq hcont continuous_const).measurableSet
  have hsign (O : G) : (O : Matrix (Fin n) (Fin n) ℝ).det = 1 ∨
      (O : Matrix (Fin n) (Fin n) ℝ).det = -1 := by
    have h := congrArg Matrix.det
      ((Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).mp O.property)
    rw [Matrix.det_mul, Matrix.det_transpose, Matrix.det_one] at h
    exact mul_self_eq_one_iff.mp h
  have hsplit : (∫ O : G, (O : Matrix (Fin n) (Fin n) ℝ).det * f O ∂μ) =
      (∫ O in Cpos, f O ∂μ) - (∫ O in Cneg, f O ∂μ) := by
    calc
      _ = ∫ O, Cpos.indicator f O - Cneg.indicator f O ∂μ := by
        apply integral_congr_ae
        exact Filter.Eventually.of_forall fun O => by
          rcases hsign O with h | h
          · have hp : O ∈ Cpos := h
            have hm : O ∉ Cneg := by change (O : Matrix (Fin n) (Fin n) ℝ).det ≠ -1; rw [h]; norm_num
            simp only [Set.indicator_of_mem hp, Set.indicator_of_notMem hm, h, one_mul, sub_zero]
          · have hm : O ∈ Cneg := h
            have hp : O ∉ Cpos := by change (O : Matrix (Fin n) (Fin n) ℝ).det ≠ 1; rw [h]; norm_num
            simp only [Set.indicator_of_mem hm, Set.indicator_of_notMem hp, h, neg_one_mul, zero_sub]
      _ = _ := by
        rw [integral_sub ((hfL μ).indicator hpos) ((hfL μ).indicator hneg),
          integral_indicator hpos, integral_indicator hneg]
  have hipos : (∫ O, f O ∂νpos) = 2 * (∫ O in Cpos, f O ∂μ) := by
    simp [νpos, integral_smul_measure]
  have hineg : (∫ O, f O ∂νneg) = 2 * (∫ O in Cneg, f O ∂μ) := by
    simp [νneg, integral_smul_measure]
  refine ⟨htL _, htL _, hfL _, hfL _, htrans _, htrans _, ?_⟩
  change (∫ x, t x ∂νpos.bind γ) - (∫ x, t x ∂νneg.bind γ) =
    2 * (∫ O : G, (O : Matrix (Fin n) (Fin n) ℝ).det * f O ∂μ)
  rw [htrans νpos, htrans νneg, hipos, hineg, hsplit]
  ring
end AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
