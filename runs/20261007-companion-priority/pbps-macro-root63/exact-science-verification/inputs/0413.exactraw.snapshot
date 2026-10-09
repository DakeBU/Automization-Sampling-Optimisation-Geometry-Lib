from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-real-root-unique62');d=r/'next-macro-source63';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run=load(d/'run.json');lease=load(d/'lease.json');assert lease['status']=='CLOSED_LAST' and lease['actual_foreground_readback']['exit_code']==0 and lease['actual_foreground_readback']['terminal_closed']
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['run_sha256']=='e958132a9014172ff31fb6f5e34c49f52b53b9b0c70ec7b6e0785046eecb6766'
assert sha(can(run['named_source_API_payload']))==run['named_source_API_payload_sha256']==lease['named_source_API_payload_sha256']=='a50698559ff7edae70bc915a572086056d1a877a022b4de228ff23f2af99ef36'
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
out=dict(status='INDEPENDENT_SCOUT63_ADOPTED_CONDITIONAL_ON62_VERIFIED_AND_NEW_STATEMENT_SOURCE_TOPOLOGY_SEALS',native_whole_run_sha256=run['run_sha256'],named_source_API_payload_sha256=run['named_source_API_payload_sha256'],qualified_pin_readbacks=len(seen),source_contract=(d/'contracts.json').as_posix(),source_graph=(d/'source-boundary-graph.pre-API.json').as_posix(),no63proof_search=True,no63claim=True)
p=r/'root.scout63.adoption.json';assert not p.exists();p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('Adopted closed independent scout63;',len(seen),'exact current pins; no proof/claim/seal/admission.')
