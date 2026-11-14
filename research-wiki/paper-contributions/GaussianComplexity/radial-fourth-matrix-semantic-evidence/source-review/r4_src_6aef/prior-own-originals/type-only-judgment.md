# Independent type-only mathematical judgment

This is a separate second phase. The original raw-source reading remains
sealed and unchanged. The sole new input was the exact selective packet
`.astis/huanjian-gc-radial-fourth-matrix-20261111/selective-type-definition-packet.json`,
SHA-256 `899221eab62ec75aa1eb8d90f62c4a2e86c154037b934042433b11acce08b6d2`.
Its referenced files, receipts, prior shared provenance, implementation,
graphs, decoder, mappings, and exposition were not opened. Inline literal
definitions were read as definitions, not as proof or verification evidence.

## Judgment and scope

Both proposed signatures are mathematically faithful to their stated local
source roles. No excess mathematical premise, definition mismatch, constant
drift, endpoint loss, or blocking type-level source discrepancy was found.

The producer expresses Ex113 under the canonical standard Gaussian law and
also asserts its source-implicit integrability. The consumer expresses the
individual-summand PSD inference supporting the first inequality of the p14
aggregate. It is a source-supported termwise inference rather than a
separately printed source equation. It does not assert the aggregate bound,
the final variance constant, centered-square identities, concentration,
or the public Lemma 4.4.

This judgment does not certify that either signature elaborates or that a
proof implements it. In particular, actual consumption of both producer
conclusions, the square calculation, and PSD/integral transport remain for
the separately authorized code phase. No source correspondence beyond the
two exact mathematical interfaces is accepted by this phase.

## Exact binding

The packet's supplied statement-seal identifier is
`cc628d801ed367e1e57e99d69449d36a90b2803f7371986b964b4864409f6dec`.
This phase did not open another statement-seal file or independently
reconstruct the seal's serialization. The following input hashes were
independently reproduced from the packet's exact strings/object:

| Item | SHA-256 |
| --- | --- |
| Producer signature | `249edf1f3d15639eca0c0db2f827bca4981faf3648653ef83fb731abe564af32` |
| Consumer signature | `d177e72a66ec143642b0518887a170f7906d9fc528a87ea399d02ee00842bfac` |
| Minimal definition context, two-space JSON plus LF | `6e519e17615212c920c3e18e57c9dd416ac5addf2511a949c1bb8050b1adee43` |
| Inline current literal definitions | `566cb351c515d58318f165c7cd2add1a6fba5994cb84ab241ae7b44b93e3a99d` |
| Inline shared canonical literal definitions | `f8da081a8f6886773ab72e7adf793fc042f9fa540467b57560db775c4b1bef10` |

The source-only seal remains
`920e93bff9d7929cf74b6d970d1afa19dbfb24c992efd943bc3de2e7288dd2d6`.
All 33 artifacts named by that seal were independently rehashed during this
phase and still matched exactly.

## Binder audit

The producer has only implicit natural-number parameters d,q and the
explicit hypothesis hq: 2*q+1<d. The consumer adds only i:Fin d. Each let
binding is a literal definition rather than a logical premise.

| Binder or component | Classification | Source justification |
| --- | --- | --- |
| d:Nat | TYPING | Finite integer ambient dimension in the source; its positive range follows from hq |
| q:Nat | TYPING | Nonnegative integer query-budget carrier |
| hq:2*q+1<d | STANDING | Exact standing range of Lemma 4.4/C.2 |
| i:Fin d, consumer only | TYPING | Universal selection of one source row i=1,...,d |
| Canonical finite Euclidean, matrix, measurable, and scalar instances | TYPING | The source works in finite-dimensional real Euclidean spaces and real matrices |

The carrier parameters are TYPING. The sole proposition premise hq is
STANDING; there is no bundled proposition requiring recursive expansion.
There are no RULED or EXCESS premises and no project-owned proposition
aliases or structures to expand. In particular, no Gaussian moment,
integrability, PSD, truncation, feature bound, expectation, variance bound,
or concentration certificate is assumed.

The hq hypothesis entails d>=2 and r=q+1>=1. It is mathematically unnecessary
for an isolated standard Gaussian fourth-moment identity, but it is an
explicit source standing restriction, so retaining it is faithful. There is
no extra q>0 restriction. Kappa, tau, and a sufficiently large C are not
needed for these local moment/algebra claims and do not appear as binders.

## Definition audit

All meaning-carrying definitions in these two signatures are literal. None
selects a characterized object, introduces an arbitrary probability law,
chooses a conditional representative, or invokes a project-owned fallback.

1. E is EuclideanSpace R (Fin(q+1)), supplied as PiLp 2. Thus it has r=q+1
   real coordinates and the Euclidean norm. WithLp.ofLp exposes those same
   coordinates; it does not rescale a vector. The ordinary Borel structure
   is the canonical structure indicated by the context.
2. mu is stdGaussian E. The supplied definition is the pushforward of
   independent scalar gaussianReal 0 1 coordinates through an orthonormal
   basis. Mathematically this is the isotropic centered Gaussian with
   identity covariance. Its meaning is independent of the chosen
   orthonormal basis. Consequently the law in the signatures is the law of
   each source gamma_i. It is not a retained or conditioned radial law.
3. r is the real cast of q+1; R(x)=||x||^2 is the source squared radius.
   G(x) is vecMulVec of the exposed coordinates with themselves, so its
   (a,b) entry is x_a*x_b. It is the unnormalized rank-one matrix xx^T.
   weighted(x)=R(x) times G(x), with no radius normalization.
