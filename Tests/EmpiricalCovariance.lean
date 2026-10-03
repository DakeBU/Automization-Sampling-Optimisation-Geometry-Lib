import AutoSamplingTheory.TechnicalLemmas.Probability.EmpiricalCovariance

namespace AutoSamplingTheory.Tests.EmpiricalCovariance

open scoped BigOperators RealInnerProductSpace
open TechnicalLemmas.Probability.EmpiricalCovariance

#check empiricalSecondMoment
#check norm_rankOne_self_eq_sq
#check empiricalSecondMoment_preconcentration

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {κ : Type*} [Fintype κ] [Nonempty κ]
    (population : E →L[ℝ] E) (sample : κ → E) (B : ℝ)
    (hB : 0 ≤ B)
    (hpopulationSymmetric : LinearMap.IsSymmetric (population : E →ₗ[ℝ] E))
    (hpopulationNorm : ‖population‖ ≤ B ^ 2)
    (hsampleNorm : ∀ i, ‖sample i‖ ≤ B) :
    (empiricalSecondMoment sample - population =
      (Fintype.card κ : ℝ)⁻¹ •
        ∑ i, (InnerProductSpace.rankOne ℝ (sample i) (sample i) - population)) ∧
    (∀ i, LinearMap.IsSymmetric
      ((InnerProductSpace.rankOne ℝ (sample i) (sample i) - population : E →L[ℝ] E) :
        E →ₗ[ℝ] E)) ∧
    (∀ i,
      ‖InnerProductSpace.rankOne ℝ (sample i) (sample i) - population‖ ≤
        2 * B ^ 2) :=
  empiricalSecondMoment_preconcentration population sample B hB
    hpopulationSymmetric hpopulationNorm hsampleNorm

end AutoSamplingTheory.Tests.EmpiricalCovariance
