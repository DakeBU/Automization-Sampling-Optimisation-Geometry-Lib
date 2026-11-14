"""Record completed independent image inspection and verify actual evidence bytes."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as advance
import astis_site

CORE = "e566930dccfa74a50fd86b743a3b8eddda21798b"
DIGEST = "5a2978a955ea15d1c1de0cec1c4d201b9d005040ae8018be6d8068b4de04583d"
TARGET = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density"
ADVANCE = "ASTIS-SA-20261106-GaussianComplexityProductDensity"
INTEGRATION = "research-wiki/paper-contributions/GaussianComplexity/ex70-integration-20261106/"
BROWSER = INTEGRATION + "final-browser/"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def raw(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def read(rel: str) -> object:
    return json.loads(raw(rel))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def receipt(rel: str, expected_log_sha: str) -> dict:
    data = read(rel)
    log = Path(data["log"]).read_bytes()
    assert sha(log) == expected_log_sha == data["log_sha256"]
    assert data["exit_code"] == 0 and data["head_before"] == data["head_after"] == CORE
    return {"receipt": rel, "receipt_raw_sha256": sha(raw(rel)), "command": data["command"],
            "started_utc": data["started_utc"], "elapsed_seconds": data["elapsed_seconds"],
            "head_before": data["head_before"], "head_after": data["head_after"], "exit_code": 0,
            "log": data["log"], "log_raw_sha256": sha(log), "log_raw_bytes": len(log)}


def main() -> None:
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip() == CORE
    assert astis_site.source_digest() == DIGEST
    manifest = read(BROWSER + "artifact-manifest.json")
    browser_report = read(BROWSER + "report.json")
    assert sha(raw(BROWSER + "report.json")) == "11c6faffd25a1e60117ff88d7ae8e8b6653e5cbfc35aac6359ded1f223ffc49d"
    assert sha(raw(BROWSER + "executed-browser-check.py")) == "05b8ef15cc0e30f9971aa9551d4e6eaf937bbfd1654d417612e14bcb026abee6"
    assert raw(BROWSER + "executed-browser-check.py") == raw(".astis/huanjian-gc-ex70-integration-20261106/check_final_reader.py")
    assert browser_report["status"] == "passed" and browser_report["head"] == CORE
    assert browser_report["browser_version"] == "156.0.8078.80"
    assert not browser_report["errors"] and not browser_report["external_GitHub_HTML_checked"]
    assert browser_report["actual_compiled_source_digest"] == DIGEST
    assert browser_report["actual_compiled_gate_commit"] == CORE
    assert browser_report["site_metadata"] == read("_site/data/build-metadata.json")
    assert browser_report["site_metadata_sha256"] == sha(raw("_site/data/build-metadata.json"))
    assert len(browser_report["pages"]) == len(browser_report["graphs"]) == 2
    assert {row["width"] for row in browser_report["pages"]} == {1440, 390}
    assert len(browser_report["visible_source_index_clicks"]) == 2
    for row in browser_report["pages"]:
        assert row["target"] == TARGET
        assert row["closed_initially"] and row["adjacent_exact_statement_and_proof"]
        assert row["full_module_and_download_verified"] and row["immutable_git_object_source_bytes_verified"]
        assert row["immutable_source_link_commit_and_path_verified"] is None
        assert row["immutable_source_link_check"] == "not_executed_own_site_route"
        assert not row["external_GitHub_HTML_checked"] and not row["page_overflow"]
    for row in browser_report["graphs"]:
        assert row["target"] == TARGET and row["one_canonical_node"]
        assert row["reference_and_source_edges_not_formal"]
        assert row["canonical_reused_nodes_present_once"] == [
            "AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw.actual_averaged_block_product",
            "AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities.actual_mixture_densities"]
        assert all(edge["evidence"] == ("formal" if edge["relation"] in {"imports", "declares"} else "overlay")
                   for edge in row["edges"])
    # The following observations were made by this reviewer from fourteen actual
    # view_image calls/results; they are not generated from DOM assertions.
    visual = {
        "actual-1440-first.png": "Rendered product-density and unit-mass formula is clear; closed Lean statement sits beside the mathematical statement, with assumptions and proof steps below. The exact e566 gate strip is visible.",
        "actual-1440-proof.png": "Five ordered proof-step headings remain compact and folded. The separate exact Lean proof disclosure is open beneath them; explanatory source-context text is visible. Code continues below this viewport crop and is checked byte-exact by DOM/browser evidence, not claimed fully visible in this PNG.",
        "actual-1440-module.png": "The complete-module disclosure is open, with copy/download controls and highlighted imports, namespace, source attribution and actual theorem start. This is the actual complete source view rather than a theorem-name inventory.",
        "case-boundary-1440.png": "Theorem3.1 is explicitly red/open. The exact Gaussian target, exact oracle, deterministic cap, TV convention and source-domain bullets are readable; its Lean statement is marked not formalized yet and strict boundary begins below.",
        "source-index-1440.png": "Visible Ex70 bridge text preserves Ex71/72 and oracle/cap/expected-cost obligations; determinant sign concerns O and worst-case deterministic cap is distinguished from expected cost. The index says building blocks, not completed paper results, and the extension link gives no chapter-completion credit.",
        "actual-1440-source-index-open.png": "One Ex70 unit opens cleanly among existing units. A visible Read full statement and proof link leads to the canonical focused reader; no duplicated detached proof is inserted into the index.",
        "actual-1440-graph.png": "The highlighted actual_product_density node is unique and readable with both canonical parents present. A solid owning-module declaration edge contrasts with dashed source-reference/audit/source overlays. Surrounding labels wrap or abbreviate within boxes; evidence colouring is separate from source scope.",
        "actual-390-first.png": "The statement, adjacent closed Lean statement and assumptions entry stack in one column. The long formula stays in its local horizontal-scroll box with an explicit scroll hint. The title is partly above the screenshot due to the scripted scroll position, not a layout overflow.",
        "actual-390-proof.png": "Proof-step headings wrap without overlap; the open Lean-proof disclosure and source-context explanation fit the narrow column. Its copy control is visible. Exact code follows below the captured viewport, with DOM/browser byte checks supplying code evidence.",
        "actual-390-module.png": "Long module path wraps inside its disclosure; copy/download controls remain usable. The dark source block scrolls internally horizontally rather than widening the whole page; imports and theorem start are visible.",
        "case-boundary-390.png": "Main theorem title and source anchor wrap clearly; exact Gaussian/oracle/seed/deterministic-cap conditions remain readable in the narrow column. The lower part continues below the viewport as expected.",
        "source-index-390.png": "The cap-versus-expected-cost boundary is visible. Reviewed work remains labelled as building blocks rather than completed paper results; index disclosures and textbook-context link fit the one-column mobile layout.",
        "actual-390-source-index-open.png": "The Ex70 index item opens with a legible title, visible canonical proof link and explanation that source assumptions, evidence and optional Lean sit beside the focused proof. Adjacent units remain compact.",
        "actual-390-graph.png": "Focused target and canonical Eq6/mixture-density parents remain readable. Dashed overlays and solid declaration structure remain distinguishable. The wider surrounding neighbourhood extends beyond the local pan viewport with a visible drag/Fit hint; no whole-page overflow is present."
    }
    screenshot_hashes = {row["file"]: row["sha256"] for row in browser_report["screenshots"]}
    assert len(visual) == len(screenshot_hashes) == 14 and visual.keys() == screenshot_hashes.keys()
    inspected = []
    assert len(manifest["artifacts"]) == 16
    for artifact in manifest["artifacts"]:
        content = raw(BROWSER + artifact["file"])
        assert sha(content) == artifact["sha256"] and len(content) == artifact["bytes"]
        if artifact["file"] != "executed-browser-check.py":
            assert content == raw(manifest["original_directory"] + "/" + artifact["file"])
        if artifact["file"].endswith(".png"):
            assert content[:8] == b"\x89PNG\r\n\x1a\n"
            width, height = struct.unpack(">II", content[16:24])
            assert (width, height) in {(1440, 1000), (390, 844)}
            assert screenshot_hashes[artifact["file"]] == artifact["sha256"]
            inspected.append({**artifact, "width": width, "height": height,
                              "actually_viewed_original": True, "inspection_tool": "view_image(detail=original)",
                              "observation": visual[artifact["file"]], "blocking_visual_findings": []})
    browser_receipt = receipt(".astis/huanjian-resume-20261103/20261107T035521844769Z-ex70-final-browser.receipt.json",
                              "deb9e345fc1c6a56ea8ea0a176997782a607691ff58df396bc1ab966839c5dd4")
    site_receipt = receipt(".astis/huanjian-resume-20261103/20261106T154239520257Z-ex70-final-site-check.receipt.json",
                           "9c034c14df3a5ef7777fb44ad29a090aee2a246637157dda7c732dad6954a0ac")
    graph_receipt = receipt(".astis/huanjian-resume-20261103/20261106T154239520257Z-ex70-final-graph-check.receipt.json",
                            "9f1430c65e76fb967038b8ee5a43274c494421b08e17390532c8c06ffcc89818")
    graph_log = json.loads(Path(graph_receipt["log"]).read_text())
    assert graph_log["status"] == "graph coverage checked"
    assert len(graph_log["contributions"]) == 1
    assert graph_log["contributions"][0]["node"] == "decl:" + TARGET
    assert not graph_log["contributions"][0]["omitted_connections"]
    assert "ASTIS site check passed" in Path(site_receipt["log"]).read_text()
    referenced_reports = {
        "candidate-e566930d-static-integration-review.json": "aa58960690b6c87b0c24c68a686b0d51817f7743c2ec70905f039f7e45acbc47",
        "candidate-e566930d-root-build-static-DOM-review.json": "9b5f7db59ed8949904d9e249c967a6f5522a1958de84028d7ba9c4d51cc9fc04"
    }
    for name, expected in referenced_reports.items():
        assert sha((OUT / name).read_bytes()) == expected
    prior_runtime = json.loads((OUT / "candidate-e566930d-root-build-static-DOM-review.json").read_text())
    assert prior_runtime["site_metadata"] == browser_report["site_metadata"]
    ledger = raw("runs/substantive_advances.jsonl")
    assert sha(ledger) == "108d5df92553290d2408c0d24b94d1ed30cebfbc2b265b8379bbc1d060f6af2d"
    states = advance._replay_advances(json.loads(line) for line in ledger.splitlines() if line.strip())
    protected_states = json.loads((OUT / "baseline-projected-state-hashes.json").read_text())
    assert all(sha(canonical(states[key])) == expected for key, expected in protected_states.items() if key != ADVANCE)
    assert [key for key, value in states.items() if value.get("state") == "STABILIZING"] == [ADVANCE]
    old_frontiers = json.loads((OUT / "baseline-old-frontier-hashes.json").read_text())
    assert all(sha(raw(rel)) == expected for rel, expected in old_frontiers.items())
    cell = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json"
    assert raw(cell) == subprocess.check_output(["git", "show", CORE + ":" + cell], cwd=ROOT)
    assert astis_site.source_digest() == DIGEST
    report = {
        "kind": "independent-final-browser-site-graph-local-integration-acceptance",
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reviewer": "/root/ex70_integration_reader_review", "core_commit": CORE,
        "source_digest": DIGEST, "status": "ACCEPTED_LOCAL_INTEGRATION_AND_READER",
        "blocking_findings": [], "actual_pngs_individually_viewed": 14,
        "viewports": [{"width": 1440, "height": 1000}, {"width": 390, "height": 844}],
        "browser_version": browser_report["browser_version"],
        "browser_report": BROWSER + "report.json", "browser_report_raw_sha256": sha(raw(BROWSER + "report.json")),
        "executed_script": BROWSER + "executed-browser-check.py",
        "executed_script_raw_sha256": sha(raw(BROWSER + "executed-browser-check.py")),
        "archive_manifest_raw_sha256": sha(raw(BROWSER + "artifact-manifest.json")),
        "all16_archives_hash_valid_and_byte_equal_to_run": True,
        "inspected_original_images": inspected,
        "actual_browser_receipt": browser_receipt, "actual_site_check_receipt": site_receipt,
        "actual_graph_check_receipt": graph_receipt,
        "preceding_independent_reports": referenced_reports,
        "root_gate": {"actual_commit": CORE, "actual_jobs": 9642,
                      "actual_root_receipt": prior_runtime["actual_root_receipt"],
                      "actual_final_build_receipt": prior_runtime["actual_site_build_receipt"],
                      "scope": "Actual root Lake/Tests/ASTIS fake-closure/ATLAS acceptance reused without rerun. Build/source digest is unchanged through all later reader checks."},
        "timing": {"root": "2026-11-06T15:09:54.568404Z; completed at15:10:57 gate evidence",
                   "site_build": "2026-11-06T15:12:35.864382Z; actual build elapsed49.091s",
                   "site_graph_checks": "2026-11-06T15:42:39.520257Z; site81.905s, graph6.091s",
                   "actual_Chrome": "2026-11-07T03:55:21.844769Z after platform approval;11.621s",
                   "boundary": "All four stages retain their true timestamps and e566 HEAD/source digest; Nov7 Chrome is not a new Lean build or a relabelled Nov6 browser run."},
        "reader_acceptance": {"five_formula_steps_and_fold_controls": "Executed Chrome toggled all5 proof steps, assumptions, exact statement and proof at both widths. Screenshots show the stated viewport crops; this reviewer does not claim every expanded formula/code region was separately pictured.",
                              "MathJax": "Actual browser waited for MathJax and found rendered containers and no math errors; page error list empty.",
                              "adjacent_exact_Lean": "DOM/static and actual browser compare exact production signature and full proof. Separate initially folded disclosures remain source-adjacent.",
                              "source_index": "One canonical Ex70 unit and actual visible click at each width into the focused source/proof reader.",
                              "sourcecase_boundary": "Theorem3.1 remains red/open; exact source Gaussian/oracle/seed/TV/deterministic-cap conditions remain unchanged. Ex70 alone is accepted; Ex71/72, both main bounds, precision/oracle/cap/expected-cost adapters remain open.",
                              "mobile": "Single-column reader and index accepted. Long formulas/code use local horizontal scrolling and graph uses the advertised local pan/Fit view; these are not whole-page overflow.",
                              "graph": "One canonical Ex70 node and each actual Eq6/mixture-density parent exactly once. Solid imports/declares are formal module structure; source-name scanner/reference/source correspondence/audit edges are overlays, not theorem implications."},
        "source_link_claims": {"actual_route": "own-site", "complete_module_and_download": "Actual HTTP200 bytes equal production and immutable e566 Git object;15,110bytes, SHAa75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228",
                               "immutable_GitHub_URL_verification": None,
                               "GitHub_URL_conditional_branch": "not_executed_own_site_route",
                               "external_GitHub_HTML_checked": False,
                               "external_HTML200_claim": False,
                               "public_source_links": False, "commit_published": False},
        "source_verdict_boundary": {"existing_source_verifier": "/root/ex70_fresh_source_module_review",
                                    "verified_mathematical_commit": "a83254ef00c8e6fd0548a25fae03f07e2a82e2b7",
                                    "candidate_audit_state": "blind-reconstructed",
                                    "candidate_audit_raw_sha256": "71e187c68c29c816e60e0b4b98b032c2efb0b860ba434a3a8629cd669bd4d3a8",
                                    "accepted_successor_audit_state": "source-reviewed",
                                    "accepted_successor_audit_raw_sha256": "91a0565ed2da64800cf3ff0f1bc5169c9d0e54e643ba892a1d81284b30644332",
                                    "publication_binding_sha256": "f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8",
                                    "new_source_verdict": False},
        "protection": {"old276foreign_states_preserved": True, "old435frontiers_byte_preserved": True,
                       "guarded7shared_paths_and_3680input_deltas": "Already independently checked in the static integration report; no further source/shared changes occurred during reader checks.",
                       "source_digest_recomputed_unchanged": True, "current_ledger_raw_sha256": sha(ledger),
                       "reviewer_ledger_frontier_code_writes": 0, "normal_parking": "PENDING_SEPARATE_PARENT_AUTHORIZATION"},
        "remaining": ["Ex71 actual affinity tensorization", "Ex72 amplified TV", "actual determinant-sign oracle/transcript/exact-matvec/TVprecision/deterministic-cap/expectedcost adapters", "fixed-spectrum hidden eigenbasis and both main lower bounds", "remote/main/live/public source delivery", "postmerge purification and ExpositionSeal", "full existing Goal acceptance"],
        "remote_hold": "Old PR385 exact5a OPEN and original-owner frozen native Bench wallcap diagnostic retained; no unchanged Bench rerun, cap change, new push, PR384 edit, merge/deploy or provider/model evaluation performed by this reviewer.",
        "scope": "Acceptance of local integration/runtime/reader at the named immutable core. No remote success, main merge, live deployment, purification/Seal or full Goal completion. No source V or parking event is added."
    }
    output = OUT / "candidate-e566930d-independent-final-browser-site-acceptance.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    assert raw("runs/substantive_advances.jsonl") == ledger
    print(json.dumps({"report": str(output.relative_to(ROOT)), "report_raw_sha256": sha(output.read_bytes()),
                      "status": report["status"], "actually_viewed_PNGs": 14, "blocking_findings": [],
                      "park": "not_executed_waiting_for_separate_authorization"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
