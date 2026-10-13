import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology
noncomputable section
set_option autoImplicit false

theorem gaussian_marginal_gradient_closable
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η) :
    let J 