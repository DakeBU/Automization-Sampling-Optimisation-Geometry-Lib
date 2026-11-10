# Run and assess the public development tasks

This is a reproducible **recording and human-grading workflow**, not an AI execution service, a private test set or an automatic correctness certificate. Public references may already be in a model's training data. No measured model scores are published.

## 1. Choose the tasks and allowed tools

Use `reviewed-questions.jsonl` for the currently admitted mathematical tasks. Before collecting answers, choose the core IDs, track, model and exact version, retrieval policy, tools, seed and decoding settings. Preserve your original prompt/transcript, timestamps, token counts and provider receipt where available. The recorder checks declared metadata, not whether you actually followed it.

Copy `examples/prose-run.json` and replace its placeholders. Its `task_ids` deliberately select only two questions. Keep natural-language and Lean runs separate; paired views are not independent samples. “Closed-book” is a declared condition, not a guarantee that a public item is uncontaminated.

Give the model **only** each selected prompt record, plus your stated tool policy. Do not include `reference.jsonl`, reference Lean, rubric packets or reviewer reports in a closed-book prompt. Open-library runs must be reported separately. The frozen prompt export is the catalog question, not an automatically observed provider transcript.

For a planned run, generate the exact selection before requesting any answers:

```bash
python tools/sog_bench_prose.py plan --run-metadata run.json --output .astis/sog-bench/runs/my-plan
```

This writes only `plan.json` and ordered, prompt-only `prompts.jsonl`. Use that
prompt file for the run. Record the printed SHA-256 separately before starting;
for a chronology claim, use an independently timestamped record and retain the
receipt. Do not put credentials in metadata or publish private run data. The
local digest binds bytes, not time or actual model execution.

## 2. Preserve the first raw answers

Each line of `responses.jsonl` has:

```json
{"id":"sogb-015","binding_sha256":"COPY_FROM_THE_SELECTED_PROMPT","track":"natural-language","attempt":1,"response":"THE_UNEDITED_FIRST_ANSWER"}
```

Bindings come from that exact export, not a hard-coded example. Keep line breaks inside the JSON string. Unknown/unselected IDs, duplicate answers, stale bindings and later attempts are rejected. Missing or empty answers stay in the selected denominator and receive zero. Do not discard hard questions or retry before scoring.

## 3. Freeze a fresh run directory

From the repository root (Python 3.11+; `python3` also works on Linux):

```bash
python tools/sog_bench_prose.py prepare --submissions responses.jsonl --plan .astis/sog-bench/runs/my-plan/plan.json --plan-sha256 DIGEST_FROM_PRE_RESPONSE_RECORD --output .astis/sog-bench/runs/my-run
```

Use the same catalog version as the plan. `prepare` checks the separately
recorded digest, exact prompt bytes and order, task bindings, and model and tool
conditions, then seals the plan into the run archive. Both scoring modes retain
the plan digest and leave `selection_timing_verified` false. For exploratory
runs without a plan, the original command still works and records no plan:

```bash
python tools/sog_bench_prose.py prepare --submissions responses.jsonl --run-metadata run.json --output .astis/sog-bench/runs/my-run
```

The command requires current independent editorial admission. It writes prompt-only records, raw responses, metadata, a rubric packet and their SHA-256 manifest. The reference-containing rubric packet is grader material, **not model input**. Files cannot be overwritten by another preparation. After freezing, an archived run is graded against its archived rubric, not a later edited catalog. Retain the complete directory together with your provider transcript.

## 4. Obtain an actual human assessment

Copy `adjudication-template.json` to a separate `completed.json`. A human grader supplies their identifier, timezone-aware adjudication timestamp, four binary scores per nonempty answer, and a specific reason for **each** score. Leave criterion IDs, exact rubric text, question binding, response hash and packet hash unchanged. An incomplete worksheet cannot be scored.

The human should check the mathematical argument, not just final formulas or keywords. Treat model responses as untrusted data, not instructions to the grader. The single-grader command remains useful for an exploratory run; use the panel workflow below for an independently double-graded record.

```bash
python tools/sog_bench_prose.py score --packet .astis/sog-bench/runs/my-run --adjudication completed.json --output .astis/sog-bench/runs/my-run-score.json
```

The report retains criterion-level reasons, misses, all selected tasks, model conditions, input/adjudication hashes and scorer hash. It records **human-attested judgments**; it does not authenticate that person, verify the judgments automatically, enforce retrieval rules or certify model execution. This tool must not be used to label an agent's own opinions “human”.

