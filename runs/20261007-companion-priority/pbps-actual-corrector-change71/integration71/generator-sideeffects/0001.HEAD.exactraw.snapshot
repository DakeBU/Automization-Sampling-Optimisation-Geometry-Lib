# Log-Concave Sampling Six-Hour Execution Pack

Generated: `2026-08-02 02:28:31`

This pack is the control-console entry point for running the hierarchical
multi-agent system on the log-concave sampling foundation.  The run must keep
the textbook as the source roadmap and Mathlib-ready reusable leaves as the output.

## One-Command Launch

```bash
python3 tools/astis.py launch-log-concave-6h --hours 6 --wall-hours 24 --lower-count 3
```

This creates a long-window `sleep-run-window` job in the background.  It uses
an active-agent budget of 6 hours, keeps a larger wall-clock safety window, runs
lower workers in parallel, and executes `python3 tools/astis.py check` after
each cycle.

## Equivalent Direct Command

```bash
python3 tools/astis.py sleep-run-window ASTIS-CHEWI-001 \
  --hours 24 \
  --agent-hours-budget 6 \
  --max-cycles 64 \
  --lower-count 3 \
  --parallel-lower \
  --upper-panel-final \
  --middle-panel-final \
  --reviewer-waste-final \
  --agent-cmd "bash tools/astis_codex_faithful.sh {root} {prompt}" \
  --execute \
  --check-each-cycle
```

## GNU Screen Mode

Use this when you want the long run to live in a named terminal session:

```bash
screen -dmS astis_log_concave_6h bash -lc 'cd /home/nitanda_sub/mark/repos/Auto-Sampling-Theory-In-Sleep; python3 tools/astis.py sleep-run-window ASTIS-CHEWI-001 --hours 24 --agent-hours-budget 6 --max-cycles 64 --lower-count 3 --parallel-lower --upper-panel-final --middle-panel-final --reviewer-waste-final --agent-cmd "bash tools/astis_codex_faithful.sh {root} {prompt}" --execute --check-each-cycle'
```

Attach/detach:

```bash
screen -r astis_log_concave_6h
```

Inside screen, detach with `Ctrl-a d`.  The run itself writes per-agent logs
under `runs/<cycle>/agent-logs/` and the global trial ledger under
`runs/trials.jsonl`.

## Role Split

| Role | Job | Required output |
| --- | --- | --- |
| upper_director | Choose the one chapter/root/leaf that gives the most reusable progress; reject wrapper churn that does not serve the textbook tree. | One cycle packet with source anchor, shared roots, lower split, and reviewer gate. |
| upper_source_math | Audit the source statement and hidden regularity before proof search starts. | Source-faithfulness decision: supported, standard background, regularity gap, or statement drift. |
| upper_proof_dag | Pick the shortest dependency path through the shared-root DAG. | A small active leaf and stale-leaf retirements. |
| upper_process_memory | Check whether the run is repeating old work or ignoring existing compiled roots. | One process correction if needed. |
| middle_formalizer | Translate the upper packet into lower-ready Lean theorem shapes. | One lower_1 math route, one lower_2 Lean implementation task, optional lower_3 API scout task. |
| middle_source_correspondence | Map textbook prose to exact Lean-facing objects and assumptions. | Source line/range, informal statement, Lean statement skeleton, hidden regularity list. |
| middle_technical_lemma | Search Mathlib, local ASTIS registry, and external reference repos as provenance only. | Compiled-local, needs-small-port, or proof-obligation classification. |
| middle_report_export | Keep library summaries and run summaries synchronized after proof progress. | Plain-language update, not proof search. |
| lower_1 | Natural-language proof scout for exactly one leaf. | Math route, required hypotheses, expected Lean theorem shape, lower_2 handoff. |
| lower_2 | Lean implementer for exactly one theorem or smaller source-cited boundary. | Compiled declaration or precise typed blocker. |
| lower_3 | API/technical-lemma scout for missing reusable facts. | One tiny local port or proof-obligation packet. |
| reviewer_gate | Deterministic correctness gate. | `python3 tools/astis.py check` status, no fake closure, source/API consistency. |
| reviewer_waste | Progress-economics review for the 6h batch. | What improved, what wasted effort, and the best next leaf. |

## Cycle Discipline

1. Upper picks one reusable shared-root leaf, not an algorithm theorem unless
   all analytic roots are already local.
2. Middle translates the leaf into a stable theorem statement, source anchor,
   hidden regularity list, and Mathlib/API search target.
3. Lower workers either compile one small ASTIS-owned theorem or return a
   strictly smaller blocker.
4. Reviewer accepts only compiled local Lean, source-indexed proof obligations,
   concrete port plans, or explicit rejection of a false/unsupported statement.
5. After a successful cycle, regenerate DAGs, module cards, and retrieval
   indexes so the next screen cycle starts from the updated plan.

## First Three Recommended Cycles

| Cycle | Objective | Reason |
|---|---|---|
| 1 | Chapter map plus shared-root lock | Prevent the system from drifting into wrappers that do not close textbook leaves. |
| 2 | `CONV/MEAS` Prekopa-Leindler audit and smallest port candidate | This is the missing preservation root for functional inequalities. |
| 3 | `DENS/CONV` nonquadratic coercive Gibbs envelope | This connects textbook target densities to normalized probability laws beyond quadratic examples. |

## Hard Stops

- Do not treat external Lean repos as callable dependencies.
- Do not add assumptions just to make Lean close.
- Do not mark a red node blue without a local compiled declaration covered by
  `lake build` and `lake build Tests`.
- Do not let lower workers edit the same theorem block in parallel unless
  middle explicitly assigned disjoint files.
