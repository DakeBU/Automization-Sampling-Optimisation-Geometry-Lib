# Canonical relative-score / coupling pairing

Module: `AutoSamplingTheory.TechnicalLemmas.InformationTheory.CanonicalFisherTransportPairing`.
Status and independent audit belong to `ASTIS-SHARED-canonical-fisher-transport-pairing`;
this card makes no Registry or chapter-completion claim.

The two public declarations are `integrable_pairing_of_isCoupling` and
`abs_integral_pairing_le_sqrt_information_mul_wasserstein`.
For the existing canonical score `s(x) = gradient (RNLogRatio.logRatio mu pi) x`,
they produce integrability of `inner (s x) (y-x)` under a coupling gamma and,
when gamma is quadratic-optimal, prove

\[
\left|\int \langle s(x),y-x\rangle\,d\gamma(x,y)\right|
\le \sqrt{\mathrm{information}(\mu,\pi)}\,W_2(\mu,\nu).
\]

Proof: pull the squared score through gamma's first marginal, obtain squared
displacement integrability from the two marginal second moments, derive L2
product and pairing integrability, apply Mathlib's Holder inequality, and use
the existing finite optimal real/extended quadratic-cost identity. The focused
test separately derives `W2 != infinity`; `toReal infinity = 0` is not a valid
interpretation of a non-finite distance here. No probability or sigma-finiteness
assumption is needed for these two analytic declarations.

The `SmoothFiniteScoreDomain` guard keeps absolute continuity, differentiability
of the selected canonical RN log-ratio mu-almost-everywhere, and squared-score
integrability. The L2 calculation uses the last field; the other fields retain
the inherited interpretation boundary. Totalized gradient and log/RN
representatives are not automatically the source's Sobolev score. An a.e.
equality of log-density representatives does not by itself identify gradients.

`Tests/CanonicalFisherTransportPairing.lean` separately exercises non-optimal
pairing integrability and finite optimal cost. Its geodesic consumer substitutes
the actual gamma pairing, canonical Fisher information and actual W2 value,
derives the missing `hcs`, and invokes the existing geodesic closure. KL
convexity, a metric/law adapter and the actual path's two-sided first variation
remain explicit inputs. Finite entropy near the endpoint and a one-sided
first-variation producer are not supplied by this test.

Source motivation: [Chewi, August 9, 2026, Theorem 8.4.1 proof,
printed p.221 / PDF p.233](https://raw.githubusercontent.com/chewisinho/chewisinho.github.io/b3ad6e874119983ae5f689a3295df4cdb44b11a7/main.pdf#page=233),
SHA256 `9b454ccf44fe700081e13a766ae9cabb83c3530f5fdc532d59ac335f53652597`.
This is an ASTIS supplementary analytic producer, not literal equivalence to
the source's optimal-map expectation or completion of the proximal theorem.
Optimal coupling/map existence, KL first variation, displacement convexity,
heat-flow domains and convergence remain separate obligations.

## Independent source-admission boundary

The independent proof gate passes, but source review
`ASTIS-RT-20260908-CanonicalFisherTransportPairing` records
**domain-mismatch / needs-revision**. Source certification is withheld, not
the truth of the displayed general coupling inequality. The source probability
laws, destination equal to the score reference, graph-coupling integral, and
selected-RN score/FI identification have not all been connected. Keep this
packet at `PROVED_LOCAL` with a proof-review pass; do not relabel it as an
assimilated Chewi statement or repair the source to fit the formalization.
See the [independent source-admission record](../../../runs/20260908-samplewiki-resume/fisher-transport-source-audit.md)
for the exact deltas and the next representative-domain audit.
