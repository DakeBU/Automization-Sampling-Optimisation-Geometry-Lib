# Independent source-first notes, phase 1

Reviewer: `mgf_fresh_source_5b7e`.
Role: independent original-source / whole-module / reader reviewer; not the formalizer, decoder, source-topology author, or acceptance owner.
This document is frozen before receipt of any new candidate module, reader, native result, decoder reconstruction, canonical reviewer packet, or prior semantic verdict.

## Inputs and exposure boundary

- Gaussian original HTML: `.astis/huanjian-handoff-20261019/2610.20492v1.html`, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
- Tropp author preprint PDF: `.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf`, SHA-256 `f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86`.
- Read repository instructions: `AGENTS.md`, contributor contract, theorem-publication protocol, proof-digestion protocol, evidence-routed-memory protocol, and `.agents/skills/astis-semantic-roundtrip/SKILL.md`. Read PDF skill for original-page inspection.
- No production Lean, ROOT signature/seal, authored lessons, old source reviews, old SG/TC/acceptance contents, previous verdicts, decoder packets, or reconstructions were read. The initial broad filename-discovery command emitted paths of older artifacts; those files were not opened and their contents were not used.
- No build, network operation, publication-state API, shared-site mutation, ledger mutation, frontier mutation, or subprocess agent was used.
- All newly written files are inside this reviewer's assigned directory.

Source reading performed:

1. Tropp complete printed pages 7-9 and 25-26, as rendered images as well as text. This covers sections 2.1-2.7, definitions needed to interpret expectation and matrix functions, and the full statement and proof of Lemma 6.7 across pp.25-26. Also read the adjacent Theorem 6.1 statement (text, pp.23-24) and its proof (complete p.26) to determine the boundary between one-matrix MGF and the sum/tail consumer. Theorem 6.2 and Lemma 6.8 were encountered only as page adjacency, not audited as candidate targets.
2. Gaussian complete C.2, from `A3.SS2` to immediately before `A3.SS3`, including Fact C.5, Fact C.6, all displayed derivations Ex85-132, and all intervening substantive paragraphs. Central review region is Ex107-121, including the three rows in `A3.EGx11` corresponding to Ex115-117.
3. Gaussian real/symmetric/Loewner notation in section 2; the hard family in 4.1; complete 4.2-4.4 to see actual uses of Lemma 4.4 and Fact C.6. Reading the main-proof consumer establishes its interface, not an audit or completion of either main lower bound. C.1/C.3/C.4 proof interiors are outside this review.

The extraction files are mechanically derived reading aids, not independent sources. Gaussian math uses the original HTML `alttext`, with original block ids retained. Tropp PDF was converted by `pdftotext -layout`; ambiguous text glyphs were checked against the page images.

## Tropp: source-level objects, assumptions, and exact MGF statement

The preprint is *User-Friendly Tail Bounds for Sums of Random Matrices*, Joel A. Tropp, revision dated 15 June 2011 on its first page.

Section 2.1 fixes finite square complex matrices unless otherwise specified. `s.a.` means self-adjoint; Loewner order is the positive-semidefinite order; the norm is the Euclidean/operator norm. Real symmetric matrices are a specialization of these source objects, not the full complex source carrier.

Section 2.2 makes a standing regularity convention: random variables are sufficiently regular to justify expectations, limit interchanges, etc.; almost-sure qualifications are often suppressed. This is mathematically meaningful context, not a license to infer unspecified integrability from a one-sided spectral bound. In particular, an upper eigenvalue bound does not itself bound the negative tail or guarantee a finite second moment. Any explicit measurable/integrable binder must be traced to this convention or proved from genuine source inputs.

Section 2.3 defines a real scalar function on a self-adjoint matrix by spectral calculus:

\[
f(A)=Qf(\Lambda)Q^*,\qquad A=Q\Lambda Q^*.
\]

Its transfer rule (2.2) is:

\[
\bigl(\forall a\in I,\ f(a)\leq g(a)\bigr),\quad
\operatorname{spec}(A)\subseteq I
\quad\Longrightarrow\quad f(A)\preceq g(A).
\]

This compares two scalar functions of the same matrix. It does **not** assert that matrix exponential is operator monotone on arbitrary pairs. The source explicitly warns in section 2.5 that the exponential is not operator monotone.

