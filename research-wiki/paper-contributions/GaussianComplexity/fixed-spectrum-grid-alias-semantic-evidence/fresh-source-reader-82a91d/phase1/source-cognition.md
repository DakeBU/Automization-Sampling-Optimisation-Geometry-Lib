# Source-only cognition freeze, phase 1

Actor: `source_reader_82a91d`. This document is my reconstruction from the pinned raw source and the separately logged governing instructions. I have received no candidate statement, implementation, decoder reconstruction, prior audit/verdict/repair, production mathematical lesson, or proposed source proof graph. It is not a source-fidelity or compilation verdict. Ambient topic/path cues, including an overly broad initial filename listing, are explicitly recorded in `raw-input-exposure-manifest.json`; I do not claim zero ambient cues.

## Pinned scope and meaning

Raw file: `.astis/huanjian-resume-20261103/2610.20492v1.html`, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

Read mathematical regions: the complete Section 4.1 (`S4.SS1`, including Eq. 11 and Remark 4.2), the exact Lemma 4.5 statement (`S4.Thmtheorem5`), and the complete Appendix C.3 (`A3.SS3`, including Facts C.7 and C.8 and all their proof paragraphs). Exact raw fragments, full text projections, a source byte-offset/hash manifest, and all 124 mathematical alttext snippets are frozen separately. No source region outside those three fragments has been semantically read.

The section constructs a deterministic cosine spectrum with a random orthogonal eigenbasis. The lemma computes two Gaussian quadratic means exactly on that finite grid, bounds their variances, and bounds the ratio of their means. Appendix C.3 supplies the inverse-spectrum cosine expansion, the grid alias calculation, the Gaussian variance calculation, and the logarithmic estimates for that ratio. The Section 4.1 algorithm/output discussion is motivation and a future consumer context; it is not an extra input to Lemma 4.5.

## Objects, domains, and quantifier order

1. The standing construction uses a finite integer dimension `d >= 2` and real condition parameter `kappa >= 2`. The source sums coordinates over `i = 1, ..., d`; its midpoint nodes are

   `theta_i = ((i - 1/2) pi) / d`,

   `lambda_i = (kappa + 1)/2 + ((kappa - 1)/2) cos(theta_i)`,

   `Lambda = diag(lambda_1, ..., lambda_d)`.

   These are Chebyshev midpoint nodes, not a grid including 0 or pi. The formula's index starts at 1. A zero-based finite encoding would need the corresponding `i + 1/2` convention; no candidate encoding has been seen.

2. For the hard family, `O ~ Haar(O(d))` is independent of the algorithm's private randomness, and `A = O Lambda O^T`. The potential is `f_A(x) = x^T A x / 2`, and the target is `pi_A = N(0, A^{-1})`. The deterministic spectrum may be given to the algorithm; the Gaussian normalizing constant is known, and the random eigenbasis is the unknown part.

3. Lemma 4.5 fixes `kappa >= 2` with this same grid and diagonal matrix. It takes `U ~ N(0, Lambda^{-1})`; the probability law is the centered diagonal-covariance Gaussian. Define

   `rho = rho_kappa = (sqrt(kappa) - 1)/(sqrt(kappa) + 1)`.

   Here `sqrt(kappa)` is positive and `0 < rho < 1`. The integer mode is an arbitrary integer `n` with `1 <= n < d`. It is not restricted to odd integers, even though the remark's later algorithm test uses `n = 2q + 1`.

4. For each such `n`, `D_n = diag(cos(n theta_i))`, `M = E ||U||^2`, and `mu_n = E[U^T D_n U]`. `M` depends on the grid and `kappa` but not on `n`; `mu_n` and `D_n` do depend on `n`. These are ordinary expectations with respect to the law of `U`, not expectations over the random rotation or algorithm randomness. The matrix `Lambda^{-1}` is the covariance of `U`, and `Lambda` is its precision.

5. Fact C.7 quantifies over every real `theta`, after the standing `kappa` and `rho` are fixed. Its series index `j >= 1` ranges over positive integers. Absolute and uniform convergence concern `theta in R` for the fixed `kappa`; there is no claim of uniformity as `kappa` tends to infinity.

6. The finite cosine-grid identity in C.8 quantifies over every integer `k`, including negative `k` and zero. In its exceptional case `k = 2 a d`, `a` ranges over all integers. In the later infinite-series alias decompositions, `a >= 1` instead ranges over positive integers. These two uses must remain distinct.

