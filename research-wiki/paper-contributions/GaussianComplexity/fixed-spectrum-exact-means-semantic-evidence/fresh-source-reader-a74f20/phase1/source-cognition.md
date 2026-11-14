# Phase 1: independent raw-source cognition

Reviewer: `/root/source_reader_a74f20`. This is a source-only inventory, not a verdict on any candidate. No candidate statement, Lean module, proof, reconstruction, previous graph/audit/frontier/ledger, or other agent's mathematical work has been supplied or sought in this phase. The task itself names the source anchors and asks special attention to C.7/C.8, the two means, variance, normalized bias, and aligned display tags; those are exposure cues, so this is not a claim of zero cueing.

## Inputs and scope

Pinned original: `.astis/huanjian-resume-20261103/2610.20492v1.html`, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. Read in full at the semantic level: `S4.SS1` (Section 4.1, including Eq. 11 and Remark 4.2), `S4.Thmtheorem5` (Lemma 4.5), and `A3.SS3` (all of Appendix C.3: C.7 and proof, C.8 and proof, and the proof of Lemma 4.5). Also read only the raw bibliography entry `bib.bib3` to identify citation [22]. The extraction program reads/parses the full source file bytes; only the selected nodes are emitted for cognition. No other raw-source sections were emitted. The bibliography entry incidentally contains other section backlink labels.

Protocol exposure is separately enumerated in `read-exposure.json`. Reading the repository AGENTS file incidentally exposed broad project priority, gate, scheduling, conceptual-mirror, and handoff prose. It did not supply this lemma's candidate statement or formal proof. Protocol search exposed bounded matching lines, not the searched files in full. The source-only synthesis below is written before any later-phase material.

## Literal family, objects, and quantifiers

Section 4.1 fixes an integer dimension `d >= 2` and real `kappa >= 2`. For coordinate indices `i = 1,...,d`, it defines

`theta_i = (i - 1/2) pi / d`,

`lambda_i = (kappa+1)/2 + ((kappa-1)/2) cos(theta_i)`,

`Lambda = diag(lambda_1,...,lambda_d)`.

These are the half-step cosine/Chebyshev grid, the particular affine cosine eigenvalues, and their diagonal matrix. They are deterministic functions of `d,kappa`; neither arbitrary eigenvalues in an interval nor an arbitrary positive diagonal matrix is the literal family. The spectrum lies in `[1,kappa]` (the displayed grid actually avoids the two endpoints). The proof later needs the weaker bound `lambda_i >= 1`.

The hard-family construction draws `O ~ Haar(O(d))`, independently of the algorithm's private randomness, and sets `A = O Lambda O^T`, `f_A(x) = x^T A x / 2`, and `pi_A = N(0,A^{-1})`. Here `x` is a real `d`-vector, `O(d)` is the real orthogonal group, and `e_i` in the remark is the standard coordinate vector. The spectrum and Gaussian normalizing constant may be supplied to the algorithm; the unknown part is the random eigenbasis. Haar rotation and algorithm randomness are context for the hard family, not extra premises of the eigen-coordinate moment calculation in Lemma 4.5.

Remark 4.2: at `kappa=2` this recovers [22]'s construction. Using the same `O`, `A = (kappa-1) A_2 - (kappa-2) I_d`; one matrix-vector response for either determines the other. It describes a test comparing `sum_i cos(n theta_i) <x,O e_i>^2` with `||x||^2`, with `n=2q+1` for a `q`-query algorithm. It reports the output ratio as at most `d^{-Omega(1)}` in absolute value (Lemma 4.4), while the absolute ratio of target means is `exp(-Theta(n/sqrt(kappa)))` (Lemma 4.5), allowing order `sqrt(kappa) log d` rather than `log d`. These asymptotic statements are contextual, not the exact conclusion of Lemma 4.5; the lemma's `n` need not be odd and has no query-count premise.

Lemma 4.5 takes `U ~ N(0,Lambda^{-1})`, a centered Gaussian real `d`-vector, and defines

`rho = rho_kappa = (sqrt(kappa)-1)/(sqrt(kappa)+1)`.

For every integer `n` with `1 <= n < d`, let `D_n = diag(cos(n theta_i))`, `M = E ||U||^2`, and `mu_n = E[U^T D_n U]`. The norm is Euclidean; both quadratic forms are real random variables. In these coordinates `||U||^2 = sum_i U_i^2` and `U^T D_n U = sum_i cos(n theta_i) U_i^2`. There is no free test vector in these means. These are expectations of the actual specified Gaussian forms, not names for arbitrary real numbers satisfying rational identities. The source does not specify a probability-space presentation; the Gaussian law determines these moments. No Haar expectation is taken here.

