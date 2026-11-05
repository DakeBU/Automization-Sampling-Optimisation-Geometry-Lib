# Fixed-target Lean runtime — under native acceptance

This is work on issue378, continuing the same Bench Goal after the hierarchical
reader shipped in PR377 at main692973fc. It is **not yet an accepted Agentic Lean
benchmark**, a model result or a security certificate. Existing website readiness
labels remain pending. No QA/level/family/source binding or production theorem is
changed, and no new Registry leaf is claimed.

## Trust boundary

Use three separate views of each currently editorially admitted aligned task:

1. `agent/`: the canonical prompt plus its named fixed-target template. No gold.
2. `verifier/`: an operator-controlled challenge, configuration and exact hashes.
3. `oracle/`: the existing reviewed reference, only for controlled software trials.

The trusted challenge deliberately contains a proof hole **only to state the
target**, following comparator's interface. It is generated outside production
Lean and is never scored as a proof or published blue. Solutions depending on
that hole (`sorryAx`), including simply importing Challenge, must fail the axiom
audit. The verifier container never receives the oracle directory. Definition
holes are disabled. The semantic target is the original task, merely assigned a
stable theorem name; no mathematical binder or definition changes.

Compilation and stdout are insufficient for adversarial submissions. Reuse
[Lean's validation guidance](https://lean-lang.org/doc/reference/4.33.0/ValidatingProofs/)
and the official [comparator](https://github.com/leanprover/comparator/tree/3927ad383f208ae977c340a91c48ac9b497d2097):
its serialized challenge/solution comparison checks relevant definitions/types,
then the permitted-axiom audit and fresh Lean-kernel replay. The pinned release
matches Lean4.33.0 and its pinned lean4export; do not silently migrate the project
to the newer built-in commands. No additional external kernel is enabled yet.
Comparator is Apache-2.0, copyright Lean FRO, LLC; it is built as an external tool,
not copied into our mathematical library. Landrun remains the real upstream
sandbox, never its fake development shim. Exact pins are in policy.json.

## Initial runtime contract

Linux x86_64 Docker only. No host fallback. Each verification call gets a fresh
nonroot, capability-free, no-new-privileges, network-none container with readonly
trusted mounts and bounded scratch, RAM, CPUs, PIDs, wall time and output.
Preflight requires cgroup-v2 observations, readonly root and Landlock ABI>=6.
Real Landrun additionally separates compiler/export subprocesses from the trusted
comparison process. Old-kernel degradation below the required ABI is rejected.
There is no host home, Docker socket, repository `.git`, credential or writable
checkout mount. The initial image uses a pinned Ubuntu base; resolved apt packages
and image identity remain build-environment inputs, not a bit-reproducible image
claim. The task's own target module is excluded from its ASTIS ancestor snapshot.

`tools/sog_bench_lean.py export` prepares operator packets. `stage` snapshots one
task's allowed owned ancestors. `run` verifies one bounded regular-file submission
inside the prepared runtime and archives diagnostics and container state. Every
call uses a fresh evidence directory. Compiler diagnostics support proof repair;
those calls do not by themselves record a provider/model trajectory or determine
the first final-answer denominator. Infrastructure errors remain distinguishable
from proof rejection/resource limits and must not become measured model scores.
The CLI exits0 for acceptance,10 for proof rejection,20 for infrastructure errors
and30 for a declared resource limit. These are verification-call outcomes, not
model scores. A separately framed trusted-challenge preflight precedes solution
verification; setup failures and setup-time limits are not mathematical rejection.
Child output is escaped diagnostic data, never a control record. Each result pins
the exact task packet and prepared-runtime receipt; changed tools/source fail closed.

Readonly public caches must also be readable by the container UID. Preparation
checks the pinned package checkouts and copies only manifest-listed packages.
Readable artifacts are hard-linked; private-mode public artifacts are copied and
made readable **without chmod on shared original inodes**. Snapshot directories
are newly created. The readonly mounts/capability/network policy is unchanged.

## Acceptance and remaining work

The dedicated `Bench isolated Lean runtime trials` CI workflow builds the pinned
tools and tests all currently admitted aligned reference targets plus explicit
negative fixtures. Read actual `software-trials.json`, not export success, for
native evidence. Preserve the first failed run and diagnose before retrying.
Local Windows tests only exercise packaging/contracts; they never execute hostile
Lean. The host intentionally lacks a usable Docker/WSL runtime.

Still required: actual native acceptance, hostile filesystem/network/resource
fixtures and independent runtime review; a tested agent-facing compiler workspace
or native harness adapter with recorded trajectories; real declared model runs;
calibration/private families; broader seven-domain/textbook-exercise coverage.
The old archived comparator pin also requires explicit future security maintenance,
not an implicit guarantee against all OS/kernel/compiler exploits. Keep complete
mathematical proof/source/graph readers and all older frontiers unchanged.
