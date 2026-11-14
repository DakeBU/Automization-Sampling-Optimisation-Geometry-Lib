# Phase 2: independent source versus whole-code review

Reviewer: `mgf_fresh_source_5b7e`.
Candidate commit: `4869db55d340cee39f0ba4d49fb0a7a4309ba2d6`.
This review was completed after the frozen source-only phase 1 and before any decoder reconstruction, canonical reviewer packet, reader candidate, earlier semantic verdict, or native acceptance record was seen.

## Result and precise scope

**No blocking source/code mismatch found at the advertised local layer.**

The new production theorem is a faithful **real, finite nonempty matrix, normalized single-matrix specialization** of Tropp Lemma 6.7, with explicit standing regularity. It proves the actual matrix-exponential expectation inequality with the source's almost-sure one-sided cap and all positive parameters. The test theorem is a genuine internally discharged application to the normalized cosine-weighted, centered, closed-cutoff Gaussian source summand on the original product experiment.

This is a direct source-versus-whole-code result, not the canonical seven-slot round-trip verdict. Reader review remains pending. No build was executed and no compiler/native acceptance record was read. ROOT's statement that a build occurred was not used as evidence of source truth or as independent compilation verification.

The reviewed primary files were extracted from the immutable commit and matched the supplied digests:

| Role | Exact file | SHA-256 | Complete lines read |
| --- | --- | --- | --- |
| P | `AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinMgf.lean` | `b46bb5a3eabbcadf31fee93d48c1fbabf9b5b42cf717a8a17c8c8cfdd210a3f3` | 1-121 |
| T | `Tests/GaussianComplexityBernsteinWeightedMgf.lean` | `42f372143ffe52e4372271d09fbc6b67391739f2fe2a5fbfffe6cd9fa586936e` | 1-159 |

Line references below refer to these complete archived files. Imports, scopes, namespaces, universes, all private declarations, all theorem binders, and every proof body were included, not just the final conclusions.

## Meaning of the formal objects

The fixed toolchain is Lean 4.33.0. The candidate manifest pins Mathlib to `db584cd6d46c92f209a44c0f1c829460d327499d`; the installed checkout reports that revision. Meaning-carrying Mathlib files were compared byte-for-byte to that Git tree and archived under `fixed-mathlib/`.

- `Matrix.PosSemidef` includes Hermitian symmetry and nonnegative quadratic forms. It is not entrywise positivity.
- With `MatrixOrder`, `A <= B` is definitionally `(B-A).PosSemidef`. Consequently the public P cap `(1-X).PosSemidef` is the source upper spectral cap, for Hermitian X. It places no lower spectral restriction on X.
- `Matrix.Norms.L2Operator` is the operator norm obtained from Euclidean continuous linear maps, not the default entrywise/sup norm.
- `NormedSpace.exp` on real matrices is the algebra/matrix exponential. Its general totalized definition has an irrelevant no-rational-algebra fallback, but real matrices have the required algebra structure, and the proof also explicitly identifies it with continuous functional calculus of `Real.exp`. No candidate-defined exponential, default matrix, or surrogate scalar function replaces the source object.
- `MeasureTheory.integral` is the Bochner integral, totalized to zero outside integrability. In P, integrability of X and X squared is assumed as explicit source-standing regularity, while integrability of the exponential is **derived**. In T, the actual mean integral of Y is backed by the imported actual-source integrability theorem; integrability of Z, X, X squared and the exponential is established through genuine dependencies. No source equality is obtained by taking advantage of nonintegrable zero defaults.
- `stdGaussian` is the finite-dimensional standard Gaussian measure built from independent `gaussianReal 0 1` coordinates; `map_pi_eq_stdGaussian` and its probability instance agree with the source law. `WithLp.toLp 2` preserves the literal coordinate vector and gives its Euclidean norm.

## P: complete declaration and proof audit

The full P module contains two private helpers and one public theorem. There are no extra declarations, scoped public parameters, mathematical axioms, placeholder closures, or theorem-shaped assumptions hidden behind project-owned structures.

