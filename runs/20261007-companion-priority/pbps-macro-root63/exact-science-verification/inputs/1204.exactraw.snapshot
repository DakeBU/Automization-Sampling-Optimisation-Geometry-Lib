# Weighted C1 compact-domain source/API pre-read

Date: 2026-10-06. Reviewer: `phase_source_reviewer_20261005`.

This is source/dependency scheduling evidence only. It records an independent
primary-source and existing-interface pre-read, not a candidate proof review,
source-acceptance verdict, compiled advance, operator-core certificate, or
paper-completion claim. No production implementation was changed or compiled
for this pre-read. Future mathematical and source reviews remain independent.

## Exact primary source and seven-slot contract

Primary edition: Chen, Chewi, Lu and Zhang, **arXiv:2609.06905v1**,
*Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy
Particle Sampler*, September 2026. This note paraphrases the source rather than
quoting a new numbered theorem.

- [Section 2.2, equations (2.6)-(2.14)](https://arxiv.org/html/2609.06905v1#S2.SS2):
  HTML lines 168-211, actual augmentation, conditionals and reflection.
- [Appendix B.2, equations (B.8)-(B.13)](https://arxiv.org/html/2609.06905v1#A2.SS2):
  HTML lines 952-975, reflected coordinates and macroscopic observable space.
- [Appendix C.1, proof of Lemma B.1 and Lemma C.1](https://arxiv.org/html/2609.06905v1#A3.SS1):
  HTML lines 1197-1310, especially 1200, 1283, 1294 and 1303-1310.

| Slot | Source contract and boundary |
| --- | --- |
| Objects | Actual augmentation, common conditional kernels, reflected conditional density, macroscopic conditional-expectation operator, and weighted closed gradient. |
| Domains | Source: real Euclidean full space. Existing shared interfaces: finite-dimensional real inner-product Borel spaces with canonical volume. This is a disclosed full-space extension, not a manifold or boundary theorem. |
| Quantifiers | Source calculations begin with compact smooth observables and extend to the actual macroscopic weighted H1 space. Existing conditional resolvent is fiberwise for every observation, positive epsilon and scalar L2 input. |
| Assumptions | Global C2 potential, positive ordered curvature bounds and positive eta; PBPS conditional interfaces retain beta*eta <= 1. A shared C1 compact-domain leaf itself needs no curvature estimate. |
| Conclusion | Genuine function/gradient graph membership and legitimate weak tests; future consumers may derive an ordinary local weak Laplacian. No H2 or global Bochner conclusion follows merely from these tests. |
| Scope | Source density/closedness and cutoff steps need actual joint approximation, integrability and limit arguments. A conditional-fiber leaf does not itself complete the macroscopic H1 extension or conditional Poincare. |
| Constants | Reflection changes Hessians by one quarter and gradient/Dirichlet scales by two/four. No constants or operators may be identified without their true adapter. |

The source's passage from compact smooth tests to H1 is an omitted analytic
detail to be proved. Its noncompact constant test also explicitly uses cutoffs.
Neither statement authorizes assuming a density or graph-domain certificate.

## Actual PBPS reflected law versus SPHMC RGO

Write the actual base Gibbs law as
`mu = volume.tilted (fun x => -V x)`. Its normalization is the actual positive
finite integral of `exp(-V)`, derived from source curvature when applying the
conditional producer. Generate independent `X ~ mu`, standard Gaussian `Z`,
and `Y_plus = X + sqrt(eta) Z`, `Y_minus = X - sqrt(eta) Z`.

For fixed observation y, the **reflected PBPS** potential is

\[
 W_y^{\mathrm{PBPS}}(u)
 =V((y+u)/2)+\frac{\|u-y\|^2}{8\eta}.
\]

Its actual normalized law is `S y = volume.tilted (-W_y)`, with the same
Markov kernels and disintegration already constructed by the conditional
interfaces. The **SPHMC RGO** potential in the original position coordinate is

\[
 W_y^{\mathrm{RGO}}(x)
 =V(x)+\frac{\|x-y\|^2}{2\eta}.
\]

Comparison source: **arXiv:2609.06906v1**, [Section 3.4 RGO definition](https://arxiv.org/html/2609.06906v1#S3.SS4),
HTML lines 353-355, and [Section 4.1](https://arxiv.org/html/2609.06906v1#S4.SS1),
HTML lines 403-430. The source-normalized SPHMC beta=1 convention must not be
silently substituted for general PBPS alpha/beta.

The true coordinate map is `F_y(x) = 2*x-y`, with inverse `(y+u)/2`.
Consequently `S y = (R y).map F_y`; these laws are not equal on the same
coordinate space. In positive dimension d, `dx = 2^(-d) du`, and the actual
unnormalized integrals satisfy `Z_PBPS(y) = 2^d Z_RGO(y)`. The density Jacobian
and normalizer therefore cancel in the normalized pushforward, not by an
assumed equality of unnormalized densities.

\[
 \nabla_u^2 W_y^{\mathrm{PBPS}}(u)
 =\tfrac14\{\nabla^2 V((y+u)/2)+\eta^{-1}I\},
 \qquad
 \frac{\alpha+\eta^{-1}}4 I
 \preceq \nabla_u^2 W_y^{\mathrm{PBPS}}
 \preceq \frac{\beta+\eta^{-1}}4 I.
\]

For a genuine differentiable test psi,
`gradient_x (psi o F_y) = 2 * (gradient_u psi) o F_y`; hence

\[
 \int\|\nabla_x(\psi\circ F_y)\|^2\,dR_y
 =4\int\|\nabla_u\psi\|^2\,dS_y.
\]

A future transport must prove these derivative/domain identities and the
corresponding resolvent parameter scaling. Reflection symmetry alone does not
identify the conditional measures, gradient operators, or their constants.

## Existing genuine interfaces and their test classes

Paths below are exact production paths; these are interfaces read during this
pre-read, not claims based on prior acceptance verdicts.

- `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean`,
  `compact_gradient_closable`: for C1 W with actual `exp(-W)` integrability,
  constructs a dense closable partial gradient D. Its graph is **exactly**
  actual compact smooth scalar representatives paired with their real
  gradients. This does not supply arbitrary C1 compact graph membership.
- `.../WeightedGradientWeak.lean`, `closed_gradient_weighted_ibp` (line 66):
  elements of this same closure obey weighted IBP against **C1 compact**
  scalar tests, with the two products proved integrable.
- `.../WeightedGradientDistribution.lean`,
  `closed_gradient_distributional` (line 43): the same elements have ordinary
  locally integrable volume representatives and ordinary weak gradient
  identities against **C1 compact** tests. This is not a converse domain
  characterization.
- `.../WeightedLocalL2.lean`, `lp_locallyMemLp_volume` (line 24): actual weighted
  L2 classes are locally volume-L2, including vector-valued gradient classes.
- `.../ClosedGraphResolvent.lean`, `weak_resolvent` (line 24): an actual closed
  partial operator has a unique positive-epsilon variational solution, with
  all tests in its actual domain and explicit L2 energy/norm bounds.
- `.../WeightedResolvent.lean`, `weak_resolvent_distributional` (line 22):
  constructs that actual closed-gradient solution. Its ordinary weak-gradient
  part permits C1 compact tests, but its weighted divergence-form resolvent
  equation currently permits **only C-infinity compact** tests.
- `AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradient.lean`,
  `conditional_gradient_closable` (line 26), and `ConditionalResolvent.lean`,
  `conditional_weak_resolvent` (line 21): retain the actual common R/S kernels,
  reflection pushforward, pointwise normalized reflected density and one
  genuine gradient closure per fiber. D is fixed before epsilon and the L2
  input. The weak equation tests every actual closure-domain element; there
  is no measurable selection of solutions in y or classical PDE assertion.
- `ConditionalBochner.lean`, `conditional_bochner_energy` (line 25): currently
  evaluates the actual weighted Laplacian/Bochner energy for compact smooth
  functions. It cannot be applied directly to a noncompact weak resolvent
  solution.

The requested name `ConditionalWeakGradient` was not found as a production
module or declaration during the bounded lookup. The actual available weak
gradient APIs are `WeightedGradientWeak`/`WeightedGradientDistribution`,
combined with `ConditionalGradient`; a missing name is not an admitted parent.

## Smallest next analytic node and proposed exact interface

Keep the **same D** already constructed from the actual compact smooth
gradient; do not replace it by a convenient operator. For C1 W and actual
exponential integrability, propose to extend that construction with the
following **conclusion**, alongside its existing dense/closable/exact-core
contract:

\[
 \forall\psi\in C_c^1(E),\quad
 \psi,\nabla\psi\in L^2(\mu),\qquad
 ([\psi],[\nabla\psi])\in D.\mathrm{closure.graph},
 \quad \mu=\mathrm{volume.tilted}(-W).
\]

There is no supplied C1 graph-membership, graph-density, moment, Poincare or
regularity certificate in this target. In the PBPS application, the existing
actual conditional producer derives W, its regularity/integrability and the
normalized law; these are not new paper hypotheses.

The first leaf to prove is **joint compact C1 approximation**:

1. Construct actual compact smooth mollifiers rho_n normalized against volume,
   with supports shrinking to zero, and `psi_n = rho_n * psi`.
2. Prove smoothness, a common compact support K, and the genuine identity
   `gradient (rho_n * psi) = rho_n * (gradient psi)`. Independently smoothing
   a supplied vector field is not enough: it must be the derivative of psi_n.
3. Prove uniform convergence of both functions and their actual gradients.
   C1 compactness supplies continuous compact gradients and uniform
   continuity; common support controls the weighted L2 passage.
4. Derive both L2 convergences from `mu(K) < infinity`, then use the actual
   original smooth-core graph and its closure to obtain the displayed pair.

Next, use this membership as a legitimate test in the **same** variational
resolvent solution. Output the weighted resolvent equation for every C1 compact
psi, with all three products integrable. Then compose it with the existing
actual conditional interfaces, retaining their R/S and D. Fiberwise existence
must not be promoted to measurable joint resolvent selection without proof.

## Pinned Mathlib candidates, not a ready-made density certificate

Verified toolchain: `leanprover/lean4:v4.33.0`. `lake-manifest.json` pins Mathlib
revision `db584cd6d46c92f209a44c0f1c829460d327499d` (input tag `v4.33.0`). The
manifest LF byte SHA256 at this pre-read is
`b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37`.

- `Mathlib/Analysis/Calculus/ContDiff/Convolution.lean`:
  `HasCompactSupport.hasFDerivAt_convolution_right`,
  `HasCompactSupport.hasFDerivAt_convolution_left`, and the corresponding
  `contDiff_convolution_right/left` APIs. These are ingredients for the real
  derivative and smoothness; their hypotheses and CLM/Riesz conversions must
  actually be discharged.
- `Mathlib/Analysis/Calculus/BumpFunction/Convolution.lean`:
  `ContDiffBump.dist_normed_convolution_le` and
  `ContDiffBump.convolution_tendsto_right_of_continuous`. The latter gives a
  pointwise approximation ingredient; a uniform joint-gradient statement
  still needs an actual proof using uniform continuity and support control.
- `Mathlib/Analysis/Normed/Lp/SmoothApprox.lean`:
  `MeasureTheory.Lp.dense_hasCompactSupport_contDiff` proves function-space
  density. It does **not** by itself prove joint function/gradient convergence.

No ignored implementation or compiler experiment was inspected to choose these
requirements. No claim is made that the joint leaf already exists in Mathlib.

## Inverse-weight tests, ordinary Laplacian and later boundaries

For compact smooth phi, choose `psi = exp(W) * phi`. This test **remains
compactly supported**. Its obstacle is regularity: C1 or C2 W generally makes
psi C1 or C2, not C-infinity. Assuming this inverse-weight test is smooth would
silently strengthen the actual source potential.

After proving the C1 graph extension and C1 resolvent tests, the actual product
rule and positive normalization give, for the same solution u and G = weak
gradient u,

\[
 \Delta u=\varepsilon u+\langle\nabla W,G\rangle-f
 \quad\text{in ordinary distributions}.
\]

`WeightedLocalL2` supplies local volume-L2 of u, G and f. The continuous
gradient of C1 W is bounded on compact sets, so this displayed right-hand side
is locally L2. This is a legitimate next consumer; **it is not an H2 theorem**.
An actual weak-Poisson-to-local-H2 producer is still required.

Noncompact objects enter separately: u is a weak resolvent solution, and source
constant/linear/score tests require actual cutoff and tail arguments. C1 compact
membership alone does not justify those limits. Global weighted H2 or Bochner
estimates need their own cutoff/domain/integrability proof; local boundedness
of gradient W does not establish global L2 of `inner (gradient W) G`. Nor does
first-order graph approximation prove a generator/operator core for D-star-D.
Conditional Poincare, BL, full PBPS C.1, full SPHMC Lemma 4.1 and both main
results remain outside this note.

## Zero dimension and anti-anchoring record

The finite-Hilbert generalization includes dimension zero. Then E is a
singleton, gradients vanish, and every scalar function is a smooth constant;
use the constant approximation sequence. The determinant factor is
`2^(-0) = 1`. Do not require a unit vector or positive dimension merely to use
a mollifier API. This case does not introduce a eta=0 limit; eta stays positive.

Before future C1 candidate packets, this pre-read inspected primary source,
existing production public contracts, bounded snippets of the old weighted
gradient implementation, and pinned Mathlib candidate signatures. It did not
inspect root's ignored C1 mollifier prototype, a future anonymous reconstruction,
future candidate complete proof, or its mathematical/source verdicts.

Earlier, the separate next-BL library search exposed GibbsGradientMoment
keywords, declaration signatures and matching lines. That limited exposure
was explicitly disclosed in the independent covariance receipts; complete
candidate blindness was not claimed. It is not evidence that a future C1
implementation is correct. This durable note preserves the source pre-read
and that honest exposure boundary, without any new acceptance or mathematics
credit.
