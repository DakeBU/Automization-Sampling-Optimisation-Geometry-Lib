from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');d=Path('.astis/decoder-80/result')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
response=load(d/'decoded.json');m=load(d/'run-manifest.json');packet=load('.astis/decoder-80/packet.json')
assert sha((d/'decoded.json').read_bytes())=='fd8e822d338d201cfce68a47ecf0b7fc0a78adf7a4ee5206a10a26a2b69e855b'
assert sha((d/'run-manifest.json').read_bytes())=='e68eab248536468e2e580d2d2176d6d60cbc66d5e57bbb244e649fb443447032'
assert m['core']['input_artifact']['canonical_packet_sha256']==packet['packet_sha256']==response['decoder_packet_sha256']
assert m['core']['input_artifact']['raw_sha256']==sha(Path('.astis/decoder-80/packet.json').read_bytes())==response['decoder_packet_raw_sha256']
assert rt.sha256_json(m['core'])==m['decoder_run_sha256']==response['decoder_run_sha256']
for key in ['source_text_visible','source_identity_visible','proof_BODY_visible']:assert m['core'][key] is False and response[key] is False
assert all(isinstance(response[k],str) and response[k].strip() for k in rt.SEMANTIC_SLOTS)
for x in m['output_artifacts'].values():assert sha(Path(x['path']).read_bytes())==x['raw_sha256']
text=response['reconstructed_theorem_text'];assert text==response['reconstructed_theorem'];assert sha(text.encode())==response['reconstructed_text_sha256']==m['core']['reconstructed_theorem_utf8_sha256']
archive=r/'anonymous-decoder80';archive.mkdir(exist_ok=False)
for p in d.rglob('*'):
 if p.is_file():
  target=archive/p.relative_to(d);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-80/packet.json').read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeMeasurability.json');a=load(ap);assert rt.decoder_packet(a)==packet
(r/'audit.before-decoder80.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=response['reconstructed_text_sha256'],decoder=response['decoder'],decoder_run_sha256=m['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=[m['core']['input_artifact']],run_artifact=(archive/'run-manifest.json').as_posix(),native_named_payload_sha256=sha((d/'decoded.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),unresolved_semantics=[],run_hash_recipe=m['hash_recipe']))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review80.packet.json',review)
save(r/'root.decoder80.adoption.json',dict(status='INDEPENDENT_BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=response['decoder'],native_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind adopted; canonical reviewer packet',review['packet_sha256'])
