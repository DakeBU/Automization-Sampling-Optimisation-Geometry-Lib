# Agent Orchestration

Samplinglib formalizes sampling, optimisation, and geometry. This document
describes the historical plain-file workflow: prompt decks and dialogue
boards live in `runs/<run-id>/`; trial memory is appended to `runs/trials.jsonl`.
Use [AGENTS.md](../AGENTS.md) for the current theorem-sized Harness and the
[contributor contract](contributor-codex-contract.md) for English public readers.

MathCode workflow reference:
https://github.com/math-ai-org/mathcode

Design-lineage ledger:
`docs/attribution.md`

The roles are layered panels rather than one monolithic agent per layer.

Upper panel:

- `11_upper_source_math`: source anchors, assumptions, regularity,
  boundary conditions, conditional-law choices, and source-contract gaps.
- `12_upper_proof_dag`: root theorem, shortest dependency path, active leaf,
  stale leaf retirement, and lower split.
- `13_upper_process_memory`: repeated failures, stale memory, report
  usability, and token/time waste.
- `10_upper_director`: synthesizes the panel and chooses one executable
  decision.

Middle panel:

- `21_middle_source_correspondence`: exact LaTeX line range, paper object,
  Lean boundary, and hypotheses.
- `22_middle_technical_lemma`: ASTIS-owned technical lemma memory, Mathlib/SLT
  provenance, port queue, and background facts.
- `23_middle_report_export`: Chinese report, Markdown status, project article,
  and technical report snippets.
- `20_middle_formalizer`: synthesizes lower packets.

Lower agents:

- `lower_1`: natural-language proof route and dependency analysis.
- `lower_2`: Lean implementation of one theorem or one strictly smaller
  source-cited boundary.
- `lower_3`: technical-lemma/API scout for the smallest background fact needed
  by the active leaf.
- `lower_4`: optional refiner after a concrete Lean failure; not enabled by
  default.

Reviewer agents:

- `40_reviewer_gate`: build gate, source correspondence, cited results, and
  hidden assumptions.  Use `python3 tools/astis.py proof-diagnostics` for
  lightweight proof-statistics and hidden-placeholder summaries when needed.
- `41_reviewer_waste`: final-audit opportunity-cost reviewer; it checks
  wrapper churn, old-context replay, and low-value targets.

This four-role loop is part of the retained ARIS/Learning-Beyond-Gradients/QBE
automation frame.  In particular, ASTIS keeps the LBG-style idea that the
system improves through role-separated iterations over code, logs, summaries,
tests, and rejected directions; the reviewer remains a separate gatekeeper.
LeanMarathon adds the proof-blueprint control state, dynamic leaf discipline,
and illness-area refiner rule; it does not remove the trial memory, negative
cache, candidate-population, or reviewer-agent components.

Generate a dry prompt deck:

```bash
python3 tools/astis.py run-cycle ASTIS-SALD-001 --cycle 1 --lower-count 3 --upper-panel --middle-panel --reviewer-waste
```

Generate repeated decks:

```bash
python3 tools/astis.py sleep-run ASTIS-SALD-001 --cycles 2 --lower-count 1 --dry-run
```

Run a graceful 6-hour SALD batch:

```bash
bash tools/astis_run_sald_closure.sh
```

The launcher does not use shell `timeout`; once a cycle begins, it lets the
current sequence and build gate finish.  By default, inner cycles are light
proof-search cycles with no upper/middle panel.  The final audit runs the
upper and middle panels plus `reviewer_waste`, then writes the batch-end
Chinese report, internal proof-note export under
`paper-notes/AutoLeanInSleepSampling/`, and external ASTIS technical-report
snippets under `/home/nitanda_sub/mark/repos/Auto_Proof_Papers/ASTIS`.

The middle agent owns this two-way conversion layer.  During proof search it
keeps conversion windows and obligations synchronized; at batch end it performs
the ARIS-style paper-writing pass that explains the latest Lean state,
remaining blocker, source anchors, and updated coordination rules in
Markdown/LaTeX.

See `docs/phase_and_agent_tasklist.md` for the two-phase faithful-paper
discipline and `docs/sleep_run_guide.md` for monitoring details.
