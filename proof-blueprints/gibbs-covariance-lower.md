# Gibbs covariance lower and actual smoothed Hessian upper

SPHMC arXiv:2609.06906v1 Section4.1 Lemma4.1 Cramer-Rao half; equation4.1; Chewi auxiliary 20261006 main.pdf Theorem3.5.8/Corollary3.5.9 zero-based pages124-125

For genuine C2 alpha I<=Hess U<=beta I, alpha>0, prove actual Gibbs probability and identity L2 and Cov_mu(v,v)>=norm(v)^2/beta for every v. Apply to actual RGO posterior V+quadratic precision eta^-1 and derive actual source unnormalized V_eta Hessian<=beta/(1+beta eta) for every observation/direction.

Samplinglib GibbsGradientMoment actual gradient L2 and private weighted_gradient/directional_ibp; GibbsPositionMoment private coordinate IBP; QuadraticRegularization and StrongConvexGibbsIntegrability. Extend existing canonical module, preserve old public gradient theorem.

Samplinglib GaussianConvolutionRegularity actual selected posterior covariance/Hessian identity, SmoothedGibbsPotential exact unnormalized potential constant; source consumer cannot import Tests.

Samplinglib/frontier cells and pinned Mathlib CovarianceBilin, L2Space, full-space directional IntegrationByParts, StrongConvexFirstOrder searched. Poincare interface is not a producer; no existing covariance lower or BL criterion. Source dependency audit SPHMC_4_1_covariance_dependency_audit.md retains separate halves.

Route: derive actual Gibbs probability/score L2 from canonical parent; strong gradient monotonicity at zero derives position L2 without minimizer; centered linear observable and actual directional score are L2 and their product integrable; full-space IBP derives expected product one and expected score square<=beta; integrate (score-beta*position)^2 and scale nonzero directions, handling zero first; derive actual quadratic posterior Hessian alpha+eta^-1..beta+eta^-1 and actual tilted_tilted measure; use actual unnormalized potential constant and covariance Hessian to get beta/(1+beta eta).

No supplied position/score moments, minimizer, covariance, score identity, normalizer or well-behaved certificate. Linear-test covariance corollary only, not full nonlinear Cramer-Rao. Coordinate IBP background moves into canonical TechnicalLemmas; historical existing consumer remains untouched. Whole-module old/new independent review is required.

Actual Gibbs all-direction covariance lower bound and its actual RGO/source V_eta Hessian upper consumer only. No Brascamp-Lieb covariance upper/Hessian lower, full Lemma4.1, general nonlinear Cramer-Rao, higher regularity, exact stationarity, approximate/stochastic/history work, PBPS process or either complete main/composition. TV never transfers unbounded expected cost.

Integrated closeout (2026-10-06): Exact proof 396f024b8c3f5a885530ecbf918b5c8465793293 independently VERIFIED; shared integration 8dcb59ea4ba9279ac4348fe3c49e985cc6fb072e. Full ASTIS gate PASS (9100 root / 9348 Tests), publication155, semantic215/8, frontier218, contributor38/34. 95 relevant Python regressions reused after exact unchanged tool/fixture/runtime checks; not rerun for this pure Lean/metadata packet. Original reader static source/formula/proof/folded-Lean/Test/residual and three affected actual graph branches checked; full site and official graph freshness/contributor checks PASS. Graph816 modules/601 public declarations; Registry472 unchanged. Rendered visual and metadata copy/download acceptance remain open. Both complete main results/composition remain unfinished.
