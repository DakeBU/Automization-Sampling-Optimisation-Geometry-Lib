import json,hashlib,pathlib,datetime
R=pathlib.Path('E:/Samplinglib')
D=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/next-source-graph94'
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
G=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/next-source-graph93/candidate-source-proof-graph93.v2.native.json'
C=G.with_name('candidate-source-coverage93.v2.native.json')
N=D.parent/'next-primary94/next-edge-recommendation94.native.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def ref(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(name,obj):
 p=D/name
 assert not p.exists(),str(p)
 p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'));return ref(p)
pb=P.read_bytes(); assert sha(pb)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(G.read_bytes())=='21b72b610f1abdaa5b54e04e00f40289f0437f26746b81fa3833f3b2e1bd6922'
assert sha(C.read_bytes())=='dcf8fba06f926ff9149920a997c95446b7693adaccabec3a388e4516a56147e6'
g=json.loads(G.read_text(encoding='utf-8-sig')); c=json.loads(C.read_text(encoding='utf-8-sig')); n=json.loads(N.read_text(encoding='utf-8-sig'))
assert len(g['nodes'])==35 and len(g['edges'])==94 and c['coverage_count']==55
regions=g['source_regions']
for v in regions.values(): assert sha(pb[v['byte_start']:v['byte_end_exclusive']])==v['raw_sha256']
chron=write('source-first-provenance94.native.json',{
 'kind':'independent-source-first-preread-provenance','author':'/root/primary_source93','status':'PREREAD_ONLY_NO_COMPLETION_CREDIT','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'primary':ref(P),'prior_source_only_note':ref(D.parent/'next-primary94/primary-only-remaining94.md'),'prior_recommendation':ref(N),
 'chronology':['Fresh raw source reread before graph inspection this task: lines350-363,613-620,2859-2912,3147-3175,3326-3340.','Inspected frozen independent graph93 only after that raw reread.','Reread raw lines1469-1520,2859-2888,3156-3175 before deriving finer geometric/density nodes.','Constructed this bounded graph from source and prior source-only recommendation; no production Lean read, proof/API search or current reviewer verdict used.'],
 'independence_boundary':'Author previously reviewed path93; this is fresh source-derived topology for a different deterministic target, not source-blind decoding.','no_canonical_mutation':True})
A='A1.SS1.p1'; B='A1.SS1.p2'; PP='A1.SS1.SSS0.Px1.p4.2'; E='A1.E7'; ABS='A1.SS1.SSS0.Px1.p4.3'; MEAS='A1.SS2.p3'
nodes=[];edges=[]
def node(i,kind,claim,anchors,status='PROPOSED_UNPROVED',boundary=''):
 nodes.append({'id':i,'kind':kind,'claim':claim,'source_regions':anchors,'status':status,'boundary':boundary})
def needs(to,frs,use):
 for fr in frs:edges.append({'from':fr,'to':to,'logic':'AND','relation':'source-proof-ingredient-not-Lean-edge','consumer_use':use})
