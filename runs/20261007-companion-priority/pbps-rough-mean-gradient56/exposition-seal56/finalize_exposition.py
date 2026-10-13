from pathlib import Path
import json,hashlib,datetime,sys,os
sys.stdout.reconfigure(encoding='utf8')
ROOT=Path('E:/Samplinglib');B=ROOT/'runs/20261007-companion-priority/pbps-rough-mean-gradient56';O=B/'exposition-seal56'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['complete_object_sha256']=sha(canonical(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('complete_object_sha256');assert sha(canonical(q))==v;return pin(p)
assert not (O/'lease.json').exists()
prep={'schema_version':1,'process':'prepare_exposition.py','actual_native_exec_chunk':'33afe3','actual_exit_code':0,'actual_pid':52972,'stdout':{'input_count':65,'checks':12,'images':4,'node_bytes':38235,'graph_nodes':13,'graph_edges':12},'execution':'Synchronous foreground tools.exec_command returned exit0; no detached process.'}
write('prepare.process.status.json',prep)
validation=json.loads((O/'verification.json').read_bytes());validation.pop('complete_object_sha256')
capturechecks=[]
for prefix in ['cdp','proof']:
 cap=json.loads((B/'visual-inspection56'/f'{prefix}.capture.json').read_bytes());assert cap['ownedBrowserExit']=={'code':0,'signal':None}
 for r in cap['records']:
  target=B/'visual-inspection56'/f'{prefix}.{r["label"]}.png';origin=Path(r['png_path']);assert origin.read_bytes()==target.read_bytes()
  inspection=B/'visual-inspection56'/f'{prefix}.{r["label"]}.inspect.json';j=json.loads(inspection.read_bytes());assert all(j[k]==v for k,v in r.items() if k!='label' and k!='png_path')
  capturechecks.append({'original':pin(origin),'portable':pin(target),'inspection':pin(inspection),'bytes_identical':True,'inspection_matches_native_capture':True,'owned_browser_exit_code':0})
assert len(capturechecks)==4
validation['portable_capture_identity_checks']=capturechecks
for k in ['companion_container','graph_container']:
 q=validation['site'][k];assert pin(q['path'])==q
validation['mutable_site_rechecked_before_closure']=True
write('verification.json',validation)
for p in O.glob('*.json'):
 if p.name=='lease.open.json':continue
 j=json.loads(p.read_bytes())
 if 'complete_object_sha256' in j:
  v=j.pop('complete_object_sha256');assert sha(canonical(j))==v,p
inputs=json.loads((O/'input.manifest.json').read_bytes())['inputs']
for q in inputs:assert pin(q['path'])==q,q['path']
outputs=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
manifest=write('manifest.json',{'schema_version':1,'artifact_kind':'native-exposition-output-manifest','pins':outputs,'self_hash_recipe':'SHA256 UTF8 JSON ensure_ascii=False sort_keys=True separators comma/colon no whitespace or terminal newline; COMPLETE object minus ONLY complete_object_sha256. Raw file receipt is distinct; no named payload alias. Manifest pins all preceding actual files including scripts/open lease and input snapshots; later run/complete/lease bound separately.'})
run=write('reviewer.exposition.run.json',{'schema_version':1,'artifact_kind':'native-independent-exposition-review-run','trusted_actor':'/root/next_primary56','scope':'scoped desktop ExpositionSeal56 only','science_commit':'db2c1237cd56698ae560a8121abfcbf374ff8838','integration_commit':'4a35307e4ca010e12bf5628b8b023c8449d9cce9','verdict':'ACCEPT_SCOPED_DESKTOP_EXPOSITION_WITH_RETAINED_DEBT','input_count':len(inputs),'output_manifest':manifest,'source_review_reuse':pin(B/'source-review56/result0.json'),'review':pin(O/'exposition.review.json'),'verification':pin(O/'verification.json'),'prepare_process':pin(O/'prepare.process.status.json'),'independent_viewed_images':4,'no_new_compiler':True,'historical_blindness':'Own primary/statement/topology before body preserved; final56 packet body visible; no57 sourcegraph/body read.','finalizer':{'script':pin(O/'finalize_exposition.py'),'pid':os.getpid(),'mode':'foreground synchronous; subsequent native tools.exec_command exit status authoritative','no_spawned_or_detached_jobs':True},'self_hash_recipe':'Complete object excluding only complete_object_sha256; sorted compact UTF8 ensure_ascii=False. No named component payload hash claimed.'})
complete=write('complete.json',{'schema_version':1,'artifact_kind':'native-scoped-exposition-completion','status':'REVIEW_COMPLETE_PENDING_FINAL_LEASE_WRITE','run':run,'manifest':manifest,'input_count':len(inputs),'checked12_exit0':True,'images4_independently_viewed':True,'scoped_acceptance':True,'full_reader_or_purified':False,'final_lease_must_be_written_last':True})
readbacks=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  q=pin(p);assert pin(p)==q;readbacks.append(q)
# Re-read the immutable input pins once more; no source/site/compiler mutations.
for q in inputs:assert pin(q['path'])==q
closed=write('lease.json',{'schema_version':1,'artifact_kind':'native-exposition-resource-lease','trusted_actor':'/root/next_primary56','status':'CLOSED','read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED','browser':'NOT_STARTED_BY_REVIEWER_CLOSED','opened_lease':pin(O/'lease.open.json'),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Own exposition-seal56 only, no canonical/Lean/site/ledger mutation and no57graph/body access.','actual_preparation_exit_code':0,'finalizer_pid':os.getpid(),'finalizer_exit_evidence':'Native synchronous tool result following final write is authoritative; no deferred/background work. This finalizer closes file handles and performs successful native readbacks before normal exit0.','output_readback_count':len(readbacks),'output_readbacks':readbacks,'input_count':len(inputs),'run':run,'complete':complete,'self_hash_recipe':'Complete object minus ONLY complete_object_sha256, compact sorted ensure_ascii=False UTF8 without newline; actual raw/LF receipt distinct.','closure_order':'This lease is the LAST filesystem write. Only readback verification and stdout follow.'})
check=json.loads((O/'lease.json').read_bytes());v=check.pop('complete_object_sha256');assert sha(canonical(check))==v
print(json.dumps({'status':'CLOSED','actual_finalizer_normal_exit_code':0,'lease':closed,'review':pin(O/'exposition.review.json'),'run':pin(O/'reviewer.exposition.run.json'),'input_count':len(inputs),'output_readback_count':len(readbacks),'schemas':{'review':1,'run':1,'manifest':1,'complete':1,'lease':1},'complete_object_self_hashes':{'review':json.loads((O/'exposition.review.json').read_bytes())['complete_object_sha256'],'run':json.loads((O/'reviewer.exposition.run.json').read_bytes())['complete_object_sha256'],'lease':v},'no_math_or_full_reader_admission':True},ensure_ascii=False))
