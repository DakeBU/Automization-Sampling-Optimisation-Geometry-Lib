# Native Harbor graph adapter

This optional adapter turns the existing independently admitted **graph-json**
tasks into native Harbor tasks. It is not a Lean submission executor, prose
judge, hidden test split, measured model result or security certification.
Runtime acceptance is per commit in the
[dedicated Linux CI](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/workflows/sog-bench-harbor.yml),
separate from export, local tests, editorial admission and trusted Lean builds.

## Export and run

Use Python 3.11+ for export. The native runner requires Python 3.12+ and a Linux
Docker host with cgroup-v2 CPU/memory limits. Windows users can export tasks
locally, then run them on such a Linux host; this does not install Docker or WSL.

```bash
python tools/sog_bench_harbor.py export --output .astis/harbor/tasks
uv tool install harbor==0.25.0
harbor run --path .astis/harbor/tasks --agent oracle --n-concurrent 2 --n-attempts 1 --max-retries 0 --job-name graph-oracle --jobs-dir .astis/harbor/jobs
harbor run --path .astis/harbor/tasks --agent nop --n-concurrent 2 --n-attempts 1 --max-retries 0 --job-name graph-nop --jobs-dir .astis/harbor/jobs
```

The destination must not exist; use a fresh name for a later snapshot. Repeat
`--task-id sogb-g001` etc. to preselect a subset at export, not after results are
known. Existing identity, family, public-dev split, question binding, snapshot,
provisional difficulty and canonical grading remain unchanged.

`oracle` copies the published reference answer; `nop` leaves the answer file empty. These
are positive/negative **software fixtures**, never scores for a language model.
The CI checks every selected trial, including zero rewards and exceptions. It
does not discard failures or retry until a passing score appears.

## What enters each environment?

```text
environment/   prompt.json + Dockerfile + limit probe (no reference answers)
solution/      reference answer + oracle-only script (not model input)
tests/         frozen question/answer + unchanged canonical scorer + verifier
```

The base Python image is pinned by OCI digest; Harbor is pinned to 0.25.0 and
its wheel hash. The export manifest hashes all task files. CI retains Docker
version, the resolved Python dependencies and native job/trial logs. Transitive
dependencies are recorded, not yet a fully hash-locked installation environment.
The producer Lean 4.33.0 toolchain and Mathlib manifest hash are also recorded;
they identify the graph's library substrate, not a Lean runtime in the agent image.
The full export contains answers: do not provide its root directory to an agent
as closed-book context. Harbor receives the task and stages only its appropriate
components; reviewers can inspect the full package.

The agent runs as the unprivileged `bench` user. Both agent and fresh verifier
use the task's Docker compose definition: `network_mode: none`, one CPU, 256 MiB
memory, 128 processes and no-new-privileges. The runtime probe checks actual UID,
the loopback-only interface list and cgroup CPU/memory/PID limits. Incompatible
hosts fail the fixture rather than earn correctness credit. This is not a proof
of container escape resistance; storage limits and arbitrary Lean sandboxing
are not certified here.

**Why does task.toml say network_mode="public"?** This means no additional Harbor
egress controller. Networking is removed by Docker compose itself. In pinned
Harbor 0.25, the framework's `no-network` instead enables a transparent-proxy
sidecar: its `network-policy` script retains DNS and ICMP and denies controlled
TCP. That is not a hard-offline container. Using the native compose definition
avoids silently substituting that weaker policy for the Bench's offline contract.
The actual runtime probe must pass; a configuration label alone is insufficient.

The verifier starts in a **fresh separate environment**, receiving the declared
`/handoff/answer.bin` and `/handoff/collection.json` artifacts. The oracle writes an undeclared marker;
verification rejects inherited marker state, testing the isolation boundary.
The agent image has neither tests nor gold. Grading imports the byte-identical
owned `sog_bench_curriculum.py`, not a parallel implementation of the score.

An empty answer file is pre-created so the nop fixture exercises rejection,
not a missing-artifact transfer failure. Missing/failed native trials remain
visible and cannot pass the complete-run check.

The output is parsed only as bounded UTF-8 JSON. Oversized/special/symlink files,
duplicate keys, non-finite values, stale bindings, invalid schemas and missing
answers fail. No `eval`, submitted Python, shell or Lean is run by the verifier.
The reward is exactly the canonical structural-set-and-truth-boundary point;
imports/constant occurrences never certify mathematical necessity.

