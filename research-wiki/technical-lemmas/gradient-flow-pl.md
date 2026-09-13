# Actual gradient-flow dissipation and PL decay

SAU ANDI-OPT-gradient-flow-pl-001; cell ASTIS-SHARED-gradient-flow-pl.
Source Chewi2605.07006v1 Section2 Lemma2.1 and Corollary2.6.

For a supplied continuous curve on[0,T] with its actual right gradient ODE
beforeT, derive d(f composed X)/dt=-norm gradient squared by the Frechet
chain rule and Riesz identity. PL gives e prime<=-2alpha e; reuse pinned
Mathlib finite-interval right-slope Gronwall to get0<=e(t)<=e(0)exp(-2alpha t).
The ASTIS SemigroupDecay interface requires all-real derivatives, so do not
force this forward flow into a negative-time existence hypothesis. No scalar
Gronwall reproof, artificial flow construction or supplied energy identity.

Source generalization: complete real Hilbert space, differentiability rather
than C2, and right derivative rather than two-sided. Terminal continuity is
retained. AtT0 the derivative clause is empty and the bound equality. Positive
alpha and supplied attained minimum retain source conventions. No pointwise
trajectory convergence, convexity, discretization, stochastic process or paper
completion. Mathematical scheduling remains the user's optimisation task.

Reuse audit: runs/semantic-roundtrip/andi-opt-gradient-flow-pl/upstream-review.json.
Conceptual-mirror audit none-found: existing metric-gradient-flow/gap-gradient
families already retain this exact dissipation/PL/Gronwall mechanism. No new
cross-domain hypothesis map or transport certificate was discovered.

Compiler diagnosis: use the explicit Riesz continuous-linear derivative and
simp only to avoid the simplifier replacing it with opaque fderiv; unfold slope
for the existing one-sided comparison. No hypothesis change. The nonstationary
quadratic test proves its real gradient/minimum/PL and actual exp(-t) trajectory;
rate exp(-2t) is exact, includingt0.

Focused compile, independent proof/source audits, root Tests import, Registry,
canonical gate and affected reader/graph publication pending. Before pushing,
run both website/formalization contract suites, not only site build/check.
