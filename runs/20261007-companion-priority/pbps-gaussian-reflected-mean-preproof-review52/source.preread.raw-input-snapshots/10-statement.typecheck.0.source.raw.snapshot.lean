import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity
open MeasureTheory
open scoped ENNReal
#check fun     {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
    {f : E → ℝ} (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) =>
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
    ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)
