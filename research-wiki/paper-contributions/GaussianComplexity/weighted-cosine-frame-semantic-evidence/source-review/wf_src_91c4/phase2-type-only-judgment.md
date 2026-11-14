# Phase 2 — exact types and canonical definitions only

Reviewer `/root/weighted_frame_fresh_source_91c4`. The phase-1 raw-source freeze remains intact. This record uses only that independent source interpretation and the supplied selective type/definition packet, SHA-256 `e1db7fbd954113035a90a60331d6430f4c116c4055e65de15899c30a2ebdb4e1`. Provenance paths, receipt names, planned filenames, seal digests, and producer/consumer-edge prose in that packet were visible, but none of their referenced artifacts was opened. They do not establish compilation, proof dependencies, or fidelity.

## Type-only result

At the level of the supplied exact signatures and canonical definitions, the deterministic producer expresses precisely the weighted coefficient-matrix comparison in the second and last lines of source EGx11. The consumer expresses the source final uncentered individual-second-moment bound in canonical single-row marginal form, together with a useful explicit integrability conclusion. The meaning of its integral is appropriately restricted: it is not a theorem over the original extended experiment, and no row-map, equality of marginal laws, independent-family realization, centering, or concentration conclusion is present.

No excess mathematical premise or off-source local-definition fallback appears in these signatures. This is a type-only semantic judgment, conditional on the supplied canonical definition context. It is not approval of an implementation, proof dependency graph, compilation receipt, blind decoding, or final source-review packet. There is no implementation in this phase.

## Independent reconstruction of the deterministic producer

For every pair of natural numbers `d,q` satisfying `2q+1<d`, put `r=q+1` as a real number. Index source row `i_source` by `i:Fin d` with `i_source=i.val+1`. Its angle is `(i.val+1/2) pi/d`, exactly the source angle `(i_source-1/2) pi/d`.

For each row the real feature vector has `q+1` coordinates, indexed `0,...,q`; its zeroth coordinate is `1`, and its coordinate `k>0` is `sqrt(2) cos(k theta_i)`. `S_i` is the sum of its coordinate squares and `feature_i=t_i t_i^T`. On the real matrix space with paired coordinate set `Fin(q+1) x Fin(q+1)`, define

\[
K={r+2\over d^2}\sum_{i=1}^{d} S_i(I_r\otimes t_it_i^T),
\qquad C={2r(r+2)\over d}.
\]

The proposition is that `C I_(r^2)-K` is positive semidefinite. Equivalently, for every real coefficient vector with entries `c_(a,j)`,

\[
{r+2\over d^2}\sum_i\|t_i\|^2
\sum_a\left(\sum_j c_{(a,j)}(t_i)_j\right)^2
\le {2r(r+2)\over d}\sum_{a,j}c_{(a,j)}^2.
\]

The local signature names this square coefficient matrix `B`; it is the object called `K` in this reconstruction, not the original source's rectangular random matrix `B`. The local variable name changes no proposition, but exposition must not identify the two different matrices.

The factor order is first identity/Gaussian coordinate, then feature coordinate. `Matrix.kronecker` acts entrywise as `A_(a,b) F_(j,k)` at paired row `(a,j)` and column `(b,k)`. `Matrix.PosSemidef` includes Hermitian symmetry and nonnegative quadratic forms. Over the finite real paired coordinate set, the finite-support formulation in its supplied definition tests every ordinary coefficient vector; it is the intended Loewner order, not entrywise nonnegativity. The identity matrix is the paired-index diagonal identity.

The signature contains the actual deterministic feature formula rather than accepting a Gram identity or a norm bound as a premise. Those mathematical ingredients therefore have to be obtained internally by any eventual proof. The presence of `r+2` is a literal positive scalar here, not a hidden Gaussian fourth-moment hypothesis.

## Independent reconstruction of the consumer

With the same natural parameters and source range, let `E=R^(q+1)` with Euclidean norm and let `mu` be the canonical standard Gaussian law on this space. For a single integration variable `x` define

\[
R(x)=\|x\|^2,\quad L=2r+3\log(1000d),\quad G(x)=xx^T,
\]
\[
y_i(x)=\mathbf1_{\{R(x)\le L\}}\,{1\over d}
\bigl(G(x)\otimes t_it_i^T\bigr),
\qquad T=\sum_{i=1}^{d}\int y_i(x)y_i(x)\,d\mu(x).
\]

The conclusion is both (i) each matrix-valued function `x -> y_i(x)y_i(x)` is Bochner integrable and (ii) `C I_(r^2)-T` is positive semidefinite, for exactly `C=2r(r+2)/d`.

The supplied multiplication-instance source expands a product as `(M*N)_(u,v)=sum_w M_(u,w)N_(w,v)`. Thus the displayed consumer has the ordinary matrix square. It has no entrywise squaring, centering, cross-row product, square of a sum, or square of an expectation. Both factors use the same row index and the same integration variable, as required by `E[Y_i^2]`.

