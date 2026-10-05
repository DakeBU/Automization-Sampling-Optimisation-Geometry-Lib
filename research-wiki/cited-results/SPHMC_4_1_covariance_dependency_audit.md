# SPHMC Lemma 4.1 covariance dependencies

2026-10-06. This is a source/dependency audit and next-target plan, not a proved
covariance inequality. Preserve the existing companion and Chewi frontiers.

Primary anchor: [SPHMC2609.06906v1 Section4.1](https://arxiv.org/html/2609.06906v1#S4.SS1),
HTML413-430. The source uses two different inequalities for the actual RGO law
with potential W_y(x)=V(x)+norm(x-y)^2/(2 eta), with eta>0 and source Hessian
kappa^-1 I <= D2V <= I. Its Hessian lies between a=kappa^-1+eta^-1 and
b=1+eta^-1. Brascamp-Lieb gives Cov(R_y)<=a^-1 I, whereas Cramer-Rao gives
Cov(R_y)>=b^-1 I. Substituting the genuine equation4.1 identity reverses the
respective directions and gives (kappa+eta)^-1 I<=D2V_eta<=(1+eta)^-1 I.
The source states this for eta<=1. No covariance certificate may be assumed
in place of either producer.

The source cites Brascamp-Lieb1976 and Chewi, *Log-concave sampling*,
Theorem3.5.8. The currently retrieved author PDF at
https://chewisinho.github.io/main.pdf has 333 pages; PDF pages124-125
(zero-based indices) contain Theorem3.5.8 and Corollary3.5.9. The book says
"well-behaved" test functions: a Lean port must derive the weighted
integrability and full-space integration-by-parts hypotheses explicitly for
linear tests. This live background copy is auxiliary evidence, not a mutation
of the project's older pinned Chewi edition or completion state.
The auxiliary downloaded bytes are cached at `.astis/chewi-20261006-covariance.pdf`,
SHA256 `8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`;
local pypdf extraction confirmed Theorem3.5.8 on zero-based page124. This cache
does not overwrite a pinned book source and is not a Lean dependency.

Pinned local environment: Lean4.33.0, Mathlib
db584cd6d46c92f209a44c0f1c829460d327499d. Search results:

- GaussianConvolutionRegularity now has a locally compiled, independently
  mathematically checked actual posterior probability/L2 and true score/covariance
  producer. Its fresh source/exactcommit admission is still pending at this audit.
- GibbsGradientMoment.gibbs_gradient_moment is a compiled ideal-Gibbs producer:
  genuine C2/positive lower and upper Hessian imply weighted gradient integrability,
  a total score-square/diagonal-Hessian identity and beta-times-dimension bound.
  Its private directional_ibp already proves the precise directional weighted
  score identity. The public trace bound alone loses the required dimension-free
  directional constant and is not a covariance inequality.
- GibbsPositionMoment contains a private coordinate_position_ibp yielding the
  position-score pairing. Its public result assumes a critical point and gives
  d/alpha total position control. It is not a sharp directional covariance bound;
  a reusable background producer belongs in TechnicalLemmas, not another paper copy.
- Pinned Mathlib full-space integral_mul_fderiv_eq_neg_fderiv_mul_of_integrable,
  tilted_tilted, actual integral_tilted, L2 and centered covariance APIs are available.
- FunctionalInequalities/Poincare.lean defines an explicit Satisfies interface;
  variance_le consumes an inequality assumption. It proves no curvature-to-Poincare
  or Brascamp-Lieb criterion. Searches of pinned probability and ASTIS technical
  lemmas found no Cramer-Rao or Brascamp-Lieb covariance producer.
- RGOCalculus and QuadraticRegularization provide genuine regularized curvature,
  Gibbs integrability and actual iterated-tilt identities, not covariance bounds.
  SLT is not an imported proof dependency; no uncompiled external candidate is admitted.

Classification: both inequalities are external-cited-result dependencies with
missing ASTIS-owned analytic producers. The lower bound has a short local-lemma
route using actual weighted directional integration by parts. The upper bound
still needs a genuine Brascamp-Lieb/curvature-to-Poincare producer or a separately
source-reviewed equivalent mathematical route. These remain separate obligations.

Next candidate shared target: for finite-dimensional Borel real Hilbert E,
actual mu=volume.tilted(-W), global C2 and 0<alpha<=beta with
alpha norm(v)^2<=D2W(x)[v,v]<=beta norm(v)^2, derive probability, id in L2(mu)
and covarianceBilin(mu)(v,v)>=norm(v)^2/beta for every v, including dimension zero.
Proposed name: TechnicalLemmas.Analysis.GibbsCovarianceLower.gibbs_covariance_lower;
canonical file/name may be reconciled with the existing GibbsGradientMoment
producer before claiming the SAU. No minimizer, covariance, score identity,
normalizer or integrability certificate is an input. A source Test must apply
to the actual W_y and show its law equals the selected Gaussian posterior.

At most seven proof steps:
1. Reuse genuine strong-convex Gibbs normalization and Gaussian tail domination.
2. Derive actual position L2 and weighted score/product/Hessian integrability.
3. Reuse/generalize the existing exact directional score-square/Hessian IBP.
4. Prove actual centered linear-position/score pairing E[r a]=norm(v)^2 by IBP.
5. Set r=inner(v,x-E_mu X) and a=DW(x)[v]; derive E[a^2]<=beta norm(v)^2.
6. Integrate (a-beta r)^2>=0, giving beta^2 E[r^2]>=beta norm(v)^2;
   divide by positive beta and identify the actual centered covariance.
7. Apply genuine quadratic-regularization/iterated-tilt parents to the source
   posterior and retain the independent Brascamp-Lieb upper-bound obligation.

Failure policy: inspect exact integrability, normed dual instances and IBP
representatives after repeated same-shape failures; do not add a supplied pairing
or covariance hypothesis. A directional lower bound is not full Lemma4.1,
source quantitative curvature, dynamics, either main result or composition.
