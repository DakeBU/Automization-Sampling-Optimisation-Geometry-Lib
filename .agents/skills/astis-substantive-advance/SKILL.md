---
name: astis-substantive-advance
description: Own one source-backed ASTIS theorem-DAG advance, with independent verification, reader publication and semantic round-trip admission.
---

# ASTIS Substantive Advance Worker Packet

Before new/changed Lean work, read **all three**:

- `docs/contributor-codex-contract.md`;
- `docs/theorem-publication-protocol.md`;
- this packet.

Then run `python3 tools/astis_publication.py packet --cell CELL_ID`. Reuse the bounded source/lesson/audit packet. For any changed production declaration, also run `python3 tools/astis_contributor_contract.py check --base BASE_COMMIT` before asking for stabilization.

New schema-v4 `PROVED_LOCAL` evidence includes `publication_declarations` equal to `lean_declarations`; `VERIFIED` and `STABILIZING` enforce completed independent semantic review. Keep source gaps, proposed repairs and actual Lean assumptions separately visible in the reader. The same protocol covers graph publication: exact declaration/module ids, source and consumer links, generated graph checks, canonical evidence colours/edge types, and one visual inspection of the affected branch. Reuse `integration_notes`; no second graph packet or graph-only agent.

The public reader-quality reference is `textbook/chapter-01/section-1-3.html`. A code dump, theorem inventory, detached proof list, or status table is not a finished textbook contribution.

Use this packet for one Universal Worker and one source-backed theorem-DAG advance. Delete fields that truly do not apply, but never hide a truth boundary, source gap, compiler failure, unchanged route, source-to-Lean semantic delta, or graph/Functor classification.

A Worker is not a narrow proof-script executor. It may cross source reading, mathematical derivation, library retrieval, counterexample search, Lean editing, focused verification, refactoring, and exposition whenever those actions help close the assigned mathematical delta.

For collaborative route work, every substantive advance must also have a persistent Frontier Cell record under `research-wiki/frontier-cells/` and pass `python3 tools/astis_frontier_cells.py check`.

## Input contract

```yaml
advance_id:
task_id:
route: samplewiki-route | riemannian-optimization | optimisation | shared
mode: faithfulPaper | exploratoryProof
frontier_cell:
frontier_cell_record:
goal:
source_anchor:
semantic_roundtrip_required: true | false
active_dag_slice:
  parents: []
  consumers: []
theorem_delta:
target_declarations: []
truth_boundary:
shared_floor_audit:
  searched: []
  classification: reuse | adapt | missing | out_of_scope
  decision: reuse_existing | adapt_existing | new_route_local | new_canonical_shared | out_of_scope
  canonical_declaration:
  canonical_shared_cell:
reuse_plan:
  searched_existing: []
  reused_declarations: []
  new_shared_declarations: []
  known_consumers: []
  planned_consumers: []
  no_duplicate_wrapper: true
  decision_reason:
reader_contract:
  reference_standard: textbook/chapter-01/section-1-3.html
  source_ordered: true
  source_statement_adjacent: true
  natural_language_formula_proof: true
  hidden_assumptions_visible: true
  lean_collapsed: true
  external_dependencies_visible: true
graph_contribution:
  lean_view: new-node | reuse-only | integration-node
  overview_view: updated | no-change-with-reason
  functor_view: none-found | candidate-published | stabilized
  edge_semantics: formal-solid; overlays-dashed
  color_semantics: evidence-status; library-scope
  focus_targets: []
  visual_review:
owned_files: []
forbidden_shared_files:
  - AutoSamplingTheory/TechnicalLemmas/Analysis.lean
  - AutoSamplingTheory/TechnicalLemmas/Measure.lean
  - Tests.lean
  - AutoSamplingTheory/TechnicalLemmas/Registry.lean
relevant_memory_cards: []
validated_cell_syntheses: []
exact_interfaces_or_errors: []
temporary_modes: []
focused_acceptance_checks: []
context_budget:
  maximum_characters:
  omitted_records:
```

## Worker instruction

Own the mathematical advance end to end. Read the exact source, challenge the statement when necessary, and **search ASTIS/Mathlib/shared Frontier Cells before inventing an API**. For Optimisation, search Optlib/CvxLean when relevant; for statistical-learning results, search StatsMLlib when relevant. Implement an isolated theorem module, add a focused test, and run the smallest useful check early. Do not stop at a former Upper/Middle/Lower boundary. Do not edit shared aggregators in the exploration lane.

The objective is not minimum local code. It is the smallest faithful **shared formal substrate**: reuse an existing canonical declaration whenever possible; if the missing lemma has multiple realistic consumers, generalize it once at the shared layer and keep route-specific hypotheses in explicit adapters. Never create wrappers merely to inflate a reuse count. Record exact reused declarations and actual/planned consumers in `reuse_plan`.

If the proposed missing lemma is useful to two or more routes, do not prove a private copy inside the current route. Record `decision: new_canonical_shared`, open/name one `route: shared` Frontier Cell, and make the current cell depend on it. A route-local cell with this decision must not advance beyond `claimed` before the shared cell exists.

For every source-facing statement, author the reader in source order: attributed source statement and formulas → hidden assumptions → readable mathematical proof → source-vs-Lean assumption ledger → folded exact Lean → ASTIS/Mathlib/external reuse → remaining boundary. The source-of-truth is declaration lessons/publication metadata; never hand-edit generated HTML.

Every contribution must classify all three graph views. Formal module/declaration structure stays solid; source, scan, curated, semantic and conceptual overlays stay dashed. Evidence-status colouring and library-scope colouring are separate. A conceptual mirror is never a solid Lean edge or certified functor without an independent formal certificate.

