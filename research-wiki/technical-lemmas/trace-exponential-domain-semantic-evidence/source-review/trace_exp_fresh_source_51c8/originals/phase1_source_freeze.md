# Phase 1 raw-source-first freeze

Status: SOURCE-ONLY INTERPRETATION FROZEN; no mathematical acceptance, no Lean verdict, no source-fidelity verdict, no repair acceptance.
Reviewer role: fresh anti-anchored postproof source / whole-module / reader reviewer, distinct from formalizer, decoder, preproof SG/TC reviewer and native verifier. Phase 1 contains no candidate implementation or candidate publication input.

## Inputs and isolation

The only mathematical inputs read were the two assigned pinned raw sources:

- Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, author preprint, PDF SHA-256 `f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86`; sections 2.1–2.4 and 3.1. Actual PDF/printed pages 7, 8 and 9 were rendered and visually inspected, including the expectation caveat.
- *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, pinned HTML SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`; necessary section 4.1/4.2 objects and Lemma 4.4, Appendix C.2 literal experiment through the C.6 proof. Raw HTML line ranges 1050–1240 and 3314–3791 were locally converted to readable text solely as private review references.

Protocols read: repository AGENTS.md, proof-digestion-protocol, theorem-publication-protocol, evidence-routed-memory-protocol, astis-semantic-roundtrip skill, and the PDF skill. The review did not read any current or historical implementation Lean, candidate Statement Seal, candidate metadata, old SG/TC packet, earlier verdict, repair proposal, canonical registry, global index, cache, ledger, Git/API/network surface or live site. No proof search, compiler/native verification, Discovery validation or proofV action was performed.

The raw full sources, rendered PDF reference pages and local extraction are references only. The explicit public leaf manifest is the only export allowlist; it does not authorize recursively exporting this directory or either original source.

## Independent source interpretation

### Tropp's carrier and functions

Tropp 2.1 uses finite square complex matrices, with self-adjoint matrices and the Euclidean induced operator (spectral) norm. Restricting that background to real Hermitian matrices means finite real symmetric matrices, and must be described as a real restriction of the source convention. It does not mean an entrywise norm. Matrix size is often determined by context.

Section 2.3 defines real scalar functions on self-adjoint matrices through spectral functional calculus, and gives the scalar-to-semidefinite transfer rule (2.2). Section 2.4 identifies the ordinary matrix exponential both by spectral calculus and its convergent matrix power series. It states that the exponential of a self-adjoint matrix is positive definite. The scalar trace exponential is the ordinary trace of that matrix exponential. The trace exponential is monotone in semidefinite order (2.5); this is distinct from operator monotonicity of the exponential itself. No entrywise exponential, normalized trace, determinant, auxiliary scalar proxy, or custom off-source fallback belongs to this meaning.

The requested finite-dimensional scalar positivity and dimension/operator-norm envelope are background consequences to be supplied, not a separately printed theorem at these anchors. Expected semantic shape: for a finite real Hermitian m-by-m matrix A and real theta, the scalar `tr(exp(theta A))` is nonnegative, and is positive when m>0, with a dimension envelope at scale `m exp(|theta| ||A||op)`. A nonempty hypothesis is necessary for strict trace positivity; for m=0 the ordinary trace is 0 and the weak envelope has both sides 0. This is a statement requirement, not a Phase 1 proof or acceptance of a future implementation. A stronger two-sided envelope may be useful but is not required merely by the stated bounded task.

Section 2.2 is an explicit sufficient-regularity standing convention for expectation/limit manipulations and often suppresses “almost surely.” It is not evidence that every random self-adjoint matrix has a finite MGF at every parameter. Section 3.1 defines the matrix MGF/cgf for real theta while expressly allowing nonexistence at some theta even when all moments exist. Therefore all-real scalar expectation claims for the actual bounded experiment require their own finite domination/measurability bridge. They cannot be inferred from the word Gaussian or from a totalized formal integral alone.

### The Gaussian full-law experiment

Parameters are integers q>=0 and d with `2q+1<d`, in particular d>=2. Set r=q+1>=1 and n=2q+1. Thus `2r<=d`. The q=0 endpoint is part of the source: r=1, n=1, and t_i has only its constant coordinate. No q>=1 or r>=2 restriction is justified. The deterministic cosine nodes are theta_i=(i-1/2)pi/d for i=1,...,d.

The independent starting vectors g_1,...,g_r have law N(0,I_d). Equivalently the rows gamma_i=((g_1)_i,...,(g_r)_i) are independent N(0,I_r). The full experiment is this original unconditioned joint Gaussian probability law. One may present an explicit product-law realization or a faithful pushforward realization, but the measure in every mean and scalar trace-exponential expectation must be that original law. The random orthogonal eigenbasis O, target N(0,A^{-1}) and algorithm private randomness are not the integration laws here.

For j=0,...,q, t_i has coordinate 1 at j=0 and sqrt(2) cos(j theta_i) otherwise. B has i-th row `d^(-1/2) (gamma_i tensor t_i)^T`. Its column/matrix coordinates use the gamma-first product order `(a,j)`, with a=1,...,r and j=0,...,q. Therefore the square matrices below have dimension r*r=r^2. A swap to `t_i tensor gamma_i` must not be silently treated as literal source identity; an explicit permutation/conjugacy bridge would be needed.

Set `R_i=||gamma_i||^2` and `L=2r+3 log(1000d)`. Here R_i is an own-row squared radius, L a scalar cutoff, and `R_*` below an operator-norm radius. These are not interchangeable. The source cutoff is inclusive: `R_i<=L`. `Y_i` is zero outside that own-row event and is defined on every outcome of the full original law:

`Y_i = d^(-1) (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i<=L}`.

Entrywise, at `(a,j),(b,k)`, the formula is `d^(-1) gamma_i[a] gamma_i[b] t_i[j] t_i[k] 1_{R_i<=L}`. The row's full r-coordinate radius controls its own truncation. Neither conditioning on a row event nor cutting off by another row or the all-row event gives this literal Y_i.

The matrix mean is the true full-law expectation `mu_i=E[Y_i]`, not an arbitrary deterministic matrix supplied with a bound. Source radial symmetry states `E[gamma_i gamma_i^T 1_{R_i<=L}]=a I_r`, where `a=(1/r) E[R_i 1_{R_i<=L}]` is the same for every i and 0<=a<=1. Consequently `mu_i=(a/d)(I_r tensor t_i t_i^T)`. The a here includes the cutoff bias; replacing it by 1 changes the source centered summands.

The centered summand is `Z_i=Y_i-mu_i`. The two actual centered sums are

- ordinary: `S=sum_{i=1}^d Z_i`;
- cosine weighted: `S_cos=sum_{i=1}^d cos(n theta_i) Z_i`.

The deterministic weights may be negative and satisfy absolute value at most 1. Both sums are real symmetric. The requested global sign choices are `S`, `-S`, `S_cos`, `-S_cos`: a single sign multiplies the entire sum. This must not become arbitrary independent signs per row, an entrywise sign, or a change of Gaussian law. All theta in R remains the scalar parameter domain for each of the four families; a theta>0 domain belongs only to subsequent Laplace optimization and does not replace this domain.

Source Ex110 says `sum_i mu_i=a I_(r^2)` and `sum_i cos(n theta_i) mu_i=0`. These are useful contextual identities; they do not turn Y_i into untruncated Gram summands. Source Ex111–112 give `||Y_i||op<=2rL/d`, `||mu_i||op<=2r/d`, and `||Z_i||op<=R_*:=2r(L+1)/d`; the same individual radius applies after cosine weighting. The corresponding source-motivated whole-sum radius is `d R_*=2r(L+1)`, valid for both global signs and both weighted/unweighted choices if the finite-sum norm bridge is supplied. It is a norm-domination envelope, not the Bernstein variance parameter.

The scalar expectations in the bounded review are `E[tr(exp(theta (sigma S)))]` and `E[tr(exp(theta (sigma S_cos)))]` for every real theta and sigma in {+1,-1}. They are ordinary real scalar integrals of the ordinary matrix exponential trace. Their finiteness/integrability is to be obtained from actual measurability and a finite deterministic envelope. Strict positivity of the scalar integrand/expectation uses r^2>0 and the full law being a probability measure. A weaker nonnegativity conclusion should be distinguished if it is all a future declaration states. The all-real claim is justified only for these truncated centered sums in this assignment; it must not be silently generalized to the untruncated B^T B or B^T D_n B.

### Measure roles and exclusions

The all-row truncation event `T={R_i<=L for every i}` has source probability at least 0.999. It is used later to identify original and truncated sums. It is not the ambient law, a conditioning denominator, an extra public assumption, or the reason a deterministic pointwise bound holds for the already-truncated Y_i.

The source exact experiment proves a tail-bias bound `(1-a)<=(L+3)/(1000rd)`. The variance parameter `v_*=2r(r+2)/d`, the two-sided Bernstein prefactor `2r^2`, tail threshold t>0, and subsequent `z=log(1000r^2)`, Delta and union bounds belong to the later concentration route. They remain context, not conclusions of a trace-exponential-domain leaf. The factor r^2 in the deterministic trace envelope is matrix dimension; the factor 2r^2 in Ex121 also reflects a two-sided tail operation and must not be substituted into the scalar trace definition.

Lemma 4.4 has an absolute C>0, tau_(d,q), a tau<=1/2 guard, and probability 0.99. Fact C.6 has probability 0.995. No result in this assignment establishes either result, matrix Bernstein, C.6, a matrix-valued MGF inequality, Lieb/subadditivity, or the main lower bound. Kappa>=2 explains the Krylov cosine change of basis, but the present deterministic t_i experiment and scalar domain bridge do not depend on kappa. Adding tau<=1/2, a concentration event, a variance estimate, or an integrability/MGF-finiteness premise merely to prove the desired scalar domain would shift a proof ingredient into an excess source binder.

## Omitted bridges to keep visible

The following requirements are intentionally independent of implementation topology. They identify what the supplied bounded theorem must account for; Phase 1 does not claim them proved.

1. Ordinary real matrix exponential must agree with the spectral/power-series object at all finite real Hermitian inputs; ordinary trace must retain the dimension factor and no normalization.
2. Finite-dimensional spectral/trace positivity and the Euclidean operator-norm envelope, including theta<0, theta=0, nonempty strict positivity and the empty finite carrier convention.
3. Actual rowwise Gaussian experiment, own-row closed cutoff, true full-law matrix mean, symmetric centered summands, gamma-first indexing and the r^2 dimension.
4. Measurability of the actual Y_i and centered finite sums, and of their scalar trace-exponential compositions; finite-dimensional exponential continuity or an equivalent justified route. Tropp's standing regularity is not a substitute for exposing the actual route.
5. Pointwise or properly stated almost-sure finite-sum radius for the two sums and both global signs. If a future implementation chooses an a.e. route, the full-law quantifiers and exceptional-set scope must be explicit.
6. Integrability/finiteness of each scalar trace-exponential under the full probability law for every real parameter via the deterministic finite envelope. A raw formal integral value is insufficient evidence of meaningful expectation.
7. Source-to-implementation bridges must be discharged dependencies rather than new premises asserting precisely the desired norm, positivity, exponential integrability, or an abstract proxy equivalent to the conclusion.

## Seven semantic slots frozen for later comparison

| Slot | Source-only requirement |
|---|---|
| Objects | Finite real symmetric matrix; ordinary matrix exponential and trace; actual full-law Gaussian gamma rows, deterministic t_i, inclusive rowwise Y_i, true mu_i, Z_i, S and S_cos; gamma-first r^2 index. |
| Domains | q natural including 0; d integer with 2q+1<d; r=q+1; i=1,...,d; gamma coordinate a=1,...,r and cosine coordinate j=0,...,q; every theta in R; global sigma=+1 or -1. Generic finite carrier strict positivity needs nonempty, weak positivity/envelope may include empty. |
| Quantifiers | Actual experiment chosen with its law before true means/sums; all outcomes or explicit a.e. scope for matrix bounds; for each real theta and each whole-sum sign, the actual scalar integrand is measurable/integrable/finite with its stated positivity. No existential cherry-picked center or law. |
| Assumptions | Source d,q range and Gaussian law; finite Hermitian typing; source regularity convention made concrete internally. No q>=1, conditioning on T, arbitrary bounded center, tau guard, supplied MGF finiteness or supplied desired norm conclusion. |
| Conclusion | Scalar trace positivity/nonnegativity and dimension/operator-norm domination; well-defined finite scalar E tr exp for the two actual truncated centered sums and their global negatives at all real theta, according to the exact future declaration. No automatic matrix-valued MGF or tail theorem. |
| Scopes/senses | Ordinary Euclidean operator norm, matrix multiplication exponential, ordinary trace, full unconditional probability integral; own-row inclusive cutoff; one global sign; matrix dimension r^2; original vs truncated sums distinguished. |
| Constant dependencies | Generic dimension m and |theta| ||A||op; actual r=q+1, L=2r+3 log(1000d), R_*=2r(L+1)/d and sum radius dR_*=2r(L+1). No hidden dependence on kappa, C/tau, future t or variance v_*. |

## Phase 2 handoff boundary

This freeze precedes independent decoder completion. Next input must be Root-provided fresh anti-anchored review packets after that completion, together with exact current whole-module text (imports/scopes/private helpers included), authored lesson(s), publication context and binding hashes, plus any separately authorized exact repair proposal packet. This reviewer will not search for candidates or old verdicts. Original findings and any repair overlays must be separate immutable artifacts. No final fidelity or reader acceptance is issued by this document.
