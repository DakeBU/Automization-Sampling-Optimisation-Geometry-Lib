# Agent Guide for Auto-Sampling-Theory-In-Sleep

ASTIS is a Lean-first SDE/Sampling proof project. The repository may contain
source contracts and explicit proof obligations, but completed mathematical
claims must compile in Lean and match their cited source boundary.

## Current user-directed priority

Read `website/content/samplewiki_companion_frontiers.json` → `execution` before
scheduling. The two September 2026 companion papers are the first mathematical
priority. Preserve older frontiers; work on them only when they supply a needed
paper dependency. Correct Lean/source results come before new graph, citation or
download features. This is scheduling, never a theorem-completion badge.

Current collaborator checkpoint: read `docs/companion-papers-handoff.md` before
resuming these papers. It records the owner's pause, reviewed local results,
pending aggregate/publication checks and the next bounded mathematical edge.

## Non-Negotiable Gate

```bash
python3 tools/astis.py check
```

The gate runs the Lake build and scans for fake proof closures.

## Canonical Operating Model: ASTIS Harness

The active unit of work is a **Substantive Advance Unit (SAU)**: one bounded,
source-backed mathematical delta in the live theorem/Lean DAG. One generalist
Worker owns an SAU end to end. Source reading, proof design, Samplinglib/Mathlib
retrieval, counterexample search, Lean implementation, compiler diagnosis, and
local exposition are temporary modes, not permanent role boundaries.

The coordinator is a thin global arbiter. It must not replay full Worker
transcripts or reproduce proofs. It reads a bounded synthesis-first capsule,
assigns ownership, suppresses duplicate theorem targets, resolves cross-cell
conflicts, and admits verified work to the single stabilization queue.

The current state is inspected with:

```bash
python3 tools/astis_advance.py capsule
```

`tools/astis_advance.py` is the active Harness control plane.
`tools/astis_harness.py` remains the durable compatibility substrate for old
Upper/Middle/Lower/Reviewer artifacts, locks, append-only JSONL, interrupted-tail
recovery, exact-field memory, and old run replay. Legacy role names are execution
slot labels only. They do not restrict what an agent may notice, prove, refactor,
test, or explain, and a new theorem must not be routed through the old ladder
merely to manufacture handoff artifacts.

## Operating Loop

Every new/changed Lean declaration also follows
`docs/theorem-publication-protocol.md`. Every new or materially changed
**source-facing** theorem/definition additionally follows
`docs/proof-digestion-protocol.md`: seal the exact statement before proof search,
classify/expand binders, audit definition semantics, reconstruct the Source Proof
Graph independently of implementation Lean, require exhaustive source coverage,
and run post-merge purification before calling the result human-facing complete.
The central invariant is `proof ingredient = dependency edge` and
`source hypothesis = theorem binder`; a producer theorem never legalizes an
extra public premise. Start with the bounded
`python3 tools/astis_publication.py packet --cell CELL_ID`, not a whole-site scan.
Author mathematical statement/formula proof once in declaration lessons; bind
source obligations and explicit assumption differences in publication metadata.
The existing encoder–denoiser skill is mandatory: independent source-blind
decoder, anti-anchored source reviewer, separately reviewed repair overlays.
New schema-v4 SAUs require real publication validation at `PROVED_LOCAL` and
completed independent source review at `VERIFIED` / `STABILIZING`. The diff-aware
CI gate covers older lanes too. Never hand-edit a chapter's completion badge.
Graph contribution is part of that same publication contract, not another
workflow: regenerate the affected graph views, run `graph-check --cell CELL_ID`,
and inspect the changed branch. Record the small graph delta in the existing
PR/integration notes; do not create another status ledger or graph-only agent.

1. Reconcile source and theorem state. For the main textbook program, select a
   dependency-ready DAG delta rather than recovering a frontier from old prose:

   ```bash
   python3 tools/astis.py harness-reconcile
   python3 tools/astis_advance.py capsule
   ```

2. Propose or claim one SAU with an exact source anchor, theorem delta, truth
   boundary, DAG parents, frontier cell, owned files, target declarations, and
   focused checks. Semantic duplicates must share one owner rather than become
   parallel branches.
