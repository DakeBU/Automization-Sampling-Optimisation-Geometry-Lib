# Strong convexity and nonlinear numerical PL pullback

Source: Chewi arXiv2605.07006v1 Exercise2.3, Definition2.5 and Section2.
SAU ANDI-OPT-pl-pullback-001; cell ASTIS-SHARED-strong-convex-pl-pullback.

The actual derivative A=Dg maps E to F; source Jacobian J is its adjoint.
Coercivity of A A-adjoint gives sigma times the base gradient square.
StrongConvexFirstOrder + Cauchy-Schwarz + completing a square gives
2alpha(f(gx)-fz)<=norm(gradient f(gx))². The chain rule identifies the true
composite gradient with A-adjoint gradient f(gx). Surjectivity supplies one
minimizing preimage of the supplied attained base minimum. Multiply by sigma>=0.

This is a numerical inequality, not an assertion of the whole C1 positive-modulus
Definition2.5 package. Exercise wording leaves continuity of Dg and positive
sigma implicit/unstated. Sigma0 is degenerate; general differentiability and
Hilbert spaces are explicit extensions. No composite convexity, unique/minimum
multiplicity, algorithm rate, matrix-coordinate certificate or paper completion.
The initial proposed C1 target was refined before proof admission after the
independent source audit: retain the precise numerical component without adding
continuity merely to claim full definition coverage.

Reuse: ASTIS first-order bound and pinned Mathlib adjoint, Riesz and Frechet chain
rule APIs. Optlib/CvxLean bounded searches in canonical upstream-review.json.
Compiler diagnosis: chain rule point argument and adjoint orientation are explicit;
normalize Riesz derivative equality without inventing a gradient premise.

Conceptual-mirror audit: none-found. This is an actual compiled within-Hilbert
pullback mechanism, not new evidence for a Riemannian or measure-space transport.
Existing gap-gradient family retained; no invented cross-domain bridge.

Focused compilation PASS2458, with actual nonlinear g(x)=x+x³ and f(t)=t²/2.
The test proves surjectivity by the intermediate value theorem, the nonconstant
derivative 1+3x², and sigma1 operator coercivity; it consumes the composite
inequality at the constructed minimizing preimage. Standard axioms only.
Independent proof/source review accepted the scoped numeric component. Full gate PASS9212, source-bound JSON retained; publication82, semantic99/6, frontier107 and site/graph checks passed. Next consumer: use a supplied upper model only when deriving GD rates;
PL does not imply gradient Lipschitz smoothness. Keep full definition regularity
and positive-modulus source obligations separate.

## Publication and integration evidence

Frozen proof/test/lesson commit7dc67252227d5fb4d05018526c4b965eb722e47d;
independent verifier pl_pullback_review. Anonymous decoder decode_57329 and
anti-anchored source reviewer pl_source_57329 accepted the scoped component:
source-underspecified, no source repair accepted. Negative sigma, the complete C1
positive-modulus definition package and source multiplicity observation remain
uncovered. Original98 audits and12 optimisation items and old ledger prefix
are preserved; no wrapper claim closes a complete exercise/chapter.

The optional independent rectangular smoke established derivative/coercivity
subproofs but its full wrapper did not compile (missing import/positivity goal).
It is not a completed test; the committed nonlinear test and generic production
both compiled. No production finding or extra premise resulted.

Aggregate candidate7c9b43d2b9b297cbd7cb8fd8c1dc8f30dd664392:
canonical tools/astis.py check PASS9212 including actual root Tests and fake
closures. Source digest4f7a21c1257ac6f86ee508d18fe17ba1a971f708ddd4c4ab94f7d795b37e453e;
generated2026-09-13T07:28:19.431131+00:00. Exact JSON copied unedited to
runs/semantic-roundtrip/andi-opt-pl-pullback/canonical-gate-evidence.json.
Analysis/Tests first-line imports and Registry423/Tests.Basic integrated.
Use explicit /opt/homebrew/bin/python3 (3.14 here): default shell Python is too
old for the site's f-string syntax. No source/toolchain workaround was added.

Graph delta: production/test modules, public theorem, source chapter02 and
independent audit. One-hop graph has4 direct relations: module declares solid,
parent StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn scanner
reference dashed, source correspondence dashed, semantic audit dashed. Source
scanning is not an exhaustive elaborated dependency export; planned GD consumer
is not shown as a compiled production implication. No family bridge/badge edits.

Root actual visual inspection (not the independent reviewer's own screenshot):
- Reader libraries/optimisation/chapter-02.html#chewi-opt-v1-exercise-2-3-pl-pullback:
  desktop1280x900 and mobile390x844, formula/assumption/boundary/semantic display
  checked. Source-underspecified and separate Definition2.5 TODO visible.
  Both Lean disclosures initially closed; opened both. Statement491 code chars,
  proof1973; actual proof code viewed. KaTeX errors0; document width=scrollWidth
  1265desktop/375mobile. Long mobile formula uses its own horizontal scroller.
- Graph focus lean-foundations.html?view=lean&focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback.exists_minimizer_and_pl&q=AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexPLPullback.exists_minimizer_and_pl:
  15nodes20edges,4highlighted direct relations; exact parent, solid/dashed arrows,
  compiled badge and reader link inspected. Mobile detail wraps full name and
  width=scrollWidth375. Fit restored after viewport testing.
- Temporary tabs17/18 closed, viewport reset, localhost preview server stopped.

Next bounded work: audit a substantive downstream use of this interface or an
uncovered source theorem; do not count a restated PL inequality as new progress.
Do not infer smoothness or a full definition package from this numerical bound.

Merged and pushed directly to `main` at `87fbc6f71a71edb200b2367ca5701ffd7c62202a` under standing
user authorization. SAU `MERGED` releases the single stabilization lane. Remote
post-push CI/deployment is separate from passed local evidence.

## Post-push contract regression repair

Site run34745599714 and formalization run34745599676 exposed the same stale
publication test: it required the live Chapter02 to remain scaffold, although
the reviewed pullback now correctly contributes a partial proof. Earlier local
Lean/site gates and integration review did not exercise this workflow assertion.
The repair scopes the empty-chapter assertion to the historical Chapter01-only
fixture and adds an isolated real pullback regression requiring the exact proof
declaration, partial status and source_complete false. No proof, source binding,
reader content or completion policy changes.

Both workflow unit suites pass locally: website209 and formalization84; six
JavaScript syntax checks and generator compilation also pass.
Full harness discovery also passes256 tests with6 Windows-only skips. Its first
sandboxed run had3 localhost socket permission errors; the permitted rerun
passed without test changes.
Independent supplementary review is recorded in the existing semantic-roundtrip evidence
directory, separately from the historical integration review. The Lean-source
digest remains4f7a21c1257ac6f86ee508d18fe17ba1a971f708ddd4c4ab94f7d795b37e453e,
so the existing canonical PASS9212 remains applicable to the unchanged Lean input.

Release lesson: before pushing a new chapter contribution, run the website and
formalization workflow contract suites as well as the canonical Lean gate and
site build/check. Keep historical migration tests on bounded fixtures; never
freeze a live chapter at scaffold or hide genuine progress to satisfy a test.
