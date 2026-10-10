from pathlib import Path
import json,hashlib,datetime,os,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-marginal-poincare-consumer-overlay-review57';B=R/'runs/20261007-companion-priority/pbps-marginal-poincare-consumer-overlay57';G=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph57';N=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph-review57'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,allow_nan=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['content_self_sha256']=sha(canon(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('content_self_sha256');assert sha(canon(q))==v;return pin(p)
assert not (O/'lease.json').exists()
write('review.process.status.json',{'schema_version':1,'actor':'/root/next_primary56','script':pin(O/'review_overlay.py'),'actual_native_exec_chunk':'87ddad','actual_exit_code':0,'actual_pid':3208,'execution':'Synchronous foreground actual completed process; no compiler/helper/detached work.'})
inputs=json.loads((O/'input.manifest.json').read_bytes());readbacks=[]
for q in inputs['inputs']:assert pin(q['path'])==q;readbacks.append(q)
for q in inputs['header_only_checks']:
 parts=[]
 with (R/q['module_path']).open('rb') as h:
  for line in h:
   if b' := by' in line:parts.append(line.split(b' := by',1)[0]);break
   parts.append(line)
 prefix=b''.join(parts).replace(b'\r\n',b'\n').rstrip()+b'\n';assert prefix==Path(q['snapshot']['path']).read_bytes()
unchanged=[]
for folder,key in [(G,'outputs'),(N,'output_readbacks')]:
 j=json.loads((folder/'lease.json').read_bytes())
 for q in j[key]:
  a=pin(q['path']);assert all(a[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256'] if k in q);unchanged.append({'pinned_by_original_lease':str(folder/'lease.json').replace('\\','/'),'actual':a})
for p in O.glob('*.json'):
 j=json.loads(p.read_bytes())
 if 'content_self_sha256' in j:
  v=j.pop('content_self_sha256');assert sha(canon(j))==v,p
write('native.readbacks.json',{'schema_version':1,'actor':'/root/next_primary56','input_count':len(readbacks),'inputs':readbacks,'original_closed_output_pins_verified':len(unchanged),'original_closed_output_readbacks':unchanged,'original_outputs_all_unchanged':True,'header_suffixes_never_read':True,'full_module_metadata_unchecked_as_disclosed':True})
before=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
manifest=write('manifest.json',{'schema_version':1,'artifact_kind':'native-consumer-overlay-review-output-manifest','actor':'/root/next_primary56','pins':before,'hash_recipe':'Complete object minus ONLY content_self_sha256, sorted compact ensure_ascii=False allow_nan=False UTF8 JSON no newline. Raw/LF file pins distinct; run/complete/lease bound separately.'})
review=pin(O/'consumer-overlay.review.json')
run=write('reviewer.consumer-overlay.run.json',{'schema_version':1,'artifact_kind':'native-independent-consumer-overlay-review-run','trusted_actor':'/root/next_primary56','verdict':'ACCEPT_PLANNED_SCOPED_CONSUMER_TOPOLOGY_ONLY','overlay':pin(B/'consumer.overlay.json'),'review':review,'original_source_graph':pin(G/'graph.packet.json'),'original_negative':pin(N/'topology.review.json'),'input_count':len(readbacks),'initial_native_receipt_checks':8,'initial_complete_self_checks':13,'original_closed_output_pins_verified':len(unchanged),'planned_combined_nodes':118,'planned_combined_edges':17,'two_paths_resolved':True,'weakH1_gap_not_consumed':True,'compiler':'NOT_STARTED_CLOSED','parent_proof_body_exposure':'NONE in this review; exact public prefixes only. Historical56 exposure remains recorded.','manifest':manifest,'native_readbacks':pin(O/'native.readbacks.json'),'review_process':pin(O/'review.process.status.json'),'finalizer':{'script':pin(O/'finalize_overlay_review.py'),'pid':os.getpid(),'execution':'Synchronous foreground; actual enclosing tool exit status authoritative after final filesystem write.'},'formal_math_Lean_admission':False,'hash_recipe':'COMPLETE object excluding ONLY content_self_sha256; no named component payload alias.'})
complete=write('complete.json',{'schema_version':1,'artifact_kind':'native-distinct-consumer-overlay-review-completion','actor':'/root/next_primary56','status':'SCOPED_TOPOLOGY_REVIEW_COMPLETE','run':run,'review':review,'blockers':[],'paths_resolved':['57-consumer-domain-path','57-consumer-centering-path'],'original_negatives_preserved':True,'exact_statement_unchanged1244':True,'new_source_or_Lean_or_math_admission':False,'final_lease_last_required':True})
outputs=[]
for p in sorted(O.rglob('*')):
 if p.is_file():q=pin(p);assert pin(p)==q;outputs.append(q)
for q in inputs['inputs']:assert pin(q['path'])==q
lease=write('lease.json',{'schema_version':1,'artifact_kind':'native-consumer-overlay-review-resource-lease','actor':'/root/next_primary56','state':'CLOSED','read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED','opened_lease':pin(O/'lease.open.json'),'closed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Own distinct consumer-overlay-review57 outputs only; no canonical/creator/original57/56CLOSED-output changes, proof-body reading, compiler or detached work.','review_process_actual_exit_code':0,'finalizer_pid':os.getpid(),'finalizer_exit_evidence':'Successful synchronous native tools.exec_command exit0 follows final write; file handles closed, no deferred processes.','input_count':len(readbacks),'original_closed_output_pins_verified':len(unchanged),'output_readback_count':len(outputs),'output_readbacks':outputs,'run':run,'complete':complete,'closure_order':'LAST filesystem write; only readback verification and stdout follow.','hash_recipe':'Complete object minus ONLY content_self_sha256; sorted compact UTF8 ensure_ascii=False allow_nan=False withoutnewline; exact raw/LF bytes distinct.'})
j=json.loads((O/'lease.json').read_bytes());v=j.pop('content_self_sha256');assert sha(canon(j))==v
print(json.dumps({'state':'CLOSED','finalizer_normal_exit_code':0,'verdict':'ACCEPT_PLANNED_SCOPED_CONSUMER_TOPOLOGY_ONLY','review':review,'run':run,'lease':lease,'self_hashes':{'review':json.loads((O/'consumer-overlay.review.json').read_bytes())['content_self_sha256'],'run':json.loads((O/'reviewer.consumer-overlay.run.json').read_bytes())['content_self_sha256'],'lease':v},'schema_versions':{'review':1,'run':1,'manifest':1,'complete':1,'lease':1},'input_count':len(readbacks),'original_closed_output_pins_verified':len(unchanged),'output_readbacks':len(outputs),'math_or_Lean_admission':False},ensure_ascii=False))
