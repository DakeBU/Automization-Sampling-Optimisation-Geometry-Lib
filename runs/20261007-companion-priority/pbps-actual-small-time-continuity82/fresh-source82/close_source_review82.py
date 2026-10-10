"""Close independent source review82; native artifacts only, no shared state."""
import hashlib,json,pathlib
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82'
OWN=RUN/'fresh-source82'
PRE=ROOT/'runs/20261007-companion-priority/pbps-process-regularity-preread82'
PACKET=RUN/'source-review82.packet.json'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'
LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-small-time-continuity.json'
CANON='5f27cc1b3ab2a6e6563f983e8f111e79151629a1c77b1c3ee701489e22966388'
MODSHA='f2bbb2a495ff6af2f2d1d73f77c498ccf16406bb0b07d20b8437631afb1a7bde'
PUBSHA='996913629e7bce2e7fb674454986bb49386ac51b3eb9a0f2856b265aa3bff8b7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf8'))
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def write(n,d):
 p=OWN/n;assert not p.exists(),n;p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
mf=load(PRE/'source_freeze82.raw-manifest.json')
assert sha(PRE/'source_freeze82.raw-manifest.json')=='45253a0383bebeffe048730edfd738b4578f281d1a6b764e95abb2388253d3c1'
for x in mf['raw_inputs']+mf['raw_outputs']:assert sha(pathlib.Path(x['path']))==x['raw_sha256']
assert sha(PRE/'header-source-review82/topology-title-ack82.json')=='659df5971d73662f2f9bcf34dda64edef3ad8ba0e5b839c5f285527a4dafd0af'
assert sha(PRE/'header-source-review82/topology-title-ack82.raw-manifest.json')=='27e8096af588b09cc1b3267e490cd00f0f90cd9b4ca73711fb7151d09e8c9a24'
inventory=load(PRE/'source_inventory82.json');graph=load(PRE/'source_proof_graph82.json')
assert (len(inventory['items']),len(graph['nodes']),len(graph['edges']))==(36,13,20)
readiness=load(OWN/'source-review82.prepacket-readiness.json')
assert readiness['canonical_packet_seen'] is False and readiness['candidate_full_body_seen'] is False
p=load(PACKET);q={k:v for k,v in p.items()if k!='packet_sha256'}
assert hashlib.sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==CANON
assert p['packet_sha256']==CANON and p['publication_binding_sha256']==PUBSHA
assert sha(PACKET)=='9469ebf2f4ccb36fa729b21a276678dd3f3fc1f4a083760531f22155e32c0ec8'
assert sha(MODULE)==MODSHA
assert MODULE.read_bytes()==p['candidate_publication_context']['current_lean_module'].encode('utf8')
blind=p['blind_reconstruction']['text']
assert hashlib.sha256(blind.encode()).hexdigest()==p['blind_reconstruction']['text_sha256']
unit=load(LESSON)['units'][0];pl=p['candidate_publication_context']['lesson']
assert {k:v for k,v in unit.items()if k!='boundary'}==pl
doc=load(RUN/'documentation-successor82.json')
before=doc['exact_replacement']['before'];after=doc['exact_replacement']['after']
mb=MODULE.read_bytes();assert mb.count(after.encode())==1
old=mb.replace(after.encode(),before.encode(),1)
assert hashlib.sha256(old).hexdigest()=='a5d0303f2f426e0029ddec2fbd56ba8f95670ce533e560d18e473c6111ef74d0'
assert len(old.splitlines())==len(mb.splitlines())
overlay=load(OWN/'proposed-exposition-overlay82.json')
assert unit['steps'][3]['formula']==overlay['overlay'][0]['new_value']
assert doc['exposition_overlay']['after']==unit['steps'][3]['formula']
header=RUN/'header82.proposed.lean'
assert sha(header)=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'

