# Gaussian directions, exact Gram means, and the scope of the lower bounds

This package covers Facts C.4 and C.5, the accuracy paragraph of Section 4.4, and the rate comparisons following Theorem 1.1 of Zhou and Suzuki, *On Complexity of Gaussian Sampling*. The source is the version dated October 2026. [Paper](https://arxiv.org/html/2610.20492v1)

| Source | Checked Lean result |
|---|---|
| Fact C.4 | `GCFinishDirectionSpan.gaussianize_uniform_complement` (file and short declaration name). For any fixed proper subspace, on any probability space, an independent uniform complementary direction replaces the direction of the residual Gaussian. The full distribution is standard Gaussian, and the direction belongs almost surely to the sum of the original subspace and the span of the new Gaussian. |
| Fact C.5 | `GCFinishGram.independent_start_gram_means` gives Bochner integrability and both matrix expectations for arbitrary independent standard Gaussian starts. The other conclusions are `GC44GramUse.range_feature` and `FixedSpectrumCosineGram.actual_cosine_frame_gram`. |
| Section 4.4, accuracy | `GCFinishAccuracy.bernstein_certificate_floor` uses the two-sided certificate with the source variance, truncation level, radius and prefactor. A certificate below one forces the deviation to exceed the reciprocal square root of the dimension. `mode_bias_upper` gives the finite-grid exponential upper bound for every mode from 1 to d−1. `accuracy_certificate_query_ceiling` uses both inequalities and an arbitrary compatible threshold to give q < √κ log(d)/8. This restricts the stated proof method. [Section 4.4](https://arxiv.org/html/2610.20492v1#S4.SS4) |
| Discussion after Theorem 1.1 | `GCFinishMatching.polynomial_condition_matching`, `polynomial_accuracy_matching`, and `saturated_rate` compare the displayed rate with the known upper rate in the three stated regimes. The constants multiplying the upper rate in the first two comparisons are δ/2 and min(1/2,c/(1+c)). For √κ ≥ d the lower rate is at least d/2. |

## A boundary case in the introduction

The paragraph after Theorem 1.1 claims that the conjectured constant-accuracy lower bound follows whenever √κ log d ≤ d. Fix ε = 1/16 and take integer dimensions d tending to infinity, with √κ = d/log d. These parameters satisfy κ ≥ 4 eventually and attain equality in the proposed range. Dividing the displayed rate in Theorem 1.1 by d gives

$$\min\left(1,\frac{\log(1+\log(d)/\varepsilon)}{\log d}\right)\longrightarrow 0.$$

The checked declarations `boundary_rate_identity`, `boundary_rate_limit`, and `boundary_rate_below_every_linear_constant` establish this for every fixed positive ε. Consequently the conjecture at that boundary needs an additional lower-bound argument. This comparison leaves the actual query complexity there open. [Theorem 1.1 and discussion](https://arxiv.org/html/2610.20492v1#S1.SS1)

## Replay

From the repository root run

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/accuracy-and-gaussian-facts-review-20261124/replay.py
```

The replay checks the SHA-256 of every reviewed source module and compiles the complete import closure in an empty temporary object directory with Lean warnings treated as errors.
