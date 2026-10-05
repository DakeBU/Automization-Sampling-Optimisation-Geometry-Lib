# Optimal gradient step from the curvature interval

Source: Chewi, *Lectures on Optimization*, arXiv:2605.07006v1 Exercise3.2,
with the Section3 C² convention and the earlier convexity/smoothness equivalences.
SAU: `ANDI-OPT-gd-optimal-step-001`.
Cells: `ASTIS-SHARED-gradient-step-endpoint-bound` and
`ASTIS-SHARED-gradient-descent-optimal-step`.
Frozen proof/lesson candidate: `81eec4b2ced5d8cd3d13a33e21a852ec7783f265`.

For a C² objective on a complete real Hilbert space, global α-strong convexity
and the β quadratic upper model in the actual gradient, the module
`Analysis/GradientDescentOptimalStep.lean` supplies:

- `gradient_step_endpoint_bound`: for h≥0,
  `‖T_h(y)-T_h(x)‖ ≤ max(|1-hα|,|1-hβ|) ‖y-x‖`, where `T_h=id-h∇f`.
  The moduli may be signed; both actual global curvature models are premises.
- `optimal_gradient_step`: for 0≤α≤β and β>0, h★=2/(α+β) gives
  factor q=(β−α)/(α+β), and q≤max(|1-hα|,|1-hβ|) for every real h.

The optimality is of the uniform endpoint envelope. It is not an assertion of
the best actual Lipschitz factor for each particular objective, an oracle lower
bound, or a convergence theorem for iterates. No minimizer is assumed or found.
For α>0, q=(κ−1)/(κ+1)<1 with κ=β/α. α=0 is a nonexpansive extension (κ undefined);
α=β>0 gives a constant update map. α≤β is explicit even in the zero space.

## Reuse and proof route

Existing `GradientDescentContraction` only handles βh≤1 and gives the weaker
square-root factor; it does not cover the balanced step in general. Existing
`ConvexSmoothGradient` and pinned Optlib `Strong_convex_Lipschitz_smooth` provide
an alternative C¹ shifted-cocoercivity route, not the source Hessian/FTC route.
The independent scoped Optlib/CvxLean audit found no exact pairwise update-map
Hessian bound. No external code is copied, and no exhaustive absence is claimed.

The proof reuses `StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn`,
`ConvexityC2.gradient_mono_iff_fderiv2_lower` and
`SmoothnessEquivalences.upper_model_iff_fderiv2_upper`. The actual Riesz Hessian
operator is symmetric by C²; the derivative of T_h is I−hH. Mathlib's
`ContinuousLinearMap.norm_eq_iSup_rayleighQuotient` bounds its norm by M_h.
The Rayleigh interval argument concerns nonzero vectors; the zero-vector quotient
is assigned zero. A continuous vector derivative along the segment is integrated
with `intervalIntegral.integral_eq_sub_of_hasDerivAt` and bounded by
`intervalIntegral.norm_integral_le_of_norm_le_const`. C² supplies symmetry and
integrability rather than adding hidden assumptions or an arbitrary Hessian field.
Finally β(1-hα)+α(hβ-1)=β-α proves the envelope lower bound algebraically.

Pinned Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`, Lean4.33.0.
The existing quadratic-regularization Riesz construction is an implementation
pattern only; that module and its audits are unchanged.

## Verification and remaining boundary

Focused production and `Tests.Shared.GradientDescentOptimalStep` pass (2869 jobs),
using only propext, Classical.choice, Quot.sound. Actual unit quadratic tests
exercise arbitrary nonnegative steps, equal moduli, and α=1,β=3; the constant
objective tests α=0 with β=1. The root Tests.lean and Analysis.lean imports are integrated before the module documentation.
Independent source-blind decoder: `gdo_blind`; proof verifier: `optimal_route_audit`;
source reviewer: `gdo_source`. Independent source/proof admission and full aggregate checks passed.
Artifacts belong in `runs/semantic-roundtrip/andi-opt-gd-optimal-step/`.

Conceptual-mirror audit: none-found. The existing curvature-growth and metric-
gradient families already retain curvature controls; balancing the two scalar
endpoints adds no new cross-domain transport. No graph-family update is justified.
The cell's generic contractive-gradient-map consumer is explicitly planned, not
an existing Lean dependency. This is textbook optimisation, not companion-paper
completion. A subsequent candidate should be selected from the live source/DAG;
no additional theorem is claimed in this cycle.

## Integration notes

Independent source and proof admission accepted, with disclosed domain-mismatch
(Hilbert/parameter extensions) and no repair proposal. Root imports and Registry
entries are integrated (418 local leaves). Full gate, generated branch checks and
reader visual inspection passed as recorded below.


- Aggregate candidate `9f461668e6db0c43ebc1fbe9af67acda3f46a64f` passed the canonical
  gate at `2026-09-13T01:54:17.958018+00:00`: 9204 jobs, including root Tests.Basic
  and Tests, fake-closure scan, ATLAS36469 declarations/26 books. Copied exact
  source-bound evidence: `runs/semantic-roundtrip/andi-opt-gd-optimal-step/canonical-gate-evidence.json`.
- Publication diff check PASS78 source items, semantic check PASS94 audits/6
  existing repairs, frontier check PASS102 cells. Old92 audit objects and old
  source items are unchanged. Two new declarations, their source item and lessons
  are added; no source repair is needed. Registry count418 is local leaves,
  not a source/book/companion-completion count.
- Generated site build/check PASS673 modules,3995 declarations,418 local leaves.
  Both affected `graph-check --cell` calls pass. Graph delta: the production and
  test modules are present; two new declarations share the actual production
  owner, chapter03 source binding and separate semantic audits. The endpoint
  scanner reference to the optimal-step theorem is dashed, not an elaborated
  dependency certificate. Existing lower/upper Hessian interfaces are reused.
- Reader: `libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-2`.
  Focus: `lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step&q=AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step`.
  Root inspected actual rendered reader at desktop1280/mobile390: formulas,
  hypotheses, accepted domain-mismatch disclosures, all4 initiallyclosed Lean
  disclosures and the opened optimal statement/proof. KaTeX errors0; document
  width equals scrollWidth (1265 desktop,375 mobile). Long mobile formulas use
  their own horizontal scroll area. Focused branch10nodes13edges4highlighted
  relations: solid module ownership and dashed scanner/source/audit edges are
  visually distinct. Mobile node detail has the full wrapped name, compiled badge
  and readable source/reference panel. This is root visual evidence, not the
  independent verifier's own screenshot inspection. No layout code changed.
- Remaining boundary: uniform C² curvature-envelope optimization only. No new
  conceptual mirror or actual planned generic consumer is certified. Any further
  optimal-step iterate bound or C¹ extension needs a separately scoped source/DAG
  delta; the rest of the chapter remains incomplete.

Merged and pushed directly to `main` at `d8bcc55fe0b5a69d62b53a7285d37fcebf0b83be` under standing user authorization. SAU is `MERGED`; stabilization reservation released. Remote post-push CI/deployment is separate from the passed local gate evidence.
