# Exact quadratic-gradient trajectories

Source: Chewi arXiv:2605.07006v1 Exercise3.3 (Section3 GD convention).
SAU `ANDI-OPT-quadratic-gd-001`; cells
`ASTIS-SHARED-quadratic-gradient-iterate` and
`ASTIS-SHARED-quadratic-gradient-eigenmode`.
Proof/lesson candidate `14b1bcffa4208b16884a8e3f39599f9932bb102c`.

For symmetric continuous linear H on a complete real Hilbert space, the actual
objective f(x)=⟨x,Hx⟩/2 and update T_h(x)=x−h∇f(x) satisfy:

- `quadratic_gradient_iterate`: T_h^[N](x)=(I−hH)^N x.
- `quadratic_eigenmode`: if Hx=μx, then T_h^[N](x)=(1−hμ)^N x,
  its norm is |1−hμ|^N‖x‖ and its objective value is (1−hμ)^(2N)f(x).

The gradient is derived internally from the true quadratic, not assumed as an
oracle identity. Differentiation of the inner product and symmetry give
Df(x)[v]=⟨Hx,v⟩. Reuse Mathlib `FunLike.coe_pow_eq_iterate` and
`Module.End.HasEigenvector.pow_apply`, splitting x=0 before requiring a nonzero
Mathlib eigenvector. Norm and quadratic homogeneity give the other equalities.
Lean4.33.0; pinned Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.

## Retrieval and source boundary

Samplinglib's existing GD results supply inequalities, not these identities.
Optlib5da27c5 LASSO.quadratic_gradient and ADMM.Gradient_of_quadratic_forms treat
squared norms of Ax using A†A; inspected CvxLean c62c2f has spectral algebra but
no matching actual GD trajectory. No external code is copied; the search is
bounded, not an exhaustive absence claim. Canonical derivative/eigenvector
results are reused rather than re-proving linear-algebra power induction.

Positive-definite Euclidean source matrices specialize the symmetric Hilbert
operator statement. Arbitrary real steps, indefinite/zero H, N=0 and x=0 are
legitimate identity domains, not enlarged convergence claims. A supplied mode
relation does not prove the existence of spectral endpoint eigenvectors in
infinite dimensions. To witness a nonzero sharp factor, x≠0 is essential.

Tests use the actual diagonal matrix diag(1,3) and each orthonormal basis vector:
at h=1/2 both norms equal (1/2)^N, with opposite signs on the high mode. A unit
scalar quadratic at h=3 has norm 2^N‖x‖ and value 4^N f(x), demonstrating that no
stability premise is hidden. Zero H and arbitrary h,N exercise the initial-point
identity. Focused build PASS2470, standard axioms only. Independent proof and source admission accepted. The canonical full Lean gate
passed, including root Tests/Tests.Basic and fake-closure scanning.

Conceptual-mirror audit: none-found. This step exposes exact scalar evolution of
an existing quadratic gradient mechanism, without constructing a new transport
between optimization, Markov spectral theory or other domains. Planned §5
polynomial-method reuse is not an existing compiled consumer or an oracle lower
bound. The publication leaves the full Section3 sharpness comparison uncovered.

## Integration notes and next boundary

Independent proof/source admission, root imports, Registry420 and the canonical
ASTIS gate passed. Site/graph checks and actual reader/branch inspection passed. Do not repeat
this trajectory target once admitted. Further work should select a new exact
source obligation, such as the remaining sharpness comparisons or a quadratic
polynomial consumer, after its own dependency and reuse audit. Neither companion
paper nor the full chapter is completed by these two declarations.

Full gate candidate `b1671576cf72e13aab55d2e861816e2233000064`, generated at `2026-09-13T02:43:24.013711+00:00`,
source digest `266dd142a92b2dae9730e56f71b82d63973496bb4b2d8a46ebf9f2f52290f01f`. Exact canonical JSON is retained with the
round-trip artifacts; it is not a substituted focused-build certificate.

- Independent proof verifier `quadratic_route_audit`, blind decoder `qgd_blind`,
  source reviewer `qgd_source`. Both fresh source reviews accept the bounded
  components with `lean-weakened-conclusion`: the whole exercise conclusion is
  broader. No source repair is needed; source generalizations remain explicit.
  Integration review preserves all94 prior audits and9 prior optimisation source
  items byte-for-byte as objects; no prior production module changed.
- Canonical gate PASS9206 jobs, including root Tests/Tests.Basic; fake-closure
  scan and ATLAS36469 declarations/26books passed. The new test root import is
  before the module documentation. Registry420 counts local leaves, not completed
  textbook or paper results. Publication PASS79 items; semantic PASS96 audits/6
  existing repair proposals; Frontier PASS104 cells.
- Site build/check PASS675 modules,4000 declarations,420 local leaves. Both
  affected graph-check calls passed. Graph delta adds production/test modules,
  two public declarations, chapter03 correspondence and their independent audits.
  The existing name scanner detects iterate → eigenmode, shown dashed; module
  ownership is solid. The planned Section5 consumer is not a compiled dependency.
  No conceptual mirror or completion badge was authored.
- Reader: `libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-3`.
  Graph focus: `lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent.quadratic_eigenmode&q=AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticGradientDescent.quadratic_eigenmode`.
  Root inspected actual desktop1280/mobile390 reader, both formula statements,
  assumptions, limitations, four initiallyclosed Lean disclosures and opened
  eigenmode statement/proof. KaTeX errors0; width=scrollWidth1265 desktop,375
  mobile. Long mobile formulas scroll within their own container. Focused
  branch7nodes9edges4highlighted relations has distinct solid/dashed edges;
  mobile node detail wraps the full name and shows compiled badge and references.
  This is root visual evidence, not the independent reviewer's own visual check.
  No layout code changed. Temporary preview tabs/server are closed after review.
- Next boundary: audit and select one remaining Exercise3.3 sharpness comparison
  or source Section5 polynomial consumer. Reuse these identities; do not repeat
  this target. Full-section sharpness, general endpoint existence and companion
  paper results remain unproved by this contribution.

Final metadata-only site regeneration/check passed; both bounded graph reports
are byte-identical to the inspected versions. Current Lean source digest still
matches the canonical gate. Independent integration review is retained at
`runs/semantic-roundtrip/andi-opt-quadratic-gd/integration-review.json`.

Merged and pushed directly to `main` at `1a7beeef7ef740fda474ff2896ba8334611b41dd` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.
