import AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
open Matrix MeasureTheory
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents

-- Both literal priors are actual probabilities at the new positive-dimension endpoint.
example : IsProbabilityMeasure ((2 : ℝ≥0∞) • (orthogonalHaar 1).restrict
    {O | (O : Matrix (Fin 1) (Fin 1) ℝ).det = 1}) := by
  exact (component_probabilities (by decide : 0 < 1)).2.2.1

example : IsProbabilityMeasure ((2 : ℝ≥0∞) • (orthogonalHaar 1).restrict
    {O | (O : Matrix (Fin 1) (Fin 1) ℝ).det = -1}) := by
  exact (component_probabilities (by decide : 0 < 1)).2.2.2

-- The literal negative-event mass at the source's smallest application dimension.
example : (orthogonalHaar 3)
    {O | (O : Matrix (Fin 3) (Fin 3) ℝ).det = -1} = (2 : ℝ≥0∞)⁻¹ := by
  exact (component_probabilities (by decide : 0 < 3)).2.1

-- Dimension zero is a genuine excluded boundary: the negative event is empty.
example : (orthogonalHaar 0)
    {O | (O : Matrix (Fin 0) (Fin 0) ℝ).det = -1} = 0 := by
  have h : {O : Matrix.orthogonalGroup (Fin 0) ℝ |
      (O : Matrix (Fin 0) (Fin 0) ℝ).det = -1} = ∅ := by
    ext O
    norm_num [Matrix.det_isEmpty]
  rw [h]
  exact measure_empty

#check component_probabilities
#print axioms component_probabilities
