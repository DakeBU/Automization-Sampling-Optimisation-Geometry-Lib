from pathlib import Path
import hashlib,json,sys
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedPathReversal.json');a=load(ap)
folder=Path('runs/semantic-roundtrip/anonymous100/decoder-native');v=load(folder/'reconstruction.json');run=load(folder/'decoder-run.json');packet=load(folder.parent/'input.json')
assert a['state']=='draft' and 'reconstruction' not in a
assert v['source_text_visible'] is False and run['source_text_visible'] is False and run['source_identity_visible'] is False and run['proof_visible'] is False
assert v['input_raw_sha256']==sha((folder.parent/'input.json').read_bytes())
assert v['packet_sha256']==packet['packet_sha256']==rt.decoder_packet(a)['packet_sha256']
assert v['reconstructed_text_sha256']==sha(v['reconstructed_theorem_text'].encode())==sha((folder/'reconstructed-theorem.txt').read_bytes())
canonical={k:x for k,x in v.items() if k not in ['decoder_run_sha256','decoder_run_hash_method']}
assert sha(json.dumps(canonical,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==v['decoder_run_sha256']
before=r/'audit-before-decoder100.json';assert not before.exists();before.write_bytes(ap.read_bytes())
a['reconstruction']=dict(text=v['reconstructed_theorem_text'],text_sha256=v['reconstructed_text_sha256'],decoder=v['decoder']['agent'],decoder_run_sha256=sha((folder/'decoder-run.json').read_bytes()),decoder_packet_sha256=v['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=['lean-statement','approved-definition-context'],observed_input_artifacts=[dict(path=(folder.parent/'input.json').as_posix(),raw_sha256=v['input_raw_sha256'])],run_artifact=(folder/'decoder-run.json').as_posix(),native_structured_payload=(folder/'reconstruction.json').as_posix(),native_named_payload_sha256=sha((folder/'reconstruction.json').read_bytes()),native_semantic_slots={k:v[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']},native_canonical_payload_hash=v['decoder_run_sha256'])
save(ap,a);review=rt.semantic_reviewer_packet(a);p=r/'reviewer-packet100.json';assert not p.exists();save(p,review)
save(r/'decoder-admission100.json',dict(decoder_native=(folder/'reconstruction.json').as_posix(),decoder_run_raw_sha256=sha((folder/'decoder-run.json').read_bytes()),packet_sha256=v['packet_sha256'],reviewer_packet_sha256=review['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'],source_verdict='pending'))
print(json.dumps(dict(reviewer_packet=p.as_posix(),canonical_packet_sha256=review['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'])))
