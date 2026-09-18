# Actual stopped proximal queries — Algorithm D.2 / Lemma D.3

Issue #311; cell `ASTIS-SW-SPHMC-approximate-proximal-execution`.
Status: PROVED_LOCAL with focused compilation, authored lessons, publication
bindings and independent encoder-denoiser source review. Commit-bound VERIFIED,
serialized root/site integration and aggregate acceptance remain pending. Root
is the unique Lean writer; construction is not an extra mathematical theorem.

## Pinned source and target

[Chen–Chewi–Lu–Zhang, arXiv:2609.06906v1, Appendix D.2](https://arxiv.org/html/2609.06906v1#A4.SS2), Algorithm D.2 and Lemma D.3 (D.5)–(D.6).
Authored restatement, not a quotation. E is a finite-dimensional complete real
inner-product space with its Borel structure; V is C2, kappa>=1, and its genuine
Hessian lies between kappa^-1 I and I. Keep 0<eta<=c0<1 and epsilon>0.

For every center y define

\[
T_y(x)=y-\eta\nabla V(x),\qquad x_n(y)=T_y^{[n]}(y),
\quad\tau(y)=\min\{n:\|x_{n+1}(y)-x_n(y)\|\le(1-\eta)\varepsilon\}.
\]

Prove the set is nonempty, tau and x_tau are measurable, the fixed point p(y)
uniquely minimizes V(x)+norm(x-y)^2/(2 eta), and norm(x_tau-p)<=epsilon.
Return **x_tau**, not x_(tau+1). A trace/recurrence must justify **tau+1**
gradient evaluations, including the final residual test; a name for this count
is not a verified evaluator. Exact-real comparison/arithmetic is the source
oracle model; do not claim machine floating-point implementation.

With R=norm(gradient V(y))/epsilon and a=-log(c0)>0, a proposed explicit bound is

\[
\tau(y)+1\le 1+\left\lceil\frac{\log(1+R/(1-c_0))}{a}\right\rceil_{\mathbb N}
\le C_{c_0}[1+\log(1+R)],
\qquad C_{c_0}=2+\frac{1+\log((1-c_0)^{-1})}{-\log c_0}.
\]

This constant is an ASTIS derivation of the source's existential C_c0, not a
constant printed in the source. R=0 stops immediately but still costs one query.

## Seven-step route and reuse

1. Derive gradient Lipschitz and strong convexity from the true Hessian through
   `QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic`.
2. Construct the eta-contraction fixed point with Mathlib `ContractingWith`;
   identify the proximal equation and genuine unique minimum with canonical
   `StrongConvexFirstOrder` / `QuadraticRegularizationFirstOrder` APIs.
3. `LipschitzWith.dist_iterate_succ_le_geometric` gives residual<=eta^(n+1)*norm(grad V(y)).
4. Prove the displayed logarithmic bound, then first-hit existence/minimality.
5. `ContractingWith.dist_le_of_fixedPoint` gives residual/(1-eta) error.
6. Iterates are measurable in y; use `measurable_find` and `Measurable.find` for
   the first-hit and returned output. No measurability hypothesis on that output.
7. Bind actual gradient-only recurrence/checks to tau+1 and test degenerate and
   nontrivial centers. Do not count value queries or assume a proximal oracle.

Planned module/name:
`AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/ApproximateProximalExecution.lean`,
namespace `AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution`,
principal theorem `approximate_proximal_execution`;
test `Tests.SmoothedPicardHMCApproximateProximalExecution`.
Imports should remain bounded to the actual quadratic/first-order and
contraction/measurable-selection/log APIs; public helper proliferation is not needed.

## Alternatives checked and not silently substituted

- `GradientDescentComplexity.distance_le_of_log_bound` uses inverse smoothness
  step on the regularized objective. Algorithm D.2 uses eta, not that step.
- `TerminalReferenceGradientDescent` / `ReferenceCarryingKernel` contain useful
  first-hit examples but solve different iteration/threshold problems.
- Existing proximal-estimator constructor only exposes eta<=1/2. Do not inherit
  this stricter range when the contraction directly covers full eta<c0<1.
- SPHMC sharp bias still lacks standardized-RGO transport, transport/Fisher and
  smoothed-score identification; centered MGF still needs genuine Gaussian
  Lipschitz concentration. Bounded-variable Hoeffding is not applicable.
- PBPS local L2 is now merged. Mathlib Sobolev is a complex tempered-distribution
  API; it does not directly give weighted local H2 for the current weak PDE.

## Consumers and strict boundary

Paper consumers: D.1 approximate-query interface, D.4 expected work, gradient-only
Theorem 5.1. All are planned source consumers, not current compiled callers.
Focused tests must exercise the actual stopped output and count, not merely a
supplied accuracy assumption. Independent source-blind/source review is required.
No expected total work, Picard moment control, sampling error, bias/MGF or full
paper completion follows. Existing proofs and Chewi frontier remain untouched.

Read-only independent scout: `next_frontier_scout`, September 18. Source/APIs
checked at main bbd66fd1, Mathlib db584cd6, Lean4.33.0. This is planning evidence,
not theorem verification or a source-equivalence certificate.

## Local checkpoint — 2026-09-18

`lake build Tests.SmoothedPicardHMCApproximateProximalExecution` passed (3252
build jobs). The principal theorem uses only `propext`, `Classical.choice`, and
`Quot.sound`. Focused tests cover empty fuel, immediate success, current-iterate
return with three queries, exhausted fuel, and a genuine potential at eta=3/4.
The result includes a unique proximal minimizer with quadratic growth,
measurable first hit and stopped output, epsilon accuracy, and the explicit
pointwise logarithmic query bound above.

`proximal_execution_proof_review` independently inspected the source, module and
tests without editing or building. No mathematical blocker was found. This is
not source-blind review or VERIFIED admission. Exact module SHA256:
`01d2b711a9916dddfef0a07325f9ce333170a32d5d6f069117a859cd4d174ed5`;
test SHA256:
`b20a10e208b06b4dff5042347f4b20f13a09a59503248ac12b61da95c0d9bfae`.

The interpreter is noncomputable exact-real finite-fuel semantics. It records
the returned point and query count, not a query-list trace; the theorem proves
successful execution at fuel N+1, not a separate arbitrary-excess-fuel theorem.
Neither pointwise work nor measurable output proves D.4 expected run-wide work.
Registry stays at 438 until the serialized admission/integration gates pass.
Latest main e2f88b3e was fetched and is already contained in this branch;
the six collaborator-entry documents were reread. No collaborator modification
or old Chewi frontier was changed.

Reader checkpoint: two declaration lessons are now authored in
`website/content/declaration_lessons/sphmc-approximate-proximal-execution.json`.
The native lesson loader passes (364 units), Frontier Cell check passes (129
cells), and `git diff --check` passes. Contributor admission intentionally still
fails: private implementation needs a fresh accepted whole-module public theorem
review. Next finish publication bindings, compiler-elaborated anonymous decoder
input, fresh independent decoding and source review; only then request admission
and serialized site/root integration. No site rendering or visual acceptance is
claimed for these newly authored units yet.

## Source-review admission checkpoint — 2026-09-18

Both public declarations now have separate publication bindings and audits:
`ASTIS-RT-20260918-ProximalExecution` and
`ASTIS-RT-20260918-ProximalQueryInterpreter`. Fresh anonymous compiler-derived
packets were decoded by `blind_20260918_d`; `source_review_20260918_d` then checked
fresh anti-anchored packets, primary source and complete module independently.
The theorem review explicitly compares the attributed expanded contract, not
an assertion that extra measurability/uniqueness conclusions were printed in D.3.
The construction review gives no accuracy or eventual-success credit by itself.

Semantic gate passes (124 audits); publication diff gate passes (97 source
items), including all four private implementation helpers; contributor diff
gate passes (2 declarations, 2 cells). Frontier Cell check passed at 130 cells.
SAU `ASTIS-20260918-ApproximateProximalExecution` is PROVED_LOCAL via its real
publication gate. No root import, Registry update, website build/visual acceptance,
deployment or commit-bound VERIFIED has occurred in this checkpoint. Registry
remains 438. Next obtain independent commit-bound verification, then serialize
integration and inspect the actual generated reader/graph before publication.
