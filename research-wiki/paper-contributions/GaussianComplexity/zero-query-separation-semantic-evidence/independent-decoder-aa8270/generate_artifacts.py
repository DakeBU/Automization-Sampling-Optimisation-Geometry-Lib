import datetime
import hashlib
import json
import os
from pathlib import Path

BASE = Path("/private/tmp/sr-pkt-aa8270")
IDENTITY = "/root/neutral_decoder_aa8270"
EXPECTED_RAW = "d5e384030e996b85c33402b5855968d32b9045791d4d6ce710d3f58027e64e0d"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def create(name, data):
    with (BASE / name).open("xb") as handle:
        handle.write(data)

started = datetime.datetime.now(datetime.timezone.utc).isoformat()
raw = (BASE / "input.json").read_bytes()
assert digest(raw) == EXPECTED_RAW
packet = json.loads(raw)
canonical = json.dumps(
    {key: value for key, value in packet.items() if key != "packet_sha256"},
    ensure_ascii=False, sort_keys=True, separators=(",", ":")
).encode("utf-8")
assert digest(canonical) == packet["packet_sha256"]
assert digest(packet["lean"]["statement"].encode("utf-8")) == packet["lean"]["statement_sha256"]
assert packet["input_artifacts"] == ["lean-statement", "approved-definition-context"]

theorem_text = (
    "For every natural number d with d ≥ 1 and every real number κ with κ ≥ 4, "
    "work in the real Euclidean space ℝ^d with coordinates indexed by 0, …, d−1. "
    "Let A₁ = diag(κ, 1, …, 1), let ν₀ be the centered Gaussian probability measure "
    "with covariance I_d, and let ν₁ be the centered Gaussian probability measure "
    "with covariance A₁⁻¹ = diag(1/κ, 1, …, 1). "
    "When d = 1, these diagonal matrices consist only of their first entry.\n"
    "\n"
    "Define the closed slab B = {x ∈ ℝ^d : |x₀| ≤ 1/2}. Then\n"
    "\n"
    "ν₁(B) − ν₀(B) > 1/8.\n"
    "\n"
    "The Gaussian parameters above are covariances, so the first coordinate under ν₁ "
    "has variance 1/κ. Both measures have mean zero. The constants 1/2 and 1/8 "
    "are fixed and do not depend on d or κ.\n"
)
theorem_bytes = theorem_text.encode("utf-8")
create("reconstructed_theorem.md", theorem_bytes)

exposure = {
    "schema_version": 1,
    "decoder": IDENTITY,
    "input_artifacts": ["lean-statement", "approved-definition-context"],
    "source_text_visible": False,
    "source_identity_supplied": False,
    "source_identity_recognized": False,
    "actual_accidental_recognition": "None occurred. I did not recognize a specific source theorem or source identity from this packet.",
    "prior_mathematical_familiarity": "I have ordinary prior mathematical familiarity with finite-dimensional Gaussian distributions, diagonal matrices, covariance, and probability inequalities. This is not a claim of zero prior mathematical familiarity.",
    "consulted_material": ["The exact supplied input.json packet, including its literal Lean statement, approved definition context, metadata, non_disclosure, and output_contract."],
    "additional_source_material_consulted": [],
    "scope": "Mathematical reconstruction only; no source identification, proof, or fidelity judgment was performed."
}
exposure_bytes = json_bytes(exposure)
create("exposure.json", exposure_bytes)

event = {
    "schema_version": 1,
    "decoder": IDENTITY,
    "event": "artifact-generation-execution",
    "actual_command": "python3 /private/tmp/sr-pkt-aa8270/generate_artifacts.py",
    "process_id": os.getpid(),
    "started_at_utc": started,
    "completed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "input_artifacts": ["lean-statement", "approved-definition-context"],
    "source_text_visible": False,
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "packet_hash_rule": "SHA256 of UTF-8 JSON with sorted keys, compact separators, ensure_ascii=false, excluding only the top-level packet_sha256 field.",
    "generated_files": {
        "reconstructed_theorem.md": {"sha256": digest(theorem_bytes), "bytes": len(theorem_bytes)},
        "exposure.json": {"sha256": digest(exposure_bytes), "bytes": len(exposure_bytes)}
    },
    "text_sha256": digest(theorem_bytes),
    "result": "Both output files were created with exclusive creation; no existing artifact was overwritten."
}
event_bytes = json_bytes(event)
create("artifact_generation_event.json", event_bytes)
print(json.dumps({
    "event_file": str(BASE / "artifact_generation_event.json"),
    "event_sha256": digest(event_bytes),
    "text_sha256": digest(theorem_bytes),
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "status": "artifacts-created"
}, ensure_ascii=False, sort_keys=True))
