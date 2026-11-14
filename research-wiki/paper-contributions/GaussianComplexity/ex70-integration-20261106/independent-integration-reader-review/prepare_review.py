"""Read-only repository inventory; writes only this independent report folder."""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "tools"))
import astis_advance as advance


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode()


def read(rel: str) -> object:
    return json.loads((ROOT / rel).read_text())


def write(name: str, value: object) -> None:
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main() -> None:
    prefix = "research-wiki/paper-contributions/GaussianComplexity/"
    prior_path = prefix + "product-density-semantic-evidence/initial-environment-queue-protection.json"
    old = read(prior_path)
    ledger = (ROOT / "runs/substantive_advances.jsonl").read_bytes()
    records = [json.loads(line) for line in ledger.splitlines() if line.strip()]
    # Pure replay avoids current_advances/load_jsonl tail recovery and locks.
    states = advance._replay_advances(records)
    state_hashes = {key: sha(canonical(value)) for key, value in states.items()}
    old_state_failures = [key for key, expected in old["protected_projected_state_hashes"].items()
                          if state_hashes.get(key) != expected]
    old_frontier_failures = [rel for rel, expected in old["protected_frontiers"].items()
                            if not (ROOT / rel).is_file()
                            or sha((ROOT / rel).read_bytes()) != expected]
    prev_inputs_path = prefix + "eq6-integration-20261106/independent-integration-reader-review/local-integration-parking.protected-inputs.json"
    prev_inputs = read(prev_inputs_path)
    input_failures = [rel for rel, expected in prev_inputs.items()
                      if not (ROOT / rel).is_file()
                      or sha((ROOT / rel).read_bytes()) != expected]
    gzmeta = old["lossless_raw_snapshot"]
    gzraw = (ROOT / gzmeta["path"]).read_bytes()
    inflated = gzip.decompress(gzraw)
    source = ROOT / old["source"]
    new_id = "ASTIS-SA-20261106-GaussianComplexityProductDensity"
    assert not old_state_failures and not old_frontier_failures and not input_failures
    assert len(old["protected_projected_state_hashes"]) == 276
    assert len(old["protected_frontiers"]) == 435
    assert sha(gzraw) == gzmeta["gzip_sha256"]
    assert sha(inflated) == gzmeta["uncompressed_sha256"]
    assert sha(source.read_bytes()) == old["source_sha256"]
    assert states[new_id]["state"] == "PROVED_LOCAL"
    assert not [key for key, value in states.items() if value.get("state") == "STABILIZING"]
    module = "AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean"
    tests = "Tests/GaussianComplexityProductDensity.lean"
    assert sha((ROOT / module).read_bytes()) == "a75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228"
    assert sha((ROOT / tests).read_bytes()) == "ad9d4fa4048a2fb88b5eaade4a7bc202f05e0a4b48a13790893f8cc768fbfccd"

    write("baseline-projected-state-hashes.json", state_hashes)
    write("baseline-old-frontier-hashes.json", old["protected_frontiers"])
    write("baseline-protected-input-hashes.json", prev_inputs)
    baseline_gzip = gzip.compress(ledger, mtime=0)
    (OUT / "baseline-advance-ledger.jsonl.gz").write_bytes(baseline_gzip)
    assert gzip.decompress(baseline_gzip) == ledger
    tracked = [module, tests, "Tests.lean", "AutoSamplingTheory.lean",
               "AutoSamplingTheory/TechnicalLemmas/Registry.lean",
               "website/content/samplewiki_companion_frontiers.json",
               "runs/substantive_discoveries.jsonl",
               "research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json",
               "research-wiki/semantic-roundtrip/audits/huanjian-product-density.json",
               "website/content/publications/huanjian-product-density.json",
               "website/content/declaration_lessons/huanjian-product-density.json"]
    write("baseline-integration-input-hashes.json",
          {rel: sha((ROOT / rel).read_bytes()) for rel in tracked})
    report = {
        "kind": "bounded-independent-integration-reader-preparation",
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reviewer": "/root/ex70_integration_reader_review",
        "scope": "Read-only preparation plus report-folder writes. No source verdict, mathematical proof, shared projection, transition, final root gate or browser acceptance.",
        "head": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "expected_mathematical_candidate": "a83254ef00c8e6fd0548a25fae03f07e2a82e2b7",
        "production_sha256": sha((ROOT / module).read_bytes()),
        "tests_sha256": sha((ROOT / tests).read_bytes()),
        "expected_publication_binding_sha256": "f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8",
        "current_advance": {"advance_id": new_id, "state": states[new_id]["state"],
                            "owner_id": states[new_id].get("owner_id")},
        "source_verdict": "Pending distinct ex70_fresh_source_module_review actor; local capsule is not a verdict.",
        "old_state_protection": {"count": 276, "failures": old_state_failures,
                                 "hash_encoding": "SHA256 of ensure_ascii=False, sort_keys=True, separators=(',',':') JSON"},
        "frontier_protection": {"old_count": 435, "current_directory_json_files": len(list((ROOT / "research-wiki/frontier-cells").glob("*.json"))),
                                "failures": old_frontier_failures,
                                "scope": "The old 435 includes three templates; new cell is the 436th JSON. Do not confuse directory count with registered cells or semantic audit count."},
        "old_eq6_inputs": {"count": len(prev_inputs), "failures": input_failures,
                          "PBPS_name_matches": sum("pbps" in x.lower() or "proximalbps" in x.lower() for x in prev_inputs),
                          "SPHMC_name_matches": sum("sphmc" in x.lower() or "smoothedpicard" in x.lower() for x in prev_inputs),
                          "Bench_name_matches": sum("bench" in x.lower() for x in prev_inputs),
                          "manifest": prev_inputs_path},
        "source_snapshot": {"path": old["source"], "sha256": sha(source.read_bytes()),
                            "lossless_old_protection_snapshot": gzmeta,
                            "gzip_integrity_checked": True},
        "ledger_baseline": {"path": "runs/substantive_advances.jsonl", "sha256": sha(ledger),
                            "bytes": len(ledger), "events": len(records), "projected_states": len(states),
                            "lossless_archive": "baseline-advance-ledger.jsonl.gz", "archive_sha256": sha(baseline_gzip),
                            "append_only_required": True},
        "single_stabilization_lane": [],
        "eq6_checkpoint": {"path": prefix + "eq6-integration-20261106/resume-checkpoint.json",
                           "state": "VERIFIED", "actual_root_ui_commit": "2c09c24ff73b42a2555493fc00616d2a0f803a86",
                           "scope": "Historical Eq6 acceptance, not a new Ex70 gate or browser run."},
        "remote_hold": "Preserve old PR385 exact5a OPEN and original-owner frozen native Bench wallcap failure; no unchanged retry, cap change, new push, PR384 edit, merge or deploy.",
        "future_next_event": "Wait for source actor's real normal-API VERIFIED receipt and explicit parent authorization before mechanical projection.",
        "status": "PREPARATION_ONLY"
    }
    write("bounded-preparation-report.json", report)
    print(json.dumps({"report": str(OUT.relative_to(ROOT) / "bounded-preparation-report.json"),
                      "head": report["head"], "old_states": 276, "old_frontiers": 435,
                      "old_inputs": len(prev_inputs), "new_state": states[new_id]["state"],
                      "status": report["status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
