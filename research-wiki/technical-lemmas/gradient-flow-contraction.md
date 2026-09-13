# Two actual gradient flows: contraction

SAU ANDI-OPT-gradient-flow-contraction-001; cell ASTIS-SHARED-gradient-flow-contraction.
Source: Chewi2605.07006v1 Definition1.5 / Theorem2.2.
User-directed optimisation continuation; no companion-paper theorem credit.

Reuse StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn.
Subtract actual right ODE derivatives, differentiate squared norm (safe at zero
separation), apply monotonicity, then existing finite-interval right-slope
Gronwall. The squared bound has rate2alpha and the norm bound ratealpha.
Alpha>=0 preserves the source convention; zero is nonexpansive. No attained
minimum, gradient Lipschitzness, nonzero distance or negative-time dynamics.
Complete Hilbert / differentiable / right-time hypotheses are explicit source
generalizations. Curves are supplied; no existence/extension theorem.

Conceptual-mirror audit: none-found. Existing metric-gradient-flow and curvature
growth families cover this mechanism; no new transport or stochastic certificate.
Focused tests derive actual quadratic trajectories for arbitrary initial points,
including coincident points and t0; separate zero-curvature test. Root Tests
import, independent audits, full gate, reader and graph inspection pending.
Next candidate: source Theorem2.4 objective rate, with alpha0 limiting case
handled explicitly, after searching existing convex-flow energy interfaces.
