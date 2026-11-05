# Same-constant Poincaré on the original compact gradient closure

From compact smooth function LSI with coefficient `2*C`, apply the
[compact PI theorem](../20261106-compact-logsobolev-poincare/README.md) to
actual compact function/gradient representatives. The joint inequality
set is norm closed: on probability L²,
`variance(u) = ‖u‖² - ⟪1,u⟫²`, and vector norm squared is continuous.
This proves the bound on every pair in the original graph's joint norm closure.
It does not assume or assert a single-valued gradient for arbitrary measures.

The [focused Lean 4.33.0 receipt](focused-receipt.json) records 3109 jobs and
standard axioms only. Its Gibbs consumer takes a C¹ observable with
`f, ∇f ∈ L²(μ)`, constructs the original closable gradient, uses actual
C¹ graph membership, and applies the closure result with the given compact
LSI. It does not assume PI, curvature or a graph-membership certificate.
This is a scoped Euclidean result, not a generator core or abstract
reversible Markov-form theorem.

The [selected proof-body diagnostic](selected-proof-bodies.json) comes from
the actual compiled declarations using the existing Bench extractor's
[probe](selected-proof-bodies.lean.txt). In the seven selected nodes, the
closure proof mentions the compact PI theorem, which in turn mentions both
quadratic limits and the cutoff extension. This is not an import scan, a
proof of mathematical necessity, or an admitted Bench graph snapshot.

The source uses an omitted density step; the exact
[Statement Seal](../../proof-obligations/chewi-exercise-1-7/compact-gradient-closure-statement-seal-v1.md)
and authored lesson identify this bridge, not a complete numbered answer.
The [independent source review](source-review-v2.result.json) accepts all
seven statement slots after the Gibbs lesson was clarified. The
[original report](source-review.result.json) preserves the exposition
finding. This checkpoint is `PROVED_LOCAL`; source acceptance is not an
independent exact-commit verification or a release.
Registry/site integration and Bench admission remain separate. No old
paper/cycle, foreign stabilization lease, family, split or question was changed.

## Next abstract route — research candidate, not compiled

The affine density hint gives the KL expansion, but does not by itself
put `log(1+ε f)` in the domain of a general generator. For bounded
generator-domain `f`, consider instead
`ρ_ε = exp(ε f) / Z_ε` and `φ(ε) = log Z_ε`. The pointwise logarithm
`log ρ_ε = ε f − φ(ε)` is affine in `f`. For an actual linear generator
with constants in its domain, `L1 = 0` and `∫ Lf = 0`, this gives
`E(ρ_ε, log ρ_ε)/ε² = ∫ ((ρ_ε−1)/ε) (−Lf)`. The density quotient
should tend boundedly to `f−∫f`, yielding `E(f,f)` without a nonlinear
log-domain hypothesis. Produce positivity, mass one and all integrability
before applying density LSI. Check the density's own domain separately:
the generator pairing needs only the first slot in L², but a form-domain
LSI can also require `ρ_ε ∈ D(E)`. In that case use the actual Markov
contraction theorem on the bounded range of `log ρ_ε`. Affineness of the
log does not prove that the exponential itself belongs to `D(L)`.

For the entropy side, `∫ρ_ε log ρ_ε = ε φ'(ε)−φ(ε)`; differentiating
this numerator gives `ε φ''(ε)`, so the scaled limit should be
`Var(f)/2`. Pinned Mathlib `MGFAnalytic.lean` already has the first
and second cumulant derivative APIs; derive their exponential integrability
domain from boundedness. This is an alternative perturbation route with
the same target constant, not a rewrite of the source's affine hint.

Beyond bounded generator-domain functions, look for a true bounded graph
core: truncate in L², then apply the Markov time average
`A_t f = (1/t)∫₀ᵗ P_s f ds`. The candidate domain identity is
`L A_t f = (P_t f−f)/t`; for fixed t this makes the truncation passage
continuous in graph norm, before t decreases to zero on the original
generator domain. This requires an actual strongly continuous Markov
semigroup and separate generator/form-domain verification. Neither the
current Euclidean theorem nor the existing bare generator integral
definitions supply those hypotheses.
