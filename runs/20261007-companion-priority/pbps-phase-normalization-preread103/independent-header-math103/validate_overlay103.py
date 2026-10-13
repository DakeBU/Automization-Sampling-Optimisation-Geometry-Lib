from pathlib import Path
import json,hashlib,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;S=R/'runs/20261007-companion-priority/pbps-actual-weighted-sector102/next-primary103';N=S/'graph-normalization103'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
bound={}
def checkref(x):
 p=R/x['path']
 if x['path'] in ['website/content/samplewiki_companion_frontiers.json','docs/companion-papers-handoff.md'] and info(p)['raw_sha256']!=x['raw_sha256']:
  recovery=load(O/'context-provenance-resolution103.native.json')
  row=next(z for z in recovery['resolutions'] if z['original_path']==x['path'])
  recovered=info(R/row['preserved_snapshot']['path']);assert recovered['raw_sha256']==x['raw_sha256'] and recovered['bytes']==x['bytes'];bound[recovered['path']]=recovered
  return
 assert info(p)['raw_sha256']==x['raw_sha256'],x['path'];bound[x['path']]=info(p)
 if 'bytes' in x:assert info(p)['bytes']==x['bytes']
def refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v and 'line_start' not in v:checkref(v)
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
orig=load(O/'closed-RAW-original-review103.native.json');refs(orig)
oc=N/'closed-RAW-manifest103.native.json';ov=N/'source-api-identity-normalization103.native.json'
assert info(oc)['raw_sha256']=='968dbef54c30dcbe9659e4143eaa4e5f32ccae708404b9ab47a91ea2d8431f37'
assert info(ov)['raw_sha256']=='e1f75bcff461bde4e8bb9a66d16a8534fa9d5a7d782389a8645d064167cf1bd5'
refs(load(oc));overlay=load(ov);refs(overlay);refs(load(S/'closed-RAW-manifest103.native.json'))
assert overlay['author']=='/root/source_final96' and not overlay['self_topology_validation'] and not overlay['proof_credit']
api=(R/overlay['pinned_API_source']['path']).read_bytes().splitlines(keepends=True)
for x in overlay['namespace_evidence'].values():assert sha(b''.join(api[x['line_start']-1:x['line_end']]))==x['raw_sha256']
docs={x['input']['path']:load(R/x['input']['path']) for x in overlay['corrections']};original=copy.deepcopy(docs)
assert len(overlay['corrections'])==4
for x in overlay['corrections']:
 assert x['operation']=='replace-exact-string-only' and x['new']==x['old'].replace('MeasureTheory.Measure.prod_withDensity','MeasureTheory.prod_withDensity')
 parts=x['json_pointer'].strip('/').split('/');p=docs[x['input']['path']]
 for part in parts[:-1]:p=p[int(part)] if isinstance(p,list) else p[part]
 key=int(parts[-1]) if isinstance(p,list) else parts[-1];assert p[key]==x['old'];p[key]=x['new']
for p,h in overlay['effective_document_canonical_sha256'].items():assert sha(canon(docs[p]))==h
graph=docs[info(S/'source-proof-graph-delta103.native.json')['path']]
for x in graph['existing_compiled_leaves_referenced']:checkref(x['artifact'])
# Reconstruct the previously independently admitted unchanged base without executing old scripts.
g=load(R/graph['inherited_delta']['path']);g101=load(R/g['base101']['path']);g99=load(R/g101['base_graph']['path']);d100=load(R/g101['prior_delta100']['path']);o100=load(R/g101['unchanged_overlay100']['path']);o102=load(R/graph['inherited_alias_overlay']['path'])
for obj in [g,g101,g99,d100,o100,o102]:refs(obj)
nodes={n['id'] for n in g99['nodes']}|set(d100['new_required_slice'])|{'RHO99'}|{n['id'] for n in g101['nodes_added']}|{n['id'] for n in g['nodes_added']}
edges={(e['from'],e['to']) for e in g99['edges']}|{tuple(e) for e in d100['delta_edges']}|{(e['from'],e['to']) for e in o100['changes'][1]['edges']}
edges-={(a,'WEIGHT100') for a in ['GIBBS98','SURV100','PRODUCT99','RENERGY']};edges|={(e['from'],e['to']) for e in g101['required_AND_edges']}
edges-={('WEIGHT100','SECTOR100'),('THETA97','SECTOR100')};edges|={(e['source'],e['target']) for e in g['AND_edges']}
nodes.remove('RHO97')
for op in o102['edge_operations']:
 e=op['old'];edges.remove((e['source'],e['target']))
 if op['operation']=='replace':e=op['new'];edges.add((e['source'],e['target']))
assert len(nodes)==42 and len(edges)==61 and nodes==set(graph['base_canonical_ids'])
base_nodes=set(nodes);base_edges=set(edges)
nodes|={n['id'] for n in graph['new_local_ingredient_nodes']}|{n['id'] for n in graph['existing_compiled_leaves_referenced']}
for group in graph['AND_dependency_groups']:
 for a in group['sources']:edges.add((a,group['target']))
