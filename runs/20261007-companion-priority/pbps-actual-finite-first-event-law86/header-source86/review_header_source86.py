"""Whole prospective private-Prop source scope audit, no proof implementation."""
from pathlib import Path
from html.parser import HTMLParser
import ast,copy,datetime,hashlib,json,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def read(p):return json.loads(p.read_bytes())
def put(n,j):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
header=O.parent/'header86.proposed.lean';assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert pin(header)['raw_sha256']=='51e925d7a7874083c0802682e7157fcaa2adf6961c2f1ba711d1646ab35e32d8' and pin(header)['bytes']==5294
fp=B/'overlay-review86/freeze_primary_review86.py';ns={'HTMLParser':HTMLParser,'re':re};tree=ast.parse(fp.read_text(encoding='utf8'));exec(compile(ast.Module(body=[next(n for n in tree.body if isinstance(n,ast.ClassDef))],type_ignores=[]),str(fp),'exec'),ns)
x=ns['X']();x.feed(primary.read_text(encoding='utf8'));i0=read(B/'source-inventory86.json');g0=read(B/'source-proof-graph86.json')
for a in i0['anchors']:assert sha(x.norm(a['source_id']).encode())==a['normalized_anchor_sha256']
assert pin(B/'overlay-review86/fresh-primary-topology86.json')['raw_sha256']=='a50b617c244a513777a10b5db9766e47a1bddbd4deb061c1c065fef935d7fee6'
proposal=B/'independent-topology86/proposed-topology-overlay86.json';assert pin(proposal)['raw_sha256']=='a8bff963452d39a1b971a90a4c68c5737ef519d9b7266294483ebf6694d3370d'
gi=read(B/'source-proof-graph86.reviewed-effective.json');ii=read(B/'source-inventory86.reviewed-effective.json')
# Replay only the already separately reviewed exact patch; compare mathematics, not root adoption reports.
g=copy.deepcopy(g0);i=copy.deepcopy(i0)
for op in read(proposal)['operations']:
 obj=g if op['file']=='graph' else i
 if op['action']=='append':obj['nodes' if op['id'].startswith('G') else 'edges'].append(op['after'])
 else:
  if op['field'].startswith('junction.routes['):
   route=op['field'].split('[',1)[1].split(']',1)[0];rec=next(q for q in next(q for q in obj['junctions'] if q['target']==op['id'])['routes'] if q['route']==route);key='ingredients'
  else:rec=next(q for q in obj['nodes' if op['id'].startswith('G') else 'items'] if q['id']==op['id']);key=op['field']
  assert rec[key]==op['before'];rec[key]=op['after']
for key in ['nodes','edges','junctions']:assert gi[key]==g[key],key
assert ii['items']==i['items'] and ii['anchors']==i['anchors']
assert (len(ii['items']),len(gi['nodes']),len(gi['edges']))==(40,37,71)
s=header.read_text(encoding='utf8');assert not re.search(r'(?m)^(?:private )?(?:theorem|lemma)\s',s)
assert len(re.findall(r'(?m)^private def ',s))==1
defs={}
matches=list(re.finditer(r'(?m)^    let ([^ :]+)\s*:',s))
for k,m in enumerate(matches):
 stop=matches[k+1].start() if k+1<len(matches) else s.index('    ∀ y xRef : E, ∀ z : E × E,',m.end())
 defs[m.group(1)]=s[m.start():stop].strip()
assert list(defs)==['P','ε','c','Φ','S','rate','Λ','τ','U','F','A','d','ρ','J']
object_findings={
 'P':'Literal countable independent expMeasure1 product, not supplied law. Concrete probability and coordinate marginal must be derived with existing UnitExponentialProduct, not assumed.',
 'ε':'toNNReal(sample k); coordinate0 is source E1. It equals positive real coordinate AE under actual product; invalid negative/zero samples may map0, which A excludes.',
 'c':'Exact center y-eta gradient V(xRef).',
 'Φ':'Exact actual real-time harmonic formula with sqrt eta momentum scale and -sin/sqrt eta velocity term.',
 'S':'Actual position-fixed orthogonal reflection. Total real division gives zero correction at zero normal, hence source R0=I. Borel, no continuity demanded.',
 'rate':'sqrt eta * max 0 <p,grad V(x)-grad V(xRef)>, source Ex1, continuous nonnegative.',
 'Λ':'Actual interval integral 0..t along actual Phi; NNReal horizon and source C1 derivative derived, not extra hypothesis.',
 'τ':'Actual hittingAfter of Lambda-e at Ici0 starting0, equivalent to source inf threshold and empty top under the existing actual clock contract.',
 'U':'Literal actual first waiting time tau evaluated at epsilon coordinate0, WithTop NNReal. No abstract event/process supplied.',
 'F':'Real coercion of untopD0. Used only under A where U is positive and bounded by finite T, so top/default0 cannot create a false marked event.',
 'A':'0<U and U≤finite T. Measurable restriction keeps first finite positive event; missing mass includes U>T or top. Null zero threshold removed explicitly.',
 'd':'rate(Phi_s z)*exp(-Lambda_z(toNNReal s)); nonnegative continuous on finite positive interval. Negative s extension has no effect on restricted density.',
 'ρ':'Lebesgue restricted Ioc(0,T), with ENNReal.ofReal(d) density. Unnormalized finite subprobability, mass 1-exp(-Lambda(T)), with no division by event probability.',
 'J':'(toNNReal s,S(Phi_s z)), exactly event time plus actual post-bounce phase from initial T0=0 in A2. Global Borel real-time extension; only positive finite s consumed.'}
