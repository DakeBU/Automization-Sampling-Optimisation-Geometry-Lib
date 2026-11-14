# Raw-source interpretation — phase 1, frozen before Lean exposure

Reviewer: `/root/weighted_frame_fresh_source_91c4`. This is an independent source-reading record, not a mathematical completion, implementation review, statement approval, process permission, or source-fidelity verdict. No proposed Lean signature, definition context, implementation, decoder reconstruction, old audit, or source-graph report was available in this phase.

## Pinned source and scope

The original is *On Complexity of Gaussian Sampling*, arXiv 2610.20492v1, in `.astis/huanjian-resume-20261103/2610.20492v1.html`: 951991 bytes, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The central source location is Appendix C.2, HTML paragraph `A3.SS2.p14`, especially displays `A3.Ex113`, `A3.Ex114`, and equation group `A3.EGx11` (children `A3.Ex115`–`A3.Ex117`). Here “p14” is the HTML paragraph identifier; this review did not inspect a paginated PDF or independently establish a PDF page number.

I read all of original Appendix C.2, HTML lines 3313–3836, and the necessary original standing material at lines 1080–1107 and 1144–1240. The bounded verbatim HTML and math-alttext display extracts are preserved alongside this record. The scope is the deterministic cosine-feature coefficient comparison used in EGx11 and the sum of the individual, uncentered, truncated second moments in that group. Later centered-variance, concentration, bias, and final Krylov conclusions are context, not conclusions awarded to this scope.

## Objects, parameters, and standing experiment

The hard family starts with integer dimension `d >= 2` and `kappa >= 2`. Its deterministic angles and eigenvalues are

\[
\theta_i=(i-\tfrac12)\pi/d,\quad
\lambda_i=(\kappa+1)/2+(\kappa-1)\cos\theta_i/2,
\quad 1\le i\le d.
\]

`Lambda` is the diagonal matrix of those eigenvalues. The source draws a Haar orthogonal `O` independently of the algorithm's private randomness and sets `A = O Lambda O^T`. This rotation and the target law are contextual; neither is an input to the EGx11 moment calculation.

The relevant query budget is an integer `q >= 0` with `2q+1 < d` (integer status is explicit in Lemma 4.3 and also inherent in the finite degree/query indexing). Put `r=q+1` and `n=2q+1`, so `r>=1`, `d>=2`, and `2r<=d`. Lemma 4.4 uses independent `g_1,...,g_r ~ N(0,I_d)`. Appendix C.2 groups their coordinates as

\[
\gamma_i=((g_1)_i,\ldots,(g_r)_i)^T\in\mathbb R^r,
\qquad
t_i=(1,\sqrt2\cos\theta_i,\ldots,\sqrt2\cos(q\theta_i))^T\in\mathbb R^r.
\]

The `gamma_i` are independent `N(0,I_r)` vectors. The `t_i` are deterministic. The source does not require the `g_a` or a representation coefficient vector to be independent of the entire extended algorithm experiment. In particular, the preceding paragraph after Lemma 4.3 explicitly allows the polynomial coefficients to depend on the entire extended experiment. No such additional independence belongs to the moment-bound statement.

The first feature coordinate is indexed by `j=0` and is exactly `1`. For `1<=j<=q`, the coordinate is `sqrt(2) cos(j theta_i)`. It is not the same formula with `sqrt(2)` at `j=0`.

`B` has dimensions `d x r^2`, with row `i` equal to `d^(-1/2) (gamma_i tensor t_i)^T`. Its range is the block Krylov space spanned by `Lambda^j g_a`, `1<=a<=r`, `0<=j<=q`. The source's `D_n` is the `d x d` diagonal matrix with entries `cos(n theta_i)`. These explain the context but no high-frequency factor `cos(n theta_i)` occurs in EGx11 itself.

## Tensor indexing, matrices, and senses

Use paired tensor coordinates `(a,j)` with Gaussian coordinate `a` first (`1<=a<=r`) and feature coordinate `j` second (`0<=j<=q`). Then

\[
(\gamma_i\otimes t_i)_{(a,j)}=(\gamma_i)_a(t_i)_j,
\]
\[
(\gamma_i\gamma_i^T\otimes t_it_i^T)_{(a,j),(b,k)}
=(\gamma_i)_a(\gamma_i)_b(t_i)_j(t_i)_k.
\]

