# Phase 3 independent mathematical, source, module and exposition judgment

I accept the **candidate-local mathematical/source semantics and authored
exposition** of the selected deterministic cosine-frame assertions and their
private actual-Gaussian entrywise-integrability/mean application. I found no
genuine source correction, added mathematical premise, false endpoint, missing
selected proof case, or mathematical repair to propose. This is an independent
code/source review, not my own Lean compilation or a global publication,
rendered-site, purification, SourceV/ledger, or Goal acceptance.

The reviewed candidate is `72e5d1405284f729f4eb600c5ae5dd556365b7e2`.
Actual `git rev-parse candidate^` returned the supplied parent
`75dcc0c9c7d9591384c6e0705e118b1ab440cd6c`. All six candidate files were read
from exact `git show candidate:path` blobs. The authorized reviewer packet was
read at its raw digest
`71a83188c154ecddba94fc180bfe6a35dae4678c644fea1390c311b3946cea09`.
Its canonical digest, computed with its self-digest field omitted, sorted keys,
compact separators, UTF-8/non-ASCII and no final LF, is exactly
`68eb57daeb019b886f64e96ea800777ac04f83af39d582ae8ff9a01c3d497921`.
The publication binding label is the supplied
`2c69e97d04c07f82e06cc79d73e7b0a1708dcae4dad8b4ae6c644e5173d27c10`;
I checked the packet's current-module, lesson projection and publication
projection against the actual candidate blobs. I did not independently
reconstruct the publication tool's full binding material or validate its
toolchain/dependency-manifest digests.

My phase-1 raw-first cognition and phase-2 selective judgment were formed and
frozen before this implementation exposure. Both manifests and every listed
payload were rechecked unchanged. The source remains the same pinned
951991-byte HTML, SHA256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
All source anchors below refer to that snapshot and phase1/source_spans.json,
with exact byte, line and math locators already frozen there.

## 1. Entire owned modules and binder/definition audit

Let P be the complete 168-line FixedSpectrumCosineGram.lean blob, SHA256
`88f29461fcac1825675e417a1bc3f3952404f1cd08183d6e484162aefe9f5d54`;
T the complete 153-line Tests/GaussianComplexityFixedSpectrumCosineGram.lean,
SHA256 `90b43f488d3fe9b6c95d4c039d0f771ee5bfecdd699b72dfa52465643f0b0dee`;
G the complete FixedSpectrumGridAlias.lean, SHA256
`c98c899bd8b596388ae433e9241a7827e01d29c3ffcc945719238fa2e96f7d60`.
I read their imports, options, namespace and all declarations/proofs. P and T
set autoImplicit false. None of these modules has ambient variable/include/omit
commands, theorem-shaped structures, extra project-owned assumptions, axioms,
sorry/admit, True predicates or trivial proof closures. A source-token scan
supports this bounded inspection; it is not a kernel axiom inventory.

P has one public handwritten theorem; T one private handwritten theorem; G one
existing public handwritten theorem. P/T expose only d,q:ℕ and hq:2q+1<d.
The natural-number carriers are TYPING; hq is the source standing range. All
θ,t,D,μ,B and scale values are literal lets. No covariance, independence,
moment, Gram, positivity, integrability or alias certificate is a caller input.
Positivity d>0 and identity-matrix PSD are established/applied internally.
The exact phase-2 private signature is an actual substring of T, not a renamed
lookalike. There are no hidden ambient binders found in either complete module.

For the public theorem's seven semantic slots:

| Slot | Judgment |
|---|---|
| objects | Same half-grid frame and odd-frequency diagonal; literal real definitions |
| domains | Equivalent after explicit one-based→zero-based reindexing and matrix/pair-index representation |
| quantifiers | Same universal d,q with strict 2q+1<d; all rows/column entries are covered |
| assumptions | Same selected-source standing range; no EXCESS premise |
| conclusion | Same three deterministic conclusions; private T additionally realizes the two selected Gaussian means and their implicit L1 obligations |
| scopes | Correctly extracted partial Fact C.5 components; range, C.6 and full Lemma 4.4 remain excluded |
| constant dependencies | Exactly dI, zero weighted Gram, 2(q+1), √2 and d^(−1/2); no chosen constant, probability or τ is claimed here |

The anonymous reconstruction stays correct for P. It was not a decoder of T;
its omission of Gaussian conclusions is appropriate to its assigned statement.
Decoder blindness/compiled flags remain supplied process metadata.

