# Source-only contract frozen before candidate exposure

Reviewer: `/root/reader_835194`. Phase: `RAWPHASE1_SOURCE_ONLY`.
Sole primary mathematical source: *On Complexity of Gaussian Sampling*,
arXiv:2610.20492v1, original HTML SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
Selected anchors: S4.E11 and Appendix C.4 (A3.SS4 / A3.Ex160), with the
original Section 2 setup and Lemma 4.6 statement. This document makes no
candidate comparison or fidelity decision.

## Exact source objects and range

For every integer (dge2), real (kappage2), and (i=1,ldots,d),

[
	heta_i=rac{(i-	frac12)pi}{d},qquad
lambda_i=rac{kappa+1}{2}+rac{kappa-1}{2}cos	heta_i,qquad
Lambda=operatorname{diag}(lambda_1,ldots,lambda_d).
]

For every real orthogonal (Oinmathrm O(d)), put (A=OLambda O^	op).
Here (A) is the **actual precision**, and the covariance is (A^{-1}).
The source's full real orthogonal group is
({Oinmathbb R^{d	imes d}:O^	op O=I_d}). Its two determinant-sign
components each have Haar probability (1/2); neither component is excluded.
The hard-input law draws (O) from the full Haar probability, independently
of algorithm randomness. The algebraic statement below is pointwise for every
(O), requiring no probability or almost-everywhere qualification.

The original formulas and Appendix C.4 give
(0<	heta_i<pi), (-1<cos	heta_i<1), and
(1<lambda_i<kappa). Thus the family's eigenvalues are strictly interior
even though admissibility is the closed comparison (I_dpreceq Apreceqkappa I_d).
Both (d=2) and (kappa=2) are included. No parity restriction occurs.
The ambient Section 2 class permits (dge1,kappage1); that broader
ambient range must not silently replace the selected hard-family range.

## Bounded determinant component

From these actual source objects, the direct finite-dimensional algebraic
consequence is

[
det(OLambda O^	op)=det A=detLambda
=prod_{i=1}^dlambda_i>0.
]

The determinant and eigenvalue product depend on (d,kappa), and are
independent of (O). The display of the finite product is a direct
linear-algebra expansion, **not a verbatim display in C.4**. The orthogonal
determinant cancellation is ((det O)^2=1); it does not assume positive
orientation. The determinant is of the actual conjugated precision, rather
than an unrelated scalar named after that matrix.

The grid formula and orthogonality are source inputs. Positive definiteness,
positive determinant, the diagonal determinant product and the conjugation
determinant identity are consequences/dependencies, not extra public premises.
No (delta,arepsilon), query budget, algorithm, large-(d) threshold,
or restriction (kappale d^{1-delta}) belongs in this local contract.

## Separate normalization levels

The source explicitly identifies (f_A(x)=V_A(x)=x^	op A x/2),
(pi_A=N(0,A^{-1})), and states by Gaussian integration

[
Z_A=(2pi)^{d/2}(det A)^{-1/2}
   =(2pi)^{d/2}(detLambda)^{-1/2}.
]

It then states that (Z_A) is independent of (O), since (Lambda) is
fixed, and is known whenever the spectrum is public. Public spectrum is a
condition of this **knowledge assertion**, not an assumption needed for the
determinant identity or the mathematical value of the normalizer.

These levels must remain distinct:

| Level | Mathematical meaning and source status |
|---|---|
| Actual determinant/product | The algebraic identity above follows from the actual S4.E11 precision construction. |
| Formula scalar | The positive real expression ((2pi)^{d/2}(prod_ilambda_i)^{-1/2}); giving this scalar a name does not itself evaluate an integral. |
| Unweighted Gaussian integral | (int_{mathbb R^d}exp(-x^	op A x/2),dx=Z_A). C.4 explicitly invokes Gaussian integration, but does not itself print this integral or name its reference measure. The unweighted Euclidean Lebesgue interpretation is a mathematical convention inferred from the potential, target and displayed normalizer. |
| Known normalizer | The explicit conditional statement: the normalizer is known whenever the fixed spectrum is public. This requires no recovery of the hidden eigenbasis. |
| Actual density | Under the Euclidean convention, (p_A(x)=Z_A^{-1}exp(-x^	op A x/2)). This density formula is an inference from the source Gaussian convention, not a separately printed C.4 formula. Its quadratic factor generally depends on (O). |
| Full C.4 | Also includes admissibility, (C^infty) regularity, Hessian (A), strong convexity, smoothness and unique minimizer 0. |
| Main lower bound | A separate statistical/oracle conclusion with additional (delta,arepsilon,d_0) and (kappa)-range restrictions. |

In particular, determinant invariance alone does not evaluate the actual
integral; a closed-form scalar definition alone does not prove it is that
integral. No Gaussian probability reference measure or Haar expectation may
replace unweighted (dx) while retaining the same displayed normalizer.

The source's fractional powers are ordinary real powers on positive bases.
In ((2pi)^{d/2}), (d/2) is real division and may be half-integral; it is
not integer truncation. The exponent (-1/2) is real, so for the positive
determinants here it means reciprocal positive square root. Positivity follows
from the construction and is not an independent mathematical restriction.

## Source context kept outside the bounded component

Lemma 4.6 says universally that (I_dpreceq OLambda O^	oppreceqkappa I_d).
C.4 proves this, then shows the potential has Hessian (A), is 1-strongly
convex and (kappa)-smooth, and has unique minimizer 0. A determinant-only
result supplies none of those whole-proof completion claims on its own.

Theorem 4.1 fixes (deltain(0,1)), has a threshold (d_0(delta)), assumes
(dge d_0(delta)), (2lekappale d^{1-delta}), and
(0<arepsilonle1/10), then lower-bounds query complexity by
(deltasqrtkappalog(d)/256). Those restrictions and that query conclusion
are contextual only. No local determinant theorem can be counted as that
lower bound or as the full Appendix C.4 proof.

## Exposure boundary

Before this freeze, the reviewer read only the assignment, the listed
repository process instructions and the one pinned primary HTML source.
No candidate Lean, test, statement seal, prepared source card, lesson, prose,
publication record, semantic audit, anonymous decoder packet, source graph,
other review, earlier verdict or current frontier was inspected. The exact
read/query ranges, wider initially requested source windows, and resulting
truncation limits are recorded in `exposure-log.json`. The seven canonical
slots are independently recorded in `semantic-slots.json`.

This is a raw-source contract freeze, not an implementation review, an API
recommendation, a source-fidelity verdict, or a source-proof-graph approval.
Phase 2 requires a separately authorized selective anonymous statement,
approved definitions and genuine blind reconstruction, followed by its own
freeze before full code/prose/critical ancestry exposure.
