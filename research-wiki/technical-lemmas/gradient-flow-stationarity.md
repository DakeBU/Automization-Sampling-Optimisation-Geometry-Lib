# Gradient-flow stationarity on a compact time interval

SAU ANDI-OPT-gradient-flow-stationarity-001; cell ASTIS-SHARED-gradient-flow-stationarity.
Source Chewi2605.07006v1 Section2, Lemma2.1 and Corollary2.8.
User-directed optimisation continuation; no companion-paper completion credit.

Reuse compact minimum and scalar K0 right-slope comparison. C1 gives gradient
continuity via fderiv and Riesz inverse. Choose minimum m, derive actual energy
derivative=-normgradient²<=-m², compare endpoints and use supplied minimum.
Divide by T>0 and take sqrt. Exact source coefficient1; no convexity or PL.
Existing PL theorem has unwanted PL/positive-curvature assumptions, hence is
not imported as an unconditional dissipation helper. MVT requires two-sided
interior derivatives; existing right-slope comparison directly fits this API.
The independent route audit considered a terminal-lower-bound generalization;
final theorem retains the source global minimizer instead.

Truth boundary: C2 Euclidean source generalized to C1 Hilbert and right-time
finite interval. Positive time implicit in finite quotient; no t0 convention.
No flow/minimum existence, final-time gradient estimate, infinite-time sequence,
trajectory convergence, discrete algorithm or stochastic transport theorem.
Conceptual-mirror audit none-found: existing metric-gradient-flow family and
prior gradient-descent-stationarity memory already retain energy-budget
averaging. No new cross-space bridge or coercivity implication.

Focused tests, independent proof/source audits, root Tests import, full gate,
reader and graph checks pending. Preserve unrelated local files.
Next candidate: source Exercise2.1 last-time convex gradient bound, after
retrieval and differentiable-gradient/Hessian interface audit.
