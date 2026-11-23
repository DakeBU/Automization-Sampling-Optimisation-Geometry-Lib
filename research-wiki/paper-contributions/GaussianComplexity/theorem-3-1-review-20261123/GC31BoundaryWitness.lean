import GC31LowerBound

/-! Boundary checks for the zero-query obstruction and Theorem 3.1. -/

open MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LowerBoundWitness

/-- Even a zero-query procedure returning a full standard Gaussian seed has an
admissible target whose distance strictly exceeds the endpoint 1/16. -/
def returnSeed : Algorithm 1 (E 1) (E 1) where
  start := id
  next _ := .inl ()
  update s _ _ := s
  output := id
  measurable_start := measurable_id
  measurable_next := measurable_const
  measurable_update := measurable_fst
  measurable_output := measurable_id

theorem zero_query_standard_seed_fails : ∃ A : Precision 1, Admissible 4 A ∧
    (1/16 : ℝ) < eventTV (returnSeed.outputLaw (stdGaussian (E 1)) 0 A) (targetLaw A) := by
  by_contra! h
  have hbad := positive_budget_of_accuracy (d := 1) (T := 0) (ε := (1/16 : ℝ))
    (κ := 4) (by decide) le_rfl le_rfl (stdGaussian (E 1)) returnSeed h
  omega

/-- The endpoint tolerance and a square condition number give a bound strictly
larger than two, even with arbitrary internal randomness and state. -/
theorem two_queries_do_not_suffice {Seed State : Type*}
    [MeasurableSpace Seed] [MeasurableSpace State] (ρ : Measure Seed) [IsProbabilityMeasure ρ]
    (alg : Algorithm 513 Seed State) : ∃ A, Admissible 263169 A ∧
      (1/16 : ℝ) < eventTV (alg.outputLaw ρ 2 A) (targetLaw A) := by
  by_contra! h
  have hlb := algorithm_query_lower_bound (d := 513) (T := 2) (κ := 263169) (ε := 1/16)
    (by decide) (by norm_num) (by norm_num) le_rfl ρ alg h
  have hs : Real.sqrt 263169 = 513 := Real.sqrt_eq_iff_mul_self_eq_of_pos (by norm_num) |>.mpr (by norm_num)
  have hl : (1 : ℝ) ≤ Real.log 17 := (Real.le_log_iff_exp_le (by norm_num)).mpr
    (Real.exp_one_lt_three.le.trans (by norm_num))
  rw [hs] at hlb
  norm_num at hlb
  rw [min_eq_left (by linarith : (513 : ℝ) ≤ 513 * Real.log 17)] at hlb
  norm_num at hlb

#print axioms zero_query_standard_seed_fails
#print axioms two_queries_do_not_suffice

end AutoSamplingTheory.ExampleCases.GaussianComplexity.LowerBoundWitness
