# Contributing to ASTIS and Samplinglib

ASTIS welcomes focused corrections, reusable Lean lemmas, faithful textbook
reconstruction, proof-route metadata, diagrams, and website improvements. This
guide keeps mathematical claims, local Lean evidence, and route progress
separate throughout review.

## 0. Collaborator / Codex entry point

All contributors and coding agents acting for them must begin from the current
repository instructions, not from a copied chat prompt.

After pulling the latest `main`, read:

1. `AGENTS.md`
2. this `CONTRIBUTING.md`
3. `.agents/prompts/collaborator-contribution.md`
4. `docs/contributor-codex-contract.md`
5. `docs/theorem-publication-protocol.md`
6. `.agents/skills/astis-substantive-advance/SKILL.md`
7. the relevant route prompt under `.agents/prompts/`

The common bootstrap is intentionally thin. The authoritative collaboration,
reader, reuse, encoder-denoiser, graph, and stabilization rules live in
`docs/contributor-codex-contract.md` and the theorem-publication protocol.

For changed production declarations, run the incremental contract against the
branch base, for example:

```bash
python3 tools/astis_contributor_contract.py check --base "$(git merge-base HEAD origin/main)"
```

or use `python3 tools/astis_contributor_contract.py check --ci` in the CI-style
mode. The tool has no `--strict` flag.

## 1. Discuss the scope

Small corrections and narrowly scoped API improvements can go directly to a
pull request. Open an issue before starting any of the following:

- a new textbook theorem route or paper-reproduction target;
- a new module, namespace, or import boundary;
- a change to an existing theorem statement, source correspondence, or
  mathematical assumptions;
- a large port from Mathlib or another Lean repository;
- a change to the ASTIS harness, typed artifacts, or acceptance gate.

State the mathematical result, source, proposed owner module, expected
dependencies, and whether the result is a reusable technical leaf or a
textbook/paper-specific consumer.

## 2. Develop in the owning layer