## 2. Deterministic proof, every branch and source correspondence

The source locations are A3.SS2.p4–p5 (ordinary cosine cancellation/Gram), p7
(weighted cancellation) and p8 (row square), within the complete Fact C.5 proof
A3.SS2.2. P preserves θ_i=(i+1/2)π/d, column 0 equal to 1, columns 1,…,q
equal to √2 cos(kθ_i), and the unnormalized Gram dI.

P34–53 derives d≥2 and signed-frequency cancellation on −2d<k<2d.
The k=0 branch directly returns d. For k≠0, a hypothetical divisibility
2d|k contradicts its strict signed window: nonnegative k uses the integer
divisibility lemma; negative k applies it to −k. P49–50 then calls the actual
G theorem. Thus neither |k|=2d nor a frequency-zero cancellation is silently
allowed. G's divisible branch explicitly gives d(−1)^(k/(2d)), confirming why
that endpoint must not be admitted.

G's actual proof was read, not inferred from its name. In its nondivisible
branch, sin(kπ/(2d))=0 would produce an integer multiple of 2d, a contradiction.
It rewrites the grid to a finite cosine progression and uses Real.sin_mul_sum_cos.
The right side becomes sin(kπ/2)cos(kπ/2)=0 via the double-angle identity and
sin(kπ)=0. The actual Mathlib real theorem is a real-part specialization of
the complex theorem; that proof uses sine subtraction and finite telescoping
(Trigonometric/Complex.lean 276–289 and 387–389).

This is **canonical reuse of a stronger existing alias theorem**, not a literal
copy of the paper's local displayed telescope. At the underlying mechanism,
the canonical library theorem also telescopes. It is appropriate to retain
this route difference rather than claim the source telescope is physically
present in P or create a second alias node. G's divisible branch is part of
the stronger reused result, not an additional source AND-premise.

P54–77 derives pair and triple product-to-sum. Its four triple frequencies are
n−(j−k), n+(j−k), n−(j+k), n+(j+k), a permutation of n±j±k in the source.
Coefficients 1/2 and 1/4 are exact. P78–84 expresses t_ij=c_j C_j(i) and proves
0≤j≤q from Fin(q+1). No positivity of j is assumed globally.

P85–124 handles every ordinary-Gram case. If j=k=0, both cosine modes are
zero and coefficient c_0²=1 turns (d+d)/2 into d. If j=k>0, the difference
mode is zero and 2j is nonzero below 2d; c_j²=2 gives d. If j≠k, both j−k
and j+k are nonzero in the signed window (the latter could vanish only if
both indices were zero, which would imply equality). This covers the mixed
constant/nonconstant columns without a missing branch.

P125–135 proves all four weighted frequencies positive and <2d using hq and
the index bounds. Their extrema are at least 1 and at most 4q+1<2d. P136–155
then performs matrix entry extensionality, literal diagonal multiplication and
restores the coordinate scale factors to establish both matrix equalities.

P156–166 proves each column square ≤1 for column 0 and ≤2 otherwise using
Real.sq_sqrt(2) and cos²≤1, sums exactly to 1+2q, then bounds by 2(q+1).
This is the deterministic t-row's squared Euclidean norm, not the supremum
norm of a raw function and not a uniform bound on Gaussian γ_i or random B rows.
For q=0 the single column is 1, n=1, all arguments remain valid, and the row
bound is 1≤2. The strict hq still permits d=2. No source κ or τ premise is
needed for these extracted identities.

## 3. Genuine Gaussian moments, L1 and finite expectations

T13–29 states the actual canonical law on E=EuclideanSpace ℝ(Fin d×Fin r),
r=q+1, with μ=multivariateGaussian 0 I and
B(x)_{i,(a,b)}=(√d)^(−1)x_(i,a)t_ib. Its tensor order agrees with γ_i⊗t_i.
This is a canonical realization of the source's d×r independent Gaussian
array, not an arbitrary family with supplied moments.

The actual Gaussian.Multivariate source (whole-file hash checked) defines the
standard law as an orthonormal-basis pushforward of a product of variance-one
real Gaussians. Its multivariateGaussian_zero_one (180–182) identifies 0,I with
that law; map_pi_eq_stdGaussian (137–143) also identifies it with the underlying
coordinate product law. This justifies the source-array regrouping at the
distribution level. EuclideanSpace/PiLp/ofLp and ordinary dot-product
normalization were checked against actual source; no hidden dimensional scale
appears. Non-PSD/zero-variance default branches are inactive at the selected I
and real variance 1 inputs.

