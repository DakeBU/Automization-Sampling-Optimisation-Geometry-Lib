# Run and assess the public development tasks

This is a reproducible **recording and human-grading workflow**, not an AI execution service, a private test set or an automatic correctness certificate. Public references may already be in a model's training data. No measured model scores are published.

## 1. Freeze the tasks and allowed tools before collecting answers

Use `reviewed-questions.jsonl` for the currently admitted mathematical tasks. Before collecting answers, choose the core IDs, track, model and exact version, retrieval policy, tools, seed and decoding settings. Preserve your original prompt/transcript, timestamps, token counts and provider receipt where available. The recorder checks declared metadata, not whether you actually followed it.

Copy `examples/prose-run.json` and replace its placeholders. Its `task_ids` deliberately select only two questions. Keep natural-language and Lean runs separate; paired views are not independent samples. “Closed-book” is a declared condition, not a guarantee that a public item is uncontaminated.

```bash
python tools/sog_bench_prose.py freeze --run-metadata run.json --output .astis/sog-bench/selection
```

Keep the printed selection SHA-256 in a separate, time-stamped lab record
before collecting answers. The receipt binds the ordered task set, exact
prompt bytes, model/version and declared conditions. Do not regenerate it to
repair a failed or incomplete run. Give the model **only** the selected rows
from `selection/prompts.jsonl`, plus the declared tool policy. Keep
`selection.json`, references, Lean answers, rubrics and reviews off the model
input. Report closed-book, supplied-source and open-library runs separately.
The digest checks consistency with the separately supplied value; it does not
authenticate its date or show what a provider actually received.

## 2. Preserve the first raw answers

Each line of `responses.jsonl` has:

```json
{"id":"sogb-015","binding_sha256":"COPY_FROM_THE_SELECTED_PROMPT","track":"natural-language","attempt":1,"response":"THE_UNEDITED_FIRST_ANSWER"}
```

Bindings come from that exact export, not a hard-coded example. Keep line breaks inside the JSON string. Unknown/unselected IDs, duplicate answers, stale bindings and later attempts are rejected. Missing or empty answers stay in the selected denominator and receive zero. Do not discard hard questions or retry before scoring.

## 3. Freeze a fresh run directory

From the repository root (Python 3.11+; `python3` also works on Linux):

```bash
python tools/sog_bench_prose.py prepare --submissions responses.jsonl --selection .astis/sog-bench/selection --selection-sha256 RECORDED_SHA256 --output .astis/sog-bench/runs/my-run
```

The command requires current independent editorial admission and the exact
selected bindings. It archives the receipt, prompt-only records, raw responses,
and grader-only rubric with their manifest. If a selected task changed or its
admission became stale, use the original admitted release to archive the run;
do not replace the question after seeing an answer. Retain the archive with
the actual provider transcript. A legacy `prepare --run-metadata` is still
available for retrospective archives and is not a preselected run.

## 4. Obtain an actual human assessment

Copy `adjudication-template.json` to a separate `completed.json`. A human grader supplies their identifier, timezone-aware adjudication timestamp, four binary scores per nonempty answer, and a specific reason for **each** score. Leave criterion IDs, exact rubric text, question binding, response hash and packet hash unchanged. An incomplete worksheet cannot be scored.

The human should check the mathematical argument, not just final formulas or keywords. Treat model responses as untrusted data, not instructions to the grader. Independent double grading and adjudication are recommended before using the results for scientific comparison; they are not provided or claimed by this pilot.

```bash
python tools/sog_bench_prose.py score --packet .astis/sog-bench/runs/my-run --adjudication completed.json --selection-sha256 RECORDED_SHA256 --output .astis/sog-bench/runs/my-run-score.json
```

The report retains criterion-level reasons, misses, all selected tasks, model
conditions and evidence hashes. When a separately recorded digest was supplied
to `score`, the report records that comparison; omitting it leaves only an
internal consistency check. This records **human-attested judgments**; it does
not authenticate the grader, verify the mathematics automatically, enforce
retrieval rules or certify model execution. Do not label an agent's opinions
“human”.

## Other tracks and limitations

For a declared graph subset, copy the exported `examples/graph-run.json`, fill
the actual run/model/time fields and set `task_ids` **before** collecting
answers. Unknown, duplicate or empty selections are rejected. Missing answers
stay in that selected denominator; unselected submissions are rejected. A subset
report is explicitly labelled as such, never a full-suite score. Omitting
`task_ids` preserves the older all-current-graph-tasks behavior.

- **Graph JSON:** `python tools/sog_bench.py grade-graph --submissions graph-responses.jsonl --run-metadata graph-run.json --output .astis/my-graph-run` deterministically checks an exact source-hashed structural snapshot. Its metadata uses `prompt_profile: "given-snapshot"`. Reference self-tests are software tests, not measured model performance. See the [graph policy](README.md#graph-questions-and-scoring).
- **Native graph environment:** [HARBOR.md](HARBOR.md) supplies the optional Harbor task exporter, pinned runtime and separate JSON verifier. Oracle/nop rewards test the integration only; a paid-agent setup, trajectory and provider run must be separately evidenced before reporting model performance. The full operator package includes answers, unlike `agent-tasks.zip`.
- **Lean:** `python tools/sog_bench.py check-lean` compiles trusted extracted references only. The separate experimental [fixed-target Linux workspace](lean-runtime/WORKSPACE.md) supports isolated submission and target/axiom checks. The [model bridge](lean-runtime/MODEL.md) requires real provider setup; software trials are not model measurements.
- **Difficulty:** labels are provisional editorial judgments, not empirical calibration. Module-import distance does not measure mathematical depth. A review correction can lower a label without adding a question or proving mathematics.
- **Training/test separation:** all these families are public-dev. Create genuinely new, independently authored private families before publication; never relabel a public variant as unseen. Restricted ATLAS material, indexes and derivatives must not enter this workflow.
- **Exports:** references and prompts are separated, but the full pilot ZIP contains both. Give models the prompt-only file, not the ZIP. Frozen review reports remain audit-only and are excluded from training/reference bundles.

See [README](README.md), [curriculum](curriculum.json), [continuing Goal](GOAL.md) and [license scope](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/blob/main/LICENSE_SCOPE.md).
