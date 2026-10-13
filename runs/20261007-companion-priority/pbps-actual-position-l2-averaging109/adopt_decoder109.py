from pathlib import Path
import hashlib,json,sys
r=Path(__file__).parent;sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPositionL2Averaging.json');a=load(ap)
folder=Path('runs/semantic-roundtrip/anonymous109/decoder-native');v,run,packet=[load(p) for p in [folder/'decoder.json',folder/'manifest.json',folder.parent/'input.json']]
assert a['state']=='draft' and 'reconstruction' not in a
assert run['decoder']==v['decoder'] and run['decoder']['agent']=='/root/blind_decoder109' and run['decoder']['role']=='independent-source-blind-decoder'
assert all(run[k] is False and v[k] is False for k in ['source_text_visible','source_identity_visible','source_anchor_visible','prior_audits_visible','repairs_visible'])
assert run['input']['raw_sha256']==v['input_raw_sha256']==sha((folder.parent/'input.json').read_bytes())
assert run['input']['packet_sha256']==v['packet_sha256']==packet['packet_sha256']==rt.decoder_packet(a)['packet_sha256']
for info in run['outputs']:assert sha(Path(info['path']).read_bytes())==info['sha256']
text=(folder/'reconstructed-theorem.txt').read_text(encoding='utf8');assert text==v['reconstructed_theorem'] and sha(text.encode())==v['reconstruction_sha256']
before=r/'audit-before-decoder109.json';assert not before.exists();before.write_bytes(ap.read_bytes())
a['reconstruction']=dict(text=text,text_sha256=sha(text.encode()),decoder='independent-source-blind-decoder:/root/blind_decoder109',decoder_run_sha256=sha((folder/'manifest.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[dict(path=(folder.parent/'input.json').as_posix(),raw_sha256=run['input']['raw_sha256'])],run_artifact=(folder/'manifest.json').as_posix(),native_structured_payload=(folder/'decoder.json').as_posix(),native_named_payload_sha256=sha((folder/'decoder.json').read_bytes()),native_semantic_slots=v)
save(ap,a);save(r/'decoder-admission109.json',dict(decoder_native=(folder/'decoder.json').as_posix(),decoder_run_raw_sha256=sha((folder/'manifest.json').read_bytes()),packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],source_verdict='pending',native_schema_preserved=True))
print('Adopted exact native blind reconstruction; source verdict pending.')
