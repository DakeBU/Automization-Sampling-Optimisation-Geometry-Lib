import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Measure.Prod
import Mathlib.Tactic.Abel
import Mathlib.Tactic.FunProp

/-!
# Reflection of the generative Gaussian augmentation

This is the generative-law proof component of Proposition 2.1(iii) in Chen,
Chewi, Lu and Zhang, arXiv:2609.06905v1, Section 2.2, equations (2.7) and (2.14):
<https://arxiv.org/html/2609.06905v1#S2.SS2>.

The law below is defined by independent `X ~ μ`, `Z ~ stdGaussian E` and
`Y = X + sqrt η • Z`. Identifying it with the normalized density (2.6) is a
separate obligation. The symmetry component needs no potential, curvature or
upper step-size bound; this generality is explicit, not a claim to have proved
those source assumptions or the invariance of any PBPS process.
-/

open MeasureTheory ProbabilityTheory

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- Reflecting the auxiliary point through the position is involutive and
preserves the generative Gaussian augmentation. All maps used in the
pushforward calculation are proved measurable. The positive-scale hypothesis
retains the paper's sampling regime; the reflection algebra itself is
scale-independent. Intended consumers are the auxiliary update in Section 3.1
and, after a separate `L²` adapter, the reflection operator in Appendix B. -/
