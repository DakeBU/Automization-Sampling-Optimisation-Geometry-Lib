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
