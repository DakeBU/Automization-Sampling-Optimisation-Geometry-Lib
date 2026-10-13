# Four-paper phased formalization priority (2026-10-08)

The existing Goal was expanded without reset: phase1 PBPS2609.06905v1/SPHMC2609.06906v1 and actual-input composition; phase2 Gaussian Cloud2609.38710v1 with Section6 recursive requests/errors/caps/expectedqueries; phase3 midpoint2610.06308v1 with deterministic upper and deterministic/randomized lower bounds and finite-step initialization. Use current capsule/handoff and execution metadata. Later-paper shared facts may come first only to remove a current blocker; all older frontiers/cycles/memory remain. Local leaves do not complete any paper. Reader follows Chapter1.3 with exact folded Lean adjacent to full source restatements/proofs; no hidden higher-derivative premise or TV-to-unbounded-cost transfer.

The older dated planning records below are preserved as historical context; they do not reset the current Goal or set scheduling.

# SPHMC / Proximal BPS: source-first dependency plan

The user selected these papers as the first mathematical priority on 2026-09-10
and deleted the old app Goal before authorizing one new Goal. The canonical
scheduling contract is `execution` in the companion model below. Chewi 8.4.1
and all earlier cells/cycle memory remain preserved, with their original
integration and source-certification boundaries; they are not marked complete.

## Canonical records

- Source cases and theorem contracts: [companion model](../website/content/samplewiki_companion_frontiers.json).
- Contribution comparison and operator walkthrough: [proof deltas](../website/content/samplewiki_proof_deltas.json).
- Reusable conceptual families: [Graph Memory](../website/content/graph_memory_index.json).
- Candidate transport contracts: [Functor Hypergraph](../website/content/functor_hypergraph.json).

The immutable arXiv v1 sources are 2609.06906 (SPHMC) and 2609.06905 (PBPS).
The source-reading pass checked their main statements and selected interfaces;
it is not independent review or a complete audit of every appendix proof.
The 34-row upstream SampleWiki snapshot is preserved. These are two additional
source cases and one view of the already published composition theorem.

## Corrections to the exploratory conversation

1. Smooth the **density**: exp(-V_eta) = exp(-V) * Gaussian, not the potential.
2. Wp-based recursion provides a **proxy** Renyi certificate. The actual output
   is close to that proxy in TV; genuine Renyi output is a different contract.
3. PBPS analyzes a **discrete augmented chain** built from a harmonic half-turn
   and auxiliary reflection, not vanilla BPS or a continuously refreshed local
   process. It adapts DMS and the Fan–Li–Lu refinement, not their rates verbatim.
4. TV contraction transfers accuracy, not unbounded cost. The latter uses the
   implemented solver/event caps and uniform conditional expected RGO cost.
5. HighAccuracyEngine follows WarmStartGenerator; the reverse order is wrong.

## Implementation order once this lane is selected

The lane is now selected. First frozen cell:
`ASTIS-SW-SPHMC-recursive-condition-contraction`, the scalar calculation in
Lemma 6.6(i). Source constants are checked directly, not assumed as convergence.
See the per-paper conversion windows for the precise local/result boundary.
The two paper main results and their composition remain open. Citation, Lean
bundle download and topology-feature work follows correct mathematical packets.

The `next_packets` list in the companion model is authoritative. Start with
read-only reuse/API audits of TV handoff, quadratic RGO calculus or reflection.
Search exact existing declarations before proposing a new theorem. Freeze only
one minimal missing interface, with a source consumer, and keep normalization,
kernel measurability, moment control and representative choices explicit.

The scalar cost sum is not the mathematical bottleneck; its hypotheses are.
The reflection algebra is not a process-invariance theorem. Discrete modified-L2
coercivity is not interchangeable with a reversible Dirichlet gap.

For the proof-technology visualizer, preserve baseline technique, adaptation,
mathematical structure, exact source anchor, candidate shared parents, and
failure boundary. Novelty role and formal proof status are separate axes.
Do not manufacture graph centrality or call an unverified analogy a functor.

## Shared analytic bridge: Hessian lower bound to strong convexity

