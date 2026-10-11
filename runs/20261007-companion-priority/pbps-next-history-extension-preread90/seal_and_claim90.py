"""Run only after distinct current-header mathematical and source acceptance."""
import copy
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PRE = Path(__file__).resolve().parent
RUN = PRE.parent / "pbps-actual-finite-history-extension90"

def load(p):
    return json.loads(p.read_bytes())

def pin(p):
    b = p.read_bytes()
    return {"path": p.relative_to(ROOT).as_posix(),
            "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

def fresh(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")

def verify(obj):
    if isinstance(obj, dict):
        sha = obj.get("raw_sha256", obj.get("sha256"))
        if "path" in obj and sha:
            p = Path(obj.get("closed_snapshot", obj["path"]))
            p = p if p.is_absolute() else ROOT / p
            assert pin(p)["raw_sha256"] == sha, p
            if "bytes" in obj:
                assert p.stat().st_size == obj["bytes"], p
        for value in obj.values():
            verify(value)
    elif isinstance(obj, list):
        for value in obj:
            verify(value)

authorization = load(PRE / "root.preproof90.authorization.json")
assert authorization["all_independent_reviews_accepted"] is True
for item in authorization["closed_evidence"]:
    verify(item)
    verify(load(ROOT / item["path"]))
header = PRE / "header90.v2.proposed.lean"
assert pin(header)["raw_sha256"] == authorization["accepted_header_raw_sha256"]
assert load(PRE / "header-elaboration90-v2/receipt.json")["exit_code"] == 0
baseline = load(PRE / "pre-fetch90.workspace-RAW.json")["tracked_modified"]
for path, sha in baseline.items():
    assert pin(ROOT / path)["raw_sha256"] == sha, path
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT).strip()

sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as adv

aid = "ASTIS-SA-20261011-PBPSActualFiniteHistoryExtension"
cid = "ASTIS-SW-PBPS-actual-finite-history-extension"
owner = "companion_root_20261005"
file = "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean"
decl = "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension.actual_finite_history_extension"
states = adv.current_advances()
assert aid not in states and not (ROOT / file).exists()
assert states["ASTIS-SA-20261011-PBPSActualConditionalNextWaitDensity"]["state"] == "VERIFIED"
assert [k for k, v in states.items() if v["state"] == "STABILIZING"] == [
    "ASTIS-SA-20261005-SPHMCImplementedPhaseKernel"]
parents = [
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity.actual_conditional_next_wait_density",
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law",
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws",
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws",
]
delta = "Derive the jointly Borel full finite-history append, its actual guarded recursion identity, and the strict finite next-history/relative-wait joint and marginal laws with all nonnegative joint tests and old-history events."
anchor = "Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2), one density/update iteration ingredient of (A.7), and Appendix A.2 finite-recursion Borel paragraph; attributed ASTIS source-implicit completion."
boundary = "Six original analytic hypotheses and literal stopped iid exponential-clock recursion unchanged. Every deterministic depth n, all abstract histories and rank-zero E included. A jointly Borel append preserves every old record and appends actual cumulative time/post-bounce state on the strict finite event B={0<W_n<d(H_n)}. Fixed Borel finite-valued d may be unbounded across histories; all jointly Borel extended nonnegative tests and null old-history events included without normalization or integrability/positive-mass premises. Negative-time/stopped append branches are auxiliary totalizations only. Joint and marginal n+1-history laws are restricted to B, never unrestricted laws or finite-wait guarantees. Only one actual history-extension edge within S87-I5/G86-11 closes if proved. Ordered absolute-time iteration, final survival/path assembly, full A7/global G86-11, physical-time residual memorylessness/random-depth restart/Markovness, invariance/nonexplosion/hypocoercivity/implementation errors/unbounded costs/main/composition/wholepaper/Goal remain OPEN. Survival88 and no-atom results are not AND parents."
RUN.mkdir(exist_ok=False)
statement = header.read_text(encoding="utf-8").split("private def ", 1)[1].split("\nend", 1)[0]
seal = {
    "status": "SEALED_BEFORE_BODY_AFTER_DISTINCT_PREPROOF_MATH_SOURCE_AND_TOPOLOGY_ACCEPTANCE",
    "sealed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "statement_version": 1, "header": pin(header), "expanded_literal_Prop": statement,
    "public_theorem": decl,
    "primary_first_freeze": pin(PRE / "independent-source-first90/source-first90.native.json"),
    "source_graph": pin(PRE / "source-proof-graph90.accepted-successor.json"),
    "source_coverage": pin(PRE / "independent-source-first90/source-coverage90.native.json"),
    "independent_authorization": pin(PRE / "root.preproof90.authorization.json"),
    "reuse_search": [pin(PRE / "retrieval90.json"), pin(PRE / "retrieval90.facade-memory-addendum.json")],
    "toolchain": pin(ROOT / "lean-toolchain"), "lake_manifest": pin(ROOT / "lake-manifest.json"),
    "truth_boundary": boundary, "proof_BODY_created": False,
    "collaborator_RAW_preservation_count": len(baseline),
    "chronology_disclosure": "Primary-first creator and distinct source-topology reconstruction preceded every90 candidate/header. Two source-topology scope strings were distinctly reviewed and adopted before header review; original source files remain immutable. V1 section-end syntax failure and V2 correction preserved. Whole V2 header independently reviewed before this Seal; no proof BODY exists.",
}
fresh(RUN / "root.statement-seal90.json", seal)
proposal = adv.AdvanceProposal(
    advance_id=aid, task_id="ASTIS-SW-PBPS-2026", goal=delta, source_anchor=anchor,
    theorem_delta=delta, truth_boundary=boundary, created_by=owner, dag_inputs=tuple(parents),
    proposed_files=(file,), focused_checks=(
        "lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension",),
    modes=("faithfulPaper",), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid, "CLAIMED", worker_id=owner,
                       evidence={"statement_seal": str(RUN / "root.statement-seal90.json"), "owned_files": [file]})
adv.transition_advance(aid, "EXPLORING", worker_id=owner,
                       evidence={"route": "Verified89 strict joint density transported through actual Borel whole-history append; guarded constructor identity derived from literal finite recursion.", "truth_boundary": boundary})
fresh(RUN / "claim.json", proposal.as_event())
c = copy.deepcopy(load(ROOT / "research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-conditional-next-wait-density.json"))
c.update(cell_id=cid, title="Actual PBPS one-step complete finite-history extension",
         source_anchor=anchor, target_statement=header.read_text(encoding="utf-8"),
         status="claimed", parents=parents,
         consumers=["PBPS A.7 actual full-history density/update iteration within S87-I5/G86-11"],
         source_targets=[decl], blocked={"status": False, "reason": "Independent preproof source, topology and whole-header mathematical reviews accepted; proof pending."})
c["evidence"] = {"substantive_advance": aid, "statement_seal": str(RUN / "root.statement-seal90.json"),
                 "focused_checks": [], "owned_files": [file], "truth_boundary": boundary}
searches = [str(PRE / "retrieval90.json"), str(PRE / "retrieval90.facade-memory-addendum.json")]
searches += [item["path"] for item in load(PRE / "retrieval90.json")["exact_inputs"]]
reason = "Actual89 supplies the exact strict density/joint-test law; actual87 supplies actual next-history Borelness, actual flow/reflection supply the constructor. Generic finite tuple and measurable measure-map transport already belong to pinned Mathlib. No copied background leaf or external port."
c["shared_floor_audit"] = {"searched": searches, "classification": "adapt", "decision": "adapt_existing",
                          "canonical_declaration": decl, "canonical_shared_cell": "", "reason": reason}
c["reuse_plan"] = {"searched_existing": searches, "reused_declarations": parents, "new_shared_declarations": [],
                   "known_consumers": [], "planned_consumers": c["consumers"], "no_duplicate_wrapper": True, "decision_reason": reason}
c["statement_seal"] = {"evidence": str(RUN / "root.statement-seal90.json"),
    "source_revision": "arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d",
    "statement_version": 1, "signature_digest": pin(header)["raw_sha256"],
    "binder_audit": ["Six original analytic hypotheses unchanged.", "Borel cutoff, history events and ENNReal functions are admissible tests.", "All append, history and transport measurability and actual recursion identities are conclusions, never provider premises."],
    "definition_kind": "28 literal model, complete-history/append/lift and restricted-law lets; auxiliary raw-negative/stopped append is identified as actual only on strict finite B."}
c["source_proof_coverage"] = {"source_graph": str(PRE / "source-proof-graph90.accepted-successor.json"),
    "source_inventory": "runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json",
    "coverage_report": authorization["math_decision"], "reviewed_adapter_overlay": authorization["source_decision"],
    "coverage_status": "Primary-first7nodes/8edges/3AND/22dispositions; distinct topology review and exact two-field source-scope repair; independent whole current-header mathematics/source accepted. Only one actual next-history extension edge targeted; no BODY credit."}
c["source_detail_audit"] = {"primary_edition": c["statement_seal"]["source_revision"], "primary_anchor": anchor,
    "fidelity_boundary": boundary, "detail_status": "omitted",
    "gap": "Source iterates density/update factors implicitly; explicit all-history Borel append and actual restricted next-history transport are needed. Full ordered-time/final-factor assembly remains separate.",
    "consulted": [{"source": "Pinned primary A.1/A.2; compiled actual89/87/flow/reflection; pinned Mathlib",
                  "anchor": "A1.E1;A1.E2;A1.E7;A1.SS2.p3", "hypothesis_adapter": "No new source premise; cutoff/joint tests/unnormalized restrictions explicit."}]}
c["proof_digestion"] = {"existing_substrate": parents,
    "bookkeeping": ["Construct jointly Borel append/lift and actual Hnext using exact verified producers.",
                    "Derive all-prefix preservation and actual guarded whole-history update from Nat.rec.",
                    "Transport verified89 joint measure and nonnegative-test identities, then marginalize."],
    "new_reusable": [], "new_topology": delta}
c["purification"] = {"status": "pending", "dead_code_audit": "Proof pending",
    "duplicate_semantics_audit": "No existing actual full next-history extension law found.",
    "canonicalization": reason, "compressed_spine_delta": delta,
    "reader_default_view": "Complete attributed statement and stepwise formula proof with exact folded Lean adjacent.", "scope": boundary}
c["learning_contract"]["failure_class"] = "NONE"
c["learning_contract"]["salvage"].update(required=False, status="not-applicable",
    reason="No BODY before Seal; V1 section-closure syntax failure and exact V2 correction retained.",
    promoted_fragments=[], discarded_fragments=[])
c["learning_contract"]["parallelism"].update(decision="serial",
    direction_fingerprints=["actual-full-history/finite-append/strict-density-transport"],
    shared_verified_context_digest=seal["primary_first_freeze"]["raw_sha256"])
c["learning_contract"]["reader_backpressure"].update(purification_status="pending", exposition_seal_status="pending",
    exposition_evidence="", source_expansion_nodes=["S90-D1", "S90-A1", "S90-M1", "S90-R1", "S90-T:TARGET", "S87-I5-ordered-assembly:OPEN"],
    lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
c["graph_contribution"].update(focus_targets=[decl], lean_view="integration-node",
    overview_view="no-change-with-reason", functor_view="none-found",
    visual_review="Pending exact proof/publication and inspectable affected branch. Conceptual overlays never formal credit.")
c["conceptual_mirror_audit"] = {"status": "pending", "discovery_ids": [], "reason": "Required before PROVED_LOCAL."}
fresh(ROOT / "research-wiki/frontier-cells" / (cid+".json"), c)
for label, args in [
    ("publication-packet-before-proof90", ["tools/astis_publication.py", "packet", "--cell", cid]),
    ("frontier-before-proof90", ["tools/astis_frontier_cells.py", "check"]),
]:
    q = subprocess.run([sys.executable, "-X", "utf8", *args], cwd=ROOT, capture_output=True)
    (RUN / (label+".stdout.json")).write_bytes(q.stdout)
    (RUN / (label+".stderr.log")).write_bytes(q.stderr)
    fresh(RUN / (label+".receipt.json"), {"exit_code": q.returncode, "terminal_closed": True})
    assert q.returncode == 0, (q.stdout+q.stderr).decode(errors="replace")[-4000:]
print("90 Statement Seal/claim complete; bounded publication/frontier PASS. No proof credit.")
