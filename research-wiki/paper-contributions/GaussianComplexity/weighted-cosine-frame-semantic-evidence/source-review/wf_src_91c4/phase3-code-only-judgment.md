# Phase 3 — exact whole-module code-only judgment

Reviewer `/root/weighted_frame_fresh_source_91c4`. This phase preserves the independently frozen raw-source and type-only phases. Its principal input is `code-only-inputs/input-manifest.json`, SHA-256 `e538521091bb7c1dcf70b36d4c779ff8f4096904525f1ad3ec0f56cfce120f3a`, and its nine hash-verified source copies. No compiler/kernel receipts, existing source graph or TC reports, proof history, decoder, publication packet, or previous external verdicts were opened. No compilation was performed.

## Bounded result and limits

I found no source-semantic blocker in the inspected producer or private consumer code. Both complete new modules preserve the previously reviewed signatures, exact feature definitions, tensor order, source parameter range, ordinary matrix square, inclusive cutoff, constants, and canonical-marginal boundary. The proof text supplies its mathematical ingredients internally and materially uses the stated canonical parents. There is no replacement public norm theorem or new public individual-moment bound.

This is a code-only mathematical/semantic review of exact source text, not compiler or kernel verification and not source-VERIFIED/publication status. The implementation-use inventory created in this phase is inferred from actual code uses; it is not a compiler-derived declaration graph. The independently reconstructed original source reasoning remains the separate phase-1 inventory.

The remaining mathematical scope boundary is the original experiment: the private consumer establishes canonical single-row marginal integrals. It neither realizes the original independent row family nor proves its marginal-law/expectation transport, and it proves no centered variance or concentration theorem. Those are not missing steps in its stated canonical theorem; they remain obligations for any broader original-experiment claim.

## Whole-module interface and exposure check

The producer copy is 4647 bytes, SHA-256 `fbdd52b69919b02d1009b642fbf4975618689b10f417d1311fb766d23e87f5ce`. It has exactly one top-level public theorem, `actual_weighted_cosine_coefficient_bound`. It imports the canonical cosine Gram module, matrix order, and Kronecker algebra. Its only proof premise is `hq : 2*q+1<d`, with implicit natural-number parameters `d,q`; there are no preceding scoped mathematical variables, local instances, axioms, opaque declarations, custom syntax/macros, or unshown helper declarations in the complete module. `autoImplicit false` is set; `noncomputable section` and the BigOperators/L2Operator scopes do not add hypotheses.

The consumer copy is 9372 bytes, SHA-256 `50283ee15678aa6f3ebadd89ce10b69a5bf2404e0e2ad8fb9d242181e74739a4`. It has exactly one top-level declaration, the private theorem `actual_uncentered_second_moment_sum_bound`. It imports the producer, canonical radial fourth-moment module, and convex integral theorem. The complete module likewise has no extra scoped mathematical variables, local instances, custom notation, axioms, or concealed top-level helpers; it sets `autoImplicit false`. Namespace `open` commands select names and do not import premises.

I compared both actual statement substrings with the exact phase-2 signatures after removing only whitespace; both are identical. The private status is now visible in actual code. All subsequent helper objects and propositions in each proof are local `let`/`have` declarations, not new public interfaces or signature assumptions. No `axiom`, `sorry`, `admit`, `unsafe`, fake `True` closure, or assumption restatement closes either inspected proof text. This text inspection does not replace a kernel/axiom audit.

## Producer: actual content and parent use

The producer calls `FixedSpectrumCosineGram.actual_cosine_frame_gram` at source-copy line 40. It extracts both required conclusions: the feature norm estimate through `frame.2.2` (lines 41–42) and the unweighted Gram identity through `frame.1` (lines 43–51). These are actual uses, not imports or name references alone. It does not rely on the parent's weighted zero-Gram conclusion, although that conclusion is in the same returned conjunction.

