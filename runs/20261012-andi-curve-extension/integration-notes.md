Current closeout: PR319 actually merged at a47d39a. Independent post-merge review accepts scoped curve PURIFIED; full-source propositions and affine import cleanup remain open. Earlier pending sections below are historical checkpoints.

# Curve extension independence — contribution checkpoint

Owner: `andi-curve-root`; branch: `codex/andi-curve-extension`.
Base main: `f4f8d3a8ef0d4918cb30c333540a303b501ffc63`.
Issue: https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/issues/318
Proof/test checkpoint: `30b1a05da320dbd6770cae1acbaa3c3fb2a6345a`, pushed.

## Mathematical delta and source boundary

One canonical shared declaration derives equality of two actual ambient
derivatives on the true velocity of a nonlinear feasible curve from relative
local equality of the maps. It does not assume the desired derivative equality
or a derivative certificate for either image curve. The local normed-space
generalization is explicit: pointwise genuine derivatives, local feasibility,
relative germs, any real parameter, and no finite-dimensional/completeness or
inner-product assumptions.

The source is Boumal's 2023 pre-publication edition, annotations through
2026-10-08, §3.4, printed35–36/PDF51–52. The source checksum was rechecked before
proof search; the personal-use PDF is not committed or redistributed. The
Statement Seal and independently reviewed Source Proof Graph predate
implementation. The reviewed graph retains the definition-based and explicit
chain-rule arguments as alternative sufficient routes. The missing project
tangent adapter is a formalization boundary, not a claimed source gap.

Publication supports only `extension-independence` as a genuine source proof
edge. Full Proposition3.35 needs the intrinsic differential restriction,
source/target tangent adapters, linearity and independence from the representing
curve. Full Proposition3.61 additionally needs the nonlinear gradient/metric
identification. Neither proposition nor Chapter3 is declared complete.

## Reuse and focused evidence

Samplinglib/shared cells, fixed Mathlib, fixed Optlib's gradient module and
CvxLean's relevant module inventory were checked. The tangent-cone uniqueness
API is neighboring mathematics, not the selected relative-germ curve adapter.
The single shared node composes existing continuity, filter pullback, genuine
chain rule, locality and derivative uniqueness; no route-local wrapper is added.
Vector-valued Boumal §3.4 and scalar extension choice in §3.8 are real planned
consumers. No implemented downstream manifold consumer is claimed yet.

