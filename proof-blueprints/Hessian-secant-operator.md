# Genuine Hessian secant operator

Source: SPHMC arXiv:2609.06906v1 Lemma 4.6, proof at the actual
`H(x,x') = integral_0^1 Hessian V_eta(x'+t(x-x')) dt` (HTML568–572).
Shared planned consumer: Chewi arXiv:2605.07006v1 Proposition 1.6 / Exercise 3.2.
Neither downstream source consumer is declared completed by this leaf.

For a C² real potential on a complete real Hilbert space, form the Riesz operator
of the **genuine second Fréchet derivative**, and integrate it in ordinary
Lebesgue measure along the unit parameter segment. For signed global diagonal
bounds α, β, prove gradient difference = the actual integral operator applied to
the displacement, symmetry, inherited diagonal bounds, and norm ≤ max(|α|,|β|).
The finite Euclidean source case α=1/(2κ), β=1 is included. C² / completeness
are explicit; continuity, measurability and Bochner integrability are derived.
There are no supplied matrix, secant identity or integrability premises.

1. Use Mathlib's `continuousLinearMapOfBilin` for the actual Hessian.
2. Derive continuous operator field from C² and the continuous Riesz map.
3. Derive its interval integrability, commute evaluation and inner pairing.
4. Apply FTC to the derivative paired with an arbitrary test vector.
5. Use genuine C² second-derivative symmetry for the integrated operator.
6. Integrate the two actual pointwise diagonal bounds on the unit interval.
7. Use the symmetric Rayleigh norm formula for the signed endpoint bound.

Searched: Analysis module card, ConvexityC2 diagonal pairing FTC,
GradientDescentOptimalStep private point-H field, pinned Mathlib Dual/Gradient/
FDeriv.Symmetric/Rayleigh/IntervalIntegral APIs, existing shared/companion cells.
No canonical all-vector integral secant producer found. No ASTIS theorem is
claimed as called merely because its mathematical mechanism informed the route.

Failure policy: freeze a route after the first and two unchanged repeats;
diagnose a missing assumption, representative, API issue or oversized target.
Never replace the real integral by a supplied operator certificate.

Boundary: genuine C² interface only; V_eta smoothing/curvature production,
actual positive-weight average at Picard nodes, remainder expansion, kernel
contraction, stochastic bias/variance/history, PBPS and both main results remain
independent. Independent actual mathematics, source-blind reconstruction and whole-module
source review pass; exact independent verification 2bb8e47850aab5a519f6c07e6bffc658443a4677.
Shared integration b3d4e8cb2ee58f42b59f8aa4cacbe4eb55c41a2c passes canonical aggregate,134 regressions,
reader/graph and metadata gates. Final bounded graph freshness and complete site/contributor checks pass;
pushed-head CI remains separate. Both full main results/composition stay unfinished; Goal active.