3. Let the owning Universal Worker cross all temporary modes needed to finish
   the mathematics. Run the smallest useful Lean check early.
4. Record bounded checkpoints. After the first occurrence and two unchanged
   repeats of the same route fingerprint and progress signature, the route is
   frozen for diagnosis. A fourth identical attempt is rejected; change the
   mathematical route or publish a strict blocker.
5. Return exactly one substantive outcome:
   - a compiled theorem edge;
   - a reusable compiled interface;
   - a compiled integration node joining existing parents; or
   - a typed obstruction that retires a route or strictly shrinks the remaining
     theorem boundary.
6. Publish cross-boundary ideas to the Discovery Ledger. Lemmas, interfaces,
   counterexamples, source gaps, refactors, conjectures, process insights, and
   conceptual mirrors must survive Worker termination without silently becoming
   formal truth.
7. **Run the conceptual-mirror audit before `PROVED_LOCAL`.** For every new
   schema-v3 SAU, explicitly return `conceptual_mirror_audit.status = none-found`
   or publish one or more typed `conceptual-mirror` discoveries and list their
   ids. A discovered recurring mechanism is not allowed to disappear in a local
   transcript merely because it is not needed to close the current theorem.
8. When several advances occupy the same connected frontier cell, any
   generalist Worker may temporarily perform **local frontier synthesis** and
   publish a `synthesis` discovery. This is an ephemeral mode, not a new fixed
   role. The global arbiter consumes validated cell syntheses and conceptual
   mirrors before raw advance records.
9. Verify independently. The verifier must name the checked commit, Lean/source
   gate, source audit, and fake-closure scan. The proving Worker cannot publish
   its own `VERIFIED` transition. A conceptual mirror likewise cannot be
   validated by its creator.
10. Serialize repository integration. Exactly one stabilization owner may
   clean-port onto current `main`, modify shared imports/root tests, update the
   Registry/source correspondence/Underlying Lean Graph/site, and publish the
   canonical PR or merge commit. Validated conceptual mirrors are stabilized in
   Graph Memory + Functor Hypergraph, not promoted into Lean dependencies.
11. Run the gate and refresh compact memory/TODO state.

Branches, commits, files, prompt count, longer logs, isolated smoke tests,
wrapper lemmas that restate assumptions, and repeated unchanged attempts are
observability data. They are not mathematical progress.

## Conceptual Mirror / Functor Hypergraph Protocol

ASTIS intentionally preserves mathematical correspondences that are weaker than
Lean theorem implication. Read these files before reconstructing such structure
from scratch:

```text
Libraries/conceptual-mirror-protocol.json
website/content/graph_memory_index.json
website/content/functor_hypergraph.json
Libraries/frontloaded-shared-spine.json
```

The three principal graph views have different truth contracts:

- **Overview Graph** answers where source libraries, shared stages, and frontier
  families live. It is project/source topology, not proof implication.
- **Lean Branches Graph** answers what compiled modules/declarations actually
  depend on. Conceptual mirrors may never be rendered as solid formal edges.
- **Functor Hypergraph** answers what mathematical mechanism recurs after
  changing the space, metric, energy, oracle, or discrepancy. Every bridge must
  keep source ids, a formula, mechanism, hypothesis map, conclusion map, and a
  failure boundary.

Use stable identities across agent memory and the reader:
`concept:<slug>` for domains, `family:<slug>` for compressed mathematical
families, `transport:<slug>` for typed conceptual bridges, and exact emitted
module/declaration ids for Lean nodes.

A `Discovery(kind="conceptual-mirror")` must carry metadata:

```text
bridge_id, family_id, domains, formula, mechanism,
hypothesis_map, conclusion_map, failure_boundary, source_ids, graph_views
```

Its validation is source/mathematical review only. It does not make a Lean edge,
a theorem equivalence, or a certified functor. The creator cannot validate it.
During stabilization, retain a validated mirror in
`website/content/graph_memory_index.json` and
`website/content/functor_hypergraph.json`; connect only source-present Lean
**candidate substrates** unless exact compiled dependencies or transport
certificates exist.

