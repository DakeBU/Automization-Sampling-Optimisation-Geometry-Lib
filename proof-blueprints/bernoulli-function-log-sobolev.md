# Genuine Bernoulli function entropy producer

SAU: `ASTIS-SA-20261007-BernoulliFunctionLogSobolev`.
Source: SPHMC arXiv:2609.06906v1, first occurrence of (4.6), omitted Gaussian
LSI background; SLT pinned `d0f506f0a695018265dccb33bcb05e2f5ca1c876`, Apache 2.0.
Local toolchain: Lean 4.33.0, Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.

The actual finite law is normalized counting measure on every function
`Fin n → Bool`, including `n = 0`. Its cardinal is `2^n`. The actual flip
replaces exactly coordinate `j` by its Boolean negation. There is no half
factor in the sum of flip energies. Arbitrary signed functions and zeros are
retained; probability and the three Bochner integrability facts are outputs.

For this law, the bounded theorem is

\[
 \operatorname{Ent}_{\mu_n}(h^2)
 =\mathbb E h^2\log h^2-\mathbb E h^2\log(\mathbb E h^2)
 \le \frac12\mathbb E\sum_j(h-h\circ\mathrm{flip}_j)^2.
\]

1. Port only the 26-helper positive Rothaus closure. Actual derivative and
   mean-value domains are proved internally. Do not use the upstream theorem
   with the opposite entropy sign.
2. Apply positive Rothaus to squares; use
   `sqrt(a²) = |a|` and `||a|-|b|| ≤ |a-b|`. Include zero squares with the
   exact logarithm division identity and `log 2 ≤ 1`.
3. Derive finite probability, integrability, and the actual `Fin.snoc`
   last-coordinate integral split.
4. Set `g(x) = sqrt((h(x,+)² + h(x,-)²)/2)`. Prove the entropy equality
   `Ent(h²) = E Ent₂(h₊²,h₋²) + Ent(g²)` by expansion of these integrals.
5. Prove the squared RMS contraction from the true two-dimensional
   Cauchy–Schwarz inequality, derived here from `(ad-bc)² ≥ 0`.
6. Apply induction to `g`; sum its coordinate contraction bounds, apply the
   signed two-point bound for the last coordinate, and use the exact energy
   split. The zero-dimensional base has one state and empty flip sum.
7. Check the actual zero-dimensional negative constant, indicator, signed
   zero-valued two-point input, and normalized two-coordinate Rademacher sum;
   the last has full-flip energy exactly four.

This entropy/RMS induction is an authored alternative to the source Han route.
Both routes are distinguished in the independently reconstructed Source Proof
Graph. The source graph and its topology review do not certify local proofs.

The compiled packet is frozen before whole-proof, source-blind decoder,
anti-anchored source, and exact-commit reviews. Local compilation is not
independent admission or integration.

The actual normalized Rademacher law limit, its entropy limit, its full-flip
energy limit with factor four, real compact Gaussian LSI, finite-Hilbert
extension, noncompact cutoff domains/limits, Gaussian T2, SPHMC (4.6), bias,
algorithms, both paper main results and composition precision/expected cost
remain separate open boundaries. The typed Bernoulli/Gaussian mechanism mirror
is conceptual only; it creates no solid Lean implication or certified functor.
