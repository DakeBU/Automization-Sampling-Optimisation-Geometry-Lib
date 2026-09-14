# Independent mathematical review, current candidate

Diagnosis: valid. No mathematical correction requested. Reviewer: independent math_verifier agent; implementation writer: root. This report applies the proof-auditor skill and records a fresh line-by-line review of the current candidate, not merely adoption of the earlier report. Commit-bound compilation and final gate verification remain pending.

## Exact scope and checked proof

The new theorem `DisplacementInterpolationConstantSpeed.wassersteinDistance_interpolation_eq_of_le_of_integrable_norm_sq` assumes probability endpoint laws with integrable squared norms, an actual optimal quadratic coupling, and ordered times $0\le s\le t\le1$. Ambient finite-dimensional real inner-product, Borel, second-countable, standard-Borel and nonempty assumptions are unchanged. It proves the requested ENNReal metric identity for actual affine pushforward laws. It neither assumes this identity nor adds absolute continuity, a map-induced coupling, density bounds or transport existence.

1. `IsQuadraticOptimalCoupling` expands to correct marginals and attainment of the actual transport-cost infimum. No target conclusion is concealed there.
2. `quadraticCost` uses the full squared norm, with no factor one-half; the distance is its infimum square root. The squared upper bound therefore yields exactly $t-s$, not a differently normalized coefficient.
3. `pointMap` is measurable; the two-time paired map is measurable. The cost proof invokes `lintegral_map` with the required measurable integrand and map. Probability of the plan follows from its left marginal, and probability of each interpolation law from measurable pushforward. Endpoints follow from the actual marginal equations.
4. The two-time mapped coupling gives the upper bound. Its exact scaling uses the affine difference and squared norm, so the reversal of the endpoint difference creates no sign problem. Taking the positive power preserves the inequality, including zero and infinity.
5. The two triangle inequalities are invoked only for probability laws. Their shared theorem does not require interpolation-law second moments; its ENNReal statement also handles infinite distances. The prefix, middle and suffix coefficients are nonnegative and sum to one.
6. The reused finite-second-moment lemma uses the independent product coupling. Coordinate squared norms remain integrable by measure-preserving projections; squared displacement is dominated by twice each coordinate squared norm. This gives finite plan cost and finite endpoint distance. Thus the actual prefix and suffix used for ENNReal cancellation are finite. No infinity is subtracted; no positive-distance division excludes zero distance or equal times.
7. The historical theorem and its module remain byte-identical to HEAD. The new theorem is isolated in `DisplacementInterpolationP2ConstantSpeed.lean`, importing the historical helper module. The focused P2ac example in `Tests/DisplacementInterpolationConstantSpeed.lean` obtains probability instances and moments from the original P2ac conjunction and derives exactly the old signature from the generalized theorem. Thus compatibility is proved as a test-level corollary, while the historical public declaration keeps its original proof. No circularity or compatibility weakening occurs; do not describe the old declaration itself as calling the new theorem.

Inspected dependencies: `DisplacementInterpolation`, `DisplacementInterpolationCost`, `WassersteinFiniteSecondMoment`, `WassersteinTriangleExact`, the historical theorem body, the new `DisplacementInterpolationP2ConstantSpeed` theorem body, and their focused tests. After the module split, I reinspected the full new proof and checked the historical module has no diff from HEAD. The tests check elaboration of the actual generalized and old public interfaces; they do not independently establish the mathematics. Standard Lean axioms must still be checked from compiled declarations at the candidate commit.

## Independent primary-source verification

Opened the official PDFs directly with the web tool during this review:

- [Statistical Optimal Transport](https://chewisinho.github.io/st_flour.pdf), Theorem 7.6, printed pp.209–210 / PDF pages215–216: arbitrary finite-second-moment probability measures, supplied optimal plan, affine displacement path and constant speed. Its proof follows the two-time coupling upper bound and endpoint triangle lower bound. The Lean theorem covers the ordered metric identity component.
- [Log-Concave Sampling](https://chewisinho.github.io/main.pdf), Theorem 1.3.23, printed p.30 / PDF page42: P2ac endpoints, a dynamic variational characterization and uniqueness of the constant-speed geodesic. The new theorem correctly distinguishes its weaker endpoint domain from that original statement.

Neither whole-source geodesic existence nor uniqueness follows from the new declaration. The declaration does not separately package a P2-valued curve or prove each interpolated squared norm integrable; this is not a missing premise for the requested metric identity, because its shared triangle theorem only needs probability normalization.

## Bounded reuse and overlap check

The candidate reuses the existing cost-scaling, exact-triangle and finite-second-moment interfaces. A fresh bounded search of pinned Mathlib's MeasureTheory subtree found no Wasserstein/displacement interpolation theorem; manifest pin is `db584cd6d46c92f209a44c0f1c829460d327499d` (v4.33.0). The shared Frontier Cell and shared-foundations searches reveal related displacement-budget routes but no competing arbitrary-P2 constant-speed theorem. This is a bounded search, not a claim about every external theorem library. Existing remote-overlap tip evidence is recorded in the earlier `math-review.md`; this reviewer has not independently refreshed those remote tips.

## Admission boundary

Mathematical/source audit: passed on the current working candidate. Commit-bound focused Lean compilation, fake-closure/axiom scan, the repository gate, and publication fidelity admission are separate required checks. No VERIFIED transition is claimed by this report.

## Commit-bound independent verification

Checked commit `b6501fd222c81c974dcad2b38376c692c212fe1f`, initially clean worktree. Focused two-thread Lean build passed (3514 jobs). Fresh printed axioms for the new and historical declarations contain only `propext`, `Classical.choice`, and `Quot.sound`. Canonical forbidden-pattern scan returned no hits; ATLAS check passed. Historical theorem module is unchanged versus the parent commit. Source/fidelity artifacts were rechecked against the independently reviewed exact component. Bounded theorem verification passes; the canonical repository gate remains a separate integration requirement. The read-only root build also passed (9026 jobs). Full Tests and the canonical state-writing gate were not rerun by this reviewer. Full details are in `commit-verification.json`.