Before proving a new lemma, search the [declaration catalog](https://dakebu.github.io/Auto-Sampling-Theory-In-Sleep/declarations/),
the [implementation map](https://dakebu.github.io/Auto-Sampling-Theory-In-Sleep/implementation-map/),
the local Lean tree, Mathlib, and relevant compatible upstreams such as Optlib,
CvxLean, or StatsMLlib. Prefer an existing declaration when its statement and
hypotheses really match. Generalize a canonical shared lemma when that is the
mathematically faithful reusable boundary; do not add route-local wrappers just
to manufacture reuse counts.

Keep these ownership boundaries explicit:

| Contribution | Canonical owner |
|---|---|
| Reusable measure, probability, analysis, process, SDE, sampler, optimisation, transport, or geometry lemma | The corresponding subject module under `AutoSamplingTheory/TechnicalLemmas/` |
| Selected reusable leaf and its provenance | `AutoSamplingTheory/TechnicalLemmas/Registry.lean` after it compiles locally |
| Textbook theorem consumer | The relevant route module and source-correspondence/publication record |
| Paper-specific theorem route | `research-wiki/paper-contributions/<paper>/` |
| Open proof target or agent handoff | A typed ASTIS packet; never a claim of local proof completion |
| Teaching exposition or route milestone | Reviewed metadata under `website/content/` |
| Diagram | Editable Mermaid under `website/diagrams/` |

Use the Lean and Mathlib versions pinned by `lean-toolchain` and
`lakefile.lean`. Follow nearby Mathlib-style naming, imports, docstrings, and
file headers. Preserve original authorship and license notices when adapting
external code, and record the exact source and any substantive changes.

Do not close mathematics with `sorry`, `admit`, `axiom`, `constant`,
`postulate`, `Prop := True`, or `:= trivial`. A task card, interface structure,
natural-language theorem, or successfully elaborated proposition is not a
proof. Add a Registry entry only for a reusable ASTIS-owned declaration that
compiles under the pinned toolchain.

For every new or changed production declaration, the corresponding Frontier
Cell must satisfy the current contributor contract, including `reuse_plan`,
`reader_contract`, and `graph_contribution` where required by the gate.

## 3. Publish source-facing mathematics, not only Lean code

Compilation certifies the Lean proposition, not its fidelity to a cited source.
Every source-facing declaration must follow `docs/theorem-publication-protocol.md`
and `docs/contributor-codex-contract.md`.

Use `textbook/chapter-01/section-1-3.html` as the reader-quality reference. Keep
source statement, notation and hidden assumptions, a readable natural-language
formula proof, source-vs-Lean assumption differences, folded exact Lean
statement/proof, actual ASTIS and external-library dependencies, and the
remaining mathematical boundary adjacent and source ordered.

The authored sources of truth are the declaration lessons and publication
metadata under `website/content/`; do not hand-edit generated `_site/` HTML.

Source-facing claims also require the encoder-denoiser semantic round trip:
original theorem/restatement -> Lean -> source-blind reconstruction ->
independent anti-anchored source review. The proving/formalizing actor must not
self-certify the independent review. Do not fabricate historical audit evidence;
old contributions that predate a required audit remain explicit legacy debt
until honestly re-audited.

Every contribution also records its graph delta. The Lean Branches Graph uses
compiler-backed formal structure; source/semantic/conceptual overlays stay
separate. The Overview Graph records route/frontier/publication placement. The
Functor Hypergraph receives only genuine reviewed conceptual mirrors; otherwise
record `none-found`. Preserve the canonical evidence-status and library-scope
colour semantics and the solid-formal / dashed-overlay edge distinction.

## 4. Verify the change

Install the pinned dependency cache once, then run the full relevant gate from
the repository root:

```bash
lake exe cache get
LEAN_NUM_THREADS=$(nproc) lake build
python3 tools/astis.py check
python3 tools/astis.py harness-test
python3 tools/astis_semantic_roundtrip.py check
python3 tools/astis_frontier_cells.py check
python3 website/scripts/lean_gate.py
ASTIS_PUBLIC_SOURCE_LINKS=1 python3 website/scripts/build_site.py
ASTIS_PUBLIC_SOURCE_LINKS=1 python3 website/scripts/check_site.py
```

For a branch contribution, also run the diff-aware publication and contributor
contract checks with the appropriate base commit, as specified in
`docs/contributor-codex-contract.md`.

The public-source flag is appropriate only when the current commit is available
on the public remote. Omit it for unpushed or private preview work; generated
pages will use checked site-local source anchors.

Before submission, confirm:

- the whole Lean build and ASTIS deterministic check pass;
- no forbidden placeholder or fake-closure token was introduced;
- imports follow the subject dependency direction and avoid a new cycle;
- the mathematical source, assumptions, constants, and endpoint conditions are
  recorded precisely;
- local declaration status and textbook/paper route status are not conflated;
- new reusable leaves have focused tests and Registry metadata when warranted;
- shared-lemma reuse was audited against Samplinglib, Mathlib, and relevant
  compatible upstreams;
- source-facing declarations have honest encoder-denoiser evidence;
- reader metadata satisfies the Chapter 1.3 presentation contract;
- Lean/Overview/Functor graph changes preserve their distinct truth semantics;
- website metadata names only declarations that exist in the current source;
- generated files under `_site/` are not committed.

## 5. Submit a focused pull request

Use the pull request template. A reviewer should be able to identify the result
and acceptance evidence without reconstructing them from the diff. Include:

- the mathematical statement and exact source anchor;
- the owning module and dependency/API decisions;
- reusable leaves, paper/textbook consumers, and remaining obligations;
- the local declaration status and mathematical route status;
- source-vs-Lean hidden/API-only assumptions;
- encoder-denoiser / independent-review status;
- shared-lemma reuse decisions and real/planned consumers;
- Lean Branches / Overview / Functor graph delta;
- commands run and their results;
- adapted-code provenance, copyright, license, and authorship changes;
- any deliberate follow-up work, stated as open rather than complete.

Review checks source fidelity, hidden hypotheses, theorem drift, module
ownership, duplicate APIs, proof completeness, reader quality, graph truth,
and gate evidence. Accepted contributions are credited in Git history and
relevant source-file author headers. For co-written commits, add one trailer for
each additional author:

```text
Co-authored-by: Full Name <email@example.com>
```

This workflow is informed by StatsMLlib's staged contribution process, adapted
to ASTIS's source correspondence, dual status model, hierarchical proof
packets, shared-lemma graph, encoder-denoiser audit, and Samplinglib memory
boundary.