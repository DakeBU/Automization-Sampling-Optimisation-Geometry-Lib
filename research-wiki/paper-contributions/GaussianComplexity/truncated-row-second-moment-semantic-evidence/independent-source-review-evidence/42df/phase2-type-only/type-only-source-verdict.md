# Phase 2 frozen type-only source comparison

Reviewer: `/root/radial_cov_fresh_source_42df`. Date: 2026-11-11 (Asia/Tokyo).

**Verdict:** The two exact proposed types are source-compatible at the canonical single-row marginal boundary. Their formulas agree with the frozen raw-source reconstruction after the explicit finite-index conversion below. The types contain no excess mathematical premise, no conditional normalization, no replacement covariance, and no supplied moment identity. Source-family row-law/integral transport remains a separately identified obligation; these types do not themselves state that transport. No source repair or additional source-facing assumption is required.

This is type/definition review only. There is no implementation to verify, and this report does not certify compilation, the eventual proof's use of the producer, a final source correspondence declaration, or a ledger transition. No candidate exposition, proposed source map, decoder output, prior review, or graph was opened. The authorized selective packet itself includes brief outcome/meaning metadata; the decision below is grounded in its exact signatures, printed canonical bodies, underlying integral definition, and my previously frozen raw-source reading.

## Immutable inputs

The Phase 1 source report remains byte-identical: `../phase1-source-reading.md`, 11977 bytes, SHA-256 `918456ba2da9330388d921dc8d7de718537472edd82d39abaa1201d3a839462f`. Every one of the 37 Phase 1 manifest entries was rehashed and matched before this comparison.

The sole new input was `.astis/huanjian-gc-truncated-radial-covariance-20261111/selective-type-definition-packet-v2.json`, 12169 bytes, SHA-256 `ca055c5b2b92df9c5426ff2ddcf8d91677971381a5f309320a3859be6235ee8b`; its exact bytes are copied beside this report. Its supplied seal binding is `ee9d261db9301f0fa750102f8105c27fbbbcef9e8a19f900636b705f461b18dd`, and its supplied definition-context binding is `d3517d6dbb577297688a00f792940dc691ed4c23f16ecc96d63d1239cc2a679a`. I did not open a seal file or other context artifact.

Direct hashes of the exact signature strings match their packet digests:

- producer `actual_truncated_row_second_moment`: `e231ce32f517936350efface8c277491562d1537dcc02441db6907410929ae05`;
- private consumer `actual_truncated_matrix_summand_mean`: `0395f749c993cc8ebad7f71d3feb36a10c84543fb54fb35dabfe81a6ded54323`.

The embedded literal-print-body string hashes to its stated digest `f8da081a8f6886773ab72e7adf793fc042f9fa540467b57560db775c4b1bef10`. The packet pins Mathlib commit `db584cd6d46c92f209a44c0f1c829460d327499d`. No Mathlib/API file search was conducted in this phase.

## Producer comparison against Ex108

The producer quantifies only over natural d,q and hq: 2*q+1<d. Its local lets select

    E = EuclideanSpace R (Fin (q+1)),
    mu = stdGaussian E,
    r = real cast of (q+1),
    R(x) = ||x||^2,
    L = 2*r + 3*Real.log(1000*real(d)),
    a = (integral of 1_{R<=L} R under mu)/r.

These are the source row dimension, Euclidean squared norm, exact cutoff, and unnormalized radial coefficient. q being a natural includes q=0 without adding a positivity assumption. hq implies d>=2; q+1 is positive. Division by r and d therefore has its intended ordinary real meaning on every admitted parameter value.

`Matrix.vecMulVec (WithLp.ofLp x) (WithLp.ofLp x)` has real entry x_alpha*x_beta. It is the uncentered outer product x*x^T: no conjugation, subtraction of a mean, or additional factor is present. `Set.indicator {R<=L} G` retains this matrix on the closed radial sublevel and is zero outside it. `Matrix.one` is the diagonal-one identity matrix. Thus the asserted equality

    integral kept dmu = a smul I

has exactly Ex108's matrix formula under a standard Gaussian row law. The additional `Integrable kept mu` conjunct makes implicit finite expectation explicit as a conclusion. It is not a caller-supplied regularity or moment premise.

## Consumer comparison against Ex107 and p12.m5

For j:Fin d, the consumer defines

    theta(j) = (real(j.val)+1/2)*pi/real(d).

The source index corresponding to j is i_source=j.val+1. Consequently

    i_source-1/2 = j.val+1/2,

so the literal formula is the source midpoint grid, with neither a shift error nor an endpoint grid. The feature index k:Fin(q+1) is a frequency index k.val in {0,...,q}. It is not one-based. Its branch at k.val=0 gives exactly 1; every positive frequency gives sqrt(2)*cos(k.val*theta(j)). Hence the vector is exactly the source t_i, including the exceptional normalization of its zeroth coordinate. At q=0 its sole coordinate is 1.

With the producer's same G, R, L, a, the consumer uses

    Y(x) = 1_{R(x)<=L} [real(d)^(-1) smul (G(x) kronecker t_i*t_i^T)].

This is precisely Ex107. Moving the indicator syntactically outside the scalar/tensor expression does not change the function: inside the event it is the displayed source matrix; outside it all entries are zero. The reciprocal is exactly 1/d.

The matrix's paired indices are `(gamma coordinate, feature frequency)`. The printed Kronecker type has product row and column indices, in the same factor order as the source. Entry ((alpha,k),(beta,ell)) is

    real(d)^(-1) * x_alpha*x_beta * t_i[k]*t_i[ell] * 1_{R(x)<=L}.

