# Samplinglib contributor and Codex contract

This contract applies to every contributor, including `jicheng9617`, `andyjm3`, `hudsonchen`, and automated coding agents acting for them. It complements `AGENTS.md`, `.agents/skills/astis-substantive-advance/SKILL.md`, and `docs/theorem-publication-protocol.md`.

## 1. Plan for a shared Lean graph before proving locally

Before creating a declaration, search Samplinglib, Mathlib, and the relevant compatible upstreams (for example Optlib, CvxLean, StatsMLlib when applicable). Prefer an existing canonical lemma. If a missing lower-level result has at least two realistic consumers, make it one `route: shared` Frontier Cell instead of copying it into each textbook route.

The objective is not to maximize the raw number of helper declarations. It is to maximize mathematically meaningful reuse: fewer canonical leaves, more genuine consumers, explicit adapters where hypotheses differ, and no wrapper lemmas created only to make a reuse count larger.

Every new or changed production declaration must record a `reuse_plan` in its Frontier Cell with:

- `searched_existing`: exact local/upstream regions or declarations searched;
- `reused_declarations`: exact ASTIS declarations actually called by the authored proof;
- `new_shared_declarations`: new canonical shared declarations introduced by this advance;
- `known_consumers` and `planned_consumers`;
- `no_duplicate_wrapper: true`;
- `decision_reason`: why this abstraction boundary is the most reusable faithful one.

A `new_canonical_shared` declaration must name at least two real consumers.

## 2. Reader standard: Chapter 1.3 is the reference

Use `textbook/chapter-01/section-1-3.html` as the presentation reference. A theorem is not publication-ready when its webpage is only a code listing, theorem inventory, status table, or giant detached proof dump.

For every source statement represented by the contribution, the reader must keep the following adjacent and in source order:

1. the original source statement or attributed faithful restatement, with exact edition/anchor;
2. notation and all explicit/hidden assumptions;
3. a readable natural-language mathematical proof with displayed formulas;
4. source assumptions versus actual Lean assumptions, including API-only assumptions;
5. the exact Lean statement in a closed disclosure;
6. the exact Lean proof in a closed disclosure;
7. ASTIS parents actually reused;
8. Mathlib and compatible external-library facts actually used (Optlib, CvxLean, StatsMLlib, etc. when applicable);
9. the remaining red boundary: what this declaration does *not* prove.

The authored source of truth is `website/content/declaration_lessons/*.json` plus `website/content/publications/*.json`. Do not hand-edit generated `_site` HTML.

Each changed binding's Frontier Cell records a `reader_contract` whose reference is `textbook/chapter-01/section-1-3.html` and explicitly confirms: source order, source-adjacent statement/proof, natural-language formula proof, visible hidden assumptions, folded Lean, and visible external dependencies.

## 3. Encoder–denoiser is mandatory for source-facing claims

Compilation only certifies the Lean proposition. It does not certify that the proposition means the cited theorem.

For a source-facing theorem, use the canonical semantic round trip:

- original theorem / faithful attributed restatement;
- Lean statement;
- source-blind reconstruction from Lean only;
- independent anti-anchored source review;
- separately reviewed theorem repair when a source gap is proposed.

The formalizer, blind decoder, and source reviewer must be distinct actors. Source repairs never silently mutate `faithfulPaper`.

## 4. Every contribution belongs to the three graph views

Every changed production declaration must record `graph_contribution` in its Frontier Cell.

### Lean Branches Graph

This view contains compiler-backed module/declaration structure. Formal structural edges are solid. Source-name scans, curated source correspondences, candidate substrates, and conceptual relations are never promoted to theorem implication.

### Overview Graph

This view records source/library/frontier placement and generated publication progress. A theorem may update the source route without claiming chapter completion.

### Functor Hypergraph

Run the conceptual-mirror audit for every substantive advance. Use `none-found` when there is no new reusable cross-domain mechanism. If there is one, publish a typed conceptual-mirror discovery with stable `family:` / `transport:` / `concept:` ids, hypothesis map, conclusion map, source evidence, and failure boundary. The creator cannot independently validate the mirror.

