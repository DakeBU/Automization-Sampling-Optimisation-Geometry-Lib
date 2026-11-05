import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Function.LocallyIntegrable

/-!
# Actual mixed Gaussian densities

The density notation of Zhou--Suzuki, arXiv:2610.20492v1, Appendix B.2
introduction and B.2.3, is realized by actual conditioned-Haar averages.
The chosen representatives are nonnegative measurable Lebesgue L1 functions
of mass one and define exactly the actual Gaussian bind mixtures.
Source densities are a.e. objects; no pointwise equality to a different
arbitrary source representative is asserted. Pointwise inner L1 is proved,
so totalized Bochner integration is not used as a fallback.
TV/affinity comparison, Eq25, products and amplification remain separate.
-/

open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
set_option autoImplicit false

theorem actual_mixture_densities {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let qpos : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νpos
    let qneg : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂νneg
    (∀ x, 0 ≤ qpos x ∧ 0 ≤ qneg x) ∧
    Measurable qpos ∧ Measurable qneg ∧
    Integrable qpos volume ∧ Integrable qneg volume ∧
    (∫ x, qpos x) = 1 ∧ (∫ x, qneg x) = 1 ∧
    νpos.bind γ = volume.withDensity (fun x => ENNReal.ofReal (qpos x)) ∧
    νneg.bind γ = volume.withDensity (fun x => ENNReal.ofReal (qneg x)) := by
  classical
  dsimp only
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let E := EuclideanSpace ℝ (Fin n)
  let μ := orthogonalHaar n
  let νpos := (2 : ℝ≥0∞) • μ.restrict
    {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let νneg := (2 : ℝ≥0∞) • μ.restrict
    {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let γ : G → Measure E := fun O => ProbabilityTheory.multivariateGaussian (0 : E)
    (singleBlockPrecision κ O)⁻¹
  let p : G → E → ℝ := fun O x =>
    Real.sqrt (singleBlockPrecision κ O).det / (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  have hlaws := GaussianMixtureLaws.actual_mixture_laws hn hκ
  have hγ : Measurable γ := hlaws.1
  let : IsProbabilityMeasure (νpos.bind γ) := hlaws.2.1
  let : IsProbabilityMeasure (νneg.bind γ) := hlaws.2.2.1
  have hpriors := DeterminantComponents.component_probabilities
    (lt_of_lt_of_le (by decide : 0 < 3) hn)
  let : IsProbabilityMeasure νpos := hpriors.2.2.1
  let : IsProbabilityMeasure νneg := hpriors.2.2.2
  have hAc : Continuous (fun O : G => singleBlockPrecision κ O) := by
    unfold singleBlockPrecision
    exact continuous_const.sub
      ((continuous_subtype_val.add continuous_subtype_val.matrix_transpose).const_smul
        ((κ - 1) / 4))
  have hpc : Continuous (Function.uncurry p) := by
    dsimp only [p, Function.uncurry, E]
    fun_prop
  have hp0 (O : G) (x : E) : 0 ≤ p O x := by dsimp [p]; positivity
  have hd (O : G) : γ O = (volume : Measure E).withDensity
      (fun x => ENNReal.ofReal (p O x)) :=
    GaussianLawDensity.gaussian_law_eq_density hn hκ O
  -- One internal construction is used for each of the two actual priors.
  have hdata (ν : Measure G) [IsProbabilityMeasure ν]
      [IsProbabilityMeasure (ν.bind γ)] :
      let q : E → ℝ := fun x => ∫ O, p O x ∂ν
      (∀ x, 0 ≤ q x) ∧ Measurable q ∧ Integrable q volume ∧
        (∫ x, q x) = 1 ∧
        ν.bind γ = volume.withDensity (fun x => ENNReal.ofReal (q x)) := by
    let q : E → ℝ := fun x => ∫ O, p O x ∂ν
    have hpi (x : E) : Integrable (fun O => p O x) ν := by
      have hpx : Continuous (fun O : G => p O x) :=
        hpc.comp (continuous_id.prodMk continuous_const)
      simpa only [integrableOn_univ] using
        (ContinuousOn.integrableOn_compact (μ := ν) isCompact_univ hpx.continuousOn)
    have hq0 (x : E) : 0 ≤ q x := integral_nonneg (fun O => hp0 O x)
    have hqm : Measurable q :=
      (hpc.stronglyMeasurable.integral_prod_left (μ := ν)).measurable
    have hpm : Measurable (Function.uncurry (fun O x => ENNReal.ofReal (p O x))) :=
      ENNReal.measurable_ofReal.comp hpc.measurable
    have hmeasure : ν.bind γ = (volume : Measure E).withDensity
        (fun x => ENNReal.ofReal (q x)) := by
      apply Measure.ext
      intro B hB
      rw [Measure.bind_apply hB hγ.aemeasurable, withDensity_apply _ hB]
      calc
        (∫⁻ O, γ O B ∂ν) =
            ∫⁻ O, (∫⁻ x in B, ENNReal.ofReal (p O x) ∂(volume : Measure E)) ∂ν := by
          apply lintegral_congr
          intro O
          rw [hd O, withDensity_apply _ hB]
        _ = ∫⁻ x in B, (∫⁻ O, ENNReal.ofReal (p O x) ∂ν) ∂(volume : Measure E) :=
          lintegral_lintegral_swap hpm.aemeasurable
        _ = ∫⁻ x in B, ENNReal.ofReal (q x) := by
          apply lintegral_congr
          intro x
          exact (ofReal_integral_eq_lintegral_ofReal (hpi x)
            (Filter.Eventually.of_forall (fun O => hp0 O x))).symm
    have hmassNN : (∫⁻ x, ENNReal.ofReal (q x)) = 1 := by
      have hu := congrArg (fun M : Measure E => M Set.univ) hmeasure
      simpa only [measure_univ, withDensity_apply _ MeasurableSet.univ,
        Measure.restrict_univ] using hu.symm
    have hqi : Integrable q volume :=
      (lintegral_ofReal_ne_top_iff_integrable hqm.aestronglyMeasurable
        (Filter.Eventually.of_forall hq0)).mp (by rw [hmassNN]; exact ENNReal.one_ne_top)
    have hmass : (∫ x, q x) = 1 := by
      rw [integral_eq_lintegral_of_nonneg_ae
        (Filter.Eventually.of_forall hq0) hqm.aestronglyMeasurable, hmassNN]
      simp
    exact ⟨hq0, hqm, hqi, hmass, hmeasure⟩
  have hpos := hdata νpos
  have hneg := hdata νneg
  exact ⟨(fun x => ⟨hpos.1 x, hneg.1 x⟩), hpos.2.1, hneg.2.1,
    hpos.2.2.1, hneg.2.2.1, hpos.2.2.2.1, hneg.2.2.2.1,
    hpos.2.2.2.2, hneg.2.2.2.2⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
