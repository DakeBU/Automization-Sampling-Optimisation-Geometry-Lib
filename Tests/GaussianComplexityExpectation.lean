import AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation
import Mathlib.Tactic.NormNum.RealSqrt

open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianExpectation

-- Endpoint ell=0: the actual test expectation yields the real density integral 1.
example (O : Matrix.orthogonalGroup (Fin 3) ℝ) :
    (∫ x : EuclideanSpace ℝ (Fin 3),
      Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (3 / 2 : ℝ) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ (singleBlockPrecision 4 O *ᵥ WithLp.ofLp x)) / 2)) = 1 := by
  have h := ((actual_gaussian_transform (n := 3) (by decide) (κ := 4) (by norm_num)
    (ℓ := 0) (by norm_num)).1 O).2.2
  norm_num only [Nat.cast_ofNat, neg_zero, zero_mul, Real.exp_zero, one_mul] at h
  simpa using h.symm

-- The endpoint signed expectation is genuinely Haar L1, not a default integral.
example : Integrable (fun O : Matrix.orthogonalGroup (Fin 3) ℝ =>
    (O : Matrix (Fin 3) (Fin 3) ℝ).det) (orthogonalHaar 3) := by
  have h := (actual_gaussian_transform (n := 3) (by decide) (κ := 4) (by norm_num)
    (ℓ := 0) (by norm_num)).2.1
  simpa using h

-- The nonconstant ell=1 test uses actual Gaussian integrals and exact -1/4.
example :
    (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      (O : Matrix (Fin 4) (Fin 4) ℝ).det *
        (∫ x : EuclideanSpace ℝ (Fin 4), Real.exp (-‖x‖ ^ 2)
          ∂multivariateGaussian (0 : EuclideanSpace ℝ (Fin 4)) (singleBlockPrecision 4 O)⁻¹)
      ∂orthogonalHaar 4) =
      (-1 / 4 : ℝ) * (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
        (3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0 - 1) /
          (9 - 3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0) ^ (2 : ℝ)
        ∂orthogonalHaar 4) := by
  have h := (actual_gaussian_transform (n := 4) (by decide) (κ := 4) (by norm_num)
    (ℓ := 1) (by norm_num)).2.2
  norm_num [Real.rpow_two] at h ⊢
  exact h

#print axioms actual_gaussian_transform
