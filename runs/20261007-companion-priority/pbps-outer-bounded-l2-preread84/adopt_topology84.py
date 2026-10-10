from pathlib import Path
import copy,hashlib,json
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('raw_sha256' in x or 'RAW_sha256' in x):
   actual=pin(x['path']);assert actual['RAW_sha256']==x.get('raw_sha256',x.get('RAW_sha256')),x['path']
   if 'bytes' in x or 'RAW_bytes' in x:assert actual['RAW_bytes']==x.get('bytes',x.get('RAW_bytes')),x['path']
  for value in x.values():verify(value)
 elif isinstance(x,list):
  for value in x:verify(value)
def checked(p,h):
 assert pin(p)['RAW_sha256']==h,p
 x=load(p);verify(x);return x
top=r/'independent-topology84/closed-RAW-manifest84.json';checked(top,'0cf8c6cf72c0b9a80433ead44aaccb88d5802cfe004db3deb6aac186b2fd656b')
review=r/'overlay-review84/topology-overlay.run-manifest84.json';checked(review,'5548e80396c8a3a9285a09075e34a4dd7300ed1acbeb21c03575a84e957933f5')
decision=checked(r/'overlay-review84/topology-overlay.decision84.json','eafcb63f0d819023fa1f68d303e997e936c7d6939f9576c6e0ec98bf57cb9035')
assert decision['verdict']=='ACCEPT_EXACT_TOPOLOGY_OVERLAY' and not decision['blocking_deltas'] and not decision['additional_required_repairs']
overlay=r/'independent-topology84/proposed-minimal-topology-overlay84.json';o=checked(overlay,'25287eb89eaa17c29feac3d55a401af06a49abfe47181e6d35b3df7b89911577')
g=load(r/'source_proof_graph84.json');i=load(r/'source_inventory84.json');assert len(o['operations'])==8
one=lambda xs,k,v:next(x for x in xs if x[k]==v)
for operation in o['operations']:
 kind=operation['operation']
 if kind=='append_node':
  assert not any(x['id']==operation['value']['id'] for x in g['nodes']);g['nodes'].append(copy.deepcopy(operation['value']))
 elif kind=='replace_edge_field':
  x=one(g['edges'],'id',operation['edge_id']);assert x[operation['field']]==operation['old'];x[operation['field']]=operation['new']
 elif kind=='append_edge':
  assert not any(x['id']==operation['value']['id'] for x in g['edges']);g['edges'].append(copy.deepcopy(operation['value']))
 elif kind=='append_junction_edge':
  x=one(g['junctions'],'id',operation['junction_id']);assert operation['value'] not in x['edges'];x['edges'].append(operation['value'])
 elif kind=='replace_junction_field':
  x=one(g['junctions'],'id',operation['junction_id']);assert x[operation['field']]==operation['old'];x[operation['field']]=operation['new']
 elif kind=='append_inventory_graph_node':
  x=one(i['items'],'id',operation['inventory_id']);assert operation['value'] not in x['graph_nodes'];x['graph_nodes'].append(operation['value'])
 elif kind=='append_scope_coverage_graph_node':
  x=one(g['scope_coverage'],'inventory_id',operation['inventory_id']);assert operation['value'] not in x['graph_nodes'];x['graph_nodes'].append(operation['value'])
 elif kind=='replace_graph_counts':
  assert g['counts']==operation['old'];g['counts']=operation['new']
 else:raise AssertionError(kind)
assert g['counts']==dict(inventory=47,nodes=23,relations=39,dependency_edges=37,excluded_associations=2)
nodes={x['id'] for x in g['nodes']};edges=[x for x in g['edges'] if x.get('dependency_edge',True)];assert len(edges)==37
pending={x:set() for x in nodes}
for x in edges:assert x['from'] in nodes and x['to'] in nodes;pending[x['to']].add(x['from'])
removed=[]
while pending:
 ready=[x for x,parents in pending.items() if not parents];assert ready,'Dependency cycle'
 for x in ready:removed.append(x);del pending[x]
 for parents in pending.values():parents.difference_update(ready)
g['reviewed_overlay']=pin(overlay);g['truth_boundary']='Independent source topology plus separately reviewed exact overlay only; original frozen bytes unchanged. No84 header, Statement Seal, proof or completion credit.'
def new(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
gp=r/'source_proof_graph84.reviewed-effective.json';ip=r/'source_inventory84.reviewed-effective.json';new(gp,g);new(ip,i)
new(r/'root.topology-adoption84.json',dict(independent_topology=pin(top),distinct_exact_overlay_review=pin(review),native_overlay_decision=pin(r/'overlay-review84/topology-overlay.decision84.json'),adopted_overlay=pin(overlay),effective_graph=pin(gp),effective_inventory=pin(ip),counts=g['counts'],dependency_DAG_acyclic=True,future_OPEN_dependencies=5,originals_unchanged=True,StatementSeal=False,proof=False,VERIFIED=False))
print('84 reviewed source graph/inventory mechanically adopted:47/23/39,37deps+2associations; no84 header/proof credit')