7. The final two-sided exponential conclusion has the additional condition `d - n >= sqrt(kappa)`. This condition is not needed for the exact means, the variance bounds, the exact normalized ratio, or the source proof's intermediate upper bound by `rho^n`. No relation between `d` and `kappa` other than this explicitly conditional separation is imposed on the earlier assertions.

## Exact conclusions and normalizations

For all the lemma's standing inputs and all integer `1 <= n < d`,

`M = (d / sqrt(kappa)) * (1 - rho^(2d))/(1 + rho^(2d))`,

`(-1)^n mu_n = (d / sqrt(kappa)) * (rho^n - rho^(2d-n))/(1 + rho^(2d))`.

Both quadratic variances are bounded as

`Var(||U||^2) <= 2 M <= 2 d / sqrt(kappa)`,

`Var(U^T D_n U) <= 2 M <= 2 d / sqrt(kappa)`.

When `d - n >= sqrt(kappa)`,

`(1 - exp(-4)) exp(-3 n / sqrt(kappa)) <= |mu_n|/M <= exp(-2 n / sqrt(kappa))`.

The exact finite-grid correction has denominator `1 + rho^(2d)` in both raw means. After division, the exact normalized ratio has denominator `1 - rho^(2d)`:

`|mu_n|/M = rho^n * (1 - rho^(2(d-n)))/(1 - rho^(2d))`.

The normalized statistic is the ratio of expectations. The lemma does not claim this equals the expectation of a random ratio, nor does it bound a realized ratio or give a concentration probability. The sign of `mu_n` is alternating: `(-1)^n mu_n > 0` for the stated mode range. The constants 2, 3, 4, and `1-exp(-4)` are literal constants in the source bounds, not unnamed asymptotic constants.

## Complete source calculation reconstructed in source order

### Section 4.1, hard-family context

`S4.SS1.p1.1` and Eq. 11 identify the construction as similar to reference `[22, Section 9.2]` but extending the spectral interval from `[1,2]` to `[1,kappa]`. The reference itself is outside the read scope; no bibliographic contents were inferred. The grid, spectrum, and diagonal matrix are the literal definitions above.

`S4.SS1.p1.2` defines Haar rotation, independence from private randomness, `A`, the quadratic potential, and the target Gaussian. `S4.SS1.p2.1` explains deterministic spectrum/known normalizer/unknown basis. These are part of the whole scoped source context, though the C.3 finite-grid calculation only uses the diagonal spectral definitions and the Gaussian `U`.

Remark 4.2 (`S4.Thmtheorem2`) states that the `kappa=2` spectrum recovers the original construction and that, with the same `O`,

`A = (kappa - 1) A_2 - (kappa - 2) I_d`.

Thus one matrix-vector response for either matrix determines the response for the other. The remark describes the later comparison between `sum_i cos(n theta_i) <x, O e_i>^2` and `||x||^2`, with `n=2q+1`. It attributes an output ratio of magnitude at most `d^(-Omega(1))` to Lemma 4.4 and a target ratio of means of magnitude `exp(-Theta(n/sqrt(kappa)))` to Lemma 4.5. It says this supports modes of order `sqrt(kappa) log d` and the factor `sqrt(kappa)` in Theorem 4.1. Lemma 4.4 and Theorem 4.1 have not been read or accepted here. The motivation neither proves the query result nor restricts the general `n` in Lemma 4.5.

### C.3 opening and Fact C.7

`A3.SS3.p1.1` repeats the exact grid and eigenvalue definitions and announces the order: cosine-expand the inverse spectrum, sum over the grid, then bound variances and normalized cosine bias.

Fact C.7 (`A3.Thmtheorem7`, display `A3.Ex133`) asserts for every real `theta`:

`2 / (kappa+1+(kappa-1)cos(theta))`

`= (1/sqrt(kappa)) * (1 + 2 sum_(j>=1) (-rho)^j cos(j theta))`,

with absolute and uniform convergence in `theta`. The left side is the literal reciprocal of the spectral formula at angle `theta`; the normalization is `1/sqrt(kappa)` and the nonconstant modes carry a factor 2 and alternating coefficients `(-rho)^j`.

`A3.SS3.p2.1`/`A3.EGx14` use `0 < rho < 1` and two complex geometric series to identify the expression inside parentheses as

`1 - rho exp(i theta)/(1 + rho exp(i theta)) - rho exp(-i theta)/(1 + rho exp(-i theta))`

`= (1-rho^2)/(1 + 2 rho cos(theta) + rho^2)`.

`A3.SS3.p2.2`/`A3.Ex136` give two algebraic normalization identities:

`(1-rho)/(1+rho) = 1/sqrt(kappa)`,

`(1 + 2 rho cos(theta) + rho^2)/(1-rho)^2 = (kappa+1+(kappa-1)cos(theta))/2`.

