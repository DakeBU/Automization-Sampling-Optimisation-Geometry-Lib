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
