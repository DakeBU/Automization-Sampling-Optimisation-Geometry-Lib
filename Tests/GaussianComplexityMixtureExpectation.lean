import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation
open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureExpectation

-- At the smallest source parameters, the zero-tilt test is L1 under the
-- actual negative mixture, rather than under a supplied proxy measure.
example : Integrable (fun x : EuclideanSpace ℝ (Fin 3) => Real.exp (-0 * ‖x‖ ^ 2))
    (((2 : ℝ≥0∞) • (orthogonalHaar 3).restrict
      {O | (O : Matrix (Fin 3) (Fin 3) ℝ).det = -1}).bind
      (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
        (singleBlockPrecision 4 O)⁻¹)) :=
  (actual_mixture_expectation_gap (by decide : 3 ≤ 3)
    (by norm_num : (4 : ℝ) ≤ 4) (by norm_num : (0 : ℝ) ≤ 0)).2.1

-- A nonzero tilt is transported through an actual negative mixture at a
-- second dimension/condition parameter; the conclusion is a real integral.
example :
    let ν := (2 : ℝ≥0∞) • (orthogonalHaar 4).restrict
      {O | (O : Matrix (Fin 4) (Fin 4) ℝ).det = -1}
    let γ : Matrix.orthogonalGroup (Fin 4) ℝ → Measure (EuclideanSpace ℝ (Fin 4)) :=
      fun O => multivariateGaussian 0 (singleBlockPrecision 9 O)⁻¹
    (∫ x, Real.exp (-1 * ‖x‖ ^ 2) ∂ν.bind γ) =
      ∫ O, (∫ x, Real.exp (-1 * ‖x‖ ^ 2) ∂γ O) ∂ν :=
  (actual_mixture_expectation_gap (by decide : 3 ≤ 4)
    (by norm_num : (4 : ℝ) ≤ 9) (by norm_num : (0 : ℝ) ≤ 1)).2.2.2.2.2.1

-- The zero-tilt endpoint forces the actual signed component expectation to
-- vanish: this consumes the gap conclusion and both actual mixture masses.
example :
    let γ : Matrix.orthogonalGroup (Fin 3) ℝ → Measure (EuclideanSpace ℝ (Fin 3)) :=
      fun O => multivariateGaussian 0 (singleBlockPrecision 4 O)⁻¹
    2 * (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det *
        (∫ x, Real.exp (-0 * ‖x‖ ^ 2) ∂γ O) ∂orthogonalHaar 3) = 0 := by
  let hlaws := actual_mixture_laws (by decide : 3 ≤ 3) (by norm_num : (4 : ℝ) ≤ 4)
  let := hlaws.2.1
  let := hlaws.2.2.1
  have hgap := (actual_mixture_expectation_gap (by decide : 3 ≤ 3)
    (by norm_num : (4 : ℝ) ≤ 4) (by norm_num : (0 : ℝ) ≤ 0)).2.2.2.2.2.2
  simpa using hgap.symm

#check actual_mixture_expectation_gap
#print axioms actual_mixture_expectation_gap
