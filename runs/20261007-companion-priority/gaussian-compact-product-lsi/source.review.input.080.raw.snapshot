from pathlib import Path
import json,hashlib,copy,re
from datetime import datetime,timezone
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/gaussian-compact-product-source-graph';O=B/'representation-overlay1';V=R/'runs/20261007-companion-priority/gaussian-compact-product-source-topology-review'
H=lambda b:hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(j):return (json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode()
def put(name,b):
 if not isinstance(b,bytes):b=enc(b)
 with (O/name).open('xb') as f:f.write(b)
 return H(b)
def load(p):return json.loads(p.read_bytes())
request=load(V/'source-topology-review.json');assert H((V/'source-topology-review.json').read_bytes())=='d7bbdb89b0af1de495ee926bc20cb24115678e5129e373cb520e1d65d277f933'
reviewlease=load(V/'reviewer.topology.lease.json');assert all(reviewlease[k]=='CLOSED' for k in ['status','read_lease','write_lease','Python_lease','compiler_lease'])
raw=(B/'source-proof-graph.independent.json').read_bytes();assert H(raw)==request['graph_raw_sha256'];old=json.loads(raw);new=copy.deepcopy(old)
assert (len(old['nodes']),len(old['edges']),len(old['or_routes']))==(79,201,2)
bindings=load(B/'input-bindings.json');pd={p['id']:p for p in bindings};src={}
for p in bindings:
 b=(R/p['path']).read_bytes();assert H(b)==p['raw_sha256'] and H(lf(b))==p['lf_sha256'],p['path'];src[p['id']]=lf(b).decode().splitlines(keepends=True)
edges={e['id']:e for e in new['edges']};removed=[];changes=[]
# T1: only the seven false anchors; retain each genuine remaining anchor.
for eid,pin,bad in [('e074','P06',{193}),('e077','P06',{169,193}),('e102','P07',{1323,1338,1339})]:
 before=copy.deepcopy(edges[eid]);e=edges[eid];gone=[a for a in e['caller_anchor'] if a['pin']==pin and a['lines'][0] in bad];assert len(gone)==len(bad)
 e['caller_anchor']=[a for a in e['caller_anchor'] if a not in gone];changes.append({'request':'T1','edge':eid,'before':before,'after':copy.deepcopy(e),'removed_false_anchors':gone})
removed=[copy.deepcopy(edges['e082'])];new['edges']=[e for e in new['edges'] if e['id']!='e082']
assert len(removed[0]['caller_anchor'])==1 and removed[0]['caller_anchor'][0]=={'pin':'P06','lines':[341,341]}
# T2: keep literal consumers/anchors; clarify generic imports vs selected API providers.
requested=request['blockers'][1]['edges'];assert [x['id'] for x in requested]==['e068','e069','e073','e078','e084','e085','e096']
for req in requested:
 e=edges[req['id']];assert e==req;before=copy.deepcopy(e);e['from']='S-IMPORTS'
 e['provider_boundary']={'classification':'UNEXPANDED_IMPORTED_TYPING_CONTRACT' if e['id']=='e068' else 'UNEXPANDED_IMPORTED_GENERIC_PRIMITIVE','selected_API_provider_claim':False,'compiled_producer_claim':False,'exact_provider_closure_expanded':False,'scope':'S-IMPORTS is a boundary marker for imported generic typing/calculus/Finset algebra, not an asserted declaration provider in the selected update/Pi or Bochner sum region.'}
 if e['id']=='e068':
  e['kind']='EXTERNAL_IMPORTED_TYPING_CONTRACT';e['ingredient']='Imported typing contract occurrence: HasFDerivAt (not a called theorem supplied by update derivative API)'
 changes.append({'request':'T2','edge':e['id'],'before':before,'after':copy.deepcopy(e)})
# T3: four exact actual domain/transport calls. No new node or provider certificate.
added=[]
for idx,c in enumerate(request['blockers'][2]['calls'],202):
 p=c['pin'];a,b=c['lines'];text=''.join(src[p][a-1:b]);assert text.strip()==c['literal_caller_text'].strip()
 e={'id':f'e{idx:03d}','from':'S-IMPORTS','to':c['consumer'],'ingredient':'Actual imported-background dependency: '+c['callee']+'; '+c['purpose'],'kind':'EXTERNAL_IMPORTED_PRIMITIVE_USE','caller_anchor':[{'pin':p,'lines':[a,b]}],'compiled':False,'provider_boundary':{'classification':'UNEXPANDED_IMPORTED_BACKGROUND_PRIMITIVE','exact_provider_closure_expanded':False,'compiled_producer_claim':False,'selected_API_provider_claim':False,'source_L1_or_law_contract_retained':True}}
 if c['callee']=='integral_condExpExceptCoord_mul_log':e['provider_header_evidence']={'pin':'P09','lines':[278,283],'scope':'Literal supporting header in already frozen raw pin, supplemental overlay evidence only; original selected inventory unchanged; imported provider closure not certified.'}
 added.append(e);new['edges'].append(e)
assert len(added)==4 and len(new['edges'])==204
# Exact non-edge/node/OR preservation; only requested representations change.
assert {k:v for k,v in new.items() if k!='edges'}=={k:v for k,v in old.items() if k!='edges'}
affected={c['edge'] for c in changes}|{'e082'};oldby={e['id']:e for e in old['edges']};newby={e['id']:e for e in new['edges']}
unchanged=[e['id'] for e in old['edges'] if e['id'] not in affected];assert len(unchanged)==190
assert all(oldby[i]==newby[i] for i in unchanged)
assert [e['id'] for e in new['edges'][:200]]==[e['id'] for e in old['edges'] if e['id']!='e082']
assert new['compiled_edges']==[] and new['nodes']==old['nodes'] and new['or_routes']==old['or_routes']
# Freeze all49 original exact input bytes plus original receipts/author artifacts.
inputs=[]
paths=[R/p['path'] for p in bindings]+[B/n for n in ['source-proof-graph.independent.json','source.inventory.json','source.contract.json','input-bindings.json','author.run.json','author.lease.json','bounded-synthesis.json']]+[V/'source-topology-review.json',V/'reviewer.topology.lease.json']
for i,p in enumerate(paths):
 b=p.read_bytes();q={'path':p.relative_to(R).as_posix(),'raw_sha256':H(b),'lf_sha256':H(lf(b)),'bytes':len(b),'raw_snapshot':f'input.{i:03d}.raw.snapshot','lf_snapshot':f'input.{i:03d}.lf.snapshot'};inputs.append(q);put(q['raw_snapshot'],b);put(q['lf_snapshot'],lf(b))
evidence=[]
anchors=[]
for c in changes:
 for a in c['before']['caller_anchor']:anchors.append(a)
anchors+=removed[0]['caller_anchor']
for e in added:anchors+=e['caller_anchor']
anchors.append({'pin':'P09','lines':[278,283]})
seen=set()
for a in anchors:
 key=(a['pin'],*a['lines'])
 if key in seen:continue
 seen.add(key);p,lo,hi=key;b=''.join(src[p][lo-1:hi]).encode();name=f'caller-provider.{len(evidence):03d}.lf.snapshot';put(name,b);evidence.append({**a,'path':pd[p]['path'],'source_raw_sha256':pd[p]['raw_sha256'],'source_lf_sha256':pd[p]['lf_sha256'],'span_lf_sha256':H(b),'snapshot':name})
successor=enc(new);sp=B/'source-proof-graph.repaired.independent.json'
with sp.open('xb') as f:f.write(successor)
delta={'schema_version':1,'representation_only':True,'modified_edges':changes,'deleted_edges':[{'request':'T1','before':removed[0],'reason':'Only false integral_prod substring; true integral_prod_left is already recorded at e080.'}],'appended_edges':added,'nonedge_fields_canonical_unchanged':True,'nodes_canonical_unchanged':True,'OR_routes_canonical_unchanged':True,'compiled_edges_unchanged_empty':True,'original_order_retained_except_deleted_e082':True,'old_edge_prefix_identity_with_exact_allowed_modifications':True,'190_unaffected_old_edges_canonical_unchanged':True,'new_mathematical_hypotheses_or_formulas':False,'new_nodes':0,'removed_false_caller_anchors':7,'provider_boundary_corrections':7}
diffhash=put('scoped-diff.json',delta);ihash=put('input-bindings.json',inputs);ehash=put('literal-caller-provider-evidence.json',evidence)
repair={'schema_version':1,'actor':'gaussian_domain_preproof_reviewer_29','status':'AUTHOR_REPRESENTATION_REPAIR_PROPOSED_AWAITING_DISTINCT_PHASE','source_review_request':{'path':(V/'source-topology-review.json').relative_to(R).as_posix(),'raw_LF_sha256':H((V/'source-topology-review.json').read_bytes()),'review_run_sha256':request['review_run_sha256']},'original_graph':{'path':(B/'source-proof-graph.independent.json').relative_to(R).as_posix(),'raw_LF_sha256':H(raw)},'successor_graph':{'path':sp.relative_to(R).as_posix(),'raw_LF_sha256':H(successor)},'counts':{'before_nodes':79,'after_nodes':79,'before_edges':201,'after_edges':204,'OR_routes':2,'original_source_pins':49,'original_regions':67,'original_selected_physical_lines':1467},'requested_changes':{'T1':'Remove7 false anchors from4 edges; e082 wholly deleted, true remaining anchors unchanged','T2':'7 generic/typing/Finset edges routed to existing S-IMPORTS with explicit unexpanded boundary; no fake selected provider claim','T3':'Append4 actual source-domain/law calls e202-e205; supporting tower header supplemental only'},'invariants':{'original_graph_inventory_contract_rawpins_BLOCKED_bytes_unchanged':True,'all79nodes_and2OR_unchanged':True,'allnonedge_graph_fields_unchanged':True,'original49sourcepins67regions_unchanged':True,'sealed678_signature_unchanged':True,'compiled_edges':[],'mathematical_binders_formulas_scope_unchanged':True},'scoped_diff':{'path':'scoped-diff.json','raw_LF_sha256':diffhash},'input_bindings':{'path':'input-bindings.json','raw_LF_sha256':ihash},'literal_evidence':{'path':'literal-caller-provider-evidence.json','raw_LF_sha256':ehash},'boundary_audit':'S-IMPORTS explicitly represents unexpanded imported generic typing/derivative/Finset and L1/law primitives. No additional imported provider is marked callable or compiled. Supplemental P09 tower header lies in an already frozen raw pin; source.inventory selection/counts are not rewritten. Original source contracts and all residual Hilbert/noncompact/T2/FIRST/main/cost gaps retained.','exposure_attestation':{'future40_implementation_Test_blind_read':False,'proof_search':False,'compiler_started':False,'canonical_shared_site_ledger_mutations':False,'source_topology_selfvalidation':False},'validation':'Only bounded author repair/invariant comparison; distinct phase must independently validate successor.'}
rh=put('repair.json',repair)
run={'schema_version':1,'actor':repair['actor'],'inputs':[{'path':x['path'],'raw_sha256':x['raw_sha256'],'lf_sha256':x['lf_sha256']} for x in inputs],'outputs':{'repair.json':rh,'scoped-diff.json':diffhash,'input-bindings.json':ihash,'literal-caller-provider-evidence.json':ehash,'../source-proof-graph.repaired.independent.json':H(successor)},'compiler_started':False,'selfvalidation':False};run['run_sha256']=H(enc(run));put('run.json',run)
for x in inputs:assert H((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
lease=load(O/'author.lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_status':'NEVER_STARTED','closed_utc':datetime.now(timezone.utc).isoformat(),'run_sha256':run['run_sha256'],'repair_raw_LF_sha256':rh,'successor_graph_raw_LF_sha256':H(successor),'independent_admission':'PENDING_DISTINCT_PHASE'});(O/'author.lease.json').write_bytes(enc(lease))
print(json.dumps({'successor_raw_LF_sha256':H(successor),'repair_raw_LF_sha256':rh,'run_sha256':run['run_sha256'],'counts':repair['counts'],'leases':'CLOSED','compiler':'NEVER_STARTED'}))