findings=[
 'Literal P/epsilon/c/Phi/S/rate/Lambda/tau/next/record/eventTime retained. Record0 is live(0,z0); finite/top guards and source coordinate0=E1 exact.',
 'Internally obtains actual80 Z and all source contracts; actual77 hazard continuity/basic0/measurable wait/survival, actual73 flow continuity/Phi0 and actualExp coordinate law/probability are genuine produced dependencies. No new certificates.',
 'Joint Z measurability pulls back at fixed y,r,z0,t; complement of equality with constant Phi_tz0 gives measurable defect on every raw sequence.',
 'Measurable w=tau(epsilon0), actual coordinate0 marginal Exp1 and map-map identify its law. map_measureReal_apply plus actual77 W survival gives exactly P[t<w]=exp(-Lambda_t), including w=top. Final displayed formula now survival only.',
 'Unfold initialized eventTime1 for finite wait and top to get eventTime1=w. Deterministic n0 covered characterization gives Z_t=Phi_tz0 whenever t<w, for all raw sequences. Correct halfopen endpoint and last live infinite-wait branch.',
 'Defect subset complement of strict survival; P probability ensures finite real measures. Measurable complement identity yields1-exp(-Lambda_t). Only inclusion, so ineffective bounce or later return causes no equality error.',
 'For each real delta>0, norm of measurable actual phase difference yields measurable closed norm-tail; no moment or integrability premise.',
 'Actual joint flow/hazard continuity restrict to NNReal finite time. Phi0=id yields deterministic distance->0 and eventually<delta. Lambda0=0 plus exp continuity yields upper bound->0 on nonpunctured nhds0. Optional cap route not used.',
 'Eventually norm-tail subset phase-flow defect because deterministic distance<delta. Probability nonnegativity and prior upper bound squeeze to0. Includes t0 correctly; full Markov/L2/invariance or alltime path continuity not inferred.'
]
lines=mb.splitlines(keepends=True);regions=[];seen=set();overlaps=[]
for i,s in enumerate(unit['steps'],1):
 r=s['lean_source_region'];a,b=r['start_line'],r['end_line'];code=b''.join(lines[a-1:b])
 assert r['source_raw_sha256']==MODSHA and sha(MODULE)==MODSHA
 assert code.decode()==s['lean'] and hashlib.sha256(code).hexdigest()==r['exact_code_raw_sha256']
 for n in range(a,b+1):
  if n in seen:overlaps.append(n)
  seen.add(n)
 regions.append({'step':i,'title':s['title'],'start_line':a,'end_line':b,'exact_code_raw_sha256':r['exact_code_raw_sha256'],
  'formula_reviewed':True,'prose_reviewed':True,'body_reviewed':True,'formula_body_exact_match':True,'finding':findings[i-1]})
gaps=sorted(set(range(106,261))-seen)
assert len(regions)==9 and not gaps and not overlaps
authored={'expected_steps':9,'reviewed_steps':9,'body_start_line':106,'body_end_line':260,'gaps':gaps,'overlaps':overlaps,
 'formula_body_exact_matches':9,'steps':regions,'entire_module_private_prop_and_theorem_BODY_read':True,
 'native_packet_lesson_equal_except_boundary':True,'native_boundary_separately_audited':True}