`A3.SS3.p2.3` combines them into the stated inverse-spectrum expansion. `A3.Ex137` bounds the absolute cosine series by

`sum_(j>=1) |(-rho)^j cos(j theta)| <= sum_(j>=1) rho^j = rho/(1-rho)`.

`A3.SS3.p2.4` uses this theta-independent geometric majorant for absolute and uniform convergence. No convergence, integrability, or existence estimate becomes an extra premise of the fact: these are proved ingredients of the source route. Complex denominators and real spectral denominators are nonzero under the standing `rho`/`kappa` range, although separate named nonvanishing lemmas are not written in the source.

### Fact C.8: finite-grid aliasing and exact means

Fact C.8 (`A3.Thmtheorem8`, `A3.Ex138`) states the two exact means above for `1 <= n < d`.

`A3.SS3.p3.1`/`A3.Ex139` give the finite-grid identity:

`sum_(i=1..d) cos(k theta_i) = d (-1)^a` if `k=2ad`, `a in Z`, and zero otherwise.

`A3.SS3.p3.2` proves the nonalias case by the finite cosine sum `sin(k pi)/(2 sin(k pi/(2d))) = 0`; the denominator is used only when `k` is not a multiple of `2d`. In the alias case each term is `cos(2ai pi-a pi)=(-1)^a`. This records the exceptional `k=0` sum `d`, the alternating signs of aliases, and the all-integer convention. It is not a continuum orthogonality rule and not an assertion that every nonzero frequency sums to zero.

`A3.SS3.p4.1`/`A3.Ex140` use the diagonal Gaussian coordinate variances `E U_i^2 = 1/lambda_i` to identify

`M = sum_i 1/lambda_i`,

`mu_n = sum_i cos(n theta_i)/lambda_i`.

`A3.SS3.p4.2` applies C.7 and its absolute convergence to interchange the series with the finite grid sum. C.7 supplies this prerequisite; it is not an independent assumption on the target.

For `M`, `A3.SS3.p5.1`/`A3.EGx15` retain only positive indices `j=2ad`, `a>=1`, giving

`M = (d/sqrt(kappa)) * (1 + 2 sum_(a>=1) (-1)^a rho^(2ad))`

`= (d/sqrt(kappa)) * (1 - 2 rho^(2d)/(1+rho^(2d)))`

`= (d/sqrt(kappa)) * (1-rho^(2d))/(1+rho^(2d))`.

For `mu_n`, `A3.SS3.p6.1` first notes `sum_i cos(n theta_i)=0`, using `1 <= n < d`. The factor 2 in C.7 cancels the product-to-sum factor `1/2`. Display `A3.Ex144` becomes

`mu_n = (1/sqrt(kappa)) sum_(j>=1) (-rho)^j [sum_i cos((j-n)theta_i) + sum_i cos((j+n)theta_i)]`.

`A3.SS3.p6.2` classifies every surviving positive `j`:

- The `j-n` sum survives at `j=n` with value `d`, or at `j=2ad+n`, `a>=1`, with value `d(-1)^a`.
- The `j+n` sum survives at `j=2ad-n`, `a>=1`, with value `d(-1)^a`.
- The three classes are disjoint because `1 <= n < d`; the minus-branch indices are positive.
- Since `2ad` is even, `(-rho)^(2ad +/- n)=(-1)^n rho^(2ad +/- n)`.

`A3.EGx16` sums those classes as

`(-1)^n mu_n = (d/sqrt(kappa)) [rho^n + sum_(a>=1) (-1)^a (rho^(2ad+n)+rho^(2ad-n))]`

`= (d/sqrt(kappa)) [rho^n - (rho^(2d+n)+rho^(2d-n))/(1+rho^(2d))]`

`= (d/sqrt(kappa)) (rho^n-rho^(2d-n))/(1+rho^(2d))`.

This is finite-dimensional alias accounting plus geometric sums. Removing the alias terms would change the exact source result even if it approached the correct limiting expression in another regime.

### Completion of Lemma 4.5: means and variances

`A3.SS3.p7.1` imports C.8 for both asserted means.

`A3.SS3.p8.1` uses diagonality of the covariance to obtain independent centered Gaussian coordinates. For each coordinate,

`E U_i^4 = 3/lambda_i^2`, `Var(U_i^2)=2/lambda_i^2`.

It also derives `lambda_i >= (kappa+1)/2 - (kappa-1)/2 = 1`. Display `A3.EGx17` gives the variance identities and bounds:

