from pathlib import Path
import json,hashlib,copy
from datetime import datetime,timezone
R=Path('E:/Samplinglib');G=R/'runs/20261007-companion-priority/gaussian-product-entropy-source-graph';O=G/'representation-overlay1'
H=lambda b:hashlib.sha256(b).hexdigest()
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def put(n,b):
 if not isinstance(b,bytes):b=enc(b)
 with (O/n).open('xb') as f:f.write(b)
 return H(b)
review_path=R/'runs/20261007-companion-priority/gaussian-product-entropy-source-graph-review/source-topology-review.json'
review_raw=review_path.read_bytes();assert H(review_raw)=='13767d3bdfed8c4b0869bed059c1874cf584696dedfaa3b34939f78aad7f3293'
review=json.loads(review_raw);assert review['review_run_sha256']=='a722293682e5fb56802ee11ad8615e471d3e46ce5780aec1e7175306521ec0b4'
phase_lease=review_path.parent/'reviewer.topology.lease.json';pl=json.loads(phase_lease.read_bytes());assert pl['status']=='CLOSED' and pl['read_lease']=='CLOSED' and pl['write_lease']=='CLOSED' and pl['compiler_lease']=='CLOSED'
graph_path=G/'source-proof-graph.independent.json';before_raw=graph_path.read_bytes();before=json.loads(before_raw)
assert H(before_raw)=='35802ddf622f1499c5e71b8cca3e31da470df590e778cdf0013e3b9b06675cf2'
assert enc(before)==before_raw
assert len(before['nodes'])==55 and len(before['edges'])==96 and len(before['or_routes'])==2 and before['compiled_edges']==[]
bindings=json.loads((G/'input-bindings.json').read_bytes());pins=[]
scope_files=[review_path,phase_lease,graph_path,G/'source.inventory.json',G/'source.contract.json',G/'input-bindings.json',G/'author.route.json',G/'lease.json',G/'run.json']+[R/x['path'] for x in bindings]
for i,p in enumerate(scope_files):
 b=p.read_bytes();l=lf(b);n=f'input.{i:02d}'
 put(n+'.raw.snapshot',b);put(n+'.lf.snapshot',l)
 pins.append({'path':p.relative_to(R).as_posix(),'raw_sha256':H(b),'lf_sha256':H(l),'bytes':len(b),'raw_snapshot':n+'.raw.snapshot','lf_snapshot':n+'.lf.snapshot'})
for a in bindings:
 b=(R/a['path']).read_bytes();assert H(b)==a['raw_sha256'] and H(lf(b))==a['lf_sha256']
 assert (G/a['raw_snapshot']).read_bytes()==b
 assert (G/a['lf_snapshot']).read_bytes()==lf(b)
inventory=json.loads((G/'source.inventory.json').read_bytes());assert inventory['region_count']==39 and inventory['physical_lines']==649
region_receipt=[]
for reg in inventory['regions']:
 p=G/reg['snapshot'];b=p.read_bytes();assert H(b)==reg['span_lf_sha256'];region_receipt.append({'path':p.relative_to(R).as_posix(),'raw_sha256':H(b),'unchanged':True})
sources={x['id']:x for x in bindings}
requests=[
 ('T1','e097','SLT-NONNEG','ae_nonneg_slice_of_ae_nonneg','SLT-BASIC',202,202,163,165,
  'Unexpanded actual AE nonnegative-fiber producer; source hF>=0 AE implies AE fibers>=0 AE. Not the L1 API-SLICES theorem.'),
 ('T2','e098','SLT-DUAL','LogSobolev.integralYLogT_of_pos_on_Y','SLT-DUAL',465,465,102,106,
  'Unexpanded EReal-to-real integralYLogT identity under AE Y>0 implies T>0; retains actual positivity boundary, no supplied L1 or output certificate.'),
 ('T2','e099','SLT-DUAL','LogSobolev.entropy_ge_integral_log','SLT-DUAL',466,466,423,434,
  'Unexpanded genuine EReal entropy duality producer requiring actual Y/T measurability, AE nonnegativity, Y/T L1, YlogY L1 and strictly positive T mean.'),
 ('T3','e100','SLT-GAUSSIAN','GaussianLSI.sum_expected_condEnt_le_grad_norm','SLT-GAUSSIAN',479,479,249,257,
  'Unexpanded actual external sum-of-coordinate entropy/gradient energy comparison with factor2; requires actual MemW12GaussianPi, differentiability, continuous partials, separate squared-Phi L1. Distinct from authored future GAUSSIAN-CONSUMER.')]
