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
All ten proxy environment variables are explicitly blanked, with a value-free
preflight observation. Docker can otherwise inject configured proxy URLs (which
can contain credentials) into containers; network-none alone does not hide these
strings. See [Docker's own proxy warning](https://docs.docker.com/engine/cli/proxy/).
The operator must provide public-only, trusted dependency/build caches; this is
not a sanitizer for arbitrary private files in a locally modified package tree.

`tools/sog_bench_lean.py export` prepares operator packets. `stage` snapshots one
task's allowed owned ancestors. `run` verifies one bounded regular-file submission
inside the prepared runtime and archives diagnostics and container state. Every
call uses a fresh evidence directory. Compiler diagnostics support proof repair;
those calls do not by themselves record a provider/model trajectory or determine
the first final-answer denominator. Infrastructure errors remain distinguishable
from proof rejection/resource limits and must not become measured model scores.
The CLI exits0 for acceptance,10 for proof rejection,20 for infrastructure errors,
30 for a declared resource limit and40 for invalid bounded submission input. A
missing/oversized/nonregular/non-UTF8 input gets its own result without starting a
container; bytes intentionally not read do not receive a fabricated full hash.
These are verification-call outcomes, not
model scores. A separately framed trusted-challenge preflight precedes solution
verification; setup failures and setup-time limits are not mathematical rejection.
Child output is escaped diagnostic data, never a control record. Each result pins
the exact task packet and prepared-runtime receipt; changed tools/source fail closed.
The complete seven-file tool inventory is checked, and verification/preparation
source hashes are recorded separately. Policy schema3 distinguishes the unchanged
256KiB aggregate supervisor-captured diagnostic cap from the 2MiB framed
transport cap. This is NOT a256KiB bound on all internally generated output:
Lean #eval, Lake and proof-export serialization can buffer internally and instead
share the4GiB cgroup memory and180-second whole-call limits. Base64 diagnostic
frames are data, never verdicts; bounded compiler output survives a later timeout.

### Streaming rejection pass, not an alternative acceptance check

Pinned Lake4.33 builds a module through rawProc/IO.Process.output, buffering the
compiler's output until exit. Native06 proved that even the child's OS stdout
therefore does not expose a pre-timeout marker through lake build. It also means
an outer diagnostic reader cannot observe a flood while Lake is accumulating it.

The candidate schema3 driver first runs the actual fixed Solution.lean through
`lake env` and real Landrun directly, with inherited stdout and **no output
artifact or writable project/cache path**. Only the child's own /dev I/O is
writable. This supports self-contained proof elaboration under the pinned imports,
not proof scripts that need filesystem mutation. It shares the SAME180-second
whole-call wall budget and256KiB aggregate diagnostic cap with later verification.
The extra pass may reject or hit a resource limit; it can NEVER accept. It does
not force later phase-dependent comparator builds/exports to stream. Native
acceptance must also see a fixture skip flooding in the readonly pass and then
flood8MiB in the later writable-cache build, with both phase markers and the
comparator's diagnostic_limit evidence (not a precheck-only pass). A fresh
successful precheck still requires the unchanged pinned official comparator's
challenge/solution definition and type comparison, axiom audit and kernel replay.
No patched Lean, comparator, extra permitted axiom or new mathematical task.

The precheck precedes comparator's challenge export, so making .lake writable
there would let submitted code corrupt the trusted baseline. The readonly policy
is deliberate. Native acceptance now also requires an actual denied write to
Challenge.olean with a specific precheck exception marker and proof that comparator
was not run. This is tested independently of the accepted real I/O-denial probes.
The wall/output markers remain mandatory, not waived. Until new native evidence
passes, this remains a proposed fix, not verified output-cap/Agentic Lean readiness.

Before any submitted source, a trusted `--version` probe exercises the SAME
lake-env/Landrun/Lean launcher. Its failure or version mismatch remains in
challenge-preflight as unscored infrastructure, not a proof rejection. A native
operator fault-injection case intentionally replaces Landrun only in a separate
fault receipt; it must fail this readiness probe before source verification.
That fixture is not an admitted pinned runtime. Subsequent nonzero source
elaboration is rejected only after trusted readiness; timeouts/OOM still retain
their actual phase. The probe is not cryptographic proof that source execution
began or a guarantee against all transient failures.

Readonly public caches must also be readable by the container UID. Preparation
checks the pinned package checkouts and copies only manifest-listed packages.
Readable artifacts are hard-linked; private-mode public artifacts are copied and
made readable **without chmod on shared original inodes**. Snapshot directories
are newly created. The readonly mounts/capability/network policy is unchanged.
Owned ancestor snapshots also carry their C/IR build artifacts, not only oleans.
Lean4.33 requires these for a complete cached build. Source/artifact timestamps
are preserved so checking a task does not unnecessarily recompile its trusted
parents. These are the same pinned module outputs, not new mathematical leaves.

## Acceptance and remaining work

The dedicated `Bench isolated Lean runtime trials` CI workflow builds the pinned
tools and tests all currently admitted aligned reference targets plus explicit
negative fixtures. Read actual `software-trials.json`, not export success, for
native evidence. Preserve the first failed run and diagnose before retrying.
Local Windows tests only exercise packaging/contracts; they never execute hostile
Lean. The host intentionally lacks a usable Docker/WSL runtime.

The first complete native pass is head72d5322d, run42010581633: all13 aligned
reference targets and all5 semantic/axiom negatives passed. Raw results, including
the earlier failures, are retained under runs/20261105-bench-lean-runtime. This is
software acceptance of that scope, not a measured model or complete harness.

The next native gate additionally requires actual denied trusted-file writes,
external TCP-connect attempts, wall/output-limit probes and invalid-input cases.
A parser error cannot pass an I/O probe: its markers and the original reference
proof must both succeed. Negative-proof fixtures must show the expected semantic
or illegal-axiom reason, not just any failure.

Native05/head ebfe3c14 repeated all13+5 successes and passed real write/TCP
probes. Its wall kill worked but the marker was buffered by Lean #eval, so the
hostile gate **failed**. The raw failure is retained; output and invalid-input
native cases were unrun. The next probe uses its own OS stdout, not #eval's
buffer, with the same limits and additional supervisor-fd protection testing.
Do not mistake this diagnosis/local patch for fresh native acceptance.

Native06/head8a852fac also failed: all13+5 and real I/O denial pass, including
supervisor-fd denial, but wall180.489s kills with exit137/non-OOM and no marker.
Raw92-file evidence and exact archive binding are retained in native-06. Flood,
invalid-file and workspace replays were unrun. The next candidate uses the real
readonly streaming pass above, rather than another stdout variant. Limits and
mandatory marker checks are unchanged; additional local tests are not native
isolation evidence.

The finite [compiler workspace](WORKSPACE.md) exposes only bounded JSON `check`
and one immutable `submit`, preserving diagnostics and first-final accounting.
Its dedicated native replays are controlled software, not model results. A
successful check without final does not pass the selected task.

Still required: successful hostile filesystem/network/resource fixtures and
independent runtime review; accepted native compiler-workspace replays and real
authenticated provider/tool trajectories; real declared model runs;
calibration/private families; broader seven-domain/textbook-exercise coverage.
The old archived comparator pin also requires explicit future security maintenance,
not an implicit guarantee against all OS/kernel/compiler exploits. Keep complete
mathematical proof/source/graph readers and all older frontiers unchanged.
