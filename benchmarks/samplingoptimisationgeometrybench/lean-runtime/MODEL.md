# Optional model-to-compiler bridge — staged, not yet accepted

`tools/sog_bench_lean_model.py` connects one explicitly selected Responses API
model to an existing pristine fixed-target compiler workspace. This is a finite
foreground process, not a website service or background ASTIS session. Its unit
fixtures do not make provider calls, execute Lean, certify native integration,
or establish model performance. Independent review and actual provider/native
acceptance remain required before advertising this as a tested model runner.

## What reaches the model

Only the canonical `agent/prompt.json`, `agent/Solution.lean.txt`, fixed tool
instructions and bounded feedback. Their hashes are checked against the frozen
operator packet. The bridge does not expose the operator directory, reference
proof, source oracle, challenge, runtime configuration, general shell, filesystem
or retrieval tool. The original public-dev answers are already public and may
be in model training; restricted ATLAS content must never enter this interface.
This is not a held-out test or proof of closed-book knowledge.

The sole function is `lean_workspace({action, source})`, where action is `check`
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
snapshot/version; the bridge records the provider's returned model ID separately:

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

## Budgets, failures and records

The API call budget is frozen to `max_checks + 1`, with0–8 existing compiler
checks and one final. Each HTTP request/response is bounded to2MiB; calls have a
60-second network timeout and no automatic retry. These are technical bounds,
**not a dollar-cost ceiling**. Input tokens, reasoning and an interrupted API
request can still be billed. Obtain an authorized provider/model and spending
policy before starting a paid run. CI/unit fixtures need no API key.

`model-session.json` reserves this model run before its first HTTP request. An
ambiguous timeout or interruption cannot be silently retried under a new output
directory on the same workspace. Keep partial records and inspect them manually;
do not delete locks or reservation evidence to improve the result. The bridge
lock excludes another bridge, not a malicious operator: do not issue manual
workspace actions concurrently. The workspace still reserves every final before
verification; an invalid, rejected, limited or interrupted final is immutable.

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
No hosted search, code execution or other provider tool is enabled.

These are operator-observed records, not cryptographic provider attestation,
malicious-operator protection, calibrated difficulty, a private-family test or a
model ranking. `model_measurement` and `provenance_authenticated` remain false.
Actual API/native evidence and review are separate from the existing native08
software-fixture acceptance. No new question, theorem or Registry credit follows.
