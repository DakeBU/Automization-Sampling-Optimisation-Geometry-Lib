# Compiler interaction: one fixed target

For operators of the experimental Linux runtime. This is a finite local CLI,
not a website execution service, general shell agent or measured leaderboard.
The native replays must pass before claiming tool acceptance; independent runtime
review and authenticated model runs remain separate.

## Agent contract

Give the agent only the selected `agent/` prompt/template and returned feedback.
Do not give it the workspace's operator directory, trusted stage, runtime tools,
challenge, oracle, reference/training export or operator credentials. Running an
agent with unrestricted access to the operator checkout does **not** implement
this separation. Public-dev gold already exists publicly; this is not a held-out
test or an assertion of enforced closed-book retrieval.

The only supported tool request is JSON:

```json
{"action":"check","source":"<complete UTF-8 Solution.lean text>"}
```

The final response uses `"action":"submit"` with the same text field. The agent
cannot select commands, paths, mounts, targets, axioms or verifier configuration.
Requests are bounded before parsing; duplicate JSON keys and unknown fields are
rejected. Lean text is data until the isolated verifier receives it. Never run
the text with host `lean`, `lake`, a shell or `#eval` for a quick syntax check.

- Up to the operator's predeclared0–8 `check` calls; default4. Every valid-shaped
  check request consumes a call, including an invalid source or runtime failure.
- One `submit` after those checks. It is reserved **before** execution. A rejected,
  timed-out, invalid or interrupted final cannot be replaced by a better final.
- A successful check is not a final answer. Closing without a final retains the
  selected target with `no-final-submission`, even if an earlier check succeeded.
- Each execution uses a fresh container and the unchanged runtime policy. The
  returned diagnostic is at most8KiB; the bounded full diagnostic and exact source
  stay in the operator evidence. Compiler feedback is untrusted text, not a new
  instruction for the agent or a verdict inferred from stdout.

## Operator setup

Use the pinned Lean4.33.0, manifest packages, trusted built ancestors, Go1.27.3
and Linux x86_64 Docker/Landlock ABI>=6 environment from the native CI workflow.
No Windows/host fallback is provided. Preparation downloads/builds trusted tools;
verification itself has no network. Use fresh paths for all commands.

```bash
python tools/sog_bench.py check-lean
python tools/sog_bench_lean_native.py prepare --output .astis/my-lean-runtime
python tools/sog_bench_lean.py export --task-id sogb-001 --output .astis/my-lean-tasks
python tools/sog_bench_lean.py stage --task .astis/my-lean-tasks/sogb-001 --output .astis/my-lean-stage
```

Create an operator-owned `provenance.json`. For a **scripted software fixture**:

```json
{"kind":"controlled-software-fixture","name":"my-tool-replay"}
```

For externally collected model work use `kind: "declared-model-run"` and record
`provider`, actual `model`/`model_version`, `retrieval_profile`, `tools`, `decoding`
and integer-or-null `seed`. This records the operator's declaration only. It does
not authenticate provider responses, enforce retrieval conditions, make private
families, calibrate difficulty or authorize a model-performance claim.

```bash
python tools/sog_bench_lean_workspace.py start --task .astis/my-lean-tasks/sogb-001 --stage .astis/my-lean-stage --runtime .astis/my-lean-runtime --output .astis/my-lean-workspace --provenance provenance.json --max-checks 4
python tools/sog_bench_lean_workspace.py act --workspace .astis/my-lean-workspace --request request.json
python tools/sog_bench_lean_workspace.py close --workspace .astis/my-lean-workspace
```

The operator passes the chosen request file; the JSON itself contains source, not
a filename to read. Repeat `act` only within the declared check budget, then make
one final submission. A bounded protocol/OS/setup error is not mathematical
rejection; retain it and inspect the evidence rather than deleting/retrying a
bad-looking run. The CLI's successful JSON delivery is not proof acceptance:
read its `kind`/`final` fields and the sealed completion, not process exit0 alone.