## Version 2: bound the declared answer before transfer

The agent still writes `/output/answer.json`; the question, valid answer schema,
identity, family, split and canonical score do not change. Native task package
version 2 changes the transfer protocol, not the mathematical benchmark item.

A trusted `[[verifier.collect]]` hook runs as root **before** Harbor downloads
declared artifacts. Its code is root-owned in the image, and `/handoff` is
root-owned mode 0700: the unprivileged agent cannot write a collection receipt.
The hook uses one bounded regular-file reader, also reused by verification:
no-follow/nonblocking open, regular-file check, size cap, and pre/post file-state
comparison. It stages at most **65536 raw bytes + 1024 receipt bytes**. Valid small
answers retain their exact bytes and SHA-256. Oversized, symlink, special, missing
or changed files produce an empty raw artifact and a typed rejection receipt.
Only the staged files are declared, so the original unbounded answer path is not
downloaded as a declared artifact.

The verifier requires the receipt's exact policy/schema, byte count and raw hash.
A valid rejection earns zero; malformed answer JSON earns zero. A missing,
inconsistent or corrupt receipt is an **unscored infrastructure failure**, never
a correctness score. This matters because pinned Harbor treats collect-hook
failure as best-effort and may continue the trial. A failed hook must not fall
back to the old raw-answer path. These receipts are local collection records,
not authenticated model/provider attestations or cryptographic signatures.

The dedicated CI additionally exercises controlled oversize, symlink, FIFO,
missing-answer and failed-hook fixtures. These are not new benchmark questions,
private families, measured models or calibration evidence.

**Remaining safety boundary:** this cap covers only the declared answer channel.
Harbor also handles automatic `/logs/artifacts`, agent/verifier logs and other
filesystem usage; their storage/transfer limits are not certified by this change.
Do not interpret a bounded parser or receipt as protection for every host path.
Whole-storage/log hardening and independent security review remain necessary
before hostile-agent or arbitrary Lean-submission evaluation.

## Actual models and remaining work

Bring your own authorized provider and compatible Harbor agent for a measured
run. Do not read credentials into the dataset or archive them in logs. The CI
uses no provider keys and makes no model calls. Compatibility of paid agents'
setup under the no-network/unprivileged policy must be tested separately; the
oracle/nop test does not certify all pre-integrated agents. Record model/version,
tools, first-attempt policy, exact task bindings, trajectories and provider
receipts where available. Declared provenance is not authentication.

Open work includes safe fixed-target/axiom-checked Lean submission execution,
prose adjudication improvements, authenticated model runs, fully locked runner
dependencies, private families, empirical calibration, broader textbook exercise
coverage and independent security review. The continuing Goal remains open.

## Primary interface references

The adapter follows Harbor's [native task layout](https://docs.harborframework.com/tasks/overview),
[configuration](https://docs.harborframework.com/tasks/configuration),
[separate verification](https://docs.harborframework.com/tasks/separate-verifier),
[artifacts](https://docs.harborframework.com/tasks/artifacts) and
[verifier reward interface](https://docs.harborframework.com/tasks/verifier).
No Terminal-Bench tasks or restricted ATLAS materials are imported.

The first native run, [41797663465](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/runs/41797663465),
correctly failed acceptance: the original probe wrongly required a loopback-only
interface list. Its raw logs/artifact remain distinct from corrected runs. The
source audit identified the pinned backend's transparent-proxy/DNS/ICMP semantics.
The corrected route enforces Docker's intrinsic `network_mode:none` and retains
UID/cgroup checks instead of relaxing the original offline requirement.
The intermediate [41799314372](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/runs/41799314372)
also remains failed: a local transparent proxy can accept a TCP handshake without
allowing external traffic, so a sampled connect test was not a sound isolation
criterion either. The static compose route replaces both surrogate probes; it
does not reinterpret either failed run as a model score or accepted environment.

The first accepted static-offline run,
[41800349808](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/runs/41800349808),
checks source commit `875dd2b593429e4900aaa58621ab4dae8a92d4bc`: all seven oracle
trials earn one point and all seven nop trials earn zero, with no exceptions.
The raw artifact was actually inspected: 21 role/probe observations (seven UID
1000 agents and fourteen UID 0 verifiers), loopback-only networking, the CPU and
memory caps, and PID limit 128. This is observed software-fixture evidence, not
a model measurement, independent security review or whole-Goal completion.