slots={
 'objects':{'original':'Actual harmonic Phi and source reflection/rate, integrated hazard/wait, initialized stopped recurrence, iid Exp1 input and physical phase. Ex22 gives first-event probability.',
  'reconstructed':'Blind reconstructs all literal definitions, single total Z, actual canonical P, phase-flow defect D_t and norm-tail A_delta,t; not an arbitrary supplied process or kernel.',
  'evidence':'Private Prop and BODY106-153 construct/consume exact actual objects. BODY162-203 identifies actual firstwait through real coordinate0 and literal first record, then covered firstarc. Source A1.E1/E2/A1.SS1.p2.2 and Ex22 match; defect event differs from firstevent event but is a subset.',
  'relation':'explicit-elaboration'},
 'domains':{'original':'Finite-dimensional Euclidean phase, finite nonnegative physical time, infinite wait for empty hit; source smalltime right approach.',
  'reconstructed':'Blind explicitly identifies finite-dimensional real Borel E including rank0, product phase norm, NNReal finite times and WithTop waits, real sequences clamped to nonnegative thresholds.',
  'evidence':'Literal domains and max product norm provide equivalent finite-dimensional phase topology; no quantitative phase-distance rate claimed. Finite t never evaluated at top. Header/body use same carriers; source A1.Ex2/A1.E1 and standing context preserved.',
  'relation':'explicit-elaboration'},
 'quantifiers':{'original':'Fixed V/alpha/beta/eta,y,r,z0; independent actual clocks, pointwise smalltime source flow/firstevent argument.',
  'reconstructed':'Blind accurately reconstructs exists one joint Z, allraw covered/fallback clauses, each-fixedparams common AE allfinite/init, every finite t defect bound, every real delta>0 nonpunctured NNReal nhds0 tail limit; no uniformparams event or limit.',
  'evidence':'BODY140-153 returns retained Z clauses verbatim, then intro y xRef z0. BODY218-260 fixes arbitrary positive delta and proves the NNReal limit. hsmall uses strict deterministic distance<delta; hbound at0 and Lambda0=0 force defect mass0, consistent with retained AEinit. No correlated random-parameter substitution occurs.',
  'relation':'explicit-elaboration'},
 'assumptions':{'original':'V C2,0<alpha<=beta, Hessian sandwich and0<eta<=1/beta.',
  'reconstructed':'Blind enumerates exactly hα,hαβ,hV,hH,hη,hβη and no trajectory/selection/regularity premise.',
  'evidence':'Private Prop and theorem bind all six original hypotheses; beta>0 follows alpha>0<=beta, so beta eta<=1 is source scale. BODY retrieves produced P probability, actual wait law/continuity/Z; no cap/nonexplosion/Markov/invariance certificate is assumed.',
  'relation':'equivalent'},
 'conclusion':{'original':'Source Ex22 and p6.1-p6.2 supply firstevent probability tending0 and flow convergence as ingredients of later fullL2 strong continuity.',
  'reconstructed':'Blind gives measurable D_t with P.real(D_t)<=1-exp(-Lambda(initialstate,t)), and measurable norm-tails tending0 for every positive real delta, while retaining every Z property. It explicitly does not equate defect and event count or infer AS/moment continuity.',
  'evidence':'Actual hsurvival162-184, hfirst/hnoevent185-203, hbound204-217 and final measurable-tail/continuity/squeeze218-260 realize the independently frozen G82-04/07/08/09/10 graph. Meaningful actual-input coupling bound beyond a supplied kernel or mere continuity premise.',
  'relation':'explicit-elaboration'},
 'scopes':{'original':'Selected smalltime source ingredient precedes completed fullL2 consumer; invariance/Jensen/density/contractivity and phase Markov/semigroup remain separate source obligations.',
  'reconstructed':'Blind confines conclusions to exact phase realization, fixedparams defect bounds and zero-time convergence in probability; no global uniform limit/common nullset, arbitrary random law, AS continuity or moment convergence.',
  'evidence':'Native publication explicitly keeps fullL2/Markov/restart/semigroup/invariance/hypocoercivity/cost/main/composition OPEN. Optional E82-14 cap route unused; G82-11/12/13 consumers excluded. ASTIS uncovered z0 versus source failed-limit zero totalization retained. Actual82 never invokes ideal H81 to infer Markovness.',
  'relation':'explicit-elaboration'},
 'constant_dependencies':{'original':'c=y-eta gradV(r), sqrt eta harmonic/rate factors and inverse sqrt eta, Exp rate1, source E_(n+1), exact firsthazard exponent and smalltime0.',
  'reconstructed':'Blind records exact signs/scales/index0, original-state freeflow hazard and no hidden rescaling/free constant. Product phase norm and real delta threshold explicit.',
  'evidence':'All literal definitions BODY106-139 match source A1.Ex1-3 and E1/E2; RHS exact1-exp(-Lambda_t), no eta-scaled time or new constant. No Ct bound or source cost rate claimed.',
  'relation':'equivalent'}
}
assert set(slots)==set(p['review_contract']['semantic_slots'])
for s in slots.values():assert s['relation']in p['review_contract']['slot_relations']
deltas=[]
def delta(slot,classification,desc):
 deltas.append({'id':'D82-%02d'%(len(deltas)+1),'slot':slot,'classification':classification,'blocking':False,'description':desc})
