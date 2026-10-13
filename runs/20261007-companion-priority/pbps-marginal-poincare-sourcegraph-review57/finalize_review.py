from pathlib import Path
import json,hashlib,datetime,os,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-marginal-poincare-sourcegraph-review57'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':str(p).replace('\\','/'),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf)}
def write(n,j):
 j['content_self_sha256']=sha(canon(j));p=O/n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8'));q=json.loads(p.read_bytes());v=q.pop('content_self_sha256');assert sha(canon(q))==v;return pin(p)
assert not (O/'lease.json').exists()
write('author.process.status.json',{'schema_version':1,'actor':'/root/next_primary56','script':pin(O/'author_review.py'),'actual_exec_chunk':'30fe30','actual_exit_code':0,'execution':'Synchronous foreground native tool completed; no helper/background/compiler job.'})
inputs=json.loads((O/'input.manifest.json').read_bytes());checked=[]
for q in inputs['inputs']:
 assert pin(q['path'])==q,q['path'];checked.append(q)
headerchecks=[]
for q in inputs['header_only_inputs']:
 parts=[]
 with (R/q['path']).open('rb') as f:
  for line in f:
   if b':= by' in line:parts.append(line.split(b':= by',1)[0]);break
   parts.append(line)
 b=b''.join(parts);assert len(b)==q['header_raw_bytes'] and sha(b)==q['header_raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['header_lf_sha256'];headerchecks.append(q)
for p in O.glob('*.json'):
 j=json.loads(p.read_bytes())
 if 'content_self_sha256' in j:
  v=j.pop('content_self_sha256');assert sha(canon(j))==v,p
for q in inputs['inputs']:
 if q['path'].endswith('.json'):
  j=json.loads(Path(q['path']).read_bytes())
  if 'content_self_sha256' in j:
   v=j.pop('content_self_sha256');assert sha(canon(j))==v,q['path']
write('input.readbacks.json',{'schema_version':1,'actor':'/root/next_primary56','actual_raw_lf_pins':checked,'input_count':len(checked),'header_only_checks':headerchecks,'all_match':True,'historical_standing_input_note':'Own57 old canonical frontier receipt verified against owned exact frozen snapshot as explicitly recorded; no assertion current canonical frontier still equals historical bytes.'})
prior=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
manifest=write('manifest.json',{'schema_version':1,'actor':'/root/next_primary56','artifact_kind':'native-exact-output-manifest','pins':prior,'self_hash_recipe':'Complete object minus ONLY content_self_sha256; UTF8 ensure_ascii=False sorted compact JSON without newline; raw bytes/LF file hashes distinct. Later run/complete/lease receipts bound separately, no cycle.'})
review=pin(O/'topology.review.json')
run=write('reviewer.topology.run.json',{'schema_version':1,'artifact_kind':'native-independent-source-topology-review-run','actor':'/root/next_primary56','creator':'/root/sourcegraph57','verdict':'ACCEPT_STANDALONE_PI_SOURCE_EXTRACTION_WITH_TYPED_CONSUMER_BLOCKERS','review':review,'source_graph_sha256':'b4c3f3db9ff224bf7fcf048026e3cc1ca003b93b708f080dca2e5307cca6c6ed','statement_lf_sha256':'e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9','input_count':len(checked),'native_receipt_checks':385,'native_complete_self_hash_checks_initial':13,'coverage_independently_enumerated':606,'nodes':111,'semantic_nodes':17,'edges':10,'consumer_missing_paths':2,'standalone_PI_statement_blockers':0,'manifest':manifest,'verification':pin(O/'native.verification.json'),'verification_process':pin(O/'verification.process.status.json'),'author_process':pin(O/'author.process.status.json'),'finalizer':{'script':pin(O/'finalize_review.py'),'pid':os.getpid(),'mode':'Synchronous foreground; actual enclosing tool exit code authoritative after final write.'},'proof_body_exposure':'No57body exists; no existing-parent proof suffix or creator parser implementation inspected. Historical56finalpacket exposure retained.','compiler':'NOT_STARTED_CLOSED','mathematical_admission':False,'hash_recipe':'COMPLETE object minus ONLY content_self_sha256; no selected/named payload hash alias.'})
complete=write('complete.json',{'schema_version':1,'actor':'/root/next_primary56','status':'ORIGINAL_INDEPENDENT_REVIEW_COMPLETE','run':run,'review':review,'all_inputs_readback':True,'input_count':len(checked),'header_only_count':len(headerchecks),'standalone_PI_scope_accepted':True,'planned_actual56_consumer_blocked':True,'source_topology_repair_implemented':False,'source_or_math_or_Lean_admission':False,'lease_written_last_required':True})
readbacks=[]
for p in sorted(O.rglob('*')):
 if p.is_file():q=pin(p);assert pin(p)==q;readbacks.append(q)
for q in inputs['inputs']:assert pin(q['path'])==q
lease=write('lease.json',{'schema_version':1,'actor':'/root/next_primary56','artifact_kind':'native-independent-source-topology-resource-lease','state':'CLOSED','read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'NOT_STARTED_CLOSED','opened_lease':pin(O/'lease.open.json'),'closed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Own original sourcegraph-review57 folder only; creator originals/56reviews/primary57/canonical metadata/Lean/ledgers untouched. No claim/proof or compiler.','input_count':len(checked),'output_readback_count':len(readbacks),'output_readbacks':readbacks,'native_verification_actual_exit_code':0,'author_actual_exit_code':0,'finalizer_pid':os.getpid(),'finalizer_exit_evidence':'Synchronous native tools.exec_command result after final write confirms actual EXIT0. No spawned/detached work; file handles closed before seal.','run':run,'complete':complete,'closure_order':'FINAL filesystem write. Only readback validation and stdout follow.','hash_recipe':'Complete object excluding ONLY content_self_sha256; sorted compact JSON ensure_ascii=False encodedUTF8 no newline; exact raw/LF file receipts separate.'})
j=json.loads((O/'lease.json').read_bytes());v=j.pop('content_self_sha256');assert sha(canon(j))==v
print(json.dumps({'status':'CLOSED','finalizer_normal_exit_code':0,'review':review,'run':run,'lease':lease,'self_hashes':{'review':json.loads((O/'topology.review.json').read_bytes())['content_self_sha256'],'run':json.loads((O/'reviewer.topology.run.json').read_bytes())['content_self_sha256'],'lease':v},'schema_versions':{'review':1,'run':1,'manifest':1,'complete':1,'lease':1},'input_count':len(checked),'output_readback_count':len(readbacks),'verdict':'ACCEPT_STANDALONE_PI_SOURCE_EXTRACTION_WITH_TYPED_CONSUMER_BLOCKERS','consumer_missing_paths':2,'mathematical_admission':False},ensure_ascii=False))