`Var(||U||^2) = 2 sum_i 1/lambda_i^2 <= 2 sum_i 1/lambda_i = 2M`,

`Var(U^T D_n U) = 2 sum_i cos^2(n theta_i)/lambda_i^2 <= 2M`.

The second bound also uses `cos^2 <= 1`. These sums use independence to remove cross-covariances; marginal moments alone would not justify the variance identities. Gaussian fourth moments imply the relevant finite integrability. `A3.SS3.p8.2` applies C.8's exact `M` to obtain `M <= d/sqrt(kappa)`. The moment and independence facts are source proof ingredients to be discharged from the specified law, not public theorem assumptions to add for convenience.

### Completion of Lemma 4.5: normalized bias and exponential constants

`A3.SS3.p9.1` uses `n<d` and `0<rho<1` to deduce `rho^n > rho^(2d-n)` and thus `(-1)^n mu_n>0`. Dividing C.8's two formulas gives `A3.Ex150`, the exact normalized ratio displayed earlier. `M>0` follows from the finite-grid formula; the normalization is meaningful on the stated domain.

`A3.SS3.p9.2` records `0<rho^(2d)<rho^(2(d-n))<1`. Display `A3.Ex151` is

`1-rho^(2(d-n)) <= (1-rho^(2(d-n)))/(1-rho^(2d)) <= 1`.

`A3.SS3.p10.1`/`A3.EGx18` introduce the logarithm identity

`log(1/rho) = log((sqrt(kappa)+1)/(sqrt(kappa)-1))`

`= 2 integral_(0..1/sqrt(kappa)) dt/(1-t^2)`

`= 2/sqrt(kappa) + 2 integral_(0..1/sqrt(kappa)) t^2/(1-t^2) dt`.

`A3.SS3.p10.2` obtains the lower bound `log(1/rho) >= 2/sqrt(kappa)` from nonnegativity of the second integrand. It uses `1-t^2 >= 1-kappa^(-1)` throughout the integration interval to bound that integral. `A3.EGx19` gives

`log(1/rho) <= (2/sqrt(kappa)) [1 + 1/(3(kappa-1))] <= 8/(3sqrt(kappa)) < 3/sqrt(kappa)`.

`A3.SS3.p10.3` identifies the use of `kappa>=2` and exponentiates to `A3.Ex157`:

`exp(-3n/sqrt(kappa)) <= rho^n <= exp(-2n/sqrt(kappa))`.

`A3.SS3.p11.1` introduces the extra separation condition `d-n >= sqrt(kappa)`. The lower bound on `log(1/rho)` gives `A3.Ex158`:

`rho^(2(d-n)) = exp(-2(d-n)log(1/rho)) <= exp(-4(d-n)/sqrt(kappa)) <= exp(-4)`.

`A3.SS3.p11.2` combines the ratio fraction bounds with this alias-tail bound:

`(1-exp(-4))rho^n <= |mu_n|/M <= rho^n`.

Combining with the power bounds gives `A3.Ex159`, exactly the lemma's final two-sided exponential estimate. `A3.SS3.p11.3` closes the source proof. These are sequential dependencies, not alternative sufficient routes and not an AND of independent hypotheses.

## Dependency and coverage inventory

The following inventory is source-first. It is not a proposed production sourcegraph and has not been compared to any existing graph.

