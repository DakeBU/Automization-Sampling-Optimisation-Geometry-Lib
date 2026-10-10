from pathlib import Path
import json,hashlib,datetime,subprocess
stage=Path(__file__).parent;root=Path(r'E:\Samplinglib')
def sha(b):return hashlib.sha256(b).hexdigest()
def read(path):
 with path.open('rb') as handle:return handle.read()
def record(path):
 raw=read(path);lf=raw.replace(b'\r\n',b'\n')
 return {'path':str(path.resolve()),'raw_bytes':len(raw),'raw_sha256':sha(raw),'lf_bytes':len(lf),'lf_sha256':sha(lf),'normalization':'literal bytes CRLF to LF, no decode/reserialization'}
def seal(name,payload):
 path=stage/name;assert not path.exists(), 'Closed native outputs may not be overwritten.'
 canonical=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
 obj=dict(payload);obj['self_digest']={'recipe':'Remove self_digest, then JSON ensure_ascii=False sort_keys=True separators=(comma,colon), UTF8 no newline','payload_bytes':len(canonical),'payload_sha256':sha(canonical)}
 with path.open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
 return record(path)
review=json.loads(read(stage/'exposition-seal55.json').decode('utf-8'));checks=json.loads(read(stage/'readback55.json').decode('utf-8'))
assert checks['status']=='PASS_PRE_CLOSURE' and review['verdict']=='ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(root)).decode().strip();assert head==review['integration_HEAD']
for p in review['pins'].values():assert record(Path(p['path']))['raw_sha256']==p['raw_sha256']
for p in review['images'].values():assert record(Path(p['path']))['raw_sha256']==p['raw_sha256']
for p in review['actual_capture_DOM'].values():assert record(Path(p['path']))['raw_sha256']==p['raw_sha256']
run=seal('run.json',{'schema_version':1,'kind':'INDEPENDENT_SCOPED_EXPOSITION_REVIEW_RUN55','reviewer':'/root/sourcegraph_creator56','status':'COMPLETE_ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'integration_HEAD':head,'science_commit':review['science_commit'],'actual_foreground_calls':[{'script':'open_review55.py','exit_code':0},{'script':'inspect_local_html55.py','exit_code':0,'corrected_extractor_comparisons':'EOL and namespace-display diagnoses retained before correction; no canonical edits.'},{'script':'build_exposition_review55.py','exit_code':0}],'independently_viewed_four_actual_images':True,'not_source_blind_or_identity_blind':True,'not_full_math_reverification':True,'compiler':'NOT_STARTED_CLOSED','named_payloads':{'review':record(stage/'exposition-seal55.json'),'readback':record(stage/'readback55.json'),'native_html':record(stage/'actual-native-dom-checks55.json')}})
manifest=seal('manifest.json',{'schema_version':1,'kind':'SCOPED_EXPOSITION_REVIEW_MANIFEST55','status':'COMPLETE','files':{p.name:record(p) for p in sorted(stage.iterdir()) if p.is_file()},'external_images':review['images'],'external_actual_DOM_capture':review['actual_capture_DOM'],'root_capture_lease':review['capture_closed_lease'],'run':run,'pins':review['pins']})
complete=seal('complete.json',{'schema_version':1,'kind':'SCOPED_EXPOSITION_REVIEW_COMPLETE55','reviewer':'/root/sourcegraph_creator56','verdict':'ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT','integration_HEAD':head,'science_commit':review['science_commit'],'manifest':manifest,'run':run,'review':record(stage/'exposition-seal55.json'),'readback':record(stage/'readback55.json'),'accepted_scope':'Actual local desktop55 companion statement, six source-attributed formula steps, exact initiallyfolded statement/fullproof, source assumptions/remaining boundary and exact55 branch truth labeling only.','excluded_claims':review['excluded_claims'],'presentation_debts':len(review['presentation_debts']),'compiler':'NOT_STARTED_CLOSED','canonical_mutations':False,'56_evidence_mutations':False})
common={'schema_version':1,'kind':'ACTUAL_SCOPED_EXPOSITION_RESOURCE_LEASE55','reviewer':'/root/sourcegraph_creator56','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CLOSED','scope':str(stage.resolve()),'readback':'PASS','integration_HEAD':head,'science_commit':review['science_commit'],'open_lease':record(stage/'lease.open.json'),'manifest':manifest,'run':run,'complete':complete,'retained_background_jobs':0,'retained_sessions':0,'read_write_closure':'Explicit file handles all context-managed; final lease handle closes before synchronous process returns.','process_closure':'Readback builder observed exit0 before closure. Parent exec_command exit0 for this closer is actual final writer termination; do not substitute self-written status for that observation.','compiler':'NOT_STARTED_CLOSED','compiler_processes_started':0,'accepted_scope':'Bounded local desktop exposition55 only; excluded claims in complete/review preserved.'}
resources={}
for name,kind in [('read.lease.json','READ'),('write.lease.json','WRITE'),('python.lease.json','PYTHON'),('compiler.lease.json','COMPILER')]:resources[name]=seal(name,dict(common,resource=kind))
lease=seal('lease.json',dict(common,resource='COMPOSITE',named_resource_leases=resources))
print(json.dumps({'review':record(stage/'exposition-seal55.json'),'manifest':manifest,'run':run,'complete':complete,'lease':lease,'verdict':'ACCEPTED_SCOPED_WITH_PRESENTATION_DEBT','compiler':'NOT_STARTED_CLOSED'}))
