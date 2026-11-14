"""Carry two independent full anonymous reconstructions without rewriting their originals."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as semantic
import astis_publication as publication

base = Path('.astis/semantic-neutral-20261113/n_decode_mp_6a17')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda value: (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode()

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

configs = [
    ('a', '/root/neutral_decode_6a17', 'e9cdc1fd37c4d46d3eef39c1acda5be183d139376c5e7f0aa581af6d08be3dea', 'd603074344160f46d6282e33a6e1666b22bbe0c415692c2ea171ec03fef9673e', 'd6cfe3ae8e7c8aaa7603244477984a3e164b9eb38e87fb2a4dce18f5acd7516f', '85a2539d169df24cafed6795f274d67fac607451c1441172628e240ef9857665', 'huanjian-real-matrix-positive-integral', 'research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence'),
    ('b', '/root/neutral_decode_d204', '55db3b687c9579ec2ed7b784898f1d932a77b2d956a69befb10d4f7d41f90f2e', '4ac774369cb4172253000f5c71b7658584c9888657075b6349bbbf2a18518d26', '88a5f28bba17c0b74298cc57b1a4c2cd5020b18949ce78571858207004341bec', 'b14be6d1b668f73400172bf9d5b7fde416bfebafeddcd0069069217889cabd6e', 'huanjian-gaussian-source-matrix-variance', 'research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence'),
]
records, declarations = [], []
for label, actor, run_hash, text_hash, freeze_hash, input_hash, slug, evidence_name in configs:
    phase = base / (label + '-output')
    run_raw = (phase / 'decoder-run.json').read_bytes()
    text_raw = (phase / 'reconstruction.md').read_bytes()
    freeze_raw = (phase / 'freeze-manifest.json').read_bytes()
    input_raw = (base / (label + '.json')).read_bytes()
    assert [sha(x) for x in [run_raw, text_raw, freeze_raw, input_raw]] == [run_hash, text_hash, freeze_hash, input_hash]
    run, packet, freeze = json.loads(run_raw), json.loads(input_raw), json.loads(freeze_raw)
    assert run['decoder_identity'] == actor and run['mathematical_evidentiary_input_count'] == 1
    assert run['sole_input']['raw_sha256'] == sha(input_raw)
    assert run['sole_input']['packet_sha256_recomputed'] == packet['packet_sha256']
    assert run['inputs_and_exposure']['original_source_text_or_identity_read'] is False
    assert run['inputs_and_exposure']['AGENTS_md_read'] is False
    assert run['output_contract']['source_text_visible'] is False
    assert run['output_contract']['decoder_run_sha256'] == ''
    assert run['output_contract']['reconstructed_theorem_text'] == text_raw.decode()
    assert run['output_contract']['reconstructed_text_sha256'] == sha(text_raw)
    assert run['reconstruction']['abridged'] is False
    assert all(run['output_contract'][slot].strip() for slot in ['objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies'])
    items = freeze.get('files', [freeze.get('decoder_run'), freeze.get('reconstruction')])
    for item in items:
        raw = Path(item['path']).read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    evidence = Path(evidence_name)
    dest = evidence / 'decoder-originals' / actor.split('/')[-1]
    for filename, raw in [('input.json', input_raw), ('reconstruction.md', text_raw), ('decoder-run.json', run_raw), ('freeze-manifest.json', freeze_raw)]:
        create(dest / filename, raw)
    audit_path = Path('research-wiki/semantic-roundtrip/audits') / (slug + '.json')
    audit = json.loads(audit_path.read_bytes())
    assert not audit['reconstruction'] and audit['verdict'] == 'pending'
    assert sha(audit['lean']['statement'].encode()) == run['sole_input']['anonymous_statement_sha256_recomputed']
    audit['state'] = 'blind-reconstructed'
    audit['reconstruction'] = {'text': text_raw.decode(), 'text_sha256': sha(text_raw), 'decoder': actor, 'decoder_run_sha256': sha(run_raw), 'decoder_packet_sha256': packet['packet_sha256'], 'source_text_visible': False, 'lean_statement_sha256': run['sole_input']['anonymous_statement_sha256_recomputed'], 'input_artifacts': ['lean-statement', 'approved-definition-context'], 'run_artifact': str(dest / 'decoder-run.json')}
    audit_path.write_bytes(dump(audit))
    assert semantic.decoder_packet(audit) == packet
    review = semantic.semantic_reviewer_packet(audit)
    review_path = evidence / 'anti-anchored-reviewer-packet.json'
    create(review_path, dump(review))
    record = {'independent_decoder': actor, 'original_input_sha256': sha(input_raw), 'original_run_sha256': sha(run_raw), 'original_reconstructed_file_sha256': sha(text_raw), 'original_freeze_manifest_sha256': sha(freeze_raw), 'source_text_visible': False, 'full_unabridged_text_embedded_exactly': True, 'run_hash_convention': 'Externally hashed completed original decoder-run.json, blank self-hash retained; no rewrite or abridgment.', 'publication_binding_sha256': audit['publication_binding_sha256'], 'anti_anchored_packet': str(review_path), 'anti_anchored_raw_sha256': sha(review_path.read_bytes()), 'anti_anchored_packet_sha256': review['packet_sha256'], 'all_originals_unchanged': True}
    create(evidence / 'decoder-original-custody.json', dump(record))
    declarations.append(audit['lean']['declaration'])
    records.append(record)
publication.check_advance(declarations, reviewed=False)
print(json.dumps({'independent_original_decoder_records': records, 'root_fidelity_verdicts': 0, 'normal_VERIFIED_calls': 0}))
