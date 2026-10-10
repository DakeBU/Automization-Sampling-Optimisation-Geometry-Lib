from pathlib import Path
import os,json,hashlib,datetime
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def cj(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def ld(n):return json.loads((O/n).read_bytes())
assert not (O/'lease.final.json').exists()
run=ld('review-run.json');r=dict(run);h=r.pop('run_sha256');assert sha(cj(r))==h
b=ld('raw-payload-bindings.json');assert b['whole_logical_run_sha256']==h
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 z=b[k];raw=(O/z['name']).read_bytes();assert len(raw)==z['RAW_bytes'] and sha(raw)==z['RAW_sha256'] and sha(raw.replace(b'\r\n',b'\n'))==z['LF_sha256']
assert ld('decision.json')==ld('complete-RAW-decision.json')==run['decisions'][0]
assert ld('RAW-input-payload.json')==run['complete_named_RAW_INPUT']['complete_payload']
for z in run['pre_finalization_owned_RAW_LF_bindings']:
 raw=(O/z['name']).read_bytes();assert len(raw)==z['RAW_bytes'] and sha(raw)==z['RAW_sha256'],z['name'];assert sha(raw.replace(b'\r\n',b'\n'))==z['LF_sha256']
for n in ['inputs.manifest.initial-SCI.json','inputs.manifest.final.json','inputs.manifest.negatives.json']:
 for z in ld(n)['inputs']:
  raw=Path(z['RAW_snapshot']['path']).read_bytes();normal=Path(z['LF_snapshot']['path']).read_bytes();assert sha(raw)==z['original']['RAW_sha256'] and normal==raw.replace(b'\r\n',b'\n')
g=ld('current-graph-and-publication-bindings.json');assert sha(Path(g['current_graph']['path']).read_bytes())==g['current_graph']['RAW_sha256']
for z in g['exact_final_cells']:assert sha((Path('E:/Samplinglib')/z['path']).read_bytes())==z['raw_sha256']
j={'schema':'repository67-actual-foreground-readback-result-v1','actual_foreground_PID':os.getpid(),'readback_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','whole_logical_run_sha256':h,'whole_object_deletion':'ONLY top-level run_sha256','all_complete_named_RAW_and_decision_equality':True,'all_pre_finalizer_owned_RAW_LF_and99_finite_input_maps_verified':True,'current_final_cells_and_graph_unchanged':True,'current_graph_freshness_admission':True,'external_actual_exit_required':True}
(O/'readback.result.json').write_bytes((json.dumps(j,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(j))