delta('objects','notation-resolution','Exp product coordinate0 realizes source E1; measurable clamp has actual Exp input law. Source initial record is live, not stopped; G82-05 title ACK removes wording ambiguity without topology change.')
delta('domains','domain-clarification','Intrinsic finite-dimensional Borel carrier/rank0 and literal product norm preserve phase topology. NNReal finite time is distinct from extended wait.')
delta('quantifiers','quantifier-clarification','Nonpunctured NNReal nhds0 extends source t-downarrow0 legitimately. Positive-delta tail at0 has probability0, derivable from hbound0 plus Phi0=id and retained AE initialization. No uniformparameter or arbitrary correlated input claim.')
delta('assumptions','notation-resolution','Six exact source binders retained; actual probability/measurability/firstwait/phase facts are produced dependencies, not public source premises.')
delta('conclusion','source-implicit','Source firstevent survival gives actual phase-flow defect upper bound via firstarc agreement. This is a strict bounded prerequisite, not a fullL2 theorem or event-equality claim.')
delta('scopes','admissible-bounded-refinement','E82-14 optional cap Ct OR route is unused; E82-13 Lambda continuity suffices. Bounded-test expectation/G82-11, fullL2/G82-12 and global/path/restart/G82-13 remain OPEN.')
delta('scopes','formalization-convention','Zero thresholds exceptional under actual Exp input; firstwaittop keeps last live arc, stopped dummy no phase, uncovered z0 distinct from source failed-limit zero. Deterministic noevent agreement holds every raw sequence on its first live interval.')
delta('constant_dependencies','notation-resolution','All eta/Exp1/clockindex/hazard signs retained; no quantitative norm-distance constant, Ct or time rescaling added.')
delta('scopes','exposition-topology-correction-adopted','Independent step4 formula overlay adopted exactly: survival only at step4, firstarc agreement step5, defect bound step6. Nine formula/BODY regions now agree in dependency order; no mathematical change.')
delta('scopes','documentation-only-successor','One module docstring line corrected; exact reverse replacement regenerates predecessor RAW a5d0303..., proving all statement/BODY bytes and line count unchanged. Final module RAW f2bbb2a4... bound.')

