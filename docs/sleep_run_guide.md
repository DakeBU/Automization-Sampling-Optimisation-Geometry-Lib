# ASTIS Sleep-Run Guide

The normal repeated-cycle command is:

```bash
python3 tools/astis.py sleep-run ASTIS-SALD-001 --cycles 2 --lower-count 1 --dry-run
```

For long faithful-paper batches, use the graceful wall-clock runner:

```bash
python3 tools/astis.py sleep-run-window ASTIS-SALD-001 \
  --hours 6 \
  --lower-count 1 \
  --agent-cmd 'bash tools/astis_codex_faithful.sh {root} {prompt}' \
  --execute \
  --check-each-cycle \
  --after-latex
```

`sleep-run-window` checks the wall clock only before starting a new cycle.  Once
a cycle starts, upper, middle, lower, reviewer, and the optional build gate all
run to completion even if the nominal window expires.

The convenience launcher is:

```bash
python3 tools/astis.py launch-sald-6h
```

It starts the same graceful 6-hour SALD process under `nohup`, writes a PID
file, writes a log under `runs/logs/`, runs one lower worker per cycle, checks
each completed cycle, and refreshes the human-readable exports after the final
completed cycle.  This includes both the internal proof article under
`paper-notes/` and, when configured, the external ASTIS technical-report
snippets selected by `ASTIS_TECH_REPORT_ROOT`.

During the inner cycle loop, ASTIS refreshes machine-facing memory such as the
retrieval index, TODO packet, paper-contribution map, and technical-lemma map.
It does not write a new Chinese summary for every cycle.  The Chinese summary
is a batch-end artifact and is written once by the finalizer after the 6-hour
window completes.

For `ASTIS-SALD-001`, `--after-latex` now runs the unified finalizer:

```bash
python3 tools/astis.py finalize-sald-cycle
```

The finalizer refreshes:

- `research-wiki/source-index/SALD_original.jsonl`;
- `proof-blueprints/ASTIS-SALD-001.md` and the legacy blueprint mirror;
- `research-wiki/paper-contributions/SALD/unfinished_source_map.md` and the
  legacy `research-wiki/paper-memory/ASTIS-SALD-001/` mirror;
- `research-wiki/technical-lemmas/index.md` and the legacy
  `research-wiki/technical-lemma-memory/` mirror;
- `research-wiki/retrieval-index/ASTIS-SALD-001.json`;
- `research-wiki/lemma-dags/SDE_Sampling_skill_tree.md` and
  `research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md`;
- `research-wiki/lemma-dags/Pro_assimilated_leaf_targets.md`;
- `docs/module-graph.svg` and
  `research-wiki/sampling-sde-library/lean-leaf-module-graph.md`;
- `docs/mathlib_ready_leaf_protocol.md`,
  `research-wiki/technical-lemmas/mathlib_ready_leaf_template.md`, and
  `research-wiki/technical-lemmas/hidden_regularities.md`;
- `runs/<latest-cycle>/memory_digest.md`, `runs/<latest-cycle>/todo.md`,
  `runs/<latest-cycle>/zh_summary.md`, and
  `runs/<latest-cycle>/article_update.tex`;
- `research-wiki/todo/SALD_REPRODUCTION_TODO.md`;
- `paper-notes/SALD/markdown/cycle-summaries/latest.md`;
- `paper-notes/project-paper/cycle-updates/ASTIS-SALD-001-latest.tex`;
- `paper-notes/AutoLeanInSleepSampling/markdown/zh/ASTIS-SALD-001-latest-zh.md`;
- `paper-notes/AutoLeanInSleepSampling/latex/main.tex`;
- `sections/generated_run_status.tex`, `sections/generated_middle_rules.tex`,
  and `sections/generated_memory_status.tex`
  under the configured technical-report checkout.

To disable this batch-end writing pass for a proof-only run, use:

```bash
python3 tools/astis.py launch-sald-6h --no-after-latex
```

## Batch-End Writing Pass

The project article export is intentionally not done after every small lower
agent change.  During Lean-heavy cycles, middle maintains the conversion window
and proof-obligation ledger.  After the final reviewer gate, the writing pass
translates the accepted Lean state and remaining proof obligations into
Markdown/LaTeX for humans:

```bash
python3 tools/astis.py export-latex
```

`export-latex` also calls:

```bash
python3 tools/astis.py export-technical-report
```

The internal Overleaf-style proof-note entry point is:

```text
paper-notes/AutoLeanInSleepSampling/latex/main.tex
```

The external technical report snippets updated by each batch are, relative to
the configured report checkout:

```text
sections/generated_run_status.tex
sections/generated_middle_rules.tex
```

The generated snippets are explanatory projections.  Lean files, conversion
windows, proof obligations, and reviewer logs remain the source of truth.

Every batch-end Chinese summary and technical-report update must start from a
non-Lean reader's view.  It must say, in plain language, which remaining items
are SALD paper contributions, which are reusable background technical lemmas,
why standard measure-theory/KL/SDE facts still need local Lean statements, and
what high-level choice a human can make before the next 6h run.

## Memory Gates

ASTIS uses two memory layers.

- `research-wiki/technical-lemmas/` and
  `AutoSamplingTheory/TechnicalLemmas/` store reusable prior knowledge:
  measure theory, probability, Taylor, Gaussian, variational, and SDE facts.
  A lemma is callable only if it is an ASTIS-owned compiled declaration.  The
  old `research-wiki/technical-lemma-memory/` path is a mirror for old runs.
- `research-wiki/paper-contributions/SALD/` stores SALD-specific paper
  contribution memory: source line ranges, proof DAG leaves, and unfinished
  paper obligations.  It should not store generic prior facts.  The old
  `research-wiki/paper-memory/ASTIS-SALD-001/` path is a mirror.
- `research-wiki/retrieval-index/<task>.json` is the compact packet that upper
  and middle should read before long logs.
- `verifier-feedback/` and `trial-log --feedback-field key=value` store typed
  reviewer/lower feedback such as `leaf`, `error_class`, `lean_build_ok`,
  `measure_theory_ok`, `technical_lemma_ok`, and `next_route`.

Reviewer should reject a completed-cycle claim if the finalizer did not refresh
the unfinished source-line map, if an active paper leaf lacks concrete source
lines, or if a technical lemma is cited before it exists as a compiled local
declaration.

## Mathlib-Ready Leaf Gate

Reusable background facts should be organized as Mathlib-ready leaf lemmas.
This is the main difference between "we know the paper proof in natural
language" and "the automation system can reuse the result in future
Sampling/SDE papers."

Run this command after changing the leaf decomposition rules or technical
lemma memory:

```bash
python3 tools/astis.py lemma-dag-refresh
```

It refreshes:

```text
docs/mathlib_ready_leaf_protocol.md
research-wiki/lemma-dags/SDE_Sampling_skill_tree.md
research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md
research-wiki/lemma-dags/Pro_assimilated_leaf_targets.md
research-wiki/technical-lemmas/mathlib_ready_leaf_template.md
research-wiki/technical-lemmas/hidden_regularities.md
agent-briefs/mathlib_ready_leaf_packet.md
```

For each next lower packet, middle must provide the theorem statement plus
local APIs and intended proof route.  If the same theorem repeatedly fails,
the next cycle must diagnose missing assumptions, false-statement risk,
representative mismatch, Mathlib API mismatch, or target size before trying a
new proof script.

## Lean Arsenal Module Graph

The public module graph is generated from the current Lean import tree and
declaration/export surface:

```bash
python3 tools/astis.py module-graph-refresh
```

It refreshes:

```text
docs/module-graph.svg
docs/assets/astis_lean_arsenal_module_graph.svg
docs/assets/astis_lean_arsenal_module_graph.png
research-wiki/sampling-sde-library/lean-leaf-module-graph.md
research-wiki/sampling-sde-library/cards/
research-wiki/external-lean-libraries/
research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json
```

Upper and middle agents should use this graph as the first routing map for
Sampling/SDE technical lemmas.  The SALD and PRIVATE modules are consumers.  The
current reusable arsenal is the green technical surface: `Probability.lean`,
`SDE.lean`, and `AutoSamplingTheory/TechnicalLemmas/*`.
The process-oriented leaf-network SVG is still generated by
`lemma-dag-refresh`, but it is a planning helper, not the public module atlas.

## ABEIS-Compatible Names

The names are aligned where this reduces cross-project memory load, but ASTIS
keeps Sampling/SDE-specific proof semantics.