Primary source audit, 2026-09-10: both papers use `V in C^2(R^d)` and the
pointwise matrix bounds `alpha I <= Hessian V(x) <= beta I` in equation (1.1).
SPHMC Section 2 fixes this convention before its RGO calculus in Section 6.2.2.
The lower bound is interpreted directionally as

$$\alpha\|v\|^2\le D^2V(x)[v,v]\qquad\text{for every }x,v.$$

The selected shared analytic implication is the strong-convexity chord bound

$$V((1-t)x+ty)\le(1-t)V(x)+tV(y)
-\frac\alpha2t(1-t)\|x-y\|^2,\qquad 0\le t\le1.$$

Classification: `local-lemma` built from existing scalar convexity and
derivative-chain APIs. No ready multivariate adapter was found in the bounded
ASTIS/Mathlib audit. The compiled normed-space statement needs no measure,
finite-dimensionality, inner product, positivity of alpha, or upper Hessian
bound; those remain explicit assumptions where the paper's later consumers
need them. Its single-writer production proof and focused consumer tests pass;
exact independent-review and admission evidence lives in
`ASTIS-SHARED-hessian-strong-convexity` and its semantic audit.

Proof route: for `v=y-x`, subtract `alpha*norm(v)^2*t^2/2` from
`V(x+t*v)`. Genuine first and second derivative witnesses give a nonnegative
scalar second derivative. Apply Mathlib
`convexOn_of_hasDerivWithinAt2_nonneg`, then use the endpoint chord inequality
and rearrange the quadratic term. Preserve `ContDiff R 2 V`: a bare lower bound
on totalized `fderiv (fderiv V)` is not the same mathematical hypothesis.

The immediate consumer is the already compiled minimizer-free
`StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn`.
For positive alpha in finite-dimensional Euclidean space, their composition
now derives integrability of the actual source Gibbs weight in focused tests, with no
minimizer or finite-normalizer assumption added. Positive mass and the normalized
probability law are existing Mathlib consumers, not proposed new wrappers.
The upper-curvature update, density-defined joint augmentation, conditional
kernel, process invariance and sampling guarantees remain distinct obligations.

## Source integration: normalized PBPS joint Gibbs density

Source: PBPS v1 Section 2.2, equations (2.6)–(2.7). With C² potential $V$,
$\alpha>0$, $D^2V(x)[v,v]\ge\alpha\|v\|^2$ and $\eta>0$, set
$\mu=\mathrm{volume.tilted}(-V)$ and
$J=(\Phi_\eta)_\#(\mu\otimes\gamma)$, where
$\Phi_\eta(x,z)=(x,x+\sqrt\eta z)$. The single certificate concludes

$$0<Z_V,\qquad J\text{ is a probability measure},\qquad
J=(dx\,dy)\,\frac{(2\pi\eta)^{-d/2}}{Z_V}
\exp\!\left(-V(x)-\frac{\|y-x\|^2}{2\eta}\right),
\quad Z_V=\int e^{-V(x)}\,dx.$$

Statement audit: a bare density equality can hold for a zero totalized tilt
when the normalizer vanishes. The single conjunction explicitly excludes
both zero denominator and zero law; do not add wrapper siblings. Prove
integrability, positivity and probability internally from the compiled Hessian
and Gibbs parents. Then reuse the existing relative-input augmentation density,
`prod_withDensity_left`, `withDensity_mul` and exponential algebra. The source
upper Hessian bound and $\eta\le1/\beta$ are not needed for this density
identity, but remain requirements of their sampling consumers. Conditional
representatives/kernels, marginal curvature, process invariance and cost stay
separate. Independent Hessian source acceptance preceded this writer's work.
The production theorem and focused tests now pass (3134 jobs); the cell
`ASTIS-SW-PBPS-gibbs-augmentation` records independent source review, aggregate
integration and commit-bound admission separately. No zero-law fallback can
satisfy the explicit positive-normalizer/probability conjunction.

## Audited successor: actual RGO curvature and gradient smoothness