new=[];literal=[]
for blocker,eid,dest,prim,k,ca,cb,da,db,contract in requests:
 a=sources[k];raw=(R/a['path']).read_bytes();ls=lf(raw).decode().splitlines()
 caller=('\n'.join(ls[ca-1:cb])+'\n').encode();callee=('\n'.join(ls[da-1:db])+'\n').encode()
 assert prim.split('.')[-1] in caller.decode() and prim.split('.')[-1] in callee.decode()
 cn=eid+'.caller.raw.snapshot.lean';dn=eid+'.callee.raw.snapshot.lean';put(cn,caller);put(dn,callee)
 literal.append({'edge_id':eid,'blocker':blocker,'primitive':prim,'source_path':a['path'],'source_pin_raw_sha256':a['raw_sha256'],'source_pin_lf_sha256':a['lf_sha256'],'caller_lines':[ca,cb],'caller_snapshot':cn,'caller_lf_sha256':H(caller),'callee_lines':[da,db],'callee_snapshot':dn,'callee_lf_sha256':H(callee)})
 new.append({'id':eid,'from':'SLT-IMPORTS','to':dest,'ingredient':prim+' (actual direct selected caller use; unexpanded external source-gap primitive)',
  'kind':'DEPENDENCY_BOUNDARY','caller_anchor':f'{k}:{ca}' if ca==cb else f'{k}:{ca}-{cb}',
  'callee_anchor':{'pin':k,'path':a['path'],'lines':[da,db]},
  'external_source_gap_primitive':{'name':prim,'contract':contract,'unexpanded':True,'local_producer':False,'extension_location':'This new dependency edge names the primitive in the existing unexpanded SLT-IMPORTS family; every original node annotation is preserved.'},'compiled':False})
after=copy.deepcopy(before);after['edges'].extend(new)
assert len(after['edges'])==100
assert {k:v for k,v in before.items() if k!='edges'}=={k:v for k,v in after.items() if k!='edges'}
assert enc(before['nodes'])==enc(after['nodes'])
assert enc(before['edges'])==enc(after['edges'][:96])
roundtrip=copy.deepcopy(after);roundtrip['edges']=roundtrip['edges'][:96];assert enc(roundtrip)==before_raw
after_raw=enc(after);successor=G/'source-proof-graph.repaired.independent.json'
with successor.open('xb') as f:f.write(after_raw)
put('before.graph.raw.snapshot.json',before_raw);put('after.graph.raw.snapshot.json',after_raw)
diff={'schema_version':1,'json_patch':[{'op':'add','path':'/edges/-','value':e} for e in new],
 'allowed_change':'Exactly four appended dependency-boundary/direct-source-use edges naming actual unexpanded SLT primitives. No node/formula/public-binder/definition/annotation/OR/compiled edge/inventory/sourcecontract/pin mutation.',
 'before':{'nodes':55,'edges':96,'OR':2,'compiled_edges':[],'raw_sha256':H(before_raw)},
 'after':{'nodes':55,'edges':100,'OR':2,'compiled_edges':[],'raw_sha256':H(after_raw)},
 'nonedges_canonical_bytes_equal':True,'nodes_canonical_bytes_equal':True,'original_96_edgeprefix_canonical_bytes_equal':True,
 'remove_only_4_appended_edges_reserializes_to_original_raw_bytes':True,
 'nonedges_sha256':H(enc({k:v for k,v in before.items() if k!='edges'})),
 'original_edgeprefix_sha256':H(enc(before['edges'])),
 'inventory_39_dispositions_649_lines_preserved':True,'all_18_original_pins_and_snapshots_preserved':True,
 'historical_conditional38_provenance_unchanged':True,'literal_source_evidence':literal}
