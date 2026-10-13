import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def j(n):return json.loads((O/n).read_bytes())
def ck(p):
 b=(R/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==p['bytes'] and len(l)==p['lf_bytes'] and sha(b)==p['raw_sha256'] and sha(l)==p['lf_sha256'],p['path']
m=j('input.manifest.json')
for row in m['qualified_raw_LF_pairs']:
 for k in ['original','raw_snapshot','lf_snapshot']:ck(row[k])
ck(m['source_primary']);raw=(R/m['source_primary']['path']).read_bytes()
for x in m['primary_regions']:
 lo,hi=x['byte_range'];assert sha(raw[lo:hi])==x['qualified_raw_slice']['raw_sha256']
assert j('compiler.inputs.before.json')['original27']==j('compiler.inputs.after.json')['original27']
assert j('focused.receipt.json')['exit_code']==0 and j('focused.receipt.json')['terminal_closed'] and j('focused.receipt.json')['compiler_runs']==1
for k in ['stdout','stderr','inputs_before','inputs_after']:ck(j('focused.receipt.json')[k])
proof=j('mathematical-proof.review.json');assert len(proof['seven_mathematical_formula_steps'])==7
for x in proof['API_maps_checked']:
 for k in ['original','selected_raw','selected_LF']:ck(x[k])
d=j('mathematical.decision.sealed.json');assert d['verdict']=='accepted-scoped-whole-math62' and d['decoder_not_read'] and d['compiler_runs']==1
assert d['repairs']==[] and d['blocking_issues']==[]
for a in d['public_axioms'].values():assert set(a)=={'propext','Classical.choice','Quot.sound'}
if sys.argv[1]=='final':
 run=j('run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];ck(run['named_payload'])
 for p in run['sealed_support_outputs']:ck(p)
 payload=j('named-mathematics.payload.json');assert payload['complete_decision']==d and payload['complete_mathematical_proof_review']==proof and payload['complete_input_manifest']==m
 assert j('verdict.json')==dict(d,review_run_sha256=run['run_sha256'])
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),all_checks='PASS',mode='final',run_sha256=run['run_sha256'],named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],decoder_read=False,compiler_runs=1)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),all_checks='PASS',mode='preseal',pairs=len(m['qualified_raw_LF_pairs']),compiler_runs=1,decoder_read=False)))
