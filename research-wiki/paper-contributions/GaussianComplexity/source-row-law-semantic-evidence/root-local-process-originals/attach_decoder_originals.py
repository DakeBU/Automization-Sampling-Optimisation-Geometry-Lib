"""Attach the exact independent blind originals and export a fresh reviewer packet."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as semantic
import astis_publication as publication

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
phase = Path('.astis/semantic-neutral-20261112/rl_decode_74bf')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-law.json')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda value: (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()
canonical = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


run_raw = (phase / 'run.json').read_bytes()
text_raw = (phase / 'reconstruction.md').read_bytes()
manifest_raw = (phase / 'exposure-input-manifest.json').read_bytes()
assert sha(run_raw) == '6b3e3d3f56b1e31ded3f1eab52f89679f6bb6252f3909a8f9606db4f9d0e2919'
assert sha(text_raw) == '926ca853e5687aaa6457b7fcd68848eab46c857fd38f08804fe4d8af31c61fb7'
assert sha(manifest_raw) == 'b6c6dd2163260b6e17ec75cadbc442a9ff8f273cac36f7764a219fd23eeb8082'
run = json.loads(run_raw)
manifest = json.loads(manifest_raw)
input_raw = (phase / 'input.json').read_bytes()
packet = json.loads(input_raw)
assert run['input_raw_sha256'] == sha(input_raw)
assert run['packet_sha256'] == packet['packet_sha256']
assert run['input_canonical_json_sha256'] == sha(canonical(packet))
assert run['decoder_run_sha256'] == sha(canonical({k:v for k,v in run.items() if k != 'decoder_run_sha256'}))
assert run['actor_id'] == '/root/neutral_decode_74bf'
assert run['source_text_visible'] is False and run['input_reads'] == 1
assert run['reconstructed_theorem_text'].encode() == text_raw
assert run['reconstructed_text_sha256'] == sha(text_raw)
assert manifest['actor_id'] == run['actor_id'] and manifest['source_text_visible'] is False
audit = json.loads(audit_path.read_bytes())
assert not audit['reconstruction'] and audit['verdict'] == 'pending'
assert sha(audit['lean']['statement'].encode()) == run['lean_statement_sha256']
destination = evidence / 'decoder-originals/rl_decode_74bf'
for filename in ('input.json', 'reconstruction.md', 'run.json', 'exposure-input-manifest.json'):
    create(destination / filename, (phase / filename).read_bytes())
audit['state'] = 'blind-reconstructed'
audit['reconstruction'] = {
    'text': text_raw.decode(), 'text_sha256': sha(text_raw),
    'decoder': run['actor_id'], 'decoder_run_sha256': sha(run_raw),
    'decoder_packet_sha256': packet['packet_sha256'], 'source_text_visible': False,
    'lean_statement_sha256': run['lean_statement_sha256'],
    'input_artifacts': ['lean-statement', 'approved-definition-context'],
    'run_artifact': str(destination / 'run.json'),
}
audit_path.write_bytes(dump(audit))
assert semantic.decoder_packet(audit) == packet
review_packet = semantic.semantic_reviewer_packet(audit)
review_path = evidence / 'anti-anchored-reviewer-packet.json'
create(review_path, dump(review_packet))
publication.check_advance([audit['lean']['declaration']], reviewed=False)
record = {
    'original_input_sha256': sha(input_raw), 'original_run_raw_sha256': sha(run_raw),
    'original_run_actor_canonical_sha256': run['decoder_run_sha256'],
    'original_reconstructed_text_sha256': sha(text_raw), 'original_manifest_sha256': sha(manifest_raw),
    'all_originals_unchanged': True,
    'canonical_audit_run_hash_convention': 'SHA256 of exact original frozen run.json bytes. The actor internal canonical-without-self hash is separately preserved and verified; no replacement decoder run is authored.',
    'independent_decoder': run['actor_id'], 'source_text_visible': False,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'anti_anchored_packet': str(review_path), 'anti_anchored_raw_sha256': sha(review_path.read_bytes()),
    'anti_anchored_packet_sha256': review_packet['packet_sha256'],
}
create(evidence / 'decoder-original-custody.json', dump(record))
print(json.dumps(record))