put('scoped-diff.json',diff);put('input-bindings.json',pins);put('preserved-source-regions.json',region_receipt)
repair={'schema_version':1,'status':'FROZEN_AUTHOR_REPRESENTATION_REPAIR_AWAITING_DISTINCT_REVIEW','actor':'gaussian_domain_preproof_reviewer_29',
 'independent_review_request':{'path':review_path.relative_to(R).as_posix(),'raw_sha256':H(review_raw),'lf_sha256':H(lf(review_raw)),'run_sha256':review['review_run_sha256'],'lease_status':'CLOSED'},
 'original_graph':{'path':graph_path.relative_to(R).as_posix(),'raw_sha256':H(before_raw)},
 'successor_graph':{'path':successor.relative_to(R).as_posix(),'raw_sha256':H(after_raw),'lf_sha256':H(lf(after_raw))},
 'exact_repair_map':[{'blocker':r[0],'edge_id':r[1],'from':'SLT-IMPORTS','to':r[2],'primitive':r[3],'caller':f'{r[4]}:{r[5]}','callee_lines':[r[7],r[8]]} for r in requests],
 'source_gap_contract_visibility':'Requested previously omitted primitive names/contracts are explicit within each new edge external_source_gap_primitive. This extends the unexpanded SLT-IMPORTS family at its direct uses, without changing any original55node annotation or introducing a public hypothesis.',
 'count_delta':{'nodes':[55,55],'edges':[96,100],'OR':[2,2],'inventory_regions':[39,39],'selected_physical_lines':[649,649],'original_pins':[18,18]},
 'coverage_boundary':'Additional callee header snapshots are overlay evidence from the SAME already-pinned raw source files; original selected649-line inventory is unchanged. No whole external closure expansion or local callable producer claimed.',
 'scope':'Source representation only; no mathematical/signature/binder/candidate-body/Test/LSI change. Original BLOCKED receipt and all earlier files immutable.',
 'diff':'scoped-diff.json','inputs':'input-bindings.json','preserved_regions':'preserved-source-regions.json',
 'compiler_started':False,'canonical_mutations':False,'selfvalidation':False,
 'remaining_boundary':['distinct phase overlay/successor topology admission','actual39 proof/tests/source/math/exact admission','finite tensorization/Gaussian product/Hilbert/cutoff/noncompact LSI','Gaussian T2/FIRST4.6/paper main/work/cost']}
put('repair.json',repair)
outputs=[{'path':n,'raw_sha256':H((O/n).read_bytes()),'lf_sha256':H(lf((O/n).read_bytes()))} for n in ['repair.json','scoped-diff.json','input-bindings.json','preserved-source-regions.json','before.graph.raw.snapshot.json','after.graph.raw.snapshot.json']]
run={'schema_version':1,'inputs':[{'path':p['path'],'raw_sha256':p['raw_sha256'],'lf_sha256':p['lf_sha256']} for p in pins],'outputs':outputs,'successor_sha256':H(after_raw),'compiler_started':False,'selfvalidation':False};run['run_sha256']=H(enc(run));put('run.json',run)
# Confirm preservation at completion; this is an author scoped-diff receipt, not topology validation.
for p in pins:assert H((R/p['path']).read_bytes())==p['raw_sha256']
lease=json.loads((O/'lease.json').read_bytes());lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','closed_utc':datetime.now(timezone.utc).isoformat(),'run_sha256':run['run_sha256'],'successor_sha256':H(after_raw),'repair_sha256':H(enc(repair))});(O/'lease.json').write_bytes(enc(lease))
print(json.dumps({'successor_raw_sha256':H(after_raw),'repair_raw_sha256':H(enc(repair)),'run_sha256':run['run_sha256'],'nodes':55,'edges':100,'OR':2,'original_prefix':96,'leases':'CLOSED','independent_topology_review':'PENDING'}))
