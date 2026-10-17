import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianMixtureLaws

-- The source endpoint gives an actual measurable Gaussian family.
example : Measurable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
    multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3)) (singleBlockPrecision 4 O)⁻¹) :=
  (actual_mixture_laws (by decide : 3 ≤ 3) (by norm_num : (4 : ℝ) ≤ 4)).1

-- The radial test at ell=0 is the constant one: integrate it under the actual
-- positive mixture, at the smallest source dimension and condition parameter.
example : (∫ _ : EuclideanSpace ℝ (Fin 3), (1 : ℝ) ∂
    (((2 : ℝ≥0∞) • (orthogonalHaar 3).restrict
      {O | (O : Matrix (Fin 3) (Fin 3) ℝ).det = 1}).bind
        (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
          (singleBlockPrecision 4 O)⁻¹))) = 1 := by
  let := (actual_mixture_laws (by decide : 3 ≤ 3) (by norm_num : (4 : ℝ) ≤ 4)).2.1
  simp

-- The negative mixture is independently a genuine probability at another
-- source input; this consumes its probability result in a Bochner expectation.
example : (∫ _ : EuclideanSpace ℝ (Fin 4), (1 : ℝ) ∂
    (((2 : ℝ≥0∞) • (orthogonalHaar 4).restrict
      {O | (O : Matrix (Fin 4) (Fin 4) ℝ).det = -1}).bind
        (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 4))
          (singleBlockPrecision 9 O)⁻¹))) = 1 := by
  let := (actual_mixture_laws (by decide : 3 ≤ 4) (by norm_num : (4 : ℝ) ≤ 9)).2.2.1
  simp

-- A concrete nontrivial Borel event evaluates through the actual negative law.
example :
    (((2 : ℝ≥0∞) • (orthogonalHaar 3).restrict
      {O | (O : Matrix (Fin 3) (Fin 3) ℝ).det = -1}).bind
        (fun O => multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
          (singleBlockPrecision 4 O)⁻¹))
      (Metric.ball (0 : EuclideanSpace ℝ (Fin 3)) 1) =
    ∫⁻ O, (multivariateGaussian (0 : EuclideanSpace ℝ (Fin 3))
      (singleBlockPrecision 4 O)⁻¹) (Metric.ball 0 1)
      ∂((2 : ℝ≥0∞) • (orthogonalHaar 3).restrict
        {O | (O : Matrix (Fin 3) (Fin 3) ℝ).det = -1}) := by
  exact (actual_mixture_laws (by decide : 3 ≤ 3) (by norm_num : (4 : ℝ) ≤ 4)).2.2.2.2
    _ Metric.isOpen_ball.measurableSet

#check actual_mixture_laws
#print axioms actual_mixture_laws
