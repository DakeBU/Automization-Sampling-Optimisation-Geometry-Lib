<div align="center">

# An Automated Theorem Proving System and Visualized Lean Library for Sampling, Optimisation, and Geometry

**Samplinglib:** Verified Sampling, Optimisation, Geometry Theory in Lean

[![Samplinglib](https://img.shields.io/badge/Samplinglib-formal_knowledge_graph-155EEF?style=flat-square)](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/)
[![Lean 4](https://img.shields.io/badge/Lean-4-6B4FBB?style=flat-square)](https://lean-lang.org/)
[![Samplinglib site](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/workflows/blueprint-site.yml/badge.svg)](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/workflows/blueprint-site.yml)

[**Home**](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/)
· [**Libraries**](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/libraries/)
· [**Current Progress**](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/progress/)
· [**Underlying Lean Graph**](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/underlying-lean-graph/)
· [**Harness**](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/workflow/)

</div>

ASTIS builds **Samplinglib**: natural-language mathematics, source anchors, Lean declarations, and theorem dependencies for sampling, optimisation, and geometry in one inspectable graph. Primary sources, official supplements, background textbooks, and formal upstream libraries have different roles and are recorded separately; frontier papers are inserted into the same graph so that their actual mathematical contribution can be compared, verified, and reused.

| Library | Primary source |
|---|---|
| Log-Concave Sampling | Sinho Chewi, textbook and official supplement |
| SampleWiki | Source-pinned frontier papers, including lower bounds |
| Riemannian Optimisation | Nicolas Boumal, *An Introduction to Optimization on Smooth Manifolds* |
| Optimisation | Sinho Chewi, *Lectures on Optimization* |
| Statistical Optimal Transport | Sinho Chewi, Jonathan Niles-Weed, Philippe Rigollet |
| Discrete Sampling | Zongchen Chen, Daniel Štefankovič, Eric Vigoda, *Spectral Independence and Local-to-Global Techniques for Optimal Mixing of Markov Chains* (arXiv:2307.13826v4) |
| Markov Chain Monte Carlo | Fearnhead, Nemeth, Oates, Sherlock, *Scalable Monte Carlo for Bayesian Learning* (arXiv:2407.12751) |

## News

- **2026-09-10:** Compiled and source-reviewed the first [SPHMC](conversion-windows/ASTIS-SW-SPHMC-2026.md) and [Proximal BPS](conversion-windows/ASTIS-SW-PBPS-2026.md) proof packets.
- **2026-09-09:** Connected mathematics-first readers to [chapter progress and semantic review](docs/theorem-publication-protocol.md).

- **2026-09-07:** Added Discrete Sampling and MCMC as peer libraries.
- **2026-09-05:** Added Statistical Optimal Transport and the Functor Hypergraph.
- **2026-08-30:** Unified cross-library progress and Frontier Cell collaboration.
- **2026-08-29:** Added source-fidelity checks and theorem denoising.
- **2026-07-27:** Added the Blueprint-style textbook and formalization website.
- **2026-07-17:** Established Auto-Sampling-Theory-In-Sleep.

## Research aim

```text
formalize → verify → connect → reuse
```

A paper may add a **LEAF**, **BRIDGE**, **SHORTCUT**, **HUB**, or **RE-ORGANIZATION**; these are overlapping structural signatures, not an automatic paper ranking. “A+B” is not inherently marginal: a reusable bridge that transports many later results can be major. A shallow A+B result instead leaves A and B as independent black boxes, joins them only in a terminal application, and creates little reusable transport, shortening, assumption relief, or downstream reach.

<p align="center">
  <img src="website/static/astis-formal-graph-value.svg" alt="How new mathematics changes the formal theorem graph" width="940">
</p>

## ASTIS Harness

Contributors start with `python3 tools/astis_publication.py packet --cell CELL_ID`.
The [publication protocol](docs/theorem-publication-protocol.md) synchronizes source
statements, formula proofs, folded Lean, assumption audits and chapter progress;
`check --base BASE_COMMIT` rejects missing or stale publication evidence.

The three formalization routes use the same theorem-driven verification workflow. A **Frontier Cell** is one theorem-sized advance with an exact target, known parents, a truth boundary, and a focused test. Parallel work may discover shared foundations, but shared declarations are reused or coordinated before publication; independent review and a single stabilization lane decide what becomes Samplinglib truth.

<p align="center">
  <img src="website/static/astis-harness-current.svg" alt="ASTIS Harness theorem-driven verification workflow" width="980">
</p>

```text
claimed → proved locally → independently verified → stabilized → merged
    │
    └→ blocked → smaller child theorem → verified → re-entry
```

Lean compilation does not by itself guarantee source fidelity. Source-facing nodes separately audit objects, domains, quantifiers, assumptions, and conclusions; denoising proposals remain explicit rather than silently changing the pinned theorem.

<details>
<summary><strong>Collaborative route protocol</strong></summary>

[Current Progress](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/progress/) is one dashboard containing **SampleWiki Route**, **Riemannian Optimization**, and **Optimisation**. Collaborators can advance different theorem-sized Frontier Cells while seeing the other routes and the shared Lean floor on the same page.

Persistent cells live under [`research-wiki/frontier-cells/`](research-wiki/frontier-cells/). Their status is evidence-backed and CI-checked by:

```bash
python3 tools/astis_frontier_cells.py check
```

Before creating a Lean declaration, a Worker must search Samplinglib, Mathlib, active shared Frontier Cells, and relevant formal upstreams. The candidate is classified as `reuse`, `adapt`, `missing`, or `out_of_scope`.

If a missing lower-level theorem is needed by two or more routes, **do not create parallel route-local copies**. Open one `route: shared` Frontier Cell, stabilize one canonical declaration, and let route-specific theorems depend on it. Near-equivalent statements use a shared mathematical core plus explicit adapters; genuinely different theorems remain separate. Shared aggregators, root registries, API collision resolution, and graph/index updates are serialized through one stabilization lane.

Full protocol: [docs/formalization-protocol.md](docs/formalization-protocol.md). Cross-route candidates and canonical shared declarations are recorded in [Libraries/shared-foundations.yml](Libraries/shared-foundations.yml).

</details>

## Attribution & design lineage

| Source | What Samplinglib / ASTIS learns from it | ASTIS-specific boundary |
|---|---|---|
| [Sinho Chewi, *Log-Concave Sampling*](https://chewisinho.github.io/main.pdf) | Primary sampling textbook order, theorem route, calculations, and source-facing statements | Faithful ASTIS paraphrase + exact source anchors + ASTIS-owned Lean declarations; no endorsement implied |
| [Sinho Chewi, *Supplement to Log-Concave Sampling*](https://chewisinho.github.io/supp.pdf) | Official material omitted from the book for space; currently the complete supplement to Chapter 2 | Treated as an additional primary-source layer and mapped after Chapter 2; summarized and formalized rather than republished wholesale |
| Sampling background / rigor references | Karatzas–Shreve, Protter, Revuz–Yor, Shreve, Bakry–Gentil–Ledoux, van Handel, Ledoux, Boucheron–Lugosi–Massart, Villani, Ambrosio–Gigli–Savaré, Santambrogio, Vershynin, and other references explicitly used or recommended around the source | Used to recover standard omitted hypotheses/proof details and cross-check conventions; they never silently replace Chewi's pinned theorem |
| [Nicolas Boumal, *An Introduction to Optimization on Smooth Manifolds*](https://www.nicolasboumal.net/book/) | Riemannian geometry and optimization spine | Chapter/source correspondence; no wholesale republication |
| [Sinho Chewi, *Lectures on Optimization*](https://arxiv.org/pdf/2605.07006) | Public theorem-proof source and chapter spine for the **Optimisation** Library | Formalized section by section from the public arXiv notes; source-facing statements remain pinned to Chewi |
| Bubeck (2015), [Beck (2017)](https://epubs.siam.org/doi/book/10.1137/1.9781611974997), Nesterov (2018) | Principal background sources named by Chewi for the optimization lectures | Background/theorem cross-checks rather than the public formalization spine |
| [Optlib](https://github.com/optsuite/optlib) | Existing convex-analysis, proximal, and optimization-algorithm theorem nodes | Provenance, compatibility, and adapters remain explicit; no silent duplication |
| [CvxLean](https://github.com/verified-optimization/CvxLean) | Formal optimization problems, equivalence, reduction, relaxation, and verified transformations | Reference/integration layer until compatibility is locally audited |
| [ATLAS v1](https://github.com/facebookresearch/atlas-lean/tree/e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6/v1) | Searchable external memory from 26 textbooks: 36,469 named source declarations with source lines, placeholder evidence, upstream target evaluations, and three-route candidate tags | CC BY-NC 4.0; the v1 rider limits use to academic/research purposes and prohibits commercial use and ML model training, fine-tuning, distillation, evaluation, or development; metadata is external reference only, and no theorem is local truth before an ASTIS-owned port passes the current Lean gate |
| [Lean-Ridgelet](https://github.com/shosonoda/lean-ridgelet) | Blueprint / implementation-map presentation | Extended from one formalization map to textbooks, frontier results, reusable theorem graphs, and source-aware statement review |
| [ARIS / Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | Long-running research, durable artifacts, recovery, and separate review | Durable state is source-backed Lean theorem progress rather than plausible research narrative |
| [Learning Beyond Gradients](https://github.com/Trinkle23897/learning-beyond-gradients) | Durable failures, rejected routes, iterative improvement, and system self-improvement | Keeps negative memory without permanent intellectual role boundaries |
| [EoH](https://github.com/FeiLiu36/EoH) | Competing candidate routes | Search is allowed only around fixed Lean-checkable targets; faithful source statements do not mutate |
| [LeanMarathon](https://github.com/YuanheZ/LeanMarathon) | Blueprint, proof-DAG leaves, bounded workers, and deterministic gates | Samplinglib makes theorem-graph memory, source correspondence, statement fidelity, and sampling-analysis obligations first-class |
| [MathCode](https://github.com/math-ai-org/mathcode) | Lean diagnostics and theorem-reuse ideas | Diagnostics are advisory; pinned Lean/source checks and independent verification are authoritative |
| [lean-stat-learning-theory](https://github.com/YuanheZ/lean-stat-learning-theory) | Mathlib probability, concentration, entropy, and functional-inequality proof idioms | External declarations become local truth only after an audited compatible port compiles |
| [StatsMLlib](https://github.com/Lean-MoDS/StatsMLlib) | Subject-owned modules, reuse-first formalization, and staged contribution | Samplinglib adds textbook correspondence, SampleWiki ingestion, statement fidelity, and graph-level contribution views |
| [FrontierAgent](https://github.com/ApodexAI/FrontierAgent) | Parallel generalist agents, bounded task boards, checkpointing, and no-progress control | ASTIS schedules theorem-DAG advances with Lean evidence, truth boundaries, independent verification, and serialized stabilization |
| [Quantum-Computing-Block-Encoding](https://github.com/DakeBU/Quantum-Computing-Block-Encoding) | Experience building automated formalization workflows | ASTIS specializes the machinery for sampling/SDE mathematics and theorem-sized Frontier Cells |

Full mathematical provenance and design lineage: [docs/attribution.md](docs/attribution.md).

## Quick start

Use the repository's pinned Lean toolchain and Python 3.12 or newer (CI uses
Python 3.12). An inherited `ELAN_TOOLCHAIN` overrides `lean-toolchain`; verify
`lean --version` before compiling. Native Windows Harness locks and atomic
publication are supported; their durability is limited by filesystem/device
flush guarantees, as documented in the implementation.

```bash
git clone https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib.git
cd Automization-Sampling-Optimisation-Geometry-Lib
python3 tools/astis.py check
python3 tools/astis_frontier_cells.py check
```

In PowerShell, select the pinned toolchain for the current shell with
`$env:ELAN_TOOLCHAIN = (Get-Content lean-toolchain -Raw).Trim()` and set
`$env:PYTHONUTF8 = '1'`. Select a Python 3.12+ executable explicitly if `python`
or `python3` resolves to an older interpreter or a Windows Store alias.

The [SampleWiki resumption packet](runs/20260908-samplewiki-resume/plan.md)
records the ordered shared-kernel route and its strict remaining boundaries.
Current verification/integration state comes from the Frontier Cells and the
SAU ledger, not from this historical run note.

```bibtex
@misc{bu2026astis,
  title  = {Auto-Sampling-Theory-In-Sleep: An Automated Theorem Proving System
            and Visualized Lean Library for Sampling, Optimisation, and Geometry},
  author = {Dake Bu and Ji Cheng and Huanjian Zhou and Andi Han and
            Zonghao Chen and Sinho Chewi and Matthew S. Zhang and Hau-San Wong and
            Qingfu Zhang and Atsushi Nitanda},
  year   = {2026},
  url    = {https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib}
}
```

**Project contributors:** Dake Bu, Ji Cheng, Huanjian Zhou, Andi Han, Zonghao Chen, Sinho Chewi, Matthew S. Zhang, Hau-San Wong, Qingfu Zhang, and Atsushi Nitanda.
