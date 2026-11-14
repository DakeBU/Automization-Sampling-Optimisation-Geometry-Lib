"""Bounded integration checks only; no compiler/site/browser or shared writes."""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as advance
import astis_publication as publication

BASE = "research-wiki/paper-contributions/GaussianComplexity/"
INTEGRATION = BASE + "ex70-integration-20261106/"
CORE = "e566930dccfa74a50fd86b743a3b8eddda21798b"
PARENT = "a1196bf6ad741a261ebc70db4c5193a00b64662e"
MATH = "a83254ef00c8e6fd0548a25fae03f07e2a82e2b7"
TARGET = "AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density"
ADVANCE = "ASTIS-SA-20261106-GaussianComplexityProductDensity"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def raw(rel: str) -> bytes:
    return (ROOT / rel).read_bytes()


def read(rel: str) -> object:
    return json.loads(raw(rel))


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def object_raw(commit: str, rel: str) -> bytes:
    return git("show", commit + ":" + rel)


def json_diff(a: object, b: object, pointer: str = "") -> list[str]:
    if type(a) != type(b):
        return [pointer]
    if isinstance(a, dict):
        result = []
        for key in sorted(set(a) | set(b)):
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            path = pointer + "/" + escaped
            result += json_diff(a[key], b[key], path) if key in a and key in b else [path]
        return result
    if isinstance(a, list):
        if len(a) != len(b):
            return [pointer]
        return [path for i, (x, y) in enumerate(zip(a, b))
                for path in json_diff(x, y, pointer + "/" + str(i))]
    return [] if a == b else [pointer]