This factor order is specified by the original formula. A conventional lexicographic flattening makes `j` the inner index; the source does not separately specify a zero-based linear flattening function. A consistent permutation of paired coordinates is a change of presentation, not an opportunity to exchange the two meanings silently. `I_r tensor t_i t_i^T` has entry `delta_ab (t_i)_j(t_i)_k`, and all the moment/comparison matrices in EGx11 are real `r^2 x r^2` matrices. `I_{r^2}` is identity on this paired coordinate set.

All transposes are ordinary real transposes. `M^2` is the ordinary matrix product `M M`, including its sum over the internal paired coordinate. It is neither entrywise/Hadamard squaring nor the scalar squared operator norm. The order `M preceq N` is the real self-adjoint Loewner order: `c^T M c <= c^T N c` for every real deterministic coefficient vector `c` of length `r^2`.

Expectations of matrices are entrywise (equivalently any compatible finite-dimensional matrix-valued integral). The relevant entries are integrable: after expansion they are bounded in absolute value by finite deterministic multiples of Gaussian polynomials of degree at most four. The source does not state integrability as an extra premise; it follows from the specified Gaussian law. The integral/order interchange requires this ordinary finite-moment justification, not a new theorem assumption.

## Truncation and exact source displays

The source fixes

\[
R_i=\|\gamma_i\|^2,\qquad L=2r+3\log(1000d),\qquad
Y_i={1\over d}(\gamma_i\gamma_i^T\otimes t_it_i^T)
\mathbf1_{\{R_i\le L\}}.
\]

The cutoff is inclusive (`<=`), and the source logarithm is the natural logarithm used in the displayed exponential-tail calculation. `Y_i` is positive semidefinite and self-adjoint. The same threshold `L` is used for every row. The result being reconstructed retains this source value of `L`; the proof's indicator-dropping argument happens not to use its numerical value. That observation is not a substituted source definition.

Ex113 says exactly

\[
\mathbb E[R_i\gamma_i\gamma_i^T]=(r+2)I_r.
\]

The source explains that off-diagonal entries vanish by sign symmetry, while a diagonal entry is `3+(r-1)=r+2`. This uses the fourth moment `E G^4=3` and the products `E G_a^2 G_b^2=1` for distinct independent standard Gaussian coordinates, with zero off-diagonal odd products. The constant is exactly `r+2`.

Using `(gamma gamma^T)^2=R gamma gamma^T`, `(t t^T)^2=||t||^2 t t^T`, the product rule for Kronecker matrices, and idempotence of the indicator, Ex114 says

\[
Y_i^2={R_i\|t_i\|^2\over d^2}
(\gamma_i\gamma_i^T\otimes t_it_i^T)
\mathbf1_{\{R_i\le L\}}.
\]

Dropping this indicator increases the positive semidefinite matrix pointwise. EGx11 is the following exact chain:

\[
\sum_{i=1}^d\mathbb E[Y_i^2]
\preceq {r+2\over d^2}\sum_{i=1}^d\|t_i\|^2(I_r\otimes t_it_i^T)
\preceq {2r(r+2)\over d^2}
\left(I_r\otimes\sum_{i=1}^dt_it_i^T\right)
= {2r(r+2)\over d}I_{r^2}.
\]

The bound is deterministic and holds for these matrices under the Gaussian experiment; it is not an event with a failure probability. The numerical coefficient is exact as written and need not be sharp.

The left side is the **sum of expectations of individual ordinary squares**. It is not `E[(sum_i Y_i)^2]`, `(sum_i E[Y_i])^2`, `sum_i (E[Y_i])^2`, a centered covariance, or the moment of a Gram deviation. No cross-row product appears here. Consequently independence between distinct rows is part of the original experiment but is not required just to establish this sum-of-marginals bound. In the next source display, `Z_i=Y_i-EY_i` is used to compare centered second moments to these uncentered ones; that is a further statement, not a meaning assigned to the present left side.

## Deterministic coefficient form and ingredients

Fact C.5 supplies the two deterministic inputs actually invoked at the end of p14:

\[
\|t_i\|^2=1+2\sum_{j=1}^q\cos^2(j\theta_i)\le1+2q\le2r,
\qquad \sum_{i=1}^dt_it_i^T=dI_r.
\]

The Gram identity is proved in the source by the midpoint-grid cosine sum `sum_i cos(k theta_i)=0` for integer `0<|k|<2d`, followed by product-to-sum for the nonconstant feature coordinates, with the constant coordinate handled separately. The grid cancellation itself follows from a telescoping sine sum and nonvanishing `sin(k pi/(2d))`. These are proof ingredients to discharge, not extra source hypotheses to request.

To make the coefficient meaning unambiguous independently of a later formal representation, write a deterministic vector as coefficients `c_(a,j)` and define `h_a(i)=sum_(j=0)^q c_(a,j) (t_i)_j`. Then the Gram identity is equivalently

