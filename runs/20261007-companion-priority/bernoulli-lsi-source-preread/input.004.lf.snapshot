---
name: astis-slt-reuse
description: Port or audit reusable probability/concentration results from YuanheZ/lean-stat-learning-theory into ASTIS-owned TechnicalLemmas under the repository-pinned Lean 4.33.0 toolchain.
argument-hint: "[upstream declaration]"
---

# ASTIS SLT Reuse

Use this before relying on a theorem inspired by
`YuanheZ/lean-stat-learning-theory`.  The theorem is callable only after it
has been ported as ASTIS-owned Lean code.

## Source

- GitHub: `https://github.com/YuanheZ/lean-stat-learning-theory`
- Paper: `https://arxiv.org/abs/2602.02285`
- Related AutoRes formalization: `https://github.com/auto-res/lean-rademacher`
- Related paper: `https://arxiv.org/abs/2503.19605`
- Local clone: `/home/nitanda_sub/mark/repos/outer_repos/sampling_theory_sde/lean-stat-learning-theory`
- Local AutoRes clone: `/home/nitanda_sub/mark/repos/outer_repos/automation_systems/lean-rademacher`
- Upstream toolchain: `leanprover/lean4:v4.27.0-rc1`
- ASTIS toolchain: `leanprover/lean4:v4.33.0`

## Workflow

1. Search `AutoSamplingTheory/TechnicalLemmas` and
   `research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl`.
2. For SALD, read
   `research-wiki/technical-lemma-memory/SALD_remaining_map.md`.
3. If no ASTIS local declaration exists, locate the upstream file and
   declaration as port source material.  Prefer the source whose statement
   matches the needed theorem boundary: `lean-rademacher` for concentration,
   Rademacher/symmetrization, separability, covering-number, and Dudley-style
   facts; `lean-stat-learning-theory` for the empirical-process proof program
   already tracked by ASTIS.
4. Copy the exact statement into a local ASTIS module or a reuse entry.
5. Classify status as `direct-port`, `needs-mathlib-api-update`,
   `reference-only`, `blocked`, or `formalized`.
6. If porting, adapt imports and Mathlib API changes in
   `AutoSamplingTheory/TechnicalLemmas/*.lean`; do not add SLT as a Lake
   dependency.
7. Run `python3 tools/astis.py check`.
8. Update `research-wiki/cited-results/SLT_reuse_audit.md` and
   `research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl`.

Do not treat an upstream theorem as proved in ASTIS until the corresponding
ASTIS declaration builds locally.

The Rademacher formalization is also a process model: large analysis projects
should stage reusable definitions, concentration lemmas, symmetrization
arguments, separability/countable-density bridges, and applications as named
DAG nodes.  Lower agents should not inline this whole pipeline into a SALD
proof attempt.