Lean4.33.0 / Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`:

- Production build passed (1880 jobs).
- `Tests.Shared.CurveExtension` passed (1989 jobs).
- The test uses the parabola `(t,t²)` and extensions `p↦p.2`, `p↦p.1²`:
  unequal ambient derivative maps agree on actual velocities `(1,2t)`.
- Axiom report contains only `propext`, `Classical.choice`, `Quot.sound`.

The independent decoder received only the anonymous theorem and approved
definition context. Its actual hashed result is retained. Independent source,
proof and exposition review is in progress. The review identified an exposition
wording error: normed spaces do carry a metric. The corrected lesson says no
*chosen Riemannian* metric or inner product is needed; the updated reviewer
packet is distinct from the archived first input. No Lean/source theorem repair
was required.

## Integration obligations

This is a compiled WIP checkpoint, not an admitted integrated result. Once
independent publication/semantic admission finishes and the single lane is
available, the sole stabilization owner must import the focused test in root
`Tests.lean`, import the shared module through Geometry and Registry, add the
bounded Registry entry, and synchronize its existing count test. Then run the
full Lean/ASTIS, contributor, publication, semantic, Frontier, process-memory,
Harness and generated site/affected-graph gates. Inspect the actual chapter and
graph. Never infer root CI coverage from the standalone test build.

The Chapter3 knowledge map must acknowledge the new curve extension edge while
keeping full nonlinear differential/gradient identification and smooth-field
work open. Exact folded Lean statement/proof and step correspondence are authored
beside the natural proof through the shared renderer. Source correspondence is
an overlay, not a formal Lean dependency. No new Functor bridge was found.

Candidate compressed spine: feasible relative germ → equal image curves →
actual chain rule and locality → unique velocity. Source/Lean drill-down retains
all hypotheses and both source proof alternatives. Independent purification,
Exposition Seal and actual merge remain pending. `MERGED` will not be treated as
`PURIFIED`.

Pre-existing untracked `.DS_Store` files and the optimisation reuse-audit note
are preserved and excluded. The overall Chewi/Boumal Goal remains active.

## Actual reviewed stabilization (2026-10-12)

The checkpoint wording above records historical WIP, not the current state.
The actual source-blind decoder and anti-anchored source/proof reviewer accepted
the selected proof edge on checked commit30b1a05. The overall source comparison
remains `lean-weakened-conclusion`; full-source-equivalence-only is a retained
blocker. No historical audit is backfilled.

The sole owner integrated root Tests, Geometry, Registry and its count test488.
Chapter3 keeps the existing shared knowledge map and explicit nonlinear/open
boundaries. Explicit source_order335/361 restores numbered book order; legacy
unordered items retain their relative order. Only presentation sorting changes
in the generator; no theorem status is inferred. The old map assertion failed
because it required only affine progress. It was updated to test both actual
proof edges and continued noncompletion; targeted and final Harness checks pass.

Actual checks on final integration tree:

- Canonical Lean/ASTIS gate PASS, root Tests9429jobs, pinned toolchain/Mathlib.
- Final Harness297tests PASS (six Windows-only skips).
- Semantic273audits/8repairs, publication207items, contributor diff-aware,
  Frontier270cells and process-memory checks PASS before final metadata update.
- Site build/check PASS:12chapters,488local leaves,897modules,4738declarations.
- Affected graph-check PASS; reference scans remain incomplete.
- Actual browser QA recorded in integration-visual-inspection.json.

Small graph delta: one canonical compiled declaration and module ownership;
Chapter3 source correspondence and independent semantic audit overlays. Overview
source topology reuses the existing Chapter3 route. No new Functor edge.
No full intrinsic manifold consumer or full proposition badge is claimed.

Remote exact-head CI and actual merge remain pending. Purification stays pending
until a scoped post-integration review. Source/Lean expansion nodes and all
lossless historical evidence remain preserved.

The reviewed integration was committed as6c72df775 and pushed in PR319.
Its actual-HEAD canonical Lean/ASTIS gate passed again and site/affected graph
was regenerated; site check passed. The new cell now carries the explicit
§13 proof_digestion and pending purification summaries as well as the existing
reader-backpressure fields. This is a metadata completion, not another math
advance or a PURIFIED certificate.

## Actual merge closeout

PR319 merged after all exact-head checks passed. Head:453ba678ef21b4d2dded384c33e3c03934982395;
merge:a47d39a5292b6441ef6c84b81829044fa4fca712; mergedAt:2026-10-11T22:27:20Z. Real responses and gate
identity are in integration-closeout.json. MERGED transition is actual, not inferred.

Contribution report (scoped to this package):

1. Source: explicit extension-choice verification following BoumalProp3.35,
   §3.4 printed35–36/PDF51–52, pinned2026-10-08 annotations; genuine proof edge,
   not full Prop3.35/3.61.
2. Lean: one canonical CurveExtension.fderiv_eq_on_curve_velocity; existing
   Mathlib facts reused. Root Tests imports the nonlinear test, Registry488.
3. Assumptions: genuine ambient pointwise differentiability, actual curve
   derivative, eventual feasibility and relative germ agreement; normed/local
   generalization explicit versus finite-dimensional smooth manifold source.
4. External dependencies: pinned Mathlib only; bounded Optlib/CvxLean retrieval,
   no external port or ATLAS proof certificate.
5. Round trip: actual blind decoder and independent anti-anchored source review;
   scoped edge accepted, overall lean-weakened-conclusion/full-source blocker kept.
6. Reuse: single shared interface, no duplicate alias/wrapper; real planned
   vector differential and scalar objective extension-choice consumers.
7. Graph: actual Lean ownership plus source/audit overlays, existing Chapter3
   Overview route/map; no Functor edge; generated branch visually inspected.
8. Remaining: current audits are real, historical evidence never fabricated;
   unrelated legacy debt not certified away. Full intrinsic tangent/differential,
   nonlinear gradient and smooth-field obligations remain open. Affine import
   cleanup pending; curve purification requires actual post-merge review.

Curve post-merge purification pending its actual independent review. Already
merged affine prerequisite remains pending only demonstrated import cleanup,
recorded in affine-post-merge-purification-review.json and its original cell.
Full sourceProp3.35/3.61 and entire Chewi/Boumal Goal remain open.

Next bounded mathematical edge should inspect sphere's intrinsic-to-ambient
inclusion differential: pinned Mathlib already supplies
range_mvfderiv_subtypeVal / injective_mvfderiv_subtypeVal_sphere
(global declarations in Manifold/Instances/Sphere.lean), and Samplinglib UnitSphere
already supplies genuine signed-geodesic derivatives. Preserve tangent and
induced-metric adapters; do not duplicate these existing results or infer
nonlinear gradient identification from an affine or curve-only theorem.

## Independent post-merge purification closeout

Actual curve-post-merge-purification-review.json accepts scoped PURIFIED (review SHA 8353ac7d72ca54a64101c5318ba3edc13b082340e68707054f2f0cfa1a80661e). Current cell projects this independent result after actual merge; frozen preflight and append-only MERGED history remain unchanged. Canonical merge-head Lean/ASTIS gate passed, including root Tests9429jobs. Proof/source/lesson bytes are unchanged; full-source lean-weakened-conclusion and intrinsic tangent/differential boundaries remain explicit. Affine import minimization is separate pending work.