# Map every independently frozen item to exact new proof, inherited actual contract, or OPEN exclusion.
def item_mapping(i):
 if i==1:return 'PROVENANCE_ONLY',[],'Pinned arXiv nonexclusive provenance; private paraphrases/minimal formulas only.'
 if i in [2,3,4]:return 'COVERED_EXACT_BINDERS',[1,2],'All six source analytic hypotheses retained and passed to actual parents; no higher derivative bound.'
 if i==5:return 'PARTIAL_FIXEDPHASE_REST_OPEN',[2,3,4,5,6,7,8,9],'Actual phase construction and smalltime prerequisite only; full source uniqueness/Markov/stationarity remain OPEN.'
 if i in [6,7,8,9]:return 'COVERED_LITERAL_PARENT',[1,2,4,5,8],'Literal fixed y,r center/flow/rate/reflection and produced actual73/77 APIs match source scales.'
 if i==10:return 'COVERED_BOUNDARY',[1,5],'No bounce continuity premise; total division reflection0=id. Firstarc proof avoids discontinuous bounce entirely.'
 if i==11:return 'COVERED_ACTUAL_INPUT',[1,2,4,5],'Actual infinitePi probability and coordinate0 marginal Exp1, index0 initial live record, source E1 first threshold.'
 if i==12:return 'COVERED_ACTUAL_FIRSTWAIT',[1,2,4,5,6],'Actual77 measurable inverse hazard W survival transported through coordinate0; top empty-hit branch explicitly handled.'
 if i==13:return 'COVERED_RECURSION_GUARDS',[1,5],'Literal finite postbounce update and absorbing stopped alternative; unfold eventTime1 without any infinity phase.'
 if i==14:return 'COVERED_FIRSTARC_AND_RETAINED_ALLFINITE',[2,5,6],'hcovered with n0 gives allraw nofirstevent phase identity; retained hAE covers allfinite source arcs, including final live infinite wait.'
 if 15<=i<=19:return 'INHERITED_NONACCUMULATION_NOT_NEW_PROOF',[2],'Energy/layer/rate controls underpin actual80 allfinite contract; no supplied cap/energy premise. Actual82 local limit consumes continuity, not quantitative layer bounds.'
 if i in [20,21]:return 'OPTIONAL_OR_ROUTE_NOT_USED',[],'Source C and Lambda<=Ct are optional quantitative sufficient alternative E82-14; actual BODY uses Lambda continuity/zero E82-13, no Ct output.'
 if i==22:return 'BOUNDARY_PRESERVED_NO_CAP_DIVISION',[4,5,6,8],'Zero cap entails infinite positive-threshold wait; top firstwait handled, and local argument never divides by cap.'
 if i in [23,24,25]:return 'INHERITED_NONACCUMULATION_PARTIAL_REST_OPEN',[2],'Actual80 retains common fixedparams AEallfinite/init. Source direct Exp mean1SLLN is distinct from inherited UnitExp indicator-SLLN sufficient alternative. Markov/Davis/restart remains OPEN.'
 if i in [26,27,28,29,30,31]:return 'EXCLUDED_OPEN',[],'Source full transition operator/adjoint/invariance/semigroup/generator exponentiation/path expansion not proved or assumed by current smalltime edge.'
 if i==32:return 'COVERED_SMALLTIME_INGREDIENT_REST_OPEN',[4,5,6,8,9],'Source deterministic flow and firstevent smalltime control realized for actual phase; invariance/Jensen/bounded-test/L2 continuation excluded.'
 if i==33:return 'COVERED_EXACT_SURVIVAL_AND_ASTIS_DEFECT',[4,5,6,8,9],'Exact Ex22 firstevent survival law consumed, actual defect subset proved, exponential limit and stochastic continuity derived.'
 if i==34:return 'CONSUMER_OPEN_SMALLTIME_INGREDIENT_ONLY',[8,9],'Provides pointwise actual stochastic continuity prerequisite; full bounded-test DCT/L2 density/contractivity not claimed.'
 if i==35:return 'COVERED_INHERITED_BOREL_AND_EXCEPTION_ADAPTER',[2,3,4,5,7],'Joint measurable actual Z and waits consumed; source failed-limit zero versus chosen uncovered z0 explicit. Measurable defects/tails proved without hidden certificates.'
 if i==36:return 'EXCLUDED_PRIOR_IDEAL_KERNEL_BOUNDARY',[],'Source q_y/Gaussian/reference integration belongs81, not duplicated or used to imply phase Markovness.'
 raise AssertionError(i)
items=[]
for i,it in enumerate(inventory['items'],1):
 status,steps,finding=item_mapping(i)
 items.append({'id':it['id'],'source_id':it['source_id'],'frozen_scope':it['scope'],'source_graph_nodes':it['source_graph_nodes'],
               'status':status,'steps':steps,'finding':finding,'blocking':False})
