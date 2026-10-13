import os,pathlib,json,hashlib,datetime
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def canon(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
run=load(O/'review-run.json');expected=run.pop('run_sha256');assert sha(canon(run))==expected
b=load(O/'raw-payload-bindings.json');assert b['whole_logical_run_sha256']==expected
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 z=b[k];p=O/z['name'];raw=p.read_bytes();assert len(raw)==z['RAW_bytes'] and sha(raw)==z['RAW_sha256'];assert sha(raw.replace(b'\r\n',b'\n'))==z['LF_sha256']
assert load(O/'complete-RAW-decision.json')==run['decisions'][0]==load(O/'decision.json')
assert load(O/'RAW-input-payload.json')==run['complete_named_RAW_INPUT_payload']['complete_payload']
for z in run['pre_finalization_owned_RAW_LF_bindings']:
 p=O/z['name'];raw=p.read_bytes();assert len(raw)==z['RAW_bytes'] and sha(raw)==z['RAW_sha256'],p.name
for n in ['inputs.manifest.json','reader-inputs.manifest.json']:
 for z in load(O/n)['inputs']:
  raw=pathlib.Path(z['RAW_snapshot']['path']).read_bytes();normal=pathlib.Path(z['LF_snapshot']['path']).read_bytes();assert sha(raw)==z['original']['RAW_sha256'] and normal==raw.replace(b'\r\n',b'\n')
assert run['decisions'][0]['current_graph_freshness_admission'] is False
result={'schema':'repo66-actual-foreground-readback-result-v1','actual_foreground_PID':os.getpid(),'readback_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'whole_logical_run_sha256':expected,'all_complete_RAW_payloads_and_decision_equality':True,'all_pre_finalizer_owned_and_RAW_LF_input_maps_verified':True,'current_graph_freshness_withheld':True,'status':'PASS','external_actual_EXIT_required':True}
(O/'readback.result.json').write_bytes(json.dumps(result,sort_keys=True,indent=2).encode()+b'\n');print(json.dumps(result))
