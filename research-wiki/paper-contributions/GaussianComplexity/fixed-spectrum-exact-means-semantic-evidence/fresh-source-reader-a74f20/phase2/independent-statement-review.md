# Independent phase 2: statement and reconstruction comparison

Reviewer: `/root/source_reader_a74f20`, distinct from decoder `/root/decoder_6f192b`. This review follows and preserves the frozen source-only phase 1, manifest SHA-256 `5afcacc0ea702615faed565f8b99ed770d712c9839c1bedde12f9bd7ca4591db`. It concerns only the exact anonymous statement, approved definition context, new source-blind reconstruction, and private consumer statement in the strict whitelist. No candidate proofs/modules, lessons/publication context, graph, runtime, prior decisions, or ledger/frontier were read. The parent canonical packet hash is an opaque binding reference, not an opened input. No compilation claim is used as fidelity evidence.

## Verdict and exact boundary

**Equivalent for the bounded source target of both actual exact Gaussian means, with integrability made explicit as conclusions. No blocking semantic delta found.** The new reconstruction accurately interprets the displayed anonymous statement in the supplied definition context. Separately, the private actual-integral consumer statement agrees with the source's positivity, first-mean upper bound, signed-mean positivity, and normalized-ratio identity under the base conditions.

This verdict is not whole-Lemma-4.5 coverage: the anonymous main statement does not assert the two variance bounds or the conditional exponential sandwich, and its private consumer does not assert those either. It is also not a C.7 convergence theorem, a review of the proof realizing C.8's source route, a compilation/axiom verdict, or final proof/runtime/reader acceptance. Those boundaries cannot be settled from statements alone.

The whitelist's `source.original_text` is an adapted source restatement, not the literal original. In particular, the sentences about Lean indexing, the literal constructor, internal proofs, and explicit integrability are explanatory additions. I used the frozen raw source, rather than that restatement's assertions about internal proofs, to judge them. Its mathematical mean formulas and domain match the raw source. The claim that facts are proved internally remains unverified in this phase.

## Seven semantic slots

### 1. Objects

Raw source: the literal midpoint cosine grid, its eigenvalues and diagonal precision `Lambda`, `U ~ N(0,Lambda^{-1})`, the diagonal cosine matrix `D_n`, and the actual real expectations `M=E||U||^2`, `mu_n=E[U^T D_n U]`.

Anonymous statement and reconstruction: the same grid and eigenvalues define the same diagonal precision. The displayed measure is the centered multivariate Gaussian with parameter `Lambda^{-1}`; the approved context says that parameter is covariance on the positive semidefinite domain. The integrand `Q(x)=sum_i cos(n theta_i) x_i^2` is exactly the diagonal quadratic form `x^T D_n x`. `WithLp.ofLp` exposes the same real coordinates, and the norm is the standard Euclidean norm. Both conclusions integrate these functions against that one explicitly constructed Gaussian measure. The private consumer defines `m` and `b` by those same integrals, rather than introducing arbitrary real variables.

The covariance/precision distinction is correct. The theorem does not pass `Lambda` itself as covariance, nor square/invert it twice. It does not replace actual integrals by deterministic sums assumed to have the right values. The reconstruction preserves these objects and correctly keeps the integration measure's dependence on `kappa`.

### 2. Domains

Raw family: integer dimension `d>=2`, real `kappa>=2`, real `d`-dimensional Euclidean vectors; Lemma 4.5 uses integer `1<=n<d`. C.8 uses the inherited family. The anonymous statement uses natural `d,n` with those bounds, and real `kappa`. A positive integer `n` is equivalently a natural in this range; no negative or zero valid source frequencies are lost. The coordinates are `Fin d`, an equivalent presentation of the finite Euclidean coordinate set. The dimension lower bound is preserved.

The source indexes `i=1,...,d`, while the statement/reconstruction use `i=0,...,d-1`. Under `i_source=i_lean+1`, `(i_source-1/2)pi/d=(i_lean+1/2)pi/d`; every eigenvalue, cosine weight, and coordinate is paired exactly. This is a bijective relabeling, not a shifted spectral grid.

### 3. Quantifiers

Both source target and anonymous statement apply separately to every admissible `d,kappa,n`, with the grid and measures defined from those values. The choice of canonical Gaussian measure represents the source's law `U~N(0,Lambda^{-1})`; expectations of the functions depend only on that law, so the source's arbitrary realization of such a random vector does not require a new independent probability-space binder in this measure formulation.