nm={
1:('COVERED',[1,2],'Exact six original standing binders; fixed V,alpha,beta,eta.'),
2:('COVERED_PARENT',[1,2,8],'Actual73 harmonic continuity/Phi0, finite NNReal time coercion.'),
3:('COVERED_PARENT',[1,2,4,8],'Actual77 nonnegative continuous hazard, Lambda0=0 and measurable actual wait.'),
4:('COVERED_ACTUAL_INPUT_INTEGRATION',[2,4],'ActualExp0 marginal plus map-map and actual77 survival law gives real product survival includingtop.'),
5:('COVERED_WITH_TITLE_ACK',[1,5],'Initialized live first record with stopped alternative; exact eventTime1=tau by finite/top cases.'),
6:('COVERED_RETAINED_PARENT',[2,3,5,7],'One actual80 jointly Borel Z, allraw covered/fallback and fixedparams common AEallfinite/init retained.'),
7:('COVERED',[5],'n0 firstarc hcovered yields Z_t=Phi_tz0 whenever t<firstwait.'),
8:('COVERED',[3,4,5,6],'Measurable defect, event inclusion, real-probability complement and exact upper bound.'),
9:('COVERED_CONTINUITY_ROUTE_CAP_OPTIONAL_NOT_USED',[8],'Lambda continuity/zero gives exponential upper-bound limit. Optional Ct edge excluded OR route.'),
10:('COVERED',[7,8,9],'Positive-delta measurable tails squeeze to0 on nonpunctured NNReal nhds0, fixedparams only.'),
11:('EXCLUDED_OPEN',[],'Bounded continuous observable expectation limit is a downstream possible consumer, not current named result.'),
12:('EXCLUDED_OPEN',[],'No L2 invariant contractive semigroup from probability convergence; source preceding invariance/Jensen/density remain separate.'),
13:('EXCLUDED_OPEN',[],'No alltime cadlag/rightcontinuity, conditional restart/Markov/path-density or cost/main/composition credit.')}
nodes=[]
for n in graph['nodes']:
 i=int(n['id'][-2:]);status,steps,finding=nm[i]
 nodes.append({'id':n['id'],'frozen_obligation':n['obligation'],'source_ids':n['source_ids'],'status':status,'steps':steps,'finding':finding,'blocking':False})
edges=[]
for e in graph['edges']:
 i=int(e['consumer'][-2:]);status,steps,finding=nm[i]
 if e['id']=='E82-14':status='OPTIONAL_OR_ALTERNATIVE_NOT_USED';steps=[];finding='Quantitative cap Ct optional sufficient route, never required AND with Lambda continuity E82-13. No cap binder/output.'
 if i>=11:status='EXCLUDED_OPEN_FUTURE_SUBSTRATE_NOT_IMPLICATION'
 edges.append({'id':e['id'],'ingredient':e['ingredient'],'consumer':e['consumer'],'frozen_reason':e['reason'],
               'status':status,'steps':steps,'finding':finding,'blocking':False})
coverage={'inventory_expected':36,'inventory_reviewed':36,'inventory_items':items,
 'nodes_expected':13,'nodes_reviewed':13,'nodes':nodes,'edges_expected':20,'edges_reviewed':20,'edges':edges,
 'unmapped_inventory_items':[],'unmapped_nodes':[],'unmapped_edges':[],
 'original_frozen_topology_bytes_unchanged':True,'title_only_ack':raw(PRE/'header-source-review82/topology-title-ack82.json'),
 'refinements':['G82-05 title clarified live first record with stopped alternative','G82-09 cap Ct optional OR not used; continuity route used','G82-11/12/13 consumers OPEN'],
 'topology_verdict':'Exhaustive scoped ingredient coverage via exact actual parents/new BODY or explicit OPEN/optional alternative. No excluded global theorem counted as proved.'}