objects=[{'name':name,'literal_definition_sha256':sha(body.encode()),'definition':body,'assessment':object_findings[name],'decision':'SOURCE_FAITHFUL_LITERAL_OR_EXPLICIT_ASTIS_ADAPTER'} for name,body in defs.items()]
slots={
 'objects':{'original':'A1.E1/E2 actual iid Exp1 wait and post-bounce initial phase; Ex1-3 literal rate/flow/S. A7 jump density factor.','reconstructed':'Concrete P,epsilon,c,Phi,S,rate,Lambda,tau; U,F,A,d,rho,J are explicit finite first-event and post-bounce law adapters.','evidence':'All fourteen definitions audited. Eight literal objects agree with source; finite law/marked measure packaging is attributed ASTIS completion.','relation':'faithful-bounded-elaboration'},
 'domains':{'original':'Real Euclidean full phase, fixed y/reference/z, finite nonnegative horizon; bounded measurable path tests in A7.','reconstructed':'Finite-dimensional real inner-product Borel E, fixed y,xRef,z; T:NNReal; Borel real h on NNReal×(E×E), real M>=0 globally bounding |h|.','evidence':'Coordinate-free/rank0 packaging is explicit. Real s is restricted to Ioc(0,T); d/J negative-time extensions cannot change the law.','relation':'faithful-bounded-elaboration'},
 'quantifiers':{'original':'Fixed parameters, initial phase, finite horizon, independent actual clocks; no uniform exceptional set across arbitrary states.','reconstructed':'Six source binders before literal definitions; forall fixed y,xRef,z, measurability outputs; forall T; forall h measurable; forall M>=0 and global bound, three L1 and integral outputs.','evidence':'No random-initial-state substitution, no all-parameters uniform AE claim. Tests have standard bounded-Borel class binders rather than extra dynamics assumptions.','relation':'faithful-bounded-elaboration'},
 'assumptions':{'original':'0<alpha<=beta, C2V, global Hessian sandwich, eta>0 and beta eta<=1.','reconstructed':'Exactly hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta with finite-dimensional Borel real phase infrastructure.','evidence':'No supplied hazard regularity, measured process, clock marginal, normalizer, invariance, positivity of rate/cap, inverse strictness, tail conditioning or path-law premise.','relation':'source-assumptions-preserved'},
 'conclusion':{'original':'A7 includes finite event density lambda(Phi_s z)exp(-Lambda_z(s)); A2 supplies its actual post-bounce mark.','reconstructed':'Meas U,F,J and A; finite restricted waiting law=rho; marked law=map J rho; finite rho, real mass=1-exp(-Lambda T), mass<=1; three integrability claims and exact bounded marked integral identity.','evidence':'This supplies first-event density, not just existing CDF/tail or measurability wrapper. It does not assert n-event path weights or full A7.','relation':'faithful-bounded-elaboration'},
 'scopes':{'original':'Complete A7/A8/invariance/L2 needs further conditional iteration, path conventions, change of variables, rho-survival identity, summability and contraction/density.','reconstructed':'Doc explicitly leaves full path law, unused-tail conditioning, reversal, invariance, semigroup/allL2, errors/cost/main/composition OPEN.','evidence':'Whole private Prop has no those conclusions. Zero/infinite waits and zero normal are retained. Source failed terminal limit0 versus later actual fallback convention is not used here to assert a stronger path law.','relation':'explicit-bounded-scope'},
 'constant_dependencies':{'original':'Hazard weight exp(-Lambda), rate sqrt eta max0, original beta*eta<=1; bounded functional norm.','reconstructed':'Exact unit Exp scale1, original eta scaling, no renormalizer; M>=0 is an arbitrary test bound. T is any finite NNReal and rho mass≤1.','evidence':'No division by rate/cap or by event probability; no new uniform exponential envelope or integrability premise. Three L1 outputs must be derived from finite event mass and bounded tests.','relation':'source-constants-preserved'}}
