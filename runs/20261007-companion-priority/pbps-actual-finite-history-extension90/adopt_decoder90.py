from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
OUT = ROOT / "runs/semantic-decoder-outputs/round90"
sys.path.insert(0, str(ROOT / "tools"))
import astis_semantic_roundtrip as rt

def load(p):
    return json.loads(p.read_bytes())

def sha(b):
    return hashlib.sha256(b).hexdigest()

expected = {
    "decoder-run.json": "b4134e2f1891da784d224913c4e66ffe1bcbfd1c25386bb599102b8064070c98",
    "reconstruction.json": "4ebb21a3620b4ccc2326771f4b1f26da5a87092e46eff283520718560e696df9",
    "manifest.json": "eeacc7307084efcfc31f50eea30fefc721badf929752a55b5baf353e55c0febb",
}
for name, digest in expected.items():
    assert sha((OUT / name).read_bytes()) == digest, name
manifest = load(OUT / "manifest.json")
native = load(OUT / "reconstruction.json")
run = load(OUT / "decoder-run.json")
packet = load(RUN / "anonymous.decoder90.json")
assert manifest["input_set_closed"] and manifest["output_set_closed"]
assert set(manifest["closed_output_set"]) == set(expected)
for item in manifest["inputs"] + manifest["outputs"]:
    b = Path(item["path"]).read_bytes()
    assert sha(b) == item["raw_sha256"] and len(b) == item["bytes"], item["path"]
assert len(run["input_reads"]) == 1 and not run["extra_mathematical_inputs"]
inp = run["input_reads"][0]
assert inp["raw_sha256"] == sha((RUN / "anonymous.decoder90.json").read_bytes()) == "33a8f6024e3073d0c74d5749029c67ffc7632d3b4ebdeffdc6893da9fd5162a0"
assert not native["source_text_visible"]
assert all(value is False for value in run["disclosure_flags"].values())
assert run["canonical_packet_hash_check"]["verified"]
assert packet["packet_sha256"] == rt.sha256_json({k: v for k, v in packet.items() if k != "packet_sha256"})
assert native["decoder_run_sha256"] == expected["decoder-run.json"]
text = native["reconstructed_theorem_text"]
assert sha(text.encode()) == native["reconstructed_text_sha256"] == manifest["reconstructed_text_utf8_sha256"]
assert native["semantic_uncertainties"] == run["semantic_uncertainties"]
ap = ROOT / "research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json"
a = load(ap)
assert a["state"] == "draft" and rt.decoder_packet(a) == packet
assert a["lean"]["statement_sha256"] == manifest["statement_utf8_sha256"]
snapshot = RUN / "audit.before-decoder90.json"
assert not snapshot.exists()
snapshot.write_bytes(ap.read_bytes())
a.update(state="blind-reconstructed", reconstruction={
    "text": text, "text_sha256": native["reconstructed_text_sha256"],
    "decoder": native["decoder"]["identity"], "decoder_run_sha256": native["decoder_run_sha256"],
    "decoder_packet_sha256": packet["packet_sha256"], "source_text_visible": False,
    "lean_statement_sha256": a["lean"]["statement_sha256"], "input_artifacts": packet["input_artifacts"],
    "observed_input_artifacts": [{"path": inp["path"], "raw_sha256": inp["raw_sha256"]}],
    "run_artifact": (OUT / "decoder-run.json").relative_to(ROOT).as_posix(),
    "native_named_payload_sha256": expected["reconstruction.json"],
    "native_run_manifest_RAW_sha256": expected["manifest.json"],
    "unresolved_semantics": [], "native_semantic_uncertainties": native["semantic_uncertainties"],
    "native_structured_payload": (OUT / "reconstruction.json").relative_to(ROOT).as_posix(),
    "run_hash_recipe": "Exact native decoder-run bytes plus anonymous RAW input and independently closed native manifest. Canonical packet hash separately verified. Native infimum-attainment/source-fidelity/unconditional-path limitations are retained verbatim for the final source reviewer."
})
ap.write_text(json.dumps(a, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
record = {
    "status": "BLIND_RECONSTRUCTION_ADOPTED_ONLY", "decoder": native["decoder"]["identity"],
    "native_manifest_RAW_sha256": expected["manifest.json"], "packet_sha256": packet["packet_sha256"],
    "raw_packet_sha256": inp["raw_sha256"], "reconstructed_text_utf8_sha256": native["reconstructed_text_sha256"],
    "native_semantic_uncertainties_preserved": native["semantic_uncertainties"],
    "classification": "Decoder retained literal infimum and made no attainment, source-fidelity, unconditional normalization or infinite-path claim. The final independent source reviewer must compare the complete reconstruction and its limitations.",
    "source_verdict": False, "VERIFIED": False
}
target = RUN / "root.decoder90.adoption.json"
assert not target.exists()
target.write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
print("Native90 blind reconstruction adopted; no source-fidelity or VERIFIED credit.")
