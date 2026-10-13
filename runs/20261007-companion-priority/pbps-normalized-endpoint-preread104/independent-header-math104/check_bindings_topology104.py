from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
S=R/'runs/20261007-companion-priority/pbps-actual-phase-normalization103/next-primary104'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
bound={}
def refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v and 'line_start' not in v:
   p=R/v['path'];i=info(p);assert i['raw_sha256']==v['raw_sha256'],v['path'];assert 'bytes' not in v or i['bytes']==v['bytes'];bound[v['path']]=i
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in S.glob('*.json'):refs(load(p));bound[p.relative_to(R).as_posix()]=info(p)
g104=load(S/'source-proof-graph-delta104.native.json');base=load(R/g104['base_source_graph103']['path'])
g=load(R/base['inherited_delta']['path']);g101=load(R/g['base101']['path']);g99=load(R/g101['base_graph']['path']);d100=load(R/g101['prior_delta100']['path']);o100=load(R/g101['unchanged_overlay100']['path']);o102=load(R/base['inherited_alias_overlay']['path'])
for x in [g,g101,g99,d100,o100,o102]:
 # The inherited mathematical graph is reused; historical scheduling snapshots are not replayed.
 pass
nodes={n['id'] for n in g99['nodes']}|set(d100['new_required_slice'])|{'RHO99'}|{n['id'] for n in g101['nodes_added']}|{n['id'] for n in g['nodes_added']}
edges={(e['from'],e['to']) for e in g99['edges']}|{tuple(e) for e in d100['delta_edges']}|{(e['from'],e['to']) for e in o100['changes'][1]['edges']}
edges-={(a,'WEIGHT100') for a in ['GIBBS98','SURV100','PRODUCT99','RENERGY']};edges|={(e['from'],e['to']) for e in g101['required_AND_edges']}
edges-={('WEIGHT100','SECTOR100'),('THETA97','SECTOR100')};edges|={(e['source'],e['target']) for e in g['AND_edges']}
nodes.remove('RHO97')
for op in o102['edge_operations']:
 e=op['old'];edges.remove((e['source'],e['target']))
 if op['operation']=='replace':e=op['new'];edges.add((e['source'],e['target']))
assert (len(nodes),len(edges))==(42,61)
nodes|={n['id'] for n in base['new_local_ingredient_nodes']}|{n['id'] for n in base['existing_compiled_leaves_referenced']}
for group in base['AND_dependency_groups']:
 edges|={(a,group['target']) for a in group['sources']}
wrong='MeasureTheory.Measure.prod_withDensity';right='MeasureTheory.prod_withDensity'
assert wrong in nodes;nodes.remove(wrong);nodes.add(right);edges={(right if a==wrong else a,right if b==wrong else b) for a,b in edges}
assert (len(nodes),len(edges))==(51,79)
before=set(edges);nodes|={n['id'] for n in g104['new_nodes']}
for group in g104['AND_dependency_groups']:edges|={(a,group['target']) for a in group['sources']}
assert all(a in nodes and b in nodes for a,b in edges)
todo=set(nodes);order=[]
while todo:
 ready=sorted(n for n in todo if not any(b==n and a in todo for a,b in edges));assert ready,'cycle';order+=ready;todo.difference_update(ready)
cov=load(S/'source-coverage-delta104.native.json');primary=(R/cov['primary']['path']).read_bytes();lines=primary.splitlines(keepends=True)
assert len(cov['regions'])==21
for row in cov['regions']:
 b=primary[row['byte_start']:row['byte_end_exclusive']];assert sha(b)==row['raw_sha256'];assert b==b''.join(lines[row['line_start']-1:row['line_end']])
rec=load(S/'recommendation104.native.json');header=(O.parent/'Header104.lean').read_text(encoding='utf-8');prod=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualWeightedSector.lean').read_text(encoding='utf-8')
start=header.index('    let c :');end=header.index('    let R :');literal=header[start:end]
assert literal==rec['literal_definition_contract']['exact_existing_definition_text_LF'];assert literal in prod
save('topology-binding-check104.native.json',{'decision':'PASS','source_graph':info(S/'source-proof-graph-delta104.native.json'),'checked_source_bindings':list(bound.values()),'effective_graph':{'nodes':sorted(nodes),'edges':[list(e) for e in sorted(edges)],'node_count':len(nodes),'edge_count':len(edges),'new_unique_edges':[list(e) for e in sorted(edges-before)],'topological_order':order},'all21_source_spans_exact':True,'first20_literal_definitions_exact_header_recommendation_public102':True,'proof_credit':False})
print(len(nodes),len(edges),len(bound))