node('H94','source-assumptions','Six analytic binders: alpha>0; alpha<=beta; V C2; all x,v lower and upper Hessian bounds bundled; eta>0; beta*eta<=1.',['S1.p1','S2.SS2.p1'],'SOURCE_GIVEN','Finite-dimensional real Hilbert/Borel typing and rank0 extension are separate. Do not strengthen assumptions; some are unused in this local deterministic argument.')
node('O94','literal-objects','c=y-eta gradV(r), h_r(x)=gradV(x)-gradV(r), literal harmonic Phi, S(x,p)=(x,R_h p) with R0=I, lambda=sqrt(eta)*max(<p,h>,0), Lambda_z(u)=integral_0^u lambda(Phi_s z) ds.',['S3.SS2.p4',A,'A1.E1'],'SOURCE_GIVEN','No alternative bounce or rate semantics.')
node('TIME94','ordered-domain','For n in Nat, finite T>=0, t in Delta_n(T): 0<t1<...<tn<T; t0=0,t_(n+1)=T.',['A1.Ex19'],'SOURCE_GIVEN','For n=0 the empty tuple exists even T=0; for n>0,T=0 there is no tuple.')
node('POST94','prescribed-state-recursion','z0 arbitrary; a_j=Phi_(tj-t_(j-1)) z_(j-1); z_j=S(a_j), 1<=j<=n.',['A1.E2',PP],'LITERAL_SOURCE_ELABORATION','Prescribed events need not have positive rate or arise from actual clocks.')
node('GAMMA94','prescribed-path','Gamma(s)=Phi_(s-tj) z_j for tj<=s<t_(j+1); Gamma(T)=Phi_(T-tn) z_n; internal jump value z_j.',['A1.E2',B,PP],'LITERAL_SOURCE_ELABORATION','Path domain closed [0,T]; no ambient extension or raw actual-process fallback involved.')
node('CONT94','regularity-ingredient','C2 V gives continuous gradient; literal lambda is continuous and nonnegative; s maps to Phi_s z is continuous for each z.',['S1.p1',A,MEAS],'ASTIS_COMPLETION_UNPROVED','Bounce may be discontinuous at zero normal; no bounce continuity required.')
node('ARC94','arc-restriction','On each open interval (tj,t_(j+1)), Gamma(s)=Phi_(s-tj) z_j. On (t_(j-1),tj), Gamma uses incoming arc j-1.',[B,PP],'ASTIS_COMPLETION_UNPROVED')
node('ARCINT94','arc-integrability','For every j=0,...,n, lambda(Phi_(s-tj) z_j) is continuous and integrable on [tj,t_(j+1)].',[A,PP,E],'ASTIS_COMPLETION_UNPROVED','Continuity on finite compact intervals supplies integrability internally; uniform energy cap unnecessary.')
node('ENDPOINT94','finite-null-set','The finite set {t0,...,t_(n+1)} is Lebesgue null; arc and post-bounce path integrands agree away from it.',[B,PP,E],'ASTIS_COMPLETION_UNPROVED','This deterministic integration null set is different from fixed-horizon event-time atomlessness END93. No endpoint state equality asserted.')
node('PATHINT94','whole-path-integrability','s maps to lambda(Gamma(s)) is Lebesgue integrable on [0,T].',[PP,E],'ASTIS_COMPLETION_UNPROVED','Use finite interval partition and finite-null modifications; no generic joint evaluation on uncountable product path space.')
node('TRANSLATE94','elapsed-time-integral','For j=0,...,n, integral_tj^t_(j+1) lambda(Phi_(s-tj) z_j) ds = Lambda_zj(t_(j+1)-tj).',['A1.E1',E],'ASTIS_COMPLETION_UNPROVED','Translation of a finite Lebesgue integral, including terminal j=n and zero length when n=0,T=0.')
node('STITCH94','finite-hazard-stitching','integral_0^T lambda(Gamma(s)) ds = sum_(j=0)^n Lambda_zj(t_(j+1)-tj).',[E],'ASTIS_COMPLETION_UNPROVED','Refines HAZARD93; not stochastic survival or law identity.')
node('LEFT94','incoming-left-limit','For each 1<=j<=n, lim_(s upward tj within [0,T]) Gamma(s)=a_j. Hence the source factor lambda(Gamma(tj-))=lambda(a_j).',[PP,E],'ASTIS_COMPLETION_UNPROVED','Strict ordering makes tj an interior time with an incoming interval. Gamma(tj)=S(a_j), and lambda(Gamma(tj)) must not replace lambda(a_j).')
node('RHO94','existing-density-definition','q_n(t)=product_(j=1)^n ofReal(exp(-Lambda_z_(j-1)(tj-t_(j-1)))*lambda(a_j)); rho_n,T=q_n*ofReal(exp(-Lambda_zn(T-tn))).',[PP,E],'EXISTING_SOURCE_COMPLETION_REUSE','Mathematical finite-clock factorization already used by path93; not a new stochastic premise. Compatibility with exact sealed literal definition must be checked later, not chosen from implementation here.')
node('ALG94','nonnegative-finite-algebra','Nonnegative incoming rates and positive exponential permit finite ofReal product multiplication; exp of negative finite sum is the product of all completed and final survival factors.',[A,E],'ASTIS_COMPLETION_UNPROVED','Zero rates allowed; no division, no conditional normalization, no infinity cancellation.')
node('DENSITY94','recommended-target','For every ordered finite tuple, PATHINT94 and STITCH94 and all LEFT94 clauses hold, and rho_n,T(t)=ofReal(exp(-integral_0^T lambda(Gamma(s)) ds)*product_(j=1)^n lambda(Gamma(tj-))).',[PP,E],'PROPOSED_TARGET_NOT_SEALED','One bounded deterministic prescribed_finite_path_density_rewrite; no new SAU, implementation or completion credit.')
node('ZERO94','edge-case-audit','n0: one terminal arc and empty jump product1; T0,n0: integral0,rho1; T0,n>0: empty domain; rank0 or zero incoming rate permits zero density.',[A,'A1.Ex19',E],'REQUIRED_TARGET_CASES_UNPROVED','n0,T>0 density is exp(-Lambda_z0(T)), not normalized1.')
node('JOINT93','existing-consumer-input','Finite-count complete-history/path law with density rho and arbitrary nonnegative coordinate-measurable tests.',[PP,E],'EXISTING_REVIEWED_BOUNDARY_NOT_REAUDITED','Root reports independent VERIFIED science93; that state is not re-certified or modified here. No production reread.')
node('TERM93','direct-consumer','Substitute DENSITY94 into JOINT93 to obtain the literal A7 fixed-count whole-path density term.',[E],'FUTURE_OPEN','This remains an actual needed substitution, not a wrapper claiming whole A7.')
node('COUNT93','existing-assembly-input','At fixed parameters and T, measurable finite count sectors are pairwise disjoint and cover almost surely.',[B,E],'EXISTING_REVIEWED_BOUNDARY_NOT_REAUDITED','Keep forall fixed T outside AE quantification; no new nonexplosion proof.')
node('ENERGY93','retained-background','Source energy preservation gives uniform rate cap along all prescribed paths with fixed initial energy.',['S3.SS2.p4','A1.SS1.p3'],'EXISTING_PROVENANCE_NOT_REAUDITED','For future printed CAP93; no new energy theorem credit and not needed for DENSITY94.')
node('CAP93','future-printed-convergence-route','For bounded real Psi, abs(sector_n)<=M*(LT)^n/n!, using source rate cap on prescribed paths, survival<=1 and simplex volume T^n/n!.',[ABS,'A1.Ex19'],'FUTURE_OPTIONAL_OPEN','Must derive cap from geometry, not add it as source binder.')
node('MASS93','future-alternative-convergence-route','Use sector mass=P(N_T=n), sum masses1, abs(sector_n)<=M*P(N_T=n); nonnegative Tonelli and positive/negative parts justify signed assembly.',[E],'FUTURE_OPTIONAL_OPEN','ASTIS alternative; not printed author proof, no simplex-volume theorem credit.')
node('A7','downstream-full-path-expansion','Countable finite-sector sum equals expectation for every bounded measurable real path functional; each signed integral exists and sum converges absolutely.',[PP,E,ABS],'FUTURE_OPEN','TERM93 and COUNT93 and one fully justified CAP93/MASS93 route. No full A7 or paper completion here.')
node('SIGMA94','measurable-carrier-boundary','Coordinate-product sigma suffices for selected measurable-functional law. Source does not specify topology; explicit arcs suffice for this deterministic time integral.',[PP,MEAS],'EXPLICIT_ASTIS_SCOPE','Do not assume generic jointly measurable evaluation on all functions; Borel-Skorokhod compatibility remains SKOR93, out of scope.')
needs('O94',['H94'],'Source-specialized literal definitions use eta and gradient.')
needs('POST94',['O94','TIME94'],'Finite recursion at prescribed times.')
needs('GAMMA94',['POST94','TIME94','O94'],'Construct each outgoing arc and terminal value.')
needs('CONT94',['H94','O94'],'Continuity and nonnegativity follow from source analytic data and formulas.')
needs('ARC94',['GAMMA94','TIME94'],'Identify the unique selected interval away from endpoints.')
needs('ARCINT94',['CONT94','POST94','TIME94'],'Continuous arc rate on compact finite interval.')
needs('ENDPOINT94',['TIME94','ARC94'],'Only finitely many endpoint discrepancies.')
needs('PATHINT94',['ARCINT94','ENDPOINT94','ARC94'],'Finite partition and AE congruence supply whole-path integrability.')
needs('TRANSLATE94',['ARCINT94','O94','TIME94'],'Translate s by tj in each interval integral.')
needs('STITCH94',['PATHINT94','TRANSLATE94','ENDPOINT94','TIME94'],'Finite integral additivity including last interval.')
needs('LEFT94',['ARC94','CONT94','TIME94','POST94'],'Local incoming interval and continuity identify each left limit.')
needs('RHO94',['O94','POST94','TIME94'],'Literal finite product plus terminal survival definition.')
needs('ALG94',['CONT94','RHO94'],'Use nonnegativity to transfer finite products through ofReal.')
needs('DENSITY94',['PATHINT94','STITCH94','LEFT94','ALG94','RHO94'],'Conjoin deterministic clauses and substitute hazard sum and incoming factors.')
needs('ZERO94',['O94','TIME94','RHO94','GAMMA94'],'Audit empty products, degenerate horizon, zero normal and rank0 without strengthening domain.')
needs('TERM93',['DENSITY94','JOINT93'],'Replace arc-factor rho by printed whole-path hazard/prejump expression.')
needs('CAP93',['ENERGY93','TIME94'],'Future cap-volume bound for each finite sector.')
needs('MASS93',['JOINT93','COUNT93'],'Future mass normalization and absolute integrability.')
needs('A7',['TERM93','COUNT93','SIGMA94'],'Common countable assembly and declared measurable test class.')
for x in ['CAP93','MASS93']:edges.append({'from':x,'to':'A7','logic':'OR','or_group':'A7-convergence','relation':'source-proof-ingredient-not-Lean-edge','consumer_use':'Exactly one complete convergence/integrability justification is sufficient.'})
allids={x['id'] for x in nodes}
assert len(allids)==len(nodes)
assert all(e['from'] in allids and e['to'] in allids for e in edges)
selected=set(k for x in nodes for k in x['source_regions'])
graph={'schema_version':1,'record_kind':'independent-source-derived-proof-graph-candidate','status':'PREREAD_ONLY_NOT_SEALED_NOT_PROVED','author':'/root/primary_source93','primary':ref(P),'provenance':chron,'prior_graph':ref(G),'prior_coverage':ref(C),'prior_topology_preserved':{'nodes':35,'edges':94,'dispositions':55,'mutation':False},'source_regions':{k:regions[k] for k in sorted(selected)},'target':'DENSITY94','working_name':'prescribed_finite_path_density_rewrite','nodes':nodes,'edges':edges,'node_count':len(nodes),'edge_count':len(edges),'source_assumptions_vs_dependencies':{'analytic_binders':n['recommended_one_statement']['six_analytic_binders'],'quantifiers':n['recommended_one_statement']['quantifiers'],'typing':'Real finite-dimensional Hilbert/Borel phase space, with disclosed rank0 extension of Euclidean source.','dependencies_not_binders':n['no_new_source_binders'],'source_hypotheses_retained_even_if_unused':True},'OR_routes':[{'target':'A7','group':'A7-convergence','alternatives':['CAP93','MASS93'],'shared_required':['TERM93','COUNT93','SIGMA94'],'status':'FUTURE_ONLY'}],'target_AND_route':'Finite arc continuity, finite-null endpoint bridge, integral translation and finite addition, incoming left limits, nonnegative exponential/product algebra. No optional global-cap premise.','edge_cases':n['recommended_one_statement']['edge_cases'],'path_conventions':n['recommended_one_statement']['path_conventions'],'path_sigma_assessment':n['path_sigma_assessment'],'scope':'Deterministic pointwise identities for every valid finite tuple. No actual waiting-time distribution, stopping-time law, normalization, countable sum, signed-test convergence, reversal, invariance, terminal kernel or implementation complexity claim.','canonical_state_mutated':False,'production_Lean_read_for_topology':False,'exact_Lean_statement_sealed':False,'source_text_policy':'Own mathematical paraphrases. Primary arXiv perpetual non-exclusive license is not a license to reproduce full article.'}
gref=write('candidate-source-proof-graph94.native.json',graph)
# Preserve all old coverage rows by immutable reference, then give a complete narrow disposition for each inherited row.
oldrows=c.get('coverage',c.get('dispositions',[]))
if not oldrows:
 oldrows=next(v for v in c.values() if isinstance(v,list) and len(v)==55)