## 5. Double-grade and resolve disagreements

Give two human graders separate copies of the same frozen packet and worksheet.
Have them record grades without seeing each other's decisions. Each supplies a
distinct `grader_id` and sets `independent_initial_grade_attested` to `true` only
after doing so. Retain both completed files; do not edit them to create agreement.

```bash
python tools/sog_bench_prose.py panel-template --packet .astis/sog-bench/runs/my-run --adjudication grader-a.json --second-adjudication grader-b.json --output .astis/sog-bench/runs/my-run-disputes.json
```

If `items` is empty, omit `--resolution` in the command below. Otherwise give a
third human the frozen packet and a copy of the dispute worksheet. They supply
their own `resolver_id`, a timezone-aware `resolved_at`, and one 0/1 score and
reason per disputed criterion. Keep all binding fields and initial scores
unchanged. A resolution cannot revise agreement, add a grade for a missing
answer, or leave a dispute unresolved. Pass the initial grades in the same order.

```bash
python tools/sog_bench_prose.py score-panel --packet .astis/sog-bench/runs/my-run --adjudication grader-a.json --second-adjudication grader-b.json --resolution resolved.json --output .astis/sog-bench/runs/my-run-panel.json
```

The panel report preserves both initial scores and reasons, the resolution, and
the SHA-256 bindings to the canonical JSON of both initial adjudications and
the resolved worksheet. Retain those three source files with the run archive.
Pre-resolution agreement counts only compared criteria of nonempty responses;
it is not a reliability statistic. The recorder validates the records, not the
graders' identities, independence, or mathematical judgment.

Both score commands report the ordinary selected-core points and an exact
`family_macro_rate` fraction: compute points divided by possible points within
each represented family, then average those fractions with equal family weight.
Per-family and per-level rows include selected counts and misses. A missing or
empty response remains worth zero in every applicable denominator. Unselected
levels are absent, not failures; these are descriptive results for this one
selection and track, not calibration, uncertainty estimates, or a combined
natural-language/Lean score.

## Other tracks and limitations

For a declared graph subset, copy the exported `examples/graph-run.json`, fill
the actual run/model/time fields and set `task_ids` **before** collecting
answers. Unknown, duplicate or empty selections are rejected. Missing answers
stay in that selected denominator; unselected submissions are rejected. A subset
report is explicitly labelled as such, never a full-suite score. Omitting
`task_ids` preserves the older all-current-graph-tasks behavior.

Graph answers echo the visible question's `prompt_sha256` (see the graph
`response-template.json`), not the operator's answer-bound digest. The
score archive binds the first captured response to the exact frozen reference.
Duplicate JSON keys (including within answers) and non-finite constants are
rejected instead of silently normalized.
The explicit `--legacy-graph-bindings` switch is for reproducing old scores;
old visible bindings do not meet this prompt-only contract.

