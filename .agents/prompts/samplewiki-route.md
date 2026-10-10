# SampleWiki Route contributor prompt

Use the following prompt to start a Codex/ChatGPT formalization session for the SampleWiki Route.

---

You are working on the **SampleWiki Route** of Samplinglib:

https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep

Your goal is to reach useful SampleWiki frontier results through the shortest dependency-first route while reusing the canonical Log-Concave Sampling textbook spine. **SampleWiki is not the owner of the Chewi textbook foundation.** If a prerequisite is simply part of the main textbook, treat it as a dependency of the frontier route rather than relabeling the textbook work as a SampleWiki theorem.

Before doing any mathematical work, read the current repository state and in particular:

`docs/formalization-protocol.md`  
`.agents/skills/astis-substantive-advance/SKILL.md`  
`.agents/skills/astis-cross-library-coordination/SKILL.md`  
`.agents/skills/astis-semantic-roundtrip/SKILL.md`  
`Libraries/frontloaded-shared-spine.json`  
`Libraries/shared-foundations.yml`  
`research-wiki/frontier-cells/README.md`

Also inspect the current dashboard and detailed SampleWiki route rather than relying on an old plan:

`/progress/#samplewiki`  
`/progress/samplewiki-detail.html`

Primary mathematical sources are the exact primary papers behind the relevant SampleWiki cases. Chewi's `main.pdf` and `supp.pdf` are the canonical Samplinglib textbook spine that those frontier results may depend on. Background textbooks may recover omitted standard details, but they must not silently change either the paper theorem or the textbook theorem.

## Boundary between textbook and frontier work

First apply `execution` in `website/content/samplewiki_companion_frontiers.json`.
The four fixed-v1 paper Goal proceeds PBPS/SPHMC+composition, then Gaussian
Cloud Section6/errors/costs, then midpoint upper/lower/finitestep results, ahead
of unrelated textbook work. A later shared dependency may come first only to
remove an identified current blocker with a real consumer;
the dependency and fidelity rules below remain mandatory. Preserve older cells.
Do not let new graph/citation/download features delay correct paper lemmas.

When the shortest path to a SampleWiki theorem passes through Chewi Sampling Chapters 1-2, first inspect `Libraries/frontloaded-shared-spine.json`. Convexity, coupling/Wasserstein, semigroup, manifold, empirical-concentration and related low-level facts should come from their canonical shared nodes. Do not create a SampleWiki-local copy, and do not count completion of those textbook prerequisites as a frontier theorem contribution.

This matters especially for the early shared spine:

- Sampling §1.3 should consume the canonical coupling/Wasserstein core co-developed with Statistical OT Chapter 1;
- Sampling §2 strong-convexity/log-concavity prerequisites should reuse the Optimization Chapter-1 convex core;
- Sampling §2.5 should consume the minimal first-order manifold adapter extracted from Boumal Chapter 3;
- Sampling §2.4 and Statistical OT Chapter 2 may share empirical-measure/basic concentration leaves while keeping frontier lower-bound/statistical arguments distinct.

Work on **one substantive theorem-sized Frontier Cell at a time**. Choose the smallest currently reachable cell that materially advances the dependency path toward useful SampleWiki results. Do not ask me to choose a theorem if the existing graph/progress state gives enough evidence for you to choose well.

Before creating any Lean declaration, perform the mandatory shared-floor audit. Search existing Samplinglib declarations, Mathlib, active `route: shared` Frontier Cells, `Libraries/frontloaded-shared-spine.json`, and `Libraries/shared-foundations.yml`. Compare theorem semantics, not only names: objects, domains, quantifiers, assumptions, normalization, conclusion, and intended consumers.

Classify the candidate as `reuse`, `adapt`, `missing`, or `out_of_scope`, and record the corresponding decision.

If the missing lower-level theorem is also useful to another textbook/research lane, **do not implement a SampleWiki-local duplicate**. Record `decision: new_canonical_shared`, open or reference one `route: shared` Frontier Cell, and make the SampleWiki cell depend on that shared cell.

Create/update the persistent Frontier Cell JSON under `research-wiki/frontier-cells/` before substantial implementation.

Follow the ASTIS state machine strictly:

`claimed → proved_locally → independently_verified → stabilized → merged`

If blocked:

`blocked → strictly smaller child theorem → verification → re-entry`

A blocked result must identify the exact mathematical/Lean obstruction and create or name a smaller child cell. Repeating the same failed proof route is not progress.

In `faithfulPaper` mode, never weaken, strengthen, or repair the source statement merely to make Lean compile. A compiled Lean proposition is not enough: source-facing results also require the semantic/source-fidelity workflow.

During exploration, prefer isolated theorem modules and focused tests. Do not casually edit shared aggregators, Registry/root interfaces, or another route's stable API. Shared integration belongs to the stabilization lane.

The proving worker may move a cell to `proved_locally` with real focused-check evidence, but must **not self-certify `independently_verified`**.

Keep the Frontier Cell record and PR template synchronized with actual evidence. Never claim a state beyond what has passed.

Start now by inspecting the latest `main`, the current SampleWiki dependency frontier, the canonical Log-Concave Sampling textbook spine, front-loaded shared foundations, and available Lean declarations. Select the next substantive frontier cell, record its source/reuse audit, and then push the mathematics and Lean implementation as far as the protocol legitimately allows.
