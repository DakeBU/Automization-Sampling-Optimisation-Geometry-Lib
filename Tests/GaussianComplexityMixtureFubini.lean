import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini
import Mathlib.Tactic.NormNum.RealSqrt

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureFubini

-- The endpoint ell=0 still has genuine joint absolute L1; n=3 uses a real half power.
example :
    Integrable (fun z : Matrix.orthogonalGroup (Fin 3) ℝ × EuclideanSpace ℝ (Fin 3) =>
      (z.1 : Matrix (Fin 3) (Fin 3) ℝ).det *
        (Real.sqrt (singleBlockPrecision 4 z.1).det / (2 * Real.pi) ^ (3 / 2 : ℝ) *
          Real.exp (-((WithLp.ofLp z.2) ⬝ᵥ
            (singleBlockPrecision 4 z.1 *ᵥ WithLp.ofLp z.2)) / 2)))
      ((orthogonalHaar 3).prod volume) := by
  have h := (literal_mixture_transform (n := 3) (by decide) (κ := 4) (by norm_num)
    (ℓ := 0) (by norm_num)).1
  norm_num only [Nat.cast_ofNat, neg_zero, zero_mul, Real.exp_zero, one_mul] at h
  exact h

-- At n=4,kappa=4,ell=1 the closed transform coefficient is exactly -1/4.
example :
    let p : Matrix.orthogonalGroup (Fin 4) ℝ → EuclideanSpace ℝ (Fin 4) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision 4 O).det / (2 * Real.pi) ^ (2 : ℝ) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision 4 O *ᵥ WithLp.ofLp x)) / 2)
    (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      (O : Matrix (Fin 4) (Fin 4) ℝ).det *
        (∫ x : EuclideanSpace ℝ (Fin 4), Real.exp (-‖x‖ ^ 2) * p O x)
        ∂orthogonalHaar 4) =
      (-1 / 4 : ℝ) *
        (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
          (3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0 - 1) /
            (9 - 3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0) ^ (2 : ℝ)
            ∂orthogonalHaar 4) := by
  have h := (literal_mixture_transform (n := 4) (by decide) (κ := 4) (by norm_num)
    (ℓ := 1) (by norm_num)).2.2
  norm_num [Real.rpow_two] at h ⊢
  exact h

#print axioms literal_mixture_transform