binders=[{'binder':n,'assessment':v} for n,v in [
 ('hα','0<alpha'),('hαβ','alpha≤beta'),('hV','C2V'),('hH','forall x,v: lower and upper global Hessian quadratic bounds'),('hη','0<eta'),('hβη','beta*eta≤1'),('E infrastructure','finite-dimensional real inner product, Borel measurability; coordinate-free source domain, rank0 allowed'),('y/xRef/z','fixed arbitrary full actual initial phase, not correlated randomness'),('T','any finite NNReal'),('h and M','Borel real marked test with arbitrary nonnegative global bound, not additional source dynamics assumption')]]
clause_findings=[
 ('Measurable U/F/J','Joint Borel source maps and hitting-time adapter derive fixed-fiber outputs; projection default measurable.'),
 ('MeasurableSet A','Positive wait and finite upper threshold event, all samples, no AE shortcut required for measurability.'),
 ('map F(P restrict A)=rho','Genuine new density equality from actual first-wait law plus derived FTC/finite-measure uniqueness; not assumed.'),
 ('marked law equality','Map composition using actual J and finite support. No phase evaluated at top; A ensures finite projection correctness.'),
 ('finite rho/real mass/ENNReal bound','Source first-event subprob mass 1-exp(-Lambda T); includes waiting beyond horizon/infinite in complement.'),
 ('Integrable h(map J rho)','Bounded Borel test on finite measure.'),
 ('Integrable h(J(F(sample)))(P restrict A)','Actual product restricted finite event, bounded test.'),
 ('Integrable h(J(s))*d(s)(volume restrict Ioc0T)','Nonnegative density, finite mass, measurable bounded h; local integrability derived.'),
 ('exact integral identity','Map/withDensity transfer of the newly proved first-event law, source A2 mark.')]
selected_nodes={1,2,3,4,5,9,10,35,36}
inventory_selected={1,2,3,4,5,6,7,8,11,12,13,14,15,16}
inventory_coverage=[{'id':q['id'],'source_ids':q['source_ids'],'nodes':q['nodes'],'header_role':('SELECTED_CONTEXT_OR_OBLIGATION' if int(q['id'][-2:]) in inventory_selected else 'FUTURE_OPEN_OR_EXCLUDED_SOURCE_BOUNDARY'),'decision':'SCOPED_COVERED_NO_FULL_SOURCE_COMPLETION'} for q in ii['items']]
node_coverage=[{'id':q['id'],'source_ids':q['source_ids'],'source_classification':q['classification'],'header_role':('SELECTED_INGREDIENT_OR_TARGET' if int(q['id'][-2:]) in selected_nodes else 'FUTURE_OPEN_OR_EXCLUDED_NOT_CLAIMED'),'note':('G35 CDF/FTC is selected sufficient route; G36 remains OR alternative' if int(q['id'][-2:]) in [35,36] else 'Source context/obligation only, no theorem completion credit')} for q in gi['nodes']]
relation_coverage=[{'id':q['id'],'from':q['from'],'to':q['to'],'route':q['route'],'dependency_edge':q['dependency_edge'],'header_role':('EXCLUDED_ASSOCIATION_NO_IMPLICATION' if not q['dependency_edge'] else ('SELECTED_OR_ALTERNATIVE_ROUTE_INGREDIENT' if q['to'] in ['G86-09','G86-10'] or q['id'] in ['E86-01','E86-02','E86-03','E86-04','E86-05'] else 'FUTURE_OPEN_OR_BACKGROUND_NOT_CLAIMED'))} for q in gi['edges']]
evidence=put('header-source.run-evidence86.json',{
 'schema':'astis.prospective-whole-header-source-run86.v1','status':'closed','created_utc':now,'primary':pin(primary),'header':pin(header),
 'source_first_chronology':['Pinned primary reread; original freeze RAWs and all56 anchors checked before opening header in this phase.','Exact header RAW/5294 bytes verified, entire single private Prop read.','Reviewed-effective source mathematics independently matched to exact19-operation replay; no root adoption report read.','All binders/14 definitions/outputs and 40 inventory/37 nodes/71 relations mapped; no implementation BODY or math-review decision consulted.'],
 'reused_evidence':{'original_source_first_seal':pin(B/'source-first-seal86.json'),'fresh_primary_topology':pin(B/'overlay-review86/fresh-primary-topology86.json'),'distinct_exact_overlay_review':pin(B/'overlay-review86/overlay-review.decision86.json'),'source_only_statement_API_receipt':pin(B/'statement-api-retrieval86.json')},
 'checks':{'header_bytes':5294,'private_Prop_count':1,'theorem_BODY_count':0,'six_source_analytic_binders':6,'literal_objects':8,'derived_adapters':6,'all_original56anchors_rechecked':True,'effective_exact_patch_replay':True,'inventory':40,'nodes':37,'relations':71,'dependencies':68,'excluded_associations':3},
 'independence':{'reviewer':'/root/fresh_source78','distinct_from_header_writer':True,'original_source_extractor_role_disclosed':True,'exact_overlay_not_authored_by_reviewer':True,'source_primary_topology_frozen_before_header':True,'no_other_reviewer_verdict_basis':True,'no_Lean_proof_BODY_read':True,'proposer_prior_BODY_leak_not_used_as_independent_source_evidence':True},
 'scope':'Prospective whole-header source review only. Final compiled BODY, publication and canonical anti-anchored blind reconstruction audit still required separately. No header Seal, proof, state, or source completion.'})