T59–70 establishes coordinate L2 using actual IsGaussian.memLp_dual at p=2
and EuclideanSpace.proj, then L2×L2→L1 using MemLp.integrable_mul. I read those
actual proofs: the dual lemma pushes to the real Gaussian marginal and its
finite moments; the product lemma uses the Holder triple to enter L1. No
independence is needed for this product-integrability argument. The inferred
Gaussian instance is constructed from the actual law; it is not a class
assumption on the source theorem. Finite dimensionality supplies the ordinary
complete/Borel/second-countable structures used by the library leaves.

T61–68 obtains coordinate means by moving a continuous coordinate projection
through the integrable vector mean, then uses integral_id_multivariateGaussian=0.
The actual general vector-integrability leaf is generated from the visible
@[to_fun integrable_fun_id] attribute on IsGaussian.integrable_id; no nonexistent
handwritten integrable_fun_id declaration is assumed. Its proof uses the
library's finite Gaussian moments. This may be stronger background than the
minimal elementary source argument, but it creates no stronger caller premise.

T71–77 calls covariance_eval_multivariateGaussian with **Matrix.PosSemidef.one
supplied inside the proof**, unfolds covariance and removes the already proved
zero means. Hence E[x_u x_v]=δ_uv. The covariance definition is genuinely the
integral of centered products. The actual multivariate covariance proof
(203–222) uses covariance of stdGaussian, affine-pushforward covariance, and
CFC.sqrt_mul_sqrt_self under the PSD hypothesis. I read this path and the
necessary square-root/matrix-action definitions and proofs. T does not locally
prove CFC.sqrt I=I or unfold that machinery; the canonical covariance theorem
discharges it. That is an honest dependency route, not a missing public premise.

T78–82 derives d>0 from hq and scale²d=1 using the genuine real square root.
T83–102 expands each ordinary/weighted Gram entry into a finite i-sum of
deterministic coefficients times x_(i,a.1)x_(i,b.1). These are same-row products;
there are no unproved cross-row terms or random/adaptive coefficients.
T109–121 makes every summand integrable by const_mul and both Gram entries
integrable by integrable_finsetSum. This precedes and independently supports
integral_finsetSum at T122 and T142. Integral_const_mul then applies to actual
integrable finite sums, not totalized nonintegrable defaults.

The ordinary mean becomes
δ_(a.1,b.1) scale² Σ_i t_(i,a.2)t_(i,b.2); P's Gram and scale²d=1 give
δ_(a.1,b.1)δ_(a.2,b.2)=δ_(a,b), with all pair-equality cases explicitly split
at T133–141. The weighted mean is the same scalar delta times P's zero weighted
Gram, hence zero at T142–151. Both L1 conclusions are actually returned.

The target is entrywise scalar Bochner integrability/means. In finite dimension
this is the source matrix expectation convention coordinatewise; the exposition
states that convention. There is no separate matrix-valued integral theorem in
T, nor a theorem about an arbitrary ambient probability space or adaptive
coefficient law. Those are not claimed by this bounded private application.

## 4. Actual use, mathematical necessity and mapping proposal

P actually calls G at P50. T actually calls P at T44–45. T projects only P.1
and P.2.1 (T49–58); the row bound P.2.2 is **not a mathematical input to the
two means**. It remains an independently proved selected source assertion and
a future concentration ingredient. I found no false AND-parent from that row
bound or from C.6. Importing a file was not used as evidence of necessity.

T is a substantive actual-law calculation, not a wrapper that restates supplied
certificates. It is private in a Tests module and has no further consumer in
that module. Thus it is a genuine private consumer of P, not evidence of a
completed production concentration/theorem integration. No repository-wide
consumer claim was made or searched.

The independently authored source-to-lean map was treated as a **proposal**.
I checked all 57 original-byte/character/line locator slices against actual
candidate/Mathlib source, and all 26 raw-source anchor slices, hashes and IDs
against my pinned raw input. Its 24 canonical rows are unique. I inspected
all 29 compact mathematical correspondences, and independently compared them
with the source/P/T reasoning above. The recorded canonical-alias substitution,
Gaussian covariance route and row-bound nonuse are accurate. C.6 Ex125 is
correctly context-only, not a formal prerequisite of these targets.

