# Raw-source understanding freeze — mm_src_8c31

This is this actor's source-first freeze **before this actor's type/seal exposure**. A global exact seal is known to exist from the assignment, but it has not been opened. This document does not claim chronological priority over that global seal. No candidate signature, project definition/API, implementation, compiler result, decoder reconstruction, source graph, earlier semantic delta, or repair has been inspected.

Actor: `/root/mm_fresh_source_8c31`. Role: independent fresh source reviewer; not formalizer, source-graph extractor, or topology challenger. Authority at this phase: raw-source reading and freezing only. This is not a source-acceptance decision, Lean-truth decision, VERIFIED transition, publication, or integration authorization.

## Pinned source and bounded scope

Original source: arXiv:2610.20492v1, *On Complexity of Gaussian Sampling*, local HTML `.astis/huanjian-resume-20261103/2610.20492v1.html`; 951991 bytes; SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

I read all of C.2 p1–p12, including the intervening Fact C.5 and Fact C.6 statements. The source-facing mathematical boundary for the new packet is: the original independent Gaussian experiment (p1), actual cutoff (p10), actual truncated matrices and their exact means (p12, Ex107/108/110), and the two deterministic cosine-feature sums supplied by Fact C.5. C.2 p4/p5/p7 are used here only as the source derivation of those deterministic feature sums, not as acceptance of a separate untruncated Gram theorem. I also read the exact original Lemma 4.4 statement (`S4.Thmtheorem4`) to recover its standing experiment and q-range directly from source. The locator/index searches incidentally exposed other raw-source snippets; they are recorded separately in `input-exposure.json`.

Exact source fragments and line/byte locators are in `source-locators.json`; `source-slice.html` retains the C.2 raw slice and `source-readable.txt` replaces MathML by its own `alttext` without changing formulas. These derived copies are reading aids; the original HTML digest is controlling.

## Original experiment, objects, and indices

The original Lemma 4.4 allows an integer q >= 0 with 2q+1 < d and takes g_1,...,g_(q+1) to be independent N(0,I_d) vectors. The packet does not inherit the later concentration conclusion or its tau <= 1/2 condition as a premise for the exact truncated-mean identities.

Set r=q+1 and n=2q+1. Thus r>=1, and the admitted parameter range includes q=0; it is not legitimate to narrow it to q>0. In this range d>=2. For i=1,...,d,

\[
\theta_i=(i-\tfrac12)\pi/d,\qquad
t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))^\top\in\mathbb R^r,
\]
\[
\gamma_i=((g_1)_i,\ldots,(g_r)_i)^\top\in\mathbb R^r.
\]

The gamma_i are the column-coordinate views of those same original g_a draws. C.2 p1 explicitly states that gamma_1,...,gamma_d are independent N(0,I_r). Subsequent expectations refer to this same original product experiment; the source does not replace it by another law or select means by an external certificate. Their common marginal law, not independence alone, makes the scalar a below the same for every i. Independence also makes the actual Y_i independent, though linearity of their first moments does not itself need independence.

The row of B is d^(-1/2)(gamma_i tensor t_i)^T. The tensor order is **Gaussian first, cosine feature second**. Writing Gaussian indices alpha,beta in {1,...,r} and feature indices j,k in {0,...,q}, a tensor matrix entry is indexed by ((alpha,j),(beta,k)) and is gamma_i(alpha) gamma_i(beta) t_i(j) t_i(k). An implementation may use finite index encodings, but any swap needs an explicit semantic adapter; it is not the literal source order.

## Actual cutoff, actual matrices, and exact expectations

C.2 p10 sets

\[
L=2r+3\log(1000d),\qquad R_i=\|\gamma_i\|^2,
\qquad\mathcal T=\{R_i\le L\ \hbox{for every }i\}.
\]

The cutoff is **closed**: retained event R_i <= L, discarded event R_i > L. This convention occurs in p10, Ex107, Ex108, and the complementary bias formula Ex109. No replacement by R_i < L is presumed at this stage.

Ex107 (`A3.Ex107`, C.2 p12.1) literally defines

\[
Y_i=\frac1d(\gamma_i\gamma_i^\top\otimes t_it_i^\top)
\mathbf1_{\{R_i\le L\}}.
\]

These are actual random r^2 by r^2 matrices on the original Gaussian product experiment, rather than arbitrary matrices constrained to have convenient means. Entrywise,

\[
(Y_i)_{(\alpha,j),(\beta,k)}
=d^{-1}\gamma_i(\alpha)\gamma_i(\beta)t_i(j)t_i(k)
\mathbf1_{\{\|\gamma_i\|^2\le L\}}.
\]

Ex108 (`A3.Ex108`, C.2 p12.2) states by radial symmetry that

\[
\mathbb E[\gamma_i\gamma_i^\top\mathbf1_{\{R_i\le L\}}]=aI_r,
\qquad
a=\frac1r\mathbb E[R_i\mathbf1_{\{R_i\le L\}}].
\]

The following source sentence explicitly says a is the same for every i. It is the scalar induced by the actual common N(0,I_r) marginal law and this same L. Equivalently one may describe it with an index-free generic G having that common marginal law; an equality-of-law argument must connect this description to the actual gamma_i. A free witness with assumed mean identities would not be this source definition.

The next sentence uses E[R_i]=r to give 0<=a<=1 and Ex109,

\[
1-a=\frac1r\mathbb E[R_i\mathbf1_{\{R_i>L\}}]
\le\frac{L+3}{1000rd}.
\]