Read-only scout, 2026-09-10: SPHMC Lemma 6.4's analytic clause is a single
useful successor, not another scalar recurrence wrapper. Encode precision
$r=A^{-1}\ge0$ so that $A=\infty$ is the genuine case $r=0$. For C² $U$ on a
real Hilbert space, nonnegative $m,L,r$, and the everywhere diagonal sandwich
$m\|v\|^2\le D^2U(x)[v,v]\le L\|v\|^2$, set
$W(x)=U(x)+r\|x-u\|^2/2$. The proposed conclusion is both
`StrongConvexOn univ (m+r) W` and `LipschitzWith (L+r) (gradient W)`.
This packet is compiled and independently source-reviewed as
`ASTIS-SHARED-quadratic-regularization`; its cell retains admission status.

Local calculations should derive C² and the exact quadratic Hessian shift,
then invoke the compiled Hessian-to-chord theorem. For smoothness, use the
genuine derivative $T_x=(\mathrm{toDual})^{-1}\circ D^2W(x)$ of the gradient.
C² symmetry plus Mathlib `ContinuousLinearMap.norm_eq_iSup_rayleighQuotient`
gives its operator norm bound from the diagonal sandwich; finish with
`lipschitzWith_of_nnnorm_fderiv_le`. No finite-dimensional spectral theorem is
required, but completeness is explicit for the gradient/Riesz API. Candidate
imports are `Calculus.FDeriv.Symmetric`, `Calculus.Gradient.Basic`,
`Calculus.MeanValue` and `InnerProductSpace.Rayleigh`.

ASTIS `hessianOpNormOfSourceHessianField` assumes the norm bound and a genuine
representative; it does not establish this missing implication. Keep these
bridges local to one substantive analytic theorem if the APIs permit. Source
specialization $m=\kappa^{-1}$, $L=1$, $r=A^{-1}$ will provide the real RGO
potential's constants; (6.1)'s ratio algebra and recursive query/error claims
remain separate. This also serves PBPS (2.9)–(2.10), without granting its
conditional-kernel or Poincaré/covariance claims.

The exact two-conclusion theorem and focused tests pass with 2943 jobs;
independent direct elaboration also passes. Tests include source constants,
zero precision, zero dimension, positive Gibbs normalization and actual RGO
composition. `quadratic-regularization.json` contains the five-step reader proof.
The public output is not the local Hessian sandwich itself. Source review
accepts direct SPHMC clause coverage and only PBPS analytic-support provenance.

## Read-only successor audit: probability-law TV handoff

After the quadratic packet, a bounded ASTIS/Mathlib audit selects one missing
Markov-kernel contraction edge. No new probability-TV definition is required:
for probability measures $\mu,\nu$ and a genuine measurable Markov kernel $K$,

$$\bigl[\forall A\text{ measurable},\ |\mu(A)-\nu(A)|\le\delta\bigr]
\quad\Longrightarrow\quad
\forall B\text{ measurable},\ |(\mu K)(B)-(\nu K)(B)|\le\delta.$$

Use `Measure.real` for event probabilities and `K ∘ₘ μ` for actual kernel
composition. No density, coupling, standard-Borel space, or supplied
integral-contraction premise is needed. The exact factor is one. For each
measurable B, the measurable function $f(x)=K(x,B)$ lies in $[0,1]$. Pinned
Mathlib `Integrable.integral_eq_integral_Ioc_meas_le` rewrites its expectation
as the integral of superlevel-event probabilities over $(0,1]$. Apply the
eventwise input bound there and integrate over this length-one interval.
Boundedness supplies every real-integral integrability premise. The audit
found kernel composition and layer-cake APIs, but no matching ASTIS-owned or
Mathlib probability-TV contraction declaration in its targeted search.

This is proposed, not implemented. Its consumer is SPHMC v1 Section 7.2:
use the same implemented PBPS kernel on the actual input and on its proxy,
then a test can combine two $\varepsilon/2$ event bounds into $\varepsilon$.
The proxy's Renyi certificate belongs only to the proxy. A TV bound cannot
transport an unbounded expected oracle cost: the actual-input query bound
must separately follow PBPS v1 (4.18), including solver caps and event-rate
control. This probability-law edge does not depend mathematically on the
quadratic-regularization packet or on scalar RGO condition-number algebra.