decision=put('header-source.decision86.json',{
 'schema':'astis.prospective-whole-header-source-decision86.v1','status':'closed','created_utc':now,'verdict':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_SCOPE','review_run_sha256':evidence['raw_sha256'],
 'header_raw_sha256':pin(header)['raw_sha256'],'semantic_slots':slots,'binder_audit':binders,'literal_and_derived_object_audit':objects,'whole_conclusion_audit':[{'clause':k,'source_assessment':v,'decision':'SOURCE_FAITHFUL_BOUNDED_OBLIGATION'} for k,v in clause_findings],
 'source_graph_coverage':{'inventory_items':inventory_coverage,'nodes':node_coverage,'relations':relation_coverage,'gaps':[],'counts':{'inventory':40,'nodes':37,'relations':71,'dependencies':68,'excluded_associations':3}},
 'boundary_cases':{'T0':'A empty and rho zero; all three L1 and zero integral valid.','rank0':'rate zero; positive thresholds wait top, no finite event mass.','zero_normal':'Total reflection is identity; no extra assumption excludes it.','flat_hazard':'CDF/FTC route does not invert a strictly monotone hazard; density zero on flat arcs.','infinite_wait':'U=top excluded by U≤finite T; F default0 cannot generate J(0) false event.','threshold0_or_negative_raw_input':'epsilon=0 can yield U0; A positive restriction removes it, consistent with actual Exp1 null exception.','M0':'Zero test; no positive M required.','endpointT':'Finite event at exactly T allowed by Ioc/A≤T, source strict simplex endpoint ambiguity avoided; nonatomic derived density makes later strict endpoint adaptation possible.','fixed_params':'No uniform all-parameter AE event or arbitrary correlated random initial state substitution.'},
 'deltas':[],'required_repairs':[],'no_required_mathematical_or_source_repairs':True,
 'truth_boundary':'Bounded first-event density plus post-bounce marked law is a genuine next producer for A7, not full A7, a process Markov theorem, invariance, or allL2. Assumptions/actual inputs unchanged; source implicit first-factor proof is explicit ASTIS completion. This is not proof acceptance or VERIFIED.'})
inputs=[primary,header,B/'source-inventory86.json',B/'source-proof-graph86.json',B/'source-first-seal86.json',fp,B/'overlay-review86/fresh-primary-topology86.json',proposal,B/'overlay-review86/overlay-review.decision86.json',B/'overlay-review86/overlay-review.run-evidence86.json',B/'source-inventory86.reviewed-effective.json',B/'source-proof-graph86.reviewed-effective.json',B/'statement-api-retrieval86.json']
manifest=put('header-source.run-manifest86.json',{'schema':'astis.raw-prospective-header-source-manifest86.v1','status':'closed','created_utc':now,'raw_inputs':[pin(q) for q in inputs],'raw_outputs':[pin(q) for q in sorted(O.iterdir()) if q.is_file() and q.name!='header-source.run-manifest86.json'],'manifest_self_hash_omitted':True,'noncircular':'Evidence binds immutable earlier inputs; decision binds evidence RAW; manifest binds all outputs except itself.','no_original_header_or_shared_production_state_mutation':True})
for q in [O/'header-source.decision86.json',O/'header-source.run-evidence86.json',O/'header-source.run-manifest86.json']:print(json.dumps(pin(q)))
