# Phase 1 frozen independent raw-source reading

Reviewer: `/root/radial_cov_fresh_source_42df`. Date: 2026-11-11 (Asia/Tokyo).
Repository: `/Users/zhouhuanjian/ASTIS-GC`.

This is a source-only reconstruction, frozen before receipt of any Lean types, project-owned mathematical definitions, target draft, statement seal, implementation, decoder reconstruction, prior review, or graph. It is not a compilation or implementation review. The only read inputs were the repository's general instructions/protocols and the pinned raw mathematical HTML. This review changes no ledger, shared state, production code, or publication metadata.

## Pinned source and exact boundary

Source: *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, local raw HTML `.astis/huanjian-resume-20261103/2610.20492v1.html`, 951991 bytes, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

The mathematical targets are Appendix C.2 paragraph 12, display `A3.Ex108` and the actual inline formula `A3.SS2.p12.m5`. The first formula is the unnormalized truncated row second moment. The second is the expectation of the individual truncated matrix defined at `A3.Ex107`. Target coverage stops at that individual expectation. No later frame sum, centered matrix, variance proxy, concentration argument, complete Lemma 4.4, or main complexity bound is claimed here.

The raw anchor files and UTF-8 byte offsets are in `anchor-index.json`. Their text companions replace each MathML subtree by that subtree's original `alttext`; the `.raw.html` files, not the text companions, are the exact source evidence. A complete byte-identical source snapshot and the general instruction snapshots are retained under `raw-inputs/`.

## Reconstructed objects and source quantifiers

The surrounding source works with a nonnegative integer query budget q and integer ambient dimension d satisfying 2q+1<d. Integer q is explicit in the preceding source paragraph `S4.Thmtheorem3.p1.1`; the conditions q>=0 and 2q+1<d and independent Gaussian starting vectors appear at `S4.Thmtheorem4.p1.1`. Put

    r = q+1,       n = 2q+1.

Thus r>=1 and d>=2. Appendix C.2 paragraph 1 defines, for each i=1,...,d,

    theta_i = ((i-1/2) pi)/d,
    t_i = (1, sqrt(2) cos(theta_i), ..., sqrt(2) cos(q theta_i))^T in R^r,
    gamma_i = ((g_1)_i, ..., (g_r)_i)^T in R^r.

The exact midpoint grid is source Eq. (11), `S4.E11`, and is recalled verbatim in `A3.SS2.p4.m2`. The zeroth cosine coordinate is 1. The sqrt(2) multiplier belongs only to positive-frequency coordinates. There is no extra 1/sqrt(d) or 1/sqrt(r) factor inside t_i or gamma_i. The source separately places d^(-1/2) on a row of B; that B definition does not alter t_i. Gamma_i is a column vector and gamma_i gamma_i^T is an r by r outer-product matrix.

The starting vectors g_1,...,g_r are independent N(0,I_d). The source explicitly states that gamma_1,...,gamma_d are independent N(0,I_r). Set

    L = 2r + 3 log(1000d),        R_i = ||gamma_i||_2^2,
    A_i = {R_i <= L}.

The logarithm is the natural logarithm, as in the source exponential tail calculation; L is a finite positive real at these source parameters. Ex107 defines the r^2 by r^2 matrix

    Y_i = (1/d) (gamma_i gamma_i^T tensor t_i t_i^T) 1_{A_i}.

The tensor is the Kronecker product in the displayed order: the gamma factor precedes the deterministic t factor. With row/column pairs (alpha,k) and (beta,ell), its entry is

    (1/d) gamma_i[alpha] gamma_i[beta] t_i[k] t_i[ell] 1_{A_i}.

The source conclusion is: there is one scalar a, determined by r and the common cutoff L, such that for every row i,

    E[gamma_i gamma_i^T 1_{A_i}] = a I_r,
    a = (1/r) E[R_i 1_{A_i}],
    E[Y_i] = (a/d) (I_r tensor t_i t_i^T).

The formula for a may use any row because all rows have the same marginal law. It is a definition, not a freely supplied scalar with an assumed isotropy property. Under the source choice of L, a depends on d and q through r and L; it does not depend on i, theta_i, or t_i. No absolute constant or unspecified parameter enters these formulas.

## Seven semantic slots frozen from the source

1. **Objects:** finite Euclidean Gaussian row gamma_i; its squared Euclidean norm R_i; radial cutoff event A_i; deterministic normalized cosine vector t_i; identity I_r; ordinary outer products and Kronecker products; scalar a; individual matrix Y_i.
2. **Domains:** q is a nonnegative integer, d a finite positive integer with 2q+1<d, r=q+1, i in {1,...,d}; gamma_i and t_i are in R^r, the row moment in R^(r by r), and Y_i in R^(r^2 by r^2). All entries and scalars are real.
3. **Quantifiers:** fix source-valid d,q and the Gaussian construction; define L and all rows; the same defined a works for every i. There is no choice of a depending on an exceptional event or on a particular realized sample.
4. **Assumptions:** the common standard Gaussian row marginal and finite deterministic dimensions suffice for the two expectation identities. Cross-row independence belongs to the source construction but is unnecessary for these local conclusions. The source restrictions on q,d are standing context, not consequences of concentration. No conditioning, high-probability event, smallness condition on a later bound, or adversarial coefficient is a premise here.
5. **Conclusion:** exact equality of unnormalized matrix expectations with the displayed isotropic row moment and deterministic tensor factor; neither an estimate nor an almost-sure equality of the random matrices themselves.
6. **Scopes/senses:** expectation is under the original Gaussian experiment, the indicator is multiplied inside the expectation, and the event is R_i<=L. These are ordinary finite matrix-valued expectations. The object is a second moment. It must not be silently replaced by a centered covariance or conditional expectation.
7. **Constant dependencies:** the exact coefficient is a=(1/r)E[R_i 1_{R_i<=L}], and the matrix mean has the additional exact 1/d. Common row marginal plus a common cutoff explain the uniformity in i. The deterministic cosine shape is not used in the local expectation calculation beyond providing a fixed finite vector.