Seed families currently include:

- `family:metric-gradient-flow`: metric gradient → energy dissipation → a
  PL-shaped coercivity bound → scalar Grönwall/exponential decay;
- `family:curvature-growth`: strong/geodesic/other source-specific curvature
  controls → quadratic growth or PL/functional-inequality controls;
- `family:gap-gradient`: Euclidean/Riemannian/Wasserstein PL and the LSI/KL
  dissipation mirror, with exact metrics and normalizations kept distinct;
- `family:l2-coercivity`: Poincaré/Dirichlet coercivity → chi-square exponential
  decay for the reversible semigroup;
- `family:proximal-energy`: one quadratic-regularized energy, consumed as a
  proximal minimizer or a Gibbs/RGO draw.

Do not conflate Euclidean strong convexity, geodesic strong convexity,
displacement convexity, Bakry–Émery curvature, PL, Poincaré, and LSI merely
because some of them imply exponential convergence. The purpose of the family
layer is to show the reusable proof skeleton **and** exactly where its adapters
and hypotheses differ.

## Frontier Cells and the Master Bottleneck

Parallel exploration is organized by connected **frontier cells**: nearby SAUs
that share DAG parents, source anchors, theorem declarations, or integration
surfaces. This is a context-compression device, not a hierarchy of mathematical
ability.

- A Worker reads the local DAG slice, exact interfaces/errors, and validated
  discoveries for its cell, not the whole project transcript.
- A local synthesis records the cell graph delta, conflicts, retired routes,
  reusable discoveries, and next independent candidates.
- The global arbiter sees one bounded summary per cell and only opens raw
  evidence for unresolved cross-cell conflicts or stabilization decisions.
- Fanout, repeated spawning, and unchanged global decisions are bounded. When a
  cell has multiple active advances but no validated synthesis, or a Worker hits
  the no-progress threshold, the cell enters the arbiter queue instead of
  causing another blind spawn.
- Shared repository truth remains serialized even though mathematical
  exploration is parallel.

This keeps the useful FrontierAgent ideas—bounded parallelism, a task board,
structured reports, checkpoint/resume, and coordinator no-progress guards—while
retaining ASTIS-specific theorem-DAG truth, exact source contracts, Lean gates,
and graph provenance.

## Substantive Evidence Contracts

A `PROVED_LOCAL` packet must contain:

- `result_kind`: `theorem-edge`, `reusable-interface`, or `integration-node`;
- the exact theorem delta and Lean declaration names;
- the Lean files and focused checks that exercise those declarations;
- the remaining truth boundary;
- `conceptual_mirror_audit` for schema-v3 advances: either an explicit
  `none-found`, or `candidates-published` with Discovery Ledger ids;
- useful discoveries and downstream integration notes.

A `BLOCKED` packet must contain:

- a typed blocker class and exact residual problem;
- the strict reduction achieved relative to the assigned SAU;
- at least one of a smaller next delta, a retired route, a counterexample, or a
  minimal reproducer.

“Lean failed”, “more work is needed”, a broad literature note, or a handoff that
merely restates the original target is not an admissible blocker.

The canonical Worker packet is:

```text
.agents/skills/astis-substantive-advance/SKILL.md
```

## Conversion and Source Discipline

Maintain a conversion window when translating between LaTeX, Markdown, and
Lean. Keep source labels indexed under `research-wiki/source-index/`. Exact
assumptions, measures, spaces, domains, representatives, and source anchors may
not be paraphrased away by capsule compaction.

Keep unproved analysis in `proof-obligations/` or
`research-wiki/cited-results/`. Keep task-local paper contribution memory
separate from reusable technical-lemma memory. For SALD, unfinished source lines
live in the canonical
`research-wiki/paper-contributions/SALD/unfinished_source_map.md`; the old
`research-wiki/paper-memory/ASTIS-SALD-001/` path is a compatibility mirror.

