"""Single stabilization lane: import and register independently verified SAU77."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.path.insert(0, str(Path.cwd() / "tools"))
import astis_advance as advance

run = Path("runs/20261007-companion-priority/pbps-unit-exponential-product77")
claim = json.loads((run / "claim.json").read_bytes())
state = advance.current_advances()[claim["advance_id"]]
assert state["state"] == "VERIFIED", state["state"]
science = "4f88383540a865aea304c63c40de5a699ea61611"
assert state["latest_evidence"]["verified_commit"] == science
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == science
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
out = run / "integration77"
out.mkdir(exist_ok=False)
owned = ["AutoSamplingTheory/TechnicalLemmas/Probability.lean",
         "AutoSamplingTheory/TechnicalLemmas/Registry.lean", "Tests/Basic.lean",
         "docs/companion-papers-handoff.md", "website/content/samplewiki_companion_frontiers.json",
         "conversion-windows/ASTIS-SW-PBPS-2026.md",
         "research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl"]
before = []
for i, name in enumerate(owned):
    raw = Path(name).read_bytes()
    snapshot = out / f"{i}.before.exactraw.snapshot"
    snapshot.write_bytes(raw)
    before.append({"path": name, "RAW_sha256": hashlib.sha256(raw).hexdigest(),
                   "snapshot": snapshot.as_posix()})
(out / "owned-before.json").write_text(json.dumps(before, indent=2) + "\n", encoding="utf-8")

def add_after(path, anchor, addition):
    p = Path(path)
    raw = p.read_bytes()
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    a = anchor.encode() + newline
    assert raw.count(a) == 1 and addition.encode() not in raw, path
    p.write_bytes(raw.replace(a, a + addition.encode().replace(b"\n", newline), 1))

decl = claim["target_declarations"][0]
module = "AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct"
add_after(owned[0], "import AutoSamplingTheory.TechnicalLemmas.Probability.UniformExpectationGap",
          "import " + module + "\n")
add_after(owned[1], "import AutoSamplingTheory.TechnicalLemmas.Probability.LawMap",
          "import " + module + "\n")
note = (f"Independently verified at {science} by /root/exact_verify77. Actual countable Exp(1) "
        "product, measurable coordinates/clamps, exact coordinate marginals and mutual independence, "
        "simultaneous almost-sure positivity/clamp equality and divergent threshold sums. No public "
        "probability/iid/integrability/convergence provider premises. ASTIS bounded-indicator SLLN "
        "route is separate from the author's open direct Exp mean-one expansion. PBPS finite-recursion "
        "spacing is the next consumer; nonaccumulation/global path/Markov/invariance/main/error/cost/"
        "actual-input composition and whole-paper/Goal completion remain open. Aggregate/reader, "
        "purification/main/live states remain separately evidence-bound.")
block = "  {\n" + "\n".join([
    '    key := "probability.unitExponentialProduct"',
    "    localDecl := " + json.dumps(decl),
    '    upstreamDecl := "Countable unit-exponential input law and divergent threshold sums"',
    '    upstreamFile := "arXiv2609.06905v1 AppendixA1 independent Exp1 inputs and Ex9/SLLN"',
    "    status := LemmaMemoryStatus.formalizedLocal",
    '    tags := ["probability", "exponential", "infinite-product", "independence", "SLLN"]',
    '    saldUse := "PBPS clock consumer; no SALD claim"',
    "    note := " + json.dumps(note)
]) + "\n  },\n"
add_after(owned[1], "def analysisMemory : List LemmaMemoryEntry := [", block)
p = Path(owned[2]); raw = p.read_bytes()
assert raw.count(b"formalizedTechnicalLemmaCount = 525") == 1
p.write_bytes(raw.replace(b"formalizedTechnicalLemmaCount = 525", b"formalizedTechnicalLemmaCount = 526"))

prefix = f"""## Actual countable exponential inputs (2026-10-10)

Independently verified science commit {science}.
The actual countable Exp(1) product is a probability measure; raw coordinate
and clamped threshold maps are Borel, raw coordinate laws are exactly Exp(1)
and mutually independent. On one full-measure event all coordinates are
strictly positive and equal their nonnegative clamps. Threshold partial sums
diverge almost surely. There are no supplied probability/iid/moment/SLLN
premises. The sufficient ASTIS indicator-SLLN route and original author direct
Exp mean-one route are explicitly distinct; the latter remains an open
background expansion. Seven adjacent formula/BODY steps, independent math,
blind reconstruction and fresh source-first review accepted the exact module.

Next edge: compose these actual inputs with the verified finite recursion76
and original-energy waiting increment to obtain event-time nonaccumulation.
Treat C0=0/positive first threshold separately; positive cap division is used
only for C0>0. In WithTop NNReal, convergence to infinity uses neighborhoods of
top or eventual passage above every finite time, not the atTop filter, which
would require eventually equal to top. No physical-time global process,
Markov/invariance/kernel, full hypocoercivity/main/error/cap/expected-query
cost or actual-input composition is admitted. TV proximity does not transfer
unbounded costs. PBPS/SPHMC plus composition precede Gaussian Cloud, then
midpoint with no extra higher derivative premise. Preserve older work.

Serialized aggregate/publication/site/graph/visual checks are pending for this
integration candidate. Main merge, PURIFIED/Exposition, live deployment and
whole-paper/Goal completion remain distinct and unearned.

"""
add_after(owned[3], "# Companion-paper formalization handoff", "\n" + prefix)
p = Path(owned[4]); raw = p.read_bytes()
assert raw.count(b'"updated": "2026-10-08"') == 1
assert raw.count(b'docs/companion-papers-handoff.md#exact-finite-pbps-jump-recursion-2026-10-10') == 1
raw = raw.replace(b'"updated": "2026-10-08"', b'"updated": "2026-10-10"', 1)
raw = raw.replace(b'docs/companion-papers-handoff.md#exact-finite-pbps-jump-recursion-2026-10-10',
                  b'docs/companion-papers-handoff.md#actual-countable-exponential-inputs-2026-10-10', 1)
p.write_bytes(raw)
p = Path(owned[5]); raw = p.read_bytes(); nl = b"\r\n" if b"\r\n" in raw else b"\n"
title, rest = raw.split(nl, 1)
text = ("\n## Countable exponential input law77 (2026-10-10)\n\n"
        f"Independent science commit {science}. The actual product/coordinate laws, "
        "mutual independence, simultaneous a.s. positivity and divergent clamped sums are verified. "
        "Statement and seven formula/BODY steps remain authored once in unit-exponential-product "
        "declaration lesson/publication, with exact adjacent folded Lean. The next actual consumer "
        "is recursion76 event-time nonaccumulation; process/invariance/main/cost/composition remain open. "
        "Aggregate/site/graph/visual/purification/main/live evidence are recorded separately in "
        "SAU77 integration notes.\n\n")
p.write_bytes(title + nl + text.encode().replace(b"\n", nl) + rest)
entry = {"key": "probability.unitExponentialProduct", "local_decl": decl,
         "local_file": claim["proposed_files"][0], "status": "formalized-local",
         "verified_commit": science, "evidence": state["latest_evidence"],
         "next_action": note}
with Path(owned[6]).open("ab") as f:
    f.write((json.dumps(entry, ensure_ascii=False) + "\n").encode())
lanes = [s for s in advance.current_advances().values() if s['state'] == 'STABILIZING']
assert len(lanes) == 1 and lanes[0]['advance_id'] == 'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'
assert lanes[0]['latest_evidence']['integration_owner'] == 'companion_root_20261005'
# The existing four-paper integration lane carries the whole pending branch.
# Keep this child advance VERIFIED until canonical integration is admitted.
(out / "integration-scope.json").write_text(json.dumps({"owned": owned, "science_commit": science,
    "single_stabilization_owner": "/root", "aggregate": "pending", "visual": "pending",
    "Goal_complete": False}, indent=2) + "\n", encoding="utf-8")
print("Prepared verified SAU77 integration: canonical Probability/Registry/Tests526; aggregate pending.")
