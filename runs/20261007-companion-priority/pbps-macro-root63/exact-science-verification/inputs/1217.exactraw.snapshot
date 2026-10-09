# Ordinary weak Laplacian of the same weighted resolvent: dependency audit

Date: 2026-10-06. Independent API/source-detail audit by
`picard_commit_verifier_20261005`, at base
`f68063e9e4a56964ecff05c2af83e2edf26f21ef` and Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`, Lean 4.33.0.

This note proposes one analytic prerequisite. It is not a Lean theorem,
source-equivalence verdict, new SAU, H2 certificate, or either paper's main
result. No Lean implementation or compiler run was performed for this audit.
Root's ignored prototypes, anonymous reconstruction and source-review results
were not inspected. The current C1 domain/test packet has independent
mathematical compilation evidence; its source admission and exact-commit
VERIFIED remain separate at the time of this note.

## Source boundary and the two conditional coordinates

[PBPS arXiv:2609.06905v1 Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1),
HTML lines 1200-1218 and 1276-1305, uses compact smooth tests, gradient
closedness/density, conditional integration by parts and a conditional
Poincare estimate. The actual reflected conditional density there has potential

\[
 W_y^{\rm PBPS}(z)=V((y+z)/2)+\frac{\|z-y\|^2}{8\eta},
 \qquad \nabla_z^2W_y^{\rm PBPS}
 =\tfrac14\{\nabla^2V((y+z)/2)+\eta^{-1}I\}.
\]

[SPHMC arXiv:2609.06906v1 Section 4.1](https://arxiv.org/html/2609.06906v1#S4.SS1),
HTML lines 403-430, uses the actual **unreflected** RGO potential

\[
 W_y^{\rm RGO}(x)=V(x)+\frac{\|x-y\|^2}{2\eta}
\]

for the BL covariance upper bound and the Cramer-Rao reverse bound. The present
weak-resolvent route is a background route toward the still-open BL half, not
the numbered covariance theorem or its completion.

The existing actual kernels satisfy
`S y = (R y).map (fun x => 2 • x-y)`. Thus the reflected and unreflected laws
are related by a pushforward, not equal on their original coordinate space.
Transport of gradients, Dirichlet energies, domains and resolvent parameters
needs its own adapter. In particular the gradient pullback has factor 2 and
the Dirichlet energy factor 4. Do not reuse the reflected equation as an
unreflected equation with unchanged operator or constants. Fiberwise existence
also does not provide a measurable selection of solutions in y.

## Exact mathematical input and smallest next output

Use a finite-dimensional real Borel Hilbert space E, including dimension zero,
canonical full-space volume, a C1 potential W with actual
`Integrable (fun x => exp(-W x)) volume`, and

\[
 \mu=\mathrm{volume.tilted}(-W),\quad \varepsilon>0,
 \quad f\in L^2(\mu).
\]

Keep the original closable partial gradient D whose graph is exactly compact
smooth scalar representatives paired with their genuine gradients. Its
existence is supplied by the existing actual Gibbs producer, not postulated
for every finite atomic measure. D is fixed before epsilon and forcing.

The C1 weak-resolvent producer constructs u in the same `D.closure.domain`,
G=`D.closure u`, the actual variational equation, local ordinary-volume
integrability and ordinary directional weak-gradient identities. Its weighted
equation permits every C1 compact psi and proves all three products L1 first:

\[
 \varepsilon\int e^{-W}u\psi
 +\int e^{-W}\langle G,\nabla\psi\rangle
 =\int e^{-W}f\psi.
\]

The proposed next conclusion concerns the same u/G/f representatives:

\[
 k=\varepsilon u+\langle\nabla W,G\rangle-f,
 \qquad
 \forall K\text{ compact},\quad
 u,G,f,k\in L^2(\mathrm{volume.restrict}\ K),
\]

\[
 \forall\phi\in C_c^2(E),\qquad
 \int u\,\Delta\phi\,dx=\int k\phi\,dx.
\]

All integrands must be genuinely integrable. This states the ordinary
**distributional** Laplacian of u. It does not use Lean's total `fderiv` or
`Laplacian.laplacian` on the arbitrary L2 representative u to assert classical
differentiability. Only the actual C2 test phi has a classical Laplacian.
C-infinity compact source tests are a specialization; C2 suffices here.

## Seven-step route with the correct sign

1. Retain the actual u and G from `WeightedResolventC1.weak_resolvent_c1`.
   Its ordinary weak-gradient conclusion refers to this same pair, with
   volume as measure. Do not choose a second solution or operator.
2. For compact C2 phi, set psi=`exp(W)*phi`. This is C1 and remains compact
   by `ContDiff.exp.mul` and `HasCompactSupport.mul_left`. C1 W is sufficient;
   asserting C-infinity psi would be false in general.
3. The true product rule gives
   `gradient psi = exp(W) • (gradient phi + phi • gradient W)`.
   Obtain it from `HasFDerivAt.exp`/`.mul`, the real Riesz gradient bridge,
   and differentiability of W/phi. Then cancel the pointwise positive weights
   `exp(-W)*exp(W)=1` inside the already justified weighted products.
4. Prove the unweighted individual products integrable, rather than relying
   on integrability of their sum. The local L2 facts below and compact test
   support give L1 of `u*phi`, `f*phi`, `inner G (gradient phi)` and
   `phi*inner (gradient W) G`. This yields
   \[
   \int\langle G,\nabla\phi\rangle
   =\int(f-\varepsilon u-\langle\nabla W,G\rangle)\phi.
   \]
5. Let b be `stdOrthonormalBasis ℝ E`. Each
   `chi_i(x)=fderiv ℝ phi x (b i)` is C1 and compact. Apply the actual ordinary
   directional identity with test chi_i and direction b_i:
   \[
   \int u\,D_{b_i}D_{b_i}\phi
   =-\int D_{b_i}\phi\,\langle G,b_i\rangle.
   \]
   Both products are L1 by that producer. Sum over the finite basis and use
   the Laplacian bridge and the orthonormal inner-product expansion. Therefore
   `integral u*Delta(phi) = - integral inner G (gradient phi)`.
6. Combine the two identities. The resulting sign is
   \[
   \Delta u=\varepsilon u+\langle\nabla W,G\rangle-f
   \quad\text{in ordinary distributions}.
   \]
7. Package compact-restriction L2 for k and locally integrable squared norms.
   The empty basis in dimension zero causes no exception. E is a singleton,
   gradients/Laplacian vanish and the same equation reduces to the actual
   scalar epsilon resolvent; no unit vector or positive-dimension premise.

## Actual interfaces available now

Production paths are under `AutoSamplingTheory/`; exact public names below
can be used without copying their proofs.

| Interface | Actual contract needed here |
|---|---|
| `TechnicalLemmas.FunctionalInequalities.WeightedResolventC1.weak_resolvent_c1` | Same D/u/G, all-domain variational equation, ordinary C1 compact directional weak gradient, and weighted C1 compact tests with all L1 products. |
| `TechnicalLemmas.FunctionalInequalities.WeightedGradientDistribution.closed_gradient_distributional` | Ordinary volume weak gradient of a member of the same closure graph; inverseweight C1 compact testing is already proved, not a converse domain characterization. |
| `TechnicalLemmas.FunctionalInequalities.WeightedLocalL2.lp_locallyMemLp_volume` | For any scalar/vector weighted L2 class a and continuous W, squared norm is locally volume-integrable and a belongs to L2 for every compact volume restriction. Apply separately to u, G and f. |
| `TechnicalLemmas.Analysis.Calculus.Gradient.fderiv_apply_eq_inner_gradient_of_differentiableAt` | Converts true directional derivatives to real gradient inner products. |
| `TechnicalLemmas.Analysis.Calculus.Laplacian.laplacian_eq_sum_stdOrthonormalBasis` | Actual Mathlib Laplacian equals the finite sum of `iteratedFDeriv ℝ 2` diagonal evaluations. No IBP or regularity of u. |
| `ExampleCases.ProximalBPS.ConditionalC1Resolvent.conditional_c1_resolvent` | Actual reflected R/S law, fixed original D before epsilon/input and the foregoing conclusions per fiber, without measurable y-selection. |

`WeightedBochner.integrated_bochner_identity` assumes C2 W and **compact
smooth f**. Its local `directional_second` and `laplacian_dirs` proofs show the
coordinate route, but are not public callable declarations. Use the existing
public Laplacian bridge plus Mathlib derivative API, or extract a minimal
shared directional bridge with explicit actual consumers if that reduces
duplication. Do not copy its entire background proof, treat the local helper
as already callable, or count extraction as new mathematical progress.
Most importantly, its global Bochner identity cannot yet be applied to the
noncompact weak resolvent solution u.

## Compact L2 passage: minimal pinned Mathlib API

`WeightedLocalL2` already proves volume measurability using
`absolutelyContinuous_tilted hI` in the needed direction, not by changing the
representative measure silently. On each compact K, continuity of the true
gradient of C1 W gives a finite bound M_K on its norm. Thus

\[
 |\langle\nabla W(x),G(x)\rangle|\le M_K\|G(x)\|
 \quad\text{for volume.restrict K almost every x}.
\]

`MemLp.of_le_mul` in
`Mathlib/MeasureTheory/Function/LpSeminorm/Monotonicity.lean:188`
requires the target's actual a.e. strong measurability and that a.e. norm
inequality. Supply the first by continuous gradient inner a.e. measurable G
and the second using `ae_restrict_mem hK.measurableSet`; a bound on K alone
is not a global bound. Then `MemLp.const_mul`, `.add` and `.sub` prove k L2
on K. No bound uniform in K, curvature premise, or global drift-product L2
is required or obtained.

For compact-test L1 products, use the compact restricted L2 functions and
bounded compact supported test/gradient, with `L2.integrable_inner` or the
MemLp product/integrability API. Then prove the restriction equals the full
integral because the test is zero outside its support. Never rearrange
unproved nonintegrable expressions using the total Bochner integral.

`memLp_two_iff_integrable_sq_norm` and
`locallyIntegrable_iff` in
`Mathlib/MeasureTheory/Function/LocallyIntegrable.lean:332`
convert every-compact L2 into locally integrable squared norm. Finite Hilbert
E is locally compact and metrizable; no new locally compact-space hypothesis
is needed in this specialization.

For directional second derivatives of a C2 test, pinned APIs include
`ContDiff.fderiv_right`, `HasFDerivAt.clm_apply`,
`iteratedFDeriv_two_apply` and
`InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis`.
Continuity and support of derivative tests follow from the true C2 derivative
and `fderiv_of_notMem_tsupport`/`HasCompactSupport.fderiv`, not an assumed
compact Hessian certificate.

## What the search did not supply

Bounded searches of ASTIS FunctionalInequalities/Analysis and pinned Mathlib
Distribution/InnerProductSpace APIs did not locate a direct public producer
joining **this ordinary weak resolvent**, its compact-restriction L2 data,
and its true distributional Laplacian into local weak H2. This is a bounded
search result, not a claim no usable theorem exists anywhere.

Mathlib `Analysis/Distribution/Sobolev.lean` provides Fourier-defined Bessel
Sobolev spaces, `memSobolev_zero_iff`, `memSobolev_besselPotential_iff`, the
L2 Fourier characterization and forward derivative/Laplacian maps. These
are ingredients, not the already instantiated converse local elliptic result.
`Lp.toTemperedDistribution` embeds actual global-volume Lp classes; the
current weighted L2 resolvent is not thereby global-volume L2 or tempered.
Do not insert either property as an unproved premise.

A possible later route is compact cutoff chi, deriving global-volume L2 of
chi*u and the distributional product identity

\[
 \Delta(\chi u)=\chi k+2\langle\nabla\chi,G\rangle+u\Delta\chi.
\]

The right-hand side is then global-volume L2 by compact support and the actual
local data. Its distribution/tempered embedding, correct cutoff product rule,
Fourier/Bessel elliptic inverse, real/complex conventions and conversion back
to local weak Hessian representatives all remain proofs. They must not be
replaced by merely observing a forward Sobolev mapping theorem. Nor does
local H2 give a global weighted H2/Bochner estimate, a D*D generator core, a
Poincare inequality, or the epsilon-to-zero centered Poisson limit.

## Remaining truth and scheduling boundary

The dependency-ready next unit is the ordinary weak Laplacian equation and
its genuine local-volume L2 right-hand side, retaining the same solution and
gradient graph. It is a source-backed analytic prerequisite with a real later
elliptic/BL consumer, not completion of macroscopic H1, conditional Poincare,
SPHMC Lemma 4.1, either sampler's main result, or their algorithm/cost
composition. No new SAU or formal graph edge is established by this note.

Noncompact constant/linear tests need their actual cutoffs and tails. Global
operator-core and Bochner estimates require separate domain/integrability
proofs. Reflection adapters, measurable y-selection, stochastic histories,
implementation/query costs and the PBPS/SPHMC independent main boundaries
remain unchanged. TV proximity transfers no unbounded expected cost.