The inherited `d,kappa` precede the grid; `U` has the stated law, and then the universal valid integer `n` determines `D_n,mu_n`. The radius ratio satisfies `0 < rho < 1` because `kappa >= 2`. In particular all denominators used below are positive and `M > 0`. No gap condition `d-n >= sqrt(kappa)` is imposed on the two means or either variance claim.

## Exact conclusions and their scopes

The two actual means, asserted by Lemma 4.5 and again by C.8, are

`M = (d/sqrt(kappa)) (1-rho^(2d))/(1+rho^(2d))`,

`(-1)^n mu_n = (d/sqrt(kappa)) (rho^n-rho^(2d-n))/(1+rho^(2d))`.

Both hold under the base family/Gaussian/valid-`n` conditions. The second formula includes its alternating sign and the finite-grid reflected term `rho^(2d-n)`; it is not merely a proportionality to `rho^n`. The first mean is independent of `n`, though C.8 presents the pair under the valid-`n` heading.

The two separate variance conclusions under the same base conditions are

`Var(||U||^2) <= 2M <= 2d/sqrt(kappa)`,

`Var(U^T D_n U) <= 2M <= 2d/sqrt(kappa)`.

They concern variance, not standard deviation or a probability deviation bound. The common `M` is the first actual mean above; it is not `|mu_n|`. The source does not assert equality of these two variances.

Only the final stated clause adds `d-n >= sqrt(kappa)`. Under that additional condition,

`(1-exp(-4)) exp(-3n/sqrt(kappa)) <= |mu_n|/M <= exp(-2n/sqrt(kappa))`.

The quantity is a ratio of means, with an absolute value on the signed mean in the numerator. It is not `E[|U^T D_n U|/||U||^2]`, not a mean of a samplewise ratio, and not a ratio of variances. The statement places both sides of this displayed sandwich under the gap condition. Its proof obtains the upper side already under the base conditions; that stronger derived upper side must be distinguished from the exact conditional scope of the displayed lemma clause.

## C.7: universal-angle expansion and full proof route

C.7 (`A3.Thmtheorem7`) inherits `kappa >= 2` and the definition of `rho`. It quantifies over every real angle `theta`, not merely the finite grid, and states

`2/(kappa+1+(kappa-1)cos(theta)) = (1/sqrt(kappa)) (1 + 2 sum_{j>=1} (-rho)^j cos(j theta))`.

The series converges absolutely and uniformly in `theta` for the fixed `kappa`. No uniformity as `kappa` varies is claimed; `rho/(1-rho)` depends on `kappa`. C.7 is an inverse-spectrum cosine expansion, not a Gaussian-moment theorem, finite-grid theorem, variance theorem, or normalized-bias theorem.

Its proof (`A3.SS3.2`, displays Ex134–137) uses `0<rho<1`, the complex exponential form of cosine and the geometric series to obtain

`1 + 2 sum_{j>=1} (-rho)^j cos(j theta)`

`= 1 - rho exp(i theta)/(1+rho exp(i theta)) - rho exp(-i theta)/(1+rho exp(-i theta))`

`= (1-rho^2)/(1+2rho cos(theta)+rho^2)`.

The definition of `rho` then gives both identities

`(1-rho)/(1+rho) = 1/sqrt(kappa)`,

`(1+2rho cos(theta)+rho^2)/(1-rho)^2 = (kappa+1+(kappa-1)cos(theta))/2`.

Combining them gives the stated expansion. Finally

`sum_{j>=1} |(-rho)^j cos(j theta)| <= sum_{j>=1} rho^j = rho/(1-rho)`.

The proof invokes the usual geometric-series convergence and a uniform summable majorant. Nonzero complex denominators follow from `|rho exp(±i theta)|=rho<1`; positivity of the real denominator follows also from the inverse-spectrum expression. The paper does not name separate lemmas for these denominator facts, cosine-exponential identities, the geometric-series theorem, or the uniform convergence criterion.

## C.8: exact finite-grid means and full proof route

C.8 (`A3.Thmtheorem8`) inherits all the family and Gaussian definitions, and for `1<=n<d` asserts exactly the two mean formulas above (Ex138). It is not merely the expansion C.7 and does not itself state the variance or exponential sandwich. Its proof (`A3.SS3.3`) contains these steps:

1. For every integer frequency `k`, the finite-grid sum is
   `sum_{i=1}^d cos(k theta_i) = d (-1)^a` if `k=2ad` for `a in Z`, and zero if `k` is not in `2d Z` (Ex139). For the second case, the half-grid cosine formula is `sin(k pi)/(2 sin(k pi/(2d)))=0`; its denominator is nonzero precisely in this case. For the first case each summand is `cos(2ai pi-a pi)=(-1)^a`. Negative and zero integer `k` belong to this assertion.