| ABEIS-style function | ASTIS canonical name | ASTIS-specific meaning |
|---|---|---|
| Blueprint | `proof-blueprints/` | Lean/Sampling proof DAG and source-line system of record. |
| Agent briefs | `agent-briefs/` | Compact instructions for upper, middle, lower, reviewer. |
| Verifier feedback | `verifier-feedback/` plus trial-log fields | Typed Lean/SDE failure diagnosis, not a finite-matrix verifier. |
| Retrieval index | `research-wiki/retrieval-index/` | Small JSON read by upper/middle to avoid replaying long logs. |
| Paper memory | `research-wiki/paper-contributions/<paper>/` | The paper's own theorem leaves and LaTeX source lines. |
| Lemma memory | `research-wiki/technical-lemmas/` | Reusable KL/FI/LSI/Fokker--Planck/Ito/Taylor/probability blocks. |

Use the direct commands when inspecting a finished cycle:

```bash
python3 tools/astis.py memory-refresh ASTIS-SALD-001 --run-id latest
python3 tools/astis.py cycle-zh-summary ASTIS-SALD-001 --run-id latest
python3 tools/astis.py project-article-update ASTIS-SALD-001 --run-id latest
```

## Multi-Agent Layering

Prompt decks can run in lightweight mode or panel mode.  Lightweight inner
cycles use `10_upper_director`, `20_middle_formalizer`, lower agents, and
`40_reviewer_gate`.  Panel mode adds bounded specialist audits before the
director/coordinator synthesis.

| Prompt | Purpose |
|---|---|
| `11_upper_source_math.md` | Source-math auditor: LaTeX anchors, assumptions, regularity, boundary conditions, source-contract gaps. |
| `12_upper_proof_dag.md` | Proof-DAG strategist: root theorem, active leaves, stale leaves, lower split. |
| `13_upper_process_memory.md` | Process/memory auditor: repeated failures, stale memory, report usability, wasted routes. |
| `10_upper_director.md` | Director synthesis: one executable source-line leaf and non-goals. |
| `21_middle_source_correspondence.md` | Source-to-Lean formalizer: exact LaTeX lines, Lean boundary, hypotheses. |
| `22_middle_technical_lemma.md` | Technical lemma curator: ASTIS-owned lemmas, Mathlib/SLT provenance, port queue. |
| `23_middle_report_export.md` | Report/export maintainer: Chinese report, Markdown/LaTeX, technical report snippets. |
| `20_middle_formalizer.md` | Middle coordinator: lower packets. |
| `30_lower_1.md` | Natural-language proof scout. |
| `31_lower_2.md` | Lean implementation worker. |
| `32_lower_3.md` | Technical-lemma/API scout for the active leaf. |
| `40_reviewer_gate.md` | Build/source/fake-closure gate. |
| `41_reviewer_waste.md` | Final-audit opportunity-cost reviewer. |

This keeps the conversation role close to the upper layer: humans provide
global taste and priority, while the upper panel must still make a concrete
local decision inside the run.  Middle is deliberately split because
Sampling/SDE formalization has three different bottlenecks: source-line theorem
architecture, reusable background lemma retrieval, and human-report clarity.

The 6h Chinese report is written once during finalization.  It should be read
as an executive report: first the completion status, current exact blocker,
and whether time was wasted; then the detailed source-line map and technical
lemma table.

Default `launch-sald-6h` cadence:

```text
inner cycles: upper_director -> middle_formalizer -> lower_1/lower_2/lower_3 -> reviewer_gate
final audit: upper panel -> upper_director -> middle panel -> middle_formalizer -> reviewer_gate/reviewer_waste
```

With `launch-sald-6h`, lower agents run in parallel by default.  Their output
goes to `runs/<run>/agent-logs/<prompt>.log`.  The active-agent budget is the
sum of process durations, not just wall-clock time, so parallelism improves
iteration latency without pretending three simultaneous Codex calls cost only
one call.

Environment controls:

```bash
ASTIS_UPPER_PANEL_FINAL=1
ASTIS_UPPER_PANEL_INNER=0
ASTIS_MIDDLE_PANEL_FINAL=1
ASTIS_MIDDLE_PANEL_INNER=0
ASTIS_REVIEWER_WASTE_FINAL=1
ASTIS_LOWER_COUNT=3
ASTIS_PARALLEL_LOWER=1
```

## Monitoring

Use:

```bash
tail -f runs/logs/<run>.log
python3 tools/astis.py trial-summary
python3 tools/astis.py status
```

Do not kill a process just because the nominal 6-hour window has elapsed.  Let
the final cycle finish so that the dialogue board, trial log, reviewer gate,
and LaTeX export stay consistent.