assert len(oldrows)==55
mapping={
 'H93':['H94'],'O93':['O94'],'SIMPLEX93':['TIME94'],'GAMMA93':['GAMMA94'],'HAZARD93':['ARCINT94','ENDPOINT94','PATHINT94','TRANSLATE94','STITCH94'],'LEFT93':['LEFT94'],'TERM93':['TERM93'],'A7':['A7'],'CAP93':['CAP93'],'MASS93':['MASS93'],'ENERGY93':['ENERGY93'],'JOINT93':['JOINT93'],'COUNT93':['COUNT93'],'PATHSPACE93':['SIGMA94'],'SKOR93':['SIGMA94']}
transfer=[]
for row in oldrows:
 targets=sorted(set(y for x in row.get('nodes',[]) for y in mapping.get(x,[])))
 transfer.append({'predecessor_id':row['id'],'source_region':row['source_region'],'source_content':row['source_content'],'disposition':'RETAINED_BOUNDARY_REFERENCE' if targets else 'EXCLUDED_FROM_DETERMINISTIC_TARGET','nodes':targets,'reason':'Inherited source item retained; mapped nodes distinguish current obligations from future/existing boundaries.' if targets else 'Unchanged prior scope/disposition remains in immutable coverage93; no new stochastic, reversal, stationary, kernel, operator or complexity work in this deterministic edge.','prior_disposition':row['disposition'],'prior_reason':row['reason'],'no_new_proof_credit':True})
