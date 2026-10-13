import copy
import datetime
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))
import astis_publication as pub
import astis_semantic_roundtrip as rt

def load(p):
    return json.loads(p.read_bytes())

def sha(b):
    return hashlib.sha256(b).hexdigest()

def pin(p):
    return {"path": p.relative_to(ROOT).as_posix(), "raw_sha256": sha(p.read_bytes()), "bytes": p.stat().st_size}

def fresh(p, obj):
    assert not p.exists(), p
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")

seen = []
def verify(obj):
    if isinstance(obj, dict):
        digest = obj.get("raw_sha256", obj.get("sha256"))
        if "path" in obj and digest:
            p = Path(obj.get("closed_snapshot", obj["path"]))
            p = p if p.is_absolute() else ROOT / p
            assert sha(p.read_bytes()) == digest, p
            if "bytes" in obj:
                assert p.stat().st_size == obj["bytes"], p
            seen.append(str(p))
        for value in obj.values():
            verify(value)
    elif isinstance(obj, list):
        for value in obj:
            verify(value)

review = RUN / "independent-exposition-repair90"
dp, mp = review / "decision90.native.json", review / "closed-raw-manifest90.json"
assert sha(dp.read_bytes()) == "fec067eeb31ccddc42dca9c971f0c6ada7022e1f3633f77c436d620c40232bdf"
assert sha(mp.read_bytes()) == "d84d81f127d5f9e4d4db4b48c32b7c1d627d9033db444fc5f87f7434160b193c"
verify(load(mp))
decision = load(dp)
verify(decision)
assert decision["decision"] == "ACCEPT_EXACT_TWO_FIELD_EXPOSITION90_REPAIR"
assert not decision["required_repairs"]
assert decision["distinct_from_proposer77_root_formalizer_and_source_graph_creator87"]
proposal = load(Path(decision["exact_proposal"]["path"]))
verify(proposal)
assert set(decision["accepted_pointers"]) == {"/units/0/steps/0/formula", "/items/0/formulae/0/tex"}
changes = []
for change in proposal["changes"]:
    target = ROOT / change["target"]["path"]
    candidate = ROOT / change["proposed"]["path"]
    old, updated = load(target), load(candidate)
    expected = copy.deepcopy(old)
    tokens = change["pointer"].strip("/").split("/")
    obj = expected
    for token in tokens[:-1]:
        obj = obj[int(token)] if isinstance(obj, list) else obj[token]
    key = int(tokens[-1]) if isinstance(obj, list) else tokens[-1]
    assert obj[key] == change["before"]
    obj[key] = change["after"]
    assert expected == updated, target
    changes.append((target, candidate, change["pointer"]))
ap = ROOT / "research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json"
module = ROOT / "AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean"
assert sha(module.read_bytes()) == "6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029"
a = load(ap)
before_packet = rt.decoder_packet(a)
assert a["state"] == "blind-reconstructed" and before_packet == load(RUN / "anonymous.decoder90.json")
snapshot = RUN / "audit.before-exposition90.json"
assert not snapshot.exists()
snapshot.write_bytes(ap.read_bytes())
for target, candidate, pointer in changes:
    target.write_bytes(candidate.read_bytes())
pub.inputs.cache_clear()
pub.load.cache_clear()
pp = ROOT / "website/content/publications/pbps-actual-finite-history-extension.json"
lp = ROOT / "website/content/declaration_lessons/pbps-actual-finite-history-extension.json"
item = load(pp)["items"][0]
a["publication_binding_sha256"] = pub.binding_digest(item, item["bindings"][0], pub.inputs())
a["publication_context"] = pub.review_context(item, item["bindings"][0], pub.inputs())
assert rt.decoder_packet(a) == before_packet
ap.write_text(json.dumps(a, ensure_ascii=False, indent=2)+"\n", encoding="utf-8", newline="\n")
pub.check_advance([a["lean"]["declaration"]], reviewed=False)
fresh(RUN / "publication-freeze90.after-exposition.json", {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "status": "DISTINCT_EXACT_TWO_FIELD_EXPOSITION_APPLIED_FINAL_SOURCE_REVIEW_PENDING",
    "inputs": [pin(p) for p in [lp, pp, ap, dp, mp]], "module": pin(module),
    "predecessor": pin(RUN / "publication-freeze90.json"),
    "publication_binding_sha256": a["publication_binding_sha256"],
    "decoder_packet_unchanged": True, "repaired_pointers": decision["accepted_pointers"],
    "checked_RAW_descriptors": len(seen), "PROVED_LOCAL": False, "VERIFIED": False
})
fresh(RUN / "source-review90.packet.json", rt.semantic_reviewer_packet(a))
print(json.dumps({"status": "DISTINCT_REPAIR_APPLIED",
    "publication_binding_sha256": a["publication_binding_sha256"],
    "checked_RAW_descriptors": len(seen), "decoder_packet_unchanged": True,
    "source_packet": pin(RUN / "source-review90.packet.json")}))