\[
\sum_{i=1}^d\sum_{a=1}^r h_a(i)^2
=d\sum_{a=1}^r\sum_{j=0}^q c_{(a,j)}^2.
\]

The deterministic weighted-cosine comparison used in EGx11 is equivalently

\[
{r+2\over d^2}\sum_{i=1}^d\|t_i\|^2\sum_{a=1}^r h_a(i)^2
\le {2r(r+2)\over d}\sum_{a=1}^r\sum_{j=0}^q c_{(a,j)}^2.
\]

This is a coefficient expansion of the second comparison in EGx11, not a separately numbered source theorem. The weights here are `||t_i||^2`; the cosine features are inside `h_a(i)`. A multiplier `cos(n theta_i)` would change this particular quantity. If one presents the scalar inequality with the common factor `(r+2)/d^2` removed, the comparison is `sum_i ||t_i||^2 sum_a h_a(i)^2 <= 2rd sum_(a,j)c_(a,j)^2`.

For the first comparison, the same coefficient expansion has `c^T Y_i^2 c = d^(-2) R_i ||t_i||^2 (sum_a (gamma_i)_a h_a(i))^2 1_(R_i<=L)`. The source fourth-moment identity gives `E[R_i (sum_a (gamma_i)_a h_a(i))^2]=(r+2)sum_a h_a(i)^2`, after dropping the indicator by nonnegativity. This records the mathematical bridge between ordinary matrix multiplication, scalar integrals, and the displayed Loewner estimate. It does not allow a random experiment-dependent coefficient vector to be pulled outside an expectation.

The determinant, `kappa`, Haar rotation, range equality, weighted zero Gram identity, truncation tail probability, bias scalar `a`, centering identity, matrix Bernstein, `tau`, and its smallness condition are not mathematical inputs to this bounded second-moment comparison. They have other roles in the surrounding argument. In particular `tau<=1/2` must not become a new premise here. The standing `2q+1<d` is the source range; weaker ranges sufficient for particular deterministic identities would be explicitly labelled generalizations, not silently substituted for it.

## Endpoint q=0

The source permits `q=0`. Then `r=1`, `n=1`, `d>=2`, `t_i=(1)`, and `gamma_i` is a single standard normal. The nonconstant-feature sum is empty; the Gram identity is `sum_i 1=d`. Here `||t_i||^2=1<=2r=2`. Ex113 is `E[gamma_i^4]=3`. `Y_i` is the scalar `gamma_i^2/d` times the inclusive cutoff indicator, and its ordinary square is `gamma_i^4/d^2` times the same indicator. The chain gives `sum_i E[Y_i^2]<=3/d<=6/d`, and the final source constant is `2r(r+2)/d=6/d`. All paired coefficient indexing has one coordinate. No positive-`q` premise, missing constant feature, or division by `q` is justified.

## Original experiment versus canonical marginal integral

The original left side uses the actual row variables `gamma_i` derived from `g_1,...,g_r`. Each row has the specified standard Gaussian law on `R^r`. One may calculate each individual expectation using a canonical variable `x~N(0,I_r)` and the deterministic function

\[
y_i(x)={1\over d}(xx^T\otimes t_it_i^T)
\mathbf1_{\{\|x\|^2\le L\}}.
\]

Thus `E_original[Y_i^2]=integral y_i(x)^2 dN(0,I_r)(x)` for every `i`, by equality of marginal laws and the integrability noted above. Summing those identities recovers the source quantity. A representation using the same integration variable `x` for every `i` computes a sum of marginal integrals; it does not represent the joint independent row experiment. No independence inference may be drawn from that canonical one-variable notation, and it cannot justify cross-row products or concentration by itself. Conversely, a theorem giving only canonical marginal integrals needs an explicit marginal-law transport to identify it with the original source expectation if original-experiment fidelity is claimed.

## Coverage and open review boundary

The bounded source ingredients are: original angle/feature definitions; Gaussian row law; source cutoff and truncated outer-product definition; Fact C.5 norm and Gram identities with their source derivation; Ex113 and its fourth-moment explanation; Ex114 with ordinary-square/rank-one algebra; p14 indicator dropping, both order comparisons and their constants. The exact raw inventory is in `source-inventory.json`.

This phase has reconstructed those meanings without seeing any proposed mathematical interface. It has not decided whether any current theorem or module realizes them, whether current code transports canonical marginal integrals, whether any hidden premise exists, or whether any publication/source graph is complete. Those questions remain for separately frozen later phases.
