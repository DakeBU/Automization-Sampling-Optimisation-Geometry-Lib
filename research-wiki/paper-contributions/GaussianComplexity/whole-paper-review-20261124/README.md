# Formalization of *On Complexity of Gaussian Sampling*

This review collects the original results of Zhou and Suzuki, *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, in a single Lean 4.33 replay. The sampling model uses an exact first-order oracle, a deterministic cap on each run, and total variation after averaging over private randomness. [Paper](https://arxiv.org/html/2610.20492v1)

**Theorem 3.1.** For each integer $d\ge1$, $\kappa\ge4$, and $0<\varepsilon\le1/16$, the query complexity is at least

$$\frac1{256}\min\left\{d,\sqrt\kappa\log\left(1+\frac{d}{\sqrt\kappa\,\varepsilon}\right)\right\}.$$

The Lean theorem quantifies over adaptive randomized algorithms and proves the result both for each successful algorithm and for the infimum over feasible budgets. An exact sampler shows the infimum is finite. [Formal theorem](../theorem-3-1-review-20261123/GC31ExactSampler.lean) · [Paper statement](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem1)

**Theorem 4.1.** For fixed $0<\delta<1$, sufficiently large $d$, $2\le\kappa\le d^{1-\delta}$, and $0<\varepsilon\le1/10$, the query complexity is at least $(\delta/256)\sqrt\kappa\log d$. The proof applies when the sampler is given the spectrum of the hard instance. [Formal theorem](../theorem-4-1-review-20261123/GC41LowerBound.lean) · [Paper statement](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem1)

## Scope of the introduction and Section 4.4

The inference after Theorem 1.1 about every $\sqrt\kappa\log d\le d$ has a gap at constant accuracy. Set $\varepsilon=1/16$ and $\sqrt\kappa=d/\log d$. Dividing the rate in Theorem 1.1 by $d$ gives $\min(1,\log(1+16\log d)/\log d)\to0$. The conjectured lower rate at these parameters is $d$. The actual optimal query complexity on this boundary would require an additional argument. The three stated matching regimes have separate positive comparison theorems. [Boundary calculation](../accuracy-and-gaussian-facts-review-20261124/GCFinishBoundary.lean) · [Matching regimes](../accuracy-and-gaussian-facts-review-20261124/GCFinishMatching.lean) · [Source discussion](https://arxiv.org/html/2610.20492v1#S1.SS1)

For the dimension limitation in Section 4.4, the $1/\sqrt{2}$ obstruction uses the detector regime $2q+1<d$ from Lemma 4.4. At the excluded endpoint $d=2q+1$, the span already saturates, yet all entries of the cosine diagonal equal zero. For the accuracy limitation, the paper’s explicit Bernstein certificate and threshold inequalities imply $q<\sqrt\kappa\log(d)/8$, independently of accuracy. Remark 4.8 records the authors’ open question about other proofs for the same family. [In-range obstruction](../lemma-4-7-review-20261124/GC47Limitation.lean) · [Endpoint](GC44Nyquist.lean) · [Accuracy ceiling](../accuracy-and-gaussian-facts-review-20261124/GCFinishAccuracy.lean) · [Source discussion](https://arxiv.org/html/2610.20492v1#S4.SS4)

## Results in source order

The table covers all 32 numbered statements, definitions and remarks in the version reviewed. Each number links to the original text. [GCWholePaper.lean](GCWholePaper.lean) imports the results together and prints their transitive axioms.

| Paper | Content and Lean entry point |
|---|---|
| [1.1](https://arxiv.org/html/2610.20492v1#S1.Thmtheorem1), [1.2](https://arxiv.org/html/2610.20492v1#S1.Thmtheorem2) | Informal forms of 3.1 and 4.1. The ordinary lower bound in 1.2 follows from 1.1 wherever their hypotheses overlap. [Overlap with the same constant](GC12Overlap.lean) · [Polynomial-accuracy comparison](GC42Comparison.lean) |
| Remark [1.3](https://arxiv.org/html/2610.20492v1#S1.Thmtheorem3) | Reduction to strongly log-concave Gibbs targets with a known minimizer and exact value-and-gradient queries. [Known-minimizer reduction](../remark-1-3-review-20261124/GC13KnownMinimum.lean) |
| [3.1](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem1) | Hidden determinant lower bound. [Individual-algorithm and infimum forms](../theorem-3-1-review-20261123/GC31LowerBound.lean) |
| [3.2](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem2), [B.1](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem1) | Equality of averaged output laws for the two signs. [First-order indistinguishability](../lemma-3-2-review-20261123/GC32Indistinguishability.lean) |
| [3.3](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem3), [B.5](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem5) | Separation in total variation of the averaged Gaussian targets. [Target separation](../theorem-3-1-review-20261123/GC33Target.lean) |
| [3.4](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem4), [B.8](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem8) | Admissibility, zero minimum value and uniqueness of the minimizer for the block family. [Block regularity](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/BlockFamily.lean) |
| [4.1](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem1) | Fixed-spectrum lower bound, including disclosed spectrum. [Lower bound](../theorem-4-1-review-20261123/GC41LowerBound.lean) · [Rotated target event](../fixed-spectrum-target-power-review-20261123/GC41Power.lean) |
| Remark [4.2](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem2) | Same-rotation affine conversion between the κ and κ=2 precision matrices and their replies. [Affine identity](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAffine.lean) |
| [4.3](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem3) | Representation of the actual adaptive output in the extended Gaussian Krylov experiment. [Representation](../theorem-4-1-review-20261123/GC43Representation.lean) |
| [4.4](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem4) | Simultaneous bound over the entire random Krylov subspace. [Uniform bound](../lemma-4-4-review-20261123/GC44Uniform.lean) |
| [4.5](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem5), [C.8](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem8) | Finite-grid means, quadratic variances and the exponential bias. [Means](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumExactMeans.lean) · [Variances](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumVariances.lean) · [Bias](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumBias.lean) |
| [4.6](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem6) | Admissibility of every orthogonal conjugate of the precision matrix. [Admissibility](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAdmissibility.lean) |
| [4.7](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem7) | The Gaussian Krylov span has dimension min(d,(q+1)²) almost surely for independent starts. [Dimension](../lemma-4-7-review-20261124/GC47Dimension.lean) |
| Remark [4.8](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem8) | Open question on stronger bounds from the same family. [Original remark](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem8) |
| [A.1](https://arxiv.org/html/2610.20492v1#A1.Thmtheorem1) | Both spherical Poisson moment identities, including dimension two. [Spherical Poisson](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/SphericalPoisson.lean) |
| [B.2](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem2) | Direction and conditional residual under component Haar. [Conditional law](../lemma-b2-review-20261119/HaarConditional.lean) |
| [B.3](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem3) | For an arbitrary admissible raw primitive-query policy, the actual history determines oriented frames and per-block ranks. Reconstructing the original matrices from their residuals gives the conditional product Haar law. Includes inverse, dependent and zero queries. [Factorization](GC3AdaptiveFactorization.lean) · [Regular conditional law](GC3ConditionalDistribution.lean) · [Boundary case](GC3DeterminedWitness.lean) |
| [B.4](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem4) | Indistinguishability of the padded transcript. [Transcript](../lemma-b4-review-20261122/B4Transcript.lean) |
| [B.6](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem6) | Signed determinant cancellation against integrable Borel tests of the scalar coordinate. [Cancellation](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/DeterminantCancellation.lean) |
| [B.7](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem7) | Single-block separation. [Proposition](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/SingleBlockSeparation.lean) |
| [C.1](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem1) | For either an image or a preimage, the observed direction is uniform on the opposite sphere and the remaining isometry is conditionally Haar. Measurable frames exist for a pair of subspaces of equal, possibly random dimension. [Both directions at arbitrary rank](GCCTaggedUnit.lean) · [Conditional residual in orthonormal coordinates](GCCAmbientRevelation.lean) · [Two-subspace frames](GCCTwoSubspaces.lean) |
| [C.2](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem2) | Haar states from the observed projection and partial action, with history-measurable frames for all ranks. The conditional completion law is independent of the frame, equals Haar with no observations, and is a point mass after full observation. [Equivalence with the law of the restricted isometry](GCCRestrictionLaw.lean) · [Endpoint laws](GCCCompletionEndpoints.lean) · [Measurable frames](GCCFrameChart.lean) · [Completion law](GCCCompletionLaw.lean) |
| [C.3](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem3) | Independent auxiliary randomness, actual image and preimage updates, exact span, and the normalized complementary direction. [Exact updated subspace and action](GCCExactUpdate.lean) · [Independent auxiliary randomness](GCCIntrinsicEndpoint.lean) · [Projected direction](GCCHaarStateRevelation.lean) · [Physical subspace restriction](GCCActualRestriction.lean) · [Rotated two-dimensional example](GCCRotatedPreimageWitness.lean) |
| [C.4](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem4) | Gaussianizing an independent uniform direction in any fixed proper subspace complement and recovering its span. [Gaussian and span](../accuracy-and-gaussian-facts-review-20261124/GCFinishDirectionSpan.lean) |
| [C.5](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem5) | Equality of the feature range and the Krylov span, cosine-frame bounds and both Bochner matrix expectations. [Range](../lemma-4-4-review-20261123/GC44GramUse.lean) · [Frame bounds](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineGram.lean) · [Gram means](../accuracy-and-gaussian-facts-review-20261124/GCFinishGram.lean) |
| [C.6](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem6) | The two Gram operator-norm bounds hold simultaneously with probability at least 199/200 throughout the source frequency range. [Gram concentration](../lemma-4-7-review-20261124/GC47FullGram.lean) |
| [C.7](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem7) | Expansion of the inverse spectrum, including absolute and uniform convergence. [Cosine expansion](../../../../AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumCosineExpansion.lean) |

Facts C.5 and C.6 use the original random matrices. The verified concentration proof uses scalar Gaussian concentration and cosine projection identities. Earlier cited algorithms, their published upper bounds, and the authors' open question are identified as literature and context.

## Replay

Run this command from the pinned repository checkout.

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/whole-paper-review-20261124/replay.py
```

The manifest records the Lean and Mathlib versions, the SHA-256 hashes of the review and repository sources, and the dependency order. The replay builds the required repository and Mathlib modules, then compiles every review module in an empty temporary object directory with warnings treated as errors. The axiom audit admits only `propext`, `Classical.choice` and `Quot.sound`.
