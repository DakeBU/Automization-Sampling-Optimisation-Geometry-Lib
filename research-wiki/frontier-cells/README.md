# ASTIS Frontier Cells

A Frontier Cell is the GitHub-visible unit of mathematical progress for the three public formalization routes and their shared lower-level foundations.

The route dashboard reads these records automatically. Keep one JSON file per cell so different collaborators can advance independent cells without editing one shared status file.

## Status machine

```text
claimed → proved_locally → independently_verified → stabilized → merged
    │
    └→ blocked → smaller child cell → verified → re-entry

quarantined = statement/source/interface conflict that must not enter Samplinglib
```

A status is evidence-backed, not aspirational:

- `claimed`: exact source anchor, target statement, and reuse/shared-floor audit are recorded.
- `proved_locally`: focused Lean checks pass for the target declaration.
- `independently_verified`: a verifier other than the proving worker records verification evidence.
- `stabilized`: root build and graph/index regeneration pass on the integration branch.
- `merged`: the reviewed/stabilized PR is merged.
- `blocked`: the exact obstruction and at least one strictly smaller child cell are recorded.
- `quarantined`: the result is intentionally prevented from entering Samplinglib.

## Cross-route reuse rule

Before creating any declaration, search:

1. Samplinglib declarations and technical lemmas;
2. Mathlib;
3. for Optimisation, Optlib and CvxLean;
4. `Libraries/shared-foundations.yml` and active shared Frontier Cells.

Classify the candidate as `reuse`, `adapt`, `missing`, or `out_of_scope`.

- Exact match: reuse the canonical declaration.
- Near-equivalent statement: use one common mathematical core plus a small explicit route adapter.
- Missing fact needed by two or more routes: create **one** `route: shared` Frontier Cell and make route-local cells depend on it.
- A route-local cell is not allowed to implement a newly discovered shared foundation after the `claimed` stage; it must first depend on the canonical shared cell.
- Different statements remain different declarations. Similar names or similar-looking formulas are not sufficient for deduplication.

## File convention

Use a descriptive file such as:

```text
research-wiki/frontier-cells/riemannian/ASTIS-RIEM-embedded-gradient.json
research-wiki/frontier-cells/optimisation/ASTIS-OPT-proximal-basic.json
research-wiki/frontier-cells/shared/ASTIS-SHARED-relative-convexity.json
```

Copy `_example.json`, change every field, and run:

```bash
python3 tools/astis_frontier_cells.py check
python3 tools/astis_frontier_cells.py summary
```

The site build also runs this validator. Invalid or evidence-free progress states are not publishable.

## Schema 3: evidence-routed learning contract

New source-facing Frontier Cells should use `schema_version: 3`. Schema 3 preserves the existing source-detail/domain contracts and additionally requires `learning_contract`: curated process-memory IDs consulted; typed failure class; salvage audit; serial/parallel admission with distinct direction fingerprints; common-blind-spot review status; and reader-backpressure / Exposition-Seal state. Historical schema-1/2 cells remain valid and are not backfilled with fictional evidence.

The control plane is explicitly non-mathematical. `REFUTED` and independently reviewed `SOURCE_INVALID` records may retire a sealed mathematical route; `API_BLOCKED`, `ENV_BLOCKED`, and `IMPLEMENTATION_FAILED` may only alter process routing. Every non-success schema-3 cell records a salvage audit before branch/dead-code cleanup.
