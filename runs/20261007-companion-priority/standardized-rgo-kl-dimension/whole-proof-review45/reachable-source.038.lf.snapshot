import AutoSamplingTheory.TechnicalLemmas.Measure.CommonNoiseContraction
import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# Gaussian smoothing as common additive noise

The transport part of heat-flow contraction does not depend on the PDE.  This
module packages a centered Gaussian noise of arbitrary scale `sigma` and then
specializes the general common-noise contraction theorem.

For the Chapter 8 proximal-sampler spine we also expose the source normalization

`P_t mu = mu * N(0, t I)`

as Gaussian smoothing with standard-deviation scale `sqrt t`.  The heat-time
parameter is an `NNReal`, so the source's nonnegative-time domain is encoded in
the type rather than hidden in a side condition.

This normalization is only a measure-level convolution definition.  It does
not by itself prove the heat/Fokker--Planck PDE or time differentiability.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Measure
namespace GaussianSmoothing

open MeasureTheory ProbabilityTheory
open scoped ENNReal

noncomputable section

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
  [SecondCountableTopology E]

/-- Centered isotropic Gaussian noise obtained by scaling the standard Gaussian
by `sigma`.  The definition is valid for every real scale; heat-flow interfaces
below use the nonnegative scale `sqrt t`. -/
noncomputable def scaledStdGaussian (sigma : ℝ) : Measure E :=
  Measure.map (fun z : E => sigma • z) (stdGaussian E)

instance scaledStdGaussian_isProbabilityMeasure (sigma : ℝ) :
    IsProbabilityMeasure (scaledStdGaussian (E := E) sigma) := by
  unfold scaledStdGaussian
  exact Measure.isProbabilityMeasure_map (by fun_prop : AEMeasurable (fun z : E => sigma • z) (stdGaussian E))

/-- Gaussian smoothing of a law by independent centered Gaussian noise of
scale `sigma`. -/
noncomputable def gaussianSmoothing (mu : Measure E) (sigma : ℝ) : Measure E :=
  CommonNoiseContraction.addNoise mu (scaledStdGaussian (E := E) sigma)

/-- Gaussian smoothing is `W₂`-contractive because it adds the same independent
noise law to both endpoint measures. -/
theorem wassersteinDistance_gaussianSmoothing_le
    (mu nu : Measure E) [IsProbabilityMeasure mu] [IsProbabilityMeasure nu]
    (sigma : ℝ) :
    WassersteinSpace.wassersteinDistance
        (gaussianSmoothing mu sigma) (gaussianSmoothing nu sigma) ≤
      WassersteinSpace.wassersteinDistance mu nu := by
  exact CommonNoiseContraction.wassersteinDistance_addNoise_le
    mu nu (scaledStdGaussian (E := E) sigma)

/-- Source-normalized heat smoothing: nonnegative heat time `t` corresponds to
adding centered Gaussian noise with standard-deviation scale `sqrt t`, hence
covariance `t I`.

This is the measure/convolution side of the heat semigroup convention used in
Chewi Chapter 8.  No PDE statement is bundled into the definition. -/
noncomputable def heatSmoothing (mu : Measure E) (t : NNReal) : Measure E :=
  gaussianSmoothing mu (Real.sqrt (t : ℝ))

/-- Unfold the source normalization from heat time to Gaussian standard
deviation. -/
theorem heatSmoothing_eq_gaussianSmoothing_sqrt
    (mu : Measure E) (t : NNReal) :
    heatSmoothing mu t = gaussianSmoothing mu (Real.sqrt (t : ℝ)) := rfl

/-- Simultaneous heat smoothing is `W₂`-contractive.

The proof is purely the common-noise coupling theorem at Gaussian scale
`sqrt t`; it does not use or assert the heat PDE. -/
theorem wassersteinDistance_heatSmoothing_le
    (mu nu : Measure E) [IsProbabilityMeasure mu] [IsProbabilityMeasure nu]
    (t : NNReal) :
    WassersteinSpace.wassersteinDistance
        (heatSmoothing mu t) (heatSmoothing nu t) ≤
      WassersteinSpace.wassersteinDistance mu nu := by
  exact wassersteinDistance_gaussianSmoothing_le
    mu nu (Real.sqrt (t : ℝ))

end

end GaussianSmoothing
end Measure
end TechnicalLemmas
end AutoSamplingTheory