When using SLT-inspired results, first read
`research-wiki/technical-lemmas/README.md`, search
`AutoSamplingTheory/TechnicalLemmas`, and update
`research-wiki/cited-results/SLT_reuse_audit.md` with the exact local port status
and ASTIS declarations.

## Mathlib-Ready Leaf Lemma Protocol

Reusable SDE/Sampling facts should be written as future Mathlib-ready leaf
lemmas. The immediate acceptance condition is still local: an ASTIS-owned
Lean declaration builds, or the result remains a named proof obligation. The
target shape should be general enough to survive outside one paper theorem
whenever possible.

A reusable technical-lemma packet records:

- one theorem or one strictly smaller source-cited boundary;
- proposed Lean name, namespace, file, and minimal imports;
- exact local ASTIS APIs and Mathlib declarations searched first;
- hidden regularity contracts: measurability, integrability, domination,
  smoothness, boundedness, positivity, conditional representative, and
  boundary/decay assumptions as needed;
- an intended proof route in at most seven steps;
- a failure policy.

Persistent failure is mathematical evidence. After two or three same-shape
failures, stop editing the script and diagnose the statement: missing
assumption, false theorem/counterexample risk, wrong representative, Mathlib API
mismatch, or target too large. A statement changes only when the diagnosis
identifies a real mathematical/source/API issue.

Entry points:

```bash
python3 tools/astis.py lemma-dag-refresh
python3 tools/astis.py module-graph-refresh
```

```text
docs/module-graph.svg
docs/mathlib_ready_leaf_protocol.md
research-wiki/sampling-sde-library/lean-leaf-module-graph.md
research-wiki/sampling-sde-library/cards/
research-wiki/external-lean-libraries/
research-wiki/lemma-dags/SDE_Sampling_skill_tree.md
research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md
research-wiki/lemma-dags/Pro_assimilated_leaf_targets.md
research-wiki/technical-lemmas/mathlib_ready_leaf_template.md
research-wiki/technical-lemmas/hidden_regularities.md
agent-briefs/mathlib_ready_leaf_packet.md
```

Before claiming a generic Sampling/SDE delta, read the corresponding module
card and reuse `Probability.lean`, `SDE.lean`, and
`AutoSamplingTheory/TechnicalLemmas/`. SALD/RMFLD files are consumers, not the
home of reusable background mathematics.

ATLAS v1 is searchable external memory, not a local proof certificate. Search
its pinned 26-book declaration inventory with:

```bash
python3 tools/atlas_memory.py search markov kernel --route samplewiki-route
python3 tools/atlas_memory.py search riemannian --route riemannian-optimization
python3 tools/atlas_memory.py search convex --route optimisation
```

Every returned item remains `external-reference`. Inspect its pinned source,
license, hypotheses, direct placeholders, and upstream evaluation before
porting. Do not use the source or index for commercial activity or to train,
fine-tune, distill, evaluate, or otherwise develop ML models.
Before using a candidate, port only the minimal needed statement. It becomes
callable Lean truth only after an ASTIS-owned declaration compiles, is tested,
and enters the Registry.

## Canonical Memory Protocol

| Function | Canonical path | Legacy mirror |
|---|---|---|
| Proof blueprint | `proof-blueprints/` | `research-wiki/blueprints/` |
| Paper contribution memory | `research-wiki/paper-contributions/SALD/` | `research-wiki/paper-memory/ASTIS-SALD-001/` |
| Technical lemma memory | `research-wiki/technical-lemmas/` | `research-wiki/technical-lemma-memory/` |
| Compact retrieval index | `research-wiki/retrieval-index/` | none |
| Typed verifier feedback | `verifier-feedback/` and trial-log feedback JSON | none |
| Agent briefs | `agent-briefs/` | none |
| Substantive-advance ledger | `runs/substantive_advances.jsonl` | old role artifacts remain readable |
| Discovery/synthesis/mirror ledger | `runs/substantive_discoveries.jsonl` | none |
| Conceptual mirror policy | `Libraries/conceptual-mirror-protocol.json` | none |
| Compact graph-family memory | `website/content/graph_memory_index.json` | none |

