from pathlib import Path
import json,hashlib,copy,datetime
root=Path('E:/Samplinglib')
base=root/'runs/20261007-companion-priority/rademacher-law-source-graph'
out=base/'source-graph-representation-overlay1'
reviewdir=root/'runs/20261007-companion-priority/rademacher-law-source-graph-review'
actor='gaussian_domain_preproof_reviewer_29'
def h(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def write(p,data):
 b=(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
 with p.open('xb') as f:f.write(b)
 return {'path':str(p.relative_to(root)).replace('\\','/'),'raw_sha256':h(b),'lf_sha256':h(lf(b)),'bytes':len(b)}
oldpath=base/'source-proof-graph.independent.json';oldraw=oldpath.read_bytes();old=json.loads(oldraw)
assert h(oldraw)=='a17249b2bb5d75fe8bb46083a9b804c23547fe4da28141f3405953b10d6a2d37'
invpath=base/'source-inventory.json';invraw=invpath.read_bytes();inv=json.loads(invraw)
assert h(invraw)=='117e490ac325838058e9ce9403e0ab9e1a72f2684a9e18a678c44dda523232cf'
requestpath=reviewdir/'source-topology-review.json';requestraw=requestpath.read_bytes();request=json.loads(requestraw)
assert h(requestraw)=='e93ed41fb519eae9f543948568a87fa54b8fac70554864e98d2a59ebeb425ca6'
phaselease=json.loads((reviewdir/'reviewer.topology.lease.json').read_bytes())
assert all(phaselease[k]=='CLOSED' for k in ['status','read_lease','write_lease','compiler_lease'])
assert request['source_only'] and not request['implementation35_exposure'] and request['status']=='BLOCKED'
originalbind=json.loads((base/'input-bindings.final.json').read_bytes())
manifest=[]
paths=[x['path'] for x in originalbind['inputs']]+[str(p.relative_to(root)).replace('\\','/') for p in
 [oldpath,invpath,base/'input-bindings.final.json',base/'run.json',base/'author.lease.json',requestpath,reviewdir/'reviewer.topology.lease.json',reviewdir/'reviewer.topology.run.json']]
for i,p in enumerate(paths):
 b=(root/p).read_bytes();pin=next((x for x in originalbind['inputs'] if x['path']==p),None)
 if pin:
  assert h(b)==pin['raw_sha256'],p
  if pin['lf_sha256'] is not None:assert h(lf(b))==pin['lf_sha256'],p
 r=f'input.{i:03d}.raw.snapshot';l=f'input.{i:03d}.lf.snapshot' if not p.endswith('.olean') else None
 with (out/r).open('xb') as f:f.write(b)
 if l:
  with (out/l).open('xb') as f:f.write(lf(b))
 manifest.append({'path':p,'bytes':len(b),'raw_sha256':h(b),'lf_sha256':h(lf(b)) if l else None,
  'raw_snapshot':r,'lf_snapshot':l,'original_45_pin_unchanged':bool(pin)})
bindings=write(out/'input-bindings.json',{'actor':actor,'inputs':manifest,'original_source_input_count':45,
 'original45_raw_LF_pins_unchanged':True,'source_only_representation_request':True,'compiler_started':False,
 'implementation_history':'Separately CLOSED35 math review exposed actual proof; NO35 implementation read or used in this source repair. Exact source-only phase request and original source/API pins exclusively govern additions.'})

rep=request['repairs'][0];req=rep['missing_edges'];assert len(req)==11
oldpairs={(e['from'],e['to']) for e in old['edges']};new=copy.deepcopy(old)
up='runs/20261007-companion-priority/gaussian-functional-availability/'
L=up+'SLT__GaussianPoincare__Limit.lean.raw.snapshot';E=up+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot';R=up+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot'
anchors=[[(E,354,359),(E,371,371)],[(L,98,123)],[(L,99,99)],[(L,139,139)],[(L,154,156)],[(L,54,54)],[(L,222,222)],[(L,39,40),(L,92,94)],[(R,86,86),(R,100,100)],[(L,100,100)],[(L,74,86)]]
anchor_receipts=[]
def anchor(p,lo,hi):
 raw=(root/p).read_bytes();lines=raw.splitlines(keepends=True);b=b''.join(lines[lo-1:hi]);name=f'source-anchor.{len(anchor_receipts):03d}.raw.snapshot'
 with (out/name).open('xb') as f:f.write(b)
 d={'path':p,'raw_line_start':lo,'raw_line_end':hi,'source_file_raw_sha256':h(raw),'span_raw_sha256':h(b),'span_lf_sha256':h(lf(b)),'snapshot':name,
  'existing_inventory_regions':[x['region_id'] for x in inv['regions'] if x['path']==p and x['raw_physical_line_start']<=lo and hi<=x['raw_physical_line_end']]}
 assert d['existing_inventory_regions'],(p,lo,hi)
 anchor_receipts.append(d);return d
added=[]
for x,sp in zip(req,anchors):
 assert (x['from'],x['to']) not in oldpairs
 e={'from':x['from'],'to':x['to'],'truth_contract':'Direct use in retained external pinned source branch; not an ASTIS35 compiled dependency or a new target premise',
    'source_evidence':x['source_evidence'],'source_anchors':[anchor(p,a,b) for p,a,b in sp]}
 if x['from']=='FINITE-INTEGRAL-API':e['precise_group_member_used']='integral_smul_measure; actual source two-atom L1 is proved in retained SLT-NU source, not a finite-count caller certificate'
 added.append(e)
new['edges']+=added
primitive=anchor(L,79,83)
annotation={'consumer_node':'SLT-LAW-CF','source_route':'External SLT charFun_map_sum_pi_const, Limit74-86, uses induction with convolution and finite-pi splitting',
 'source_anchor':primitive,'imported_primitives':['charFun_conv','measurePreserving_piFinSuccAbove','Measure.conv','Measure.map_prod_map','Measure.map_map'],
 'exact_use':'Limit79 rewrites charFun_conv; Limit81 applies measurePreserving_piFinSuccAbove(...,0).map_eq; Limit83 transports the product-map splitting through true convolution/map identities.',
 'route_distinction':'This retained SLT external imported primitive route is distinct from authored actual-count exp factorization and from Mathlib independence/product CF route. No identification, theorem equivalence or formal dependency between these routes is asserted.',
 'hypothesis_boundary':'Retain SLT IsFiniteMeasure mu on the helper, actual balanced product probability when used. No new public target premise and no mandatory imported route for authored direct-count alternative.',
 'truth_boundary':'External-reference source primitive boundary only; no ASTIS callable producer, port or new compilation credit.'}
new['external_primitive_route_annotations']=[annotation]
assert len(old['nodes'])==len(new['nodes'])==54 and len(old['edges'])==96 and len(new['edges'])==107
assert new['edges'][:96]==old['edges'] and new['nodes']==old['nodes'] and len(new['or_hyperedges'])==2 and new['compiled_edges']==[]
assert set(new)-set(old)=={'external_primitive_route_annotations'}
assert all(new[k]==v for k,v in old.items() if k!='edges')
successor=write(base/'source-proof-graph.repaired.independent.json',new)
repair=write(out/'repair.json',{'actor':actor,'status':'AUTHORED_UNREVIEWED_REPRESENTATION_REPAIR','role':'original source graph author, NOT validator',
 'request':{'path':str(requestpath.relative_to(root)).replace('\\','/'),'raw_sha256':h(requestraw),'phase_read_write_compiler_CLOSED':True},
 'original_graph':{'path':str(oldpath.relative_to(root)).replace('\\','/'),'raw_sha256':h(oldraw),'lf_sha256':h(lf(oldraw))},
 'successor_graph':successor,'input_bindings':bindings,'exact_added_edges':added,'exact_external_annotation':annotation,
 'unchanged':{'all_original_graph_keys_except_edges':True,'old96_edges_prefix_exact':True,'nodes54_exact':True,'or_hyperedges2_exact':True,'compiled_edges_empty':True,
 'source_inventory_raw_sha256':h(invraw),'source_inventory_regions':79,'source_inventory_physical_lines':1559,'source_inventory_bytes_unchanged':True,
 'original45_source_pins_unchanged':True,'public_target_formula_quantifiers_assumptions_unchanged':True,'source_graph_truth_status_UNREVIEWED':True},
 'diff_scope':'Only append exact eleven requested direct source-use edges and one external_primitive_route_annotations member. No existing node/formula/route/source input/disposition changed.',
 'history':'Original PRIMARY/API graph authored before future implementation. Separate whole-math35 review has since CLOSED; this repair is solely governed by original pinned source and independent phase source-only request, not implementation topology.',
 'mechanical_checks_not_selfvalidation':'Equality/count/hash checks describe authored diff and input preservation only. Distinct phase overlay review must admit topology.',
 'compiler_started':False,'production_Test_shared_metadata_writes':False,'remaining_boundary':old['excluded_completion']})
for x in manifest:
 b=(root/x['path']).read_bytes();assert h(b)==x['raw_sha256'],x['path']
 if x['lf_sha256'] is not None:assert h(lf(b))==x['lf_sha256'],x['path']
assert oldpath.read_bytes()==oldraw and invpath.read_bytes()==invraw
material={'actor':actor,'repair':repair,'successor_graph':successor,'bindings':bindings,'all_input_hashes_rechecked':True,
 'added_edges':11,'old_edge_count':96,'successor_edge_count':107,'nodes_unchanged':54,'or_routes_unchanged':2,'inventory_regions_unchanged':79,'inventory_lines_unchanged':1559,
 'compiler_started':False,'source_topology_self_validation':False,'production_writes':False}
runhash=h(json.dumps(material,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
run=write(out/'run.json',dict(material,deterministic_run_sha256=runhash,status='CLOSED_AUTHOR_REPAIR_AWAITING_DISTINCT_PHASE'))
p=out/'lease.json';lease=json.loads(p.read_bytes());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,
 closed_utc=datetime.datetime.utcnow().isoformat()+'Z',run=run,deterministic_run_sha256=runhash,outcome='Authored exact representation-only successor, no selfvalidation; distinct phase overlay review required')
p.write_text(json.dumps(lease,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'successor':successor,'repair':repair,'run':run,'runhash':runhash,'input_count':len(manifest),'all_leases':'CLOSED'},indent=2))
