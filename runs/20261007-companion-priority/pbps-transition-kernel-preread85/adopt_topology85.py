"""Materialize separately reviewed exact source-topology overlay, no proof credit."""
from pathlib import Path
import copy,hashlib,json
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def verify(x):
 if isinstance(x,dict):
  h=x.get('RAW_sha256',x.get('raw_sha256'))
  if 'path' in x and h:
   a=pin(x['path']);assert a['RAW_sha256']==h,x['path']
   n=x.get('RAW_bytes',x.get('bytes'))
   if n is not None:assert a['RAW_bytes']==n,x['path']
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
def checked(p,h):
 assert pin(p)['RAW_sha256']==h,p
 x=load(p);verify(x);return x
top=r/'independent-topology85/closed-RAW-manifest85.json'
checked(top,'263697473fee96b8938e5e89762da23adeff4f53313b989f38d60b53a52ccfb5')
review=r/'overlay-review85/run-manifest85.json'
checked(review,'c32fed2cfdc624019a177876b12b483ee3c739e98371912a2d853256f8ab8ebd')
decision=r/'overlay-review85/decision85.json'
d=checked(decision,'9427dcb5a335f09df8166ef55904117be8b84b7be9d0a06a6ed136e15f96734a')
assert d['verdict']=='ACCEPT_EXACT_PROPOSED_OVERLAY' and not d['blocking_deltas'] and not d['required_additional_repairs']
overlay=r/'independent-topology85/proposed-minimal-topology-overlay85.json'
o=checked(overlay,'0d4911d3f7f495bc7b1a8f9c944eaaf64032a0ddc3c62b57266440a13e8441d9')
original={name:pin(r/name) for name in ['source-proof-graph85.json','source-inventory85.json']}
data={name:load(r/name) for name in original}
assert len(o['operations'])==7
for op in o['operations']:
 target=data[op['file']];s=op['selector']
 if 'field' in s:
  assert target[s['field']]==op['before'];target[s['field']]=copy.deepcopy(op['after'])
 else:
  key='id' if 'id' in s else 'target'
  matches=[(n,x) for n,x in enumerate(target[s['collection']]) if x[key]==s[key]]
  assert len(matches)==1 and matches[0][1]==op['before']
  target[s['collection']][matches[0][0]]=copy.deepcopy(op['after'])
g=data['source-proof-graph85.json'];i=data['source-inventory85.json']
assert len(g['nodes'])==21 and len(g['edges'])==29 and len(i['items'])==16
deps=[e for e in g['edges'] if e['dependency_edge']]
assert len(deps)==26 and sum(not e['dependency_edge'] for e in g['edges'])==3
pending={n['id']:set() for n in g['nodes']}
for e in deps:assert e['from'] in pending and e['to'] in pending;pending[e['to']].add(e['from'])
while pending:
 ready=[n for n,p in pending.items() if not p];assert ready,'cycle'
 for n in ready:del pending[n]
 for p in pending.values():p.difference_update(ready)
def new(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
gp=r/'source-proof-graph85.reviewed-effective.json';ip=r/'source-inventory85.reviewed-effective.json'
new(gp,g);new(ip,i)
for name,p in original.items():assert pin(r/name)==p
new(r/'root.topology-adoption85.json',dict(independent_topology=pin(top),distinct_exact_overlay_review=pin(review),native_decision=pin(decision),adopted_overlay=pin(overlay),originals=original,effective_graph=pin(gp),effective_inventory=pin(ip),counts=o['counts_unchanged'],dependency_DAG_acyclic=True,originals_unchanged=True,StatementSeal=False,proof=False,VERIFIED=False))
print('Source-only topology85 adopted:16/21/29;26 dependencies+3 excluded associations; no proof credit')
