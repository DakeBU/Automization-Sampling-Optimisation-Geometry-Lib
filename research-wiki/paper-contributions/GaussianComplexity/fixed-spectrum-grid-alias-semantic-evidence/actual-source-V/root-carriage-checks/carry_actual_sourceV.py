from pathlib import Path
import hashlib,json,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools');import astis_advance as adv
W=Path('.astis/semantic-neutral-20261109/src_82a91d/normal-sourceV-runtime')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-grid-alias-semantic-evidence/actual-source-V')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p):
 b=p.read_bytes();return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def put(p,b):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert sha((W/'FREEZE.json').read_bytes())=='b06d4a484637da43cda04edcab5491a5451f9d9a42229b7df30fd54998691718'
f=json.loads((W/'FREEZE.json').read_text())
for r in f['files']:
 p=W/r['path'];assert sha(p.read_bytes())==r['sha256'] and p.stat().st_size==r['bytes'],p
result=json.loads((W/'API-result.json').read_text());assert result['normal_API_attempt_count']==1 and result['exit_code']==0 and result['return_value'] is None and result['resulting_target_state']=='VERIFIED'
assert result['worker_id']=='/root/source_reader_82a91d'
orig=json.loads((W/'original-evidence.json').read_text());raw=(W/'exact-appended-event.raw.jsonl').read_bytes();event=json.loads(raw)
assert len(raw)==8069 and sha(raw)=='9dc1b2a3da3d43934cf7bd68ee773c8bd3cbc1deebae0844aa6058e18db4fdd4'
assert event['evidence']==orig and event['to_state']=='VERIFIED' and event['worker_id']==result['worker_id']
assert sha((W/'original-evidence.json').read_bytes())=='9075300e2ea7fef6f62470c04849b51be151c20b6424ca220cb38d3ce6aa260a'
canon=json.dumps(orig,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert sha(canon)=='95d1c3ff915f190c4072c33962b809103a69a4aa07b0e9fd22c53aa833f17c9a'
L=Path('runs/substantive_advances.jsonl');before=(W/'advance-ledger.before.raw').read_bytes();assert L.read_bytes()==before+raw
states=adv._replay_advances([json.loads(x) for x in L.read_bytes().splitlines()]);old=adv._replay_advances([json.loads(x) for x in before.splitlines()]);aid=event['advance_id']
assert states[aid]['state']=='VERIFIED' and {k:v for k,v in states.items() if k!=aid}=={k:v for k,v in old.items() if k!=aid}
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==(W/'discovery-ledger.before.raw').read_bytes()
E.mkdir();payload=[p for p in sorted(W.rglob('*')) if p.is_file()]
archive=E/'normal-independent-sourceV-runtime.lossless.tar.gz'
with tarfile.open(archive,'w:gz') as t:
 for p in payload:t.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for p in payload:assert t.extractfile(str(p)).read()==p.read_bytes(),p
put(E/'runtime-archive-manifest.json',dump({'archive':ref(archive),'files':[ref(p) for p in payload],'scope':'Actual original independent sourceV one-call runtime, all original evidence and raw append; no later integration/park or new builds.'}))
for n in ['FREEZE.json','API-result.json','original-evidence.json','original-evidence-digest.json','exact-appended-event.raw.jsonl','execute.receipt.json','execution-report.md','normal-reviewed-admission.receipt.json','preflight-success.json']:
 put(E/n,(W/n).read_bytes())
put(E/'root-readback-no-status-API.json',dump({'actual_sourceV_API_calls_by_root':0,'actual_independent_API_calls':1,'actual_original_evidence_field_count':len(orig),'original_field_names':list(orig),'original_raw_evidence':ref(E/'original-evidence.json'),'canonical_original_object_sha256':sha(canon),'exact_append':ref(E/'exact-appended-event.raw.jsonl'),'all_other_advance_states_preserved':len(old)-1,'discovery_bytes_preserved':True,'current_normal_state':'VERIFIED','verified_commit':orig['verified_commit'],'checked_commit_layers':orig['checked_commit_layers'],'later_existing_V_release':'Preserve EVERY original field/value from this exact object and add ONLY post_integration. Do not assume C7s13-field count: this actual packet has12.','frontier_projection':'Performed separately by original independent verifier, never by proving worker self-certification.','integration_site_browser_remote_purification_Goal_credit':False}))
print(json.dumps({'actual_sourceV_state':'VERIFIED','independent_actor':result['worker_id'],'actual_API_calls_by_root':0,'actual_evidence_fields':len(orig),'append_sha256':sha(raw),'all_other_states_preserved':True,'archive_sha256':sha(archive.read_bytes())}))
