# Native Harbor graph adapter

This optional adapter turns the existing independently admitted **graph-json**
tasks into native Harbor tasks. It is not a Lean submission executor, prose
judge, hidden test split, measured model result or security certification.
Initial status: implementation/local tests; native Linux CI evidence is required
before calling this integration operationally tested.

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

`oracle` copies the published reference answer; `nop` supplies no answer. These
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
The full export contains answers: do not provide its root directory to an agent
as closed-book context. Harbor receives the task and stages only its appropriate
components; reviewers can inspect the full package.

The agent runs as the unprivileged `bench` user. Both agent and verifier have a
loopback-only network, one CPU and 256 MiB memory. A runtime probe checks those
actual cgroup/network observations; incompatible hosts fail the fixture rather
than earn correctness credit. It is not a proof of container escape resistance.
Storage/PID limits and arbitrary Lean sandboxing are not certified here.

The verifier starts in a **fresh separate environment**, receiving only the
declared `/output/answer.json` artifact. The oracle writes an undeclared marker;
verification rejects inherited marker state, testing the isolation boundary.
The agent image has neither tests nor gold. Grading imports the byte-identical
owned `sog_bench_curriculum.py`, not a parallel implementation of the score.

The output is parsed only as bounded UTF-8 JSON. Oversized/special/symlink files,
duplicate keys, non-finite values, stale bindings, invalid schemas and missing
answers fail. No `eval`, submitted Python, shell or Lean is run by the verifier.
The reward is exactly the canonical structural-set-and-truth-boundary point;
imports/constant occurrences never certify mathematical necessity.

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
