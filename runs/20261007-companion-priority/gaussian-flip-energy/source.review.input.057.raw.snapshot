from pathlib import Path
import json,hashlib,copy,datetime
ROOT=Path('E:/Samplinglib'); P='runs/20261007-companion-priority/'
BASE=ROOT/(P+'gaussian-flip-energy-source-graph'); OUT=BASE/'representation-overlay1'
REVIEW=P+'gaussian-flip-energy-source-graph-review/source-topology-review.json'
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(name,obj):
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();(OUT/name).open('xb').write(b);return sha(b)
pins=[]
def pin(path,kind='IMMUTABLE_REPAIR_INPUT'):
 b=(ROOT/path).read_bytes();i=len(pins);r='input.%03d.raw.snapshot'%i;l=r.replace('.raw.','.lf.')
 (OUT/r).open('xb').write(b);(OUT/l).open('xb').write(lf(b))
 p=dict(path=path,raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b),raw_snapshot=r,lf_snapshot=l,kind=kind)
 pins.append(p);return p,b
rv,rb=pin(REVIEW,'DISTINCT_CLOSED_BLOCKED_REPRESENTATION_REVIEW')
assert rv['raw_sha256']==rv['lf_sha256']=='5325a3865fa103198afb4fa166a9d8bca48eeaf2a49c394d804dc222192c8ec4'
review=json.loads(rb);assert review['verdict']=='BLOCKED' and review['blocking']
assert all(review[k]=='CLOSED' for k in ['read_lease','write_lease','compiler_lease']) and not review['compiler_started']
assert review['independent_from_graph_author']
pin(P+'gaussian-flip-energy-source-graph-review/reviewer.topology.lease.closed.json','DISTINCT_REVIEW_CLOSED_LEASE')
original={}
for f in ['source-proof-graph.independent.json','source.inventory.json','source.contract.json','bindings.json','run.closed.json','lease.json','author.py']:
 p,b=pin(P+'gaussian-flip-energy-source-graph/'+f,'ORIGINAL_AUTHOR_ARTIFACT_NEVER_MODIFIED');original[f]=(p,b)
graph=json.loads(original['source-proof-graph.independent.json'][1]);inventory=json.loads(original['source.inventory.json'][1])
contract=json.loads(original['source.contract.json'][1]);bindings=json.loads(original['bindings.json'][1])['inputs']
assert len(graph['nodes'])==68 and len(graph['edges'])==176 and len(graph['OR_routes'])==2 and graph['compiled_edges']==[]
assert len(inventory['regions'])==104 and inventory['physical_lines']==1539 and len(bindings)==45
assert original['source-proof-graph.independent.json'][0]['raw_sha256']==review['graph_raw_sha256']
assert original['source.inventory.json'][0]['raw_sha256']==review['source_inventory_raw_sha256']
assert original['source.contract.json'][0]['raw_sha256']==review['source_contract_raw_sha256']
assert json.loads(original['lease.json'][1])['status']=='CLOSED'
requests=review['repairs'];assert len(requests)==18
raw_pin_checks=[]
for e in bindings:
 for field,digest in [('raw_snapshot','raw_sha256'),('lf_snapshot','lf_sha256')]:
  b=(BASE/e[field]).read_bytes();assert sha(b)==e[digest],e['path']
 raw_pin_checks.append(dict(path=e['path'],raw_snapshot=e['raw_snapshot'],lf_snapshot=e['lf_snapshot'],raw_sha256=e['raw_sha256'],lf_sha256=e['lf_sha256'],unchanged=True))
region_checks=[]
for e in inventory['regions']:
 for field,digest in [('raw_snapshot','raw_sha256'),('lf_snapshot','lf_sha256')]:
  b=(BASE/e[field]).read_bytes();assert sha(b)==e[digest],e['id']
 region_checks.append(dict(id=e['id'],raw_sha256=e['raw_sha256'],lf_sha256=e['lf_sha256'],unchanged=True))
sourcepaths=sorted({r['path'] for r in requests});sources={}
for path in sourcepaths:
 e=next(e for e in bindings if e['path']==path)
 b=(BASE/e['raw_snapshot']).read_bytes();assert sha(b)==e['raw_sha256']
 p,current=pin(path,'EXACT_CALLER_SOURCE_ONLY_SAME_FROZEN_PIN');assert current==b
 sources[path]=(b,e,p)