There is no existential hidden constant, asymptotic qualifier, almost-everywhere weakening, selected special mode, query count, or oddness requirement. The contextual `n=2q+1` in Remark 4.2 is correctly absent. The exact statement and reconstruction agree about all natural powers and the per-parameter interpretation. No algorithm/Haar randomness is quantified because these eigen-coordinate moments do not require it.

### 4. Assumptions and binder/definition audit

All public premise binders in the anonymous statement are `hd:2<=d`, `hκ:2<=κ`, `hn:1<=n`, and `hnd:n<d`. The remaining objects are displayed `let` definitions. Their literal expansions are given, so no opaque proposition or record can hide an assumed exact moment formula, variance bound, Gaussian bridge, summability condition, or ratio identity.

The approved constructor context includes totalized matrix/real inverses and a totalized matrix square root. These do not add a premise or alter this source domain: `cos(theta_i)>=-1`, `kappa-1>=0`, and the literal eigenvalue expression imply `lambda_i >= (kappa+1)/2-(kappa-1)/2=1`. Thus `Lambda` and its inverse are diagonal positive definite matrices, so the inverse and square root agree with their ordinary positive definite meanings and the constructor is the source Gaussian. This mathematical domain justification requires no candidate proof/API inspection.

Likewise `d>=2` and `kappa>=2` imply `d>0`, `sqrt(kappa)>1`, `0<r<1`, and every denominator in the displayed means is positive. Since `n<d`, natural subtraction `2*d-n` is ordinary subtraction, with positive result. In the private consumer, `d-n>0`, and `2*(d-n)=2d-2n`. These totalization issues cause no mismatch within the stated bounds.

Integrability is explicitly in the anonymous conclusion, not its hypotheses. The raw source defines actual Gaussian means, computes finite expressions for them, and further computes fourth moments and finite variances in its proof. Finite-dimensional Gaussian second moments imply integrability of `||x||^2`; `|Q(x)|<=sum_i x_i^2=||x||^2` implies integrability of `Q`. Accordingly the explicit Bochner integrability conclusions are source-implicit regularity made visible, not added assumptions or a source repair. Independence and Gaussian fourth moments are also not new statement premises.

No gap hypothesis `d-n>=sqrt(kappa)` is needed for these two means or the private exact-ratio identity. It is correctly absent. Adding it here would strengthen the source premises unnecessarily.

### 5. Conclusions

Raw C.8 Ex138, with its proof Ex140–147, gives the actual expectations

`M=(d/sqrt(kappa)) (1-r^(2d))/(1+r^(2d))`,

`(-1)^n mu_n=(d/sqrt(kappa)) (r^n-r^(2d-n))/(1+r^(2d))`.

The anonymous statement concludes integrability of both integrands and precisely these two equalities for their actual integrals. It retains the first finite-grid correction, the alternating sign multiplying the second actual mean, its reflected term `r^(2d-n)`, and the denominator `1+r^(2d)`. The reconstruction contains the same formulas and explicitly keeps them with the same measure. There is no absolute value substituted for the second signed equality and no missing factor of `d`, `sqrt(kappa)`, or 2.

The private consumer concludes `0<m`, `m<=d/sqrt(kappa)`, `0<(-1)^n*b`, and

`|b|/m = r^n (1-r^(2*(d-n)))/(1-r^(2*d))`.

These are exactly the source's derived positivity, first-mean bound (p8.2), signed-mean positivity, and ratio identity (p9.1/Ex150). To check their mathematical implication without candidate proof access: `0<r<1` makes `0<r^(2d)<1`, so the first exact formula has positive numerator/denominator and factor at most 1. Since `n<d`, `n<2d-n` and `r^n>r^(2d-n)`, giving the strict signed-mean positivity. Factoring the latter difference as `r^n(1-r^(2(d-n)))` and dividing by the positive first mean cancels `d/sqrt(kappa)` and `1+r^(2d)` and yields the displayed ratio.

### 6. Scopes and senses

All equalities concern exact real expectations/Bochner integrals. They are not deterministic pointwise identities for a sample, not an expectation of a ratio, not `E|Q|/M`, and not a ratio of variances. The consumer's `|b|/m` puts the absolute value on the actual signed mean `b` after integration; it does not move the absolute value inside the integral.