I did not open the map's raw-graph/typed-overlay lineage files, native constant
traversal log, compiler-metadata file, or any SG/TC/root verdict. Their linked
hashes and claimed generated-provider counts remain supplied metadata. In
particular, I independently inspected the handwritten source use sites, not
the claimed 24 generated certificate inventory or exact private kernel name.
No duplicate source result or new canonical mathematical node is justified by
those provider counts. This review accepts the mathematical correspondences,
not an unseen whole-graph closure certificate.

## 5. Exposition and six exact folded-code strings

The complete candidate lesson (SHA256
`b3985aea4653fe06c5de62c19272ffa2e45eca2445cc30ee0165d7ff4537dec5`) and
publication (SHA256
`d845e8bbca121add9e5444bc47ea663f541d15f007cbce4a21b3fd2d6da18a53`) were
read and compared with P/T and the pinned raw source. The concise public claim
is accompanied by all conditions/objects and a progressive six-step formula
proof. The steps explain mathematical operations, not merely tactics.

The zero-mode formula, product-to-sum normalization, weighted frequency range,
1+2q row bound, Gaussian coordinate L1/delta moment and final two mean formulas
are all correct. The private-law paragraph is explicitly marked as private
application context; it does not introduce a new public Gaussian hypothesis.
The publication binds the public auxiliary as a prerequisite and explicitly
limits its coverage. The entrywise Gaussian formulation is disclosed.

Every supplied step.lean string was independently checked as a unique literal
substring of the immutable target blob, with exact bytes and hashes recorded
in bindings_locators_blocks_verification.json:

| Folded step | Actual target span | Match |
|---|---|---|
| 1 cosine cancellation | P34–53 | Exact |
| 2 Gram normalization, pair/triple algebra and cases | P54–124 | Exact |
| 3 weighted modes and matrix assembly | P125–155 | Exact |
| 4 row square bound | P156–166 | Exact |
| 5 actual Gaussian moments/L1/normalization | T59–82 | Exact |
| 6 complete private Gaussian application | T1–153, all 7494 bytes | Exact whole-module equality |

Step 2 also prepares the triple-product identity for step 3, as its prose
explicitly explains. Step 6 intentionally contains the complete module, so
local definitions/imports and the private theorem's full context are available.
Static data requests progressive layout. I did not render a browser/site or
verify actual initially-closed UI state; that delivery check remains separate.

## 6. Complete bounded source disposition and final limits

| Raw source component | Candidate-local disposition |
|---|---|
| C.2 definitions t,γ,B,D and source standing range | Literal t/D/B and canonical actual Gaussian realization; source object semantics preserved |
| C.5 p4 local cancellation telescope | Cancellation proved through canonical G reuse; nonliteral route explicitly retained |
| C.5 p5 ordinary deterministic Gram | Covered by P, including constant/mixed/positive cases |
| C.5 p6 ordinary Gaussian mean | Covered privately by T entrywise, with actual L1 expansion |
| C.5 p7 weighted deterministic cancellation and Gaussian mean | Covered by P/T with every frequency bound and exact normalizations |
| C.5 p8 deterministic row-square bound | Covered by P; not claimed as a parent of T means |
| C.5 p3 range(B)=K_q | Excluded/open; no Chebyshev change-of-basis proof is claimed |
| C.6, full Lemma 4.4, main lower bounds/adapters | Excluded/open; no concentration/probability/absolute-C or uniform-Krylov inference is claimed |

The last exclusions are genuine remaining source boundaries, not failures of
these selected statements. Source C.6 uses stronger fourth-moment/truncation/
Bernstein inputs absent from P/T; the actual code and exposition do not infer
them from the two means. A full uniform bound also needs range(B)=K_q and the
τ≤1/2 combination. No Gaussian independence proof or expected-query/adaptive
factorization should be credited merely from the present scalar means.

Final semantic verdict for this bounded unit: **equivalent-after-elaboration**
(one-based source vectors versus zero-based matrices, canonical Gaussian law,
entrywise finite-dimensional expectations with source-implicit L1 made explicit).
No mathematical repair is required, and no canonical content was modified.
This judgment is independent of formalizer and decoder. It is bound to the
actual immutable files read here, with the above explicit evidence limits.
