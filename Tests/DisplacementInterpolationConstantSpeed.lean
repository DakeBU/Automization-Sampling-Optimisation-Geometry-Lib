import AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationP2ConstantSpeed

namespace AutoSamplingTheory.Tests.DisplacementInterpolationConstantSpeed

open MeasureTheory Set
open scoped ENNReal
open AutoSamplingTheory.TechnicalLemmas.Measure

#check DisplacementInterpolationConstantSpeed.isProbabilityMeasure_displacementInterpolation
#check DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_le
#check DisplacementInterpolationConstantSpeed.interpolation_coefficients_sum_one
#check DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq
#check DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le
#print axioms DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] [StandardBorelSpace E] [Nonempty E]
    {γ : Measure (E × E)} {μ₀ μ₁ : Measure E}
    [IsProbabilityMeasure μ₀] [IsProbabilityMeasure μ₁]
    (hμ₀ : Integrable (fun x : E => ‖x‖ ^ 2) μ₀)
    (hμ₁ : Integrable (fun x : E => ‖x‖ ^ 2) μ₁)
    (hγ : DisplacementInterpolation.IsQuadraticOptimalCoupling γ μ₀ μ₁)
    {s t : ℝ} (hs0 : 0 ≤ s) (hst : s ≤ t) (ht1 : t ≤ 1) :
    WassersteinSpace.wassersteinDistance
        (DisplacementInterpolation.displacementInterpolation γ s)
        (DisplacementInterpolation.displacementInterpolation γ t) =
      ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ :=
  DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq
    hμ₀ hμ₁ hγ hs0 hst ht1

example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [SecondCountableTopology E] [StandardBorelSpace E] [Nonempty E]
    {γ : Measure (E × E)} {μ₀ μ₁ : Measure E}
    (hμ₀ : WassersteinSpace.IsAbsolutelyContinuousFiniteSecondMoment μ₀)
    (hμ₁ : WassersteinSpace.IsAbsolutelyContinuousFiniteSecondMoment μ₁)
    (hγ : DisplacementInterpolation.IsQuadraticOptimalCoupling γ μ₀ μ₁)
    {s t : ℝ} (hs0 : 0 ≤ s) (hst : s ≤ t) (ht1 : t ≤ 1) :
    WassersteinSpace.wassersteinDistance
        (DisplacementInterpolation.displacementInterpolation γ s)
        (DisplacementInterpolation.displacementInterpolation γ t) =
      ENNReal.ofReal (t - s) * WassersteinSpace.wassersteinDistance μ₀ μ₁ :=
  letI : IsProbabilityMeasure μ₀ := hμ₀.1
  letI : IsProbabilityMeasure μ₁ := hμ₁.1
  DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq
    hμ₀.2.2 hμ₁.2.2 hγ hs0 hst ht1

end AutoSamplingTheory.Tests.DisplacementInterpolationConstantSpeed
