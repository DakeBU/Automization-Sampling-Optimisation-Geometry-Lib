import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
from tools import astis_advance

discovery_id = "ASTIS-DISC-20261111-GaussianRowKernelDoobLayerCake"
actor = "/root/truncated_radial_topology_93de"
review = Path(".astis/semantic-neutral-20261110/rm_tc_93de/conceptual-review")
evidence = Path(
    "research-wiki/paper-contributions/GaussianComplexity/"
    "truncated-radial-moment-semantic-evidence"
)
ledger = Path("runs/substantive_discoveries.jsonl")
verdict = review / "verdict.md"


def digest(data):
    return hashlib.sha256(data).hexdigest()


candidate_bytes = (evidence / "conceptual-mirror-layer-cake.json").read_bytes()
raw_event = (evidence / "conceptual-mirror-raw-discovery.exact.jsonl").read_bytes()
assert digest(candidate_bytes) == "cb76ae66f04fbb38ec7a96c04d225bde4e6292b6afb413be9020baa3448ea609"
assert digest(raw_event) == "f5687b9645495f8be14cfff6d750a182e2be4fe1ca89c693464416ad0263f7ac"
candidate = json.loads(candidate_bytes)
raw = json.loads(raw_event)
assert raw["event"] == "discovery"
assert raw["status"] == "raw"
assert raw["kind"] == candidate["kind"] == "conceptual-mirror"
assert raw["discovery_id"] == candidate["discovery_id"] == discovery_id
assert raw["advance_id"] == candidate["advance_id"]
assert raw["metadata"] == candidate["metadata"]
assert raw["created_by"] == candidate["proposed_by"] != actor
verdict_sha256 = digest(verdict.read_bytes())
note = f"Independent conceptual-mirror validation. Evidence {verdict} (SHA-256 {verdict_sha256})."

before = ledger.read_bytes()
before_state = astis_advance.current_discoveries(ledger)
assert ledger.read_bytes() == before
assert before.endswith(b"\n")
assert before.splitlines(keepends=True).count(raw_event) == 1
assert before_state[discovery_id] == raw
before_other = {key: value for key, value in before_state.items() if key != discovery_id}
assert len(before_other) == 41

astis_advance.transition_discovery(discovery_id, "validated", actor=actor, note=note)

after = ledger.read_bytes()
after_state = astis_advance.current_discoveries(ledger)
assert ledger.read_bytes() == after
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines(keepends=True)) == 1 and append.endswith(b"\n")
event = json.loads(append)
assert event == {
    "schema_version": raw["schema_version"],
    "event": "discovery_transition",
    "discovery_id": discovery_id,
    "from_status": "raw",
    "to_status": "validated",
    "actor": actor,
    "note": note,
    "created_at": event["created_at"],
}
assert after_state[discovery_id] == {
    **raw,
    "status": "validated",
    "updated_at": event["created_at"],
    "latest_note": note,
    "latest_actor": actor,
}
after_other = {key: value for key, value in after_state.items() if key != discovery_id}
assert before_other == after_other
other_canonical_bytes = json.dumps(
    before_other, ensure_ascii=False, sort_keys=True, separators=(",", ":")
).encode()

result = {
    "event": event,
    "exact_raw_discovery_sha256": digest(raw_event),
    "prior_ledger_bytes": len(before),
    "prior_ledger_sha256": digest(before),
    "after_ledger_bytes": len(after),
    "after_ledger_sha256": digest(after),
    "prior_ledger_is_exact_prefix": True,
    "append_bytes": len(append),
    "append_sha256": digest(append),
    "append_line_count": 1,
    "other_replayed_values_identical": len(after_other),
    "other_replayed_values_canonical_sha256": digest(other_canonical_bytes),
    "candidate_metadata_matches_raw": True,
    "verdict_sha256": verdict_sha256,
}
(review / "validation-append.exact.jsonl").write_bytes(append)
result_bytes = (json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
(review / "transition-result.json").write_bytes(result_bytes)
print(result_bytes.decode(), end="")