This is read context and a source consequence, not an external moment/bias certificate to add as a public premise. The new packet's central exact-mean conclusion does not need to be widened into acceptance of this tail/bias estimate.

C.2 p12.4 gives the individual expectation

\[
\mathbb EY_i=(a/d)(I_r\otimes t_it_i^\top).
\]

Fact C.5 is then invoked for Ex110 (`A3.Ex110`):

\[
\sum_{i=1}^d\mathbb EY_i=aI_{r^2},\qquad
\sum_{i=1}^d\cos(n\theta_i)\mathbb EY_i=0.
\]

The display uses **sums of expectations**. C.2 p12.5 then says the truncated weighted sum has zero expectation. That prose invokes finite linearity for the actual matrices. I do not select a candidate formal endpoint before seeing its exact type: sum_i E[Y_i], E[sum_i Y_i], and the weighted versions have distinct syntax and require the actual finite-exchange justification when interchanged. The expected weighted actual sum is mathematically consistent with Ex110 once its integrability and finite exchange are discharged internally.

## The only deterministic feature identities imported here

Fact C.5 (`A3.Ex87`) includes

\[
\sum_i t_it_i^\top=dI_r,\qquad
\sum_i\cos(n\theta_i)t_it_i^\top=0.
\]

C.2 p4 obtains the cosine-sum identity sum_i cos(k theta_i)=0 for integral 0<|k|<2d by telescoping sines at the half-step grid. p5 applies it to the constant coordinate and the frequencies j-k and j+k to obtain the first deterministic matrix sum. p7 applies the triple-product identity with n=2q+1: every n +/- j +/- k lies from 1 through 4q+1<2d, for 0<=j,k<=q, giving the weighted zero sum. The source standing condition 2q+1<d supplies the frequency separation. With q=0, t_i=(1), n=1, the positive-coordinate cases in p5 are empty and the same identities still apply. No extra q>0 premise is justified.

These deterministic identities are source proof ingredients to be supplied internally, not Gram/feature-sum certificates that may be added to the public source theorem as hypotheses. The untruncated Gram-mean statements in Fact C.5 and p6/p7 were read for complete p1–p12 context; they are not a substitute for computing the actual truncated mean.

## Internal mathematical obligations versus source gaps

The raw source is terse at “by radial symmetry.” The mathematical content to supply internally is: invariance of the common standard Gaussian marginal under coordinate sign flips/permutations; preservation of the radial closed event; vanishing off-diagonal integrals; equality of diagonal integrals; the trace identity yielding a=E[R 1]/r; and transport from the common marginal to each actual gamma_i. None is an additional source hypothesis.

Measurability follows internally from the original Gaussian random vectors, their coordinate/norm operations, the closed radial event, and finite matrix operations. For the truncated entries, |gamma_i(alpha)gamma_i(beta)| <= R_i, so on the retained event it is <=L. With |t_i(j)|<=sqrt(2), the actual Y_i entries are bounded by 2L/d in this parameter range. This supplies integrability directly. Deterministic cosine weights have magnitude at most one; finite sums remain integrable. Taking entries, pulling out deterministic factors, and exchanging expectation with a finite sum are internal obligations. Full Gaussian second moments used elsewhere are also properties of the actual law, not imported premises.

I identify **no genuine source gap in this bounded exact-mean claim at raw-source stage**. This does not certify any unseen formal theorem. In particular, failure to have a convenient project lemma for radial symmetry, moments, measurable indicators, tensor entries, or finite integration would be an implementation/API obligation; it would not by itself show a source defect or authorize a repair. Conversely a candidate that postulates the actual mean, common a, Gram sums, integrability, or a changed sampling law must later be checked against this frozen source boundary rather than excused as a missing source condition.

## Frozen seven-slot baseline (source only; no comparison verdict)

1. **Objects:** original independent g_a; their gamma_i views; deterministic half-grid t_i; actual closed-cutoff Y_i; scalar a induced by the common marginal; actual finite matrix sums.
2. **Domains:** nonnegative integral q, r=q+1, n=2q+1, d with 2q+1<d; i=1,...,d; gamma in R^r; features j=0,...,q; matrices on Gaussian-first pairs of r coordinates and r features.
3. **Quantifiers:** all such q,d and the original independent standard Gaussian experiment; one common scalar a with the displayed law-defined value works for all i; both aggregate identities hold in that same experiment. No new moment/certificate quantifier is source-authorized.
4. **Assumptions:** the original parameter/grid and Gaussian-law experiment. Radial first moments, integrability, individual means, and deterministic feature sums are conclusions/proof ingredients to establish, not added premises. No concentration event, tau cap, Gram certificate, or bias cap is a premise of the exact identities.
5. **Conclusion:** Ex108 radial scalar mean; p12.4 individual actual E[Y_i]; Ex110 sums of those expectations equal a I and zero; p12.5 actual weighted-sum zero expectation with internal finite exchange. The exact candidate consumer endpoint remains unseen and unselected.
6. **Scopes/senses:** unconditional entrywise/matrix expectations under the original experiment; closed cutoff; exact equalities, not high-probability statements or concentration estimates; Gaussian-first tensor order; common a across i, with q=0 retained.
7. **Constant dependencies:** r and n determined by q; L=2r+3 log(1000d); a determined only by r and that L/common standard Gaussian marginal (hence q,d), not i or an externally chosen mean witness. The zero weighted mean and aI identity require no chosen absolute concentration constant C.

Next authorized step, only after a separate packet authorization: type-only exposure and a separate immutable type-only freeze. No later stage has been performed in this artifact.
