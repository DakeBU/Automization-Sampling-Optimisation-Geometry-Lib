# Compact Euclidean PI candidate: independent local review

Verdict: **ACCEPT the bounded local candidate; no required repairs.**
Reviewer: `agent-task:/root/compact_pi_candidate_review`. This is an evidence
receipt, not a Source Seal, formal VERIFIED transition, or publication.

Reviewed commit: `92646ca64630f81b1fb80196f5907d783512a924`.

| Exact Git input | Blob |
| --- | --- |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactLogSobolevPoincare.lean` | `a89f583e9c48d8f3f8d90b232afba01683eae362` |
| `Tests/Shared/CompactLogSobolevPoincare.lean` | `9a56aa5c8f7ef3260e3f6c9e82ef4437e06d623d` |
| `compact-pi-statement-v1.lean.txt` | `38082d6a26559e7c09ddc8874173533ff7812e79` |
| `compact-pi-statement-v1.md` | `200a2298f87a394ca4c0b353d6f5d5a832a81249` |
| `compact-pi-candidate-v1.md` (commit version) | `9243a5083135c2a0ebf000d7137fb3e1d12d39e3` |

The reviewed reader proof includes the Taylor-remainder edit to
`compact-pi-candidate-v1.md`, separately bound by raw SHA-256
`f6006e2da730714ee0f43883bdf1d3356d97f7deafaccf60c7da7757438780cf`.

- **Signature and scope.** The exact declaration header matches the frozen
  signature (LF SHA-256 `43766c48f2ff7a0ffdd2e8005994d65246766329cef913be80a22ef4ce072714`).
  Both tests are smooth and compactly supported; only the probability measure
  and compact-test LSI are assumed beyond the carrier and target test data.
  Neither centering, integrability nor a sign condition on the fixed real
  coefficient is an extra premise. `Admissible` is proved, not assumed:
  it supplies integrability of the original observable, its centered square,
  and its squared gradient norm. The theorem proves an inequality at the same
  coefficient, not the `Poincare.Satisfies` wrapper or optimal-constant equality.
- **Domain and normalization.** For `g = f - integral f`, probability gives
  finiteness and integral of the constant 1 equal to 1; hence the mean of `g`
  vanishes. Boundedness follows from continuity and compact support of `f`.
  It is `Dg = Df`, not `g`, whose support remains compact. The perturbation
  producer supplies the eventual global density interval [1/2, 3/2],
  smooth square root, square-integrability, entropy integrability and
  derivative energy. Continuity and the Riesz norm identity give gradient
  `MemLp`, and the cutoff extension (not direct compact-test LSI) applies
  to the square root. With `p = 1 + e*g = u^2` the mass is one, the
  normalization vanishes, and the integrable compensation `1 - p` has
  integral zero.
- **Limits and constants.** The inequality is divided by `e^2 > 0` on
  the two-sided punctured neighborhood. The Taylor integral remainder in
  the reader proof is valid on the positive segment and gives the integrable
  envelope `g^2` and the pointwise limit `g^2/2`. The Lean entropy producer
  instead uses genuine log differentiation, L'Hopital and a scalar bound
  before dominated convergence. The genuine square-root energy quotient
  is `||Dg||^2 / (4*p)`, bounded by `||Dg||^2/2` in the reader proof;
  the Lean energy producer uses the integrable envelope `||Dg||^2`.
  The limits yield `(1/2)*Var <= 2*C*(1/4)*Energy`, hence
  `Var <= C*Energy` without dividing by or taking the sign of `C`.
- **Lean check.** The exact test instantiates the implication with the
  established standard Gaussian LSI at `C = 1` and checks admissibility
  as well as the PI bound. It uses the prior Gaussian result at lower
  regularity only to discharge the compact-smooth LSI premise. The two new
  Git blobs contain no placeholder/fake closure. The focused build, direct
  test, and standard axiom scan were supplied by the coordinator, not rerun
  as part of this semantic review.

The existing [independent source topology review v2](source-topology-review-v2.json)
(blob `8064496bc3e965f68fb8eff23f8c18b1a48990b6`) supplies the pinned
primary-source boundary: Exercise 1.7 (PDF p. 55) for the linearization
and §2.1.1 (PDF pp. 60–61) for the compact test classes and the
`2*C`/`C` normalization. The bounded result does not certify (1.E.1)
as a standalone actual-law KL expansion, the form-domain/core extension,
the abstract reversible-semigroup implication, Corollary 2.1.2, or the
whole exercise. No Cell, ledger, registry, or main-branch state was changed.