Section 2.4 supplies (2.3), for self-adjoint A:

\[
I+A\preceq\exp(A).
\]

Section 2.7 supplies the expectation-order implication (2.13):

\[
X\preceq Y\ \text{a.s.}\quad\Longrightarrow\quad
\mathbb E X\preceq\mathbb E Y.
\]

Its regularity is governed by section 2.2. A theorem using Bochner/entrywise integrals must account for legitimate expectations. Probability normalization matters when replacing the expectation of constant I by I.

Lemma 6.7 (pp.25-26) is the following one-random-matrix assertion:

\[
\mathbb E X=0,\qquad X=X^*\ \text{a.s.},\qquad
\lambda_{\max}(X)\leq1\ \text{a.s.}
\]

imply, for every scalar \(\theta>0\),

\[
\mathbb E\exp(\theta X)
\preceq
\exp\bigl((e^\theta-\theta-1)\,\mathbb E(X^2)\bigr).
\tag{T-MGF}
\]

The multiplication inside the final exponential is scalar multiplication of the matrix second moment, not an entrywise scalar exponential. There is no independence hypothesis (only one random matrix), no trace in the conclusion, no dimension factor, no sum, and no tail probability. There is no restriction \(\theta<3\) or \(\theta\leq1\). The explicit source interval is \(\theta>0\), not all real theta. No PSD assumption on X and no lower-eigenvalue bound are imposed.

The source proof, completely read, uses these ingredients in this order:

1. Fix theta > 0 and set
   \[
   f(x)=\frac{e^{\theta x}-\theta x-1}{x^2}\quad(x\ne0),
   \qquad f(0)=\theta^2/2.
   \]
2. The smooth extension f is increasing on the **whole real line**, hence f(x) <= f(1) for x <= 1. The source leaves the derivative verification as an exercise.
3. Apply spectral transfer using the actual eigenvalue interval \(( -\infty,1]\): \(f(X)\preceq f(1)I\).
4. Expand and apply congruence by X:
   \[
   \exp(\theta X)=I+\theta X+Xf(X)X
   \preceq I+\theta X+f(1)X^2.
   \]
   Congruence preserves order even when X is indefinite. Neither X nor f(X) may be silently replaced by entrywise operations.
5. Take expectations by (2.13), remove the mean-zero term, and use (2.3) with \(A=f(1)\mathbb E(X^2)\):
   \[
   \mathbb E e^{\theta X}
   \preceq I+f(1)\mathbb E(X^2)
   \preceq\exp(f(1)\mathbb E(X^2)).
   \]
6. Since \(f(1)=e^\theta-\theta-1\), this is (T-MGF).

If a new result chooses an arbitrary positive scale R, the substitution X=Z/R and source parameter theta*R gives the mathematically derived formula

\[
\mathbb E e^{\theta Z}\preceq
\exp\left(\frac{e^{\theta R}-\theta R-1}{R^2}\,\mathbb E(Z^2)\right),
\quad R>0,\ \theta>0,\ \lambda_{\max}(Z)\leq R.
\]

This scaled display is a reviewer inference from Lemma 6.7, not the literal lemma statement, and is not a prediction of any candidate interface. R=0 is outside that division argument and requires separate treatment. A two-sided norm hypothesis would permit application to both signs, but is stronger than the original one-sided premise.

## Gaussian C.2: actual local objects and source formulas

All matrices in the Gaussian source are real; order is defined for symmetric matrices by positivity of B-A. The hard family has

\[
\theta_i=(i-\tfrac12)\pi/d,\qquad
\lambda_i=(\kappa+1)/2+(\kappa-1)\cos(\theta_i)/2,
\qquad i=1,\ldots,d,
\]

with d>=2, kappa>=2. For the local concentration argument q is an integer >=0, \(2q+1<d\), \(r=q+1\), \(n=2q+1\), and the d-dimensional vectors \(g_1,\ldots,g_r\) are independent standard real Gaussians. Thus

\[
\gamma_i=((g_1)_i,\ldots,(g_r)_i)^\top\sim N(0,I_r),
\quad i=1,\ldots,d,
\]

are independent **across i**. Deterministic vectors and matrices are

