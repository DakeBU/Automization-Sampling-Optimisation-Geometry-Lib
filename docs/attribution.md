# Attribution and Design Lineage

Samplinglib distinguishes **mathematical source provenance** from **system-design lineage**. A primary mathematical source controls a source-facing theorem; an official supplement adds source material; a background textbook can recover omitted standard details or cross-check conventions; a formal upstream can be reused after compatibility is audited. None of these roles is silently substituted for another.

## Mathematical source hierarchy

### Log-Concave Sampling

- **Primary source:** Sinho Chewi, [*Log-Concave Sampling*](https://chewisinho.github.io/main.pdf). This controls the textbook order, source-facing statements, assumptions, calculations, and source anchors.
- **Official source supplement:** Sinho Chewi, [*Supplement to Log-Concave Sampling*](https://chewisinho.github.io/supp.pdf), dated November 2, 2024. The supplement states that it contains material omitted from the book for space. Its current contents are entirely a **Supplement to Chapter 2**: Marton's tensorization, concentration of measure, tensorization and Gozlan's theorem, metric-measure spaces and synthetic Ricci curvature, exercises, and references. Samplinglib maps all of these sections after Chapter 2.
- **Background and rigorous-completion references:** when the book intentionally sketches standard details, ASTIS makes the hidden hypotheses explicit and cross-checks them against standard sources. Current references include Karatzas--Shreve, *Brownian Motion and Stochastic Calculus*; Protter, *Stochastic Integration and Differential Equations*; Revuz--Yor, *Continuous Martingales and Brownian Motion*; Shreve, *Stochastic Calculus for Finance II*; Steele, *Stochastic Calculus and Financial Applications*; Pavliotis, *Stochastic Processes and Applications*; Le Gall, *Brownian Motion, Martingales, and Stochastic Calculus*; Bakry--Gentil--Ledoux, *Analysis and Geometry of Markov Diffusion Operators*; van Handel, *Probability in High Dimension*; Ledoux, *The Concentration of Measure Phenomenon*; Boucheron--Lugosi--Massart, *Concentration Inequalities*; Vershynin, *High-Dimensional Probability*; Villani, *Topics in Optimal Transportation* and *Optimal Transport: Old and New*; Ambrosio--Gigli--Savaré, *Gradient Flows in Metric Spaces and in the Space of Probability Measures*; and Santambrogio, *Optimal Transport for Applied Mathematicians*.

These background references do **not** replace Chewi's theorem. They are used to justify or reconstruct standard prerequisites that a compact source proof may leave implicit. Per-lemma provenance is also recorded in `website/content/implicit_prerequisites.json`.

### Riemannian Optimization

- **Primary source:** Nicolas Boumal, [*An Introduction to Optimization on Smooth Manifolds*](https://www.nicolasboumal.net/book/).
- **Formal/background layer:** Mathlib and compatible Samplinglib geometry interfaces are searched before new lower-level definitions or lemmas are introduced.

Boumal remains the source-facing chapter authority. A shared Lean lemma is reused across Chewi/Boumal only after the objects, hypotheses, conventions, and conclusion have been checked for semantic compatibility.

### Optimisation

- **Primary public source:** Sinho Chewi, [*Lectures on Optimization*](https://arxiv.org/pdf/2605.07006), May 11, 2026. This 149-page public theorem--proof document is the chapter spine that Samplinglib formalizes.
- **Background lineage explicitly named by Chewi:** Sébastien Bubeck, *Convex Optimization: Algorithms and Complexity* (2015); Amir Beck, [*First-Order Methods in Optimization*](https://epubs.siam.org/doi/book/10.1137/1.9781611974997) (2017); and Yurii Nesterov, *Lectures on Convex Optimization* (2018). Chewi states that his notes are primarily based on these sources.
- **Formal upstreams:** [Optlib](https://github.com/optsuite/optlib) and [CvxLean](https://github.com/verified-optimization/CvxLean), together with Mathlib.

Beck is therefore an important background and theorem cross-check, but it is **not** the public formalization spine of the Optimisation website. The public route follows Chewi's arXiv notes section by section.

### ATLAS v1 external memory

- **Source:** [facebookresearch/atlas-lean v1](https://github.com/facebookresearch/atlas-lean/tree/e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6/v1), pinned at `e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6`.
- **License boundary:** v1 is limited to academic/research use under CC BY-NC 4.0. Its rider prohibits commercial use and use to train, fine-tune, distill, evaluate, or otherwise develop ML models. The root Apache-2.0 license does not relicense `v1/`.
- **ASTIS use:** a deterministic metadata index covers all 36,469 named source declarations and records exact file/line anchors, direct placeholders, upstream target evaluations, topics, and conservative route candidates. The external source stays in a separate checkout.
- **Truth boundary:** an ATLAS record is never blue or locally callable. It must be statement-audited, minimally ported or reproved under the ASTIS toolchain, tested, registered, source-mapped, and independently reviewed.

The relevant surfaces are probability/stochastic analysis for the SampleWiki and sampling floor, differential/manifold geometry for Riemannian Optimization, and convexity/duality/algorithmic material for Optimisation. These are retrieval candidates, not claims of theorem equivalence with Chewi or Boumal.

### OpenAI Math external proof memory

- **Source:** [openai/math](https://github.com/openai/math), pinned for the
  current intake at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`
  (October 6, 2026).
- **License:** Apache-2.0 for the published repository. Individual manuscript
  citation instructions and source provenance remain attached to their upstream
  directories.
- **ASTIS use:** proof-route retrieval, statement and definition comparison,
  candidate reusable leaves, and external conceptual/source graph nodes. The
  seven-library placement map is
  `research-wiki/openai-math-textbook-coverage.json`.
- **Truth boundary:** upstream Comparator evidence or compiling `OAI.*` code is
  not an ASTIS-owned theorem, does not become a solid local Lean edge, and does
  not imply that a whole manuscript family has been formalized. Local blue
  status still requires an ASTIS-owned declaration passing the current Lean,
  source-fidelity and publication gates.

### Source/copyright boundary

The public reader distinguishes:

- a primary or official source, cited with exact anchors;
- a necessary short quotation when appropriate;
- a faithful ASTIS paraphrase;
- an ASTIS supplemental derivation or hidden-assumption packet;
- an ASTIS-owned Lean formalization.

A public source is not wholesale republished merely because it is used as a formalization target. The reader summarizes, anchors, and formalizes the mathematics while retaining source provenance.

## System-design lineage

ASTIS is not a copy of any single automation system. It is a Lean-first sampling/SDE proof system whose design is shaped by source fidelity, hidden regularity, conditional laws, weak generators, KL/FI/LSI chains, discretization, reusable formal memory, and independent verification.

| Source | Design idea absorbed by ASTIS | ASTIS-specific boundary | Why it matters here |
|---|---|---|---|
| Sho Sonoda's [Lean-Ridgelet](https://github.com/shosonoda/lean-ridgelet) and [Blueprint site](https://shosonoda.github.io/lean-ridgelet/blueprint/html-multi/overview/#Lean-Ridgelet-Blueprint--L2-theory___-arXiv___2106___04770v2-implementation-map) | Blueprint-style organization and an implementation map linking informal mathematics to Lean declarations. | Lean-Ridgelet is Apache-2.0. ASTIS independently implements its website and formal graph, copying no Lean-Ridgelet code or template. | The implementation-map idea is extended to textbooks, hidden-assumption packets, theorem DAGs, frontier results, and reusable formal memory. |
| [ARIS / Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Long-window autonomous research, durable artifacts, recovery, and separate review. | ASTIS makes source-backed Lean theorem state and exact proof obligations the primary object rather than experiments or paper drafting alone. | Long runs remain recoverable without treating a plausible narrative as mathematical truth. |
| [Learning Beyond Gradients](https://github.com/Trinkle23897/learning-beyond-gradients) | Durable trial memory, rejected routes, iterative improvement, and system self-improvement. | The current Harness keeps durable evidence and negative memory without treating fixed roles as intellectual boundaries. | Failed proof routes remain reusable negative knowledge. |
| [EoH](https://github.com/FeiLiu36/EoH) | Population-style competing solution routes. | Candidate variation is permitted only after a Lean-checkable target is fixed; `faithfulPaper` mode may not mutate the source theorem or assumptions to make proof easier. | Alternative proof mechanisms can be explored without weakening source fidelity. |
| [LeanMarathon](https://github.com/YuanheZ/LeanMarathon) and [arXiv:2606.05400](https://arxiv.org/abs/2606.05400) | Blueprint as system of record, dynamic proof-DAG leaves, bounded workers, connected-problem refinement, and deterministic gates. | ASTIS keeps a local source-backed blueprint and theorem graph rather than requiring GitHub/PR/Slurm as its execution substrate. | The active target is selected from the dependency graph instead of from a flat task list. |
| [MathCode](https://github.com/math-ai-org/mathcode) | Lean diagnostics, theorem-reuse memory, hidden-placeholder scans, and subgoal planning. | Diagnostics are advisory; ASTIS acceptance still requires its pinned Lean gate plus explicit source correspondence. | Search and diagnosis accelerate proof work without becoming a substitute for formal verification. |
| [lean-stat-learning-theory](https://github.com/YuanheZ/lean-stat-learning-theory) and [arXiv:2602.02285](https://arxiv.org/abs/2602.02285) | Mathlib proof idioms for probability, concentration, entropy duality, functional inequalities, and discretization. | Toolchain differences mean external declarations are audited reference/port memory until compatible local declarations compile. | Later Workers can borrow verified theorem shapes rather than repeatedly reconstruct informal analogies. |
| [StatsMLlib](https://github.com/Lean-MoDS/StatsMLlib) and its [contributor guide](https://statsmllib.github.io/contribute.html) | Subject-owned module placement, reuse-first development, complete-proof policy, source attribution, whole-library verification, and staged contribution. | Samplinglib adds textbook/paper correspondence, SampleWiki ingestion, theorem-DAG placement, strict obstructions, and source-aware admission. | The library is organized as reusable subject knowledge rather than one-off proof scripts. |
| [FrontierAgent](https://github.com/ApodexAI/FrontierAgent) | Bounded task boards, parallel generalist sub-agents, structured reports, checkpoint/resume, fanout guards, and coordinator no-progress protection. | ASTIS replaces generic file tasks with source-backed theorem-DAG advances and requires Lean evidence, truth boundaries, independent verification, graph placement, and serialized stabilization. | It supports broad Worker capability and bounded global coordination without allowing generic task completion to masquerade as theorem progress. |
| [Quantum-Computing-Block-Encoding](https://github.com/DakeBU/Quantum-Computing-Block-Encoding/tree/wip/ghl2025-faithful-20260518-0201) | The earlier concrete Upper/Middle/Lower/Reviewer Harness, conversion windows, proof obligations, and proof-blueprint discipline. | ASTIS replaces quantum-specific contracts with sampling/SDE objects and has since moved from permanent role boundaries to theorem-sized Universal Workers and dynamic Frontier Cells. | The earlier hierarchy supplied useful source and review discipline; the current Harness keeps those invariants while reducing context handoff. |
| ABEIS-style internal harness naming | Compatible names for proof blueprints, agent briefs, verifier feedback, retrieval indexes, paper contribution memory, and technical-lemma memory. | ASTIS feedback is typed for sampling/SDE proof work: source-line coverage, Lean build, Mathlib API, measure theory, regularity assumptions, technical lemmas, and theorem status. | Shared vocabulary reduces engineering overhead without importing another domain's mathematical semantics. |

## Earlier and current Harness architecture

The earlier ASTIS Harness was intentionally role-layered:

```text
Upper
source audit · mathematical strategy · proof-DAG planning
    ↓
Middle
source ↔ Lean correspondence · retrieval · theorem mapping
    ↓
Lower workers
proof scouting · Lean implementation · API search
    ↓
Reviewer
Lean gate · source audit · fake-closure rejection
```

That architecture established several invariants that remain important:

- source statements and assumptions must stay explicit;
- proof attempts and failures need durable typed evidence;
- Lean success does not replace source-semantic review;
- verification should be independent of the proving attempt;
- failed routes should be remembered rather than rediscovered.

The current Harness changes the **unit of delegation**, not those invariants. A Universal Worker handles one Substantive Advance Unit end to end. Nearby advances form dynamic Frontier Cells, ordinary code reduces their structured state, and a Thin Master handles only cross-frontier decisions.

```text
source + verified Lean graph
        ↓
Substantive Advance Board
        ↓
Frontier Cells
Universal Workers in parallel
        ↕
Discovery Ledger + deterministic reduction
        ↓
Thin Master
        ↓
Independent verification
        ↓
Single stabilization lane
        ↓
Samplinglib + Underlying Lean Graph
```

Historical `upper`, `middle`, `lower_*`, and `reviewer` names remain valid when reading old logs or selecting execution profiles. They no longer define what an agent is permitted to notice, prove, refactor, test, or explain.

## Why the formal graph is a scientific output

Samplinglib is the verified library, but ASTIS is also intended as an instrument for understanding sampling theory. A prose proof does not by itself tell us exactly which assumptions were required, which lemmas are safely reusable, or how a result attaches to the accumulated body of checked mathematics.

Lean verification turns a result into an exact callable declaration. The Underlying Lean Graph records its parents and consumers. This lets a reader ask whether new work adds a terminal leaf, bridges previously separate branches, shortens an important dependency route, creates a reusable interface, exposes a hidden regularity assumption, or reorganizes a substantial part of the proof structure.

This graph-level view is not itself a theorem about scientific importance. It is a structural lens for making the conceptual spine of a field easier to learn, inspect, and compare.

## Mode boundary

The EoH-style population element remains separated from faithful paper reproduction.

- In `faithfulPaper`, ASTIS may keep several proof routes for a fixed lemma, but it may not change the source theorem, assumptions, constants, or proof target.
- In `exploratoryProof`, ASTIS may compare theoretical variants once the acceptance predicate is explicit and Lean-checkable.

The acceptance rule is stricter than every search heuristic: a mathematical claim is admitted only through compiled Lean plus explicit source correspondence and independent verification, or it remains a named proof obligation, discovery, blocker, or quarantined claim.
