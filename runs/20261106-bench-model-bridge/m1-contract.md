# M1 candidate contract: canonical external-run termination

Proposal before implementation. This is recording infrastructure in the same
Bench Goal, not a theorem, score or native/provider acceptance. It repairs M1 of
the preserved independent v1 review; M2's existing narrow repair remains intact.
Root is sole writer. No accepted main archive/session is rewritten.

## Interface and authority

The workspace gains two operator-only Python operations:

1. `reserve_external_run(directory, metadata)`: only an open pristine selected
   workspace, under its existing exclusive operation lock. Metadata has exactly
   bounded `client`, 64-hex `client_source_sha256_lf` and 64-hex
   `selection_sha256`. Persist one `external-run.json` before the first provider
   call, binding the session SHA256. Existing reservation is never overwritten.
2. `finish_external_run(directory, disposition, reason, evidence_sha256)`: require
   a valid reservation and an unclosed workspace; persist one `external-end.json`
   under the same lock. Bind reservation/session hashes, canonical event-history
   digest/count, typed disposition/reason and a 64-hex digest of actual client
   termination evidence. Never overwrite it. No new model-facing action is added.

These are trusted-operator evidence, not malicious-operator attestation. No key,
path to execute, shell command or verifier override belongs in this interface.
The proof acceptance algorithm, allowed axioms and sandbox policy are unchanged.

`completed` reasons are `final-submitted`, `model-no-final`,
`model-protocol-error`, `model-output-budget`. `infrastructure-error` reasons
are `provider-transport`, `provider-http`, `provider-identity`,
`provider-protocol`, `verifier-infrastructure`, `operator-infrastructure` and
`client-interrupted`. Unknown combinations/hashes fail closed. A `final-submitted`
reason requires an actual reserved final; ordinary no-final reasons require no
final. Infrastructure evidence may accompany a real final but never replace it.

## Canonical completion and batch accounting

Use one shared outcome derivation in `close` and `suite_status`:

- A genuine reserved final, if its result exists, retains exactly that result.
  External failure cannot turn a rejected/invalid final into an infrastructure
  exclusion, replace an accepted final, or permit another final.
- Any actually interrupted verifier action remains `infrastructure-error`.
- Without a final, a valid external end of `infrastructure-error` is a distinct
  unscored `infrastructure-error`, not `no-final-submission`.
- Without a final, a `completed` external end yields `no-final-submission`.
- A reservation with no end is *not* a live-process assertion or a terminal
  outcome in read-only status. An unclosed child remains `unfinished`. Only an
  explicit `close`/`suite-close`, after the operator stops client/tool work,
  classifies that unended collection as interrupted infrastructure.
- Existing unmanaged sessions keep their original behavior. Old closed archives
  remain immutable. A legacy prototype `model-session.json` without the new
  lifecycle is unsupported and requires inspection, not silent reinterpretation.

Completion binds any external reservation/end hashes. Recompute and compare
them during suite accounting along with the real event history. Later drift,
or an external end without its reservation, fails closed. No actions after an
external end. All selected tasks remain in the suite; missing/invalid/unattempted
and infrastructure cases remain separate, with no aggregate model score added.

## Bridge integration and crash handling

Replace the prototype's model-only reservation with the generic workspace
lifecycle. Freeze a fresh selected workspace and prompt-side hashes before any
HTTP call. Keep0–8 checks, one immutable final, zero automatic API retries and
the existing request/response bounds. Missing API authorization is no invitation
to run a model or submitted Lean on this Windows host.

Provider HTTP/transport/identity integrity errors and returned check-verifier
infrastructure errors end the external run with an infrastructure disposition.
A completed genuine model response with malformed/unknown/missing tool calls is
a model protocol/no-final result, not a free infrastructure exclusion. An API
incomplete response caused by the declared `max_output_tokens` is a model-output
budget stop; failed/cancelled/other incomplete provider responses remain separate
provider failures. Preserve raw response, ID/model/usage and typed evidence.

Write client termination evidence before `finish_external_run`. Soft interruption
may write `client-interrupted` evidence and close; hard interruption can retain a
reservation/partial files without an end. No automatic retry or stale-lock
deletion; manual `suite-close` after stopped work uses the rule above. A write or
history-drift failure must retain incomplete evidence rather than fabricate a
successful seal. Keep model_measurement/provenance_authenticated false.

## Required evidence before admission

Unit tests must cover provider HTTP/transport failure, failed check infrastructure,
identity failure, ordinary missing final, model protocol/output-budget stops,
unended collection before/after explicit close, all genuine final outcomes,
interrupted verifier final, duplicate operations, hash/history drift and actual
suite rollups including an unattempted second selected target. Preserve existing
software-only semantics and old prototype/review hashes.

Then independent exact-code review and a new Linux native fixture must exercise
this bridge/workspace boundary with no provider credentials. Real provider/native
acceptance, model measurement, private families/calibration, seven-domain depth
and numbered textbook exercise coverage remain separate required Goal work.