The statement has the bounded two-mean scope of C.8; it does not silently claim all of C.7 or the whole of Lemma 4.5. The private consumer's base-domain exact ratio agrees with Ex150, before the source introduces `d-n>=sqrt(kappa)` in p11/Ex158. The final exponential sandwich in the lemma is conditional on that added gap; the consumer makes no exponential sandwich claim, so its absence of the gap is faithful. The source also proves its exponential upper side under base conditions, but that additional derived result is absent here and is not needed for this bounded comparison.

Bochner integrability in the main conclusion prevents totalized integrals from masquerading as actual means. The consumer does not restate integrability, but its literal `m,b` definitions denote the same measure/functions whose integrability is asserted by the main statement; mathematically these integrals have the source's ordinary finite-expectation meaning on this domain.

### 7. Constants and dependencies

All constants and exponents in the two exact formulas and private ratio match the source exactly: half-step `1/2`, affine-spectrum halves, Euclidean square exponent 2, sign `(-1)^n`, prefactor `d/sqrt(kappa)`, denominator `1+r^(2d)`, reflected exponent `2d-n`, and consumer exponents `2(d-n),2d`. No unspecified constant or asymptotic replacement is introduced.

`theta` depends on `d` and its index; eigenvalues, `Lambda`, and `mu` depend on `d,kappa`; `Q` depends on `d,n`; `r` depends only on `kappa`; `m` is independent of `n` even though packaged in a statement quantifying over `n`; `b` depends on all three parameters. These agree with the raw source and the reconstruction. The private first-mean upper bound has exact constant 1, and the signed-mean and ratio conclusions introduce no new constants. The source variance constant 2 and exponential constants `1-exp(-4),3,2` are outside this bounded theorem's conclusions and cannot be credited to it.

## Delta and adaptation classification

1. **Equivalent representation, nonblocking:** one-based coordinates to `Fin d` with the corresponding angle conversion; positive integer modes to natural modes; a law-specific random vector to its canonical Gaussian measure; diagonal quadratic matrix form to the coordinate sum.
2. **Source-implicit regularity made an explicit conclusion, nonblocking:** both integrability claims. They follow on the literal Gaussian domain and add no premise. They do not require changing the source theorem.
3. **Standard totalized definitions restricted to the ordinary domain, nonblocking:** matrix inverse, covariance square root, real division/square root, and natural subtraction. The displayed source assumptions and definitions imply the relevant positivity/range facts. The reconstruction's ordinary-Gaussian interpretation is therefore justified, without accepting any claim about candidate proof implementation.
4. **Bounded coverage, neither mismatch nor completion credit:** this is the actual-mean subtarget plus a private exact-ratio consumer. It leaves C.7's full analytic expansion/convergence, both variance results, and the conditional exponential sandwich outside its statement. A later whole-lemma claim would need those separate obligations.
5. **Restatement labeling caveat, nonblocking:** `source.original_text` contains explanatory implementation-oriented text and internal-proof assertions that are not literal raw-source sentences. The adapted mathematical target is faithful; proof assertions remain deferred. This review does not endorse treating that string as a verbatim quotation.

No mathematically necessary extra hypothesis, source repair, missing conditional premise, altered expectation, or changed constant was identified. No repair proposal is made. The source proof routes remain those independently inventoried in phase 1, not anything inferred from an unseen candidate proof.

## Input binding and deferred authority

Whitelist raw hashes verified: selective input `c40c778612c2a6c649c33347d5621ab1cd59c11971eb6986c219cc3a504be4fe`; its manifest `e6a665fdcd24e37e913aad795b77f50ec2f2aaea805c161c7adc62a7f1f7a977`. Embedded source-restatement, exact-statement, and reconstruction text digests were recomputed and matched their claims. The private consumer text digest is `9c01fa76e762811783369ef250d011e8ff41f9dd709fc1f4648bff413542559a`. Frozen phase1 raw/cognition digests were recomputed without modification and matched.

The reconstruction metadata reports `source_text_visible=false`; I have no contrary exposure in this review, but that field is a supplied metadata assertion, not independently observed decoder history. My own phase1 preceded this whitelist exposure. This phase gives an independently reasoned, input-bound statement fidelity verdict; a canonical full-packet review, whole-module/axiom/proof-route review, runtime checks, reader checks, and any normal V action require later authority and are not performed or certified here.
