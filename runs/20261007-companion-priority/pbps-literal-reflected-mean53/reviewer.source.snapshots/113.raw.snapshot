import AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity

/-!
# Literal Gaussian posterior reflection: compact-observer regularity

Authored background for PBPS arXiv:2609.06905v1 Appendix C.1 normalized
conditional-density differentiation. The probability input, compact C1 observer
and finite Hilbert/rank-zero scope explicitly generalize the paper's Gibbs input
and smooth compact tests. The result concerns the specified posterior at every
parameter, not an arbitrary almost-everywhere conditional representative.

The source-density pointwise adapter, actual Tf closed-gradient membership,
rough B.13, hypocoercivity, algorithm errors and main/query-cost results remain
separate. Domination and derivative continuity are proved internally.
-/

open MeasureTheory Filter Set
open scoped Topology InnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean

noncomputable section
set_option maxHeartbeats 800000
set_option backward.isDefEq.respectTransparency false

/-- Compact C1 observables have C1 means under the literal reflected Gaussian
posterior. No input moment, density or analytic certificate is assumed. -/
theorem gaussian_reflected_mean_c1
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
    {f : E → ℝ} (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) :
    let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
    let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
    ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)
 