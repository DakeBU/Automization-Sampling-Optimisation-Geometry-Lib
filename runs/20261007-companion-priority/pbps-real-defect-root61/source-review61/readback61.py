import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def j(n):return json.loads((O/n).read_bytes())
def check(p):
 b=(R/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n')
 assert len(b)==p['bytes'] and len(l)==p['lf_bytes'] and sha(b)==p['raw_sha256'] and sha(l)==p['lf_sha256'],p['path']
m=j('input.manifest.json')
for row in m['qualified_raw_LF_pairs']:
 for k in ['original','raw_snapshot','lf_snapshot']:check(row[k])
s=j('primary-first.boundary.json');check(s['primary']);p=(R/s['primary']['path']).read_bytes()
assert len(s['source_regions'])==23
for x in s['source_regions']:assert sha(p[x['start_utf8_byte']:x['end_utf8_byte_exclusive']])==x['slice_sha256']
f=j('formula-provider-source.review.json');assert len(f['formula_steps'])==9 and f['private_provider_count']==10 and f['public_proof_count']==2
for i in [0,1]:
 d=j(f'source.{i}.decision.sealed.json');assert len(d['semantic_slots'])==7 and d['repairs']==[] and d['excess_count']==0 and d['blocking_deltas']==0
 assert d['verdict']=='equivalent-after-elaboration'
if len(sys.argv)>1 and sys.argv[1]=='final':
 run=j('run.json');assert run['run_sha256']==sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))
 check(run['named_payload']);payload=j('named-source-review.payload.json')
 assert payload['complete_decisions']==[j(f'source.{i}.decision.sealed.json') for i in [0,1]]
 assert payload['complete_formula_provider_review']==f and payload['complete_input_manifest']==m
 for p in run['sealed_support_outputs']:check(p)
 for i in [0,1]:
  d=j(f'source.{i}.decision.sealed.json');d['review_run_sha256']=run['run_sha256'];assert j(f'source.{i}.review.json')==d
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode='final',pairs=len(m['qualified_raw_LF_pairs']),run_sha256=run['run_sha256'],payload_sha256=run['named_payload']['raw_sha256'],all_checks='PASS',proof_or_compiler_credit=False)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),mode='preseal',pairs=len(m['qualified_raw_LF_pairs']),all_checks='PASS',proof_or_compiler_credit=False)))
