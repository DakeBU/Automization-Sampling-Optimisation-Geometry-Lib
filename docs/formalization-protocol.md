# ASTIS Collaborative Formalization Protocol

This protocol governs collaborative formalization across the public **SampleWiki Route**, **Riemannian Optimization**, **Optimisation**, **Statistical Optimal Transport**, and **Higher-Order Smoothness × Sampling** routes. It converts the ASTIS Harness into a GitHub-visible workflow and prevents independent collaborators from rebuilding the same lower-level mathematics in parallel.

## 1. Unit of work: one Frontier Cell

All routes, including shared, Discrete Sampling and MCMC, additionally follow
[the theorem publication contract](theorem-publication-protocol.md) and the
[proof-digestion protocol](proof-digestion-protocol.md): source-facing statements
are sealed before proof search; source proof topology is reconstructed separately
from Lean implementation topology; source coverage is exhaustive; and merged
proofs are not human-facing complete until purified. The publication contract keeps one authored
formula proof with adjacent folded Lean, explicit source/assumption mapping,
mandatory encoder–denoiser evidence, and generated chapter/graph status.

Every substantive formalization advance is one theorem-sized **Frontier Cell** with:

New source-facing cells should use schema 3 and follow `docs/evidence-routed-memory-protocol.md`; historical schema-1/2 cells remain valid. Schema 3 makes failure typing, salvage, process-memory consultation, parallel-direction admission, common-blind-spot review, and reader-backpressure state machine-checkable.

- one exact source anchor;
- one exact mathematical target;
- known parents and intended consumers;
- an explicit truth boundary;
- a reuse/shared-floor audit;
- focused Lean checks;
- evidence-backed status.

Persistent records live under `research-wiki/frontier-cells/`. One JSON file is used per cell so parallel collaborators do not contend on one central task file.

## 2. State machine

```text
claimed → proved locally → independently verified → stabilized → merged
    │
    └→ blocked → smaller child theorem → verified → re-entry
```

Repository spellings are:

```text
claimed
proved_locally
independently_verified
stabilized
merged
blocked
quarantined
```

A worker may not skip evidence by changing a label. `tools/astis_frontier_cells.py check` rejects unsupported states.

### claimed

The exact source and target are pinned. The worker has searched existing shared mathematics and recorded a `reuse | adapt | missing | out_of_scope` classification.

### proved_locally

The target declaration compiles and focused checks exercise the actual theorem. This is not yet published truth.

### independently_verified

A verifier other than the proving worker checks the exact commit, theorem statement, source fidelity where applicable, and fake-closure risks.

### stabilized

The verified change has been clean-ported onto current integration state; root build, shared registry/graph regeneration, and site/index checks pass.

### merged

The stabilized PR is merged. Only this state is treated as repository truth on the public dashboard. **Merged is an integration state, not the final reader-facing state.** A merged source route may still carry `purification: pending` under `docs/proof-digestion-protocol.md`; it must not be advertised as fully digested until the dead/duplicate/wrapper audit, canonical shared-spine extraction, route compression, and reader compression have completed.

### blocked

A blocked cell must record the exact obstruction and create or name at least one **strictly smaller** child cell. Repeating the same failed route without reducing the mathematical boundary is not progress.

### quarantined

Use when the proposed theorem, source mapping, interface, or proof route is not safe to merge. Quarantine remains visible evidence and is not silently repaired into a different source theorem.

## 3. Mandatory cross-route reuse audit

Before creating a new Lean declaration, search in this order:

1. Samplinglib / existing ASTIS declarations and technical lemmas;
2. Mathlib;
3. active `route: shared` Frontier Cells and `Libraries/shared-foundations.yml`;
4. for Optimisation-related work, Optlib and CvxLean;
5. source-specific route code for near-equivalent interfaces.

Compare **semantic theorem fingerprints**, not names: objects, domains, quantifiers, assumptions, normalization, conclusion, and intended consumers.

Then choose exactly one decision:

