# Picard-center gradient moments

Source: Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1, Appendix D.2,
Lemma D.4, equation (D.7), specifically the two-layer Picard-center argument
on lines 2177--2181 of the version-1 HTML.

## Frozen edge

Work under the normalized Hessian bounds used by the paper and the existing
actual stopped gradient-descent implementation of an approximate proximal
query.  On an arbitrary probability space carrying one realized phase, assume
a second-moment bound for the current position and the post-refresh momentum,
measurable innovations with the standard Gaussian second-moment bound, time
nodes satisfying `|t_i| <= 1`,
and the absolute row-sum bound for the integrated interpolation weights.

Construct the actual stopped proximal output at every layer-1 center.  Prove
gradient-square integrability and explicit second-moment bounds for:

1. every layer-1 queried gradient, using the center moment internally;
2. every stochastic gradient used to form layer 2;
3. every layer-2 queried gradient, using the center moment internally.

The center moments are proof-internal dominating quantities; the public
interface exports the gradient moments needed by the expected-work consumer.
A separate refresh-moment adapter must connect the repeated-chain state bound
to the post-refresh momentum used by Algorithm 3.1.

The proof must not use independence: the source only needs marginal Gaussian
second moments for this edge.  The resulting constants may be explicit
sufficient constants; the paper's universal `C` absorbs them.

## Reuse

- `ApproximateProximalExecution.approximate_proximal_execution` supplies the
  measurable actual stopped program and its pointwise error certificate.
- The existing `ProximalEstimatorLipschitz` API was audited, but its current
  `eta <= 1/2` interface is stricter than this source edge.  Prove exact-prox
  nonexpansiveness locally from strong monotonicity and the optimality equation,
  using the shared quadratic-regularization identities, and identify the exact
  minimizer by uniqueness rather than assuming two witnesses coincide.
- Mathlib finite-sum, Bochner-integrability and norm inequalities supply the
  deterministic L2 propagation.

## Excluded claims

The run-wide state moment bound from the Wq analysis, its post-refresh momentum
adapter, the actual iterated
Algorithm 3.1 probability kernel/history law, the numerical substitutions in
(5.12)/(D.4), the phase count and total work (D.8), and Theorem 5.1 remain
separate.  This edge does not infer an unbounded expected cost from TV distance.
