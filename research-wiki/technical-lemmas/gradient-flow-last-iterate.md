# Convex gradient-flow Lyapunov and last-time upper bounds

SAU ANDI-OPT-gradient-flow-last-iterate-001; cell ASTIS-SHARED-gradient-flow-last-iterate.
Source Chewi2605.07006v1 Exercise2.1 upper-bound component; no companion credit.
Reuse ConvexityC2 and StrongConvexFirstOrder, plus Riesz derivative pattern from
GradientDescentOptimalStep. Hessian sign and actual gradient derivative derived;
no supplied Hessian positivity or scalar Lyapunov dissipation premise.
Differentiate L=t²normgrad²+2tgap+distance², cancel terms, use convex support;
right K0 scalar comparison gives antitone L on[0,T]. Drop nonnegative terms
for gradient²<=D0/t²; support+Cauchy+Young gives4tgap<=L<=D0 and gap<=D0/(4t).

C2 Hilbert generalization explicit; minimum and actual flow supplied. Positive
time only for normalized rates, closed Lyapunov includes0 and T0. Nonsmooth
positive-part sharpness witness remains an unbound source obligation; do not
mark full Exercise2.1 complete. No Exercise2.2 or existence claim.
Conceptual-mirror audit none-found: existing metric-gradient-flow family and
convex energy-distance mechanisms already retained. No new transport edge.

Focused tests, independent reviews, full gate and reader/graph checks pending.
Preserve unrelated local files. Next candidate: inspect the Exercise2.1
positive-part sharpness witness with its local smooth-arc/global C2 boundary.