`WithLp.ofLp` exposes the coordinate vector without changing its entries. `vecMulVec` is the unnormalized outer product. `Set.indicator` returns the displayed matrix on the inclusive event and the zero matrix outside, so it is exactly the source truncation; there is no retained-probability division. The `1/d` scaling occurs inside each factor of the ordinary square. The given `stdGaussian` definition uses independent variance-one Gaussian coordinates in an orthonormal basis, the canonical standard Gaussian law. No arbitrary law or covariance is supplied as a premise.

The supplied Bochner integral definition has a zero default for nonintegrable functions, and a completeness branch. Here the real matrix carrier has a finite paired index set and the specified Euclidean operator-norm structure, hence is finite dimensional and complete. More importantly, integrability of every squared summand is a conclusion of the same proposition. A successful proof therefore cannot obtain the stated theorem just by allowing its individual expectations to use a nonintegrable zero default. The finite sum is an ordinary sum over all `d` rows. In this finite-dimensional matrix setting, the integrable Bochner moments agree with the entrywise source expectations.

## Binder and definition audit

Both exact signatures bind only the following mathematical inputs:

| Input | Classification | Reason |
|---|---|---|
| `d : Nat` | TYPING / source dimension | Finite integer dimension implicit in the source grid. |
| `q : Nat` | TYPING / source query budget | The source allows integer `q>=0`; a natural binder encodes precisely that nonnegative integer domain. |
| `hq : 2*q+1<d` | SOURCE / STANDING | The explicit original range in Lemma 4.4 and its surrounding Krylov setup. |

All remaining named objects are local `let` definitions rather than assumptions: `r,theta,t,S,feature,N,K,C` in the producer and `E,mu,r,R,L,theta,t,G,N,Y,secondSum,C` in the consumer. The carrier structures are canonical finite real/Euclidean/matrix structures from the supplied context. There are no project-owned bundled propositions, concentration events, covariance conditions, moment estimates, positivity witnesses, Gram identities, integrability assumptions, or downstream conclusions passed as binders. There is no EXCESS binder in the supplied signatures.

Every meaning-carrying local mathematical object is literal. In particular, the feature `if k.val=0` is the source constant-coordinate case distinction, and the indicator's zero branch is the source truncation. Neither is an invented fallback off the stated mathematical domain. The source range implies `d>=2` and `r>=1`, so the totalized real inverse/division at `d=0` does not enter any admitted parameter instance. The canonical Gaussian and integral definitions are standard ambient primitives, not a project definition that chooses an unproved characterized object. The consumer explicitly discharges the integrability issue as a conclusion.

## Source comparison and boundary

The seven slots agree with the independently frozen raw interpretation for the bounded formula: real paired-coordinate objects; nonnegative integer query range; universal `d,q` with the exact source inequality; no added premises; the same PSD comparison; finite-sum, ordinary-square, inclusive-cutoff and marginal-integral senses; and the literal constants `(r+2)/d^2`, `2r(r+2)/d`, and `L=2r+3log(1000d)`.

The producer is a deterministic substep of EGx11 rather than a claim to formalize all of Ex113–Ex117. It omits no necessary public source parameter by leaving out `kappa`, `n`, `tau`, or the Haar experiment: those objects do not occur in the deterministic comparison. The consumer's explicit integrability assertion strengthens the written source display by exposing a mathematical prerequisite that the Gaussian setting already supplies; it is not an assumption added for proof convenience.

The one material scope qualification is the canonical marginal formulation. The original has actual row variables `gamma_i` in the extended experiment. The consumer instead integrates each deterministic function `y_i` against the canonical `N(0,I_r)` measure. This is the correct formula for each original row moment once equality of that row's marginal law is supplied. Using one variable name `x` in each separate integral does not create a joint realization and implies no row independence. The consumer proves no original row law or expectation-transport theorem. It is faithful to the bounded canonical moment calculation; claiming an original-family result requires the separately stated marginal-law/expectation identification. This qualification was already present in the raw freeze and was not inferred from a target implementation.

No claim here establishes source-proof coverage beyond this bounded formula, actual consumption of a producer, or the absence of theorem-shaped assumptions in code. Those are reserved for the later whole-module and anti-anchored phases.

## q=0 check

With `q=0`, the hypothesis reduces to `1<d`; thus the permitted dimensions are integers `d>=2`. `Fin(q+1)` is a singleton, `r=1`, and the feature branch gives exactly `t_i(0)=1`. Hence `S_i=1`, the outer product and each tensor factor have one entry, `K=3/d`, and `C=6/d`. The producer states the valid scalar comparison `3/d<=6/d`.

For the consumer, `E` is one-dimensional standard Gaussian space, `L=2+3log(1000d)`, and `y_i(x)=x^2/d` on `x^2<=L`, zero otherwise. Its ordinary square is `x^4/d^2` times the same indicator. The sum of canonical moments is bounded by `3/d<=6/d`, and the explicit integrability conclusion is consistent with the fourth Gaussian moment. No nonconstant coordinate, positive-`q` assumption, or empty-carrier convention is needed.

## Frozen status

Type semantics: matches the bounded deterministic comparison and canonical marginal second-moment formula, with the original-experiment transport boundary stated above. Implementation/proof, compiler, source topology, decoder, and final publication judgments: unexamined. Stop after this separate freeze.
