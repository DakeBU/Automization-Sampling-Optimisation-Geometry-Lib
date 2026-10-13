import hashlib,json,os,pathlib,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def j(n):return json.loads((O/n).read_bytes())
def ck(p):
 b=(R/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==p['bytes'] and len(l)==p['lf_bytes'] and sha(b)==p['raw_sha256'] and sha(l)==p['lf_sha256'],p['path']
for name in ['input.manifest.json','supplemental.input.manifest.json']:
 for row in j(name)['qualified_raw_LF_pairs']:
  for k in ['original','raw_snapshot','lf_snapshot']:ck(row[k])
m=j('input.manifest.json');ck(m['primary']);primary=(R/m['primary']['path']).read_bytes();b=j('primary-first.boundary.json')
for x in b['source_regions']:
 a,z=x['byte_range'];assert sha(primary[a:z])==x['qualified_raw_slice']['raw_sha256']
assert len(b['source_regions'])==23 and m['coverage_items']==45 and m['source_nodes']==14 and m['source_hyperedges']==9
proof=j('formula-source.review.json');assert len(proof['formula_steps'])==7 and proof['private_provider_count62']==0 and proof['public_proof_count62']==2
for i in [0,1]:
 d=j(f'source.{i}.decision.sealed.json');assert d['verdict']=='equivalent-after-elaboration' and len(d['semantic_slots'])==7 and d['excess_count']==0 and d['repairs']==[] and d['blocking_issues']==[]
 assert all(not x['blocking'] for x in d['deltas'])
 p=json.loads((R/m['qualified_raw_LF_pairs'][3+i]['raw_snapshot']['path']).read_bytes());assert sha(canon({k:v for k,v in p.items() if k!='packet_sha256'}))==d['reviewer_packet_sha256']==p['packet_sha256'];assert d['publication_binding_sha256']==p['publication_binding_sha256']==proof['bindings_checked'][i]['publication_binding_sha256']
assert j('author.receipt.json')['source_decisions_fixed']
if sys.argv[1]=='final':
 run=j('run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256'];ck(run['named_payload'])
 for p in run['sealed_support_outputs']:ck(p)
 payload=j('named-source-review.payload.json');assert payload['complete_source_decisions']==[j(f'source.{i}.decision.sealed.json') for i in [0,1]] and payload['complete_formula_source_review']==proof
 assert payload['complete_original31_input_manifest']==m and payload['complete_supplemental_manifest']==j('supplemental.input.manifest.json')
 for i in [0,1]:assert j(f'source.{i}.review.json')==dict(j(f'source.{i}.decision.sealed.json'),review_run_sha256=run['run_sha256'])
 print(json.dumps(dict(actual_foreground_pid=os.getpid(),checks='PASS',mode='final',run_sha256=run['run_sha256'],named_source_payload_sha256=run['named_source_payload_sha256'],original_pairs=31,supplemental_pairs=17,compiler=False)))
else:print(json.dumps(dict(actual_foreground_pid=os.getpid(),checks='PASS',mode='preseal',original_pairs=31,supplemental_pairs=17,primary23_coverage45=True,formula_steps=7,compiler=False)))