\[
t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))^\top,
\quad B_{i,:}=d^{-1/2}(\gamma_i\otimes t_i)^\top,
\quad D_n=\operatorname{diag}(\cos(n\theta_i)).
\]

B has size d by r^2. The Gram matrices and every Y_i, Z_i below have size r^2 by r^2, which is the dimension producing the prefactor r^2 in Bernstein.

Fact C.5 establishes rather than assumes, within the paper's proof:

\[
\operatorname{range}(B)=\mathcal K_q,\quad
\mathbb E B^\top B=I_{r^2},\quad
\mathbb E B^\top D_nB=0,
\]

\[
\|t_i\|^2\leq2r,\quad
\sum_i t_it_i^\top=dI_r,\quad
\sum_i\cos(n\theta_i)t_it_i^\top=0.
\tag{G-basis}
\]

The proof uses the nonconstant affine relation between lambda_i and cos(theta_i), the triangular Chebyshev change of basis, discrete cosine orthogonality for nonzero |k|<2d, and product-to-sum identities. The weighted frequency range is explicitly
\(1\leq n-j-k\leq n\pm j\pm k\leq n+j+k\leq4q+1<2d\).

Before Ex107 the proof sets

\[
L=2r+3\log(1000d),\qquad R_i=\|\gamma_i\|^2,
\qquad\mathcal T=\{\forall i,\ R_i\leq L\}.
\]

It derives the Gaussian norm-squared MGF \(\mathbb Ee^{R_i/3}=3^{r/2}\), the tail bound \(\mathbb P(R_i>2r+3x)\leq e^{-x}\) for x>=0, \(\mathbb P(\mathcal T)\geq0.999\), and the tail-integral bound

\[
\mathbb E[R_i\mathbf1_{R_i>L}]\leq(L+3)/(1000d).
\tag{G-bias-input}
\]

The core Ex107-121 formulas, read with all intervening paragraphs, are:

| Original anchor | Formula / obligation |
| --- | --- |
| Ex107 | \(Y_i=d^{-1}(\gamma_i\gamma_i^\top\otimes t_it_i^\top)\mathbf1_{R_i\leq L}\). These are independent, symmetric, PSD random matrices. |
| Ex108 | Radial symmetry gives \(\mathbb E[\gamma_i\gamma_i^\top\mathbf1_{R_i\leq L}]=aI_r\), where \(a=r^{-1}\mathbb E[R_i\mathbf1_{R_i\leq L}]\). The common scalar a does not depend on i. |
| Ex109 | \(0\leq a\leq1\), \(1-a=r^{-1}\mathbb E[R_i\mathbf1_{R_i>L}]\leq(L+3)/(1000rd)\). |
| Paragraph before Ex110; Ex110 | \(\mathbb EY_i=(a/d)(I_r\otimes t_it_i^\top)\); then \(\sum_i\mathbb EY_i=aI_{r^2}\) and \(\sum_i\cos(n\theta_i)\mathbb EY_i=0\), using G-basis. |
| Paragraph before Ex111 | Define \(Z_i=Y_i-\mathbb EY_i\). Centering is part of the construction, not an extra source theorem premise. |
| Ex111 | \(\|Y_i\|_{op}=R_i\|t_i\|^2\mathbf1_{R_i\leq L}/d\leq2rL/d\); \(\|\mathbb EY_i\|_{op}=a\|t_i\|^2/d\leq2r/d\). |
| Ex112 and next paragraph | \(\|Z_i\|_{op}\leq R_*:=2r(L+1)/d\). Also \(\|\cos(n\theta_i)Z_i\|_{op}\leq R_*\), using the absolute cosine bound. |
| Ex113 and explanation | \(\mathbb E[R_i\gamma_i\gamma_i^\top]=(r+2)I_r\). Off-diagonal entries vanish by sign symmetry; diagonal entries are \(3+(r-1)\). |
| Ex114 | \(Y_i^2=d^{-2}R_i\|t_i\|^2(\gamma_i\gamma_i^\top\otimes t_it_i^\top)\mathbf1_{R_i\leq L}\). Indicator idempotence and rank-one square identities are used. |
| `A3.EGx11`, Ex115-117 | Dropping the indicator is valid in PSD order. Then \(\sum_i\mathbb EY_i^2\preceq(r+2)d^{-2}\sum_i\|t_i\|^2(I_r\otimes t_it_i^\top)\preceq2r(r+2)d^{-1}I_{r^2}\). This uses both G-basis bounds, not just a trace estimate. |
| Ex118 | \(\mathbb EZ_i^2=\mathbb EY_i^2-(\mathbb EY_i)^2\preceq\mathbb EY_i^2\). The two noncommuting cross terms each have expectation \((\mathbb EY_i)^2\); the deterministic square is PSD. |
| Ex119 | The sequence has variance parameter at most \(v_*:=2r(r+2)/d\), i.e. the operator norm of \(\sum_i\mathbb EZ_i^2\) is bounded by v_*. |
| Ex120 | \(\mathbb E[(\cos(n\theta_i)Z_i)^2]=\cos^2(n\theta_i)\mathbb EZ_i^2\preceq\mathbb EZ_i^2\). The weights are deterministic and may be negative. |
| Paragraph before Ex121; Ex121 | Each of the two sequences is independent, centered and self-adjoint. For t>0, \(\mathbb P(\|\sum_i Z_i\|_{op}>t)\leq2r^2\exp[-t^2/(2(v_*+R_*t/3))]\), and the same bound holds for the cosine-weighted sum. |

