# Samplinglib collaborator contribution bootstrap

Use this prompt as the common entry point for any external or internal collaborator (including `jicheng9617`, `andyjm3`, `hudsonchen`) and for Codex/ChatGPT agents acting on their behalf.

This file is intentionally a **thin bootstrap**, not a second copy of the project protocol. The authoritative rules live in the files listed below; if they change, follow the latest repository version.

## Read first

Before planning or editing, pull the latest `main` and read, in this order:

1. `AGENTS.md`
2. `CONTRIBUTING.md`
3. `docs/contributor-codex-contract.md`
4. `docs/theorem-publication-protocol.md`
5. `.agents/skills/astis-substantive-advance/SKILL.md`
6. the relevant route prompt under `.agents/prompts/` (for example `.agents/prompts/optimisation.md`, `.agents/prompts/samplewiki-route.md`, or `.agents/prompts/statistical-optimal-transport.md`)

Repository-local instructions are authoritative. Do not rely on a copied prompt from chat when it conflicts with the current repository.

## Required planning output

Before coding, identify:

- the exact source theorem/statement and edition/anchor;
- the Lean declaration(s) to add, change, or reuse;
- the canonical owning module and Frontier Cell;
- existing Samplinglib / Mathlib / compatible upstream declarations searched;
- whether the result is reuse, an adapter, a new route-local leaf, or a genuinely reusable shared declaration;
- the reader-publication delta;
- the encoder–denoiser / source-blind semantic-audit plan;
- the Lean Branches Graph, Overview Graph, and Functor Hypergraph delta.

Do not start by creating a route-local helper if an equivalent or more reusable canonical lemma already exists.

## Non-negotiable publication contract

For every new or changed source-facing production declaration, follow `docs/contributor-codex-contract.md` and `docs/theorem-publication-protocol.md` exactly. In particular:

- reader presentation follows the Chapter 1.3 standard: source statement, notation/assumptions, natural-language formula proof, source-vs-Lean assumptions, folded Lean statement/proof, exact ASTIS and external-library dependencies, and remaining boundary;
- source-facing claims require the encoder–denoiser semantic round trip with a source-blind reconstruction and independent anti-anchored review;
- Frontier Cells record `reuse_plan`, `reader_contract`, and `graph_contribution`;
- formal Lean dependency edges remain distinct from source/semantic/conceptual overlays;
- Functor Hypergraph entries are added only for genuine reviewed conceptual mirrors; otherwise record `none-found`;
- do not fabricate historical audit evidence. Old work that predates a required audit is legacy debt until it is honestly re-audited.

## Collaboration safety

Do not overwrite shared registries, ledgers, graph truth, or concurrent contributor work with an old branch snapshot. Rebase or clean-port onto current `main`, use the repository's fragment/serialized mechanisms where provided, and preserve original contributor ancestry/credit.

## Checks

Use the exact commands required by the current protocol. For the incremental contributor contract, the supported interface is:

```bash
python3 tools/astis_contributor_contract.py check --base "$(git merge-base HEAD origin/main)"
```

or the CI-oriented form:

```bash
python3 tools/astis_contributor_contract.py check --ci
```

There is **no `--strict` flag**. Continue with the publication, semantic-roundtrip, Frontier Cell, site/graph, Lean/Tests, and ASTIS gates required by `docs/contributor-codex-contract.md` before claiming completion.

## Final report

Report separately:

1. source statements covered;
2. Lean declarations added/reused/generalized;
3. hidden/API-only assumptions;
4. external-library dependencies;
5. semantic round-trip and independent-review status;
6. shared-lemma reuse decisions and consumers;
7. Lean/Overview/Functor graph changes;
8. remaining mathematical boundary, blockers, or legacy audit debt.
