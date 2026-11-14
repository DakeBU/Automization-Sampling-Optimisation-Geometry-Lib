"""Record the one authorized normal verification with private replay comparison."""

import copy
import datetime as dt
import json
import os
import stat
import subprocess
import sys
import time
from pathlib import Path

import check_verification_inputs as inputs


sys.path.insert(0, str(inputs.ROOT))
from tools import astis_advance
from tools.astis_publication import check_advance


OUTPUT = inputs.PHASES / "phase5"
LEDGER = Path("runs/substantive_advances.jsonl")
LEDGER_PREFIX_SHA = "6f0d361eac4a51473d1fec4b3bf26decbba9eb4ff6e6d015e84385fda7b4bc53"
CELL = Path("research-wiki/frontier-cells/ASTIS-SHARED-std-gaussian-radial-exponential.json")
CELL_OLD_SHA = "5f4b67c963390aef0c665944be2b6b90895d29fdfe4945eed9db6ed385042673"
MARKER = OUTPUT / "normal-VERIFIED-call.O_EXCL.json"
FRONTIER_COMMAND = [inputs.PYTHON, "-B", "tools/astis_frontier_cells.py", "check"]


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def create_exclusive(path, raw, mode=0o644):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())


def replay(raw):
    inputs.require(raw.endswith(b"\n"), "Ledger lacks a complete terminal LF")
    records = [json.loads(line) for line in raw.splitlines()]
    inputs.require(all(isinstance(record, dict) for record in records), "Invalid ledger record shape")
    return astis_advance._replay_advances(records), records


def foreign_cells():
    return {path: inputs.sha(path.read_bytes()) for path in CELL.parent.glob("*.json") if path != CELL}


def prepare():
    evidence = inputs.check_inputs()
    inputs.require(not MARKER.exists(), "Normal verification marker already exists")
    ledger_raw = inputs.pinned(LEDGER, LEDGER_PREFIX_SHA)
    inputs.require(ledger_raw == inputs.git_blob(inputs.HEAD, LEDGER), "Ledger prefix differs from immutable HEAD")
    before, old_records = replay(ledger_raw)
    item = before[inputs.ADVANCE]
    old_proof = evidence["original_proved_local"]
    proof_raw = Path(old_proof["append_path"]).read_bytes()
    target_events = [record for record in old_records if record.get("advance_id") == inputs.ADVANCE]
    inputs.require(ledger_raw.splitlines(keepends=True).count(proof_raw) == 1
                   and target_events[-1] == old_proof["event"], "The exact original PROVED_LOCAL event is not current")
    inputs.require(item["state"] == "PROVED_LOCAL" and item["owner_id"] == inputs.OWNER
                   and item["schema_version"] == 4 and item["publication_declarations"] == [inputs.PRODUCER]
                   and item["latest_evidence"] == old_proof["evidence"], "Current replayed target mismatch")

    cell_raw = inputs.check_current(CELL, CELL_OLD_SHA)
    cell_before = json.loads(cell_raw)
    inputs.require(cell_before["status"] == "proved_locally" and cell_before["owner_id"] == inputs.OWNER
                   and cell_before["advance_id"] == inputs.ADVANCE
                   and cell_before["evidence"]["independent_verification"] == "",
                   "Frontier status or evidence field was not the expected baseline")
    source_status = b'"status": "proved_locally"'
    source_field = b'"independent_verification": ""'
    inputs.require(cell_raw.count(source_status) == cell_raw.count(source_field) == 1,
                   "Frontier target fields are not unique in the raw cell")
    new_cell = cell_raw.replace(source_status, b'"status": "independently_verified"', 1).replace(
        source_field, f'"independent_verification": "{inputs.REVIEW}"'.encode("utf-8"), 1
    )
    expected_cell = copy.deepcopy(cell_before)
    expected_cell["status"] = "independently_verified"
    expected_cell["evidence"]["independent_verification"] = str(inputs.REVIEW)
    inputs.require(json.loads(new_cell) == expected_cell, "Frontier replacement would change other fields")

    all_foreign_cells = foreign_cells()
    check_advance([inputs.PRODUCER], reviewed=True)
    return evidence, ledger_raw, before, old_records, cell_raw, new_cell, all_foreign_cells