## Normalization and endpoint checks

The indicator truncation is unnormalized: there is no division by P(A_i). Conditional second moment given A_i, when defined, would introduce that denominator and would be a different formula. The source later notes E[R_i]=r and therefore 0<=a<=1; this is consistent with retained Gaussian mass and confirms that a is not an imposed unit normalization.

The event includes its boundary: R_i<=L. The complementary tail event in the intervening Ex109 is R_i>L. A continuous Gaussian makes equality at the positive boundary null, but that fact does not license changing the literal definition or inventing fallback semantics. There is no random cutoff and no threshold depending on gamma_i beyond R_i's comparison with the fixed L.

The endpoint q=0 gives r=1, n=1 and d>=2. The cosine vector is exactly (1), gamma_i is one real standard Gaussian coordinate, Ex108 is the scalar second-moment equality, and Y_i=gamma_i^2 1_{gamma_i^2<=L}/d. Nothing in either scoped identity requires q>0 or r>=2. Dimension r=0 is outside this source boundary and must not be introduced by totalizing 1/r.

## Source proof sequence and omitted background

The source sequence is:

1. C.2 paragraph 1 fixes r,n,t_i,gamma_i and asserts independent standard Gaussian rows.
2. C.2 paragraph 10 fixes L and R_i. The subsequent moment-generating function/tail argument establishes other truncation facts but is not a prerequisite for the scoped identities.
3. Paragraph 12 introduces the independent truncated matrices and defines Y_i in Ex107.
4. The sentence “By radial symmetry” immediately supplies Ex108, including the trace-normalized definition of a.
5. The next sentence says a is the same for every i. E[R_i]=r then gives 0<=a<=1.
6. Ex109 is an intervening tail-bias identity and upper bound; it is excluded from this target and is unnecessary for deriving the individual E[Y_i] formula.
7. The actual inline p12.m5 then states E[Y_i]=(a/d)(I_r tensor t_i t_i^T). Subsequent frame summation is outside this packet.

The source compresses the radial-symmetry step. Its omitted background is: the standard Gaussian law is invariant under finite-dimensional orthogonal changes of coordinates; the cutoff depends only on the Euclidean norm and is invariant under the same changes; hence the integrated outer-product matrix is a scalar multiple of identity. Equivalently, coordinate sign changes cancel off-diagonal entries and coordinate permutations equalize diagonal entries. Tracing the finite matrix then identifies that common diagonal value as E[R_i 1_{A_i}]/r. These are explanation of the source's compressed step, not extra assumptions to expose as public theorem premises.

The individual Y_i expectation uses linearity and pulling out the fixed finite Kronecker factor. Its exact coefficient is inherited from Ex108 and Ex107. It does not use a trigonometric frame identity, the fact that rows are independent of each other, or a sum over i.

Measurability and finite integrability are omitted in the paper's notation but follow from the already stated Gaussian object. The coordinate polynomials, norm square, radial sublevel indicator, outer product, and deterministic tensor product are Borel measurable. Every entry of the truncated outer product is dominated in absolute value by R_i, and its operator norm is R_i 1_{A_i}. Since E[R_i]=r<infinity, the matrix is integrable. Likewise the operator norm of Y_i is bounded by (||t_i||_2^2/d)R_i. There are finitely many matrix entries, so entrywise expectation and the finite-dimensional Bochner expectation coincide. This is a finite expectation, not an arbitrary totalized integral that can silently return zero for a nonintegrable expression. No new integrability hypothesis is required at the source-facing boundary. Standard Gaussian finite second moments discharge it internally.

## Coverage dispositions and limits

**Included source nodes:** midpoint-grid convention; nonnegative integer query budget and 2q+1<d context; C.2 p1 definitions and common Gaussian row law; C.2 p10 definitions L,R_i; p12 introduction/Ex107; radial-symmetry sentence/Ex108; same-a sentence and E[R_i]=r background; actual p12.m5.

**Excluded with reasons:** B and its geometry are surrounding coordinate bookkeeping; the spectrum/kappa parts of Eq. (11) do not affect these two means; the full Krylov-space lemma and its final bound are later consumers; the earlier cosine frame expectation/sums and every later frame sum are unrelated to the individual mean; p10 tail estimates and the all-rows truncation event are concentration/bias preparation; Ex109's bias bound is a separate estimate; centered matrices, variances, Bernstein/concentration, and all final bounds are outside the assigned boundary.

**Raw-source exposure disclosure:** while locating definitions, this reviewer also saw source-only contextual material beyond the assigned mathematical coverage: the complete source statement at S4.Thmtheorem4, the complete C.1 section emitted by a scope-location query, C.2 p4's trigonometric paragraph, and S4 paragraphs returned by an integer/query-budget search. None was implementation, a target type, a prior report, or a decoder output. Those contextual conclusions are not imported as premises or claimed coverage. The exact target interpretation above comes from the identified anchors.

No invalidity or required source repair has been found for the two scoped formulas. The compressed symmetry and finite-integrability bridges are omitted background arguments, not evidence of a missing source premise. Any stronger or differently normalized proposition in a later type packet must be reviewed against this frozen reading.

Phase 1 ends here. Await the selective exact type/definition packet before performing any comparison.
