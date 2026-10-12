from pathlib import Path
import hashlib,json,sys
r=Path('runs/20261007-companion-priority/pbps-actual-normalized-endpoint104');sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualNormalizedEndpointSector.json');a=load(ap);folder=Path('runs/semantic-roundtrip/anonymous104/decoder-native');v=load(folder/'reconstruction.json');run=load(folder/'decoder-run.json');packet=load(folder.parent/'input.json')
assert a['state']=='draft' and 'reconstruction' not in a
assert all(run[k] is False for k in ['source_text_visible','source_identity_visible','prior_audit_visible','repair_proposals_visible'])
assert len(run['input_artifacts'])==1 and run['input_artifacts'][0]['sha256_raw']==sha((folder.parent/'input.json').read_bytes())
assert run['canonical_supplied_packet_sha256']==packet['packet_sha256']==rt.decoder_packet(a)['packet_sha256']
for d in run['reconstruction_artifacts']:assert sha(Path(d['path']).read_bytes())==d['sha256_raw']
before=r/'audit-before-decoder104.json';assert not before.exists();before.write_bytes(ap.read_bytes());text=(folder/'reconstruction.txt').read_text(encoding='utf8')
a['reconstruction']=dict(text=text,text_sha256=sha(text.encode()),decoder=run['decoder_identity'],decoder_run_sha256=sha((folder/'decoder-run.json').read_bytes()),decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[dict(path=(folder.parent/'input.json').as_posix(),raw_sha256=run['input_artifacts'][0]['sha256_raw'])],run_artifact=(folder/'decoder-run.json').as_posix(),native_structured_payload=(folder/'reconstruction.json').as_posix(),native_named_payload_sha256=sha((folder/'reconstruction.json').read_bytes()),native_semantic_slots=v)
save(ap,a);review=rt.semantic_reviewer_packet(a);p=r/'reviewer-packet104.json';assert not p.exists();save(p,review)
save(r/'decoder-admission104.json',dict(decoder_native=(folder/'reconstruction.json').as_posix(),decoder_run_raw_sha256=sha((folder/'decoder-run.json').read_bytes()),packet_sha256=packet['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],source_verdict='pending'));print(review['packet_sha256'])
