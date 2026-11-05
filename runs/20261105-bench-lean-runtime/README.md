# Agentic Lean runtime checkpoint

Continues the existing Bench Goal after PR377/main692973fc; issue378 records the
bounded evaluator task. Branch: codex/sog-bench-lean-executor. No mathematical
frontier, production Lean, Registry, QA binding, split, level or prior review is
changed. The website's executor-pending boundary remains accurate.

The code now prepares separate agent/challenge/oracle packets for all13 currently
admitted aligned targets. Actual local export and the first trusted stage work.
Eight packaging/isolation-argument tests pass; Python syntax and diff checks pass.
The first real export caught a wrong editorial-schema key (`status` rather than
`editorial`); it was corrected by reusing review.accepted and adding regression
coverage, without changing admission evidence. Windows has no usable Linux/Docker
runtime. No submitted or hostile Lean was executed on the host.

The pinned official comparator/exporter use Lean4.33.0. Real Landrun inside a
readonly/nonroot/network-none/resource-limited Docker container protects build and
export; comparator checks serialized meanings, allowed axioms and kernel replay.
The statement-only challenge's explicit proof hole is never a proof/blue leaf;
importing it must fail the solution axiom check. Gold is not mounted in that
verifier. All external sources/pins and limits are in lean-runtime/policy.json.

Native CI has not yet run at this checkpoint. The draft acceptance workflow must
actually pass all13 oracle targets and five negative software fixtures; export is
not runtime acceptance. Hostile I/O/resource trials, independent runtime review,
agent trajectories/harness and real model/provenance/calibration/private-family
work remain open. Software fixtures are not model measurements. Preserve failed
native evidence and diagnose before changing code; do not silently weaken gates.

The collaborator-owned untracked KernelReversibilityTransport source/test, three
older blind reports and both preserved stashes remain untouched and unstaged.

## First real native outcome and exact repairs

Draft PR379/headac2b6e78 started native run41997590399/job127144468544. It actually
compiled all trusted references plus the pinned comparator/exporter/Landrun, then
failed building the image: the pinned Ubuntu image already has UID1000. No oracle
or negative proof ran. The log is retained locally at
.astis/sog-bench/lean-native-first-failure.log and in the immutable GitHub job.
The Dockerfile now creates the home directory for numeric UID1000 without adding
another account or granting capabilities. This is an infrastructure repair, not
proof rejection, native acceptance or a model score.

Separately, direct Lean4.33 Lake source inspection identified that stripping Git
metadata from a Git manifest forces offline materialization to attempt a fetch or
replacement. The trusted stage now uses a path projection of the *same* original
package graph, retains the original manifest, and checks every prepared checkout
against its pinned revision. The project root's manifest/toolchain stay unchanged.
A local trusted `lake env lean --version` loading probe succeeds on that projected
graph; it executes no submitted/hostile Lean. A ninth regression test verifies the
projection. Agent packets retain project license/notices. Preparation inputs are
archived before the Docker build so a future setup failure still has tool hashes.

The GitHub connector had a transport failure during observation; the same live
run was rechecked using cached Git authentication, kept only in memory, through
the repository's read-only Actions API. No credential was printed, saved or sent
to a redirected log host. Observation failure did not trigger a replacement run.
The actual terminal infrastructure failure, then these exact code repairs, are
the reason for a fresh-head acceptance attempt. Full native/hostile/harness/model
requirements remain open. Root Tests9611 and ASTIS check passed with unchanged Lean.

## Native02: actual isolation, failed trusted dependency read

Fresh-head40103979 run41999171893/job127149770711 built the image and actually
started the first controlled oracle container. Immutable artifact13401483013 has
ZIP SHA256994a8f46b3aa7671cf369b7283e10ba70ede34fd0d8311f0c9d92d19bf50dbfe.
The three raw JSON members retained in native-02 are unmodified extractions:
preparation, software-trials and the first oracle result. The observation reports
UID/GID1000, capabilities0, no-new-privileges1, only lo, readonly root, Landlock
ABI8, memory4294967296, PID128 and CPU200000/100000. This is real scoped runtime
evidence, not successful mathematical/model acceptance.

The trusted Challenge build failed reading dependency .trace files with EACCES,
before any Solution verification. The old raw report's `proof-rejected` field is
preserved verbatim, but this is diagnosed as **infrastructure**, not a wrong
reference proof. The suite stopped at that first unexpected oracle outcome;
0/13 positive targets and no negative fixtures are accepted. Lake4.33's actual
readTraceFile uses ordinary IO.FS.readFile, so readonly data is compatible; do not
weaken mounts or replace the checker. The next repair copies private-mode public
cache files and normalizes only the new snapshot directories for container read
access. Original shared cache inode permissions stay unchanged. The POSIX mode
test runs only in Linux CI; preparation now records actual copied-mode examples.

