# Actual source smoothed Gibbs potential

One integration-node SAU ASTIS-SA-20261006-SPHMCSmoothedGibbsPotential; root sole production writer and original sole stabilization/PR313 lane. Exact primary2609.06906v1 equation1.1, Section3.1 HTML237 and Section4.1 HTML403-412. V is explicitly C2 in the primary; genuine lower Hessian alpha>0 suffices. Upper Hessian/eta cap are unnecessary here and their omission is an explicit generalization.

Shared floor: exact GaussianConvolutionRegularity independently VERIFIED6e84711c/integrated a72fc720; HessianStrongConvexity and StrongConvexGibbsIntegrability reused unchanged. Existing actual Gibbs augmentation and smoothed initialization do not prove source V_eta/partition equivalence. Pinned Mathlib actual Tilted/withDensity/Bochner/ENNReal/log APIs searched. No assumed minimizer, Gibbs normalization, covariance or supplied smoothness.

Target: C_eta=(sqrt(2pi eta))^(-dim E), A_eta(y)=C_eta integral exp(-V(x)-norm(y-x)^2/(2eta))dx, V_eta=-log A_eta. Derive Z_V>0, original probability, actual smoothed density exp(-V_eta)/Z_V, integrable A_eta with integral Z_V, actual smoothed Gibbs tilt, V_eta C2, and normalized U_eta=V_eta+log Z_V.

Route: (1) true lower Hessian to strong convexity and Gibbs integrability; (2) positive Z_V and original normalized probability; (3) apply actual shared Gaussian density/C2 producer; (4) integral_tilted gives C_eta Z_mu=A_eta/Z_V everywhere; (5) actual smoothed probability total mass plus nonnegative measurable density derives integrability and integral A_eta=Z_V; (6) identify actual source Gibbs tilt; (7) positive log_div and constant subtraction give source V_eta C2/exact normalization convention.

Failure policy: no statement mutation for namespace or coercion errors. Ignored prototype diagnosis resolved ofReal congruence, namespace (sections are not namespaces), and explicit derived pushforward probability instance; no added mathematical premise. A real repeated-route failure must publish a reduced blocker. Private prototype output is not admitted formal truth.

Conceptual mirror none-found: source normalization adapter of the same augmentation. Score/covariance/posterior moments, Brascamp-Lieb/Cramer-Rao/Hessian bounds, higher derivatives, stationarity/accuracy/work, PBPS process and both full main/composition remain open. TV never transfers unbounded expected cost.
