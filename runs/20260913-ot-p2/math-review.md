# Independent mathematical review: arbitrary-P2 ordered constant speed

Diagnosis: valid mathematical generalization in the reviewed working diff. No mathematical correction requested. This is a pre-commit source and proof audit, not commit-bound verification or a VERIFIED transition. Reviewed base HEAD: `706aa85d185488abf957e31e18fc0e0e6f94c655`; candidate commit and compiler/gate evidence remain pending. Reviewer is independent of the implementation writer. Review applied the proof-auditor skill checklist for assumptions, line-by-line implications, normalization and source labels.

## Exact claim and proof audit

The new declaration `DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq` takes probability endpoint laws on a finite-dimensional real inner-product space, Borel measurable structure, the displayed second-countability/standard-Borel/nonempty instances, integrable squared norms, a supplied optimal quadratic coupling, and $0\le s\le t\le1$. It proves $W_2(\mu_s,\mu_t)=(t-s)W_2(\mu_0,\mu_1)$, represented in ENNReal. It does not assert existence of an optimal plan or full geodesic-space structure.

- Normalization: `quadraticCost z = ENNReal.ofReal (norm (z.1-z.2)^2)` and distance is the square root of its coupling infimum. There is no factor one-half in this W2 definition. Squaring/rpow monotonicity preserves the exact coefficient.
- No circularity: `IsQuadraticOptimalCoupling` is the conjunction of correct marginals and equality of endpoint plan cost with the transport infimum. It contains no interpolation metric identity, continuity, finiteness or geodesic conclusion.
- Measurability and mass: affine `pointMap` and paired map are measurable; `lintegral_map` is used with both measurability proofs. Left endpoint probability plus the coupling gives probability of the plan, hence probability of each mapped interpolation law. No absolute continuity is used here.
- Upper bound: the canonical two-time coupling has cost $|s-t|^2$ times endpoint cost, giving the distance bound by monotonicity of the positive square. The sign reversal in point-map differences disappears under the squared norm.
- Lower bound: two valid probability-law triangle inequalities bound the endpoint distance by the three segments. Nonnegative coefficients $s,t-s,1-t$ sum to one. Endpoint finite second moments imply finite W2 via the independent product coupling, with domination by twice each endpoint squared norm. Both prefix and suffix are strictly below infinity before ENNReal cancellation. No subtraction of infinite quantities occurs. Degenerate cases $s=t$, endpoint times, and zero endpoint distance remain covered without division.
- Second-moment scope: the result does not separately certify integrability of every interpolation law or bundle a P2-valued curve. Its triangle dependency only needs probability measures. This is sound for the stated metric identity; a stronger P2-path interface would need that additional explicit result.
- Ambient assumptions specialize to the source Euclidean space and do not add density, smoothness or positivity restrictions on measures. They should not be advertised as an arbitrary metric-space theorem.
- Compatibility: the original theorem retains its P2ac signature and obtains its probability instances and integrability from the original conjunction. Its proof invokes the new theorem, so there is no cyclic dependence.

## Independently checked sources

Official author PDF https://chewisinho.github.io/st_flour.pdf downloaded and SHA256 recomputed: `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`, matching Libraries/StatisticalOptimalTransport/source-map.json. Theorem 7.6, printed pp.209-210, PDF pages215-216 (one-based), states the arbitrary-W2 displacement path is a constant-speed geodesic, using a supplied optimal transport plan. Its proof gives the two-time coupling upper bound and endpoint triangle lower bound. This implementation covers the ordered metric identity component; the source also asserts existence of geodesics, outside this declaration.

Official author PDF https://chewisinho.github.io/main.pdf downloaded and SHA256 recomputed: `8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`. Theorem1.3.23, printed p.30/PDF page42, explicitly assumes P2ac endpoints and describes affine interpolation of optimally coupled random variables, as a unique constant-speed geodesic. Its dynamic variational formula, uniqueness and optimal-plan existence are not proved here. Removing absolute continuity is correctly attributed to Statistical Optimal Transport rather than silently weakening Chewi's source domain.

## Bounded reuse and overlap audit

Searched ASTIS measure technical lemmas, Mathlib/MeasureTheory, frontier-cell records and Libraries/shared-foundations.yml for Wasserstein, displacement interpolation and constant speed. Existing finite-moment, coupling-cost, exact-triangle and Chewi wrappers supply the necessary parents; no other arbitrary-P2 constant-speed declaration appeared. Mathlib search yielded no matching Wasserstein/displacement theorem in the bounded measure subtree; this is not a claim about all external libraries.

Read remote-overlap source and independently checked live `git ls-remote` tips. `origin/wasserstein-displacement-constant-speed-ordered` is `83f960e3124a7ec180dd07222e69cc4cbb30532c`; its ordered theorem requires P2ac. `origin/wasserstein-displacement-geodesic-full` is `754c0be64b0d382ad10108350af367f9d48e43e8`; its actual file is DisplacementInterpolationGeodesic.lean, whose arbitrary-time metric theorem still requires P2ac. These branches do not already supply the proposed generalized endpoint domain. The local cell ASTIS-SHARED-displacement-interpolation-p2 is the new ownership record, not independent proof evidence.

## Pending

Await candidate commit, then bind independent Lean/source and fake-closure verification to that commit. This report makes no build, full-gate or publication-admission claim.
