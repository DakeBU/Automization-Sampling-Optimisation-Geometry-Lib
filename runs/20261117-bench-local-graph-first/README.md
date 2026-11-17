# First paired local-model graph diagnostic

Two existing public-dev families were selected before inference: the convex
flow proof/statement graph (`sogb-g007`) and the quadratic lower-bound graph
(`sogb-g010`). Each has a supplied-snapshot condition and a fresh conversation
with up to eight graph lookups. The model chooses any lookup actions; the
operator does not insert successful queries or correct its answer.

The fixed model is Qwen2.5-0.5B-Instruct at revision
`7ae557604adf67be50417f59c2c2f167def9a775`, using the previously pinned local
Safetensors/tokenizer and CPU inference packages. No API or download was used.
The [selection](suite/selection.json) records assets, source fingerprints,
greedy float32 decoding, seed 6015, four CPU threads, 192 new tokens per turn,
8192 input tokens, tool budget and condition order. The pre-run digest is
`0a2abcf1f00e17983683c3f4652d23310011c55f1a4ebdf3ae5e34dbc7d989e0`.

## Observed result

| Task | Evidence condition | Input/output tokens | Valid final | Score |
| --- | --- | ---: | --- | ---: |
| sogb-g007 | Supplied snapshot | 1169 / 125 | No | 0 |
| sogb-g007 | Bounded lookup | 622 / 91 | No | 0 |
| sogb-g010 | Supplied snapshot | 1224 / 76 | No | 0 |
| sogb-g010 | Bounded lookup | 593 / 48 | No | 0 |

All four generations contained Markdown-fenced multiline JSON with fields
other than the specified action schema. The collector consumed the raw lines
without repair. Neither lookup condition made a valid `find` or `inspect`
call; the eight charged non-final lines are **not eight successful searches**.
Each condition ended on its first generation, with no valid final and no
second model turn. There was no inference exception. Thus both conditions
record 0/2 on this selection, not an estimate of graph reasoning quality,
mathematical knowledge, or the benefit of retrieval. Output lengths were
below the declared 192-token cap; the observation is not output truncation.

## Inspect or reproduce the accounting

[Model captures](model/) retain exact messages, input/output token IDs and
unedited text. [Collector records](suite/runs/) retain raw action bytes and
actual observations. [Accounting](accounting.json) is a derived convenience
report, not an independently trusted score. From this checkout:

```bash
python tools/sog_bench_graph_local.py replay --output runs/20261117-bench-local-graph-first --plan-sha256 0a2abcf1f00e17983683c3f4652d23310011c55f1a4ebdf3ae5e34dbc7d989e0
```

Replay loads no model and executes no generated code. It regenerates the
conversation and scores from the recorded bytes; it does not authenticate
inference, timestamps or operators. Independent code and runtime/readback
reviews are kept [separately](../20261117-bench-local-graph-review/).
Token consistency is a separate pinned-tokenizer check, not part of that CLI.

These are public, potentially contaminated tasks and one small model, not a
held-out benchmark, difficulty calibration, model ranking or Lean evaluation.
Keep this diagnostic out of training/reference gold and retain failures in
the selected denominator. A stronger model or structured-output protocol
would require a new predeclared run, not repairs to this one.
