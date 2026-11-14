"""Carry exact blind outputs and export a fresh anti-anchored review packet."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as semantic
import astis_publication as publication

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
phase = Path('.astis/semantic-neutral-20261112/n_decode_9e31')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-row-independence.json')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


run_raw = (phase / 'run_transcript.json').read_bytes()
text_raw = (phase / 'reconstruction.md').read_bytes()
input_raw = (phase / 'input.json').read_bytes()
assert sha(run_raw) == 'f5946852ce343bfd40c2c44aaf93a282cbcc29f68bc2c11f175b4d75212718fb'
assert sha(text_raw) == '608361f0c4c0832a2724c49b2febc2733e87050dca19b18746a1b6012b7a2a8c'
assert sha(input_raw) == '6dea1b9d1fc2f203c16642cffd76ff0df8a29813121e51f157554dab3abf500a'
run, packet = json.loads(run_raw), json.loads(input_raw)
assert run['actor']['agent_task_path'] == '/root/neutral_decode_9e31'
assert run['source_text_visible'] is False
assert len(run['input_manifest']) == 1 and run['input_manifest'][0]['raw_input_sha256'] == sha(input_raw)
assert run['canonical_packet']['sha256'] == packet['packet_sha256']
assert run['output_contract']['reconstructed_text_sha256'] == sha(text_raw)
assert run['exposure_manifest']['source_identity_visible'] is False
assert run['exposure_manifest']['repository_protocol_or_AGENTS_read'] is False
audit = json.loads(audit_path.read_bytes())
assert not audit['reconstruction'] and audit['verdict'] == 'pending'
assert sha(audit['lean']['statement'].encode()) == run['input_manifest'][0]['anonymous_statement_sha256']
dest = evidence / 'decoder-originals/n_decode_9e31'
for filename in ('input.json', 'reconstruction.md', 'run_transcript.json'):
    create(dest / filename, (phase / filename).read_bytes())
audit['state'] = 'blind-reconstructed'
audit['reconstruction'] = {
    'text': text_raw.decode(), 'text_sha256': sha(text_raw),
    'decoder': run['actor']['agent_task_path'], 'decoder_run_sha256': sha(run_raw),
    'decoder_packet_sha256': packet['packet_sha256'], 'source_text_visible': False,
    'lean_statement_sha256': run['input_manifest'][0]['anonymous_statement_sha256'],
    'input_artifacts': ['lean-statement', 'approved-definition-context'],
    'run_artifact': str(dest / 'run_transcript.json'),
}
audit_path.write_bytes(dump(audit))
assert semantic.decoder_packet(audit) == packet
review = semantic.semantic_reviewer_packet(audit)
review_path = evidence / 'anti-anchored-reviewer-packet.json'
create(review_path, dump(review))
publication.check_advance([audit['lean']['declaration']], reviewed=False)
record = {
    'original_input_sha256': sha(input_raw), 'original_run_sha256': sha(run_raw),
    'original_reconstructed_file_sha256': sha(text_raw),
    'run_hash_convention': 'Exact original frozen run_transcript.json bytes, externally hashed; no replacement or self-excluding run.',
    'reconstruction_scope': 'The exact full frozen reconstruction.md including seven-slot discussion is the canonical reconstruction. The run separately quotes an abridged main theorem in its output contract and binds the full reconstruction file by its exact byte hash.',
    'independent_decoder': run['actor']['agent_task_path'], 'source_text_visible': False,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'anti_anchored_packet': str(review_path), 'anti_anchored_raw_sha256': sha(review_path.read_bytes()),
    'anti_anchored_packet_sha256': review['packet_sha256'], 'all_originals_unchanged': True,
}
create(evidence / 'decoder-original-custody.json', dump(record))
print(json.dumps(record))