A conceptual mirror is not a Lean theorem edge or a certified functor unless a separate formal certificate exists.

## 5. Graph colour and edge semantics are part of truth, not decoration

Preserve the canonical graph semantics:

- evidence-status colouring distinguishes compiled / partial / audited / planned / open / proposal states;
- library-scope colouring is a separate view and never upgrades evidence;
- formal module/declaration structure uses solid edges;
- source, curated, scan-derived, semantic, and conceptual overlays use dashed edges.

Do not invent route-specific colours that imply a theorem has stronger evidence than it has. Do not render a conceptual mirror as a solid Lean dependency.

The Frontier Cell records:

- `lean_view`: `new-node`, `reuse-only`, or `integration-node`;
- `overview_view`: `updated` or `no-change-with-reason`;
- `functor_view`: `none-found`, `candidate-published`, or `stabilized`;
- `edge_semantics: "formal-solid; overlays-dashed"`;
- `color_semantics: "evidence-status; library-scope"`;
- graph focus targets and the visual review performed.

## 6. Stabilization and collaboration safety

Exploration workers do not edit shared aggregators, root tests, semantic registries, or global graph truth. The stabilization owner rebases/clean-ports onto current `main`, then updates public imports, root tests, publication/semantic metadata, graph views, and website surfaces.

Never overwrite another contributor's append-only or registry work with an old branch snapshot. When a shared metadata file has moved on `main`, merge semantically or use the repository's fragment/serialized mechanism rather than taking one side wholesale.

Before merge, run at least:

```bash
python3 tools/astis_contributor_contract.py check --base BASE_COMMIT
python3 tools/astis_publication.py check --base BASE_COMMIT
python3 tools/astis_semantic_roundtrip.py check
python3 tools/astis_frontier_cells.py check
python3 website/scripts/build_site.py
python3 tools/astis_publication.py graph-check --cell CELL_ID
python3 website/scripts/check_site.py
lake build Tests
python3 tools/astis.py check
```

The incremental contributor check requires `--base`, or `--ci` with
`PUBLICATION_BASE`. There is no `--strict` flag. It reports the resolved base,
HEAD and affected declarations/cells; it includes untracked production and
publication metadata in local checks. No affected targets is reported as N/A,
not as certification of the whole inventory.

Changed lessons, source items, individual publication bindings and Frontier
Cells are checked even without a Lean edit. Deletions retain their old targets
so removing a binding or lesson cannot hide it from the check. Changed unbound
planned cells must also supply the three cell contracts, without claiming a
compiled theorem. Unchanged metadata outside the comparison scope is not
certified by this incremental command; the publication, semantic, Lean and site
gates remain independently required.

The `Contributor contract` CI workflow runs on pushes, PRs and merge groups.
It uses the PR/merge-group base or previous push tip. For a new topic branch
whose previous tip is zero, it uses the merge base with `origin/main`, not
`HEAD^`. A manual workflow run uses its selected commit as base; this checks
regressions but may have no changed contribution. Missing CI base, unavailable
Git history or initial creation of `main` without an explicit base fails closed.

The PR must state the graph delta, remaining mathematical boundary, reuse decision, and reader/source-fidelity status. Generated `_site/` output is never committed.

## 7. Minimal Codex instruction

A contributor can start Codex with:

> Read `AGENTS.md`, `docs/contributor-codex-contract.md`, `docs/theorem-publication-protocol.md`, and `.agents/skills/astis-substantive-advance/SKILL.md` before planning. Treat Chapter 1.3 as the reader-quality reference. Reuse and generalize canonical shared Lean lemmas before adding route-local copies; record actual and planned consumers. Complete the encoder–denoiser audit. Publish the exact Lean/Overview/Functor graph delta using canonical colour and solid/dashed edge semantics. Do not merge or claim completion until the current-main publication, semantic, graph, site, root Tests, and ASTIS gates pass.
