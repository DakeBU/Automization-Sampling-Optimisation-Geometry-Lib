from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');d=Path('.astis/decoder-81/result')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
response=load(d/'decoded.json');manifest=load(d/'run-manifest.json');packet=load('.astis/decoder-81/input/packet.json')
assert sha((d/'decoded.json').read_bytes())=='15c9721c7c8360f0b13cdb1ec7b0ea8e8631857cf121b0182a4fb8be18de0d1e'
assert sha((d/'run-manifest.json').read_bytes())=='bb6bc115157332aab856dcd57c37ac2db03b7cbf42848757612ddd40ef5d2fa5'
assert sha(Path('.astis/decoder-81/input/packet.json').read_bytes())=='5a5b161a2bdaa49ce4ced1b31144e994954220bf29ccb2579d01216c361a8eff'
core={k:v for k,v in manifest.items() if k!='decoder_run_sha256'}
assert rt.sha256_json(core)==manifest['decoder_run_sha256']==response['decoder_run_sha256']=='63a67310b81512818078ffc3b64ec67f3fda5284fd45be8c33d2bf2f4b7976fa'
assert rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})==packet['packet_sha256']==response['decoder_packet_sha256']==manifest['packet_sha256']
assert manifest['source_text_visible'] is False and response['source_text_visible'] is False
assert manifest['input_artifacts']==response['input_artifacts']==packet['input_artifacts']
assert all(isinstance(response[k],str) and response[k].strip() for k in rt.SEMANTIC_SLOTS)
text=response['reconstructed_theorem_text'];assert sha(text.encode())==response['reconstructed_text_sha256']==manifest['reconstructed_text_sha256']==sha((d/'reconstruction.txt').read_bytes())
archive=r/'anonymous-decoder81';archive.mkdir(exist_ok=False)
for p in d.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
(archive/'parent-packet.json').write_bytes(Path('.astis/decoder-81/input/packet.json').read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSIdealHalfTurnKernel.json');a=load(ap);assert rt.decoder_packet(a)==packet
(r/'audit.before-decoder81.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=response['reconstructed_text_sha256'],decoder=response['decoder'],decoder_run_sha256=manifest['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=[dict(path='.astis/decoder-81/input/packet.json',raw_sha256=sha(Path('.astis/decoder-81/input/packet.json').read_bytes()))],run_artifact=(archive/'run-manifest.json').as_posix(),native_named_payload_sha256=sha((d/'decoded.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),unresolved_semantics=[],run_hash_recipe='Native manifest is flat core plus decoder_run_sha256; canonical UTF8 sorted compact ensure_ascii=False JSON with decoder_run_sha256 omitted. Packet digest omits packet_sha256. Native files are unchanged.'))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review81.packet.json',review)
save(r/'root.decoder81.adoption.json',dict(status='INDEPENDENT_BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=response['decoder'],native_manifest_RAW_sha256=sha((d/'run-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind adopted; canonical source packet',review['packet_sha256'])