def run_frontier_check():
    start = now()
    monotonic = time.monotonic()
    result = subprocess.run(FRONTIER_COMMAND, cwd=inputs.ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log_path = OUTPUT / "whole-frontier.actual.log"
    create_exclusive(log_path, result.stdout)
    receipt = {
        "command": FRONTIER_COMMAND, "cwd": str(inputs.ROOT), "started_utc": start,
        "exit_code": result.returncode, "elapsed_seconds": time.monotonic() - monotonic,
        "log": str(log_path), "log_sha256": inputs.sha(result.stdout),
        "head": inputs.git("rev-parse", "HEAD").decode().strip(),
    }
    create_exclusive(OUTPUT / "whole-frontier.actual.receipt.json", json_bytes(receipt))
    inputs.require(result.returncode == 0 and b"ASTIS Frontier Cell protocol check passed" in result.stdout,
                   "Whole Frontier check failed after cell update")
    return receipt


def record(prepared):
    evidence, raw_before, before, records_before, cell_raw, new_cell, foreign_cell_hashes = prepared
    started = now()
    monotonic = time.monotonic()
    receipt = {
        "command": [inputs.PYTHON, "-B", str(OUTPUT / Path(__file__).name), "--verify"],
        "cwd": str(inputs.ROOT), "started_utc": started, "head_before": inputs.HEAD,
        "advance_id": inputs.ADVANCE, "verifier_id": inputs.REVIEWER, "api_calls": 0,
    }
    log_path = OUTPUT / "normal-verification.actual.log"
    log = []
    try:
        inputs.require(inputs.git("rev-parse", "HEAD").decode().strip() == inputs.HEAD
                       and LEDGER.read_bytes() == raw_before and CELL.read_bytes() == cell_raw,
                       "Immutable HEAD, ledger or cell changed before the normal call")
        create_exclusive(MARKER, json_bytes({
            "started_utc": started, "advance_id": inputs.ADVANCE, "actor": inputs.REVIEWER,
            "head": inputs.HEAD, "precall_ledger_sha256": LEDGER_PREFIX_SHA,
            "purpose": "Exactly one normal PROVED_LOCAL to VERIFIED call.",
        }))
        receipt["api_calls"] = 1
        astis_advance.transition_advance(
            inputs.ADVANCE, "VERIFIED", worker_id=inputs.REVIEWER, evidence=evidence
        )

        raw_after = LEDGER.read_bytes()
        inputs.require(raw_after.startswith(raw_before), "The exact ledger prefix did not survive")
        append = raw_after[len(raw_before):]
        inputs.require(append.endswith(b"\n") and append.count(b"\n") == 1, "Ledger did not append exactly one line")
        event = json.loads(append)
        inputs.require(event["event"] == "transition" and event["advance_id"] == inputs.ADVANCE
                       and event["from_state"] == "PROVED_LOCAL" and event["to_state"] == "VERIFIED"
                       and event["worker_id"] == inputs.REVIEWER and event["evidence"] == evidence,
                       "Appended event differed from the authorized transition")
        create_exclusive(OUTPUT / "actual-VERIFIED-append.exact.jsonl", append)
        create_exclusive(OUTPUT / "actual-VERIFIED-evidence.full.json", json_bytes(event["evidence"]))

        after, records_after = replay(raw_after)
        foreign_before = {key: item for key, item in before.items() if key != inputs.ADVANCE}
        foreign_after = {key: item for key, item in after.items() if key != inputs.ADVANCE}
        inputs.require(foreign_before == foreign_after, "A full foreign replay value changed")
        item = after[inputs.ADVANCE]
        stable_keys = set(before[inputs.ADVANCE]) - {"state", "last_actor", "latest_evidence", "updated_at"}
        inputs.require(item["state"] == "VERIFIED" and item["owner_id"] == inputs.OWNER
                       and item["last_actor"] == inputs.REVIEWER and item["latest_evidence"] == evidence
                       and all(item[key] == before[inputs.ADVANCE][key] for key in stable_keys),
                       "Target owner or other retained target replay field changed")
        inputs.require(len(records_after) == len(records_before) + 1, "Ledger replay event count mismatch")
        inputs.require(CELL.read_bytes() == cell_raw and foreign_cells() == foreign_cell_hashes,
                       "A Frontier file changed before the bounded cell write")
        staging = OUTPUT / "frontier-cell-replacement.tmp"
        mode = stat.S_IMODE(CELL.stat().st_mode)
        create_exclusive(staging, new_cell, mode)
        os.chmod(staging, mode)
        os.replace(staging, CELL)
        inputs.require(CELL.read_bytes() == new_cell, "Bounded Frontier write did not persist exactly")
        frontier = run_frontier_check()
        inputs.require(LEDGER.read_bytes() == raw_after and CELL.read_bytes() == new_cell
                       and foreign_cells() == foreign_cell_hashes and frontier["head"] == inputs.HEAD,
                       "Verified state changed after the whole Frontier check")

        report = {
            "advance_id": inputs.ADVANCE, "normal_api_calls": 1,
            "state_before": "PROVED_LOCAL", "state_after": "VERIFIED",
            "reviewer": inputs.REVIEWER, "owner_preserved": inputs.OWNER,
            "old_raw_prefix_bytes": len(raw_before), "old_raw_prefix_sha256": inputs.sha(raw_before),
            "old_raw_prefix_preserved_exactly": True,
            "new_appended_events": 1, "exact_append_sha256": inputs.sha(append),
            "new_ledger_sha256": inputs.sha(raw_after),
            "foreign_full_replay_values_preserved": len(foreign_before),
            "foreign_full_evidence_and_owners_preserved": True,
            "private_foreign_baseline_exported": False,
            "foreign_frontier_files_byte_preserved": len(foreign_cell_hashes),
            "cell": str(CELL), "cell_before_sha256": inputs.sha(cell_raw),
            "cell_after_sha256": inputs.sha(new_cell),
            "only_changed_cell_fields": ["status", "evidence.independent_verification"],
            "independent_verification_evidence": str(inputs.REVIEW),
            "reader_controls": "HOLD", "browser_desktop_and_mobile": "pending",
            "whole_frontier": frontier,
        }
        create_exclusive(OUTPUT / "bounded-preservation-report.json", json_bytes(report))
        log.extend([
            f"VERIFIED normal transition recorded by {inputs.REVIEWER}.",
            f"Exact single append SHA-256 {inputs.sha(append)}.",
            f"Owner and all {len(foreign_before)} full foreign replay values preserved.",
            "Only this Frontier cell's status and independent-verification path changed.",
            "Whole Frontier check passed. Reader controls and desktop/mobile acceptance remain HOLD.",
        ])
        receipt["exit_code"] = 0
    except Exception as exc:
        log.append(f"{type(exc).__name__}: {exc}")
        receipt["exit_code"] = 1
    receipt["head_after"] = inputs.git("rev-parse", "HEAD").decode().strip()
    receipt["elapsed_seconds"] = time.monotonic() - monotonic
    log_raw = ("\n".join(log) + "\n").encode("utf-8")
    create_exclusive(log_path, log_raw)
    receipt["log"] = str(log_path)
    receipt["log_sha256"] = inputs.sha(log_raw)
    create_exclusive(OUTPUT / "normal-verification.actual.receipt.json", json_bytes(receipt))
    print(log_raw.decode("utf-8"), end="")
    return receipt["exit_code"]


def main():
    inputs.require(sys.argv[1:] in (["--preflight"], ["--verify"]), "Supply --preflight or --verify")
    prepared = prepare()
    if sys.argv[1] == "--preflight":
        evidence, raw, before, records, _, _, foreign_cell_hashes = prepared
        print(json.dumps({
            "head": inputs.HEAD, "proof_commit": inputs.MATH, "advance_id": inputs.ADVANCE,
            "current_state": before[inputs.ADVANCE]["state"], "current_owner": inputs.OWNER,
            "old_ledger_sha256": inputs.sha(raw), "old_event_count": len(records),
            "foreign_replay_values_held_privately": len(before) - 1,
            "foreign_frontier_hashes_held_privately": len(foreign_cell_hashes),
            "strict_publication_gate": "PASS", "gate_receipts_checked": len(evidence["gate"]),
            "normal_api_calls": 0,
        }, ensure_ascii=False))
        return 0
    return record(prepared)


if __name__ == "__main__":
    raise SystemExit(main())
