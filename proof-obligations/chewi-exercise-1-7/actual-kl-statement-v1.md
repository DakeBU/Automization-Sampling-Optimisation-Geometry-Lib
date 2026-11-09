# Frozen candidate: the actual-law expansion (1.E.1)

Statement ID: `chewi-ex1-7-actual-kl-v1`. The exact Lean signature in
[`actual-kl-statement-v1.lean.txt`](actual-kl-statement-v1.lean.txt) has LF
SHA-256 `21bee5da0f009cb6bcd1c0585ba1a32ddb4739113aa45cf96179d9a467119bfa`.
This freezes the local interface before implementation, not an official
Cell or publication transition.

Sinho Chewi, *Log-Concave Sampling*, August 20, 2026, PDF SHA-256
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`:
[Exercise 1.7 / (1.E.1), printed p. 43 / PDF p. 55](https://chewisinho.github.io/main.pdf#page=55),
and [its explicit use in Corollary 2.1.2, printed p. 50 / PDF p. 62](https://chewisinho.github.io/main.pdf#page=62).
The [independent source topology review](source-topology-review-v2.json)
already separates the actual KL edge from the compensated real integral
and the compact Euclidean PI conclusion.

For a probability measure \(\mu\) and a bounded a.e.-strongly-measurable
real function \(f\) with zero mean, set \(\nu_\varepsilon=(1+\varepsilon f)\mu\)
using the actual `Measure.withDensity` construction. For all sufficiently
small \(|\varepsilon|\), including zero, this is a probability law with
finite extended-real KL. Its real KL therefore has the expansion
\(\varepsilon^2\int f^2\,d\mu/2+o(\varepsilon^2)\).

The measurable carrier is `TYPING`; the probability measure and centering
are `SOURCE`. Strong measurability and an a.e. uniform bound are the analytic
consequences actually used from the source's smooth bounded tests, not added
requirements on those tests. The generic statement drops geometry and support;
that covers both compact smooth tests and bounded smooth tests with only
compact gradient support. The two-sided neighborhood strengthens the source's
positive-parameter use. The `ofReal` density cannot clip values near zero
since the upstream law theorem proves the a.e. lower bound \(1/2\).

The current tests already check the punctured normalized limit in isolation.
Promote its proof by reuse, not by treating the anonymous test as a new leaf.
The new source-facing result binds it to actual finite probability KL and
the full-neighborhood little-o remainder, including the exact zero endpoint.
`toReal` alone does not prove finiteness. No LSI, Fisher information, T2,
transport estimate, or form-domain theorem is included.