The proposed equality has coefficient a/real(d) and identity in the gamma factor, so it is the actual source inline p12.m5,

    E[Y_i] = (a/d) (I_r kronecker t_i*t_i^T).

`Integrable Y mu` again occurs as a conclusion. There is no row sum, frame identity, centered matrix, variance, concentration event, or final Lemma 4.4 conclusion in this type.

## Canonical measure, norm, and Bochner semantics

The printed `EuclideanSpace` is PiLp 2. The input norm in R(x) is therefore the Euclidean norm. `WithLp.ofLp` exposes the coordinate function without changing or rescaling the underlying vector.

The printed `stdGaussian` is the pushforward of the product of real `gaussianReal 0 1` laws through an orthonormal basis. Thus it is the ordinary centered, covariance-identity Gaussian on the finite Euclidean carrier. The standard orthonormal basis may be represented through canonical library choices; the source agreement uses the invariant standard-Gaussian law, not an unjustified claim that every implementation step of that basis is definitionally identical to the source's coordinate construction. No Gaussian-law certificate appears as a theorem premise.

The packet's scope `Matrix.Norms.L2Operator` selects the real Euclidean operator norm. The printed normed additive group is induced through matrices as continuous linear maps between Euclidean spaces. It is not an entrywise maximum or Frobenius norm. The finite matrix space is complete, and this norm gives the usual finite-dimensional topology; integration consequently agrees with the ordinary source matrix expectation.

The exact underlying Bochner definition has a complete-space branch and then an integrability branch; a nonintegrable function would return zero. The two matrix-integrability assertions are explicit target conjuncts and therefore rule out treating either displayed matrix equality as a consequence of that totalized nonintegrable branch. The scalar a's radial integral is not separately asserted integrable in the proposed signatures, but it is a finite measurable truncated squared norm under the fixed Gaussian probability measure at finite L. Its integrability is a source-implicit internal obligation, not a missing source premise or an invented zero fallback. A final proof/source check should ensure this ordinary-integral meaning is discharged when it interprets a.

## Seven-slot audit

1. **Objects — aligned.** E, mu, R, G, kept, a, t_i, Y and identity are literal standard Gaussian/Euclidean/matrix objects with the correct dimensions.
2. **Domains — aligned after explicit indexing.** Natural d,q match the integer query-budget setting; E has exactly r=q+1 real coordinates; source rows 1,...,d correspond to Fin d by successor; source feature frequencies 0,...,q correspond to Fin(q+1) by val. Product indices have gamma first.
3. **Quantifiers — aligned at the canonical marginal boundary.** Producer proves one generic standard-row identity for every valid d,q. Consumer proves the deterministic row-specific Y identity for every i:Fin d under that same common row law. Neither declaration quantifies over the original joint family or arbitrary ambient probability space.
4. **Assumptions — no excess.** The only proposition input is source hq; Gaussianity is fixed in the definition of mu, rather than assumed isotropy, finite moments, a covariance identity, or a caller-provided expectation equation. No q>0, r>=2, smallness, or all-rows good-event premise appears.
5. **Conclusions — aligned with implicit regularity made explicit.** Exact unnormalized second-moment equality and exact individual Kronecker expectation, together with integrability conclusions. The producer does not separately claim a in [0,1] or the Ex109 bias estimate; those are outside this target.
6. **Scopes/senses — aligned with the stated transport limit.** Closed cutoff R<=L; original law rather than conditioning; real matrix-valued Bochner expectation; same common a. Canonical law model is used instead of the literal original family experiment, requiring the source bridge below before whole-family credit.
7. **Constant dependencies — aligned.** r=q+1, exact L=2r+3log(1000d), exact trace normalization 1/r and matrix factor 1/d. a is independent of i because mu and L are independent of i. No hidden constant or changed cosine multiplier is introduced.

## Explicit remaining bridge, without an added premise

The source states the formulas for gamma_i=((g_1)_i,...,(g_r)_i) in a jointly constructed independent Gaussian array. These types instead work on E with the canonical measure mu. A source correspondence claiming the paper's actual row formulas must still identify each source row with that canonical marginal and transport the integrals. Precisely:

1. Reindex source rows i_source in {1,...,d} by j:Fin d with i_source=j.val+1, and source Gaussian labels 1,...,r by alpha:Fin(q+1) with label=alpha.val+1. Feature frequencies remain zero-based.
2. From the source's independent g_a~N(0,I_d) construction, establish that the E-valued row map is measurable (or has the appropriate almost-everywhere measurability) and its pushforward law is mu. This is a consequence of the existing source Gaussian construction, not a new public hypothesis. If the original source row-law assertion is used as background, its exact canonical-law identification still must be recorded.
3. Use that law equality to transport scalar and matrix integrability/integrals for the exact radial functions and exact Y_i. The deterministic feature row agrees by the midpoint/frequency reindexing above.

Common row marginal suffices for this bridge for every i. Cross-row independence is necessary in the source's later concentration setup but is not used by either local expectation identity. The producer and consumer do not encode or prove joint row independence. No new premise should be added to compensate for the absent transport declaration, and no full-family or concentration credit should be inferred from these marginal types alone.

Type-only source acceptance is therefore bounded: the exact proposed canonical marginal types may proceed to proof, while the source-family transport, proof implementation, compilation, dependency use, and final source verification remain unverified work.
