import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-!
# Actual determinant-conditioned Gaussian mixture laws

Zhou--Suzuki arXiv:2610.20492v1, Section 3.1 single-block definition before Eq6,
Section2 determinant priors and AppendixB2.2. The source leaves measurable-family
and probability-construction bookkeeping implicit. Those producers are proved
here for the actual Gaussian constructor, using the identical law-density and
component-prior nodes. Product targets, H-to-TV and main bounds are separate.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianLawDensity
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws

theorem actual_mixture_laws {n : ℕ} (hn : 3 ≤ n) {κ : ℝ} (hκ : 4 ≤ κ) :
    let μ := orthogonalHaar n
    let νpos := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
    let νneg := (2 : ℝ≥0∞) • μ.restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin n) ℝ → Measure (EuclideanSpace ℝ (Fin n)) :=
      fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ O)⁻¹
    Measurable γ ∧ IsProbabilityMeasure (νpos.bind γ) ∧
      IsProbabilityMeasure (νneg.bind γ) ∧
      (∀ B : Set (EuclideanSpace ℝ (Fin n)), MeasurableSet B →
        (νpos.bind γ) B = ∫⁻ O, γ O B ∂νpos) ∧
      (∀ B : Set (EuclideanSpace ℝ (Fin n)), MeasurableSet B →
        (νneg.bind γ) B = ∫⁻ O, γ O B ∂νneg) := by
  classical
  dsimp only
  let G := Matrix.orthogonalGroup (Fin n) ℝ
  let E := EuclideanSpace ℝ (Fin n)
  let μ := orthogonalHaar n
  let νpos := (2 : ℝ≥0∞) • μ.restrict
    {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = 1}
  let νneg := (2 : ℝ≥0∞) • μ.restrict
    {O : G | (O : Matrix (Fin n) (Fin n) ℝ).det = -1}
  let γ : G → Measure E := fun O =>
    multivariateGaussian (0 : E) (singleBlockPrecision κ O)⁻¹
  let p : G → E → ℝ := fun O x =>
    Real.sqrt (singleBlockPrecision κ O).det / (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  have hAc : Continuous (fun O : G => singleBlockPrecision κ O) := by
    unfold singleBlockPrecision
    exact continuous_const.sub
      ((continuous_subtype_val.add continuous_subtype_val.matrix_transpose).const_smul ((κ - 1) / 4))
  have hpc : Continuous (fun z : G × E => p z.1 z.2) := by
    dsimp only [p, E]
    fun_prop
  have hpm : Measurable (Function.uncurry (fun O x => ENNReal.ofReal (p O x))) :=
    ENNReal.measurable_ofReal.comp hpc.measurable
  have hd : γ = fun O => (volume : Measure E).withDensity
      (fun x => ENNReal.ofReal (p O x)) := by
    funext O
    exact gaussian_law_eq_density hn hκ O
  have hm : Measurable γ := by
    rw [hd]
    exact measurable_withDensity hpm
  have hpriors := component_probabilities (lt_of_lt_of_le (by decide : 0 < 3) hn)
  let : IsProbabilityMeasure νpos := hpriors.2.2.1
  let : IsProbabilityMeasure νneg := hpriors.2.2.2
  have hprob (O : G) : IsProbabilityMeasure (γ O) := by
    dsimp [γ]
    infer_instance
  refine ⟨hm, isProbabilityMeasure_bind hm.aemeasurable
    (Filter.Eventually.of_forall hprob),
    isProbabilityMeasure_bind hm.aemeasurable (Filter.Eventually.of_forall hprob), ?_, ?_⟩
  · intro B hB
    exact Measure.bind_apply hB hm.aemeasurable
  · intro B hB
    exact Measure.bind_apply hB hm.aemeasurable

end AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
