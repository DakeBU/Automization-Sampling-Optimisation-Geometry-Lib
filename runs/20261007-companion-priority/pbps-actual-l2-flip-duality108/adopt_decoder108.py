from pathlib import Path
import hashlib, json, sys

r = Path(__file__).parent
sys.path.insert(0, str(Path.cwd() / 'tools'))
import astis_semantic_roundtrip as rt
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def save(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

ap = Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualL2FlipDuality.json')
a = load(ap)
folder = Path('runs/semantic-roundtrip/anonymous108/decoder-native')
v, run, packet = [load(p) for p in [folder/'decoder.json', folder/'manifest.json', folder.parent/'input.json']]
assert a['state'] == 'draft' and 'reconstruction' not in a
assert run['decoder'] == 'independent-source-blind-decoder:/root/blind_decoder108'
assert all(run[k] is False for k in ['source_text_visible','source_identity_visible','source_anchor_visible','source_theorem_number_visible','source_facing_declaration_identity_visible','previous_audit_visible','source_semantic_audit_visible','fidelity_verdict_visible','repair_visible','repair_proposal_visible'])
assert run['input']['raw_sha256'] == sha((folder.parent/'input.json').read_bytes())
assert run['input']['packet_sha256'] == packet['packet_sha256'] == rt.decoder_packet(a)['packet_sha256']
assert v['statement_sha256'] == a['lean']['statement_sha256']
for path, info in run['outputs'].items():
    assert sha((folder/path).read_bytes()) == info['raw_sha256']
before = r/'audit-before-decoder108.json'
assert not before.exists()
before.write_bytes(ap.read_bytes())
text = (folder/'reconstructed-theorem.txt').read_text(encoding='utf8')
a['reconstruction'] = dict(text=text, text_sha256=sha(text.encode()), decoder=run['decoder'], decoder_run_sha256=sha((folder/'manifest.json').read_bytes()), decoder_packet_sha256=packet['packet_sha256'], source_text_visible=False, lean_statement_sha256=a['lean']['statement_sha256'], input_artifacts=['lean-statement','approved-definition-context'], observed_input_artifacts=[dict(path=(folder.parent/'input.json').as_posix(),raw_sha256=run['input']['raw_sha256'])], run_artifact=(folder/'manifest.json').as_posix(), native_structured_payload=(folder/'decoder.json').as_posix(), native_named_payload_sha256=sha((folder/'decoder.json').read_bytes()), native_semantic_slots=v)
save(ap,a)
save(r/'decoder-admission108.json', dict(decoder_native=(folder/'decoder.json').as_posix(), decoder_run_raw_sha256=sha((folder/'manifest.json').read_bytes()), packet_sha256=packet['packet_sha256'], publication_binding_sha256=a['publication_binding_sha256'], source_verdict='pending', reviewer_packet='Fresh final packet after independently accepted header/source topology; no implementation route change.'))
print('Adopted exact native blind output; source verdict remains pending.')