new=[]
def cov(i,anchors,content,ids,disp='SOURCE_GAP',why='ASTIS supplies omitted deterministic justification; no new source assumption.'):
 new.append({'id':i,'source_regions':[regions[k] for k in anchors],'source_content':content,'disposition':disp,'nodes':ids,'reason':why,'no_proof_credit':True})
cov('C94-01',['S1.p1','S2.SS2.p1'],'Six analytic assumptions, fixed parameters and finite Euclidean phase.',['H94'],'NODE','Retain exact source assumptions; Hilbert/rank0 typing is an explicit elaboration.')
cov('C94-02',['S3.SS2.p4',A,'A1.E1'],'Literal center,residual,flow,reflection,rate and elapsed hazard.',['O94'],'NODE','Source definitions, including zero-normal convention.')
cov('C94-03',['A1.Ex19'],'Strict ordered simplex, augmented initial and terminal times.',['TIME94'],'NODE','Endpoints 0 and T excluded as prescribed jumps.')
cov('C94-04',['A1.E2',B,PP],'Poststate recursion and half-open physical arcs including terminal value.',['POST94','GAMMA94'],'NODE','Prescribed finite paths do not require positive rates or actual clock realization.')
cov('C94-05',[A,MEAS],'Continuous gradient and harmonic arcs give continuous nonnegative arc rate.',['CONT94','ARCINT94'])
cov('C94-06',[B,PP,E],'Explicit interval selection; endpoint jumps only change finitely many time values.',['ARC94','ENDPOINT94'])
cov('C94-07',[E],'Whole-path hazard integrability and translation/addition of all n+1 arcs.',['PATHINT94','TRANSLATE94','STITCH94'])
cov('C94-08',[PP,E],'Each positive-index jump has incoming left-limit state and incoming rate.',['LEFT94'])
cov('C94-09',[E],'Existing completed-arc and final survival factors rewritten as printed exponential and prejump product.',['RHO94','ALG94','DENSITY94'])
cov('C94-10',['A1.Ex19',A,E],'Zero horizon, empty history, rank0 and zero rates.',['ZERO94'])
cov('C94-11',[PP,E],'Exact finite-count law is an existing consumer input; printed fixed-count expression is still future assembly.',['JOINT93','TERM93'],'NODE','No new stochastic proof credited to this deterministic graph.')
cov('C94-12',[E,ABS],'Countable nonnegative and bounded signed-test expansion and convergence.',['COUNT93','CAP93','MASS93','A7'],'EXCLUDED','Future TERM93 plus count partition plus CAP93 OR MASS93; neither route required by DENSITY94.')
cov('C94-13',[PP,MEAS],'Unspecified path sigma/topology and lack of generic uncountable-product joint evaluation.',['SIGMA94'],'SOURCE_GAP','Explicit coordinate sigma sufficient for selected law; Skorokhod compatibility is separate and unresolved.')
cov('C94-14',[A],'Bounce involution and possible discontinuity.',['O94','CONT94'],'EXCLUDED','Retain R0 identity and zero rate, but involution not needed and bounce continuity cannot be assumed.')
cov('C94-15',['A1.E1','A1.E2',MEAS],'Actual exponential clocks, generalized inverse, raw stopped recursion, Borel terminal version.',['JOINT93'],'EXCLUDED','Existing upstream law provenance; deterministic tuple statement neither re-proves nor takes these as binders.')
cov('C94-16',['S3.SS2.p4','A1.SS1.p3',ABS],'Energy cap and stationary/reference distribution context.',['ENERGY93','CAP93'],'EXCLUDED','Energy cap only future printed summability route; fixed reference and initial phase have no distribution in target.')
cov('C94-17',[ABS],'Integration of A7 against stationary initial measure and ensuing reversal.',['A7'],'EXCLUDED','Downstream invariance/reversal is beyond countable A7 and this deterministic edge.')
coverage={'schema_version':1,'record_kind':'bounded-source-coverage-and-inherited-dispositions','status':'PREREAD_ONLY_NOT_ACCEPTED','graph':gref,'primary':ref(P),'prior_coverage':ref(C),'prior_inventory_preserved_count':55,'inherited_dispositions':transfer,'new_narrow_dispositions':new,'new_narrow_disposition_count':len(new),'source_gap_meaning':'An omitted representation or intermediate proof argument to be supplied by ASTIS, not an author error or permission to add hypotheses.','coverage_boundary':'Every one of the55 frozen prior items retained by exact reference with a narrow disposition;17 refined items cover the deterministic target and explicit exclusions. Not whole-paper exhaustive.','unmapped_inherited_rows':[],'uncovered_selected_inventory_rows':[],'canonical_state_changed':False}
cref=write('candidate-source-coverage94.native.json',coverage)
# Directed acyclicity and exact source slice hashes are artifact consistency checks only.
adj={x:[] for x in allids}
for e in edges:adj[e['from']].append(e['to'])
vis=set();active=set()
def walk(x):
 assert x not in active,'cycle '+x
 if x in vis:return
 active.add(x)
 for y in adj[x]:walk(y)
 active.remove(x);vis.add(x)
