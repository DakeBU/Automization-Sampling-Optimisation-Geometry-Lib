import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad

open MeasureTheory
open scoped NNReal
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianOddLoad

-- The exact public proposition, including integrability and degenerate variance.
example : ∀ {U : ℝ → ℝ} {β a : ℝ} (v : ℝ≥0), Measurable U →
    Function.Odd U → (∀ y, |U y| ≤ β * |y|) → a ∈ Set.Icc (0 : ℝ) 1 →
    Integrable (fun y ↦ Real.exp (-a * U y)) (ProbabilityTheory.gaussianReal 0 v) ∧
      (∫ y, Real.exp (-a * U y) ∂ProbabilityTheory.gaussianReal 0 v) ≤
        Real.exp (β ^ 2 * (v : ℝ) / 2) := gaussian_odd_load_bound

example (v : ℝ≥0) :
    (∫ y, Real.exp (-y) ∂ProbabilityTheory.gaussianReal 0 v) ≤ Real.exp ((v : ℝ) / 2) := by
  simpa using (gaussian_odd_load_bound (U := id) (β := 1) (a := 1) v
    measurable_id (by intro y; rfl) (by intro y; simp) (by norm_num)).2

example {U : ℝ → ℝ} {β : ℝ} (hU : Measurable U) (hodd : Function.Odd U)
    (hbound : ∀ y, |U y| ≤ β * |y|) :
    (∫ y, Real.exp (-U y) ∂ProbabilityTheory.gaussianReal 0 0) ≤ 1 := by
  simpa using (gaussian_odd_load_bound (a := 1) 0 hU hodd hbound (by norm_num)).2

example (v : ℝ≥0) :
    (∫ y : ℝ, Real.exp (0 * y) ∂ProbabilityTheory.gaussianReal 0 v) ≤ 1 := by
  have h := gaussian_odd_load_bound (U := fun _ ↦ 0) (β := 0) (a := 0) v
    measurable_const (by intro y; simp) (by intro y; simp) (by norm_num)
  convert h.2 using 1 <;> norm_num

#print axioms gaussian_odd_load_bound
