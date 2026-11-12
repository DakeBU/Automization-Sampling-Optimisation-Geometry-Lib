# Optional model-to-compiler bridges

The [credential-free JSONL transport](#credential-free-jsonl-transport) can
connect an operator's local model or another agent without a Responses API
account. Both transports use the same isolated Lean workspace and verifier.

`tools/sog_bench_lean_model.py` connects one explicitly selected Responses API
model to an existing pristine fixed-target compiler workspace. This is a finite
foreground process, not a website service or background ASTIS session. Its unit
fixtures do not make provider calls, execute Lean, certify native integration,
or establish model performance. Independent review and actual provider/native
acceptance remain required before advertising this as a tested model runner.

## What reaches the model

Only the canonical `agent/prompt.json`, `agent/Solution.lean.txt`, fixed tool
instructions and bounded feedback. Their hashes are checked against the frozen
operator packet. The bridge does not directly append the operator directory,
reference proof, source oracle, challenge or runtime configuration, and offers
no general shell, filesystem or network tool. The default arm offers no separate
lookup; the opt-in transport pilot below returns only bounded signatures.
Submitted Lean can nevertheless
print readable public container data into bounded compiler feedback; the accepted
runtime mounts no oracle directory. This is not new feedback noninterference or
enforced closed-book isolation. The original public-dev answers are public and may
be in model training; restricted ATLAS content must never enter this interface.
This is not a held-out test or proof of closed-book knowledge.

The compiler function is `lean_workspace({action, source})`, where action is `check`
or `submit` and source is full Lean text. All Lean remains data until the existing
workspace passes it to the provisioned Linux Docker/Landrun verifier. No host
Lean or shell fallback is added. The accepted runtime's type/definition, axiom
and fresh-kernel checks, resource bounds and trust assumptions are unchanged.

## Operator setup

First follow [WORKSPACE.md](WORKSPACE.md), on its supported Linux environment,
with pinned Lean4.33.0, Mathlib and the native runtime. Export and stage the
selected targets. Freeze the *whole* evaluation selection with `suite-start`
before any model work; do not collect only successful responses. For a genuinely
single-target pilot, `start` already freezes denominator1. Use these declared
provenance fields, replacing both model placeholders with the intended actual
snapshot/version. The returned `model` must exactly equal the frozen
`model_version`; missing or different identity stops dispatch. If intentionally
requesting an alias, freeze the expected returned snapshot ID in advance rather
than resolving it after seeing the response. There is no automatic alias repair.
Repeated provider response IDs are rejected even with distinct tool-call IDs.
The raw response and identity/usage are retained before tool dispatch:

```json
{
  "kind": "declared-model-run",
  "provider": "openai",
  "model": "YOUR_EXPLICIT_MODEL",
  "model_version": "YOUR_EXPLICIT_VERSION",
  "retrieval_profile": "provided-prompt-template-only",
  "tools": ["lean_workspace"],
  "decoding": {"max_output_tokens": 4096},
  "seed": null
}
```

This narrow bridge rejects mismatched tool/retrieval/decoding declarations. It
does not silently drop unsupported seed or temperature settings. Model choice
is explicit: there is no default model or implied subscription entitlement.
Configure `OPENAI_API_KEY` outside Git and chat. The CLI removes that variable
from its child-process environment and keeps its value out of command-line
arguments, model input, request bodies, receipts and stdout.

```bash
python tools/sog_bench_lean_model.py \
  --workspace .astis/my-lean-suite/tasks/sogb-001 \
  --output .astis/my-model-transcript \
  --model YOUR_EXPLICIT_MODEL --max-output-tokens 4096
```

The workspace and transcript must be fresh. For a batch, run the bridge for each
already selected child and then use the existing `suite-close`; unattempted and
failed targets remain selected. Do not change the denominator after seeing a
model answer. Keep the provider transcript together with the workspace evidence.

## Paired pilot: lookup off versus on

The optional lookup arm currently covers only the admitted strict Wasserstein
triangle target `sogb-018`. Generate its canonical corpus before setting up
the two fresh workspaces:

```bash
python tools/sog_bench_lean_statement_lookup.py --output .astis/transport-lookup.json
```

The returned digest pins 12 project-owned declaration signatures from the
existing replayable transport graph. The builder excludes benchmark answer
modules (including the target's own module), copies no proof bodies, docs,
graph edges, textbook text, oracle, rubric or ATLAS material, and requires each
lemma to be available in the task's existing import closure. The signatures
can omit section context; they are not alternate targets or evidence that
a lemma is logically necessary. Reuse retains the project Apache-2.0 notices.

Preselect both arms before starting, using the **same** target packet, stage,
runtime, model version, decoding and compiler-check count. Start two fresh
workspaces with the usual `start` command. Use the baseline provenance above
for lookup off. For lookup on, replace the retrieval/tools fields and add:

```json
{
  "retrieval_profile": "transport-statements-v1",
  "tools": ["lean_workspace", "lookup_lean_statements"],
  "max_searches": 2,
  "retrieval_corpus_sha256": "COPY_CANONICAL_SHA256"
}
```

These are fields of the otherwise unchanged provenance object. Invoke the
normal bridge in both arms, adding `--lookup-corpus .astis/transport-lookup.json`
only for lookup on. The bridge regenerates the exact canonical corpus and
checks its bytes, digest and task binding *before* reserving a run or calling
the provider. A re-signed file containing foreign content is not accepted.
The model can request a short word/name query, never a file or URL. It receives
at most three ranked signatures per call. Exhausting lookup removes that tool;
it does not consume a compiler check or another final attempt.

Archive both trajectories with their workspace receipts, including failures.
Compare the exact task/agent inputs and runtime hashes first. Report lookup
calls, returned declaration IDs, total API turns/usage, Lean check outcomes and
first-final verification **separately**. More tool turns are possible in the
lookup arm by design. Lookup off does not disable Lean's own reasoning or
search tactics. Neither arm establishes unseen performance; this single
public-dev pilot is not a calibration or a general search benchmark.

## Budgets, failures and records

The API call budget is frozen to `max_checks + max_searches + 1`, with 0–8
compiler checks, 0–4 eligible lookup calls and one final. Each HTTP
request/response is bounded to 2 MiB; calls have a
60-second network timeout and no automatic retry. These are technical bounds,
**not a dollar-cost ceiling**. Input tokens, reasoning and an interrupted API
request can still be billed. Obtain an authorized provider/model and spending
policy before starting a paid run. CI/unit fixtures need no API key.

The canonical workspace `external-run.json` reserves this collection before its
first HTTP request. An
ambiguous timeout or interruption cannot be silently retried under a new output
directory on the same workspace. Keep partial records and inspect them manually;
do not delete locks or reservation evidence to improve the result. The bridge
lock excludes another bridge, not a malicious operator: do not issue manual
workspace actions concurrently. The workspace still reserves every final before
verification; an invalid, rejected, limited or interrupted final is immutable.

Normal termination writes actual bounded JSON evidence, copied exactly to the
workspace's `external-evidence.json` and bound into `external-end.json` along
with session/reservation/selection/client-source/cause and event-history hashes.
Both single completion and batch rollup re-read these canonical bytes. They
distinguish provider/verifier/operator infrastructure from genuine model missing
final/protocol/output-budget cases. Every selected target stays represented;
infrastructure is unscored, not silently dropped or counted as a math failure.

A genuine observation-backed native final always retains its exact result,
even if external collection subsequently fails. A native wall-limit result is
still `resource-limit`, not a missing observation. Missing earlier/nonterminal
observation is invalid history and fails closed. Without an end record, read-only
status remains unfinished; only explicit close/suite-close **after client/tool
work has stopped** marks interrupted infrastructure. No lock/reservation implies
process liveness. Partial copies, interrupted writes and old unsupported
`model-session.json` prototypes require inspection, never silent migration or
automatic retry. Canonical evidence is bounded to512KiB and rejected on duplicate
keys, nonfinite JSON, incorrect bindings or drift; this is trusted-operator
recording, not authentication of a malicious operator's claimed provider cause.

The transcript stores exact bounded request/response bodies, selected safe HTTP
receipt fields, provider response/model IDs, usage when returned, tool feedback,
timestamps and file hashes. HTTP/setup errors, malformed/multiple/unknown tool
calls, missing finals and verifier infrastructure failures remain distinguishable.
There is no automatic retry of a provider HTTP error. A trusted API credential
echo is not archived. A successful check alone never becomes an accepted final.

The function call loop uses stateless `store:false`, preserves all response
items (including encrypted reasoning) and supplies each function output with its
actual call ID. See the official [function-calling guide](https://developers.openai.com/api/docs/guides/function-calling)
and [Responses creation reference](https://developers.openai.com/api/reference/resources/responses/methods/create).
No hosted search, code execution or other provider tool is enabled. Lookup is
deterministic local ranking, not a provider-side search or execution service.

The optional native CI `model-bridge-trials` uses a separately labelled
`controlled-software-fixture` client: it exercises actual compiler feedback and
two-target failure accounting but makes **zero** provider calls. Its synthetic
Responses-shaped messages, model/version names and HTTP-shaped fields are not
real provider responses or AI reasoning. Real CLI runs still require declared
OpenAI provider/model/version provenance and an authorized API key.

These are operator-observed records, not cryptographic provider attestation,
malicious-operator protection, calibrated difficulty, a private-family test or a
model ranking. `model_measurement` and `provenance_authenticated` remain false.
Actual API/native evidence and review are separate from the existing native08
software-fixture acceptance. No new question, theorem or Registry credit follows.

## Credential-free JSONL transport

`tools/sog_bench_lean_stdio.py` is a foreground pipe to the same fixed-target
workspace. It does **not** launch an agent or model, read weights, install a
runtime, make network calls, run host Lean or accept commands or filenames.
It requires the prepared Linux Docker/Landrun runtime from [WORKSPACE.md](WORKSPACE.md).
In the workspace provenance, record your actual local model/version,
decoding and seed, set `"tools":["lean_workspace"]`,
`"retrieval_profile":"provided-prompt-template-only"` and
`"transport":"fixed-target-lean-jsonl-v1"`. Use
`controlled-software-fixture` for scripted inputs. For multiple targets,
freeze them all with `suite-start` before feeding any model.

```bash
python tools/sog_bench_lean_stdio.py --workspace .astis/my-lean-suite/tasks/sogb-001 --output .astis/my-jsonl-transcript
```

The first stdout line is the prompt and checked source template. Forward that
line and subsequent bounded feedback only; do not mount the workspace,
operator archive or repository as solver context. Send exactly one UTF-8 JSON
line for each `{"action":"check","source":"complete Lean file"}` or
`{"action":"submit","source":"complete Lean file"}`. Checks are bounded and
never count as finals. The first well-shaped submit is immutable, including a
verifier rejection or an invalid source. A malformed frame stops collection.
No extra command, shell, retrieval or
network tool is offered by this pipe. The operator controls any separate
model process and must not run manual workspace actions concurrently. The
pipe waits for input; set any inference/transport deadline in that operator
process, separately from the verifier's resource limits.

If the agent intentionally ends without a final, send
`{"action":"stop","reason":"model-no-final"}` (or `model-output-budget`).
Bare EOF, an unterminated frame, or a broken transport is infrastructure,
not an observed model stop. A genuine observed native final keeps its exact
outcome even if the feedback pipe closes. The collector reserves before
emitting the prompt, records bounded raw requests and feedback, and uses the
existing external termination and suite accounting. Do not retry an
interrupted collection, delete its reservation, or replace its first final.
Review partial evidence after stopping the pipe. Exit code zero means the
collector completed its protocol, not that Lean accepted the proof.

Unit tests use a mocked verifier and the native CI canary uses a scripted
wrong target, not a model. Neither is a model score. A model's fixed-target
answer is verified only if the real isolated comparator/kernel path produces
that result; generating or archiving candidate text is not verification.

The [public-dev one-shot capture](../../../runs/20261110-bench-local-lean-first/README.md)
is a separate, pinned Qwen answer on a fixed target. Its CI verification
reuses the same isolation but does not replay a live model/tool conversation.
It sends the exact captured text, including any formatting mistakes.

### Agent-selected graph lookup plus Lean

For a separate public-dev condition, set the following fields when starting
the same fixed-target workspace. This example pairs `sogb-046` with
`sogb-g010`. For a declared model run also record the actual provider,
model, version, decoding and seed as above. Use a fresh workspace per
condition; this does not change the target, allowed imports or first-final rule.

```json
{
  "transport": "fixed-target-lean-graph-jsonl-v1",
  "retrieval_profile": "same-family-imported-compiled-slice-v1",
  "tools": ["lean_workspace", "compiled_graph_lookup"],
  "graph_task_id": "sogb-g010",
  "max_graph_lookups": 2
}
```

Use the same JSONL command. The external agent may choose
`{"action":"find","query":"eigenmode"}`, `{"action":"inspect","id":"…"}`,
`check`, `submit` or `stop`; no order is prescribed. Searches only see
selected declarations whose actual owning modules are in the fixed local
import closure. The admitted graph task must be in the same public-dev
family. The answer owner is excluded, along with edges to excluded nodes;
no reference proof, graph answer, full graph, source path or file contents
are returned. The optional graph tool is distinct from general library search.
The operator stage’s local module inventory and sources must match the
current fixed closure; stale stages are rejected before emitting a prompt.

Invalid lookups count toward the declared graph budget. Graph and Lean calls
are separately counted; neither changes the first-final denominator.
Only Lean actions enter the verifier workspace. On the operator side,
`selection.json` binds the reviewed graph, projection, stage, implementation and
budget; `graph-projection.json` plus hashed request/observation files record
exactly what was searched and returned. Share only the prompt/feedback wire
with the agent, not these directories. Edges mean selected compiled-body
occurrences, not necessity or the full dependency closure.

`python tools/sog_bench_lean_stdio.py --audit-graph-output PATH` replays the
archived lookup replies against the selected projection and lookup
implementation. It does not rerun Lean or authenticate an operator.

The `graph-stdio-trial` native CI fixture interleaves real graph responses
with changed-target rejection and acceptance of a trusted first final.
The actions are scripted; the fixture is not evidence of model-selected
tools, proof repair, held-out accuracy or calibration. For a real comparison,
freeze task families and record both prompt-only and graph-assisted conditions,
including every selected target, raw model response and native outcome.

### Opt-in local model with live feedback

For a real credential-free trial, the existing **Bench isolated Lean
runtime trials** workflow has a manual `local_model_pilot` option. Ordinary
PR, push, and unselected manual runs do not download model weights or run
inference. Select the exact branch when dispatching. This optional job is
separate from the required software trials and never deploys Pages.

The pilot uses the same pinned public Qwen2.5-0.5B-Instruct Safetensors as
the one-shot capture, verified against all eight recorded file hashes.
The host provisions the model and CPU packages; inference loads only local
files with remote code disabled. The isolated verifier does not receive
the weights, host credentials, or a shell command from the model. Only the
fixed prompt-only Lean prefix, its first body, and the bounded check
diagnostic are model inputs. The text is appended unedited, even if it
contains Markdown or otherwise fails.

On an already prepared Linux host, the equivalent foreground command is:

```bash
python tools/sog_bench_lean_local.py \
  --task .astis/lean-local-tasks/sogb-015 --stage .astis/lean-local-stage \
  --runtime .astis/lean-local-runtime --model-directory .astis/lean-local-weights \
  --output .astis/lean-local-evidence
```

The operator schedules one check and then one immutable final for one
public-dev target; this measures response to feedback, **not autonomous
tool selection**. The evidence binds both token/message records to the
exact submitted files and the first native diagnostic. A setup or transport
failure retains the selected target but produces no score. Report only
what the actual artifact shows, not a held-out result, a calibration run,
or a claim that a proof was repaired merely because feedback was delivered.
