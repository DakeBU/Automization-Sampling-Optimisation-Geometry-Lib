# M1 exact successor contract (v2)

Retain m1-contract.md and its changes-requested preflight unchanged. This v2
replaces only the ambiguities identified there; all other scope/invariants and
required tests in that candidate still apply. This is not an implementation or
an admission verdict. It does not change mathematical QA or the proof verifier.

## C1: actual canonical evidence bytes

`finish_external_run(directory, *, disposition, reason, evidence: Path)` accepts
an operator-selected **actual file**, not an asserted digest. Read it once with
the existing bounded regular-file reader, at most512KiB, strict UTF-8 JSON,
duplicate-key rejection and no NaN/Infinity. Require exactly these fields:

```text
schema_version: integer1 (not Boolean)
kind: external-client-termination-evidence
session_sha256: exact current session bytes
reservation_sha256: exact external-run.json bytes
selection_sha256: exact reservation metadata value
client_source_sha256_lf: exact reservation metadata value
disposition: completed | infrastructure-error, equal to the operation argument
reason: allowed reason for that disposition, equal to the operation argument
client_stop: nonempty bounded string (at most256 characters)
facts: JSON object (within the same whole-file byte bound)
```

The client writes this termination-evidence file **before** calling finish. The
workspace validates its bindings and copies those exact bytes once to the fixed
canonical `external-evidence.json`, then writes `external-end.json` binding the
real copy's digest plus reservation/session and canonical history digest/count.
Never overwrite either file. A partial copy with no end is an unended run;
read-only status stays unfinished, explicit close after stopped work gives
interrupted infrastructure. Failure/drift must not produce a fabricated end.

Both close and suite accounting re-read the bounded canonical evidence, rehash
its actual bytes, and validate its exact fields/bindings against the end,
reservation, session and current event history. Missing/changed evidence or
unknown field/cause combinations fail closed. A digest naming absent evidence
is not enough. Copied facts remain trusted-operator observations, not proof of
provider behavior or malicious-operator attestation. Client raw request/response
files remain separately bound/auditable in their complete transcript; this
generic workspace does not authenticate those external provider bytes.

## Final-result definition and order

A final result exists only when `history()` returns that final's non-None result:
the persisted observation and result kind/hash pair were validated. Merely
finding result.json is not this condition. A missing observation is interrupted;
malformed/hash-drifted evidence fails closed.

An absent observation on an earlier/nonterminal action is invalid history and
fails closed; it cannot reclassify a later valid final as infrastructure. With
valid history, a final's observation-backed result takes precedence and retains
its exact native kind, including resource-limit and infrastructure results.
A missing observation on the final itself is interrupted infrastructure; a
native interruption field in a valid wall-limit result is not a missing
observation. External failure cannot change accepted/rejected/invalid/
limited finals, exclude them or allow replacement. End reason `final-submitted`
requires an actual reserved final; normal no-final reasons require none.
Infrastructure evidence can accompany a final but cannot override its result.

Without a final: interrupted verifier action, unended external collection at
explicit close, or ended external infrastructure => infrastructure-error.
Otherwise => no-final-submission. Live/unclosed read-only children remain
unfinished, with no liveness inference from reservation/locks. Managed completion
binds all three canonical external file digests (end/evidence may be null only
for interrupted unended collection). Existing unmanaged archives keep their
old fields/behavior and are not re-signed or silently migrated.

## Provider/model classification order

Before trusting any output-budget classification, validate HTTP200, strict JSON
object, meaningful response ID/model, exact predeclared model_version and fresh
response ID. Keep the existing exact M2 identity policy. Then inspect status:

- Only identity-valid `incomplete` with exact
  `incomplete_details.reason=max_output_tokens` is completed/model-output-budget.
- failed/cancelled/other incomplete/unknown statuses or malformed provider
  envelope => infrastructure/provider-protocol.
- For completed responses require an output array of objects. Invalid server
  structure or unrequested hosted-tool output => infrastructure/provider-protocol.
- A well-formed completed response with no/multiple/unknown function calls,
  malformed function arguments, unknown fields or a check beyond its budget =>
  completed/model-protocol-error. Missing function-call identity or replayed
  call ID is provider-identity. No extra provider call repairs such a stop.
- Valid final source still goes through existing workspace.act; oversize/invalid
  final input remains a genuine reserved invalid final, never an exclusion.
- Provider transport/HTTP/identity failure, check-verifier infrastructure and
  operator/runtime exceptions use their respective infrastructure reasons.

Persist bounded raw response and available ID/model/usage before dispatch, keep
source text as data, add no API retry/model-facing tool/host execution, and do not
infer a model score from any controlled interface/native fixture.

## Tests/admission

In addition to the original matrix, test absent/swapped/mutated canonical evidence,
Boolean schema/counts, wrong session/reservation/selection/client-source/cause,
partial-copy/no-end handling, every native final kind (including observed wall
limit versus missing observation), provider status/identity order, and two-child
suite rollups with the second child unattempted. Contract preflight is not code
review; exact-code review plus a new credential-free Linux native bridge fixture
are still required. Authorized real API/native acceptance remains separate.