repaired=copy.deepcopy(graph);append=[];caller_pins=[]
nodeids={n['id'] for n in graph['nodes']}
oldpairs={(e['from_node'],e['to_node']) for e in graph['edges']}
for index,r in enumerate(requests):
 assert r['from_node'] in nodeids and r['to_node'] in nodeids
 assert (r['from_node'],r['to_node']) not in oldpairs
 assert r['kind_requested']=='EXTERNAL_SOURCE_USE'
 b,originalpin,pininfo=sources[r['path']];lines=b.splitlines(keepends=True);uses=[]
 for use in r['uses']:
  snippets=[]
  for line in use['lines']:
   lb=lines[line-1];s=lb.decode('utf-8');assert use['identifier'] in s,(r,use,line,s)
   n=len(caller_pins);raw='caller.%03d.raw.snapshot'%n;norm=raw.replace('.raw.','.lf.')
   (OUT/raw).open('xb').write(lb);(OUT/norm).open('xb').write(lf(lb))
   e=dict(path=r['path'],physical_line=line,identifier=use['identifier'],literal_line=s.rstrip('\r\n'),raw_sha256=sha(lb),lf_sha256=sha(lf(lb)),raw_snapshot=raw,lf_snapshot=norm)
   caller_pins.append(e);snippets.append(e)
  uses.append(dict(identifier=use['identifier'],lines=use['lines'],caller_snapshots=snippets))
 anchor=r['path']+'#'+','.join('L'+str(i) for i in sorted({i for u in r['uses'] for i in u['lines']}))
 edge=dict(id='e%03d'%(177+index),from_node=r['from_node'],to_node=r['to_node'],kind=r['kind_requested'],anchor=anchor,ingredient='Direct source definition/consumer use: '+', '.join(u['identifier'] for u in r['uses'])+'; literal caller anchors retained.',truth_contract='source/API ingredient edge only; no compiled dependency certification',source_uses=dict(path=r['path'],source_raw_sha256=originalpin['raw_sha256'],source_lf_sha256=originalpin['lf_sha256'],uses=[dict(identifier=u['identifier'],lines=u['lines']) for u in r['uses']]))
 repaired['edges'].append(edge)
 append.append(dict(request_index=index,review_request=r,added_edge=edge,caller_evidence=uses))
assert repaired['edges'][:176]==graph['edges']
assert all(repaired[k]==v for k,v in graph.items() if k!='edges')
assert len(repaired['edges'])==194
outpath=BASE/'source-proof-graph.repaired.independent.json'
newbytes=(json.dumps(repaired,ensure_ascii=False,indent=2)+'\n').encode();outpath.open('xb').write(newbytes)
emit('scoped-diff.json',dict(diff_kind='JSON_APPEND_ONLY_EDGES',operations=[dict(op='add',path='/edges/'+str(176+i),value=q['added_edge']) for i,q in enumerate(append)],unchanged_keys=[k for k in graph if k!='edges'],old_edge_prefix_length=176,preserved_nodes=68,preserved_OR_routes=2,compiled_edges=[],new_edge_count=194,mathematical_binder_definition_or_target_change=False))
emit('caller-bindings.json',dict(exact_caller_lines=caller_pins,count=len(caller_pins),source_source_use_only=True))
repair=dict(schema_version=1,artifact_kind='source-graph-representation-author-repair',status='AUTHOR_REPAIRED_FROZEN_PENDING_DISTINCT_REVIEW',actor='gaussian_domain_preproof_reviewer_29',not_self_validation=True,request_receipt=rv,request_run_sha256=review['review_run_sha256'],original_graph=original['source-proof-graph.independent.json'][0],successor_graph=dict(path=P+'gaussian-flip-energy-source-graph/source-proof-graph.repaired.independent.json',raw_sha256=sha(newbytes),lf_sha256=sha(lf(newbytes))),scope='Exactly18 independently requested direct source-use edges appended; no existing field/edge/node/OR/statement/source/binder/formula mutation.',counts=dict(before_nodes=68,after_nodes=68,before_edges=176,after_edges=194,OR_routes=2,source_pins=45,source_regions=104,selected_physical_lines=1539),exact_repairs=append,preservation=dict(original_artifacts=[p for p,b in original.values()],raw_LF_source_pins=raw_pin_checks,raw_LF_regions=region_checks,contract_unchanged=True,inventory_unchanged=True,original_BLOCKED_review_unchanged=True,all_176_original_edges_unchanged=True,all_other_graph_keys_unchanged=True),source_statement_admission='No theorem/binder change requested. Independent prospective37 StatementSeal belongs to phase/root, not claimed by this author repair.',remaining_truth_boundary=graph['remaining_truth_boundary'],compiled_edges=[],compiler_started=False,future37_body_Test_blind_exposure=False,author_acceptance_claim=False,read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED')
emit('repair.json',repair)
emit('bindings.json',dict(inputs=pins,all_raw_LF_bound=True,reused_original45_source_snapshots=raw_pin_checks,source_regions104_unchanged=region_checks))
for p in pins:
 b=(ROOT/p['path']).read_bytes();assert sha(b)==p['raw_sha256'] and sha(lf(b))==p['lf_sha256'],p['path']
outputs=[]
for f in ['repair.json','scoped-diff.json','caller-bindings.json','bindings.json','repair.py']:
 b=(OUT/f).read_bytes();outputs.append(dict(path=P+'gaussian-flip-energy-source-graph/representation-overlay1/'+f,raw_sha256=sha(b),lf_sha256=sha(lf(b))))
outputs.append(repair['successor_graph'])
runid=sha(json.dumps(dict(inputs=pins,outputs=outputs),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
emit('run.closed.json',dict(deterministic_run_sha256=runid,inputs_count=len(pins),outputs=outputs,caller_line_snapshot_count=len(caller_pins),all_original_inputs_unchanged=True,mechanical_author_checks='Exact requested endpoints/kinds/identifiers at literal source caller lines; only18 edge additions, old176prefix and every other field unchanged. This is author construction evidence, NOT independent topology acceptance.',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False))
lease=json.loads((OUT/'lease.json').read_text());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',deterministic_run_sha256=runid,successor_graph_sha256=sha(newbytes))
(OUT/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status='CLOSED',successor_graph_raw_sha256=sha(newbytes),repair_raw_sha256=sha((OUT/'repair.json').read_bytes()),run=runid,nodes=68,edges=194,OR_routes=2,caller_line_snapshots=len(caller_pins),independent_topology_admission=False)))
