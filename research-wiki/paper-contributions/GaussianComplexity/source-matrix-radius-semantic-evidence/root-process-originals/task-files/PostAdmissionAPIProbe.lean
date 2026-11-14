import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.Analysis.CStarAlgebra.Matrix

open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix Kronecker Matrix.Norms.L2Operator

-- Post-source-admission retrieval/type inspection only. No target proof.
#check AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means
#check AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram
#check InnerProductSpace.norm_rankOne
#check InnerProductSpace.symm_toEuclideanLin_rankOne
#check Matrix.cstar_norm_def
#check Matrix.toEuclideanCLM
#check Matrix.ofLp_toEuclideanCLM
#check ContinuousLinearMap.opNorm_le_bound
#check EuclideanSpace.norm_sq_eq

set_option pp.all true in
#synth Norm (Matrix (Fin 2 × Fin 2) (Fin 2 × Fin 2) ℝ)