2. Since `E U_i^2 = 1/lambda_i`, finite expectation linearity gives `M = sum_i 1/lambda_i` and `mu_n = sum_i cos(n theta_i)/lambda_i` (Ex140). These are the bridge from actual Gaussian means to deterministic sums. They must not disappear when treating the algebraic summations.
3. C.7 gives a convergent inverse-eigenvalue expansion at each grid angle. Its absolutely convergent series may be interchanged with the finite sum. This is a proof ingredient, not a new public assumption that the grid moments or convergence already hold.
4. For `M`, only `j=2ad`, `a>=1`, survive, in addition to the constant term. Thus (Ex141–143)
   `M = (d/sqrt(kappa))(1+2 sum_{a>=1} (-1)^a rho^(2ad))`
   `= (d/sqrt(kappa))(1-2rho^(2d)/(1+rho^(2d)))`
   `= (d/sqrt(kappa))(1-rho^(2d))/(1+rho^(2d))`.
5. For `mu_n`, `sum_i cos(n theta_i)=0` since `1<=n<d`. Product-to-sum cancels the factor 2 in C.7 and gives (Ex144)
   `mu_n = (1/sqrt(kappa)) sum_{j>=1} (-rho)^j [sum_i cos((j-n)theta_i)+sum_i cos((j+n)theta_i)]`.
6. The first inner sum survives precisely at `j=n` (value `d`) or `j=2ad+n`, `a>=1` (value `d(-1)^a`). The second survives precisely at `j=2ad-n`, `a>=1` (value `d(-1)^a`). The three positive-frequency classes are disjoint because `1<=n<d`; the negative shifted exponent in `2ad-n` is still positive. At all these indices `(-rho)^(2ad±n)=(-1)^n rho^(2ad±n)`.
7. Reindexing those absolutely convergent classes and summing their geometric tails gives (Ex145–147)
   `(-1)^n mu_n = (d/sqrt(kappa))[rho^n + sum_{a>=1} (-1)^a (rho^(2ad+n)+rho^(2ad-n))]`
   `= (d/sqrt(kappa))[rho^n-(rho^(2d+n)+rho^(2d-n))/(1+rho^(2d))]`
   `= (d/sqrt(kappa))(rho^n-rho^(2d-n))/(1+rho^(2d))`.

Steps 4 and 7 are two distinct finite-grid computations. The paper leaves the elementary geometric-tail manipulation and rational simplification unnamed; the displayed equalities make their content explicit. The first tail uses ratio `-rho^(2d)`, and both shifted tails in the second computation have that same ratio and different initial powers. Neither exact mean is an assumption of this proof.

## Lemma 4.5 after C.8: variance branch

The proof of the lemma (`A3.SS3.4`) first invokes C.8 for both means (`A3.SS3.p7`). Its variance branch (`p8`, Ex148–149) then uses the Gaussian law and diagonal covariance, hence independent coordinates. Each `U_i` is centered Gaussian with variance `1/lambda_i`, so

`E U_i^4 = 3/lambda_i^2`, and `Var(U_i^2)=2/lambda_i^2`.

Also `lambda_i >= (kappa+1)/2-(kappa-1)/2 = 1`. The squared coordinates are independent, and weighting by deterministic cosine values gives

`Var(||U||^2) = 2 sum_i 1/lambda_i^2 <= 2 sum_i 1/lambda_i = 2M`,

`Var(U^T D_n U) = 2 sum_i cos^2(n theta_i)/lambda_i^2 <= 2M`.

The second inequality also uses `cos^2 <= 1`. Finally the exact formula for `M` yields `M <= d/sqrt(kappa)`, since `(1-rho^(2d))/(1+rho^(2d)) <= 1`. The base moment assumptions suffice: no spectral-gap condition involving `d-n`, no query count, no oddness, no small-bias hypothesis, and no separately assumed Gaussian fourth moment is added. The unnamed background ingredients are Gaussian fourth moments, independence from diagonal Gaussian covariance, preservation of independence under coordinate squaring, variance of an independent finite weighted sum, and finite second/fourth moment existence. The source gives no full derivations or citations for these standard probability facts.

## Lemma 4.5 after C.8: normalized-bias branch

Under the base conditions, `n<d` and `0<rho<1` imply `rho^n>rho^(2d-n)`, hence `(-1)^n mu_n>0`. Dividing the two exact means, with `M>0`, gives (p9, Ex150)

`|mu_n|/M = rho^n (1-rho^(2(d-n)))/(1-rho^(2d))`.

Since `0<rho^(2d)<rho^(2(d-n))<1`, the correction factor obeys (Ex151)

`1-rho^(2(d-n)) <= (1-rho^(2(d-n)))/(1-rho^(2d)) <= 1`.

