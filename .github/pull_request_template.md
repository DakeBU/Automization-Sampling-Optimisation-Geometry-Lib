## Frontier Cell

- Route: `samplewiki-route | riemannian-optimization | optimisation | shared | n/a`
- Frontier Cell ID / record:
- Harness state: `claimed | proved_locally | independently_verified | stabilized | merged | blocked | quarantined | n/a`
- Exact textbook/paper/source anchor:
- Exact theorem-sized target:

## Reuse / shared-floor audit

- Samplinglib searched:
- Mathlib searched:
- Optlib / CvxLean / StatsMLlib searched when relevant:
- Active shared Frontier Cells / `Libraries/shared-foundations.yml` searched:
- Classification: `reuse | adapt | missing | out_of_scope | n/a`
- Decision: `reuse_existing | adapt_existing | new_route_local | new_canonical_shared | out_of_scope | n/a`
- Canonical declaration / shared cell when applicable:
- Exact ASTIS declarations actually reused:
- Existing consumers of the shared leaves:
- Planned consumers of any new shared leaf:
- Why this abstraction boundary maximizes real reuse without wrapper duplication:

If a missing lower-level lemma is useful to two or more routes, do **not** implement parallel route-local copies. Open/use one `route: shared` Frontier Cell and make the route-local theorem depend on it. Do not create wrapper lemmas merely to inflate a reuse count.

## Reader / encoder–denoiser contract

Reference reader: `textbook/chapter-01/section-1-3.html`.

- [ ] Source statements are presented in source order and adjacent to their proof material
- [ ] Exact source edition/anchor and faithful attributed statement are visible
- [ ] Natural-language mathematical proof uses displayed formulas, not a tactic paraphrase
- [ ] Hidden/implicit assumptions and source-vs-Lean deltas are visible
- [ ] Exact Lean statement and proof are folded beside the mathematics
- [ ] ASTIS parents and Mathlib/Optlib/CvxLean/StatsMLlib dependencies are distinguished
- [ ] Fresh source-blind decoder + independent anti-anchored source review are complete
- [ ] Any proposed source repair was reviewed separately and does not silently change `faithfulPaper`

## Graph contribution

- Lean Branches Graph: `new-node | reuse-only | integration-node | n/a`
- Overview Graph: `updated | no-change-with-reason | n/a`
- Functor Hypergraph: `none-found | candidate-published | stabilized | n/a`
- Conceptual-mirror discovery IDs, if any:
- Graph focus target(s):
- Visual review performed:

Truth-preserving rendering contract:

- formal module/declaration structure = **solid** edges;
- source/scan/curated/semantic/conceptual overlays = **dashed** edges;
- evidence-status colour and library-scope colour remain separate;
- conceptual similarity never becomes a formal Lean edge or certified functor without a separate certificate.

## Mathematical change

- Result or correction:
- Owning Lean module:
- Reusable technical leaf, textbook/paper consumer, shared foundation, harness, or website change:
- Known parents and downstream consumers:

## Status boundary

- Local declaration status:
- Mathematical route/paper-reproduction status:
- Remaining obligations or external dependencies:
- If blocked: exact blocker and strictly smaller child Frontier Cell(s):

## Design and provenance

- Important statement, naming, import, or API decisions:
- Adapted code, license, authorship, and changes from the source:
- Source-to-Lean semantic drift risks:

## Verification

- [ ] Read `docs/contributor-codex-contract.md`
- [ ] `python3 tools/astis_publication.py check --base BASE_COMMIT`
- [ ] `python3 tools/astis_contributor_contract.py check --base BASE_COMMIT`
- [ ] Each changed declaration has an authored formula proof and adjacent collapsed Lean
- [ ] Source/actual assumptions and local-vs-Mathlib reuse are explicit
- [ ] Independent encoder–denoiser audit is fresh; source repairs are separately reviewed
- [ ] Chapter progress is generated from proof-obligation mappings, not hand-edited
- [ ] `python3 tools/astis_frontier_cells.py check`
- [ ] Relevant focused Lean tests exercise the named declaration
- [ ] Independent verification performed by someone/agent other than the proving worker before `independently_verified`
- [ ] `lake build`
- [ ] `python3 tools/astis.py check`
- [ ] `python3 tools/astis.py harness-test`
- [ ] `python3 website/scripts/lean_gate.py`
- [ ] Site build and `python3 website/scripts/check_site.py` when site-facing
- [ ] Affected graphs regenerated; `graph-check --cell CELL_ID` and site check pass
- Graph delta (in this PR, not a second report): focus links, changed parents/consumers or topology, remaining red boundary, views actually inspected; `n/a` with reason for unrelated changes
- [ ] No `sorry`, `admit`, hidden axiom/interface closure, or fake completion
- [ ] Generated `_site/` output is not committed

## Reviewer notes

Describe statement drift risks, hidden analytic assumptions, shared-foundation collisions, unresolved source correspondence, reader-layout debt, or follow-up work that must remain visibly open.
