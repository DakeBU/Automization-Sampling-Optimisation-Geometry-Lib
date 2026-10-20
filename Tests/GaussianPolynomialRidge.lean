import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge

-- Non-even actual ridge features: opposite directions have the same Gaussian L2 norm.
example :
    ∃ hbase : MemLp (fun z : ℝ => z ^ 2 + z) 2 (gaussianReal 0 1),
    ∃ hplus : MemLp (fun x : ℝ => ⟪(1 : ℝ), x⟫_ℝ ^ 2 + ⟪(1 : ℝ), x⟫_ℝ) 2 (stdGaussian ℝ),
    ∃ hminus : MemLp (fun x : ℝ => ⟪(-1 : ℝ), x⟫_ℝ ^ 2 + ⟪(-1 : ℝ), x⟫_ℝ) 2 (stdGaussian ℝ),
      ‖hplus.toLp _‖ = ‖hbase.toLp _‖ ∧ ‖hminus.toLp _‖ = ‖hbase.toLp _‖ := by
  rcases standard_gaussian_polynomial_ridge_uniform_L2 (E := ℝ)
    (Polynomial.X ^ 2 + Polynomial.X) with ⟨hbase, _, hf, hn⟩
  let plus : {w : ℝ // ‖w‖ = 1} := ⟨1, by norm_num⟩
  let minus : {w : ℝ // ‖w‖ = 1} := ⟨-1, by norm_num⟩
  have hp := hf plus
  have hm := hf minus
  have hn1 := (hn plus).1
  have hn2 := (hn minus).1
  simp only [Polynomial.eval_add, Polynomial.eval_pow, Polynomial.eval_X] at hbase hp hm hn1 hn2
  exact ⟨hbase, hp, hm, hn1, hn2⟩

-- The zero polynomial still supplies a nonvacuous base witness and positive bound.
example : ∃ h : MemLp (fun z : ℝ => (0 : Polynomial ℝ).eval z) 2 (gaussianReal 0 1),
    0 < ‖h.toLp _‖ + 1 := by
  rcases standard_gaussian_polynomial_ridge_uniform_L2 (E := ℝ)
    (0 : Polynomial ℝ) with ⟨h, hb, _, _⟩
  exact ⟨h, hb⟩

-- Dimension zero needs no chosen unit vector and preserves the scalar base conclusion.
example : ∃ h : MemLp (fun z : ℝ => (Polynomial.X : Polynomial ℝ).eval z) 2 (gaussianReal 0 1),
    0 < ‖h.toLp _‖ + 1 := by
  rcases standard_gaussian_polynomial_ridge_uniform_L2 (E := EuclideanSpace ℝ (Fin 0))
    (Polynomial.X : Polynomial ℝ) with ⟨h, hb, _, _⟩
  exact ⟨h, hb⟩

#print axioms standard_gaussian_polynomial_ridge_uniform_L2
