"""Close independent source/full-BODY review83; native owned files only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,copy
R=Path('E:/Samplinglib');RUN=R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83';O=RUN/'independent-source83'
B=R/'runs/20261007-companion-priority/pbps-bounded-test-preread83'
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
PACKET=RUN/'source-review83.packet.json';MODULE=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean'
LESSON=R/'website/content/declaration_lessons/pbps-actual-bounded-test-continuity.json'
CANON='7726306966313a43399d1b2297f2f3e2821cc2118cd63bd6790d62c1bc6ee439'
MODSHA='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
PUBSHA='d9e38c7530c2c337b7e95a866a299ba3110c9f1c64db4e4d2e049f0b90fcf04c'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf8'))
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def save(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
assert sha(P)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
manifest_names=['source_freeze83.closed-raw-manifest.json','overlay-review83/overlay-review83.closed-raw-manifest.json','header-source-review83/header-source-review83.closed-raw-manifest.json']
manifest_pins=['6f0e838a8c3ada6dec3d3e842be55252885f0ba49f861256309963d5e8b6201d','22be7ba723c330baca0875e389c125fb7aff11018e8556b35a63c752acb07785','f1e52b12be1013d581400b98db0e37916ba82e23c6903451122e6828ffd71831']
preseal=[]
for name,pin in zip(manifest_names,manifest_pins):
 p=B/name;assert sha(p)==pin
 m=load(p)
 for a in m['raw_inputs']+m['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
 preseal.append(raw(p))
inv=load(B/'source_inventory83.json');orig=load(B/'source_proof_graph83.json');sup=load(B/'optional-route-topology-supplement83.json')
GP=B/'source_proof_graph83.reviewed-effective.json';g=load(GP)
assert sha(GP)=='1c051926157579e6a62d2984868340504a9b4708890fc61da4cdea34409a80c3'
overlay=load(B/'independent-topology83/proposed-minimal-topology-overlay83.json')
expected=copy.deepcopy(orig['edges']+sup['added_edges']);ee={e['id']:e for e in expected}
for eid,a in zip(['E83-29','E83-30','E83-28'],overlay['patches']):
 if eid!='E83-28':assert ee[eid]['status']==a['before'];ee[eid]['status']=a['after']
 else:assert ee[eid]==a['before'];ee[eid].clear();ee[eid].update(a['after'])
assert g['nodes']==orig['nodes'] and g['edges']==expected and g['reviewed_junctions']==overlay['junctions']
assert (len(inv['items']),len(g['nodes']),len(g['edges']))==(30,17,30)
assert sum(e.get('dependency_edge',True)for e in g['edges'])==29
x=load(PACKET);q={k:v for k,v in x.items()if k!='packet_sha256'}
assert sha(PACKET)=='ed5ccf8591bde857b95b93328a7cb16c4da356e81d2b1351ad0a05ba7e93be36'
assert hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==CANON==x['packet_sha256']
assert x['publication_binding_sha256']==PUBSHA
c=x['candidate_publication_context'];mb=MODULE.read_bytes();ms=mb.decode()
assert sha(MODULE)==MODSHA==c['file'] and mb==c['current_lean_module'].encode()
assert hashlib.sha256((R/'lean-toolchain').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==c['toolchain']
assert hashlib.sha256((R/'lake-manifest.json').read_bytes().replace(b'\r\n',b'\n')).hexdigest()==c['dependencies']
assert hashlib.sha256(x['blind_reconstruction']['text'].encode()).hexdigest()==x['blind_reconstruction']['text_sha256']
assert x['blind_reconstruction']['source_text_visible']is False
assert hashlib.sha256(x['source']['original_text'].encode()).hexdigest()==x['source']['text_sha256']
unit=load(LESSON)['units'][0];assert {k:v for k,v in unit.items()if k!='boundary'}==c['lesson']
hs=(RUN/'header83.proposed.lean').read_text('utf8');assert sha(RUN/'header83.proposed.lean')=='1bf2b24f0ba521449aba10ac3559a27c4db7f2eab0df89c98587f623695b07ff'
hn=hs.index('private def ');mn=ms.index('private def ')
assert hs[hn:hs.index('\nend',hn)].strip()==ms[mn:ms.index('\n\n\nset_option maxHeartbeats',mn)].strip()
parent82=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'
assert ms[ms.index('    {E : Type*}'):].startswith('\n'.join(parent82.read_text('utf8').splitlines()[15:90]))
assert re.findall(r'    let (\S+)',ms[:ms.index('set_option maxHeartbeats')])==['P','ε','c','Φ','S','rate','Λ','τ','next','record','eventTime']
assert not re.search(r'\b(?:axiom|sorry|admit)\b',ms) and 'Prop := True'not in ms
findings=[
 'Same literal canonical probability input, harmonic center/flow, rate and initial-state integrated hazard. Private Prop retains all11 source actual definitions, source six binders and stopped-recursion semantics.',
 'Direct actual82 call returns the same single Z,hZM,hcovered,hfallback,hAE,hshort. Four producer calls are internal: actual82, actual77 hazard continuity/zero, actual73 flow continuity/Phi0 and actual Exp-product probability. hclock.2.2.2.1 is exactly hazard basic0; hflow.2.2.1 exactly Phi0. All old clauses returned before new test quantifiers.',
 'For each fixed tuple/time, pull back joint Z measurability, compose continuous real f, obtain AEStronglyMeasurable and Integrable.of_bound using actual finite probability P and global abs boundM. Actual integral existence is proved, not inferred from total Bochner integral notation.',
 'D_t measurable from actual82. Indicator of constant2M integrable. Pointwise discrepancy norm bounded by2M on D_t via two global test bounds; outside D_t equality makes it0. Bound holds every raw sample, no identification of defect with event count.',
 'norm_integral_le_of_norm_le uses integrable indicator; integral_sub uses separately proved actual hfi and constant integrability. Probability normalization integrates constant freeflow test to itself; exact indicator integral=2M P.real(D). Multiply actual82 bound by2M>=0. No toReal infinity loophole because actual P is probability.',
 'Return measurable/integrable/quantitative estimates at all finite times. Restrict joint actual flow/hazard continuity to NNReal time and fixed tuple. Test continuity plus Phi0=id yields test-flow limit. Hazard0 fact already obtained in step2, used explicitly in step7; displayed Lambda_t->Lambda0=0 is licensed by available facts.',
 'Actual hazard continuity/zero and continuous exp imply q_t->0; multiply fixed finite2M. No linear capCt, moment bound or samplewise-AS argument required.',
 'Absolute expectation difference squeezed between0 and2M q_t, convert real norm limit to signed difference0, add independent test-flow limit and cancel. Ordinary nonpunctured NNReal0 includes0 consistently with actual82 AEinit. Only fixed-state/test expectation prerequisite, no outer-state L2 argument.'
]
lines=mb.splitlines(keepends=True);regions=[];seen=set();overlaps=[]
for i,s in enumerate(unit['steps'],1):
 a=s['lean_source_region'];lo,hi=a['start_line'],a['end_line'];code=b''.join(lines[lo-1:hi])
 assert a['source_raw_sha256']==MODSHA and code.decode()==s['lean'] and hashlib.sha256(code).hexdigest()==a['exact_code_raw_sha256']
 for ln in range(lo,hi+1):
  if ln in seen:overlaps.append(ln)
  seen.add(ln)
 regions.append({'step':i,'title':s['title'],'start_line':lo,'end_line':hi,'exact_code_raw_sha256':a['exact_code_raw_sha256'],'formula_reviewed':True,'prose_reviewed':True,'BODY_reviewed':True,'formula_BODY_exact_match':True,'finding':findings[i-1]})
gaps=sorted(set(range(121,231))-seen)
assert len(regions)==8 and not gaps and not overlaps
assert [a['tex']for a in c['formulae']]==[unit['steps'][i]['formula']for i in [2,3,4,7]]
authored={'expected_steps':8,'reviewed_steps':8,'body_start_line':121,'body_end_line':230,'gaps':gaps,'overlaps':overlaps,'formula_body_exact_matches':8,'steps':regions,
 'whole_module_imports_scopes_private_Prop_public_theorem_BODY_read':True,'header_private_Prop_exact_unchanged':True,
 'all_public_formulae_reviewed':True,'all_public_assumptions_statement_boundary_reviewed':True,'native_lesson_equal_to_packet_except_boundary':True,'native_boundary_separately_audited':True}
slots={
 'objects':{'original':'Actual harmonic phase and iid Exp1 event recursion, physical interpolation, source C_c pointwise test expectation ingredient.',
 'reconstructed':'Blind reconstructs literal11 definitions, one total jointly Borel Z with all actual82 clauses, and actual real test integral under canonical P; same Z precedes every f/M.',
 'evidence':'Entire private Prop and BODY121-146 match source A1.E1/E2/Ex1-3 and retained actual82. BODY147-230 derives actual bounded-test integrals/estimate/limit, not an arbitrary supplied process/kernel/certificate.', 'relation':'explicit-elaboration'},
 'domains':{'original':'Finite-dimensional Euclidean phase, finite nonnegative physical time with possibly infinite waits; source C_c tests.',
 'reconstructed':'Blind states intrinsic finite-dimensional real Borel E including rank0, product norm E×E, NNReal finite times and extended waits, continuous real tests with global boundM.',
 'evidence':'No dimension positivity/positive waiting-time premise. Literal product norm gives finite-dimensional phase topology. C_b is explicit ASTIS extension of source C_c pointwise class, no unbounded-test/Feller C0 claim.','relation':'explicit-elaboration'},
 'quantifiers':{'original':'Fixed deterministic y,r,z0 pointwise expectation before outer state integration; C_c test arbitrary.',
 'reconstructed':'Blind accurately separates allraw covered/fallback from each-fixedparams common AEallfinite/init, all finite-t measurable estimates and each real delta>0 tail limit. One Z before every continuous f and every admissible M>=0; expectation limit ordinary nonpunctured NNReal0.',
 'evidence':'BODY132-146 selects/retains single actual82 Z before intro y xRef z0 f hf M hM hbound. No uniformparams AE or arbitrary correlated random-state substitution; no uniform test/state/time convergence. Bound valid at0 and M0 via same proof.','relation':'explicit-elaboration'},
 'assumptions':{'original':'Six original dynamics conditions: alpha>0,alpha<=beta,V C2,Hessian sandwich everywhere,eta>0,eta<=1/beta.',
 'reconstructed':'Blind lists exactly hα,hαβ,hV,hH,hη,hβη. Continuous real f and nonnegative global abs boundM define test class, not a seventh dynamics assumption.',
 'evidence':'Exact unchanged header/private Prop and actual82 prefix verified. beta>0 follows alpha>0<=beta, so beta eta<=1 retains source scale. Probability, phase measurability, defect probability, flow/hazard continuity and actual integrability are produced internally, no public certificate premises.','relation':'equivalent'},
 'conclusion':{'original':'Ex22 first-event probability vanishes and deterministic flow tends identity; implicit pointwise C_c expectation convergence feeds source p6.2 outer L2 DCT.',
 'reconstructed':'Blind correctly states all retained82 outputs plus each finite-t actual test measurability/integrability, abs(E f(Z_t)-f(Phi_tz0))<=2M(1-exp(-Lambda_t)), and fixedstate expectation limit f(z0).',
 'evidence':'BODY147-191 proves actual integrability/2M estimate,192-230 proves limit. Source firstevent controls phase-flow defect by inclusion, then bounded integration and deterministic continuity close genuine missing pointwise expectation consumer. Quantitative2M and C_b are attributed ASTIS elaborations, not literal source theorem quotation.','relation':'explicit-elaboration'},
 'scopes':{'original':'Source p6.1 first has invariance/Jensen contraction; p6.2 outer-state DCT and density/contractivity extend to full L2. Memoryless Markov constructed earlier, not consequence of this limit.',
 'reconstructed':'Blind gives fixedparameter/test clock expectation only and distinguishes sequencewise vs AE quantifiers. Bound publication explicitly leaves full L2/process/law/cost/main/composition obligations OPEN.',
 'evidence':'G15/G16/G17 excluded; E28 is nondependency boundary association. Preferred integrated-defect AND branch used; complete epsilon/delta alternative G13/E24/E29/E30 is OR and unused. No AS inference or outer-state DCT appears in BODY; no unbounded-cost transfer.','relation':'explicit-elaboration'},
 'constant_dependencies':{'original':'Exact eta/sqrteta/reciprocal scales, Exp1 clocks and source E_(n+1), initial-state hazard q_t=1-exp(-Lambda_t).',
 'reconstructed':'Blind preserves exact scales/signs/index0 and numerical1,2, every finite real M>=0; no extra dimension/cap/moment/time-rescaling constant.',
 'evidence':'All11 definitions literal.2M is sum of two global abs bounds, multiplied only by nonnegative2M and true finite probability. Initial-state freeflow hazard, not current-path hazard. No Ct output or quantitative phase-distance rate.','relation':'explicit-elaboration'}}
assert set(slots)==set(x['review_contract']['semantic_slots'])
assert all(s['relation']in x['review_contract']['slot_relations']for s in slots.values())
deltas=[]
def delta(slot,classification,desc):deltas.append({'id':f'D83-{len(deltas)+1:02d}','slot':slot,'classification':classification,'blocking':False,'description':desc})
delta('objects','notation-resolution','Index0 real exponential coordinate realizes source E1, clamp is AE actual positive clock. Literal stopped records and source physical phase retained.')
delta('domains','explicit-elaboration','Intrinsic Borel/rank0/product phase and NNReal finite time preserve source phase topology; source C_c extended explicitly to bounded continuous real C_b tests.')
delta('quantifiers','quantifier-clarification','One Z before all tests/bounds; every admissible M>=0 globalbound quantified. Fixedparams AEallfinite/init retained; no uniformparams nullset or arbitrary correlated random-parameter substitution.')
delta('assumptions','test-class-definition','Continuity and boundedness of f define the tested class, not added potential/trajectory hypotheses. All six source dynamics binders exact.')
delta('conclusion','source-implicit','Pointwise expectation convergence is genuine implicit ingredient between Ex22 rare-first-event/flow control and outer-state DCT, now derived from actual inputs.')
delta('constant_dependencies','explicit-elaboration','Explicit2M estimate follows bounded discrepancy on phase-flow defect. Defect is only contained in first-event event; no equality, Ct cap or moment rate asserted.')
delta('scopes','formalization-convention','Uncovered fallbackz0 is labelled ASTIS representative vs source failed-limitzero; fixedparams null exceptions ignored by integrals. Last infinite-wait arc remains live and covered; stopped dummy never phase.')
delta('scopes','optional-route-not-used','Preferred complete integrated-defect route used. E29/E30 AND inside optional epsilon/delta route, whole branch OR with preferred route. No probability->AS DCT shortcut.')
delta('scopes','excluded-boundary','Fullouter L2/invariance/Jensen/density/operator laws/Markov/restart/main/cost/composition remainOPEN; E28 dependency_edge=false association is not theorem implication.')
delta('quantifiers','nonpunctured-zero','Ordinary NNReal nhds0 includes0; actual AEinit and Phi0=id make actual expectation0=f(z0), quantitativeq0=0 compatible even raw zero thresholds exceptional.')
node_map={
1:('COVERED_EXACT_BINDERS',[1,2],'All six source hypotheses unchanged, passed to actual producers.'),
2:('COVERED_LITERAL_RETAINED_CONTRACT',[1,2],'All11 definitions/initialized live stopped recursion and halfopen physical semantics retained.'),
3:('COVERED_INTERNAL_ACTUAL_PARENT',[2,3],'Actual82 Z/actual P probability supplied internally. No supplied arbitrary process.'),
4:('COVERED_INTERNAL_PARENT',[2,6],'Actual73 joint flow continuity and Phi0=id consumed exactly.'),
5:('COVERED_INTERNAL_PARENT_AND_NEW_LIMIT',[2,7],'Actual77 hazard continuity/zero, actual82 defect bound inherits firstwait survival; q_t->0 proved.'),
6:('COVERED_INHERITED_FIRSTARC',[2],'Actual82 full BODY freshly checked actual initial firstarc and finite/top firstwait split; no83 duplication needed.'),
7:('COVERED_INTERNAL_ACTUAL82',[2,4,5],'Measurable actual D and real-probability bound consumed to obtain integrated test estimate.'),
8:('COVERED_CB_TEST_ELABORATION',[2,3,4,6],'Continuous real f and every globalM>=0 bound; literal source C_c subset.'),
9:('COVERED_NEW_INTEGRATION',[3,4,5],'Actual measurable/integrable test and constant indicator; integral_sub has genuine integrability.'),
10:('COVERED_NEW_INTEGRATION',[4,5],'Allraw pointwise2M indicator bound, integration/normalization and actual defect bound.'),
11:('COVERED_TEST_FLOW_LIMIT',[6],'Continuous f composed with actual freeflow, Phi0=id.'),
12:('COVERED_NEW_EXPECTATION_LIMIT',[7,8],'Quantitative bound tends0, abs/signed difference and testflow limit yield actual expectationlimit.'),
13:('OPTIONAL_OR_NOT_USED',[],'Bounded epsilon/delta convergence-in-probability route remains a valid sufficient alternative, not invoked or claimed separately compiled.'),
14:('SOURCE_CC_SPECIALIZATION_AVAILABLE',[3,8],'C_c finite-dimensional tests bounded continuous, hence pointwise source ingredient obtained. No separate C_c declaration/outerL2 credit.'),
15:('EXCLUDED_OPEN',[],'Outer phase squared DCT needs own measurable normalizednu and domination, not done here.'),
16:('EXCLUDED_OPEN',[],'Invariance/Jensen contraction and dense L2 representative extension not done here.'),
17:('EXCLUDED_OPEN',[],'Global process/kernel/path/restart/Markov/invariance/hypocoercivity/cost/main/composition remain separate.')}
nodes=[]
for n in g['nodes']:
 status,steps,finding=node_map[int(n['id'][-2:])];nodes.append({'id':n['id'],'source_ids':n['source_ids'],'frozen_obligation':n['obligation'],'status':status,'steps':steps,'finding':finding,'blocking':False})
items=[]
for i,a in enumerate(inv['items'],1):
 if i==1:status='PROVENANCE_ONLY';steps=[];finding='Pinned nonexclusive arXivv1, minimal private source paraphrases only.'
 elif i in [2,3,4]:status='COVERED_EXACT_BINDERS';steps=[1,2];finding='Exact six original analytic dynamics conditions, no higher derivative/moment assumptions.'
 elif i in [5,6,7,8,9,10,11,12,13,14]:status='COVERED_LITERAL_DEFINITIONS_AND_INHERITED_ACTUAL';steps=[1,2];finding='Literal dynamics/indexing/finite-time/top/zero/reflection/halfopen source semantics preserved by exact82 contract and actual calls.'
 elif i==15:status='INHERITED_NONACCUMULATION_MARKOV_OPEN';steps=[2];finding='Existing fixedparams AEallfinite/init preserved. Source direct Exp mean1SLLN distinguished from UnitExp bounded-indicatorSLLN sufficient alternative; memoryless Markov continuation OPEN.'
 elif i==16:status='COVERED_BOREL_AND_EXCEPTION_ADAPTER';steps=[2,3];finding='Actual jointZ fixedtime composition yields real test measurability; source failed-limit0 vs uncoveredz0 explicit.'
 elif i in [17,18,19,27,28]:status='COVERED_SOURCE_POINTWISE_INGREDIENT_AND_ASTIS_INTEGRATION';steps=[3,4,5,6,7,8];finding='Actual integration closes pointwise bounded continuous test consumer beyond82, with exact2M; C_c source class distinguished from C_b extension.'
 elif i==29:status='OPTIONAL_OR_ROUTE_NOT_USED';steps=[];finding='Epsilon/delta bounded probability route is alternative only. No AS shortcut, not required AND with implemented route.'
 else:status='EXCLUDED_OPEN';steps=[];finding='Outer DCT/Jensen/invariance/density/L2/global process/path-law/idealreference/composition remain explicitOPEN, not proved or public premises.'
 items.append({'id':a['id'],'source_id':a['source_id'],'source_graph_nodes':a['source_graph_nodes'],'frozen_classification':a['classification'],'status':status,'steps':steps,'finding':finding,'blocking':False})
edges=[]
for e in g['edges']:
 i=int(e['id'][-2:]);status,steps,finding=node_map[int(e['consumer'][-2:])]
 if i in [21,22,23,24,29,30]:status='OPTIONAL_OR_BRANCH_NOT_USED';steps=[];finding='AND ingredients inside optional G13 branch, complete branch OR preferred G12 branch; not additional required premise.'
 if i==28:status='EXCLUDED_BOUNDARY_ASSOCIATION';steps=[];finding='dependency_edge=false: no L2 to global Markov/restart/invariance/cost inference.'
 edges.append({'id':e['id'],'ingredient':e['ingredient'],'consumer':e['consumer'],'frozen_status':e['status'],'dependency_edge':e.get('dependency_edge',True),'status':status,'steps':steps,'finding':finding,'blocking':False})
coverage={'inventory_expected':30,'inventory_reviewed':30,'inventory_items':items,'nodes_expected':17,'nodes_reviewed':17,'nodes':nodes,
 'relations_expected':30,'relations_reviewed':30,'relations':edges,'edges_expected':30,'edges_reviewed':30,'edges':edges,
 'dependency_rows':29,'excluded_boundary_associations':1,'unmapped_inventory_items':[],'unmapped_nodes':[],'unmapped_relations':[],
 'original_frozen_source_bytes_unchanged':True,'effective_graph_matches_exact_separately_reviewed_overlay':True,
 'topology':'All in-scope actual ingredients consumed internally or derived; optional complete branch remains OR and unused; outer/global obligations excludedOPEN.'}
dependencies=[
 {'declaration':unit['astis_dependencies'][0],'path':parent82.as_posix(),'consumed_at':[132,134],'audit':'Entire exact actual82 module freshly read. hshort measurability/defect/tail plus jointZ/covered/fallback/commonfixedparamsAEallfinite/init consumed with all six binders, every clause returned. Actual82 firstwait input law and noeventfirstarc implementation rechecked.'},
 {'declaration':unit['astis_dependencies'][1],'path':(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean').as_posix(),'consumed_at':[135,138],'audit':'Exact private Prop/typing and consumed primitive BODY read: .1 joint hazard continuity, .2.2.2.1 basiczero. Primitive obtains actual flow/rate continuity and parametric interval primitive, no new certificate.'},
 {'declaration':unit['astis_dependencies'][2],'path':(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean').as_posix(),'consumed_at':[139,141],'audit':'Exact private Prop/typing and continuity/Phi0 BODY read; .1 continuity and .2.2.1 identity correct, eta signs/scales match.'},
 {'declaration':unit['astis_dependencies'][3],'path':(R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean').as_posix(),'consumed_at':[142,144],'audit':'Exact product definition/privateProp/probability producer BODY read; .1 is genuine IsProbabilityMeasure actualP, internally factorExp1 probability and infinitePi instance. No arbitrary probability assumption.'}]
independence={'reviewer':'/root/fresh_source78','formalizer':x['roles']['formalizer'],'decoder':x['roles']['blind_decoder'],'independent_from_formalizer':True,'independent_from_decoder':True,
 'authored_source_extraction_not_proof':True,'authored_exact_overlay':False,'distinct_overlay_proposer':'/root/exact_verify77','original_graph_selfapproval_claimed':False,
 'source_inventory_created_utc':inv['created_utc'],'source_first_graph_frozen_before_any83header':True,'primary_and_frozen_graph_rechecked_before_final_packet_or_BODY':True,
 'preseal_raw_reuse':preseal,'prior_review_reasoning_not_used_as_fidelity_evidence':True,'no_other_math_source_review_verdict_or_root_adoption_summary_read':True,
 'blind_reconstruction_read_only_after_independent_source_freeze':True,'owned_outputs_only':True,'no_production_shared_or_state_writes':True,'no_self_VERIFIED_or_stabilization':True}
truthboundary={'accepted':'Bounded actual fixedstate real-test measurability/integrability, explicit2M phase-flow expectation estimate and zero-time clock expectation limit, all82 actual contracts retained.',
 'source_direct':['A1.E1/E2 initialized iid Exp1 stopped recursion','A1.Ex1-3 actual dynamics','A1.SS1.p2.2 halfopen live interpolation','A1.Ex22 firstevent control','A1.SS1.SSS0.Px1.p6.1-p6.2 pointwise C_c consumer'],
 'ASTIS_elaborations':['Intrinsic finite-dimensional Borel/rank0 carriers','Source exceptional version vs actual uncoveredz0 totalization','Bounded continuous real C_b extension of source C_c','Explicit quantitative2M integrated-defect estimate','Nonpunctured NNReal0 expectation limit'],
 'open':['Outer-state L2 dominated convergence','Invariance/Jensen contraction/density/representative operator extension','Markov/restart/strongMarkov/semigroup/ChapmanKolmogorov/filtration','Full path regularity/AS convergence/Feller C0 preservation/moments','Arbitrary correlated random-parameter law or uniformparameter event/limit','Ideal H_y invariance/reference producer and actualinputcomposition','Implementation/errors/caps/querycost/hypocoercivity/main/fourpaperGoal','Reader visual/PURIFIED/live completion'],
 'special_cases':{'zero_threshold':'Every rawclamp sample retained; only fixedparams AEinit claimed. At0 q0=0 and Phi0=id give actual expectation0=f(z0).',
 'infinite_wait':'Last live arc remains covered at every finite time; stopped auxiliary record carries no phase. New test integral uses retained actualZ, not stopped fallback.',
 'rank0':'Allowed singleton phase; no positivityofdimension assumption.',
 'M':'Every admissible realM>=0;M0 valid. Globalabsbound gives actual finiteprob integrability, not an unbounded-cost expectation result.',
 'parameters':'Fixed deterministic tuple/test/bound, oneZ; no uniformparameter AE or arbitrary correlated substitution.',
 'probability':'ActualP probability internally produced; real measure/integral_const normalization finite, no toReal(infinity)=0 trick.',
 'DCT':'No samplewise AS convergence inferred from probability convergence; implemented route uses integration on actual measurable defect. Outer-stateDCT remainsOPEN.'}}
paths=[P,PACKET,MODULE,LESSON,RUN/'header83.proposed.lean',GP,R/'lean-toolchain',R/'lake-manifest.json']
for name in manifest_names:
 m=load(B/name);paths+=[Path(a['path'])for a in m['raw_inputs']+m['raw_outputs']];paths.append(B/name)
paths +=[Path(a['path'])for a in dependencies]
paths +=[R/p for p in ['.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntegrableOn.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Set.lean','.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/theorem-publication-protocol.md']]
inputs=[raw(p)for p in dict.fromkeys(paths)];now=datetime.now(timezone.utc).isoformat()
evidence=save('source-review.run-evidence83.json',{'schema':'independent-source-review-run-evidence-v1','created_utc':now,'status':'closed','reviewer_packet_sha256':CANON,'reviewer_packet_raw_sha256':sha(PACKET),
 'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,'raw_inputs':inputs,'independence':independence,'authored_step_coverage':authored,'source_counts':[30,17,30],
 'dependency_audit':dependencies,'publication_configuration_hashes':'Packet toolchain/dependency hashes match LF-normalized content; native raw_inputs separately bind exact CRLF file bytes. Module/packet/native outputs use exact RAW hashes.',
 'compiler_limit':'Packet compiled=true and supplied pinned toolchain recorded; no compiler rerun/commit verification or state transition claimed. Source comparison rests on source, exact actual statement/BODY and semantic dependency APIs.',
 'noncircular_rule':'Evidence omits own/result/manifest hashes; result binds this exact RAW. Final manifest lists exact native inputs/outputs and omits own selfhash.'})
result=save('source-review.result83.json',{'schema_version':1,'reviewer':'/root/fresh_source78','verdict':'equivalent-after-elaboration',
 'verdict_reason':'Exact source/independently frozen topology, fresh blind reconstruction, unchanged private Prop, full BODY and eight contiguous adjacent formula/prose/Lean regions faithfully realize the bounded actual pointwise clock-expectation ingredient. Six source analytic binders/11literaldefs/all82clauses preserved; actual test integrability and quantitative2M estimate/limit produced internally. C_b and2M explicitly ASTIS elaborations of source C_c ingredient. No blocking delta or required mathematical/exposition repair; full outerL2/global consumers remainOPEN.',
 'semantic_slots':slots,'deltas':deltas,'repairs':[],'blocking_deltas':[],'no_required_mathematical_repairs':True,'no_required_exposition_repairs':True,
 'reviewer_packet_sha256':CANON,'reviewer_packet_raw_sha256':sha(PACKET),'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,'review_run_sha256':sha(evidence),'review_run_path':evidence.as_posix(),
 'independent_from_formalizer':True,'independent_from_decoder':True,'independence':independence,'authored_step_coverage':authored,'source_graph_coverage':coverage,'actual_dependency_audit':dependencies,'truthboundary':truthboundary,
 'blind_binding':{k:x['blind_reconstruction'][k]for k in ['text_sha256','decoder_packet_sha256','decoder_run_sha256','source_text_visible']},
 'native_publication_lesson':raw(LESSON),'whole_Prop_header_unchanged':True,'no_shared_or_state_mutation':True,'scope':'Independent source/fullBODY/exposition review only, not proving-worker selfverification or full paper/source theorem completion.'})
outputs=[Path(__file__).resolve(),evidence,result]
manifest=save('source-review.run-manifest83.json',{'schema':'independent-source-review-noncircular-raw-manifest-v1','created_utc':now,'status':'closed','reviewer':'/root/fresh_source78',
 'reviewer_packet_sha256':CANON,'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,'raw_inputs':inputs,'raw_outputs':[raw(p)for p in outputs],
 'source_first_chronology':{'inventory_created_utc':inv['created_utc'],'preseal_manifests':preseal,'source_graph_preheader_and_unchanged':True,'final_primary_graph_recheck_preceded_packet_BODY':True},
 'self_hash_omitted':True,'binding_DAG':'Exact inputs -> evidence -> result -> manifest; manifest selfhash omitted and externally reported.'})
for a in load(manifest)['raw_inputs']+load(manifest)['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
assert load(result)['review_run_sha256']==sha(evidence)
print(json.dumps({'status':'closed','verdict':load(result)['verdict'],'coverage':[30,17,30,8],'inputs':len(inputs),'outputs':[raw(p)for p in [result,evidence,manifest]]},indent=2))
