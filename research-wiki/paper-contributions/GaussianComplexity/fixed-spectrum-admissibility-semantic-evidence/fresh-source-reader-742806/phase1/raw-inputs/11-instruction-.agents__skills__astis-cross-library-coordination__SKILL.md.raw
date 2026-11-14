# ASTIS Cross-Library Coordination

Use this skill whenever a theorem-sized task in the SampleWiki, Riemannian Optimization, or Optimisation route may touch mathematics that another route could also need.

## Goal

Let the three routes advance independently without creating duplicate or incompatible lower-level Lean declarations. Source-facing theorems remain attached to their own sources; only genuinely shared mathematical foundations are shared.

The public coordination surface is `/progress/`. The persistent unit of work is one JSON Frontier Cell under `research-wiki/frontier-cells/`. The machine check is:

```bash
python3 tools/astis_frontier_cells.py check
```

## Source authority

- **Log-Concave Sampling / SampleWiki:** Sinho Chewi's `main.pdf` is primary for the textbook; `supp.pdf` is an official Chapter 2 source layer; SampleWiki cases remain pinned to their primary papers.
- **Riemannian Optimization:** Nicolas Boumal is the source-facing route; Mathlib/shared geometry interfaces are searched first.
- **Optimisation:** Sinho Chewi's *Lectures on Optimization* (arXiv:2605.07006) is the public source-facing spine. Bubeck, Beck, and Nesterov are background/cross-check references; Optlib and CvxLean are formal upstreams.

## Mandatory pre-declaration audit

Before creating a declaration:

1. Recover the exact source theorem/definition, assumptions, domains, conclusion, constants, and conventions.
2. Search Samplinglib and Mathlib.
3. Search active `route: shared` Frontier Cells and `Libraries/shared-foundations.yml`.
4. For optimisation-relevant work, search the pinned Optlib and CvxLean surfaces.
5. Compare **semantic theorem fingerprints**, not names alone: objects, quantifiers, assumptions, conclusion, normalization, and intended consumers.
6. Record exactly one classification: `reuse`, `adapt`, `missing`, or `out_of_scope`.
7. Record exactly one decision: `reuse_existing`, `adapt_existing`, `new_route_local`, `new_canonical_shared`, or `out_of_scope`.

No Worker may skip this audit because a new declaration is easy to prove.

## Collision rule

- **Exact shared theorem:** keep one canonical shared declaration. Every route imports or depends on that declaration.
- **Near-equivalent theorem:** factor the genuinely common mathematical core once and keep a small route-specific adapter for convention or source differences.
- **Genuinely different theorem:** keep separate declarations even if names or formulas look similar.
- **Missing shared foundation:** open one canonical `route: shared` Frontier Cell. Do not open parallel route-local implementations.
- **Conflicting stable interfaces:** do not overwrite a stable declaration. Isolate the smallest common child theorem or adapter and serialize shared-file changes through stabilization.

If a route-local cell discovers `new_canonical_shared`, that route-local cell may remain `claimed`, `blocked`, or `quarantined`, but it may **not** advance to `proved_locally`. It must name `canonical_shared_cell`, then depend on the shared cell. `tools/astis_frontier_cells.py` enforces this invariant.

When one route discovers that another active route is rebuilding an existing declaration, stop the duplicate implementation, record the canonical reusable node, and rebase the dependent task on it.

## State machine

Every cell follows:

```text
claimed → proved locally → independently verified → stabilized → merged
    │
    └→ blocked → smaller child theorem → verified → re-entry
```

Repository states are `claimed`, `proved_locally`, `independently_verified`, `stabilized`, `merged`, `blocked`, and `quarantined`.

- `proved_locally` requires focused Lean evidence.
- `independently_verified` requires evidence from a verifier other than the proving Worker.
- `stabilized` requires root build and graph/index regeneration.
- `merged` requires the merge/PR reference.
- `blocked` requires an exact obstruction and at least one strictly smaller child cell.

A local proof is never a published route milestone merely because it compiles.

## Exploration vs stabilization

Parallel Workers own isolated theorem modules and focused tests. During exploration they should not independently edit shared aggregators, root registries, or another route's stable interface just to make a branch compile.

The single stabilization lane is responsible for:

- clean-porting onto current `main`;
- resolving duplicate theorem names/APIs;
- integrating canonical shared foundations;
- editing shared aggregators/root tests;
- updating Registry, graph, source, semantic-roundtrip, and site surfaces;
- root build and final merge.

This serialization is what lets parallel mathematical work remain efficient without making Samplinglib truth multi-valued.

## Verification contract

Every new or adapted node follows:

`source audit -> search/reuse -> theorem-sized Frontier Cell -> focused compile/test -> independent theorem review -> source-fidelity review when source-facing -> repository root build -> graph/index regeneration -> single stabilization lane -> merge`

Use `.agents/skills/astis-substantive-advance/SKILL.md` for the Worker packet and `.agents/skills/astis-semantic-roundtrip/SKILL.md` for source-facing semantic review.

## Shared-floor checkpoints

Treat these as intersection checkpoints, not automatic equivalences:

- Chewi sampling §2.5 Riemannian Manifolds ↔ Boumal geometry foundations.
- Chewi sampling §4.3 convex-optimization proof route ↔ Chewi Optimisation §§1-3 and §9 + compatible Optlib convex analysis.
- Chewi sampling Chapter 8 proximal sampler ↔ Chewi Optimisation §8 Proximal methods + relevant frontier sampling results.
- Chewi sampling Chapter 10 structured sampling ↔ Chewi Optimisation §10 Mirror methods and §12 Stochastic optimization + corresponding Optlib/CvxLean interfaces.

At every checkpoint, prove compatibility before reuse. If hypotheses or conventions differ, keep the difference explicit in an adapter.


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
