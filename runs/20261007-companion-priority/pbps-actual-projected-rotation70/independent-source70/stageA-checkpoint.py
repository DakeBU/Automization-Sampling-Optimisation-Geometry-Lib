import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,base64,os,datetime
O=pathlib.Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
J=lambda p:json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
run=J(O/'stageA.preparation-only.run.json');whole=dict(run);whole.pop('run_sha256');assert H(C(whole))==run['run_sha256']
named={}
for n in ['stageA.complete-RAW-review.txt','stageA.preparation-only.run.json','stageA.preparation-only.checks.json','stageA.source-expectations70.before-current-BODY.frozen.json','stageA.source-proof-graph70.frozen.json','stageA.primary419-NODE-EXCLUDED70.frozen.json','stageA.exhaustive-finite-obligations70.frozen.json','stageA.anti-anchoring-exposure70.frozen.json','stageA.complete-primary-input-manifest.frozen.json','stageA.complete-exact-RAW-LF-input-payload.json']:
 b=(O/n).read_bytes();named[n]={'RAW_bytes':len(b),'RAW_sha256':H(b),'complete_RAW_base64':base64.b64encode(b).decode('ascii')}
save('stageA.complete-named-preparation-review-expectation-input-payload.json',{'schema':'source70-stageA-complete-named-preparation-payload-v1','source_verdict':None,'status':'OPEN_PENDING_OFFICIAL_PACKET','names':named,'current70_BODY_read':False,'not_final_closed_package':True})
prior=J(O/'stageA.prior83.integrity.json');B=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/independent-header-source70')
for e in prior['regular_files_verified']:
 p=B/e['name'];assert H(p.read_bytes())==e['RAW_sha256'] and p.stat().st_mtime_ns==e['mtime_ns']
assert H((B/'lease.final.json').read_bytes())==prior['lease_RAW_sha256'] and H((B/'owned-manifest.json').read_bytes())==prior['manifest_RAW_sha256']
entries=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  raw=p.read_bytes();entries.append({'name':p.relative_to(O).as_posix(),'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_bytes':len(raw.replace(b'\r\n',b'\n')),'LF_sha256':H(raw.replace(b'\r\n',b'\n'))})
save('stageA.bounded-checkpoint-manifest.json',{'schema':'source70-stageA-preparation-checkpoint-manifest-v1','captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'OPEN_PENDING_OFFICIAL_PACKET','not_final_closure_manifest':True,'finite_captured_file_count':len(entries),'entries_canonical_sha256':H(C(entries)),'entries':entries,'excluded_self_and_future_terminal_artifacts':'checkpoint manifest and this foreground receipt/stdout/stderr appear after finite capture; final close must include them','source_graph_nodes':22,'source_graph_edges':49,'source_math_items':419,'frozen_expectations_RAW_sha256':'a1257be6ef44d34f268e7297044392d3a288c5ddb62f38e67cdab33e70fe6c1f','prior83_unchanged_hashes_and_mtimes':True,'last_CLOSED_lease_written':False})
print(json.dumps({'actual_pid':os.getpid(),'finite_checkpoint_files':len(entries),'checkpoint_manifest_RAW_sha256':H((O/'stageA.bounded-checkpoint-manifest.json').read_bytes()),'checkpoint_entries_sha256':H(C(entries)),'named_preparation_payload_RAW_bytes':(O/'stageA.complete-named-preparation-review-expectation-input-payload.json').stat().st_size,'prior83_native_unchanged':True,'current70_BODY_read':False,'source_verdict':None,'OPEN_pending_official_packet':True},ensure_ascii=True))