independence={'reviewer':'/root/fresh_source78','role':'independent anti-anchored source reviewer82','proving_worker':False,
 'source_first':True,'source_only_freeze_created_utc':inventory['created_utc'],'source_pins_verified_before_fullBODY':True,
 'prepacket_readiness':raw(OWN/'source-review82.prepacket-readiness.json'),'source_inventory_counts':[36,13,20],
 'own_source_graph_frozen_before_candidate':True,'original_frozen_bytes_unchanged':True,
 'candidate_BODY_first_read':'Original a5d0303... after own source freeze recheck; final canonical doc-only successor separately checked.',
 'blind_reconstruction_visible_only_after_source_freeze_and_canonical_packet':True,
 'not_read':['Other reviewers mathematical/source fidelity verdicts','root adoption reports','other source extractor decisions'],
 'notice_received':'Root reported a docstring-only cleanup observation; no mathematical/source verdict or reasoning was supplied by that notice and none used as evidence.',
 'owned_outputs_only':True,'no_production_or_shared_mutation':True,'no_proof_or_VERIFIED_state_transition':True}
docaudit={'module_docstring':{'before_raw_sha256':'a5d0303f2f426e0029ddec2fbd56ba8f95670ce533e560d18e473c6111ef74d0','after_raw_sha256':MODSHA,
 'exact_reverse_replacement_verified':True,'statement_BODY_bytes_identical':True,'line_count_unchanged':True},
 'step4_formula':{'independent_overlay':raw(OWN/'proposed-exposition-overlay82.json'),'exact_overlay_applied':True,
 'final_value':unit['steps'][3]['formula'],'firstarc_step':5,'defect_bound_step':6,'mathematical_change':False},
 'final_publication_binding_sha256':PUBSHA,'two_documentation_edits_acknowledged':True}
truthboundary={'accepted':'Actual fixed-reference phase-flow defect probability and zero-time stochastic continuity, with full actual80 Z semantics retained.',
 'source_direct':['A1.E1/E2 actual initialized threshold recurrence','A1.SS1.p2.2 halfopen flow interpolation','A1.Ex22 firstevent probability','A1.SS1.SSS0.Px1.p6.1-p6.2 genuine downstream smalltime consumer'],
 'astis_elaborations':['Actual canonical product first-coordinate wait-law transport','Measurable defect event and inclusion instead of movement-event equality','Positive real threshold tails using product phase norm','NNReal nonpunctured0 limit through actual probability bound/init','Intrinsic Borel/rank0 and explicit stopped/fallback conventions'],
 'open':['FullL2 strong continuity/contraction/semigroup','Phase Markov/restart/strongMarkov/ChapmanKolmogorov/filtration','Invariance/reversibility/adjoint/hypocoercivity','Full alltime cadlag/rightcontinuity and moment convergence','Arbitrary correlated/random initialization and uniformparams events/limits','Universal version uniqueness/path density','Ideal H81 reversal/invariance/augmented composition','Implemented reference/cap/errors/query cost/main/fourpaperGoal','Reader visual/main/PURIFIED/live completion'],
 'special_cases':{'zero_threshold':'Raw zero waits allowed, actual Exp positivity AE; nofalse allraw initialization. Bound at0 is0 and forces real defect probability0.',
 'firstwait_top':'True initial live arc continues at every finite time, no stopped dummy or fallback substitution.',
 'last_live_top':'Retained actual80 allfinite semantics preserve later infinite-wait arcs; new firstevent argument needs initial arc only.',
 'delta':'Every real delta>0, closed norm-tail; delta0 excluded as necessary since tail mass1 there.',
 'filter':'Nonpunctured NNReal nhds0; includes0 consistently. No two-sided negative physical time or fullsemigroup continuity.',
 'finite_probability':'P IsProbabilityMeasure internally from actual Exp product; real-measure monotonicity/complement cannot exploit toReal(infinity)=0.',
 'rank0':'Allowed point phase, zero rate/infinite firstwait gives defect0.',
 'optional_cap':'Cap Ct is unused optional sufficient alternative; no divide by cap or newpremise.'}}

