import AutoSamplingTheory.ExampleCases.SampleWiki.Cases.RankOneCovarianceComplement

open AutoSamplingTheory.ExampleCases.SampleWiki.Cases.RankOneCovarianceComplement

example : ∃ P : ℝ →L[ℝ] ℝ, P.IsPositive ∧
    P.adjoint.comp P + InnerProductSpace.rankOne ℝ (0 : ℝ) 0 =
      ContinuousLinearMap.id ℝ ℝ :=
  exists_positive_complement 0 (by simp)

example : ∃ P : ℝ →L[ℝ] ℝ, P.IsPositive ∧
    P.adjoint.comp P + InnerProductSpace.rankOne ℝ (1 : ℝ) 1 =
      ContinuousLinearMap.id ℝ ℝ :=
  exists_positive_complement 1 (by simp)

#print axioms exists_positive_complement
