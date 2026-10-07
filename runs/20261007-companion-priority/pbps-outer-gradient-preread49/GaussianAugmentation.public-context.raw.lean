import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
import Mathlib.MeasureTheory.Group.Prod

/-!
# Density of the Gaussian augmentation

The joint-law density component of equations (2.6)-(2.7) in
arXiv:2609.06905v1, Section 2.2. The reference measure here is `μ.prod volume`.
Inserting the source's Gibbs density for `μ` to obtain a density relative to
`volume.prod volume` is a separate obligation. No reflection or PBPS-process
invariance, conditional representative, convergence, or query cost is claimed.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The law of independent `X ~ μ`, `Z ~ stdGaussian E` and
`Y = X + sqrt η • Z` has the displayed joint density relative to
`μ.prod volume`. The input law may be singular with respect to volume. -/