4. The matrix identity is supplied as a diagonal matrix of ones; hence
   (r+2) times that identity has diagonal r+2 and off-diagonal zero, exactly
   as Ex113. Scalar action is ordinary real scalar multiplication.
5. L=2*r+3*log(1000*d) has the source constants and natural logarithm.
   For row j:Fin d, theta(j)=(j.val+1/2)*pi/d. The source row is
   i_src=j.val+1, giving (i_src-1/2)*pi/d. This is the exact midpoint grid.
6. The feature coordinates are indexed by k:Fin(q+1), so k.val=0,...,q.
   Coordinate zero is exactly one. The others are sqrt(2)*cos(k*theta_i).
   The if expression implements the source's distinguished constant
   coordinate; it is not an off-source default. feature is t_i*t_i^T.
7. The first Kronecker factor is G and the second is feature. Thus the
   pair indices are (Gaussian coordinate, feature coordinate), consistent
   with gamma_i tensor t_i. The first Fin(q+1) coordinate corresponds to
   the source a=1,...,r after adding one; the second already corresponds
   to the source j=0,...,q. Both factors have r coordinates and the matrix
   has r^2 rows and columns.
8. Y is the indicator of R<=L times d^(-1)*(G tensor feature). The cutoff
   is closed at L, returns zero outside, and has no probability
   renormalization. Its definition is exactly the source Y_i under the
   single-row standard Gaussian law.
9. The supplied multiplication instance computes a finite sum over the
   intermediate matrix index. Therefore squared(x)=Y(x)*Y(x) is ordinary
   matrix multiplication, as in Ex114, rather than entrywise squaring.
10. The upper matrix is

       ((r+2)*sum_k t_i(k)^2/d^2) * (I_r tensor t_i*t_i^T).

    The explicit finite sum is the Euclidean squared length of t_i.
    There is no function-space supremum norm ambiguity. The coefficient
    and tensor order match the source's untruncated single-row mean.
11. Matrix.PosSemidef M means Hermitian symmetry plus nonnegative
    quadratic forms for every finitely supported vector. On the finite
    real paired index set, this is precisely symmetry and nonnegative
    quadratic forms for every real vector. Therefore PosSemidef
    (upper-integral(squared)) is E[Y_i^2] <= upper in the source order,
    with the correct direction.
12. Integrable is almost-everywhere strong measurability plus finite norm
    integral. The declared matrix norm is the Euclidean L2 operator norm.
    Finite-dimensional matrix topology and completeness give the usual
    matrix-valued Bochner integral. The supplied integral definition has a
    nonintegrable zero case, but both signatures explicitly conclude
    Integrable for the exact integrand whose mean they assert. Thus that
    case cannot supply the claimed mathematics in a proved conjunction.

## Seven semantic slots

| Slot | Producer | Consumer |
| --- | --- | --- |
| Objects | Standard Gaussian vector, squared radius, rank-one matrix | Source cosine row, source radial cutoff, truncated Kronecker summand and its square |
| Domains | Real r-dimensional Euclidean space; real r by r matrices | Same Gaussian space; real r^2 by r^2 paired-index matrices |
| Quantifiers | Every natural d,q with the source standing inequality | Same, and every source row i |
| Assumptions | Only 2q+1<d, with canonical fixed law | Same; feature and cutoff are fixed literal source definitions |
| Conclusion | Integrability and exact mean (r+2)I | Integrability of Y_i^2 and the individual PSD upper bound |
| Scopes and senses | Unconditional matrix expectation under the marginal standard Gaussian law | Unconditional mean under that law; pointwise matrix square; Loewner upper bound |
| Constant dependencies | Exact r+2; no free/asymptotic constant | Exact (r+2)||t_i||^2/d^2 and the source cutoff constants; no kappa dependence |

Passing from a source random row gamma_i to integration against its canonical
law preserves these local claims. Independence between different source
rows is unnecessary for them. These signatures make no joint-law or
simultaneous-event assertion, so they cannot alone be used as a
concentration theorem.

## Source-implicit conclusions and endpoint

The source-implicit integrability is valid: weighted entries are Gaussian
quartic polynomials and the truncated squared entries are dominated by
Gaussian quartic polynomials with deterministic finite coefficients.
Finite-dimensional matrix integrability follows. It belongs in the
conclusions as proposed. Measurability, fourth moments, PSD of the removed
tail, and expectation preserving PSD order must be discharged inside the
proof, not supplied by a hidden premise.

The consumer upper bound follows by Ex114's rank-one/Kronecker square
identity, removing its indicator from a PSD expression, and Ex113's exact
mean. This is the termwise step whose sum is displayed in p14. The
additional deterministic bounds ||t_i||^2<=2r and sum_i t_i*t_i^T=dI are
needed only for the later aggregate simplification. They are neither
premises nor conclusions here. The consumer does not formalize that final
aggregate merely by testing this termwise inequality.

At q=0, E has one coordinate, r=1, and t_i=(1). The producer asserts
integrability of x^4 and E[x^4]=3. The consumer has

    Y=d^(-1)*x^2*1_{x^2<=L},
    upper=3/d^2,
    E[Y^2]<=3/d^2.

These are exactly the scalar endpoint. Summing d such terms would give
3/d before the source's later loosening to 6/d, but that sum is not in the
consumer signature. No dimension-zero or division-by-zero problem occurs.

## Retained boundaries

This is an accepted type-only judgment with no blocking mathematical
delta. Source-implicit additions are explicit integrability and the
canonical-law formulation. The consumer is an explicitly limited termwise
source inference. Proof completeness, whole-module semantics, exact
elaboration, axiom/fake-closure checks, actual producer use, publication
coverage, anti-anchored semantic review, and normal independent
verification are all outside this phase and remain unassessed.
