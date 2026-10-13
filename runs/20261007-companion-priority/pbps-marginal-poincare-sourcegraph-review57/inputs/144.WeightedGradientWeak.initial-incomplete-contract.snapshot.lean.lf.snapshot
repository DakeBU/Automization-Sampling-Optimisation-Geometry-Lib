import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient
namespace AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak
open MeasureTheory InnerProductSpace
open scoped RealInnerProductSpace ContDiff Topology
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

theorem closed_gradient_weighted_ibp (W : E → ℝ) (hW : ContDiff ℝ 1 W)
    (hI : Integrable (fun x => Real.exp (-W x))) :
    let μ 