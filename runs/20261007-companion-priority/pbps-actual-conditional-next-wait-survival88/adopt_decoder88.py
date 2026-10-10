from pathlib import Path
import hashlib,json,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;d=r/'anonymous-decoder'
sys.path.insert(0,str(R/'tools'));import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
expected={'reconstructed-theorem.json':'ff168dc546148e12e1693b7be65a61ceb1d7d1a5a09817033bd6d73f80c3c0a2','decoder.run.json':'e280d496df1cedd33e2b5e52bdf39ee413d27a5a327b9b55af0b1de4de939ddf','closed-RAW-manifest.json':'48839dccf8a58804250d0ff9d74989922d7f865ec67c85df13662d694636d6cd'}
for p,h in expected.items():assert sha((d/p).read_bytes())==h,p
m=load(d/'closed-RAW-manifest.json');n=load(d/'reconstructed-theorem.json');run=load(d/'decoder.run.json');packet=load(r/'anonymous.decoder88.json')
for group in ['inputs','outputs']:
 for x in m[group]:
  b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x.get('raw_sha256',x.get('sha256')),x['path']
inp=run['mathematical_inputs'][0]
assert sha((r/'anonymous.decoder88.json').read_bytes())==inp['raw_sha256']=='5118dc1a431a2f1068f98abd68a5b1e19e63efa9bbf27a90b7caf69fb9b4ef60'
assert rt.sha256_json(packet)==inp['canonical_sorted_json_complete_sha256']
assert packet['packet_sha256']==inp['packet_sha256_declared']==rt.sha256_json({k:v for k,v in packet.items() if k!='packet_sha256'})
assert n['source_text_visible'] is False and run['source_text_visible'] is False
assert n['decoder_run_sha256']==expected['decoder.run.json']
text=n['reconstructed_theorem_text'];assert sha(text.encode())==n['reconstructed_text_sha256']==run['reconstructed_text_sha256']
assert all(isinstance(n[k],str) and n[k].strip() for k in rt.SEMANTIC_SLOTS)
assert n['unresolved_fields']==run['unresolved_fields']==[]
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitSurvival.json';a=load(ap);assert a['state']=='draft' and rt.decoder_packet(a)==packet
snap=r/'audit.before-decoder88.json';assert not snap.exists();snap.write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed',reconstruction=dict(text=text,text_sha256=n['reconstructed_text_sha256'],decoder=n['decoder'],decoder_run_sha256=n['decoder_run_sha256'],decoder_packet_sha256=packet['packet_sha256'],source_text_visible=False,lean_statement_sha256=a['lean']['statement_sha256'],input_artifacts=packet['input_artifacts'],observed_input_artifacts=[dict(path=inp['path'],raw_sha256=inp['raw_sha256'])],run_artifact=(d/'decoder.run.json').as_posix(),native_named_payload_sha256=expected['reconstructed-theorem.json'],native_run_manifest_RAW_sha256=expected['closed-RAW-manifest.json'],unresolved_semantics=[],native_unresolved_fields=[],run_hash_recipe='Exact native decoder.run.json bytes; complete canonical anonymous packet plus exact RAW input; source not visible.'))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
out=r/'root.decoder88.adoption.json';assert not out.exists();out.write_text(json.dumps(dict(status='BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=n['decoder'],native_manifest_RAW_sha256=expected['closed-RAW-manifest.json'],packet_sha256=packet['packet_sha256'],source_verdict=False,VERIFIED=False,interpretation_to_compare='Native wording d need not be deterministic is retained: quantifiers fix a deterministic Borel function d, while d(H_n) is random. Source reviewer must explicitly assess this wording against the exact decoded quantifiers; no silent native repair.'),indent=2)+'\n',encoding='utf8',newline='\n')
print('88 exact native blind reconstruction adopted; no source fidelity/VERIFIED credit.')