| Complete declaration | Code range | Source connection / independent check |
| --- | --- | --- |
| `capped_matrix_exp_norm_le` | 13-29 | Derives `||exp(s A)|| <= exp(s)` from Hermitian A, A<=I, s>0 using the same-matrix spectral transfer rule. Negative eigenvalues are unrestricted. Because exp(s*x)>0 and x<=1, its absolute value is at most exp(s). This fills an explicit regularity obligation from Tropp section 2.2; it does not change the lemma's cap to a two-sided norm bound. |
| `exp_sub_one_add_posSemidef` | 31-43 | Directly realizes Tropp (2.3), I+A<=exp(A), by scalar `1+x<=exp x` and CFC. Only Hermitian A is assumed. It does not apply a false operator-monotonicity principle to two unrelated matrices. |
| `centered_bounded_matrix_mgf` | 46-119 | Real normalized one-matrix MGF. The exact conclusion is exp(g(s) integral X^2) minus integral exp(sX) PSD, where g(s)=exp(s)-s-1. This is the correct order direction and the correct matrix meaning. |

Public binder audit for P:

| Binder / condition | Classification and source relationship |
| --- | --- |
| Omega and measurable space; probability measure mu | Probability-space typing/standing setting. The source uses a random matrix and expectation; probability normalization is necessary for E I=I. |
| Finite decidable nonempty matrix index type, real entries | Carrier specialization/typing. Real symmetric is narrower than the source's general complex self-adjoint carrier. Nonempty finite indices represent positive matrix dimension. The theorem and reader must keep the real specialization explicit; it is not a complete complex-matrix port. |
| `AEStronglyMeasurable X mu` | Explicit regularity from section 2.2. It is redundant with the following `Integrable X mu` by Mathlib's definition of Integrable, so it adds no extra mathematical restriction. |
| `Integrable X mu`, `Integrable (X*X) mu` | Explicit source-standing regularity, needed for genuine mean and finite second moment. A one-sided spectral cap does not by itself give the second moment; the theorem correctly does not pretend otherwise. |
| a.e. Hermitian | Source object assumption. For real entries this is symmetry. |
| a.e. `(1-X).PosSemidef` | Source `lambda_max(X)<=1`, interpreted a.s. as specified in section 2.2. It is not pointwise everywhere and not `||X||<=1`. |
| `integral X=0` | Source centering assumption, on a genuine integrable X. |
| `s>0` | Exact explicit source parameter range. No upper bound on s was added. |

No EXCESS mathematical premise was found for the stated real normalized source specialization. In particular, independence, exponential integrability, PSD X, and a two-sided norm cap are not public premises.

All local proof stages were checked:

1. P64-72: continuity gives exponential measurability. The cap helper bounds its norm a.e.; probability implies finite measure; `Integrable.of_bound` then gives actual exponential integrability.
2. P73-81: a.e. Hermitian X implies X*X = X-star*X is PSD. The actual integrable square is averaged using the imported PSD integral theorem. Nonnegativity of g(s) makes C=g(s) E X^2 PSD and hence Hermitian. This is a proved local fact, not an extra public covariance assumption.
3. P82-104: Q=I+sX+gX^2 and F=Q-exp(sX) are genuinely integrable. Integral additivity, scalar linearity, probability normalization and zero mean give E Q=I+C and E F=I+C-E exp(sX).
4. P105-111: the already existing deterministic `bernstein_exponential_quadratic_bound` supplies F>=0 a.e.; positivity under integration is applied only after F's integrability is proved.
5. P113-119: I+C<=exp(C) and I+C-E exp(sX)>=0 are added in the PSD cone. The final algebraic decomposition preserves the intended noncommutative order. No multiplication of unrelated expectations or exponential-of-a-sum factorization appears.

The imported deterministic module was read **in full** (148 lines). Its scalar integral-remainder kernel proves the smooth source remainder, including x=0, and monotonicity on the entire real line when s>0. The source leaves this as a differential-calculus exercise; replacing that omitted computation by the equivalent integral-kernel proof does not alter the statement or source assumptions. Its final transfer is on the same matrix, and it proves the exact source quadratic exponential bound on the full x<=1 domain.

The imported PSD integral module was read **in full** (44 lines). It proves that the true PSD cone is closed and convex, then applies Mathlib `Convex.integral_mem` with a real probability measure and integrable input. It is ASTIS reusable background for Tropp (2.13), not a theorem explicitly printed in the Gaussian source.

## T: literal original experiment and internally discharged application

