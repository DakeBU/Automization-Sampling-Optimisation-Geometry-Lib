"""Adopt only the exact, distinctly reviewed source-topology overlay. No proof credit."""
from pathlib import Path
import json,hashlib,copy,datetime
R=Path('E:/Samplinglib');D=Path(__file__).parent
def load(p): return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def verify(x):
 if isinstance(x,dict):
  h=x.get('raw_sha256',x.get('RAW_sha256'))
  if h and 'path' in x:
   p=R/x['path'];a=pin(p);assert a['raw_sha256']==h,x['path']
   n=x.get('bytes',x.get('RAW_bytes'));assert n is None or n==a['bytes'],x['path']
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
def checked(p,h):
 assert pin(p)['raw_sha256']==h,p
 x=load(p);verify(x);return x
t=D/'independent-topology86/closed-RAW-manifest86.authoritative.json'
checked(t,'7970ce0bde03f67e6ac472f74644d71a8beddb1023768069bebff327e862854e')
m=D/'overlay-review86/overlay-review.run-manifest86.json'
checked(m,'ebf6a7d0188be0d5b16f3b8f5952dc1b2750b193cb2bf9a3f612f40f033faf51')
dec=D/'overlay-review86/overlay-review.decision86.json'
a=checked(dec,'c45e58b10c64a063bfffa38beecd7f4279f102cae9dc895f778749ea94bc942a')
assert a['verdict']=='ACCEPT_EXACT_OVERLAY_SOURCE_TOPOLOGY_ONLY' and not a['gaps'] and not a['required_additional_repairs'] and a['all_before_after_operations_accepted']
op=D/'independent-topology86/proposed-topology-overlay86.json'
o=checked(op,'a8bff963452d39a1b971a90a4c68c5737ef519d9b7266294483ebf6694d3370d')
originals={n:pin(D/n) for n in ['source-proof-graph86.json','source-inventory86.json']}
g=load(D/'source-proof-graph86.json');i=load(D/'source-inventory86.json')
assert len(o['operations'])==len(a['operation_results'])==19
for item in o['operations']:
 target=g if item['file']=='graph' else i
 if item['action']=='append':
  collection='nodes' if item['id'].startswith('G') else 'edges'
  assert not any(x['id']==item['id'] for x in target[collection])
  assert item['before'] is None;target[collection].append(copy.deepcopy(item['after']))
 elif item['action']=='replace':
  f=item['field']
  if f.startswith('junction.routes['):
   key=f.split('[',1)[1].split(']',1)[0]
   junction=next(x for x in g['junctions'] if x['target']==item['id'])
   row=next(x for x in junction['routes'] if x['route']==key);field='ingredients'
  else:
   collection='nodes' if item['file']=='graph' else 'items'
   row=next(x for x in target[collection] if x['id']==item['id']);field=f
  assert row[field]==item['before'],item
  row[field]=copy.deepcopy(item['after'])
 else:raise AssertionError(item)
deps=[e for e in g['edges'] if e['dependency_edge']]
assert (len(i['items']),len(g['nodes']),len(g['edges']),len(deps))==(40,37,71,68)
assert len(g['edges'])-len(deps)==3
pending={n['id']:set() for n in g['nodes']}
for e in deps:assert e['from'] in pending and e['to'] in pending;pending[e['to']].add(e['from'])
while pending:
 ready=[n for n,p in pending.items() if not p];assert ready,'cycle'
 for n in ready:del pending[n]
 for p in pending.values():p.difference_update(ready)
anchors={x['source_id'] for x in i['anchors']}; covered={s for x in i['items'] for s in x['source_ids']}
assert len(anchors)==56 and anchors<=covered
def new(p,x):
 assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
gp=D/'source-proof-graph86.reviewed-effective.json';ip=D/'source-inventory86.reviewed-effective.json'
new(gp,g);new(ip,i)
for n,p in originals.items():assert pin(D/n)==p
z={'accepted':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'independent_topology_proposal_manifest':pin(t),'distinct_primary_first_exact_overlay_review':pin(m),'native_decision':pin(dec),'adopted_overlay':pin(op),'originals':originals,'effective_graph':pin(gp),'effective_inventory':pin(ip),'counts':o['prospective_counts'],'dependency_DAG_acyclic':True,'all56_anchors_mapped':True,'originals_unchanged':True,'parent_BODY_read_deviation_retained':True,'fresh_distinct_primary_first_review_is_admission_basis':True,'original_graph_inventory_pointer_retained_as_preoverlay_provenance':True,'StatementSeal':False,'proof':False,'VERIFIED':False}
new(D/'root.topology-adoption86.json',z)
print(json.dumps({'accepted_source_topology_only':True,'effective_counts':z['counts'],'no_proof_credit':True}))
