import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def j(n):return json.loads((O/n).read_bytes())
def check(p):
 b=(R/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==p['bytes'] and len(l)==p['lf_bytes'] and sha(b)==p['raw_sha256'] and sha(l)==p['lf_sha256'],p['path']
m=j('input.manifest.json')
for row in m['qualified_raw_LF_pairs']:
 for k in ['original','raw_snapshot','lf_snapshot']:check(row[k])
check(m['primary']);raw=(R/m['primary']['path']).read_bytes()
for row in m['primary_regions']:
 lo,hi=row['byte_range'];assert sha(raw[lo:hi])==row['qualified_raw_slice']['raw_sha256']
for x in j('api.lookup.review.json')['qualified_native_API_maps']:
 for k in ['original','selected_raw','selected_LF']:check(x[k])
 lines=(R/x['original']['path']).read_bytes().splitlines(keepends=True);lo,hi=x['lines'];assert b''.join(lines[lo-1:hi])==(R/x['selected_raw']['path']).read_bytes()
d=j('statement-binder.decision.sealed.json');assert d['verdict']=='accepted-preproof-source-contract' and d['excess_count']==0 and d['repairs']==[] and d['blocking_issues']==[]
assert j('source.coverage.before-candidate.json')['item_count']==45
assert len(j('source.graph.before-candidate.json')['nodes'])==14 and len(j('source.graph.before-candidate.json')['hyperedges'])==9
mode=sys.argv[1]
if mode=='final':
 run=j('run.json');assert run['run_sha256']==sha(canon({k:v for k,v in run.items() if k!='run_sha256'}));check(run['named_payload'])
 for p in run['sealed_support_outputs']:check(p)
 payload=j('named-preproof.payload.json');assert payload['complete_decision']==d and payload['complete_input_manifest']==m
 assert j('statement-binder.review.json')==dict(d,review_run_sha256=run['run_sha256'])
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode=mode,all_checks='PASS',run_sha256=run['run_sha256'],payload_sha256=run['named_payload']['raw_sha256'],pairs=44,no_proof_credit=True)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode=mode,all_checks='PASS',pairs=44,no_proof_credit=True)))