assert all(a in nodes and b in nodes for a,b in edges)
todo=set(nodes);order=[]
while todo:
 ready=sorted(n for n in todo if not any(b==n and a in todo for a,b in edges));assert ready,'dependency cycle';order+=ready;todo.difference_update(ready)
def ancestors(target):
 seen=set();todo=[target]
 while todo:
  for a,b in edges:
   if b==todo[0] and a not in seen:seen.add(a);todo.append(a)
  todo.pop(0)
 return seen
assert 'SECTOR102-UNNORM' not in ancestors('NORM')
assert {a for a,b in edges if b=='SECTOR100'}=={'NORM','SECTOR102-UNNORM'}
assert 'MeasureTheory.prod_withDensity' in ancestors('NORM')
assert graph['node_refinement']['id']=='NORM' and not graph['certified_Lean_edges_added']
cov=load(S/'source-coverage-delta103.native.json');basecov=load(R/graph['base_effective102']['path'])
assert len(cov['regions'])==21 and {x['id'] for x in cov['regions']}=={x['id'] for x in basecov['source_regions']}
raw=(R/cov['primary']['path']).read_bytes()
for x in cov['regions']:
 assert sha(raw[x['byte_start']:x['byte_end_exclusive']])==x['raw_sha256']
 assert sha(b''.join(raw.splitlines(keepends=True)[x['line_start']-1:x['line_end']]))==x['raw_sha256']
assert (O/'context-provenance-resolution103.native.json').exists(), 'selected mathematics checked; awaiting context provenance record'
save('source-topology-admission103.native.json',dict(decision='ACCEPT_BASE_PLUS_API_IDENTITY_OVERLAY_TOPOLOGY_AND_COVERAGE',reviewer='/root/exact_verifier96',review_mode='Independent noncreator validation after separately frozen primary/header mathematical reconstruction; no claim that inherited context was unseen.',header=info(O.parent/'Header103.lean'),source_first_route=info(O/'source-first-route103.native.json'),original_negative=info(O/'source-topology-decision103.original.native.json'),original_closed_review=info(O/'closed-RAW-original-review103.native.json'),base_graph=info(S/'source-proof-graph-delta103.native.json'),overlay=info(ov),overlay_closure=info(oc),exact_four_string_repairs_only=True,historical_scheduling_context_recovery=info(O/'context-provenance-resolution103.native.json'),mathematical_incidence_unchanged=True,effective_graph=dict(base_nodes=42,base_edges=61,new_local_ingredient_nodes=['VY-DOM103','PHASE-FACTOR103'],existing_API_nodes_referenced=7,nodes_including_API_references=len(nodes),edges=len(edges),acyclic=True,topological_order=order,new_edges=[list(x) for x in sorted(edges-base_edges)],stable_target='NORM',same_witness_contract102_retained=o102['same_witness_contract']),coverage=dict(all21_RAW_slices_rehashed=True,all_inherited_source_ids_retained=True,selected_regions=['standing-curvature','standing-eta','target-position-energy','phase-gibbs-law'],later_averaging_separately_excluded=True,actual_energy_and_phase_order=True,normalizer_proportionality_expanded_without_extra_binders=True),required_dependency_audit=['H99 Hessian/C2 supplies strong convexity and exp(-V) integrability.','H99 eta positivity and DEFWEIGHT101 literal target energy supply proximal domination, hence VY-DOM103 and Zx positivity.','VY-DOM103, exact Gaussian integral and product integration supply PHASE-FACTOR103; scalar sqrt/natural-power conversion recorded explicitly as an internal side condition.','PHASE-FACTOR103, tilted definition, measurable density representatives, stdGaussian density and product-withDensity supply NORM.','NORM is analytically independent of102. Only future normalized SECTOR100 jointly needs NORM and SECTOR102-UNNORM.'],omitted_ordinary_API_details='Measurability, positivity, tilted expansion and real/ENNReal scalar conversion are explicit ingredient side conditions on the associated nodes, not new public assumptions.',missing_dependency_edges=[],remaining_defects=[],no_header_change=True,no_proof_implementation=True,no_claim_or_seal=True,no_VERIFIED=True,no_creator_self_validation=True,no_full_primary_copy=True))
save('closed-RAW-review103.native.json',dict(status='CLOSED_PROSPECTIVE_HEADER_MATH_AND_CORRECTED_TOPOLOGY_ACCEPTED',reviewer='/root/exact_verifier96',inputs=list(bound.values())+[info(ov),info(oc)],owned_artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_intentionally_omitted=True,original_negative_preserved=True,no_proof_credit=True,no_full_primary_copy=True))
for n in ['header-math-decision103.native.json','source-topology-admission103.native.json','closed-RAW-review103.native.json']:print(json.dumps(info(O/n)),flush=True)