The full T module contains one private cap-conversion lemma and one private application theorem, with no public mathematical claim added by the test module.

| Complete declaration | Code range | Audit |
| --- | --- | --- |
| `one_sub_posSemidef_of_norm_le_one` | 11-19 | The norm of a Hermitian matrix bounds the absolute value of each spectral value, hence each spectral value<=1. This is a correct sufficient-condition adapter for the Gaussian source's two-sided norm bound. It is not substituted into P's public cap hypothesis. |
| `actual_source_weighted_normalized_single_summand_mgf` | 21-157 | Under only natural d,q and the source condition `2*q+1<d`, unfolds the original law and source formulas, proves all application hypotheses internally and invokes P for every s>0 and every source row i. |

The theorem's objects at T23-49 agree literally with the Gaussian local experiment:

- Omega is r independent d-dimensional vector draws, not a replacement space whose independent rows are merely assumed.
- mu is the actual finite product of `stdGaussian (EuclideanSpace R (Fin d))`.
- `row i omega` collects the i-th physical coordinate from all r columns, matching gamma_i. The source's 1-based i is represented by `i.val+1`; the angle `(i.val+1-1/2)*pi/d` is exactly the midpoint grid.
- `t i 0=1`; the nonconstant coordinate k is `sqrt(2)*cos(k*theta_i)`, for k=1,...,q. The order of Kronecker factors is gamma outer product first, t outer product second, matching Ex107.
- Y uses the **closed** condition `||row||^2 <= L`; its false branch is zero, precisely the source indicator formula. This is not conditioning or renormalization of the Gaussian law.
- mean_i is the **actual** integral of Y_i against this same mu. Z_i=Y_i-mean_i. No arbitrary center or precomputed certificate is substituted.
- rho=`2*r*(L+1)/d` is the source R_star from Ex112. The test defines X_i=rho^-1*(w_i Z_i), where w_i=cos((2q+1) theta_i). This normalization is explicit in the theorem and must be explicit in the reader.
- The matrix index is `(Fin r x Fin r)`, so the matrix dimension is r^2. The conclusion is a normalized single-summand expectation inequality, not an r^2-prefactored tail inequality.

Every local stage was checked, including the statements of the actual dependencies:

| T range | Obligation discharged internally |
| --- | --- |
| 85-89 | Matrices have the Borel structure, and the exact Gaussian product law is a probability measure. |
| 93-105 | Radius and structure theorems are called with only hq. Their fully expanded definitions match the local Y, mean, Z, mu, L and t. No norm, integrability, independence or mean certificate becomes a public assumption. |
| 106-112 | hq implies d>=2 and hence d>0. r=q+1>0, log(1000*d)>=0, and L+1>0 yield rho>0. Thus the inverse in X is never an off-source zero-inverse branch. |
| 113-119 | Source Y and actual-mean operator-norm estimates yield `||Z_i||<=rho`, exactly the triangle-bound form of Ex112. |
| 120-126 | Uses `abs(cos)<=1`, not cos>=0. Negative cosine weights are fully allowed. |
| 127-138 | Positive rho gives `||X_i||<=1`, then Hermitian structure gives the source one-sided cap. Scalar Hermitian scaling holds for negative real w as well. |
| 140-150 | Measurability and integrability pass through deterministic scalar multipliers; actual mean zero gives E(w_i Z_i)=0 and E X_i=0. No weighted-mean PSD assumption is introduced. |
| 151-154 | The squared matrix is measurable and has norm at most 1; its integrability follows from the exact finite probability law. This avoids assuming a fourth-moment theorem for the normalized bounded summand. |
| 155-157 | The public P theorem receives the internally proved hypotheses and the caller's arbitrary positive s. |

The structure dependency returns independence of the centered Z_i family, but T correctly discards that component because a one-matrix MGF does not require independence. T does not claim a sum-level theorem or use independence implicitly.

Endpoint and sign checks:

- q=0 is included: hq becomes 1<d, r=1, t has only its constant coordinate, and the matrix index is nonempty. No step assumes q>0.
- The closed cutoff includes equality R_i=L; none of the dependencies silently uses an open retained ball.
- All s>0 are retained, without a small-s range.
- Negative weights occur already for q=0,d=2 at the last grid point (cos(3*pi/4)<0). The proof is uniform in these values through absolute norms and real scalar Hermitian scaling; no special positive-weight law is substituted.
- There is no kappa binder, consistent with this local concentration ingredient's independence from kappa.