input_paths=[pathlib.Path(x['path'])for x in mf['raw_inputs']+mf['raw_outputs']]
input_paths +=[PRE/'source_freeze82.raw-manifest.json',PRE/'header-source-review82/topology-title-ack82.json',PRE/'header-source-review82/topology-title-ack82.raw-manifest.json',header,
 PACKET,MODULE,LESSON,RUN/'documentation-successor82.json',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
input_paths +=[ROOT/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{n}.lean' for n in ['ActualHarmonicFlow','ActualHazardClock','ActualFiniteJumpRecursion','ActualPhysicalTimeCover','ActualPhysicalTimeMeasurability']]
input_paths +=[ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean']
inputs=[raw(x)for x in dict.fromkeys(input_paths)]
now=datetime.now(timezone.utc).isoformat()
evidence=write('source-review.run-evidence82.json',{'schema':'independent-source-review-run-evidence-v1','created_utc':now,'status':'closed',
 'reviewer_packet_sha256':CANON,'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,
 'raw_inputs':inputs,'independence':independence,'authored_step_coverage':authored,'source_counts':[36,13,20],
 'documentation_successor_audit':docaudit,'compiler_limit':'Exact BODY/type/source reviewed. Root supplied EXIT0 receipt; no independent compiler execution or verification credit claimed by this review.',
 'noncircular_rule':'Evidence omits own/result/final-manifest hashes; result binds this exact RAW. Manifest binds native files and omits only its own digest.'})
result=write('source-review.result82.json',{'schema_version':1,'reviewer':'/root/fresh_source78','verdict':'equivalent-after-elaboration',
 'verdict_reason':'Final exact module and nine complete adjacent formula/prose/BODY regions faithfully realize the bounded actual firstevent/smalltime source prerequisite. No required mathematical repair or blocking source delta; independent formula-order correction adopted and exact doc-only successor verified. Full global consumers remain OPEN.',
 'reviewer_packet_sha256':CANON,'reviewer_packet_raw_sha256':sha(PACKET),'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,
 'review_run_sha256':sha(evidence),'review_run_path':evidence.as_posix(),'semantic_slots':slots,'deltas':deltas,
 'blocking_deltas':[],'repairs':[],'no_required_mathematical_repairs':True,'no_unresolved_exposition_repairs':True,
 'authored_step_coverage':authored,'source_graph_coverage':coverage,'independence':independence,'truthboundary':truthboundary,
 'documentation_successor_audit':docaudit,'native_publication_lesson':raw(LESSON),
 'blind_binding':{'text_sha256':p['blind_reconstruction']['text_sha256'],'decoder_packet_sha256':p['blind_reconstruction']['decoder_packet_sha256'],'decoder_run_sha256':p['blind_reconstruction']['decoder_run_sha256']},
 'scope':'Independent source and exposition/BODY fidelity only; no proving-worker selfverification, compiler rerun, state transition or full source theorem completion.'})
outputs=[OWN/'source-review82.prepacket-readiness.json',OWN/'proposed-exposition-overlay82.json',pathlib.Path(__file__).resolve(),evidence,result]
out=write('source-review.run-manifest82.json',{'schema':'independent-source-review-noncircular-raw-manifest-v1','created_utc':now,'status':'closed','reviewer':'/root/fresh_source78',
 'reviewer_packet_sha256':CANON,'publication_binding_sha256':PUBSHA,'full_module_sha256':MODSHA,'raw_inputs':inputs,'raw_outputs':[raw(x)for x in outputs],
 'source_first_chronology':{'source_inventory_created_utc':inventory['created_utc'],'prepacket_readiness_created_utc':readiness['created_utc'],'original_freeze_unchanged':True,'original_source_manifest':raw(PRE/'source_freeze82.raw-manifest.json')},
 'self_hash_omitted':True,'noncircular_rule':'All native inputs/outputs RAW bound; only this manifest selfhash omitted and reported externally.'})
for x in load(out)['raw_inputs']+load(out)['raw_outputs']:assert sha(pathlib.Path(x['path']))==x['raw_sha256']
assert load(result)['review_run_sha256']==sha(evidence)
print(json.dumps({'status':'closed','verdict':load(result)['verdict'],'coverage':[36,13,20,9],'outputs':[raw(x)for x in [result,evidence,out]],'input_count':len(inputs),'output_count':len(outputs)},indent=2))