The parent theorem's full source copy was read. It has exactly the same midpoint grid, constant-coordinate case, nonconstant `sqrt(2)` scaling, source range, and finite matrix dimensions. Its norm conclusion is `sum_k t_ik^2 <= 2*(q+1)` over the reals. Its proof derives the norm internally from `cos^2<=1`, counts the constant coordinate separately, and handles `Fin(q+1)` by `Fin.sum_univ_succ`. Its Gram proof uses the canonical exact grid-alias theorem, then product-to-sum, with zero and nonzero feature coordinates explicitly distinguished. The alias provider's full code was also read: it computes the literal grid sum for every integer frequency with dimension premise `2<=d`, not an assumed cancellation witness. The source range supplies that dimension premise.

In the producer, the literal feature outer products are summed entrywise to turn `t^T t=d I_r` into `sum_i feature_i=d I_r`. A linear Kronecker map sends this to

\[
\sum_i K_i=dI_{r^2},\qquad K_i=I_r\otimes t_it_i^T.
\]

Each `K_i` is proved positive semidefinite using the real rank-one outer-product theorem and the canonical Kronecker PSD theorem (lines 62–65). With `S_i=||t_i||^2` and `alpha=(r+2)/d^2`, the actual positive residual is

\[
\alpha\sum_i(2r-S_i)K_i.
\]

The norm bound makes every scalar weight nonnegative; `alpha>=0` is established internally. The code identifies this residual with `C I-alpha sum_i S_i K_i`, where `C=2r(r+2)/d`. The only cancellation by `d` explicitly derives `d!=0` from `hq` at line 82. Thus neither the norm estimate, Gram identity, nor positivity is being supplied as a hidden public premise. The local matrix name `B` denotes the weighted square coefficient matrix, not the paper's rectangular random `B`.

The read Kronecker background confirms paired indices and factor order, bilinearity, `I tensor I=I`, and the ordinary product rule. The read PSD background confirms rank-one, nonnegative scaling, finite-sum, addition, and Kronecker positivity. All are mathematical dependency uses inside the proof.

## Consumer: exact square, integrability, and aggregate residual

The consumer's `weighted(x)=R(x) G(x)` is exactly the canonical radial fourth-moment integrand. At lines 63–64 it applies `actual_radial_fourth_moment_matrix` and explicitly changes the resulting conjunction to

\[
\operatorname{Integrable}(RG,\mu)
\quad\land\quad\int RG\,d\mu=(r+2)I_r.
\]

Both conjuncts are materially consumed: integrability supplies all linear images and all subsequent integral interchanges; the equality evaluates each untruncated moment. The full canonical radial-moment module was read. It proves its own matrix integrability by a fourth-norm domination argument and finite-coordinate/continuous-linear transport. It derives off-diagonal zero by a coordinate reflection preserving the canonical Gaussian law and radius. It transports diagonal entries to independent scalar Gaussian coordinates, expands the radius, evaluates the diagonal fourth moment and mixed second-moment products, and obtains `3+(r-1)=r+2`. The scalar fourth-moment provider's full module was read: it proves `E X^4=3v^2` from the Gaussian moment-generating function. None of these moment values or integrability results is an additional consumer binder.

The code defines the continuous linear map

\[
T_i(A)={S_i\over d^2}(A\otimes t_it_i^T),\qquad
W_i(x)=T_i(R(x)G(x)).
\]

Every `W_i` is integrable by that map applied to the parent's integrable `RG` (lines 59–66). This is a genuine matrix-valued linear image; no entrywise-product expectation is confused with a product of expectations.

The rank-one ordinary-square identity is proved explicitly at lines 72–84 by finite matrix multiplication. `G(x)^2=R(x)G(x)` uses the Euclidean norm-square sum, and `feature_i^2=S_i feature_i` uses its actual coordinates. The Kronecker multiplication identity, both copies of the internal `1/d` scaling, and an on/off cutoff split then establish (lines 85–102)

\[
y_i(x)y_i(x)=\mathbf1_{\{R(x)\le L\}}W_i(x).
\]

The result keeps exactly one indicator and the coefficient `R(x)S_i/d^2`. It is ordinary matrix multiplication throughout, not entrywise squaring. The good set is proved measurable from the continuous radius. Each squared summand is then proved integrable using the integrable `W_i` and its measurable indicator, and this is the explicit first conjunct returned by the theorem. The proof therefore does not exploit the Bochner integral's nonintegrable zero branch.

