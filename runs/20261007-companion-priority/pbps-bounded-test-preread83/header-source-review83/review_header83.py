"""Primary-first prospective exact-header scope review; no proof/state credit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,copy
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-bounded-test-preread83'
O=B/'header-source-review83';C=R/'runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83'
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
H=C/'header83.proposed.lean';META=C/'prospective-statement83.json'
A=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf8'))
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def save(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
assert sha(P)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(H)=='1bf2b24f0ba521449aba10ac3559a27c4db7f2eab0df89c98587f623695b07ff'
assert sha(B/'source_freeze83.closed-raw-manifest.json')=='6f0e838a8c3ada6dec3d3e842be55252885f0ba49f861256309963d5e8b6201d'
frozen=load(B/'source_freeze83.closed-raw-manifest.json')
for a in frozen['raw_inputs']+frozen['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
inv=load(B/'source_inventory83.json');orig=load(B/'source_proof_graph83.json');sup=load(B/'optional-route-topology-supplement83.json')
overlaypath=B/'independent-topology83/proposed-minimal-topology-overlay83.json';overlay=load(overlaypath)
assert sha(overlaypath)=='6a8870abda762b76523c2bc9fef7dac87cef1b7dd64c1c034865745abbb702a6'
effectivepath=B/'source_proof_graph83.reviewed-effective.json';g=load(effectivepath)
expected=copy.deepcopy(orig['edges']+sup['added_edges']);byid={e['id']:e for e in expected}
for eid,p in zip(['E83-29','E83-30','E83-28'],overlay['patches']):
 if eid!='E83-28':assert byid[eid]['status']==p['before'];byid[eid]['status']=p['after']
 else:assert byid[eid]==p['before'];byid[eid].clear();byid[eid].update(p['after'])
assert g['nodes']==orig['nodes'] and g['edges']==expected and g['reviewed_junctions']==overlay['junctions']
assert (len(inv['items']),len(g['nodes']),len(g['edges']))==(30,17,30)
assert sum(e.get('dependency_edge',True)for e in g['edges'])==29
hs=H.read_text('utf8');lines=hs.splitlines();oldlines=A.read_text('utf8').splitlines()
# Entire old private-Prop contract, omitting only its name, is exact prefix of new Prop.
oldblock='\n'.join(oldlines[15:90]);hstart=hs.index('    {E : Type*}')
assert hs[hstart:].startswith(oldblock)
assert re.findall(r'    let (\S+)',hs)==['P','ε','c','Φ','S','rate','Λ','τ','next','record','eventTime']
assert hs.count('∃ Z :')==1 and hs.index('∃ Z :')<hs.index('∀ f :')
assert '∀ M : ℝ, 0 ≤ M → (∀ z : E × E, |f z| ≤ M) →'in hs
assert '2 * M * (1 - Real.exp (-Λ y xRef z₀ t))'in hs
assert 'Tendsto (fun t : ℝ≥0 => ∫ sample, f (Z y xRef z₀ t sample) ∂P)'in hs
assert 'theorem 'not in '\n'.join(l for l in lines if not l.startswith('/-!')) # no83 theorem BODY
def lineof(s):return next(i+1 for i,l in enumerate(lines)if s in l)
loc={'analytic_binders_start':lineof('(hα :'),'literal_definitions_start':lineof('let P :'),
 'exists_actual_Z':lineof('∃ Z :'),'new_test_quantifier':lineof('∀ f :'),
 'test_bound_quantifier':lineof('∀ M :'),'test_measurability':lineof('Measurable (fun sample'),
 'test_integrability':lineof('Integrable (fun sample'),'quantitative_estimate':lineof('2 * M *'),
 'expectation_limit':lineof('Tendsto (fun t : ℝ≥0 => ∫ sample')}
slots={
 'objects':{'original':'Literal actual harmonic phase, iid Exp1 recurrence and physical realization; source C_c test expectation as pointwise ingredient.',
 'reconstructed':'One existential actual Z with all actual82 clauses, then every continuous bounded real f and actual integral over literal P.',
 'evidence':'All11 definitions and old private-Prop contract exact prefix preserved; integral uses f(Z...) under same P, not a user-supplied kernel/process.', 'relation':'explicit-elaboration'},
 'domains':{'original':'Finite-dimensional Euclidean phase, finite nonnegative time, possibly infinite waits; source compactly supported continuous phase tests.',
 'reconstructed':'Intrinsic finite-dimensional real Borel E, product phase including rank0, NNReal time and WithTop waits, real bounded continuous tests.',
 'evidence':'FiniteDimensional/Borel/InnerProduct carriers unchanged. C_b is explicit ASTIS extension of C_c, not a faithful source quotation or C0/Feller claim.','relation':'explicit-elaboration'},
 'quantifiers':{'original':'Fixed deterministic y,r,z0; source pointwise operator ingredient before outer initial-state integration.',
 'reconstructed':'Exists one joint Z before all deterministic y,r,z0,f,M. For each continuous f, every M>=0 satisfying global bound, every finite t measurable/integrable/estimate, then nonpunctured NNReal0 expectation limit.',
 'evidence':'Universal M formulation is equivalent to choosing a nonnegative bound for each bounded test; no bound existence assumed for unbounded f. Fixedparams AE allfinite/init inherited, no uniformparams AE or arbitrary correlated random-state substitution.','relation':'explicit-elaboration'},
 'assumptions':{'original':'Six original conditions: alpha positive, alpha<=beta, V C2, Hessian sandwich everywhere, eta positive, eta<=1/beta.',
 'reconstructed':'Exact hα,hαβ,hV,hH,hη,hβη retained. Continuous f and M>=0 global abs bound define test class; no supplied trajectory/probability/expectation certificate.',
 'evidence':'Exact prefix comparison verifies all six and11 definitions. Alpha positivity/order gives beta>0, beta eta<=1 equivalent scale. Probability/integrability/defect bound must be produced internally by actual parents.','relation':'equivalent'},
 'conclusion':{'original':'Source Ex22 first-event control and flow continuity supply pointwise bounded C_c expectation convergence needed in p6.2.',
 'reconstructed':'All actual82 outputs retained, plus measurable/integrable f(Z_t), abs(E f(Z_t)-f(Phi_tz0))<=2M[1-exp(-Lambda_t)] for every finite t, and E f(Z_t)->f(z0).',
 'evidence':'Bounded discrepancy<=2M on measurable phase-flow defect, zero outside, explains quantitative output without equating defect with jump event. Exact limit filter is ordinary NNReal nhds0. This is a genuine integration consumer, not restatement of82 as public premise.','relation':'explicit-elaboration'},
 'scopes':{'original':'Pointwise C_c expectation is prerequisite of outer-state L2 DCT; invariance/Jensen/density/contraction and process laws remain distinct.',
 'reconstructed':'Prospective metadata explicitly keeps unbounded tests, AS paths, outer L2/Markov/restart/semigroup/invariance/hypocoercivity/main/cost/composition OPEN.',
 'evidence':'No such output appears in Prop. Effective E28 dependency_edge=false; optional epsilon/delta route remains OR with preferred branch. Header-only review cannot certify future actual82 consumption or proof.','relation':'explicit-elaboration'},
 'constant_dependencies':{'original':'Exact eta/sqrteta/inverse sqrteta scales, clock rate1/index E_(n+1), initial-state integrated hazard and source first-event probability.',
 'reconstructed':'Definitions unchanged, q_t=1-exp(-Lambda(initialstate,t)), precise2M factor from absolute test difference; no extra rate/cap/dimension constant.',
 'evidence':'No time rescaling or quantitative phase norm estimate. M0 gives zero test. Test/integral real codomain and actual probability finiteness required later for bounded integration.','relation':'explicit-elaboration'}}
item_coverage=[]
for i,a in enumerate(inv['items'],1):
 if i==1:status='PROVENANCE_ONLY';reason='Source pin/license retained, no bulk copying.'
 elif i in [2,3,4]:status='EXACT_HEADER_BINDERS';reason='Six original dynamics conditions exact retained prefix.'
 elif i in [5,6,7,8,9,10,11,12,13,14]:status='EXACT_HEADER_DEFINITIONS_OR_RETAINED_BOUNDARY';reason='Literal11 definitions, initialized live record and all82 covered/fallback/AE clauses exact retained.'
 elif i==15:status='INHERITED_NONACCUMULATION_MARKOV_OPEN';reason='Retained fixedparams AEallfinite/init, underlying source SLLN alternative explicit; memoryless Markov continuation not claimed.'
 elif i==16:status='RETAINED_MEASURABLE_ADAPTER';reason='Joint actual Z Borel and exceptional uncovered z0 convention retained; source failed-limit zero remains separate convention.'
 elif i in [17,18,19,27,28]:status='NEW_OUTPUT_OR_REQUIRED_FUTURE_BODY_INGREDIENT';reason='Source firstevent/flow pointwise consumer maps to new measurable/integrable actual expectation estimate/limit; proof not yet present.'
 elif i==29:status='OPTIONAL_OR_FUTURE_ROUTE';reason='Actual82 tail/local continuity bounded split is valid optional alternative, no AS-DCT inference and not mandatory AND with preferred route.'
 else:status='EXCLUDED_OPEN';reason='Outer-state DCT/Jensen/invariance/density/global process/path-law/ideal reference consumers remain OPEN; not source completion.'
 item_coverage.append({'id':a['id'],'source_id':a['source_id'],'source_graph_nodes':a['source_graph_nodes'],'status':status,'reason':reason,'blocking':False})
node_coverage=[]
for n in g['nodes']:
 i=int(n['id'][-2:])
 if i==1:status='EXACT_BINDERS'
 elif i==2:status='EXACT_LITERAL_DEFINITIONS'
 elif i in [3,6,7]:status='RETAINED_ACTUAL82_OUTPUT'
 elif i in [4,5,11]:status='REQUIRED_FUTURE_INTERNAL_PARENT_INGREDIENT'
 elif i in [9,10,12]:status='NEW_HEADER_OUTPUT_NOT_YET_PROVED'
 elif i==8:status='TEST_CLASS_CB_ASTIS_EXTENSION'
 elif i==13:status='OPTIONAL_OR_FUTURE_ROUTE'
 elif i==14:status='SOURCE_CC_SPECIALIZATION_CONSUMER'
 else:status='EXCLUDED_OPEN'
 node_coverage.append({'id':n['id'],'status':status,'obligation':n['obligation'],'blocking':False})
edge_coverage=[]
for e in g['edges']:
 eid=int(e['id'][-2:])
 if eid==28:status='EXCLUDED_BOUNDARY_ASSOCIATION_NOT_DEPENDENCY'
 elif eid in [26,27]:status='EXCLUDED_OPEN_FUTURE_CONSUMER'
 elif eid in [21,22,23,24,29,30]:status='OPTIONAL_ROUTE_AND_WITHIN_OR_BETWEEN_BRANCHES'
 elif eid<=10:status='RETAINED_ACTUAL82_ANCESTRY_FUTURE_INTERNAL_CONSUMPTION'
 else:status='FUTURE_BOUNDED_TEST_PROOF_INGREDIENT'
 edge_coverage.append({'id':e['id'],'ingredient':e['ingredient'],'consumer':e['consumer'],'status':status,'dependency_edge':e.get('dependency_edge',True),'blocking':False})
coverage={'inventory_expected':30,'inventory_reviewed':30,'inventory':item_coverage,'nodes_expected':17,'nodes_reviewed':17,'nodes':node_coverage,
 'relations_expected':30,'relations_reviewed':30,'relations':edge_coverage,'dependency_rows':29,'boundary_associations':1,'unmapped_inventory':[],'unmapped_nodes':[],'unmapped_relations':[],
 'complete_scope_review_only_not_BODY_coverage':True}
independence={'reviewer':'/root/fresh_source78','source_extraction_author':True,'original_graph_selfapproval_claimed':False,
 'distinct_overlay_proposer':'/root/exact_verify77','exact_overlay_scope':'Only reviewed distinct exact patches in previous owned overlay review; here applied-effective graph checked mechanically against those patches, not prior verdict reasoning.',
 'primary_first_this_turn':True,'original_frozen_bytes_unchanged':True,'no83BODY_implementation_seen':True,'no_other_source_or_math_reviewer_verdict_read':True,
 'reviewed_actual82':'Only exact private-Prop contract lines16-90 freshly read for retained-prefix comparison. No83 proof exists in reviewed header.',
 'source_only_owned_outputs':True,'no_shared_state_or_statement_seal_or_proof_credit':True}
boundaries={'rank0':'Allowed finite-dimensional singleton phase; no positive-dimension premise.',
 'zero_threshold':'Raw clamped0 thresholds allowed; allraw covered/fallback retained, initialization only each-fixedparams AE. No new allraw Z0 claim.',
 'infinite_wait':'Infinity stops next record but last live phase arc covers every finite remaining time. NNReal elapsed used only live stored finite time.',
 'null_versions':'Source failed-limit0 vs chosen uncoveredz0 convention retained. Integrals ignore fixedparams null exception; no single global-parameter nullset or arbitrary correlated initialization.',
 'time0':'Ordinary nonpunctured NNReal nhds0 includes0; retained AEinit gives integral f(Z0)=f(z0), compatible with quantitative bound q0=0.',
 'bounded_real_test':'Global abs bound with M>=0 yields genuine actual integrability and2M control. Unbounded continuous tests require extra uniform integrability/moments and are excluded.',
 'no_AS_DCT':'Optional probability route uses epsilon/delta bounded expectation estimate, not inference of AS convergence. Outer initial-phase L2 DCT remains OPEN.',
 'full_operator_laws':'No Feller C0 preservation, uniform state/time consequence, Markov/restart/semigroup/invariance/L2 contraction/density or cost/composition result.'}
inputs=[P,H,META,A,B/'source_inventory83.json',B/'source_proof_graph83.json',B/'optional-route-topology-supplement83.json',B/'source_freeze83.closed-raw-manifest.json',overlaypath,effectivepath]
now=datetime.now(timezone.utc).isoformat()
evidence=save('header-source-review83.run-evidence.json',{'schema':'prospective-source-header-review-run-evidence-v1','created_utc':now,'status':'closed','raw_inputs':[raw(p)for p in inputs],
 'header_raw_sha256':sha(H),'effective_graph_raw_sha256':sha(effectivepath),'checks':{'original_freeze_RAWs_unchanged':True,'effective_graph_exact_reviewed_patches_only':True,'all82_contract_exact_prefix':True,'literal_definitions_count':11,'six_analytic_binders_unchanged':True,'one_Z_before_all_tests':True,'M_nonnegative_universal_globalbound':True,'no83theorem_BODY':True},
 'statement_regions':loc,'independence':independence,'noncircular_rule':'Evidence has no self/result/manifest digest; decision binds exact evidence RAW; manifest binds all inputs/native outputs and omits selfhash.'})
decision=save('header-source-review83.decision.json',{'schema':'independent-prospective-source-header-review-v1','created_utc':now,'status':'closed','reviewer':'/root/fresh_source78',
 'verdict':'SOURCE_COMPATIBLE_BOUNDED_ASTIS_ELABORATION_HEADER_ONLY','header':raw(H),'prospective_metadata':raw(META),'effective_source_graph':raw(effectivepath),'review_run_sha256':sha(evidence),
 'verdict_reason':'Exact whole-Prop preserves six source binders,11 literal definitions and every actual82 clause, and adds an honest actual bounded-real-test expectation integration consumer. Explicit C_b extension of literal C_c pointwise source ingredient, precise nonnegative bound and2M estimate; no arbitrary process/certificate premise or full L2/global claim. No necessary mathematical/header repair found; future BODY must internally consume actual82 and prove new integrals/estimate/limit.',
 'semantic_slots':slots,'source_graph_coverage':coverage,'statement_regions':loc,'boundaries':boundaries,'independence':independence,
 'future_BODY_requirements':['Internally obtain actual P probability and same actual82 Z witness, retaining every clause; no public extra premise.',
 'Derive actual f(Z_t) measurable/integrable via fixed-time joint Z and continuous bounded f, with finite P.',
 'Derive abs expectation defect via bounded2M discrepancy on measurable defect event and actual82 probability bound; do not identify defect with all jump events.',
 'Use actual flow/hazard continuity and test continuity for nonpunctured0 expectation limit, or optional complete epsilon/delta route; AND inside branch, OR between sufficient branches.',
 'Keep outer L2 DCT, invariance/Jensen contraction/density and process/kernel/global/cost/composition conclusions OPEN.'],
 'blocking_deltas':[],'required_mathematical_repairs':[],'proposed_header_overlays':[],'no_required_header_repairs':True,
 'credit_boundary':'Prospective SOURCE HEADER scope review only; no Lean typecheck/BODY proof, blind decoder, final source fidelity/VERIFIED or83completion claim. Originalgraph not self-approved.',
 'StatementSeal':False,'proof_reviewed':False,'VERIFIED':False})
manifest=save('header-source-review83.closed-raw-manifest.json',{'schema':'acyclic-closed-raw-review-manifest-v1','created_utc':now,'status':'closed','raw_inputs':[raw(p)for p in inputs],
 'raw_outputs':[raw(Path(__file__).resolve()),raw(evidence),raw(decision)],'self_hash_omitted':True,'binding_DAG':'Raw inputs -> evidence -> decision -> manifest; manifest selfhash omitted.',
 'original_frozen_source_bytes_unchanged':True,'header_only_no_shared_state':True})
for a in load(manifest)['raw_inputs']+load(manifest)['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
assert load(decision)['review_run_sha256']==sha(evidence)
assert len({a['id']for a in item_coverage})==30 and len({a['id']for a in node_coverage})==17 and len({a['id']for a in edge_coverage})==30
print(json.dumps({'status':'closed','verdict':load(decision)['verdict'],'coverage':[30,17,30],'outputs':[raw(p)for p in [decision,evidence,manifest]]},indent=2))
