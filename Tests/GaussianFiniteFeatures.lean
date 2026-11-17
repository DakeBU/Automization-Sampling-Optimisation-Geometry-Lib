import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteFeatureCore

open MeasureTheory ProbabilityTheory
open scoped InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteFeatures

-- Odd degree, negative coefficient, and antipodal directions retain the signed correlation.
example :
    ⟪finiteGaussianHermiteRidgeL2 {1} (fun _ => (-3 : ℝ)) (1 : ℝ),
      finiteGaussianHermiteRidgeL2 {1} (fun _ => (-3 : ℝ)) (-1 : ℝ)⟫_ℝ = -9 := by
  rw [finiteGaussianHermiteRidgeL2_inner _ _ _ _ (by norm_num) (by norm_num)]
  norm_num [real_inner_comm, Real.inner_apply]

-- Degree zero remains present with the probabilists Hermite normalization.
example :
    ⟪finiteGaussianHermiteRidgeL2 {0} (fun _ => (2 : ℝ)) (1 : ℝ),
      finiteGaussianHermiteRidgeL2 {0} (fun _ => (2 : ℝ)) (-1 : ℝ)⟫_ℝ = 4 := by
  rw [finiteGaussianHermiteRidgeL2_inner _ _ _ _ (by norm_num) (by norm_num)]
  norm_num

-- Empty support is the zero class even in a zero-dimensional ambient space.
example (c : ℕ → ℝ) (w : EuclideanSpace ℝ (Fin 0)) :
    finiteGaussianHermiteRidgeL2 ∅ c w = 0 := by
  simp [finiteGaussianHermiteRidgeL2]

-- The smoothness API includes non-unit parameter points, such as the origin.
example : DifferentiableAt ℝ
    (finiteGaussianHermiteRidgeL2 (E := ℝ) {0, 1, 3} (fun j => (j : ℝ) - 2)) 0 :=
  (finiteGaussianHermiteRidgeL2_contDiff _ _).differentiable (by norm_num) 0

#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth.standard_gaussian_polynomial_ridge_L2_smooth
#print axioms gaussianHermiteRidgeL2_contDiff
#print axioms gaussianHermiteRidgeL2_ae
#print axioms finiteGaussianHermiteRidgeL2_inner
#print axioms finiteGaussianHermiteRidgeL2_contDiff
