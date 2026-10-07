import copy, datetime, hashlib, json
from pathlib import Path

root=Path('E:/Samplinglib')
base=root/'runs/20261007-companion-priority/gaussian-compact-entropy-source-graph'
out=base/'representation-overlay1'
review=root/'runs/20261007-companion-priority/gaussian-compact-entropy-source-graph-review/source-topology-review.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def rel(p):return str(p.relative_to(root)).replace('\\','/')
def serialized(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(p,x):
    b=serialized(x)
    with p.open('xb') as f:f.write(b)
    return {'path':rel(p),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
old=(base/'source-proof-graph.independent.json').read_bytes()
assert sha(old)=='7f3ae37663d5b4bf27fe5201c0bbf6b22d8c89b1fc4c9234c577e48e9ace1933'
rv=review.read_bytes()
assert sha(rv)=='ac864f5afb10e7f33a6a18182c87cf244eeafb0a0bffc5713b0269faee99d885'
request=json.loads(rv)
assert request['status']=='BLOCKED' and request['blocker_class']=='source-topology-representation'
phaselease=review.parent/'reviewer.topology.lease.json'
pl=json.loads(phaselease.read_text(encoding='utf-8'))
assert 'CLOSED' in str(pl) and 'ACTIVE' not in str(pl)
graph=json.loads(old);assert serialized(graph)==old
pins=json.loads((base/'input-bindings.json').read_text(encoding='utf-8'))['inputs']
inputs=[]
def bind(p,expected=None):
    b=p.read_bytes();x={'path':rel(p),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
    if expected:
        for k in ['raw_sha256','lf_sha256','bytes']:assert x[k]==expected[k],(p,k)
    for kind,val in [('raw',b),('lf',lf(b))]:
        sp=out/('input.%03d.%s.snapshot'%(len(inputs),kind))
        with sp.open('xb') as f:f.write(val)
        x[kind+'_snapshot']=rel(sp)
    inputs.append(x)
for x in pins:bind(root/x['path'],x)
for p in [base/'source-proof-graph.independent.json',base/'source.inventory.json',base/'source.contract.json',base/'input-bindings.json',base/'run.closed.json',base/'author.lease.json',review,phaselease]:bind(p)
assert len(pins)==37
inventory=json.loads((base/'source.inventory.json').read_text(encoding='utf-8'))
assert len(inventory['regions'])==114
region_checks=[]
for r in inventory['regions']:
    for kind in ['raw','lf']:
        p=root/r[kind+'_snapshot'];b=p.read_bytes();assert sha(b)==r[kind+'_sha256']
        region_checks.append({'path':rel(p),'sha256':sha(b),'bytes':len(b)})
source=root/'runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianPoincare__Limit.lean.raw.snapshot'
sb=source.read_bytes();assert sha(sb)=='4bc70c94e5d9cca273fdd816431e80af6d19de36af0d64a7854d1b05353a346b'
lines=sb.splitlines(keepends=True);span=b''.join(lines[1212:1234])
assert b'rademacherLaw' in span and b'stdGaussianMeasure' in span
span_info={'path':rel(source),'lines':[1213,1234],'whole_raw_sha256':sha(sb),'whole_lf_sha256':sha(lf(sb)),
           'raw_start':sum(map(len,lines[:1212])),'raw_end':sum(map(len,lines[:1234])),
           'raw_sha256':sha(span),'lf_sha256':sha(lf(span)),
           'raw_snapshot':rel(out/'source.Limit.1213-1234.raw.snapshot'),
           'lf_snapshot':rel(out/'source.Limit.1213-1234.lf.snapshot'),
           'original_inventory_region':'R029 (broader1196-1234 source block; exact new edge anchor1213-1234)'}
for kind,val in [('raw',span),('lf',lf(span))]:
    with (root/span_info[kind+'_snapshot']).open('xb') as f:f.write(val)
successor=copy.deepcopy(graph);changes=[]
for eid in ['e134','e135','e136']:
    i=next(i for i,e in enumerate(successor['edges']) if e['id']==eid)
    before=copy.deepcopy(successor['edges'][i]);assert before['kind']=='EXTERNAL_SOURCE_USE'
    assert before['to']=='GAP-REAL-COUNT'
    successor['edges'][i]['kind']='DEPENDENCY_BOUNDARY'
    assert {k:v for k,v in before.items() if k!='kind'}=={k:v for k,v in successor['edges'][i].items() if k!='kind'}
    changes.append({'request':'T1','id':eid,'json_pointer':'/edges/%d/kind'%i,'before':'EXTERNAL_SOURCE_USE','after':'DEPENDENCY_BOUNDARY','before_edge':before,'after_edge':successor['edges'][i],'reason':'Authored real-product-to-actual-count carrier adapter absent from external source.'})
newedge={'id':'e163','from':'SLT-REAL-LAW','to':'SLT-ENTROPY-LIMIT','kind':'EXTERNAL_SOURCE_USE',
         'ingredient':'Literal rademacherLaw(n+1).toMeasure and stdGaussianMeasure used in tendsto_entropy_f_sq statement and proof.',
         'anchor':span_info}
assert not any(e['from']==newedge['from'] and e['to']==newedge['to'] for e in graph['edges'])
successor['edges'].append(newedge);successor['counts']['edges']=163
changes.append({'request':'T2','id':'e163','json_pointer':'/edges/162','before':None,'after':newedge,'reason':'Actual direct law-definition source ingredient retained explicitly.'})
assert len(successor['nodes'])==65 and len(successor['edges'])==163 and len(successor['or_routes'])==2 and successor['compiled_edges']==[]
for k in graph:
    if k not in ['edges','counts']:assert graph[k]==successor[k],k
assert {k:v for k,v in graph['counts'].items() if k!='edges'}=={k:v for k,v in successor['counts'].items() if k!='edges'}
for i,e in enumerate(graph['edges']):
    expected=copy.deepcopy(e)
    if expected['id'] in ['e134','e135','e136']:expected['kind']='DEPENDENCY_BOUNDARY'
    assert successor['edges'][i]==expected
target=write(base/'source-proof-graph.repaired.independent.json',successor)
diff=write(out/'scoped-diff.json',{'status':'AUTHOR_REPRESENTATION_ONLY_NOT_VALIDATION','requested_changes':changes,
 'derived_count_update':{'json_pointer':'/counts/edges','before':162,'after':163},
 'invariants':['65nodes identical','all node formulas/binders/definitions/source_regions identical','all mathematical/source truth boundaries identical','2OR routes identical','all other original162edge fields unchanged','compiled_edges remains empty','root ofCompactSupport namespace unchanged','original114regions1195lines/4primary coverage unchanged'],
 'before_graph_raw_sha256':sha(old),'after_graph':target})
binding=write(out/'input-bindings.json',{'normalization':'Raw exact bytes; LF normalization replaces CRLF then CR by LF; no input JSON reserialization.',
 'inputs':inputs,'all37_original_source_pins_unchanged':True,'original_raw_LF_region_snapshots_unchanged':region_checks,
 'literal_new_edge_source_span':span_info,'no_candidate_or_proof36_read':True,'no_new35_status_read':True})
repair=write(out/'repair.json',{'status':'AUTHORED_UNREVIEWED_REPRESENTATION_SUCCESSOR','actor':'gaussian_domain_preproof_reviewer_29',
 'role':'Original source author, not independent topology validator','exact_request':{'path':rel(review),'raw_sha256':sha(rv),'lf_sha256':sha(lf(rv))},
 'repairs':['Retag e134,e135,e136 DEPENDENCY_BOUNDARY, endpoints/ingredients/anchors unchanged.','Append e163 SLT-REAL-LAW -> SLT-ENTROPY-LIMIT direct EXTERNAL_SOURCE_USE with exact pinned Limit1213-1234 raw/LF span.'],
 'successor_graph':target,'scoped_diff':diff,'input_bindings':binding,'counts':successor['counts'],
 'all_original_graph_inventory_contract_pins_lease_review_preserved':True,
 'mathematical_target_public_binders_formulas_OR_routes_unchanged':True,
 'remaining_boundary':['full-flip-energy4','noncompact actual32 sqrtRN/cutoff/W12','finite-Hilbert/tensorization','GaussianLSI','T2','FIRST4.6','bias/main/work/composition'],
 'no_compiler_no_canonical_production_shared_state_writes':True,'source_topology_admission':'Pending distinct phase successor review; author cannot validate.'})
for x in inputs:
    b=(root/x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256']
outputs=[target,diff,binding,repair]
runid=sha(json.dumps({'inputs':[{k:x[k] for k in ['path','raw_sha256','lf_sha256']} for x in inputs],
                    'outputs':outputs},sort_keys=True,separators=(',',':')).encode())
run=write(out/'run.closed.json',{'deterministic_run_sha256':runid,'outputs':outputs,'all_inputs_unchanged_at_close':True,
                              'role':'source author repair only; no selfvalidation','read_write_compiler':'CLOSED','compiler_started':False})
lease=json.loads((out/'lease.json').read_text(encoding='utf-8'))
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,
             closed_utc=datetime.datetime.utcnow().isoformat()+'Z',deterministic_run_sha256=runid,run=run)
(out/'lease.json').write_bytes(serialized(lease))
print(json.dumps({'successor':target,'repair':repair,'run':run,'run_id':runid,'input_count':len(inputs),'counts':successor['counts'],'leases':'CLOSED'},indent=2))