The named two-sided bounded matrix Bernstein inequality in Ex121 is an external mathematical input. The Gaussian original does not name Tropp in this paragraph, and a case-insensitive search of the complete original-derived text found no occurrence of Tropp. No direct Gaussian-to-Tropp citation is asserted here. Tropp is independently matched background.

## Actual downstream consumer boundary

Immediately after Ex121 the paper chooses

\[
z=\log(1000r^2),\qquad
\Delta=\sqrt{2v_*z}+2R_*z/3.
\]

Ex123 expands the quadratic to show
\(\Delta^2-2z(v_*+R_*\Delta/3)=(2R_*z/3)\sqrt{2v_*z}\geq0\).
Each tail probability is at most 0.002, and a union bound gives both centered-sum bounds with probability at least 0.996 (Ex124).

On \(\mathcal T\), Ex125 identifies

\[
B^\top B-I_{r^2}=\sum_i Z_i-(1-a)I_{r^2},
\qquad B^\top D_nB=\sum_i\cos(n\theta_i)Z_i.
\]

The common scalar bias a and the weighted-mean cancellation are essential to the second identity. Intersection with the truncation event gives probability >=0.995 and the bounds Delta+(1-a), Delta (Ex126). The source then establishes an **absolute** constant c such that

\[
\Delta+(1-a)\leq c\left[r\sqrt{\log d/d}+r(r+\log d)\log d/d\right].
\]

The same absolute choice of C in \(\tau_{d,q}\) establishes Fact C.6. This constant must not depend on kappa, q, d, or Gaussian samples.

The remaining C.2 paragraphs prove Lemma 4.4: on the single simultaneous event, every u in K_q is Bc; the Gram bounds give

\[
\|u\|^2\geq(1-\tau)\|c\|^2,
\quad |u^\top D_nu|\leq\tau\|c\|^2,
\quad |u^\top D_nu|\leq2\tau\|u\|^2
\]

provided \(\tau\leq1/2\). The conclusion is simultaneous for every u on one event; a separate high-probability assertion for each fixed u is weaker. The proof's probability 0.995 is relaxed to the lemma's 0.99.

The main text's actual uses are:

- Section 4.2 after Lemma 4.4: combine the simultaneous statement with the adaptive output's Krylov representation to bound \(|X^\top OD_nO^\top X|\leq2\tau\|X\|^2\). The coefficients may depend on the full experiment, so fixed-coefficient concentration cannot replace simultaneous control.
- Section 4.3, algorithmic-output part: after q's range implies n<d and tau<=1/2 for sufficiently large d depending only on delta, Lemmas 4.3/4.4 yield the failure bound 0.01 for the signed separating event. This is a consumer of the full local chain, not of a single MGF theorem alone.
- Section 4.4 accuracy limitation: the paper refers to the Bernstein calculation in Fact C.6 when describing the scale available to that proof. That limitation claim is not certified by checking Lemma 6.7 alone.

The target-moment and total-variation contradiction branches, Theorem 4.1, Theorem 3.1, whole-paper closure, site delivery and purification are not completed or reviewed by this local source audit.