def main() -> None:
    assert git("rev-parse", "HEAD").decode().strip() == CORE
    assert git("branch", "--show-current").decode().strip() == "huanjian/gaussian-product-density-integration-20261106"
    manifest = read(INTEGRATION + "shared-integration-manifest.json")
    assert manifest["base_commit"] == PARENT and len(manifest["paths"]) == 7
    shared = {row["path"] for row in manifest["paths"]}
    for row in manifest["paths"]:
        assert sha(raw(row["path"])) == row["after_sha256"]
        assert raw(row["path"]) == object_raw(CORE, row["path"])
        if row["before_sha256"] is not None:
            assert sha(object_raw(PARENT, row["path"])) == row["before_sha256"]
        else:
            assert subprocess.run(["git", "cat-file", "-e", PARENT + ":" + row["path"]], cwd=ROOT,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0
    case_rel = "website/content/samplewiki_companion_frontiers.json"
    case_before = json.loads(object_raw(PARENT, case_rel))
    case_after = read(case_rel)
    pointers = json_diff(case_before, case_after)
    assert pointers == ["/cases/4/reader_guide/3", "/cases/4/theorems/0/boundary"]
    assert case_before["execution"] == case_after["execution"]
    old_inputs = json.loads((OUT / "baseline-protected-input-hashes.json").read_text())
    changed_old_inputs = [rel for rel, expected in old_inputs.items()
                          if not (ROOT / rel).is_file() or sha(raw(rel)) != expected]
    assert set(changed_old_inputs) == shared & old_inputs.keys()
    assert len(changed_old_inputs) == 5
    old_frontiers = json.loads((OUT / "baseline-old-frontier-hashes.json").read_text())
    assert len(old_frontiers) == 435
    assert all(sha(raw(rel)) == expected for rel, expected in old_frontiers.items())
    baseline_ledger = gzip.decompress((OUT / "baseline-advance-ledger.jsonl.gz").read_bytes())
    source_v_prefix = gzip.decompress(raw(INTEGRATION + "normal-stab-claim-ledger-prefix.jsonl.gz"))
    ledger = raw("runs/substantive_advances.jsonl")
    assert ledger.startswith(source_v_prefix) and source_v_prefix.startswith(baseline_ledger)
    claim = read(INTEGRATION + "normal-stab-claim.json")
    stab_append = ledger[len(source_v_prefix):]
    assert sha(source_v_prefix) == claim["before_sha256"]
    assert sha(ledger) == claim["after_sha256"]
    assert sha(stab_append) == claim["append_sha256"]
    stab_rows = [json.loads(line) for line in stab_append.splitlines() if line.strip()]
    assert len(stab_rows) == 1
    stab = stab_rows[0]
    assert stab["advance_id"] == ADVANCE and stab["worker_id"] == "huanjian_gc_20261106_ex70_integration"
    assert stab["from_state"] == "VERIFIED" and stab["to_state"] == "STABILIZING"
    states = advance._replay_advances(json.loads(line) for line in ledger.splitlines() if line.strip())
    hashes = json.loads((OUT / "baseline-projected-state-hashes.json").read_text())
    assert all(sha(canonical(states[key])) == expected for key, expected in hashes.items() if key != ADVANCE)
    assert states[ADVANCE]["state"] == "STABILIZING"
    assert states[ADVANCE]["owner_id"] == "huanjian_gc_20261106_ex70"
    assert states[ADVANCE]["last_actor"] == "huanjian_gc_20261106_ex70_integration"
    lanes = [key for key, value in states.items() if value.get("state") == "STABILIZING"]
    assert lanes == [ADVANCE]
    initial = read(BASE + "product-density-semantic-evidence/initial-environment-queue-protection.json")
    snapshot = initial["lossless_raw_snapshot"]
    assert sha(raw(snapshot["path"])) == snapshot["gzip_sha256"]
    assert sha(gzip.decompress(raw(snapshot["path"]))) == snapshot["uncompressed_sha256"]
    assert sha(raw(initial["source"])) == initial["source_sha256"]
    pins = {
        "AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean": "a75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228",
        "Tests/GaussianComplexityProductDensity.lean": "ad9d4fa4048a2fb88b5eaade4a7bc202f05e0a4b48a13790893f8cc768fbfccd",
        "website/content/declaration_lessons/huanjian-product-density.json": "cf00807161ee7aabf1a9675e25e513bf88c2ae4e7912456953a9f1eec0bf9cd3",
        "website/content/publications/huanjian-product-density.json": "67a09acc094e5fb6023c53e13202e634324b7747f20e568da878c291782c46ac",
        "research-wiki/semantic-roundtrip/audits/huanjian-product-density.json": "91a0565ed2da64800cf3ff0f1bc5169c9d0e54e643ba892a1d81284b30644332"
    }
    assert all(sha(raw(rel)) == expected for rel, expected in pins.items())
    assert all(raw(rel) == object_raw(CORE, rel) for rel in pins)
    assert all(raw(rel) == object_raw(MATH, rel) for rel in pins if "audits/" not in rel)
    assert raw("research-wiki/semantic-roundtrip/audits/huanjian-product-density.json") == object_raw(PARENT, "research-wiki/semantic-roundtrip/audits/huanjian-product-density.json")
    item = next(item for item in publication.load() if item["id"] == "huanjian-product-density")
    binding = next(binding for binding in item["bindings"] if binding["declaration"] == TARGET)
    actual_binding = publication.binding_digest(item, binding)
    assert actual_binding == "f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8"
    registry = raw("AutoSamplingTheory/TechnicalLemmas/Registry.lean").decode()
    old_registry = object_raw(PARENT, "AutoSamplingTheory/TechnicalLemmas/Registry.lean").decode()
    assert registry.count('key := "gaussian-complexity.product-density"') == 1
    assert registry.count('localDecl := "' + TARGET + '"') == 1
    import_line = "import AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity\n"
    assert raw("AutoSamplingTheory.lean") == object_raw(PARENT, "AutoSamplingTheory.lean") + import_line.encode()
    assert raw("AutoSamplingTheory.lean").decode().count(import_line) == 1
    assert raw("Tests.lean").decode().count("import Tests.GaussianComplexityProductDensity\n") == 1
    def eq6_entry(text: str) -> str:
        start = text.index('key := "gaussian-complexity.averaged-block-law"')
        return text[start:text.index('\n  }', start)]
    def without_sald(text: str) -> str:
        return re.sub(r'    saldUse := "[^"\n]*",?\n', '', text)
    assert without_sald(eq6_entry(registry)) == without_sald(eq6_entry(old_registry))
    basic_before = object_raw(PARENT, "Tests/Basic.lean").decode()
    assert raw("Tests/Basic.lean").decode() == basic_before.replace(
        "formalizedTechnicalLemmaCount = 612", "formalizedTechnicalLemmaCount = 613")
    tests = raw("Tests/GaussianComplexityProductDensity.lean").decode()
    production = raw("AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean").decode()
    assert len(re.findall(r'^example\s', tests, flags=re.M)) == 2
    assert tests.count("have h := ProductDensity.actual_product_density hn hnd hκ hb") == 2
    assert "rw [hambient, withDensity_apply _ hB]" in tests
    assert "rw [hcoord, withDensity_apply _ hB]" in tests
    assert len(re.findall(r'^theorem\s', production, flags=re.M)) == 1
    assert "MixtureDensities.actual_mixture_densities hn hκ" in production
    assert "AveragedBlockLaw.actual_averaged_block_product hn hnd hκ hb" in production
    cell_rel = "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json"
    cell = read(cell_rel)
    parent_cell = json.loads(object_raw(PARENT, cell_rel))
    inherited = ["target_statement", "parents", "reuse_plan", "learning_contract", "reader_contract",
                 "statement_seal", "source_proof_coverage", "proof_digestion", "purification", "conceptual_mirror_audit"]
    assert all(cell[key] == parent_cell[key] for key in inherited)
    assert cell["evidence"]["existing_verification_projection"] == parent_cell["evidence"]["existing_verification_projection"]
    assert cell["status"] == "independently_verified"
    assert cell["evidence"]["current_local_integration"]["state"] == "STABILIZING"
    checks = []
    for entry in read(INTEGRATION + "precore-checks.json")["checks"]:
        receipt = read(entry["receipt"])
        log_rel = str(Path(entry["receipt"]).with_suffix("").with_suffix(".log"))
        log = raw(log_rel)
        assert sha(log) == entry["raw_log_sha256"] == receipt["log_sha256"]
        assert receipt["exit_code"] == 0
        assert receipt["head_before"] == receipt["head_after"] == PARENT
        checks.append({"receipt": entry["receipt"], "actual_head": PARENT, "exit_code": 0,
                       "raw_log_sha256": sha(log), "command": receipt["command"]})
    report = {
        "kind": "bounded-independent-static-integration-review",
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reviewer": "/root/ex70_integration_reader_review",
        "core_commit": CORE, "source_V_metadata_parent": PARENT, "mathematical_candidate": MATH,
        "status": "STATIC_INTEGRATION_ACCEPTED_FINAL_RUNTIME_UI_PENDING",
        "shared_manifest_exact_paths": sorted(shared),
        "shared_path_count": 7,
        "samplewiki_raw_scalar_changes": pointers,
        "execution_main_source_statements_oracle_caps_cost_contracts": "All other raw JSON leaves byte/semantic preserved. The two reader scalar updates expose accepted Ex70 only and retain Ex71/72 and both main bounds as open.",
        "source_code_tests_lesson_pub_audit_pins": pins,
        "actual_publication_binding_sha256": actual_binding,
        "canonicality": {"new_Registry_entries": 1, "new_public_source_theorems": 1,
                         "new_root_imports": 1, "new_root_test_imports": 1,
                         "count_612_to_613": "Administrative inventory assertion only",
                         "old_Eq6_entry": "Only saldUse is changed to cite the actual production Ex70 consumer; old note and proof scope preserved.",
                         "duplicate_parent_proofs": False, "generated_graph": "Pending final build and graph-check; stale _site preview not accepted."},
        "actual_consumer_review": {"count": 2, "domain": "All allowed d,n,kappa and either fixed common sign",
                                   "ambient": "Same actual D.bind gamma on arbitrary measurable sets equals the actual ambient density lintegral",
                                   "split": "Same actual target mapped by literal split on arbitrary measurable sets equals coordinate density lintegral",
                                   "same_target_directly_called": True,
                                   "compiler_boundary": "Textual/static review plus original source V only; current canonical root runtime gate is not yet accepted."},
        "contract_inheritance": {"preserved_current_parent_fields": inherited,
                                 "existing_source_V_projection_preserved": True,
                                 "source_review_audit_note": "Current audit source-reviewed/accepted91a056 is inherited from source-V metadata parent. Mathematical candidate audit was blind-reconstructed71e187, not byte-equal to the accepted successor.",
                                 "remaining": "Ex71/72, actual oracle/transcript/TVprecision/deterministic query cap/expectedcost, hidden eigenbasis, both main lower bounds, remote/main/live, purification/ExpositionSeal and full Goal remain open."},
        "protection": {"old_276_projected_states_preserved": True, "old_435_frontier_byte_hashes_preserved": True,
                       "old_3680_inputs": {"unchanged": len(old_inputs) - len(changed_old_inputs), "authorized_shared_changes": sorted(changed_old_inputs), "unexpected_changes": []},
                       "source_snapshot_and_lossless_gzip_preserved": True,
                       "source_V_ledger_prefix_sha256": sha(source_v_prefix), "current_ledger_sha256": sha(ledger),
                       "exact_V_prefix_preserved": True, "single_STAB_append_raw_sha256": sha(stab_append),
                       "single_STAB_owner": stab["worker_id"], "single_STAB_lane": lanes,
                       "original_proof_owner": states[ADVANCE]["owner_id"], "reviewer_ledger_writes": 0},
        "actual_precore_check_receipts": checks,
        "precore_scope": "Actual precursor commands ran at a119 with the then-uncommitted guarded shared bytes; they are not relabelled as fresh e566 root/build/browser checks.",
        "pending": ["Actual canonical root Lean/Tests/ASTIS gate", "Final current site build/check", "Final graph-check and rendered branch", "Actual installed Chrome1440/390 interactions and fourteen originals individually viewed", "Separate later normal parking authorization"],
        "nonblocking_historical_text": "The inherited consulted Eq6 hypothesis_adapter still says the new coordinate-volume proof remains pending. It is a preproof consultation description, superseded by current source_detail_audit gap and evidence; no new source defect or blocking claim is inferred.",
        "final_acceptance": False,
        "new_source_verdict": False
    }
    assert git("rev-parse", "HEAD").decode().strip() == CORE and raw("runs/substantive_advances.jsonl") == ledger
    output = OUT / "candidate-e566930d-static-integration-review.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"report": str(output.relative_to(ROOT)), "report_raw_sha256": sha(output.read_bytes()),
                      "status": report["status"], "shared_paths": 7, "foreign_states": 276, "old_frontiers": 435,
                      "unexpected_protected_changes": 0, "final_acceptance": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
