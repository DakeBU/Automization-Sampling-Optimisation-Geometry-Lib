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
