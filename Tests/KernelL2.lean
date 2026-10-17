import AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2

#check AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2.invariant_kernel_l2_operator
#print axioms AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2.invariant_kernel_l2_operator

open MeasureTheory ProbabilityTheory

-- Zero target on the empty state space remains a valid finite invariant target.
example : ∃ A : Lp ℝ 2 (0 : Measure Empty) →L[ℝ] Lp ℝ 2 (0 : Measure Empty), ‖A‖ ≤ 1 := by
  obtain ⟨A, hA, _⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.KernelL2.invariant_kernel_l2_operator
      (0 : Measure Empty) Kernel.id (by simp [Kernel.Invariant])
  exact ⟨A, hA⟩
