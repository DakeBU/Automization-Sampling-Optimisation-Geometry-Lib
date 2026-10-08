import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianComplementaryNoise

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianComplementaryNoise

-- Exercise singular maps and different-dimensional (zero-dimensional) input.
example : ((stdGaussian ℝ).prod (stdGaussian (EuclideanSpace ℝ (Fin 0)))).map
    (fun p => p.1 + (0 : ℝ)) = stdGaussian ℝ := by
  exact map_stdGaussian_product_of_adjoint_norm_sq
    (ContinuousLinearMap.id ℝ ℝ) (0 : EuclideanSpace ℝ (Fin 0) →L[ℝ] ℝ)
    (by intro t; simp [ContinuousLinearMap.adjoint_id])

#print axioms map_stdGaussian_product_of_adjoint_norm_sq