The supervisor additionally preflights the trusted Challenge separately before
solution verification and emits framed phases. Output text cannot become a control
record; partial output retains the last valid phase for failure classification.
CLI status, consistent container/exit evidence, tool/receipt drift and framing now
have tests. The local suite runs14 tests:13 pass and the POSIX-specific one is
skipped on Windows; this is not a Linux permission/runtime pass. The initial framing fixture
mistakenly used pretty multiline JSON rather than the producer's actual compact
NDJSON; that fixture was corrected, not the strict parser. The next exact-head
native run must still pass every positive/negative task. Website readiness stays
pending; no native result, QA, theorem or Goal completion is claimed.

## Native03: eleven real target checks; remaining preflight timeout

Headcd2eddcc run42003282167/job127163630550 finished with11 accepted reference
targets (001,002,003,015,016,017,018,019,021,022,023). The immutable14 raw JSON
members in native-03 preserve all12 attempted outcomes, preparation and summary.
Artifact13404717712 ZIP SHA256 is
3fae6fe927ca14665dfc8373ad820ebd3332b2933205557d8b264d18ee3f1a61,
matching the job's advertised digest. Each positive is an actual fixed-target
comparison, permitted-axiom audit and kernel replay, not a model measurement.
The whole run still failed:025 reached the unchanged180-second wall limit in
challenge-preflight;028 and all five negative fixtures were not attempted.
The failed result correctly records infrastructure-error, not proof rejection.
Its only captured output was the phase marker, so no specific last compiler
action or sole cause of timeout is inferred from that empty diagnostic.

The cache-read repair is evidenced by the prepared snapshot:130335 private-mode
public cache files were copied (examples report0600),9975 were hard-linked.
The source host's inodes were not chmodded; actual readonly/nonroot/cgroup checks
remain present. Direct Lean4.33 Module.checkArtifactsExist inspection then exposed
a separate definite staging defect: C output is required, but owned snapshots
copied only lib/lean artifacts. Current host GibbsC1Poincare.trace likewise names
its C artifact. Missing C/IR forces rebuilding already-compiled ancestors. The
next fix includes the same allowed parents' complete C/IR/lib artifacts and
preserves timestamps; no target, assumption, proof or180-second budget changes.
It must still be tested rather than assumed to resolve the whole timeout.

Bounded live diagnostic frames now preserve compiler output even if a later
timeout kills the container. Child data is base64, not control/verdict text.
Policy schema2 records a separate2MiB wire limit while retaining the256KiB raw
diagnostic limit. Tool-inventory/source-version guards and new complete-cache/
framing tests bring the local suite to17 (16 pass,1 POSIX test skipped on Windows).
No missing artifact is paper progress and no oracle time is a calibrated task
difficulty or model score. Full13-positive/five-negative, hostile-I/O/resource,
independent review/harness and actual-model requirements remain open. The PR
stays draft and public readiness remains executor pending.

## Native04: complete fixed-target and negative acceptance

Head72d5322df56c8f010010659f6ff9166c8feee07f, run42010581633/job127188269829
succeeded. All13 admitted fixed targets passed real comparison, axiom checks and
fresh Lean-kernel replay. All5 negative cases were rejected; the actual diagnostics
identify the changed statement, sorryAx, bogus axiom, imported Challenge's sorryAx
and a spoofed success line still rejected for sorryAx, respectively. The native
Linux job also passed all17 then-current unit tests. Exact-head contributor,
Bench, native-Harbor-graph and site workflows succeeded separately. This is not
merge, independent runtime review or a model measurement.

Artifact13407573365 has verified ZIP SHA256
3ce1baca77bdbe169a9778f9dae5250709e44869444fbbbb50fd7cda6dd765b8.
The20 JSON members under native-04 are unchanged extractions: preparation,
summary and18 per-call results. Earlier failed evidence remains untouched.
Oracle025 took152.7 seconds and028 took118.5, below the unchanged180-second
limit. Those are software fixture timings, not difficulty calibration or model
performance. No source, theorem, assumption, cache identity or time budget was
relaxed to obtain this pass.

The next bounded patch adds real denied-write/network probes, wall/output limits
and missing/oversized/invalid-UTF8/symlink/FIFO handoff evidence. These have21
local contract tests (19 pass,2 POSIX-only skips); that Windows result does not
execute or certify the hostile native fixtures. A fresh native CI must check the
actual markers and expected causes. Invalid inputs now receive bounded evidence
without a container rather than disappearing as uncaught exceptions. Agent tool
trajectories, first-final accounting, independent runtime review and actual-model
provenance/calibration/private-family work remain separate required steps.
