from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79');d=Path('.astis/decoder-79/result')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
response=load(d/'decoded.json');m=load(d/'run-manifest.json');packet=load('.astis/decoder-79/packet.json')
assert m['packet_canonical_sha256']==packet['packet_sha256']
assert m['packet_raw_sha256']==sha(Path('.astis/decoder-79/packet.json').read_bytes())
assert rt.sha256_json({k:v for k,v in m.items() if k not in ['decoder_run_sha256','decoder_run_hash_algorithm','output_artifacts']})==m['decoder_run_sha256']==response['decoder_run_sha256']
assert rt.sha256_json({k:v for k,v in response.items() if k!='decoder_run_sha256'})==m['semantic_payload_sha256']
assert all(m[k] is False for k in ['source_seen','identity_seen','proof_BODY_seen'])
assert set(m['seven_slots'])==set(rt.SEMANTIC_SLOTS) and all(response[k] for k in rt.SEMANTIC_SLOTS)
for item in m['output_artifacts']:assert sha(Path(item['path']).read_bytes())==item['raw_sha256']
text=response['reconstructed_theorem_text'];assert sha(text.encode())==m['reconstructed_text_sha256']
archive=r/'anonymous-decoder79';archive.mkdir(exist_ok=False)
for p in d.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-79/packet.json').read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeCover.json');a=load(ap);assert rt.decoder_packet(a)==packet
(r/'audit.before-decoder79.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=m['reconstructed_text_sha256'],decoder=response['decoder'],decoder_run_sha256=m['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=m['mathematical_inputs'],run_artifact=(archive/'run-manifest.json').as_posix(),native_named_payload_sha256=sha((d/'decoded.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),unresolved_semantics=[],run_hash_recipe=m['decoder_run_hash_algorithm']))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review79.packet.json',review)
save(r/'root.decoder79.adoption.json',dict(status='INDEPENDENT_BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=response['decoder'],native_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind adopted; canonical reviewer packet',review['packet_sha256'])