A successful return closes the proposed theorem edge, reusable interface, or integration node. A blocked return must strictly reduce the boundary and include evidence strong enough to change the next scheduling decision. “Lean failed” or “more work remains” is not a result.

Useful cross-boundary ideas belong in the Discovery Ledger even when they do not finish the current edge. When several advances share one connected frontier cell, the Worker may temporarily synthesize that cell and publish a `synthesis` discovery. This temporary mode does not limit the Worker’s mathematical scope and does not create a permanent hierarchy.

## Bounded checkpoint contract

Checkpoints are observability, not progress claims:

```yaml
route_fingerprint:
progress_signature:
mathematical_delta:
exact_residual:
context_characters:
```

After the first occurrence and two unchanged repeats of the same route and progress signature, the route is frozen for diagnosis. The next action must change the route fingerprint, publish a strict blocker/counterexample, or close a theorem delta. Do not spend another context window replaying the same state.

## Output contract

```yaml
advance_id:
route:
frontier_cell:
frontier_cell_record:
state: PROVED_LOCAL | BLOCKED | QUARANTINED
result_kind: theorem-edge | reusable-interface | integration-node | strict-obstruction
mathematical_result:
theorem_delta:
lean_declarations: []
lean_files: []
shared_floor_audit:
  searched: []
  classification:
  decision:
  canonical_declaration:
  canonical_shared_cell:
reuse_plan:
  searched_existing: []
  reused_declarations: []
  new_shared_declarations: []
  known_consumers: []
  planned_consumers: []
  no_duplicate_wrapper: true
  decision_reason:
reader_contract:
  reference_standard: textbook/chapter-01/section-1-3.html
  source_ordered: true
  source_statement_adjacent: true
  natural_language_formula_proof: true
  hidden_assumptions_visible: true
  lean_collapsed: true
  external_dependencies_visible: true
graph_contribution:
  lean_view:
  overview_view:
  functor_view:
  edge_semantics: formal-solid; overlays-dashed
  color_semantics: evidence-status; library-scope
  focus_targets: []
  visual_review:
focused_checks:
  - command:
    result:
source_fidelity:
semantic_roundtrip:
  required:
  audit_id:
  state: not-applicable | draft | blind-reconstructed | semantic-diffed | source-reviewed | accepted | rejected
  verdict:
  remaining_semantic_delta:
truth_boundary:
route_fingerprint:
progress_signature:
exact_blocker:
blocker_class:
strict_reduction:
next_smaller_delta:
retired_route:
minimal_reproducer:
new_discoveries:
  - discovery_id:
    kind: lemma | interface | counterexample | source-gap | refactor | conjecture | process | synthesis | conceptual-mirror
    frontier_cell:
    statement:
    evidence:
    where_it_matters:
    provenance:
integration_notes:
  public_imports_needed: []
  registry_or_site_updates: []
  downstream_consumers: []
context_accounting:
  input_characters:
  output_characters:
  reused_cell_synthesis:
branch:
commit:
```

For `PROVED_LOCAL`, `result_kind` must be `theorem-edge`, `reusable-interface`, or `integration-node`, and declaration/check evidence is mandatory. Update the persistent Frontier Cell to `proved_locally` only after focused checks pass.

For `BLOCKED`, use `result_kind: strict-obstruction` and provide a typed blocker, strict reduction, plus at least one smaller child Frontier Cell, retired route, counterexample, or minimal reproducer. Update the persistent record to `blocked` with the child IDs.

## Source-facing semantic addendum

A source-facing theorem is not assimilated merely because its Lean declaration compiles. When `semantic_roundtrip_required: true`, open or update the canonical semantic audit and follow `.agents/skills/astis-semantic-roundtrip/SKILL.md`.

The formalizer may prepare the draft audit, but cannot serve as the blind decoder or source reviewer. Export the anonymous decoder packet and the later anti-anchored review packet through:

```bash
python3 tools/astis_semantic_roundtrip.py decoder-packet \
  --audit-id ASTIS-RT-... \
  --output runs/semantic-roundtrip/ASTIS-RT-....decoder.json
python3 tools/astis_semantic_roundtrip.py reviewer-packet \
  --audit-id ASTIS-RT-... \
  --output runs/semantic-roundtrip/ASTIS-RT-....review.json
python3 tools/astis_semantic_roundtrip.py check
```

A repair proposal is evidence about a source gap; it is not permission to mutate `faithfulPaper`. Until independent source review accepts it, keep the pinned source theorem, Lean target, semantic delta, and proposed repair separately visible.

## Independent verification addendum

The proving Worker cannot publish `VERIFIED` or update a cell to `independently_verified`. An independent verifier records:

```yaml
verifier_id:
verified_commit:
gate:
source_audit:
semantic_roundtrip_audit:
fake_closure_scan:
```

A green local helper is not enough if it only restates a supplied assumption, does not exercise the named declaration, or proves a Lean proposition whose fidelity to the source remains unaudited.

## Stabilization addendum

Only the designated stabilization lane may:

- clean-port onto current `main`;
- edit shared aggregators and root tests;
- resolve duplicate theorem names/interfaces;
- integrate `route: shared` Frontier Cells into canonical declarations;
- update Registry, graph, source, semantic-roundtrip, and site surfaces;
- record root build and graph regeneration evidence;
- move a cell to `stabilized` and then `merged` after the PR lands.

Before requesting merge, run the publication gate, contributor-contract gate, semantic-roundtrip check, Frontier Cell check, focused/root Lean checks, site build/check, and `graph-check --cell CELL_ID`. Generated `_site` output is never committed.
