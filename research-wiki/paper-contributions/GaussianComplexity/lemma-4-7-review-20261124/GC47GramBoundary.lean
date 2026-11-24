import GC47FullGram

/-! The first positive-degree grid satisfying the source frequency condition.
At d=4 and q=1, the threshold exceeds 1/2 and the two source Gram bounds
still hold simultaneously with probability at least 199/200. -/
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGramWitness

theorem gram_probability_four_one :
    (1 : ℝ)/2 < queryThreshold 2048 4 1 ∧
    (199/200 : ℝ) ≤ (gaussianStarts 4 1).real (gramGood 4 1 (queryThreshold 2048 4 1)) := by
  constructor
  · have hl : (3 : ℝ)/4 ≤ Real.log 4 := by
      convert Real.one_sub_inv_le_log_of_pos (x := (4 : ℝ)) (by norm_num) using 1
      norm_num
    have hs := Real.sqrt_nonneg (Real.log 4)
    norm_num [queryThreshold]
    nlinarith [sq_nonneg (Real.log 4)]
  · exact simultaneous_gram_concentration_full (by decide)

#print axioms gram_probability_four_one
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGramWitness
