"""Run only after distinct whole-header and source topology acceptance."""
from pathlib import Path
import copy, datetime, hashlib, json, subprocess, sys

root = Path.cwd()
pre = Path(__file__).parent
run = pre.parent / "pbps-actual-absolute-next-event-time91"
aid = "ASTIS-SA-20261011-PBPSActualAbsoluteNextEventTime"
cid = "ASTIS-SW-PBPS-actual-absolute-next-event-time"
owner = "companion_root_20261005"
file = "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean"
decl = "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law"
parents = [
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension.actual_finite_history_extension",
    "AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity.actual_conditional_next_wait_density",
]
def load(p):
    return json.loads(Path(p).read_bytes())
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p).replace("\\", "/"), "raw_sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
def fresh(p, obj):
    assert not p.exists(), p
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
auth = load(pre / "root.preproof91.authorization.json")
assert auth["all_independent_reviews_accepted"] and not auth["Lean_BODY"]
for x in auth["checked_RAW"]:
    assert pin(x["path"])["raw_sha256"] == x["raw_sha256"], x["path"]
header = pre / "header91.proposed.lean"
assert pin(header)["raw_sha256"] == auth["accepted_header_raw_sha256"]
baseline = load(pre / "pre-fetch91.workspace-RAW.json")
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == baseline["HEAD"]
for p, sha in baseline["tracked_modified"].items():
    assert pin(p)["raw_sha256"] == sha, p
assert not subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True).strip()
sys.path.insert(0, str(root / "tools"))
import astis_advance as adv
states = adv.current_advances()
assert aid not in states and not (root / file).exists() and not run.exists()
assert states["ASTIS-SA-20261011-PBPSActualFiniteHistoryExtension"]["state"] == "VERIFIED"
assert [k for k, v in states.items() if v["state"] == "STABILIZING"] == ["ASTIS-SA-20261005-SPHMCImplementedPhaseKernel"]
delta = "Derive actual next absolute-event-time density against real Lebesgue measure, exact strict relative/absolute event identification, and complete-history transport with all nonnegative joint tests."
anchor = "Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2), one absolute-time coordinate ingredient of (A.7), and Appendix A.2; attributed ASTIS source-implicit completion."
boundary = ("Exactly six original analytic hypotheses and literal iid Exp(1) stopped recursion. Fixed y,xRef,z0 and deterministic event depth n; arbitrary fixed Borel finite-valued absolute horizon b may be unbounded across histories. U reads the actual next record. Strict live event a(Hn)<U<b(Hn) equals the positive relative-cap event. Borel absolute density, every-history fiber mass<=1, guarded actual clock/whole-history append, exact actual restricted joint/marginal laws and all joint ENNReal tests on every old-history event (including null ones) are derived internally. Stopped time0, raw negative flow and T+max(u-T,0) off-support append are auxiliary only. No normalization, integrability, finite-wait, no-atom, survival or coordinate/provider premise. Existing actual-input a.s. nonaccumulation78 and half-open coverage79 are retained and not reproved. Only one coordinate edge within S87-I5/G86-11 is targeted. Finite ordered iteration, final88 survival/hazard assembly, endpoint resolution when used, actual count/prescribed path identification, A7 summability/fullA7, physical-time residual restart/Markov, invariance/semigroup/L2/hypocoercivity, implementation/errors/unbounded costs/main/composition/full papers/Goal remain OPEN.")
run.mkdir()
seal = {
    "status": "SEALED_BEFORE_BODY_AFTER_DISTINCT_PREPROOF_MATH_SOURCE_AND_TOPOLOGY_ACCEPTANCE",
    "sealed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "statement_version": 1,
    "header": pin(header), "expanded_literal_Prop": header.read_text(encoding="utf-8").split("private def ", 1)[1].split("\nend", 1)[0],
    "public_theorem": decl,
    "primary_first_freeze": pin(pre / "independent-source-first91/primary-first91.freeze.native.json"),
    "source_graph": pin(pre / "source-proof-graph91.accepted-successor.json"),
    "source_coverage": pin(pre / "independent-source-first91/source-coverage91.v2.native.json"),
    "independent_authorization": pin(pre / "root.preproof91.authorization.json"),
    "reuse_search": [pin(pre / "independent-source-first91/retrieval91.native.json"), pin(pre / "retrieval91.facade-memory-reuse.json")],
    "toolchain": pin("lean-toolchain"), "lake_manifest": pin("lake-manifest.json"),
    "truth_boundary": boundary, "proof_BODY_created": False, "collaborator_RAW_preservation_count": 21,
    "chronology_disclosure": "Creator primary-only graph and distinct primary-only reconstruction preceded candidate/header. Exact three-operation A7 route overlay independently reviewed by89, applied before header. Whole35-let header independently accepted by77 mathematics/type and87 source before this Seal. Originals and reviewer-only pointer negatives retained.",
}
sealpath = run / "root.statement-seal91.json"
fresh(sealpath, seal)
proposal = adv.AdvanceProposal(
    advance_id=aid, task_id="ASTIS-SW-PBPS-2026", goal=delta, source_anchor=anchor,
    theorem_delta=delta, truth_boundary=boundary, created_by=owner, dag_inputs=tuple(parents),
    proposed_files=(file,), focused_checks=("lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime",),
    modes=("faithfulPaper",), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(proposal)
adv.transition_advance(aid, "CLAIMED", worker_id=owner, evidence={"statement_seal": str(sealpath), "owned_files": [file]})
adv.transition_advance(aid, "EXPLORING", worker_id=owner, evidence={"route": "Actual90 strict full-history law; internally derived history-dependent Lebesgue translation and actual next-record-time identification.", "truth_boundary": boundary})
fresh(run / "claim.json", proposal.as_event())
c = copy.deepcopy(load("research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-extension.json"))
c.update(cell_id=cid, title="Actual PBPS strict next absolute-event-time density",
         source_anchor=anchor, target_statement=header.read_text(encoding="utf-8"), status="claimed",
         parents=parents, consumers=["S91-J: constant absolute horizon supplies next ordered-simplex coordinate of A7"],
         source_targets=[decl], blocked={"status": False, "reason": "Whole source topology and exact route repair plus independent current-header math/type/source accepted; proof pending."})
c["evidence"] = {"substantive_advance": aid, "statement_seal": str(sealpath), "focused_checks": [], "owned_files": [file], "truth_boundary": boundary}
searches = [str(pre / "independent-source-first91/retrieval91.native.json"), str(pre / "retrieval91.facade-memory-reuse.json")]
reason = "Reuse actual90 complete-history extension;89 directly only for jointly Borel density/all-history fiber facts besides its transitive probability role. Pinned Mathlib additive invariance/skew-product and measure integration APIs supply coordinate transport internally. No duplicate background or upstream port."
c["shared_floor_audit"] = {"searched": searches, "classification": "adapt", "decision": "adapt_existing", "canonical_declaration": decl, "canonical_shared_cell": "", "reason": reason}
c["reuse_plan"] = {"searched_existing": searches, "reused_declarations": parents, "new_shared_declarations": [], "known_consumers": [], "planned_consumers": c["consumers"], "no_duplicate_wrapper": True, "decision_reason": reason}
c["statement_seal"] = {"evidence": str(sealpath), "source_revision": "arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d", "statement_version": 1, "signature_digest": pin(header)["raw_sha256"], "binder_audit": ["Six original analytic binders unchanged.", "Borel b/A/G/F specify admissible observables, not analytic hypotheses.", "Actual recursion/coordinate invariance/measurability/density/fiber bounds are conclusions or internal dependencies, never provider binders."], "definition_kind": "35 literal lets:14 model plus actual complete histories, literal next-record observer, total absolute append and strict restricted density/law objects."}
c["source_proof_coverage"] = {"source_graph": str(pre / "source-proof-graph91.accepted-successor.json"), "source_inventory": "runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json", "coverage_report": auth["math_decision"]["path"], "reviewed_adapter_overlay": auth["source_decision"]["path"], "coverage_status": "Source-first20nodes/23edges/27dispositions; independent topology and exact3op route repair, whole35let/sixbinder math/type/source accepted. Only one strict actual absolute-coordinate edge targeted; proof pending."}
c["source_detail_audit"] = {"primary_edition": c["statement_seal"]["source_revision"], "primary_anchor": anchor, "fidelity_boundary": boundary, "detail_status": "omitted", "gap": "Explicit actual relative-to-absolute weighted law and next-record identification are implicit in A7 iteration.", "consulted": [{"source": "Pinned primary A1/A2, actual90/89 and fixed Mathlib", "anchor": "A1.E1;A1.E2;A1.E7;A1.SS2", "hypothesis_adapter": "No extra source premise; all Borel/translation/guard/fiber facts proved internally."}]}
c["proof_digestion"] = {"existing_substrate": parents, "bookkeeping": ["Derive Borel absolute observers/append and history-dependent Lebesgue shear.", "Identify strict relative/absolute guards and actual next-record time from literal recurrence.", "Translate weighted density and actual full-history law; derive all joint tests and fiber mass."], "new_reusable": [], "new_topology": delta}
c["purification"] = {"status": "pending", "dead_code_audit": "Proof pending", "duplicate_semantics_audit": "No existing actual absolute-time density law located by bounded retrieval.", "canonicalization": reason, "compressed_spine_delta": delta, "reader_default_view": "Complete attributed statement/formula proof, exact folded Lean adjacent.", "scope": boundary}
lc = c["learning_contract"]
lc["failure_class"] = "NONE"
lc["salvage"] = {"required": False, "status": "not-applicable", "reason": "No proof before Seal; exact source graph repair and reviewer-only pointer negative retained.", "promoted_fragments": [], "discarded_fragments": []}
lc["parallelism"].update(decision="serial", direction_fingerprints=["actual-absolute-clock/strict-density/Lebesgue-translation"], shared_verified_context_digest=seal["primary_first_freeze"]["raw_sha256"])
lc["reader_backpressure"].update(purification_status="pending", exposition_seal_status="pending", exposition_evidence="", source_expansion_nodes=["S91-M", "S90-E", "S89-D", "S91-T", "S91-C:TARGET", "S91-J:OPEN", "S91-F:OPEN", "S91-A7:OPEN"], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
c["graph_contribution"].update(focus_targets=[decl], lean_view="integration-node", overview_view="no-change-with-reason", functor_view="none-found", visual_review="Pending proof/publication and actual inspectable affected branch; no visual or formal credit from overlays.")
c["conceptual_mirror_audit"] = {"status": "pending", "discovery_ids": [], "reason": "Required before PROVED_LOCAL."}
fresh(root / "research-wiki/frontier-cells" / (cid + ".json"), c)
for label, args in [
    ("publication-packet-before-proof91", ["tools/astis_publication.py", "packet", "--cell", cid]),
    ("frontier-before-proof91", ["tools/astis_frontier_cells.py", "check"]),
]:
    q = subprocess.run([sys.executable, "-X", "utf8", *args], capture_output=True)
    (run / (label + ".stdout.json")).write_bytes(q.stdout)
    (run / (label + ".stderr.log")).write_bytes(q.stderr)
    fresh(run / (label + ".receipt.json"), {"exit_code": q.returncode, "terminal_closed": True})
    assert q.returncode == 0, (q.stdout + q.stderr).decode(errors="replace")[-4000:]
print(json.dumps({"Seal": pin(sealpath), "advance": aid, "state": "EXPLORING", "proof_credit": False}))
