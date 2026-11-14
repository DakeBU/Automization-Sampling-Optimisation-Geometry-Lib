import datetime
import hashlib
import json
import os
import stat
from pathlib import Path

BASE = Path("/private/tmp/sr-pkt-aa8270")
IDENTITY = "/root/neutral_decoder_aa8270"
EXPECTED_RAW = "d5e384030e996b85c33402b5855968d32b9045791d4d6ce710d3f58027e64e0d"
ACTUAL_TOOL_RECEIPT = json.loads("{\"tool\":\"functions.exec -> tools.exec_command\",\"arguments\":{\"cmd\":\"python3 /private/tmp/sr-pkt-aa8270/generate_artifacts.py\",\"max_output_tokens\":1500},\"result\":{\"chunk_id\":\"253e4b\",\"wall_time_seconds\":0.000008875,\"exit_code\":0,\"original_token_count\":112,\"output\":\"{\\\"event_file\\\": \\\"/private/tmp/sr-pkt-aa8270/artifact_generation_event.json\\\", \\\"event_sha256\\\": \\\"951e47063dfac5c8f8ebd768891aa43f30ecc0dcaffe23559ae072cf2592d2cc\\\", \\\"packet_sha256\\\": \\\"c54ff851447010351fc5d14f3c05178becdbad0944bdbb515feb22ae8b0479da\\\", \\\"raw_input_sha256\\\": \\\"d5e384030e996b85c33402b5855968d32b9045791d4d6ce710d3f58027e64e0d\\\", \\\"status\\\": \\\"artifacts-created\\\", \\\"text_sha256\\\": \\\"00f1434c843913852af29594943b6cde780b22028f198e245322bb37fd4ce27a\\\"}\\n\"}}")

def digest(data):
    return hashlib.sha256(data).hexdigest()

def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def create(name, data):
    with (BASE / name).open("xb") as handle:
        handle.write(data)

raw = (BASE / "input.json").read_bytes()
assert digest(raw) == EXPECTED_RAW
assert stat.S_IMODE((BASE / "input.json").stat().st_mode) == 0o444
packet = json.loads(raw)
canonical = json.dumps(
    {key: value for key, value in packet.items() if key != "packet_sha256"},
    sort_keys=True, separators=(",", ":"), ensure_ascii=False
).encode("utf-8")
assert digest(canonical) == packet["packet_sha256"]
assert packet["input_artifacts"] == ["lean-statement", "approved-definition-context"]

text_bytes = (BASE / "reconstructed_theorem.md").read_bytes()
exposure_bytes = (BASE / "exposure.json").read_bytes()
event_bytes = (BASE / "artifact_generation_event.json").read_bytes()
event = json.loads(event_bytes)
observed = json.loads(ACTUAL_TOOL_RECEIPT["result"]["output"])
assert ACTUAL_TOOL_RECEIPT["result"]["exit_code"] == 0
assert ACTUAL_TOOL_RECEIPT["arguments"]["cmd"] == event["actual_command"]
assert observed["event_sha256"] == digest(event_bytes)
assert observed["text_sha256"] == digest(text_bytes)
assert event["generated_files"]["exposure.json"]["sha256"] == digest(exposure_bytes)
assert event["raw_input_sha256"] == digest(raw)
assert event["packet_sha256"] == digest(canonical)

execution_receipt = {
    "schema_version": 1,
    "decoder": IDENTITY,
    "receipt_kind": "Recorded result of the completed artifact-generation tool execution",
    "actual_tool_receipt": ACTUAL_TOOL_RECEIPT,
    "artifact_generation_event_sha256": digest(event_bytes),
    "generator_sha256": digest((BASE / "generate_artifacts.py").read_bytes()),
    "input_artifacts": ["lean-statement", "approved-definition-context"],
    "source_text_visible": False,
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "text_sha256": digest(text_bytes)
}
execution_bytes = json_bytes(execution_receipt)
create("artifact_generation_execution_receipt.json", execution_bytes)

decoder_run = {
    "schema_version": 1,
    "decoder": IDENTITY,
    "task": "blind-theorem-reconstruction",
    "packet_id": packet["packet_id"],
    "input_artifacts": ["lean-statement", "approved-definition-context"],
    "source_text_visible": False,
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "packet_hash_rule": "SHA256 of UTF-8 JSON with sorted keys, compact separators, ensure_ascii=false, excluding only the top-level packet_sha256 field.",
    "lean_statement_sha256": digest(packet["lean"]["statement"].encode("utf-8")),
    "text_sha256": digest(text_bytes),
    "run_hash": digest(execution_bytes),
    "run_hash_basis": "SHA256 of the exact bytes of artifact_generation_execution_receipt.json, recording the actual completed generator command and its tool result.",
    "execution_receipt_file": "artifact_generation_execution_receipt.json",
    "artifact_generation_event_file": "artifact_generation_event.json",
    "artifact_generation_event_sha256": digest(event_bytes),
    "exposure_sha256": digest(exposure_bytes),
    "method": "Independent natural-language reconstruction from the literal Lean proposition and approved minimal definition context. No source identification, fidelity verdict, or proof assessment.",
    "artifact_write_policy": "Exclusive creation only; no earlier artifact bytes overwritten."
}
run_bytes = json_bytes(decoder_run)
create("decoder_run.json", run_bytes)

