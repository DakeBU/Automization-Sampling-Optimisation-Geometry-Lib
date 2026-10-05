# Optimisation contributor prompt

Use the following prompt to start a Codex/ChatGPT formalization session for the Optimisation Route.

Before anything else, pull the latest `main` and read the common collaborator bootstrap and contract:

`AGENTS.md`  
`CONTRIBUTING.md`  
`.agents/prompts/collaborator-contribution.md`  
`docs/contributor-codex-contract.md`  
`docs/theorem-publication-protocol.md`

The common contract is authoritative for reader publication, shared-lemma reuse, encoder–denoiser semantic checks, Lean/Overview/Functor graph publication, collaboration safety, and stabilization. The Optimisation instructions below add route-specific source/dependency guidance; they do not weaken the common contract.

---

You are working on the **Optimisation Route** of Samplinglib:

https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep

The primary formalization source is:

Sinho Chewi, *Lectures on Optimization*  
https://arxiv.org/pdf/2605.07006

Formalize Chewi's notes section by section. Bubeck, Beck, and Nesterov are background/cross-check references rather than the controlling public source. Mathlib, Optlib, and CvxLean are formal upstreams that must be searched before reproving existing mathematics.

Before starting, read:

`docs/formalization-protocol.md`  
`.agents/skills/astis-substantive-advance/SKILL.md`  
`.agents/skills/astis-cross-library-coordination/SKILL.md`  
`Libraries/frontloaded-shared-spine.json`  
`Libraries/shared-foundations.yml`  
`Libraries/FirstOrderOptimization/upstreams.yml`  
`research-wiki/frontier-cells/README.md`

Then inspect:

`/progress/#optimisation`

Use the current graph/progress state rather than a stale chapter schedule.

## Front-loaded shared-spine rule

Optimization Chapters 1-2 are not merely route-local chapters. They are expected producers of canonical Euclidean foundations used immediately by Log-Concave Sampling Chapters 1-2 and Statistical OT Chapter 1. Before proving a chapter-local version of convexity, strong convexity, subgradient, differential/gradient, quadratic-energy, chain-rule, energy-dissipation, or Grönwall facts, inspect the matching `sf-*` node in `Libraries/frontloaded-shared-spine.json`.

Book order is not Lean dependency order. If Statistical OT §1.5 needs an exact Fenchel/conjugacy lemma from Optimization Chapter 9, it is legitimate to extract that theorem early into the shared spine after auditing its own source prerequisites. **Do not** mark Chapter 9 complete, and do not drag the whole Chapter 9 API forward.

Conversely, Optimization Chapter 2 should share scalar chain-rule/energy-dissipation/contraction lemmas with later sampling/Riemannian consumers, but it must not invent a universal `GradientFlow` abstraction that identifies Euclidean ODE, Riemannian flow, and Wasserstein flow definitionally.

Advance **one theorem-sized Frontier Cell at a time**. Choose the smallest currently reachable theorem/interface that materially advances Chewi's notes and has useful downstream leverage.

Before adding a Lean declaration, search in this order:

Samplinglib → Mathlib → active shared Frontier Cells / `Libraries/shared-foundations.yml` → Optlib / CvxLean → route-local near-equivalent declarations.

Compare exact mathematical semantics rather than declaration names.

Record:

`classification: reuse | adapt | missing | out_of_scope`

and

`decision: reuse_existing | adapt_existing | new_route_local | new_canonical_shared | out_of_scope`

Important sampling intersections include:

Optimization Chapter 1 → Sampling Chapter 2 strong-convexity/log-concavity prerequisites  
Optimization Chapter 2 → Sampling §§1.4-1.5 scalar energy-dissipation/contraction ingredients  
Optimization Chapter 9 ↔ Statistical OT §§1.5-1.6, pulled forward only at the exact shared-duality lemma level  
Chewi Sampling Chapter 8 ↔ Optimisation Chapter 8 Proximal methods  
Chewi Sampling Chapter 10 ↔ Optimisation Chapter 10 Mirror methods and Chapter 12 Stochastic optimization

These are **candidate intersections, not assumed equivalences**.

For example, a convexity/proximal/mirror lemma that is mathematically identical across fields should become one canonical shared Lean node. A sampling-specific Markov kernel, invariant-law argument, RGO construction, stochastic correction, transport optimizer, or manifold adapter remains route-specific unless its exact semantics match.

If you discover a missing theorem needed by another textbook/research lane, **do not implement a private Optimisation version**. Record `decision: new_canonical_shared`, open/reference one `route: shared` Frontier Cell, and make the current cell depend on it.

Register/update the Frontier Cell JSON before substantial implementation.

For every changed production declaration, satisfy the common contributor contract before claiming completion: populate the required `reuse_plan`, `reader_contract`, and `graph_contribution`; publish a Chapter-1.3-quality declaration lesson; run the source-blind encoder–denoiser audit for source-facing claims; and record the exact Lean Branches / Overview / Functor graph delta. Do not add a Functor edge merely because two formulas look similar.

Use the ASTIS state machine:

`claimed → proved_locally → independently_verified → stabilized → merged`

If blocked:

`blocked → strictly smaller child theorem → verification → re-entry`

A blocked cell must identify the exact obstruction and a smaller child. Do not keep broadening the task or replaying an unchanged proof attempt.

In `faithfulPaper` mode, Chewi's exact theorem remains controlling. Background books may clarify the proof but cannot silently replace his assumptions or theorem statement.

Prefer focused compilation/tests during exploration. Do not independently edit root registries, shared aggregators, or stable common interfaces. Those changes are serialized during stabilization.

The proving worker may establish `proved_locally`, but **cannot self-assign `independently_verified`**.

Before handoff, run the exact current contract gates. In particular, the incremental contributor-contract command supports `check --base ...` or `check --ci`; there is no `--strict` flag.

Start now by inspecting the latest `main`, the common collaborator contract, the front-loaded shared spine, current Optimisation dashboard, Chewi's next reachable theorem(s), Mathlib/Optlib/CvxLean matches, and existing shared cells. Select the next substantive Frontier Cell, perform the complete reuse audit, register it, and then push the formalization forward as far as real evidence allows.