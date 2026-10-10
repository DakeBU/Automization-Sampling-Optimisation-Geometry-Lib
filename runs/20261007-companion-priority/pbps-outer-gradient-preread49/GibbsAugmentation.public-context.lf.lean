import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation
import Mathlib.MeasureTheory.Measure.Tilted

/-!
# The normalized Gibbs augmentation density

This source-specific integration of shared analytic and Gaussian parents
establishes the actual probability-law identification in Chen, Chewi, Lu and
Zhang, arXiv:2609.06905v1, Section 2.2, equations (2.6)-(2.7):
<https://arxiv.org/html/2609.06905v1#S2.SS2>.

The positive genuine Hessian lower bound and C² regularity imply finite positive
Gibbs mass without an assumed minimizer. The Gaussian augmentation of that Gibbs
probability then has the displayed density relative to product canonical volume.
Positive normalization and probability are explicit conclusions: a zero
totalized tilt cannot satisfy this certificate.

The source upper Hessian bound and upper scale restriction are not needed here.
Finite real inner-product spaces, including dimension zero, are explicit
generalizations. Conditional representatives, process invariance and complexity
are not conclusions. Reflection of this source law is a downstream consumer.
-/

open MeasureTheory ProbabilityTheory
open scoped ENNReal

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The Gibbs normalizer is strictly positive, its generative Gaussian
augmentation is a probability measure, and this measure has the exact normalized
source density. Integrability, positive normalization and measurable transport
are derived internally from genuine C²/Hessian hypotheses, not supplied. -/
