# Statistical Optimal Transport, Exercise 6 — Bench intake draft

This is a public-development candidate and supporting proof guide, not an
admitted question, a Lean reconstruction task, or a held-out family. Do not
include it in model inputs or score it until independent editorial admission.

## Identity and source

- Domain: Statistical Optimal Transport. Suggested family: `statot-gaussian-mixture-transport`. Keep the upper/lower subparts, constant variants and later Lean/graph views in this family; none is eligible as an unseen item after public exposure.
- Chewi, Niles-Weed and Rigollet, [*Statistical Optimal Transport*, §1.8, Exercise 6](https://chewisinho.github.io/st_flour.pdf#page=50), printed p.44 / PDF p.50, 290 pages, July 2024 preface, PDF SHA-256 `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`. [§1.2](https://chewisinho.github.io/st_flour.pdf#page=23) supplies the finite-moment setting and the Lp order.
- Original mathematical restatement and solution. No permission to export the source PDF, screenshots, or prose as benchmark data is assumed.

## Prompt-only draft

On the real Borel line let \(m>0\) and \(G_a=\mathcal N(a,1)\), with variance one.
Set
\[
\mu=\tfrac12G_{-m}+\tfrac12G_m,\qquad
\nu=\tfrac14G_{-m}+\tfrac34G_m.
\]
For \(p\in\{1,2\}\), let \(W_p(\mu,\nu)\) be the infimum over all
couplings of \((\int |x-y|^p\,d\gamma)^{1/p}\). Prove
\(m/2\le W_2(\mu,\nu)\le m\). For the lower bound, justify that
every real 1-Lipschitz \(f\) satisfies
\(\mathbb E_\mu f-\mathbb E_\nu f\le W_1\le W_2\), and choose a suitable
\(f\). For the upper bound, give an explicit coupling and check its
marginals and cost. Do not assume either an optimal coupling or a duality formula.

Provisional natural-language level **L4**: the requested answer combines the
global lower bound and a designed feasible plan, and derives the integrability
and normalization needed to connect them. This is a proposed label, not a
calibration result. The prompt-only version permits a prose proof without a
tool or source lookup. Do not reuse this answer-bearing document as an
open-library retrieval corpus. No Lean or graph difficulty label yet.

## Reference solution draft

1. Both measures have unit mass and finite second moment: for each
   \(G_a\), the second moment is \(1+a^2\), and the finite mixtures have
   nonnegative weights summing to one. A real 1-Lipschitz function has
   \(|f(x)|\le |f(0)|+|x|\), so it is integrable against both laws by
   Cauchy–Schwarz. It is measurable by continuity.
2. For every coupling \(\gamma\), its projections give the marginal
   integrals, and \(\gamma\) is a probability measure. Thus
   \[
     \mathbb E_\mu f-\mathbb E_\nu f
     =\int(f(x)-f(y))\,d\gamma
     \le \int |x-y|\,d\gamma
     \le (\int |x-y|^2\,d\gamma)^{1/2}.
   \]
   The first bound applies to every linear cost, so it also bounds their
   infimum from below. Then \(W_1\) bounds every root quadratic cost from
   below, hence bounds their infimum from below. Neither step selects an
   optimal plan. Here \(\mathbb E_\mu x=0\) and \(\mathbb E_\nu x=m/2\),
   by the means of the two components. Use \(f(x)=-x\) for the sign shown.
3. If \(Z\sim G_0\), let \(Q_{a,b}\) be the law of \((Z+a,Z+b)\).
   These are Borel pushforwards, with respective marginals \(G_a,G_b\).
   The measure
   \[
     \gamma=\tfrac14Q_{-m,-m}+\tfrac14Q_{-m,m}+\tfrac12Q_{m,m}
   \]
   has first marginal with weights \((1/2,1/2)\) and second with weights
   \((1/4,3/4)\). The shared noise cancels before taking the square. The
   quadratic cost is \(\tfrac14\,0+\tfrac14(2m)^2+\tfrac12\,0=m^2\).
   The infimum is at most the cost of this feasible plan, so \(W_2\le m\).
   This construction need not be optimal, and the bounds do not identify
   the exact distance.

## Proposed rubric (four independent points)

1. Establishes both law normalizations and finite moments, and uses
   measurability and integrability of the Lipschitz test in the joint
   expectation identity.
2. Correctly takes the two infima with the proper signs and computes the
   signed mean gap \(m/2\) using a valid 1-Lipschitz test. An equivalent
   valid all-coupling proof of the requested comparisons receives credit.
3. Supplies a bona fide coupling and verifies both marginals and the
   square-cost bound. Any valid explicit coupling with cost at most
   \(m^2\) receives credit; the displayed three branches are not required.
4. Assembles the unsquared bound with constants independent of \(m>0\),
   distinguishing feasibility from optimality and not asserting an exact
   value of \(W_2\).

## Formal evidence boundary

- Upper: `GaussianMixtureCoupling.exists_gaussian_mixture_coupling_cost`
  supplies one feasible plan with exact cost.
- Lower: `WassersteinLipschitzLower.expectation_sub_le_linearCost_and_le_wassersteinDistance`
  supplies the two reusable inequalities. The extended nonnegative
  comparison takes the nonnegative part of the signed gap, equivalent here
  because the right side is nonnegative.
- The anonymous example in `Tests/Shared/WassersteinLipschitzLower.lean`
  composes the two on the literal source distributions, supplying their
  probability, moments and means. Do not advertise the example as a named
  production declaration or an aligned reconstruction challenge. A graph
  task must use actual admitted declaration/evidence positions and a
  separately reviewed question. An induced graph path is not proof
  necessity.
