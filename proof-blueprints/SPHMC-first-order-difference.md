# Actual exact-gradient first-order difference

SPHMC arXiv:2609.06906v1 Algorithm3.1 exact-gradient replacement; Lemma4.6
HTML556–589. One actual integration theorem for the source numerical kernel,
consumed by Proposition4.7 and Lemma4.8. Root is the sole Lean writer.

Inputs: complete finite real inner-product E (including0), f globally C2,
κ≥1 and true global (2κ)^-1 I≤D2f≤I; J≥2,h>0 and h²Λ_J≤1 with the **actual**
Chebyshev-Lobatto supremum and cardinal integral coefficients. These are the
normalized smoothed-potential interface; production of f=V_eta and its C2/
curvature properties is separate. No new source regularity is hidden.

1. Reuse real nodes/row integral bounds/Λ≥1 and positive momentum integrals,
   whose sum is h. Derive h≤1; do not assume convenient coefficients.
2. Construct real source Φ from two Gaussian half-refreshes, X0=x+tP0,
   X1=X0−sum ω_ij grad f(X0_j), both endpoint sums using grad f(X1_j),
   and its actual measurable Markov kernel. Khat/Kbar stay separate.
3. Use the genuine Hessian secant integral at each X0 pair. Bound the exact
   first Picard error E_i by h²Λ D/2, D=||Δx||+||Δp||. Hence ||ΔX1_i||≤2D.
4. Construct every genuine X1 secant H_j and **actual** H=h^-1 sum b_j H_j;
   integrate positive weights to obtain symmetry, source curvature and norm≤1.
5. Expand both exact endpoint differences. Derive |1−a|≤h/2 and
   |a²−1+h|≤h² from real exponential facts, a=exp(−h/2). Show position
   residual≤(3/2)h²ΛD, momentum residual≤(5/2)h²ΛD.
6. Use the true L2 product norm, not the default product max norm. The residual
   has norm≤4h²ΛD≤8h²Λ||Δ0||. Derive a genuine pointwise bounded linear
   remainder mapping Δ0 to that actual residual via Mathlib rankOne; handle
   Δ0=0 internally. No assumed residual/operator certificate.
7. Focus compile the complete actual packet and meaningful numerical examples;
   then independent mathematics, blind decoder, source review and exact commit
   verification. Only the original sole stabilization lane may aggregate it.

Search: actual ImplementedPhaseKernel/PhaseMetric, coefficient/positivity/
HessianSecantOperator parents, current cells, Mathlib ProdL2/ProdLp, Gaussian
product kernel maps, real exponential remainder and rankOne APIs. Parent calls
must match authored proof; private implementation helpers receive no credit.

Freeze after first and two unchanged repeats of the same failure route; diagnose
statement/API issues rather than accept a supplied H, coefficient or contraction.

Boundary: V_eta producer, contraction step absorption, logΛ/B2, invariance/local
sampling error/history, stochastic actual-query cost, PBPS and both complete main
results/composition remain open. Compiled exact-gradient K semantics do not prove
the full sampler. Conceptual-mirror audit and publication are required before
PROVED_LOCAL; no new graph/citation feature blocks this mathematics.

Integrated closeout (2026-10-06): exact proof866deafe independently VERIFIED;
shared integration2dbff280, root9093/Tests9334 and95 relevant regression tests
PASS. Publication143, semantic198/8, frontier206, contributor21/21, full site
and fresh bounded graph coverage pass. Registry472 unchanged. Five structural
import/ownership edges; source and intended consumers remain nonformal overlays.
Static companion source/formula/folded Lean checked; actual rendered visual QA
and metadata copy/download delivery remain open. Main results/composition open.