| Scoped region | Disposition and direct mathematical role |
| --- | --- |
| `S4.SS1.p1.1`, `S4.E11` | Included: cited construction context, dimension/parameter inputs, grid and spectral definitions. |
| `S4.SS1.p1.2` | Included: hard-family rotation, independence, precision/potential/target definitions. Context for, but no extra premise of, the diagonal target lemma. |
| `S4.SS1.p2.1` | Included: information model and known normalizer. Not used to prove C.7/C.8. |
| `S4.Thmtheorem2` and its paragraph | Included: affine `kappa=2` comparison and test motivation. Its external `[22]`, Lemma 4.4, and Theorem 4.1 are boundary references, not accepted results of this review. |
| `S4.Thmtheorem5`, `S4.EGx1`, `S4.Ex17` | Included: full source statement, inputs, exact means, both variance bounds, and conditional exponential estimate. |
| `A3.SS3.p1.1` | Included: repeated definitions and source proof order. |
| `A3.Thmtheorem7`, `A3.Ex133` | Included: inverse-spectrum cosine series and absolute/uniform convergence. |
| `A3.SS3.p2.1`, `A3.EGx14` | Included: geometric-series evaluation through complex exponentials. |
| `A3.SS3.p2.2`, `A3.Ex136` | Included: both normalization identities. |
| `A3.SS3.p2.3`, `A3.Ex137`, `A3.SS3.p2.4` | Included: combine identities and give a uniform geometric majorant. |
| `A3.Thmtheorem8`, `A3.Ex138` | Included: exact finite-grid moment claims. |
| `A3.SS3.p3.1`, `A3.Ex139`, `A3.SS3.p3.2` | Included: all-integer grid alias identity and its two cases. |
| `A3.SS3.p4.1`, `A3.Ex140` | Included: identify Gaussian means as reciprocal-spectrum weighted sums. |
| `A3.SS3.p4.2` | Included: interchange series and finite grid sum using C.7 absolute convergence. |
| `A3.SS3.p5.1`, `A3.EGx15` | Included: surviving `2d` aliases, geometric sum, exact `M`. |
| `A3.SS3.p6.1`, `A3.Ex144` | Included: vanishing base mode and product-to-sum formula for `mu_n`. |
| `A3.SS3.p6.2`, `A3.EGx16` | Included: exhaustive/disjoint alias classes, parity, both geometric sums, exact signed `mu_n`. |
| `A3.SS3.p6.3` | Proof terminator only; excluded from mathematical-node content. |
| `A3.SS3.p7.1` | Included: C.8 directly supplies the means in Lemma 4.5. |
| `A3.SS3.p8.1`, `A3.EGx17` | Included: diagonal Gaussian independence, fourth moments, eigenvalue floor, variance identities and inequalities. |
| `A3.SS3.p8.2` | Included: exact `M` yields its upper bound. |
| `A3.SS3.p9.1`, `A3.Ex150` | Included: strict signed mean positivity and exact normalized ratio. |
| `A3.SS3.p9.2`, `A3.Ex151` | Included: strict order of alias powers and ratio-fraction sandwich. |
| `A3.SS3.p10.1`, `A3.EGx18` | Included: logarithm integral identity and split. |
| `A3.SS3.p10.2`, `A3.EGx19` | Included: logarithm lower/upper bounds, explicit integration and constants. |
| `A3.SS3.p10.3`, `A3.Ex157` | Included: parameter restriction use and exponential power bounds. |
| `A3.SS3.p11.1`, `A3.Ex158` | Included: separation condition gives alias-tail bound `exp(-4)`. |
| `A3.SS3.p11.2`, `A3.Ex159` | Included: combine ratio and power bounds into the lemma conclusion. |
| `A3.SS3.p11.3` | Proof terminator only; excluded from mathematical-node content. |
| Headings/proof labels `A3.SS3.2`, `.3`, `.4` | Excluded as standalone mathematical claims; retained as ownership/order markers. |

The source invokes unnamed standard facts: complex geometric-series summation, cosine/exponential and product-to-sum identities, the finite trigonometric sum, finite-sum interchange with an absolutely convergent series, diagonal Gaussian independence and second/fourth moments, variance additivity for independent squared coordinates, and elementary integration/logarithm/exponential identities and monotonicity. They are mathematical dependencies of the source derivation. The bounded source does not provide a separate citation for each. Their lack of a local formal implementation cannot be classified in this phase because implementation/API search is forbidden. No source gap is being asserted from that absence alone.

## Explicit boundaries and later comparison questions

- Phase 1 establishes my frozen source reading, not any Lean proposition's source fidelity, kernel truth, API availability, reader correctness, publication acceptance, or V transition.
- Lemma 4.5 includes all three groups: exact means, both variance bounds, and the conditional normalized-bias estimate. A formal result limited to an earlier group could be a faithful partial ingredient only with that narrower boundary stated; it would not be the whole lemma.
- Fact C.7 includes both the pointwise identity and absolute/uniform convergence; a candidate identity alone would have a narrower public scope than the complete fact. A local implementation may prove prerequisites separately, but their conclusions should not become unexplained public source premises.
- Fact C.8's finite grid is exact. Its `1+rho^(2d)` denominator, reflected exponent `2d-n`, parity sign, and integer alias classes are meaning-carrying, as are the `1-rho^(2d)` denominator after normalization and the `d-n` separation used only for the final lower bound.
- The hard family mentions Haar rotation and algorithm randomness, but no query lower bound, target/output test theorem, total variation result, concentration event, or complexity scaling is proved by this scoped review. The Section 4.1 references to those future consumers remain open here.
- No source repair is proposed. No candidate binder, fallback definition, excess hypothesis, or current implementation is known yet. Later comparison must distinguish source premises, standing construction inputs, type information, and proof ingredients.
- If later packets contain prior judgments, repair decisions, or sourcegraph conclusions, that exposure must be recorded separately rather than retroactively included in this source-only freeze.