reconstruction = {
    "reconstructed_theorem_text": text_bytes.decode("utf-8"),
    "reconstructed_text_sha256": digest(text_bytes),
    "objects": "The identity matrix I_d; the diagonal real matrix A₁ whose coordinate-0 diagonal entry is κ and whose other diagonal entries are 1; their actual matrix inverses; the centered Gaussian probability measures ν₀ with covariance I_d⁻¹ = I_d and ν₁ with covariance A₁⁻¹ = diag(1/κ, 1, …, 1); the closed coordinate slab B = {x : |x₀| ≤ 1/2}; and the ordinary real probabilities ν₀(B) and ν₁(B).",
    "domains": "d ranges over natural numbers satisfying d ≥ 1. κ ranges over real numbers satisfying κ ≥ 4. Coordinates are indexed by Fin d = {0, …, d−1}; vectors lie in the real Euclidean space ℝ^d with its Borel sigma-algebra. Matrices are d-by-d real matrices. The probability measures are on that Euclidean space. All fractions and the final inequality are real-valued.",
    "quantifiers": "For every natural number d and every proof hd of 1 ≤ d, and for every real number κ and every proof hκ of 4 ≤ κ, the conclusion holds for the locally defined A₁, ν₀, ν₁, and B. The x in the definition of B is bound by set comprehension. No existential choice or further universal parameter occurs.",
    "assumptions": "The only numerical assumptions are 1 ≤ d and 4 ≤ κ. The first makes coordinate 0 available; the second implies κ > 0 and hence that A₁ is positive definite and nonsingular. The approved Gaussian definition then gives the stated centered probability measures and covariances. These consequences are not additional hypotheses.",
    "conclusion": "The ν₁-probability of |x₀| ≤ 1/2 minus the ν₀-probability of the same event is strictly greater than 1/8: ν₁(B) − ν₀(B) > 1/8. In particular, both event masses are real probabilities, with the order of subtraction as displayed.",
    "scopes": "The universal d, hd, κ, and hκ enclose all four local let definitions and the final inequality. A₁ is defined before and used in ν₁. ν₀ uses the inverse identity covariance, ν₁ uses the inverse A₁ covariance, and B uses coordinate 0 justified by hd. The slab bound includes its endpoints because its inequality is ≤. The final mass comparison is strict. When d = 1, no remaining diagonal coordinates occur.",
    "constant_dependencies": "The slab half-width 1/2, probability gap 1/8, dimension lower bound 1, and parameter lower bound 4 are fixed numerical constants. The gap 1/8 and width 1/2 are independent of d and κ. A₁ and ν₁ depend on d and κ, while ν₀ depends only on d; B depends only on the ambient d-coordinate space and its designated first coordinate. ν₁ has first-coordinate variance 1/κ, not standard deviation 1/κ.",
    "decoder": IDENTITY,
    "decoder_run_sha256": digest(run_bytes),
    "source_text_visible": False
}
assert set(reconstruction) == set(packet["output_contract"])
for key, template in packet["output_contract"].items():
    assert type(reconstruction[key]) is type(template), key
assert reconstruction["reconstructed_text_sha256"] == digest(reconstruction["reconstructed_theorem_text"].encode("utf-8"))
reconstruction_bytes = json_bytes(reconstruction)
create("reconstruction.json", reconstruction_bytes)

names = [
    "input.json",
    "generate_artifacts.py",
    "freeze_artifacts.py",
    "reconstructed_theorem.md",
    "exposure.json",
    "artifact_generation_event.json",
    "artifact_generation_execution_receipt.json",
    "decoder_run.json",
    "reconstruction.json"
]
manifest = []
for name in names:
    path = BASE / name
    content = path.read_bytes()
    os.chmod(path, 0o444)
    assert stat.S_IMODE(path.stat().st_mode) == 0o444
    manifest.append({
        "path": str(path),
        "name": name,
        "bytes": len(content),
        "sha256": digest(content),
        "mode": "0444"
    })
freeze_receipt = {
    "schema_version": 1,
    "decoder": IDENTITY,
    "frozen_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "freeze_command": "python3 /private/tmp/sr-pkt-aa8270/freeze_artifacts.py",
    "process_id": os.getpid(),
    "input_artifacts": ["lean-statement", "approved-definition-context"],
    "source_text_visible": False,
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "text_sha256": digest(text_bytes),
    "run_hash": digest(execution_bytes),
    "decoder_run_sha256": digest(run_bytes),
    "artifacts": manifest,
    "receipt_self_excluded": True,
    "receipt_self_exclusion_reason": "The receipt excludes its own bytes and digest to avoid a hash cycle; its digest is reported by the completed tool execution.",
    "artifact_write_policy": "All new files were created exclusively; no earlier artifact bytes were overwritten. The input bytes remain unchanged."
}
freeze_bytes = json_bytes(freeze_receipt)
create("freeze_receipt.json", freeze_bytes)
os.chmod(BASE / "freeze_receipt.json", 0o444)

for entry in manifest:
    path = BASE / entry["name"]
    assert digest(path.read_bytes()) == entry["sha256"]
    assert stat.S_IMODE(path.stat().st_mode) == 0o444
assert digest((BASE / "input.json").read_bytes()) == EXPECTED_RAW
assert stat.S_IMODE((BASE / "freeze_receipt.json").stat().st_mode) == 0o444
print(json.dumps({
    "status": "frozen-and-verified",
    "decoder": IDENTITY,
    "raw_input_sha256": digest(raw),
    "packet_sha256": digest(canonical),
    "text_sha256": digest(text_bytes),
    "run_hash": digest(execution_bytes),
    "decoder_run_sha256": digest(run_bytes),
    "artifacts": manifest,
    "freeze_receipt": {
        "path": str(BASE / "freeze_receipt.json"),
        "bytes": len(freeze_bytes),
        "sha256": digest(freeze_bytes),
        "mode": "0444"
    }
}, ensure_ascii=False, indent=2))