## Frozen obligations and anticipated fidelity checks

These are source-derived checks, fixed without seeing a candidate:

1. **Matrix meaning:** finite real/complex carrier and dimension, self-adjointness/symmetry, Loewner order, matrix exponential, matrix square, and scalar multiplication must preserve their source meanings. An entrywise exponential or entrywise positivity is not a substitute.
2. **Probability meaning:** expectation is under a probability law; a.s. bounds and standing regularity must be visible or correctly derived. Do not use totalized integrals of nonintegrable functions as actual source expectations.
3. **Tropp MGF binders:** zero mean, one-sided upper eigenvalue bound, theta>0, and the source standing regularity. A norm bound is a specialization; independence is unnecessary here. E exp <= exp of the second moment is the exact form, not merely a scalar quadratic-form bound or trace bound.
4. **Scalar remainder:** removable value at x=0 and monotonicity over all real x<=1 must be justified. A proof valid only on [0,1] cannot support the source's indefinite matrices. A theta-domain restriction is a genuine narrowing.
5. **Order operations:** spectral transfer for functions of one matrix, congruence, expectation-order passage, linearity and probability normalization, then I+A<=exp(A). No arbitrary matrix-exponential operator-monotonicity step is available.
6. **Gaussian construction:** Ex107-120 facts are proof obligations obtained from Gaussians, deterministic cosine vectors, truncation and centering. They cannot become new public premises of a claimed faithful Fact C.6 or Lemma 4.4. A generic reusable theorem may legitimately assume its own explicit bounds but cannot claim to have discharged the Gaussian adapters.
7. **Two signs / weighted case:** centered summands may be indefinite; cosine weights may be negative. A PSD-only theorem or one-sided bound requires additional adapters to reach the two-sided operator-norm source conclusion. Independence across i and deterministic weights must be retained.
8. **Variance and constants:** preserve the full PSD summed-second-moment bound, r^2 matrix dimension, v_*=2r(r+2)/d, R_*=2r(L+1)/d, t>0, the denominator's /3 and factor 2, and the exact failure probabilities at the actual consumer. Do not replace variance by a trace or sum of norms without naming the resulting weaker theorem.
9. **Completion separation:** a source-faithful one-matrix MGF can discharge only that local background ingredient. Complete Ex121 additionally needs a sum-MGF/Laplace mechanism and the two-sided/sign argument; complete Fact C.6 additionally needs truncation, bias, variance and numerical/event-budget steps; complete Lemma 4.4 additionally needs the uniform range/Gram argument.
10. **Reader:** the attributed original statement, full assumptions and parameter domain, displayed proof steps, actual mathematical dependencies and remaining boundary must stay adjacent. The Tropp background attribution must not become a fictitious explicit citation by the Gaussian authors. Source gaps must remain visible even if some narrower Lean proposition compiles.

## Ambiguities, omissions, and nonclaims

- Tropp's section 2.2 intentionally suppresses a full measure-theoretic regularity specification. A modern explicit formal theorem must expose the required conditions and classify their relation to this standing convention. A one-sided upper spectral bound alone does not supply second-moment integrability.
- Tropp's monotonicity calculation for f is omitted as an exercise, not proved in the original paragraph. This is an explicit expansion obligation, not evidence that the lemma is false.
- Gaussian invokes the two-sided bounded matrix Bernstein inequality by name without an exact theorem/citation at Ex121. Tropp's Theorem 6.1 has matching one-sided tail structure; applying it to both signs under the Gaussian norm bound is a mathematically compatible background route. The paper does not identify that route as its own literal citation.
- Gaussian's independent-row Gaussian claim, radial-symmetry expectation, fourth-moment identity, tail integral and final absolute-constant simplification each contain mathematical content beyond the single MGF lemma. They remain real obligations for any full consumer claim.
- No source falsehood or necessary source repair was found in the read local formulas. This is a provisional original-source reading, not a fidelity verdict on unseen code, an accepted repair, a topology approval or a completion status.

Next authorized step: wait for ROOT's immutable new P/T module and reader materials; review source versus whole code and reader independently **before** viewing any decoder reconstruction; then compare all seven slots only after receipt of canonical fresh reviewer packets. No normal VERIFIED API is called by this reviewer.
