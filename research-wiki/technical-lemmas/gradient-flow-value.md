# Convex gradient-flow objective rate

SAU ANDI-OPT-gradient-flow-value-001; cell ASTIS-SHARED-gradient-flow-value.
Source: Chewi2605.07006v1 Theorem2.4. User-directed optimisation continuation;
no companion-paper theorem credit. Reuse shared first-order convex support.

Actual chain rule derives objective decrease using scalar right-slope Gronwall
on every subinterval with K=epsilon0. Differentiate squared distance to the
supplied minimizer, then use first-order support and objective decrease to
freeze the terminal gap in constant negative forcing. Scalar (not norm) Gronwall
permits that negative forcing. K0 gives D0/(2t); K=-alpha gives
alpha*D0/[2(exp(alpha*t)-1)]. No scalar comparison or generic integral reproof.

Source endpoint: printed t>=0 is singular at0 for both coefficient branches.
Keep original source wording; formal theorem uses positive observation time.
Quadratic exp(-t) actual flow at0 gives gap1/2, while Lean total quotient is0.
A separate exact-proposal review is required for the positive-time domain
clarification. No analytic alpha-to-zero limit theorem is claimed. Hilbert/
differentiability/right-time generalizations and supplied minimum remain clear.

Conceptual-mirror audit none-found: existing metric-gradient-flow/curvature-growth
families already retain distance-energy scalar comparison; no new transport.
Frozen proof, tests, independent decoder/source/repair audits and publication
checks pending; remember root Tests import and explicit elan/Homebrew PATH for
full harness localhost tests. Existing unrelated local files remain excluded.
Next candidate after this packet: inspect Chewi Corollary2.8 gradient-norm
consequence and existing actual-flow dissipation/integral interfaces before
choosing another reachable theorem edge.