At the end of a completed proof cycle, refresh compact memory and TODO state.
Human-facing Chinese summaries are written once at the final long-run closeout,
not after every inner action.

```bash
python3 tools/astis.py memory-refresh ASTIS-SALD-001 --run-id latest
python3 tools/astis.py project-article-update ASTIS-SALD-001 --run-id latest
```

Old `launch-sald-6h` profiles may still expose `upper`, `middle`, `lower_*`, and
`reviewer` keys for replay compatibility. Treat those keys as parallel
execution slots hosting Universal Workers and independent verification—not as a
permission system. New orchestration should write SAU/discovery state first and
should not require every slot to run on every theorem.

## Mode Discipline

`faithfulPaper` reproduces a cited source. Do not add assumptions, weaken the
statement, or replace the route without recording the exact source gap.

`exploratoryProof` validates active research. Candidate routes may compete, but
success still requires a Lean-checkable target, explicit truth boundary, and
independent review. EoH-style populations are allowed only for fixed targets in
this mode; they may not mutate a faithful theorem until it becomes provable.

## Review Discipline

Reject:

- `axiom`, `sorry`, `admit`, `Prop := True`, or `:= trivial` used to close
  mathematics;
- hidden assumptions not present in the source proof;
- SLT/Mathlib dependencies marked formalized before an ASTIS-owned local
  declaration builds;
- faithful tasks that do not update source-to-Lean correspondence;
- completion claims whose unfinished paper leaves lack concrete LaTeX line
  ranges;
- packets that cite a technical lemma before it exists as a compiled local
  declaration;
- schema-v3 `PROVED_LOCAL` packets that omit the conceptual-mirror audit;
- self-verification by the SAU owner or self-validation of a conceptual mirror;
- conceptual similarity rendered as a formal Lean dependency, theorem
  equivalence, or certified functor without certificates;
- vague BLOCKED returns or unchanged retry loops;
- local Workers editing shared aggregation/site truth outside stabilization;
- a global coordinator that re-reads all transcripts instead of using bounded
  frontier-cell syntheses and compact graph-family memory.


## Cross-domain routes and source detail audit

Statistical Optimal Transport and Higher-Order Smoothness × Sampling are coordinated with the existing routes. Read `docs/cross-domain-program.md` and `docs/conceptual-mirror-protocol.md`; use `Libraries/cross-domain-program.json` for dependency-ready shared work and `website/content/graph_memory_index.json` for compact conceptual families. New Frontier Cells use schema 2 with `source_detail_audit`; new substantive advances use schema 4 and require `conceptual_mirror_audit` plus publication admission before `PROVED_LOCAL`. Search formal libraries first; when textbook detail is omitted, consult exact background theorems and record hypotheses/conventions instead of silently changing the target. Conceptual transport hyperedges are not Lean dependencies or certified functors. Upper-bound integrator and lower-bound oracle-hardness lanes remain independent until their comparison contracts match.


## Discrete Sampling peer route

Use `discrete-sampling` for finite-state Ising/Glauber, hard-core and matroid work,
not continuous-state time discretization. Read `docs/discrete-sampling-protocol.md`,
`Libraries/DiscreteSampling/source-map.json` and `.agents/prompts/discrete-sampling.md`.
Pull §3 foundations forward; use shared kernel/scalar/entropy cores without waiting
for SDEs. Every discrete route or shared discrete-consumer cell must carry
`discrete_state_contract`. The existing schema-v3 conceptual-mirror audit and independent
verification gates apply unchanged. Candidate bridge display is not validated admission.

## MCMC method / target perspective

Read `docs/mcmc-library-protocol.md`, `Libraries/MCMC/source-map.json` and
`website/content/sampling_perspectives.json`. MCMC is a method family; target
log-concavity, discrete state space and geometric/optimization lenses are distinct
axes. Keep source membership / planned-reuse colour independent of proof status.
Roberts–Rosenthal math/0404033v4 supplies general-state rigor; it is not merely a
bibliographic mention. Exact invariance, convergence, estimator error and numerical
bias are different obligations. Extend existing shared nodes before defining copies.
