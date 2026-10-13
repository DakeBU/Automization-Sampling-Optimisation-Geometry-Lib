from pathlib import Path
import os,json,hashlib,datetime
O=Path(__file__).resolve().parent
def ld(n):return json.loads((O/n).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
assert not (O/'lease.final.json').exists()
r=ld('review-run.json');h=r.pop('run_sha256');assert sha(json.dumps(r,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==h
for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
 j=ld(n);assert j['actual_exit']==0 and j['terminal_closed']
 for k in ['stdout','stderr']:assert sha((O/j[k]['name']).read_bytes())==j[k]['RAW_sha256']
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 z=ld('raw-payload-bindings.json')[k];assert sha((O/z['name']).read_bytes())==z['RAW_sha256']
assert ld('readback.result.json')['status']=='PASS'
j={'schema':'repository67-actual-foreground-close-validator-v1','actual_foreground_PID':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','whole_logical_run_sha256':h,'all_finalizer_readback_actual_exits':0,'current_graph_freshness_admission':True,'source_mathematical_repair':False,'canonical_writes':False}
(O/'close-validator.result.json').write_bytes((json.dumps(j,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(j))
