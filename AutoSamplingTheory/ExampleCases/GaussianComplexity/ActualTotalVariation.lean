import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
import AutoSamplingTheory.TechnicalLemmas.Probability.KernelTotalVariation
import Mathlib.Probability.Distributions.Bernoulli
/-!
# The radial test bounds TV of the actual mixtures

Zhou--Suzuki, arXiv:2610.20492v1, Section2 accuracy convention and AppendixB2.2
Eq20. All source objects are literal: full Haar, twice-restricted sign priors,
actual Gaussian bind mixtures, and the normalized Euclidean Gaussian density.
The factor-one bounded-test estimate is obtained by applying the identical
compiled Markov TV contraction node to a Bernoulli test kernel. Measurability,
probability, Bochner L1, density identification and the real event supremum
conditions are internal. No Poisson estimate, product, transcript, cost or main
query lower bound is claimed.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation
theorem actual_radial_test_tv {n : ℕ} (hn : 3 ≤ n) {κ : ℝ}
    (hκ : 4 ≤ κ) {ℓ : ℝ} (hℓ : 0 ≤ ℓ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let Ppos := νpos.bind γ
    let Pneg := νneg.bind γ
    let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    2 * |∫ O : Matrix.orthogonalGroup (Fin n) ℝ,
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x) ∂μ| ≤
      sSup {z : ℝ | ∃ B : Set (EuclideanSpace ℝ (Fin n)),
        MeasurableSet B ∧ z = |Ppos.real B - Pneg.real B|} := by
  classical
  dsimp only
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let E := EuclideanSpace ℝ (Fin n)
  let μ := orthogonalHaar n
  let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
  let Ppos := νpos.bind γ
  let Pneg := νneg.bind γ
  let t : EuclideanSpace ℝ (Fin n) → ℝ := fun x => Real.exp (-ℓ * ‖x‖ ^ 2)
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let f : G → ℝ := fun O => ∫ x, t x ∂γ O
  have hlaws := actual_mixture_laws hn hκ
  let : IsProbabilityMeasure Ppos := hlaws.2.1
  let : IsProbabilityMeasure Pneg := hlaws.2.2.1
  have hgap := actual_mixture_expectation_gap hn hκ hℓ
  have htc : Continuous t := by dsimp [t]; fun_prop
  have ht0 (x : E) : 0 ≤ t x := (Real.exp_pos _).le
  have ht1 (x : E) : t x ≤ 1 := by
    exact Real.exp_le_one_iff.mpr
      (mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr hℓ) (sq_nonneg _))
  have htnorm (x : E) : ‖t x‖ ≤ 1 := by
    simpa only [Real.norm_eq_abs, abs_of_nonneg (ht0 x)] using ht1 x
  have hp0 (O : G) (x : E) : 0 ≤ p O x := by dsimp [p]; positivity
  have hpm (O : G) : Measurable (fun x => ENNReal.ofReal (p O x)) := by
    dsimp [p]; fun_prop
  have hpfin (O : G) : ∀ᵐ x ∂(volume : Measure E),
      ENNReal.ofReal (p O x) < ⊤ :=
    Filter.Eventually.of_forall fun _ => ENNReal.ofReal_lt_top
  have hpoint (O : G) :
      Integrable (fun x => t x * p O x) volume ∧
        f O = ∫ x, t x * p O x := by
    let : IsProbabilityMeasure (γ O) := by dsimp [γ]; infer_instance
    have htL : Integrable t (γ O) :=
      (integrable_const (1 : ℝ)).mono' htc.aestronglyMeasurable
        (Filter.Eventually.of_forall htnorm)
    have hd : γ O = volume.withDensity (fun x => ENNReal.ofReal (p O x)) :=
      gaussian_law_eq_density hn hκ O
    have htd : Integrable t (volume.withDensity (fun x => ENNReal.ofReal (p O x))) :=
      hd ▸ htL
    have hw := (integrable_withDensity_iff (hpm O) (hpfin O)).mp htd
    refine ⟨?_, ?_⟩
    · simpa only [ENNReal.toReal_ofReal (hp0 O _)] using hw
    · change (∫ x, t x ∂γ O) = _
      rw [hd, integral_withDensity_eq_integral_toReal_smul (hpm O) (hpfin O)]
      apply integral_congr_ae
      exact Filter.Eventually.of_forall fun x => by
        change (ENNReal.ofReal (p O x)).toReal * t x = t x * p O x
        rw [ENNReal.toReal_ofReal (hp0 O x), mul_comm]
  have hsign (O : G) : (O : Matrix (Fin n) (Fin n) ℝ).det = 1 ∨
      (O : Matrix (Fin n) (Fin n) ℝ).det = -1 := by
    have h := congrArg Matrix.det
      ((Matrix.mem_orthogonalGroup_iff (Fin n) ℝ).mp O.property)
    rw [Matrix.det_mul, Matrix.det_transpose, Matrix.det_one] at h
    exact mul_self_eq_one_iff.mp h
  have hparts :
      Integrable f (μ.restrict {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}) ∧
      Integrable f (μ.restrict {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}) := by
    constructor
    · exact (integrable_smul_measure (by norm_num : (2 : ℝ≥0∞) ≠ 0)
        (by norm_num : (2 : ℝ≥0∞) ≠ ⊤)).mp hgap.2.2.1
    · exact (integrable_smul_measure (by norm_num : (2 : ℝ≥0∞) ≠ 0)
        (by norm_num : (2 : ℝ≥0∞) ≠ ⊤)).mp hgap.2.2.2.1
  have hunion : {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = 1} ∪
      {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = -1} = Set.univ := by
    exact Set.eq_univ_iff_forall.mpr hsign
  have hfL : Integrable f μ := by
    have hU := integrableOn_union.mpr hparts
    simpa only [hunion, integrableOn_univ] using hU
  have hdetm : Continuous (fun O : G => (O : Matrix (Fin n) (Fin n) ℝ).det) := by
    fun_prop
  have hdetb (O : G) : ‖(O : Matrix (Fin n) (Fin n) ℝ).det‖ ≤ 1 := by
    rcases hsign O with h | h <;> simp [h]
  have hHactualL : Integrable
      (fun O : G => (O : Matrix (Fin n) (Fin n) ℝ).det * f O) μ :=
    hfL.bdd_mul hdetm.aestronglyMeasurable (Filter.Eventually.of_forall hdetb)
  have hHdensityL : Integrable (fun O : G =>
      (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)) μ := by
    apply hHactualL.congr
    exact Filter.Eventually.of_forall fun O => by
      change (O : Matrix (Fin n) (Fin n) ℝ).det * f O =
        (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)
      rw [(hpoint O).2]
  have hH : (∫ O : G, (O : Matrix (Fin n) (Fin n) ℝ).det * f O ∂μ) =
      ∫ O : G, (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x) ∂μ := by
    apply integral_congr_ae
    exact Filter.Eventually.of_forall fun O => by
      change (O : Matrix (Fin n) (Fin n) ℝ).det * f O =
        (O : Matrix (Fin n) (Fin n) ℝ).det * (∫ x, t x * p O x)
      rw [(hpoint O).2]
  let D : Set ℝ := {z | ∃ B : Set E, MeasurableSet B ∧
    z = |Ppos.real B - Pneg.real B|}
  have hDne : D.Nonempty := ⟨0, ∅, MeasurableSet.empty, by simp⟩
  have hDbd : BddAbove D := by
    refine ⟨1, ?_⟩
    rintro z ⟨B, hB, rfl⟩
    have hp0 : 0 ≤ Ppos.real B := measureReal_nonneg
    have hp1 : Ppos.real B ≤ 1 := measureReal_le_one
    have hn0 : 0 ≤ Pneg.real B := measureReal_nonneg
    have hn1 : Pneg.real B ≤ 1 := measureReal_le_one
    exact abs_le.mpr ⟨by linarith, by linarith⟩
  have hδ (B : Set E) (hB : MeasurableSet B) :
      |Ppos.real B - Pneg.real B| ≤ sSup D :=
    le_csSup hDbd ⟨B, hB, rfl⟩
  let b : E → unitInterval := fun x => ⟨t x, ht0 x, ht1 x⟩
  have hbc : Continuous b := by dsimp [b]; fun_prop
  let K : Kernel E ℝ := ⟨fun x => bernoulliMeasure (1 : ℝ) 0 (b x), by
    refine Measure.measurable_of_measurable_coe _ fun B hB => ?_
    simp only [bernoulliMeasure_apply _ hB]
    split_ifs <;> fun_prop⟩
  let : IsMarkovKernel K := ⟨fun x => by
    change IsProbabilityMeasure (bernoulliMeasure (1 : ℝ) 0 (b x))
    infer_instance⟩
  have hKtest (x : E) : (K x).real {1} = t x := by
    exact bernoulliMeasure_real_apply_of_mem_of_notMem (b x)
      (measurableSet_singleton 1) (by simp) (by norm_num)
  have happly (ρ : Measure E) [IsProbabilityMeasure ρ] :
      (K ∘ₘ ρ).real {1} = ∫ x, t x ∂ρ := by
    change (Measure.bind ρ K {1}).toReal = _
    rw [Measure.bind_apply (measurableSet_singleton 1) K.aemeasurable]
    calc
      _ = ∫ x, (K x {1}).toReal ∂ρ :=
        (integral_toReal (K.measurable_coe (measurableSet_singleton 1)).aemeasurable
          (Filter.Eventually.of_forall fun x => measure_lt_top (K x) {1})).symm
      _ = _ := integral_congr_ae (Filter.Eventually.of_forall hKtest)
  have htest := AutoSamplingTheory.TechnicalLemmas.Probability.KernelTotalVariation.abs_real_comp_sub_le
    Ppos Pneg K hδ {1} (measurableSet_singleton 1)
  rw [happly Ppos, happly Pneg] at htest
  have hgap' : (∫ x, t x ∂Ppos) - (∫ x, t x ∂Pneg) =
      2 * (∫ O : G, (O : Matrix (Fin n) (Fin n) ℝ).det *
        (∫ x, t x * p O x) ∂μ) := by
    exact hgap.2.2.2.2.2.2.trans (congrArg (fun y : ℝ => 2 * y) hH)
  rw [hgap', abs_mul, abs_of_pos (by norm_num : (0 : ℝ) < 2)] at htest
  exact htest
end AutoSamplingTheory.ExampleCases.GaussianComplexity.ActualTotalVariation
