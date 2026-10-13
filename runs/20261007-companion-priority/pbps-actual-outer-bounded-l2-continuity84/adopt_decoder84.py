from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
r=Path(__file__).parent;d=Path('.astis/decoder84');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert sha((d/'decoder-result.json').read_bytes())=='9d2944e2cfa4a4b2729f7e56560f18e0cbed5f35ed3d5e57130dc06d51ebb77a'
assert sha((d/'RAW-manifest.json').read_bytes())=='72a7e8a9cc62ba5f9a36a21217419910e7c2606a13ae8c24c93b899d9e28212e'
native=load(d/'decoder-result.json');run=load(d/'decoder-run.json');manifest=load(d/'RAW-manifest.json');packet=load(r/'anonymous.decoder84.json')
for group in ['input_artifacts','output_artifacts']:
 for x in manifest[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
runhash=sha((d/'decoder-run.json').read_bytes());assert runhash==native['decoder_run_sha256']=='6cf8ec9203b11da9ad27531ee8b6f94c66d6ffaef31261e745e42c68089ce8d5'
assert run['source_text_visible'] is False and native['source_text_visible'] is False and run['allowed_inputs_only']
assert packet['packet_sha256']==run['packet_declared_sha256']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
text=native['reconstructed_theorem_text'];assert sha(text.encode())==native['reconstructed_text_sha256']==run['reconstructed_text_sha256']==sha((d/'reconstruction.txt').read_bytes())
assert all(isinstance(native[k],str) and native[k].strip() for k in rt.SEMANTIC_SLOTS)
archive=r/'anonymous-decoder84';archive.mkdir(exist_ok=False)
for p in d.iterdir():
 if p.is_file():(archive/p.name).write_bytes(p.read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity.json');a=load(ap);assert rt.decoder_packet(a)==packet
assert a['lean']['statement_sha256']==run['anonymous_statement_sha256']
(r/'audit.before-decoder84.json').write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=native['reconstructed_text_sha256'],decoder=native['decoder'],decoder_run_sha256=runhash,decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=run['input_artifacts'],run_artifact=(archive/'decoder-run.json').as_posix(),native_named_payload_sha256=sha((d/'decoder-result.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'RAW-manifest.json').read_bytes()),unresolved_semantics=[],run_hash_recipe='Exact native decoder-run.json bytes, not a self hash; native files unchanged. Canonical input_artifacts are the descriptors of the proven exact anonymous packet; observed_input_artifacts preserve native exact allowed packet+skill paths/hashes.'))
save(ap,a);review=rt.semantic_reviewer_packet(a);save(r/'source-review84.packet.json',review)
save(r/'root.decoder84.adoption.json',dict(status='INDEPENDENT_BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=native['decoder'],native_manifest_RAW_sha256=sha((d/'RAW-manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],source_verdict=False,VERIFIED=False))
print('Blind adopted; canonical source packet',review['packet_sha256'],'RAW',sha((r/'source-review84.packet.json').read_bytes()))
