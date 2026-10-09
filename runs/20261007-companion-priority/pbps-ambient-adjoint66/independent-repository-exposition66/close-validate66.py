import os,pathlib,json,hashlib,datetime
O=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((O/n).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
run=load('review-run.json');h=run.pop('run_sha256');assert sha(json.dumps(run,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==h
for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json']:
 j=load(n);assert j['actual_exit']==0 and j['terminal_closed']
 for k in ['stdout','stderr']:z=j[k];assert sha((O/z['name']).read_bytes())==z['RAW_sha256']
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 z=load('raw-payload-bindings.json')[k];assert sha((O/z['name']).read_bytes())==z['RAW_sha256']
assert load('readback.result.json')['status']=='PASS'
j={'schema':'repo66-actual-foreground-close-validator-v1','actual_foreground_PID':os.getpid(),'validated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','whole_logical_run_sha256':h,'current_graph_freshness_admission':False,'source_mathematical_repair':False,'all_finalizer_and_readback_actual_exits':0,'canonical_writes':False}
(O/'close-validator.result.json').write_bytes(json.dumps(j,sort_keys=True,indent=2).encode()+b'\n');print(json.dumps(j))