## Evidence and remaining boundary

`session.json` freezes task/binding, first-final policy, check budget, selected
target denominator1, source/runtime receipt hashes, selection timestamp and
declared provenance. Each sequential action preserves the submitted bounded
source, event, native result, diagnostic and observation hashes. Exclusive
operator locking prevents concurrent calls reserving two finals; crash recovery
is inspection-only, not an automatic replay. Source/result drift fails closed.

`completion.json` records all checks, final presence/outcome and interruptions.
Infrastructure errors stay unscored and distinct from mathematical failures;
missing/invalid finals remain selected. These files are operator records, not
cryptographic attestation against a malicious operator. `model_measurement` and
`provenance_authenticated` remain false. Authenticated raw provider/tool
trajectories and the declared tool/retrieval policy are still required before
reporting actual model performance. The batch recorder below supplies selected-
task accounting, not that authenticated model connection.

## Batch selection: never count only surviving answers

For a batch, use `suite-start` **before any model/tool work**, instead of starting
only the tasks for which answers happened to return. The task/stage directories
come from the same canonical export and trusted staging commands above.

```bash
python tools/sog_bench_lean_workspace.py suite-start --tasks .astis/my-lean-tasks --stages .astis/my-lean-stages --runtime .astis/my-lean-runtime --task-id sogb-001 --task-id sogb-002 --output .astis/my-lean-suite --provenance provenance.json --max-checks 4
python tools/sog_bench_lean_workspace.py act --workspace .astis/my-lean-suite/tasks/sogb-001 --request request.json
python tools/sog_bench_lean_workspace.py suite-close --suite .astis/my-lean-suite
```

Export and stage **both** selected targets first; the single-target setup example
above is not already a two-task stage tree. Every selection must currently have
an admitted aligned Lean task. `suite.json` freezes exact core/family/public-dev
identity and bindings before initializing children. A failed initialization stays
selected as `initialization-error`, not deletion. Closing retains all selected
targets, including unattempted ones, with separate accepted/rejected/invalid/no-
final/infrastructure outcomes. Partial initialization is not automatic permission
to restart or silently replace the selection.

`suite-status` is read-only; a live, unclosed task is `unfinished`, not an inferred
failure. `suite-close` is for the operator after tool calls stop. It closes the
existing children once and seals `accounting.json`; later evidence/denominator
drift fails. Exclusive locks are operational exclusion, not proof a process is
still live. No aggregate success rate, calibrated difficulty or model leaderboard
is inferred from these records. Authenticated raw provider/prompt/tool recording
and the declared retrieval policy remain required for a measured evaluation.

CI `workspace-trials` replays an intentionally wrong target, returns actual native
feedback, submits the unchanged reference, and checks that a second final is
blocked. Separate cases retain a successful check without final and an invalid
final. Its preselected two-task suite retains an unattempted second target in the
denominator. These scripted fixtures test the tool/recorder, not an AI's reasoning.
Keep the independent mathematical admission and all existing graph/source readers
unchanged; reference acceptance is not new theorem or Registry credit.

## Optional external collector lifecycle

The staged [model bridge](MODEL.md) uses operator-only `reserve_external_run`
and `finish_external_run`; these are not new model-facing commands. They bind a
pristine selected session and a real bounded canonical termination-evidence copy.
The shared completion/rollup derivation keeps provider/runtime infrastructure
unscored and distinct from actual model missing finals, while never changing a
genuine reserved final's result. No lifecycle or hash is provider attestation.

Read-only unclosed status stays `unfinished`, including an unended collection;
only explicit `close`/`suite-close` after client/tool work stops classifies that
interruption. Missing nonterminal observation and later evidence drift fail
closed. Existing unmanaged archive behavior remains unchanged; unsupported old
prototype markers are not automatically migrated. See the exact staged contract
and required new native/code review in MODEL.md before using a collector.
