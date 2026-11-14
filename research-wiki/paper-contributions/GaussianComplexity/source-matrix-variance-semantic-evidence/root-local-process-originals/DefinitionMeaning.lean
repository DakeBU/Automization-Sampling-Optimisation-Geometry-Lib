import Mathlib

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator
set_option pp.universes true

-- Literal standard semantics and actual instances only; no target proof/API retrieval.
#print Matrix
#print Matrix.mul
#print Matrix.PosSemidef
#print Matrix.IsHermitian
#print Matrix.conjTranspose
#print Matrix.vecMulVec
#print Matrix.kronecker
#print Matrix.kroneckerMap
#print MeasureTheory.Integrable
#print MeasureTheory.HasFiniteIntegral
#print MeasureTheory.AEStronglyMeasurable
#print MeasureTheory.integral
#print Set.indicator
#print EuclideanSpace
#print WithLp.toLp
#print ProbabilityTheory.stdGaussian
#print MeasureTheory.Measure.pi

section
variable {d q : ℕ}
#synth Mul
  (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
#synth NormedRing
  (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
#synth NormedSpace ℝ
  (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
#synth CompleteSpace
  (Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ)
#synth IsProbabilityMeasure
  (Measure.pi (fun _ : Fin (q + 1) => stdGaussian (EuclideanSpace ℝ (Fin d))))
#synth SigmaFinite (stdGaussian (EuclideanSpace ℝ (Fin d)))
end
