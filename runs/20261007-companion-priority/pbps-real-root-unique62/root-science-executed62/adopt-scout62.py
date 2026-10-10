from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-real-root-unique-preproof62');d=Path('runs/20261007-companion-priority/pbps-real-defect-root61/next-macro-source62');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run=load(d/'run.json');lease=load(d/'lease.json');assert lease['status']=='CLOSED_LAST' and lease['readback_exit_code']==0
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='1aa1f8bbd60884c0fd8017c74993242bfcff43237f0615bd5053f2e0958564a8'
assert sha(can(run['named_source_API_payload']))==run['named_source_API_payload_sha256']==lease['named_source_API_payload_sha256']=='033b2b34661ab47f48764c6b3dbbc5027663ede89802b697c879708cb565e844'
seen=set()
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():
   key=(str(Path(x['path']).resolve()),x['raw_sha256'],x['lf_sha256'])
   if key not in seen:
    b=Path(x['path']).read_bytes();z=b.replace(b'\r\n',b'\n');assert sha(b)==x['raw_sha256'] and sha(z)==x['lf_sha256'],x['path']
    for k,v in [('bytes',len(b)),('raw_bytes',len(b)),('lf_bytes',len(z))]:
     if k in x:assert x[k]==v
    seen.add(key)
  for y in x.values():walk(y)
 elif isinstance(x,list):
  for y in x:walk(y)
for p in d.glob('*.json'):walk(load(p))
types=[]
for i in range(2):
 p=r/f'type-header{i}/receipt.json';q=load(p);assert q['exit_code']==0 and q['terminal_closed'];walk(q);types.append(dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()),actual_PID=q['actual_foreground_pid'],exit_code=0))
out=dict(status='INDEPENDENT_SCOUT62_AND_EXACT_TYPE_PROBES_ADOPTED_NOT_STATEMENT_SEALED_NOT_CLAIMED',native_whole_run_sha256=run['run_sha256'],named_source_API_payload_sha256=run['named_source_API_payload_sha256'],recipes=run['hash_recipes'],qualified_pin_readbacks=len(seen),source_graph=(d/'source-proof-graph.json').as_posix(),source_contract=(d/'contracts.json').as_posix(),source_API_manifest=(d/'input.manifest.json').as_posix(),types=types,selected='REAL_POSITIVE_ROOT_UNIQUENESS_BEFORE_CANONICAL_MACRO_TRANSPORT',parent61_science_commit='bcd245d90b21b899acb9937fc54dffcea20e86ee',parent61_exact_verification_pending=True,no62proof_search=True,no62claim=True)
p=r/'root.scout62-and-type.adoption.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Adopted native independent62 scout and two type-only EXIT0/CLOSED receipts;',len(seen),'qualified pins. No statement seal/claim/proof.')
