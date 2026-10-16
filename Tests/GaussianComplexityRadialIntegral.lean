import AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral
import Mathlib.Tactic.NormNum.RealSqrt

open Matrix MeasureTheory
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.RadialIntegral

/- The source permits ell=0. At O=I and kappa=4 the denominator base is 2,
so this is the genuine standard Gaussian kernel, with finite volume integral. -/
example : Integrable (fun x : EuclideanSpace ℝ (Fin 3) => Real.exp (-‖x‖ ^ 2 / 2)) volume := by
  have hi := (radialized_test_integral (by decide : 3 ≤ 3)
    (by norm_num : 4 ≤ (4 : ℝ)) (by norm_num : 0 ≤ (0 : ℝ))).1
      (1 : Matrix.orthogonalGroup (Fin 3) ℝ)
  dsimp at hi
  norm_num at hi
  convert hi using 1
  funext x
  congr 1
  ring

/- At ell=1 the base is 9-3U. Dimension3 retains the real exponent 3/2;
using natural-number division in the production statement would fail this test. -/
example :
    (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
      (O : Matrix (Fin 3) (Fin 3) ℝ).det * Real.sqrt (singleBlockPrecision (4 : ℝ) O).det *
        (∫ x : EuclideanSpace ℝ (Fin 3),
          Real.exp (-(9 - 3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0) * ‖x‖ ^ 2 / 4))
      ∂orthogonalHaar 3) / (2 * Real.pi) ^ ((3 : ℝ) / 2) =
      (1 / (2 : ℝ) ^ ((3 : ℝ) / 2)) *
        (∫ O : Matrix.orthogonalGroup (Fin 3) ℝ,
          (3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0 - 1) /
            (9 - 3 * (O : Matrix (Fin 3) (Fin 3) ℝ) 0 0) ^ ((3 : ℝ) / 2)
          ∂orthogonalHaar 3) := by
  have hb := (radialized_test_integral (by decide : 3 ≤ 3)
    (by norm_num : 4 ≤ (4 : ℝ)) (by norm_num : 0 ≤ (1 : ℝ))).2.2.2
  norm_num at hb
  simpa only [neg_sub, one_div] using hb

/- The even-dimensional coefficient is negative. The source endpoint ell=0
gives base 5-3U and exactly -1/4, with no remaining pi normalization factor. -/
example :
    (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
      (O : Matrix (Fin 4) (Fin 4) ℝ).det * Real.sqrt (singleBlockPrecision (4 : ℝ) O).det *
        (∫ x : EuclideanSpace ℝ (Fin 4),
          Real.exp (-(5 - 3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0) * ‖x‖ ^ 2 / 4))
      ∂orthogonalHaar 4) / (2 * Real.pi) ^ 2 =
      (-1 / 4) *
        (∫ O : Matrix.orthogonalGroup (Fin 4) ℝ,
          (3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0 - 1) /
            (5 - 3 * (O : Matrix (Fin 4) (Fin 4) ℝ) 0 0) ^ 2
          ∂orthogonalHaar 4) := by
  have hb := (radialized_test_integral (by decide : 3 ≤ 4)
    (by norm_num : 4 ≤ (4 : ℝ)) (by norm_num : 0 ≤ (0 : ℝ))).2.2.2
  norm_num [Real.rpow_natCast] at hb
  simpa only [neg_sub, neg_div, neg_mul] using hb

#print axioms radialized_test_integral