`W_i(x)` is proved PSD directly as a nonnegative multiple of `vv^T`, with `v_(a,j)=x_a(t_i)_j` and multiplier `(S_i/d^2)R(x)` (lines 106–118). Consequently the entire pointwise residual `sum_i W_i(x)-sum_i y_i(x)^2` is PSD, by a finite sum and an inclusive cutoff split (lines 121–129). The common variable `x` is legitimate for this sum of separate canonical marginal integrals; it is not an asserted joint independent-row realization.

The code proves integrability of both finite sums and hence of their difference. It proves that the real PSD cone is closed by Hermitian symmetry and all quadratic-form inequalities, and convex by nonnegative scalar multiplication and addition (lines 134–148). The supplied pinned `Convex.integral_mem` statement was checked: it requires a probability measure, complete normed real space, closed convex target, almost-everywhere membership, and integrability. Here these are the canonical Gaussian probability measure, finite real matrix space, the established cone properties, pointwise residual positivity, and established integrability. No normalized cutoff measure or retained-probability factor enters.

Thus the actual integrated residual is

\[
\int\Bigl(\sum_iW_i-\sum_i y_i^2\Bigr)d\mu\succeq0.
\]

Every integral rewrite has its required integrability supplied: continuous-linear commutation uses the parent's first conjunct; evaluation of `int W_i` uses its second conjunct; sum/integral and subtraction use the established `W_i` and squared-summand integrability. The resulting residual is `B-sum_i int y_i^2`, with the same literal `B=alpha sum_i S_i K_i` as in the producer.

Finally the producer is actually invoked at line 173, changed to `C I-B >=_PSD 0`, and added to this integrated residual. The final `abel` only cancels `B` in an additive matrix identity. It does not create an estimate or replace a moment theorem. The resulting conclusion is exactly `C I-sum_i int y_i^2 >=_PSD 0`, together with every individual integrability assertion.

## Source reasoning versus implementation dependency information

The independently frozen source reasoning is: Fact C.5 supplies the deterministic norm and Gram identities; Ex113 supplies the Gaussian radial fourth moment; Ex114 computes an individual ordinary square; positivity permits indicator dropping; EGx11 sums, applies the deterministic feature bound, and collapses the Gram sum.

The code realizes the same bounded mathematics by two explicitly visible routes: a deterministic PSD residual from the canonical frame theorem, and an integrated aggregate PSD residual from the canonical radial moment and exact indicator-square identity. Its closure/convexity proof is an implementation of finite-dimensional order-under-expectation, not an extra source hypothesis. Its Gram parent reuses the stronger exact grid-alias theorem associated with source C.3, rather than literally repeating C.2's direct telescoping calculation. This is a compatible reusable implementation route, not evidence that the original author depended on C.3. Its scalar fourth-moment provider uses an MGF calculation, while the original p14 simply quotes the standard Gaussian fourth moments. Neither implementation route should be retroactively inserted as author-source proof topology.

`phase3-implementation-use-inventory.json` records these observed use sites and meanings. Imports are listed separately from actual calls. It does not certify elaboration reachability, implicit/simplifier dependencies, or kernel proof terms. Those require later compilation/kernel/declaration evidence and must remain separate from the raw source graph.

## Endpoints, constants, and remaining gaps

The source range remains precisely natural `q>=0` and `2q+1<d`. It supplies `d>=2`, so all source divisions are meaningful. Nothing adds `q>0`, `tau<=1/2`, an event, or a norm/Gram/moment premise. With `q=0`, every feature and tensor coordinate set is a singleton; the parent norm proof retains the constant feature, the radial moment is `3`, the weighted coefficient matrix is `3/d`, and the stated loose upper coefficient remains `6/d`. The consumer reduces to an integrable scalar cutoff fourth moment scaled by `1/d^2`. There is no zero-cardinality loophole or loss of the constant feature.

No in-scope semantic repair is requested from this code-only phase. The outstanding review/evidence boundaries are: (1) no compiler/kernel or actual elaborated declaration graph has been examined; (2) no blind reconstruction or anti-anchored final packet has been examined; (3) original-family row-law/expectation transport, joint independence use, centering, and concentration are outside the current theorem; and (4) the private Tests declaration is a material consumer, not an independently public source result. This record grants no process permission and no whole-paper/source completion status.
