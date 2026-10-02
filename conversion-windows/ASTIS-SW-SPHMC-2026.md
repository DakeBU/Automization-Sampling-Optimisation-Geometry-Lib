# Smoothed Picard HMC · formalization result window

Primary: [arXiv:2609.06906v1](https://arxiv.org/html/2609.06906v1).
Reader: [existing companion page](../website/content/samplewiki_companion_frontiers.json).
The public route is `example-cases/samplewiki/companions/smoothed-picard-hmc.html`.

Current compiled packets: `ASTIS-SW-SPHMC-recursive-condition-contraction` and
`ASTIS-SW-SPHMC-rgo-closure`.
The Frontier Cell is authoritative for compilation/review status; no duplicate
completion counter is kept here. The teaching proof and source correspondence
are in `declaration_lessons/sphmc-recursive-condition.json`,
`declaration_lessons/sphmc-rgo-closure.json`, `publications/sphmc.json` and
`publications/sphmc-rgo-closure.json` under `website/content/`.

## Compiled initialization component: Lemma 4.16 at q = 2

`ASTIS-SW-SPHMC-initial-gibbs-q2` connects the actual normalized Gibbs law,
its Gaussian smoothing, and the phase-space coupling used by Lemma 4.16.  In
the paper's normalized regime, write $\kappa=1/\alpha$, let $p$ be a supplied
critical point, and assume

$$
\|\nabla U(x_{\rm ref})\|^2\le\alpha d,
\qquad 0<\alpha\le1,
\qquad 0\le\eta\le1.
$$

The compiled proof first obtains
$\|x_{\rm ref}-p\|^2\le d/\alpha$ from genuine Hessian strong convexity.
It then combines the Gibbs moment about $p$ with the squared triangle
inequality, adds the exact $\eta d$ Gaussian-smoothing contribution, and
couples the two momentum coordinates identically:

$$
\begin{aligned}
\mathbb E_\pi\|X-x_{\rm ref}\|^2&\le4d/\alpha,\\
\mathbb E\|X+\sqrt\eta G-x_{\rm ref}\|^2&\le(4\kappa+\eta)d,\\
W_{2,M_\kappa}^2(\delta_{x_{\rm ref}}\otimes\gamma,
  \Pi_\eta)&\le5\kappa d.
\end{aligned}
$$

This is an explicit conditional $q=2$ proof component, not all of Lemma 4.16.
The source states a universal-constant bound for every $q\ge2$; the all-$q$
concentration argument and a source-level theorem constructing the critical
point from the curvature hypotheses remain separate open edges.  The constant
$5$ is the ASTIS-derived second-moment constant, not a constant printed by the
paper.  The reader proof and folded Lean are generated from
`sphmc-initial-gibbs-q2.json` in the declaration-lesson and publication
metadata directories.

## Exact conversion

In (6.1)–(6.2), let $k=\kappa_A\ge2$, $h=\eta_j$, $\tau=k$,
$a=(h+\tau)/\beta_A$, with $\beta_A>0$. Then

$$k_+=\frac{k(a\beta_A+1)}{a\beta_A+k}
      =\frac{k(k+h+1)}{2k+h}.$$

The local declaration `RecursiveCondition.contraction_bounds` proves
$k/2\le k_+\le4k/5$ for $0<h<1/4$ by positive-denominator algebra.
The source domain $0<h\le c_0<1/4$ implies this range; conversely every such
$h$ admits $c_0=h$, so the unused cutoff can be eliminated. This is the
scalar proof component of Lemma 6.6(i), consumed by the recursive-depth argument
in Theorem 6.5, not a new ASTIS complexity result.

## Remaining proof edges

Gibbs-density identification and curvature/parameter updates (Lemma 6.4);
well-conditioned contraction (Lemma 6.6(ii)); stage termination and accumulated
cost/error; normalized density smoothing and score regularity; Picard local
error and moment propagation; proxy construction; final actual-input cost.
Theorems 1.1–1.3 remain open. No diagram or citation/download feature is a
prerequisite for the next correct Lean packet.

## Lemma 4.17: exact RGO recovery is compiled; fiberwise W2 contraction is blocked

The recovery identity is already stronger than a paper-specific invariance
wrapper: `GaussianConditionalKernel.exists_tilted_isCondKernel` supplies the
joint disintegration certificate, and `RGOBackward.rgo_backward_recovery`
records the SPHMC specialization. A duplicate recovery declaration is therefore
not a new mathematical leaf.

The remaining first inequality in Lemma 4.17 is genuinely analytic. With
`alpha = kappa^{-1}` and `lambda = alpha + eta^{-1}`, the cited
Lee--Shen--Tian proof is

\[
W_2^2(R_{\eta,y},R_{\eta,y'})
 \le \frac{2}{\lambda}\,\mathrm{KL}(R_{\eta,y}\|R_{\eta,y'})
 \le \frac{1}{\lambda^2}\,\mathrm{FI}(R_{\eta,y}\|R_{\eta,y'}),
\]

while direct differentiation of the normalized density ratio gives

\[
\nabla\log\frac{dR_{\eta,y}}{dR_{\eta,y'}}(x)
 = \frac{y-y'}{\eta}.
\]

Consequently

\[
W_2(R_{\eta,y},R_{\eta,y'})
 \le \frac{1}{1+\alpha\eta}\,\lVert y-y'\rVert
 = \frac{\kappa}{\kappa+\eta}\,\lVert y-y'\rVert.
\]

At the pinned toolchain, neither Mathlib nor Samplinglib contains the required
strong-convex Gibbs log-Sobolev instance and Otto--Villani `LSI -> T2` backend.
The route is therefore recorded as the typed blocker
`ASTIS-SW-SPHMC-rgo-fiber-w2-contraction`, with the strictly smaller shared child
`ASTIS-SHARED-strong-convex-gibbs-lsi-t2`. A theorem assuming the desired T2
bound, or a coupling with the desired cost, would only restate the missing
content. The alternative Wasserstein-subdifferential/JKO proof is source-valid
but retired for this packet because its absent formal substrate is larger.

## Compiled normalized-law component: Lemma 6.4

The distribution-level edge is now `RGOClosure.quadratic_tilt_tilt`, not an
assumed scalar recurrence. Use precisions $r=A^{-1}\ge0$, $s=a^{-1}>0$ so $A=\infty$
is represented by $r=0$ without dividing by an infinite value. With
$w=(r+s)^{-1}(ru+sy)$ the calculation to justify is

$$\frac r2\|x-u\|^2+\frac s2\|x-y\|^2
=\frac{r+s}{2}\|x-w\|^2
 +\frac{rs}{2(r+s)}\|u-y\|^2.$$

The last term is independent of $x$. Its positive finite exponential factor
cancels between the unnormalized density and its normalizer. This cancellation
is proved for actual `Measure.tilted` measures. Positive finite normalizers
follow internally from measurable weights in $(0,1]$ over a probability base.
The $r=0$ and equal-precision cases are directly tested. Neither an assumed law
equality nor a zero-measure fallback is used.

Bounded API audit (pinned Mathlib and current ASTIS, 2026-09-10):
Real inner-product bilinearity provides square expansion; Mathlib `tilted_tilted`,
`tilted_const` and `isProbabilityMeasure_tilted` already supply normalization.
The new ASTIS theorem joins these existing facts. No independent PBPS consumer
of this exact nested-tilt identity was found, so it remains route-local.

Next adapter audit: set $\mu=\mathrm{volume.tilted}(-U)$ and reuse
`tilted_tilted`; this already is the normalized potential-defined density.
No separate density-equality reexport is needed. The genuinely missing premise
is integrability of $e^{-U}$ under the source hypotheses. Existing ASTIS
strong-convexity envelopes require a supplied minimizer; the source does not
supply one, and the formalization must not add that premise.

Compiled shared prerequisite: `ASTIS-SHARED-strong-convex-gibbs-integrability`,
with its exact independent-review/admission status in that Frontier Cell:

$$m>0,\quad V\text{ differentiable},\quad V\text{ is }m\text{-strongly convex}
\quad\Longrightarrow\quad e^{-V}\in L^1(\mathrm{volume}).$$

The proof uses the compiled first-order lower bound at zero and Young's inequality to get

$$V(x)\ge\frac m4\|x\|^2+V(0)-\frac{\|\nabla V(0)\|^2}{m},$$

then reuses `Analysis.Integrability.integrable_exp_neg_add_mul_norm_sq`.
The focused tests derive a strictly positive normalizer, form the actual Gibbs
probability law, and supply it to `quadratic_tilt_tilt`, including zero initial
precision. These are real consumers, not new normalization wrappers. Teaching
and source metadata are `strong-convex-gibbs-integrability.json` in the existing
declaration-lesson and publication directories.
The coefficient $m/4$ is only a domination envelope, not a changed curvature
constant. That integrability packet alone does not convert the paper's
Hessian formulation. The separately compiled shared adapter
`ASTIS-SHARED-hessian-strong-convexity` now proves

$$V\in C^2,\quad D^2V(x)[v,v]\ge\alpha\|v\|^2
\quad\Longrightarrow\quad
V(ax+by)\le aV(x)+bV(y)-\frac\alpha2ab\|x-y\|^2$$

for $a,b\ge0$, $a+b=1$, with exactly the same $\alpha$. Its proof restricts
to a line and subtracts the scalar quadratic; no derivative of the ambient
norm is required. Positive-curvature finite-dimensional consumer tests now
derive integrability, a strictly positive normalizer and a Gibbs probability
directly from C²/Hessian assumptions, then feed it into RGO closure.
See that cell and `hessian-strong-convexity.json` for byte-bound review and
admission status. The separately compiled and source-reviewed
`ASTIS-SHARED-quadratic-regularization` now derives actual quadratic
differentiation, strong convexity and gradient Lipschitz continuity:

$$W=U+\frac r2\|\cdot-u\|^2,\qquad
\alpha_W=m+r,\qquad \operatorname{Lip}(\nabla W)\le L+r.$$

Its five-step lesson explains genuine Hessian differentiation, Riesz
representation, symmetry, the Rayleigh norm bound and the mean-value theorem.
Specialize $m=\kappa^{-1},L=1,r=A^{-1}$; $r=0$ covers $A=\infty$.
The source condition-number substitution, actual recursive sampler and its
error/query bills remain separate. No invariant-law conclusion is inferred.

## Common-kernel TV error transfer

The shared `KernelTotalVariation.abs_real_comp_sub_le` now proves the selected
data-processing step in Section 7.2, proof of Theorem 1.3:

$$\sup_S|\mu(S)-\nu(S)|\le\delta
\quad\Longrightarrow\quad
\sup_T|(\mu K)(T)-(\nu K)(T)|\le\delta.$$

Both input laws are probabilities and K is an actual common measurable Markov
kernel. The proof derives bounded input integrability and both layer integrals
over $(0,1]$; its measure is one, so the factor is exactly one. No density or
Standard Borel assumption is introduced. A focused consumer adds a separately
assumed proxy mixing error by triangle. It does not transfer unbounded query
costs. The four-step lesson and separate folded Lean are generated from
`markov-tv-contraction.json`; the cell records exact admission status.

The explicit RGO Markov kernel and genuine joint-law disintegration are now
compiled in `ASTIS-SHARED-gaussian-rgo-conditional-kernel`. A focused consumer
recovers the original law by applying its all-y normalized kernel to the actual
Gaussian-smoothed marginal. The five-step lesson and source review are linked
from that cell; commit admission remains separately recorded. This justifies
the exact backward-law mechanism, not the recursive sampler's error or cost.

## Lemma6.4 source integration

`RGOCalculus.rgo_calculus` now compiles the source calculus as one integration
node: genuine curvature and gradient smoothness, integrable positive Gibbs
normalization, actual probability laws, exact normalized target update and
the condition-number identity. Cell `ASTIS-SW-SPHMC-rgo-calculus` holds its
independent source/commit admission status; local compilation is not that status.

$$r=A^{-1}\ge0,\quad \alpha=\kappa^{-1}+r,\quad\beta=1+r,
\quad r^+=r+a^{-1},\quad w=(r^+)^{-1}(ru+a^{-1}y),$$
$$R^{U_{A,u}}_{a,y}=R^U_{(r^+)^{-1},w},\qquad
K^+=\frac{\beta+a^{-1}}{\alpha+a^{-1}}
=\frac{(a\beta+1)K}{a\beta+K},\quad K=\beta/\alpha.$$

Zero precision retains A=infinity. The scalar consumer test substitutes
$a=(h+K)/\beta$ and obtains $K/2\le K^+\le4K/5$ when $K\ge2$ and
$0<h<1/4$. This is the actual target-bound adapter to Lemma6.6(i), not a
construction of recursive random stages. The five-step authored lesson explains
why potentials differ by a constant while their normalized laws are equal.
Every statement/proof retains its separate initially folded Lean disclosure.

## Lemma 6.6(ii): one well-conditioned parameter update

`RecursiveVariance.variance_update_bounds` and its focused tests compile. Exact
source and commit admission is separately tracked by
`ASTIS-SW-SPHMC-recursive-variance-contraction`, not certified by this note.
The authored `sphmc-recursive-variance.json` lesson contains the four-step proof
and corresponding folded Lean. For r>=0 and 0<h<=c, it establishes

$$a=\frac{h+c}{1+r},\quad r^+=r+a^{-1}>0,\quad
0<A^+=(r^+)^{-1}=\frac{h+c}{1+r+r(h+c)}\le2c,$$
$$0<\rho=\frac{2c}{1+2c}<1,\qquad r>0\Longrightarrow A^+\le\rho/r.$$

At zero precision the next parameter is h+c. The finite-parameter comparison
never uses the totalized real inverse of zero as infinity. The same update is
tested with the actual normalized Gibbs target from RGOCalculus; the scalar
production theorem imports only Mathlib. This parameter is not Gibbs covariance.
The selected branch needs no c<1/4 restriction; that extension is disclosed.

Finite-stage termination, branch persistence, implemented oracle, recursive
error and expected query costs remain separate red targets. Neither complete
paper is claimed.

## Actual recursive parameter schedule: active proof packet

Cell `ASTIS-SW-SPHMC-recursive-depth` is independently **VERIFIED** and in
stabilization. `depth_commit_verifier` accepted commit
`457144154299d0a4efc444dc41518727252e74c9` after a successful focused build,
standard-axiom check and exact-bound independent semantic review by
`lambda_decoder` and `depth_final_source`. The canonical aggregate gate and
formalization CI passed at candidate `c533963`. Local reader/graph checks and
targeted browser inspection passed after repairing statement display for local
let-definitions. PR250 remains in stabilization; live publication and neither
complete paper are admitted. Exact command/hash evidence is in
`runs/20260910-companion-priority/recursive-depth.progress.json`. The source contract and
proof route are in `proof-blueprints/SPHMC-recursive-depth.md`.

The single public declaration is `RecursiveDepth.parameter_control`. Its
statement defines the source (6.1) update, (6.2) heat schedule and actual
repeated update using local lets and `Nat.rec`. Its proof contains the internal
facts `well_conditioned_persists` and `finite_depth`; these are not separate
public theorem claims. Lemma6.6's two existing contraction proofs are reused.
The target bound is

\[
(4/5)^M K_0<2 \quad\Longrightarrow\quad
0<r_{M+1+N}^{-1}\le 2c\left(\frac{2c}{1+2c}\right)^N.
\]

It retains κ≥1, r₀≥0, 0<ηⱼ≤c<1/4, the actual branch test, and the first
positive-precision step. The Gibbs consumer test uses the same next precision
and center in `RGOCalculus.rgo_calculus`; its conclusion is next-target
normalizability, not a stochastic implementation or conditional-kernel proof.

The existence of a finite threshold-hitting depth is distinct from the precise
logarithmic schedule in (6.4). That schedule's constants, random history
measurability, terminal FORS, recursive errors and expected costs remain open.

## Prescribed logarithmic depth: locally proved and source reviewed

The successor cell `ASTIS-SW-SPHMC-logarithmic-depth` has passed the actual
`PROVED_LOCAL` publication gate. Its sole public theorem is
`LogarithmicDepth.terminal_depth`. The production module and
`Tests/SmoothedPicardLogarithmicDepth.lean` passed the focused build (2948 jobs).
Independent `depth_commit_verifier` replayed the production proof and found
only standard Lean axioms, without authorizing source or commit admission.

The theorem retains the same actual schedule. For positive natural dimension,
q≥2, 0<Δ≤1/2, 0<γ≤1 and C≥8, it proves

\[
L=q+\log(K_0dq/\Delta)\ge2,\qquad
B=\frac{\gamma}{\sqrt{dL}+L}\in(0,1],\qquad
J=\left\lceil C\log(eK_0/B)\right\rceil>0,
\]
\[
0<r_J^{-1}\le B,\qquad
J\le\left(3C+\frac C2\log(1/\gamma)\right)L.
\]

The terminal constant γ is separate from the heat-schedule constant c.
The displayed sufficient constants refine the parameter argument; they are
not author-specified values or a claim that C=8 suffices for every later
sampler obligation. A universal upper coefficient requires fixed universal γ.
The terminal consumer uses the actual precision to prove integrability and
normalization of the terminal Gibbs target in its actual ambient dimension.
It does not implement FORS or certify its output error or expected work.

Five authored proof steps and source bindings are in
`website/content/declaration_lessons/sphmc-logarithmic-depth.json` and
`website/content/publications/sphmc-logarithmic-depth.json`. Independent
`log_depth_blind_decoder` reconstructed the anonymous proposition;
`log_depth_source_review` accepted the fresh primary-source packet as
equivalent after elaboration for the disclosed constant refinement, retaining
informational precision-representation, constant-dependence and scope deltas.
Exact local evidence is in `runs/20260911-companion-priority/`.
This advances the prior open deterministic-depth boundary only. Independent
commit admission, integration and rendered-reader validation
remain pending; stochastic history, FORS, recursive errors and expected costs
remain separate mathematical obligations. Neither complete paper is admitted.

## Lemma 4.17: the relative-score calculation now compiles

The shared cell ASTIS-SHARED-tilted-log-ratio-representative now isolates the
source equation used in the Lee--Shen--Tian proof cited by SPHMC. For

\[
q_{\eta,y}(x)=-\frac{\|x-y\|^2}{2\eta},\qquad
r_{y,y'}(x)=q_{\eta,y}(x)-\log Z_y-q_{\eta,y'}(x)+\log Z_{y'},
\]

the new Lean declarations prove both

\[
\operatorname{llr}(R_{\eta,y},R_{\eta,y'})=r_{y,y'}
\quad R_{\eta,y}\text{-a.e.},
\qquad
\nabla r_{y,y'}(x)=\eta^{-1}(y-y').
\]

The first equality keeps sigma-finiteness, measurability and both exponential
integrability obligations explicit. The second differentiates the displayed
smooth representative only. It does **not** differentiate Mathlib's canonical
measurable llr: equality almost everywhere does not preserve a classical
gradient after arbitrary changes on a null set.

This closes the exact algebra/calculus content of equation (11), not SPHMC
Lemma 4.17. A representative-to-canonical-Fisher adapter and the
strong-convex Gibbs LSI/Talagrand T2 backend are still red; only after those
independent analytic edges can the exact
\(\kappa/(\kappa+\eta)\) Wasserstein contraction be claimed.