for x in allids:walk(x)
checks=write('artifact-checks94.native.json',{'kind':'preread-artifact-consistency-only','primary_sha_checked':True,'all_inherited_source_region_byte_hashes_checked':len(regions),'new_nodes':len(nodes),'new_edges':len(edges),'graph_acyclic':True,'prior_nodes_edges_dispositions':[35,94,55],'inherited_dispositions':len(transfer),'new_dispositions':len(new),'all_edge_endpoints_exist':True,'no_Lean_build_or_proof_validation':True})
inputs=[ref(P),ref(G),ref(C),ref(N),ref(D.parent/'next-primary94/primary-only-remaining94.md')]
outputs=[chron,gref,cref,checks,ref(D/'write_graph94.py')]
manifest=write('closed-RAW-manifest94.native.json',{'schema_version':1,'kind':'closed-RAW-preread-manifest','status':'PREREAD_ONLY_NO_COMPLETION_CREDIT','hash_recipe':'SHA256 of exact file bytes, before parsing or newline normalization; offsets byte_start inclusive, byte_end_exclusive. Manifest excludes itself to avoid recursive hash; its RAW SHA is reported externally. No JSON canonical hash substituted for RAW.','inputs':inputs,'outputs':outputs,'closed':'All authored files in owned directory except this manifest enumerated as outputs. External files are read-only inputs.','no_production_or_canonical_files_written':True})
print(json.dumps({'graph':gref,'coverage':cref,'manifest':manifest,'counts':[len(nodes),len(edges),len(transfer),len(new)]},indent=2))