The proof next bounds powers of `rho` under `kappa>=2` alone. It writes (p10, Ex152–154)

`log(1/rho) = log((sqrt(kappa)+1)/(sqrt(kappa)-1))`

`= 2 integral_0^(1/sqrt(kappa)) 1/(1-t^2) dt`

`= 2/sqrt(kappa) + 2 integral_0^(1/sqrt(kappa)) t^2/(1-t^2) dt`.

The integral is nonnegative, so `log(1/rho)>=2/sqrt(kappa)`. On this interval `1-t^2 >= 1-kappa^(-1)>0`; integrating `t^2` gives (Ex155–156)

`log(1/rho) <= 2/sqrt(kappa) + [2/(1-kappa^(-1))] integral_0^(1/sqrt(kappa)) t^2 dt`

`= (2/sqrt(kappa))(1+1/(3(kappa-1))) <= 8/(3sqrt(kappa)) < 3/sqrt(kappa)`.

The last numerical comparisons use `kappa>=2`. Exponentiation for positive `n` yields (Ex157)

`exp(-3n/sqrt(kappa)) <= rho^n <= exp(-2n/sqrt(kappa))`.

Only now does the additional condition `d-n>=sqrt(kappa)` enter (p11, Ex158). It gives

`rho^(2(d-n)) = exp(-2(d-n) log(1/rho)) <= exp(-4(d-n)/sqrt(kappa)) <= exp(-4)`.

Consequently `(1-exp(-4))rho^n <= |mu_n|/M <= rho^n`. Combining with Ex157 gives Ex159, the exact sandwich in Lemma 4.5. The source does not appeal to asymptotics for the constants: `1-exp(-4)`, `3`, and `2` are literal constants, and the logarithm estimate contains the explicit intermediate `8/3`. Unnamed steps include the elementary integral identity for the logarithm, its denominator/continuity domain, evaluation of the polynomial integral, monotonicity of powers and exponential, cancellation by positive denominators, and handling the alternating sign via absolute value.

## Source coverage and omissions boundary

- Section 4.1: family at Eq. 11, rotation, potential, Gaussian target, deterministic spectrum/known normalizer, and the whole comparison remark have been inventoried.
- Lemma 4.5: definitions, both mean formulas (`S4.Ex16`, a `tbody` inside `S4.EGx1`), both variance claims, added gap condition, and final bias sandwich (`S4.Ex17`) are distinct source obligations.
- C.7: statement Ex133; geometric/complex calculation Ex134–135; parameter identities Ex136; uniform absolute majorant Ex137.
- C.8: statement Ex138; all-integer grid sum Ex139; actual expectation-to-sum bridge Ex140; first mean Ex141–143; product-to-sum Ex144; frequency classes and parity in prose; second mean Ex145–147.
- Main lemma proof: C.8 invocation p7; independence/fourth moments/lambda lower bound and two variance rows Ex148–149 in p8; sign and normalized ratio Ex150, correction factor Ex151; log identities/bounds Ex152–156; power bounds Ex157; added gap and reflected-tail bound Ex158; final Ex159.
- Ex141–143, Ex145–149, Ex134–135, and Ex152–156 are `tbody` nodes, not independent tables. Their parent aligned tables are respectively EGx15, EGx16, EGx17, EGx14, EGx18, and EGx19. Selecting tables only would miss exact row anchors, though the complete C.3 section extraction includes them all.

The source does not spell out measure-theoretic random-variable representations, integrability proofs, Gaussian independence/fourth-moment derivations, elementary geometric/cosine/logarithm identities as separately named results, or a particular implementation API. These are proof details or background obligations, not source-authorized extra hypotheses. The source supplies actual Gaussian moment definitions and exact computations; it does not replace either mean with a premise saying the desired formula holds. No source correction or mathematical counterexample is proposed in this phase.

The only external citation in the selected source family is [22, Section 9.2]; the raw bibliography calls it OpenAI (2026), *Subpolynomial query complexity for well-conditioned log-concave sampling*, OpenAI Math Release preprint, identifier `OAI:Subpolynomial-query-complexity-for-well-conditioned-log-concave-sampling-September-26-2026`. I identified that citation from this raw bibliography only. I did not inspect or use the external package/reference. Appendix C.3 itself provides the relevant exact elementary calculations and makes no further external citation.

## Freeze boundary

This inventory is the independent source cognition before candidate/reconstruction exposure. Its semantic slots are objects, domains, quantifiers, assumptions, conclusions, scopes/senses, and constants/dependencies as detailed above. No Lean truth, candidate fidelity, candidate coverage, repair acceptance, or compilation verdict is issued. Later comparison requires the next authorized strict whitelist input; final whole-module/runtime review is a later phase.