## Actual dependency reading and no hidden source assumptions

The following additional ASTIS modules were extracted from the same immutable commit and read completely. Their hashes are recorded in `archive-manifest.json`:

1. `FixedSpectrumSourceMatrixRadius` (226 lines): rank-one and Kronecker operator-norm identities are proved, and the source t bound, actual truncated mean and Gaussian second norm moment yield Ex111's Y/mean bounds.
2. `FixedSpectrumSourceMatrixStructure` (148 lines): actual Y measurable/centered structure and Hermitian symmetry are constructed; zero mean follows from integrability and the true mean integral.
3. `FixedSpectrumSourceMatrixMean` (120 lines): uses the actual row transport and retained row second moment; linear Kronecker transport gives the source mean, with no assumed row-law certificate.
4. `FixedSpectrumTruncatedRowMoment` (182 lines): closed retained ball, integrability, sign-flip cancellation, coordinate-swap symmetry and the retained radial trace give aI. The scalar is the unnormalized retained radial moment divided by r, not a conditional covariance.
5. `FixedSpectrumSourceRowLaw` (54 lines): proves the canonical row marginal through the original independent-column Gaussian product measure.
6. `FixedSpectrumSourceRowIndependence` (98 lines): transports the full scalar-array product law by flattening, transposing indices and regrouping. It does not infer joint independence merely from correct scalar marginals.
7. `StdGaussianMoment` (59 lines): true Gaussian L2/covariance facts and finite-dimensional Parseval establish E||gamma||^2=r and integrability.
8. `FixedSpectrumCosineGram` (168 lines): full discrete cosine frame formulas and the required t bound, including q=0. The frame bound actually used by Radius is internally proved from the cosine square bound.
9. `FixedSpectrumGridAlias` (86 lines): literal midpoint-grid cosine alias; used by the frame module's orthogonality calculations. This is a dependency-context check, not new credit for Gaussian C.3 or its target-moment branch.

No circular dependency or theorem-shaped assumption smuggling was found in these actual call paths. ASTIS dependency reading here checks the candidate's object/assumption semantics; it does not refresh any older source-review or publication status by implication.

## Boundaries that must remain visible

No production-code repair is requested for the pinned candidate at this local layer. The following qualifications are part of the result and must be retained through any later reader/packet work:

1. The public theorem is explicitly real, normalized and single-matrix. It is not a full complex-carrier port of Tropp, not a sum-MGF theorem, and not Ex121.
2. Tropp is independently matching background. The Gaussian original does not explicitly name/cite Tropp at Ex121. Do not attribute a direct Gaussian-to-Tropp citation that the original does not contain.
3. The source's broad standing regularity has been expanded into measurable/integrable assumptions in P. The exponential integrability is derived; second-moment integrability remains explicit. Do not describe the one-sided cap alone as implying the latter.
4. T proves the normalized **cosine-weighted single-summand** application. It does not itself provide a separately stated unweighted application theorem, a sign-pair/sum result, a uniform variance sum, a two-sided operator-norm tail, or a concentration event.
5. Existing Gaussian Ex107-112 mean/radius/structure facts used here remain existing genuine dependency obligations. This review does not reclassify them as new independent progress or erase their prior source boundaries.
6. Gaussian Ex113-120 include the fourth-moment and summed variance work needed for Bernstein; P/T do not establish that whole sequence merely by proving integrability of each normalized square. The coefficient v_star, tail prefactor 2*r^2, failure probabilities, truncation-event budget, absolute-constant simplification and simultaneous Krylov conclusion remain outside this new local theorem.
7. Fact C.6, Lemma 4.4, both main lower bounds, whole-paper closure, merge/main/site delivery and purification remain unaccepted by this bounded review.
8. No accepted source repair is inferred. The phase-1 observations about broad source regularity, the omitted scalar calculus exercise, and the unnamed exact Bernstein reference remain recorded rather than rewritten by proof success.

Pending next inputs: immutable authored lesson/publication/fold/source/locator materials for a separate reader review; canonical anti-anchored reviewer packets only after this report is frozen. No normal VERIFIED API has been called.