- `reuse_existing` — exact theorem already exists;
- `adapt_existing` — common core exists but route conventions require a small adapter;
- `new_route_local` — genuinely route-specific theorem;
- `new_canonical_shared` — missing foundation needed by two or more routes;
- `out_of_scope` — not part of the current formalization boundary.

## 4. Shared-foundation collision rule

When two routes need the same lower-level theorem:

- do **not** create two route-local versions;
- open one `route: shared` Frontier Cell;
- list all consuming routes;
- stabilize one canonical declaration;
- make route-local theorems depend on that declaration;
- use explicit adapters if conventions differ.

If a route-local worker discovers that its proposed declaration should be shared, it may remain `claimed`, `blocked`, or `quarantined`, but it may not advance to `proved_locally` as a duplicated route-local implementation. The shared cell must be opened first. This rule is enforced by `tools/astis_frontier_cells.py`.

`Libraries/shared-foundations.yml` records known cross-route checkpoints and canonical shared declarations as they become stable.

## 5. Exploration lane vs stabilization lane

Parallel workers may freely work on isolated theorem modules and focused tests. They should not independently edit shared aggregators, root registries, or another route's stable interface merely to make their branch compile.

Shared-file changes are serialized during stabilization. The stabilization lane is responsible for:

- resolving duplicate theorem names and APIs;
- clean-porting onto current `main`;
- updating public imports and registries;
- root build and site validation;
- graph/index regeneration;
- merging the reviewed result.

This keeps parallel mathematical exploration cheap while making shared library truth single-valued.

## 6. Source fidelity remains independent of Lean success

A source-facing theorem must keep its source statement, assumptions, constants, and conventions visible. Lean compilation proves the Lean proposition; it does not by itself prove that the Lean proposition faithfully represents the source.

Use the semantic-roundtrip workflow when required. The proving worker may prepare the audit but may not serve as the independent verifier/source reviewer.

## 7. GitHub collaboration contract

For a new theorem-sized task:

1. create or update one Frontier Cell JSON record;
2. work on a dedicated branch/PR;
3. fill the formalization section of `.github/pull_request_template.md`;
4. keep the cell status synchronized with actual evidence;
5. record shared-floor search results before adding new declarations;
6. when blocked, split into smaller child cells rather than expanding the task indefinitely;
7. request independent verification before stabilization;
8. merge only after shared/root/site gates pass.

The public `/progress/` dashboard reads the cell records and displays all three routes together. No collaborator names or internal staffing assignments are required on the public site; the unit of coordination is the route and Frontier Cell.

## 8. Required local checks

At minimum:

```bash
python3 tools/astis_frontier_cells.py check
python3 tools/astis.py check
python3 tools/astis.py harness-test
```

For source-facing or site-facing changes, also run the relevant semantic/source checks and:

```bash
python3 website/scripts/build_site.py
python3 website/scripts/check_site.py
```

The exact focused Lean command for the cell must also be recorded in its `evidence.focused_checks` field before `proved_locally`.


## 8. Cross-domain sources, omitted details and conceptual transports

This protocol also governs **Statistical Optimal Transport Route** and **Higher-Order Smoothness × Sampling**. All five routes share the [dependency partial order](../Libraries/cross-domain-program.json); a research route uses `exploratoryProof` without changing any `faithfulPaper` target.

New Frontier Cells use schema version 2 and record `source_detail_audit`: primary edition/anchor, whether detail is sufficient/omitted/cites_external, the exact gap, consulted background theorem/page and convention/assumption adapter. Omitted or externally delegated proofs require an actual consulted source, not a generic bibliography. Every new cell records Samplinglib and Mathlib searches. The higher-order route also records its comparison contract (potential class, p/q/k/r, metric, start and cost model).

When formal reuse fails, consult targeted authoritative background texts as described in [the source hierarchy](cross-domain-program.md). Keep the primary theorem fixed; missing assumptions become explicit semantic-repair proposals. A text-to-text correspondence is not a formal dependency edge. Functor candidates additionally require object/morphism maps and identity/composition proofs before any certification. No automatic compression may erase assumptions or primitive proof support.
