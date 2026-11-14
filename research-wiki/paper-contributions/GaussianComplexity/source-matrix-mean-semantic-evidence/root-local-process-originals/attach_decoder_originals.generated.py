"""Carry exact blind outputs and export a fresh anti-anchored review packet."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as semantic
import astis_publication as publication

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
phase = Path('.astis/semantic-neutral-20261112/n_decode_38df')
audit_path = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-mean.json')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


run_raw = (phase / 'run_transcript.json').read_bytes()
text_raw = (phase / 'reconstruction.md').read_bytes()
input_raw = (phase / 'input.json').read_bytes()
assert sha(run_raw) == 'c02e83f479f013440c6da7708d5a018a8dc38dba870cb7335932fe5656bd8383'
assert sha(text_raw) == '34b56baf21f85e6b49de73db76ad1e95ee14c56bb5602ac1fc6c9fb89bb0b358'
assert sha(input_raw) == 'e1dcc94907868ac4f28f0a0959d80947404cb7596451ec1ae90fe593d83f67e9'
run, packet = json.loads(run_raw), json.loads(input_raw)
assert run['decoder_identity'] == '/root/neutral_decode_38df'
assert run['source_text_visible'] is False
assert run['mathematical_evidentiary_input_count'] == 1 and run['sole_input']['raw_sha256'] == sha(input_raw)
assert run['sole_input']['packet_sha256_recomputed'] == packet['packet_sha256']
assert run['output_contract']['reconstructed_text_sha256'] == sha(text_raw)
assert run['inputs_and_exposure']['original_source_text_or_identity_read'] is False
assert run['inputs_and_exposure']['AGENTS_md_read'] is False
assert not run['reconstruction']['abridged']
assert run['output_contract']['reconstructed_theorem_text'] == text_raw.decode()
audit = json.loads(audit_path.read_bytes())
assert not audit['reconstruction'] and audit['verdict'] == 'pending'
assert sha(audit['lean']['statement'].encode()) == run['sole_input']['anonymous_statement_sha256_recomputed']
dest = evidence / 'decoder-originals/n_decode_38df'
for filename in ('input.json', 'reconstruction.md', 'run_transcript.json'):
    create(dest / filename, (phase / filename).read_bytes())
audit['state'] = 'blind-reconstructed'
audit['reconstruction'] = {
    'text': text_raw.decode(), 'text_sha256': sha(text_raw),
    'decoder': run['decoder_identity'], 'decoder_run_sha256': sha(run_raw),
    'decoder_packet_sha256': packet['packet_sha256'], 'source_text_visible': False,
    'lean_statement_sha256': run['sole_input']['anonymous_statement_sha256_recomputed'],
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
    'reconstruction_scope': 'The exact full frozen reconstruction.md is the canonical reconstruction. The run embeds that complete text without abridgment and binds its complete bytes. Final externally hashed run is carried without rewriting or an invented self-hash.',
    'independent_decoder': run['decoder_identity'], 'source_text_visible': False,
    'publication_binding_sha256': audit['publication_binding_sha256'],
    'anti_anchored_packet': str(review_path), 'anti_anchored_raw_sha256': sha(review_path.read_bytes()),
    'anti_anchored_packet_sha256': review['packet_sha256'], 'all_originals_unchanged': True,
}
create(evidence / 'decoder-original-custody.json', dump(record))
print(json.dumps(record))
