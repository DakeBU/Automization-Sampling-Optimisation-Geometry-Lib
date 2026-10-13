from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path(__file__).parent;d=Path('.astis/decoder87');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
 assert not Path(p).exists(),p
 Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
out=d/'output';native=load(out/'reconstruction.native.json');run=load(out/'native-run-evidence.json');manifest=load(out/'raw-manifest.closed.json');packet=load(d/'input.json')
assert sha((out/'reconstruction.native.json').read_bytes())=='8bc0d0fbf7f7a3f68fb5dc8dddf50a88aea1b54de7d3d294efbe57b083647f52'
assert sha((out/'native-run-evidence.json').read_bytes())=='29b4b2d54a0dbd133faae763b8eba7a97ebe6e22a31f4907222becf5e5e97162'
assert sha((out/'raw-manifest.closed.json').read_bytes())=='4803cb0a101db85a6b90db6da26cbed32aca1e9f2e68b3799fe518bcdc63fbee'
for x in manifest['outputs']:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
assert sha((d/'input.json').read_bytes())==run['raw_input_sha256']=='f4b8c55f238f2ecaeb082f698bb0873073ea81eeacea7624777607cbef322fea'
assert rt.sha256_json(packet)==run['canonical_complete_packet_sha256']
assert packet['packet_sha256']==run['declared_packet_sha256']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert native['source_text_visible'] is False and run['source_text_visible'] is False
text=native['reconstructed_theorem_text'];assert sha(text.encode())==native['reconstructed_text_sha256']
assert all(isinstance(native[k],str) and native[k].strip() for k in rt.SEMANTIC_SLOTS)
# Native unresolved_fields are preserved: absent source identity and an explicitly
# unclaimed random-depth extension, not unresolved interpretation of this Prop.
assert len(native['unresolved_fields'])==2
assert 'Source theorem identity' in native['unresolved_fields'][0]
assert 'random stopping depths' in native['unresolved_fields'][1]
archive=r/'anonymous-decoder87';archive.mkdir(exist_ok=False)
for p in out.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryTailLaw.json');a=load(ap);assert rt.decoder_packet(a)==packet
save(r/'audit.before-decoder87.json',a)
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=native['reconstructed_text_sha256'],decoder='/root/blind_decoder87',decoder_run_sha256=native['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=[{'path':run['input_artifact'],'raw_sha256':run['raw_input_sha256']}],run_artifact=(archive/'native-run-evidence.json').as_posix(),native_named_payload_sha256=sha((out/'reconstruction.native.json').read_bytes()),native_run_manifest_RAW_sha256=sha((out/'raw-manifest.closed.json').read_bytes()),unresolved_semantics=[],native_unresolved_fields=native['unresolved_fields'],unresolved_classification='Source identity is deliberately hidden; random-depth extension is explicitly outside the theorem. Neither is an unresolved semantic slot of the supplied deterministic-depth Prop.',run_hash_recipe='Exact native run bytes; closed native outputs archived unchanged. Canonical descriptors bind the sole approved anonymous input.'))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(r/'root.decoder87.adoption.json',dict(status='BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder='/root/blind_decoder87',native_manifest_RAW_sha256=sha((out/'raw-manifest.closed.json').read_bytes()),packet_sha256=packet['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind87 adopted only; fresh source packet awaits independently accepted exposition overlay.')