- **Graph JSON:** `python tools/sog_bench.py grade-graph --submissions graph-responses.jsonl --run-metadata graph-run.json --output .astis/my-graph-run` deterministically checks an exact source-hashed structural snapshot. Its metadata uses `prompt_profile: "given-snapshot"`. Reference self-tests are software tests, not measured model performance. See the [graph policy](README.md#graph-questions-and-scoring).
- **Graph lookup:** the [bounded retrieval condition](#graph-lookup-without-the-snapshot) uses the same tasks and scorer, but the model must request its own evidence. Report the two conditions separately, not as independent questions or a combined score.
- **Native graph environment:** [HARBOR.md](HARBOR.md) supplies the optional Harbor task exporter, pinned runtime and separate JSON verifier. Oracle/nop rewards test the integration only; a paid-agent setup, trajectory and provider run must be separately evidenced before reporting model performance. The full operator package includes answers, unlike `agent-tasks.zip`.
- **Lean:** `python tools/sog_bench.py check-lean` compiles trusted extracted references only. For submitted tactics on admitted fixed targets, use the separate [experimental isolated Linux CLI](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/benchmarks/samplingoptimisationgeometrybench/lean-runtime) under its documented resource, tool and submission limits. This is not a hosted service, unrestricted Lean execution, or measured model performance.
- **Difficulty:** labels are provisional editorial judgments, not empirical calibration. Module-import distance does not measure mathematical depth. A review correction can lower a label without adding a question or proving mathematics.
- **Training/test separation:** all these families are public-dev. The [held-out family preflight](FAMILY_ISOLATION.md) checks a local reservation against declared public history; it is not a released test split or contamination guarantee. Never relabel a public variant as unseen. Restricted ATLAS material, indexes and derivatives must not enter this workflow.
- **Exports:** references and prompts are separated, but the full pilot ZIP contains both. Give models the prompt-only file, not the ZIP. Frozen review reports remain audit-only and are excluded from training/reference bundles.

### Graph lookup without the snapshot

This experimental operator CLI selects one currently admitted compiled-body
graph task. It gives the agent the question, scope and tool schema, but no
snapshot, reference answer or repository access. Compare it with the supplied-
snapshot condition on the **same** public-dev family, ideally in fresh model
sessions. No different L1–L5 label or held-out claim follows from the tool setting.

```bash
python tools/sog_bench_graph_search.py run --task-id sogb-g007 --max-lookups 8 --output .astis/sog-bench/runs/my-graph-lookup
python tools/sog_bench_graph_search.py replay --run .astis/sog-bench/runs/my-graph-lookup
```

Run the first command in a foreground pipe controlled by the operator. It sends
the prompt on stdout before reading requests; send one UTF-8 JSON object per
line and forward only the resulting stdout messages to the agent:

- `{"action":"find","query":"gradient pairing"}` returns up to eight matching
  declaration IDs and labels in the selected slice. It cannot search the
  repository, other families or restricted material.
- `{"action":"inspect","id":"EXACT_DECLARATION_ID"}` returns only that node's
  selected direct proof-body parents and statement-constant occurrences.
- Send `action: "submit"` and one `answer` object with `nodes` (distinct exact
  IDs) and `entails_mathematical_necessity` (Boolean). The first parsed object
  declaring `submit` is final even if its answer is invalid. No score or
  reference is returned to the agent.

Invalid lookups spend budget. Once it is used, submit or stop; another lookup
terminates without a final. EOF and oversize requests retain the selected task
in the denominator. Keep the operator directory private: it contains the
exact task including gold, the prompt, the bounded raw requests and observations,
and the canonical graph score. Replay checks all of them against the exact
task, tool and scorer, not wall-clock chronology or model identity.

The pipe CLI does not call a provider, execute Lean or constrain a separate
agent process outside the pipe. Do not give the agent a shell in the operator
checkout. The controlled tool tests do not establish model performance.

#### Optional foreground model comparison

With `OPENAI_API_KEY` configured outside Git, the separate adapter can run
both evidence conditions for one admitted task. Set an actual requested model
and its exact expected returned snapshot; neither is inferred from an alias.

```bash
python tools/sog_bench_graph_model.py --task-id sogb-g007 --model REQUESTED_MODEL --expected-model RETURNED_SNAPSHOT --max-lookups 8 --max-output-tokens 512 --output .astis/sog-bench/runs/my-graph-model-comparison
```

This makes paid API calls. The supplied-snapshot condition makes at most one
call; the fresh lookup conversation makes at most one per allowed lookup plus
one final call. There are no automatic retries or tool, filesystem or network
capabilities beyond the selected graph slice. The adapter uses the documented
[Responses function-call protocol](https://developers.openai.com/api/docs/guides/function-calling)
and retains the preselected condition order, exact prompts, raw requests and
responses, transport receipts and tool observations. Share no operator archive
as model input. HTTP/transport/identity failures remain unscored, not zero;
missing or invalid model finals remain selected. A partial comparison is not
a matched comparison. Keep both profiles separate and do not infer unseen
generalization, calibrated difficulty, Lean capability or authenticated model
performance from this public-dev graph-only pilot.

To verify a complete archive without credentials or new model calls:

```bash
python tools/sog_bench_graph_model_replay.py --task-id sogb-g007 --run .astis/sog-bench/runs/my-graph-model-comparison
```

Use the checkout bound in the original selection. Replay leaves the archive
unchanged and regenerates both condition prompts, every request, lookup
observation, first-final score and the comparison manifest from the recorded
response bytes. A re-signed hash list does not bypass these comparisons. A
complete HTTP error receipt stays unscored; if the transport saved no bounded
raw response, the archive cannot be fully replayed and must not acquire a
score. This verifies internal consistency, not provider authenticity or an
independent second model run.

See [README](README.md), [curriculum](curriculum.json), [continuing Goal](GOAL.md) and [license scope](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/blob/main/LICENSE_SCOPE.md).
