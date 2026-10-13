from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78');d=Path('.astis/decoder-78/response')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
response=load(d/'response.json');manifest=load(d/'run-manifest.json');packet=load('.astis/decoder-78/packet.json')
assert sha((d/'response.json').read_bytes())=='4c8ae475773996cd7ba8799732411baa77d8755b00653a260f531fe63dec9099'
assert sha((d/'run-manifest.json').read_bytes())=='b991a8eac036169588d9fad419dd6d74c7e25a5df84fc22c99dabf00c7ac6f64'
for group in ['input_artifacts','output_artifacts']:
 for p in manifest[group]: assert sha(Path(p['path']).read_bytes())==p['raw_sha256']
assert response['decoder_packet_sha256']==packet['packet_sha256']
assert all(response[k] is False for k in ['source_text_visible','source_identity_visible','proof_BODY_visible'])
assert set(response['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
text=response['reconstructed_theorem'];assert sha(text.encode())==response['reconstructed_text_sha256']
archive=r/'anonymous-decoder78';archive.mkdir(exist_ok=False)
for p in d.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-78/packet.json').read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualNonaccumulation.json');a=load(ap)
assert rt.decoder_packet(a)==packet
(r/'audit.before-decoder78.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=response['reconstructed_text_sha256'],decoder=response['decoder'],decoder_run_sha256=sha((d/'run-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=manifest['input_artifacts'],run_artifact=(archive/'run-manifest.json').as_posix(),native_named_payload_sha256=sha((d/'response.json').read_bytes()),unresolved_semantics=[],run_hash_recipe='SHA256 of immutable native run-manifest RAW bytes; response and input/output hashes checked.'))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review78.packet.json',review)
save(r/'root.decoder78.adoption.json',dict(status='INDEPENDENT_BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=response['decoder'],native_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind decoder adopted; canonical anti-anchored reviewer packet',review['packet_sha256'])
