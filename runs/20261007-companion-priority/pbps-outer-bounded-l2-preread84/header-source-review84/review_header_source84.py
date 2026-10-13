"""Source-facing whole-header prospective review; never reads84 proof or other verdicts."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime
ROOT=Path('E:/Samplinglib');BASE='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/'
HEADER='runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84/header84.proposed.lean'
PRIMARY='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=(ROOT/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'bytes':len(b)}
assert pin(PRIMARY)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class H(HTMLParser):
 def __init__(self):super().__init__();self.st=[];self.m=0;self.o={}
 def handle_starttag(self,t,a):
  d=dict(a)
  if t not in {'br','hr','meta','link','img','input','source','wbr','area','base','col','embed','param','track'}:self.st.append((t,d.get('id')))
  if t=='math':
   self.m+=1
   if self.m==1:
    for _,i in self.st:
     if i:self.o.setdefault(i,[]).append(d.get('alttext',''))
 def handle_endtag(self,t):
  if t=='math':self.m-=1
  for k in range(len(self.st)-1,-1,-1):
   if self.st[k][0]==t:self.st=self.st[:k];break
 def handle_data(self,s):
  if not self.m:
   for _,i in self.st:
    if i:self.o.setdefault(i,[]).append(s)
 def normalized(self,i):return ' '.join(' '.join(self.o[i]).split())
h=H();h.feed((ROOT/PRIMARY).read_text(encoding='utf-8'))
frozen={'source_inventory84.json':'c9e17b30fd27cc9c2b30f4707d9e63c11404a6642bd6348a4bd1c5605cec6265',
 'source_proof_graph84.json':'d05d7fd9b77f49acd939d31fa858585552956a6793dc4c3e0ab3063d944fafcb',
 'bounded_candidate84.json':'64d2a26607af9e6e426ca5d0830b592404dca4c516cbac0869bc6c656f3e9e0f',
 'source_freeze84.seal.json':'80f8c14962a0bc21b7969341e415acc1ee8663220552d799c6f373b732eb8883',
 'source_freeze84.raw-manifest.json':'b5ebfdb08166f55881ee2eadc4b9faf7844e97608b79abb5a07116b095e47c1b',
 'overlay-review84/topology-overlay.decision84.json':'eafcb63f0d819023fa1f68d303e997e936c7d6939f9576c6e0ec98bf57cb9035',
 'overlay-review84/topology-overlay.run-evidence84.json':'150a06b4cdcc117187af1303db4c7875b25d63ae62aa108cfb68532074dad60a',
 'overlay-review84/topology-overlay.run-manifest84.json':'5548e80396c8a3a9285a09075e34a4dd7300ed1acbeb21c03575a84e957933f5',
 'source_inventory84.reviewed-effective.json':'5ac25472d2e3b78944ee1d52093d945230c5f3163ffc253a57713f2e0f02ff09',
 'source_proof_graph84.reviewed-effective.json':'65306373dad98344a7cab842ceeb0105125efa69bfcdab09a2bd9b5b10f3e213'}
for p,v in frozen.items():assert pin(BASE+p)['raw_sha256']==v,p
inventory=json.loads((ROOT/(BASE+'source_inventory84.reviewed-effective.json')).read_bytes())
g=json.loads((ROOT/(BASE+'source_proof_graph84.reviewed-effective.json')).read_bytes())
for a in inventory['source_anchor_coverage']:
 assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
assert len(inventory['items'])==47 and len(g['nodes'])==23 and len(g['edges'])==39
assert pin(HEADER)['raw_sha256']=='936b76036df8d283acb212f2f1ba780c4446aa2e1c7dc84bfdff0ff9c02f29b0'
assert pin(HEADER)['bytes']==7652
text=(ROOT/HEADER).read_text(encoding='utf-8');lines=text.splitlines()
assert len(lines)==128 and lines[110]=='set_option maxHeartbeats 1600000 in'
parent='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean'
assert pin(parent)['raw_sha256']=='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
pt=(ROOT/parent).read_text(encoding='utf-8')
prefix=pt[pt.index('private def actual_bounded_test_expectation_continuity_statement'):pt.index('\n\n\nset_option maxHeartbeats')]
target_prefix=prefix.replace('actual_bounded_test_expectation_continuity_statement','actual_outer_bounded_l2_continuity_statement',1)
assert text[text.index('private def '):].startswith(target_prefix)
assert lines[112].strip().startswith('(let q') and 'IsProbabilityMeasure (q y)' in lines[115]
assert 'IsProbabilityMeasure (ν y)' in lines[115]
assert '(𝓝 0) (𝓝 0)' in lines[124]

regions=[('H84-01',20,28,'All six analytic binders and finite-dimensional Borel phase domain'),
 ('H84-02',29,61,'All eleven literal actual clock/recurrence/flow/rate definitions'),
 ('H84-03',62,64,'One jointly measurable actual phase witness Z'),
 ('H84-04',65,70,'All-sample half-open live-arc equality'),
 ('H84-05',71,74,'All-sample uncovered-arc z0 fallback'),
 ('H84-06',75,82,'For each fixed y/reference/z0 common AE all finite times and initialization'),
 ('H84-07',83,90,'Actual measurable first-event defect estimate'),
 ('H84-08',91,95,'All positive delta norm-tail measurability and nonpunctured zero-time limit'),
 ('H84-09',96,108,'Actual83 inner bounded-test measurability/integrability/2M defect and every-state expectation limit'),
 ('H84-10',109,112,'Prospective connective and the stray standalone command blocker at111'),
 ('H84-11',113,116,'Exact conditional Gibbs q, unscaled standard Gaussian phase product, both probability outputs'),
 ('H84-12',117,123,'Fixed-parameter bounded-test state expectation measurability, squared integrability and4M2 domination'),
 ('H84-13',124,125,'Actual phase-law outer squared integral tends0 at ordinary NNReal nhds0')]
header_regions=[{'region_id':x,'start_line':a,'end_line':b,'assessment':s,
 'line_code_utf8_lf_sha256':sha(('\n'.join(lines[a-1:b])+'\n').encode())} for x,a,b,s in regions]
assert set(range(20,126))==set(n for _,a,b,_ in regions for n in range(a,b+1))

# Exhaustive source-item mapping; internal ingredients need not be extra public premises.
imap={
 1:('SOURCE_CONTEXT',[8],'Source identity in header; license retained in pinned source freeze, not a theorem binder.'),
 2:('RETAINED_DOMAIN_AND_QUANTIFIERS',[21,22,23,75,117],'Finite real E including rank0, deterministic fixed y/reference; no randomized-parameter AE switch.'),
 3:('EXACT_BINDER',[24],'h_alpha strictly positive genuine curvature.'),
 4:('EXACT_BINDER',[24],'h_alpha_beta ordering retained.'),
 5:('EXACT_BINDER',[24],'ContDiff R2 V retained.'),
 6:('EXACT_BINDER',[25,26,27],'Universal x,v and both Hessian inequalities retained.'),
 7:('EXACT_BINDER',[28],'eta strictly positive retained.'),
 8:('EXACT_BINDER',[28],'beta eta<=1 retained; no scale strengthening.'),
 9:('EXACT_INLINE_DEFINITION',[114],'V_y quadratic potential appears inside exact q tilt; no additional supplied potential.'),
 10:('EXACT_DEFINITION_AND_OUTPUT',[113,114,116],'q_y exact volume tilt, normalization output, no arbitrary q or q-hat.'),
 11:('EXACT_DEFINITION_AND_OUTPUT',[115,116],'nu_y actual q_y x standard Gaussian, no reference dependence.'),
 12:('EXACT_RETAINED_DEFINITION',[31,32,33,34,35],'Center and harmonic flow including sqrt eta / inverse sqrt eta match source.'),
 13:('EXACT_RETAINED_DEFINITION',[36,37,38],'Zero reflection normal gives identity via total real division convention.'),
 14:('EXACT_RETAINED_DEFINITION',[39,40,41,42],'Positive-part rate and interval integral Lambda retained.'),
 15:('EXACT_RETAINED_DEFINITION',[29,30,58],'iidExp1 canonical P, toNNReal coordinate and zero-index/source E_(n+1) adapter retained.'),
 16:('EXACT_RETAINED_DEFINITION',[43,44,45,46,47],'Closed threshold Lambda>=e from0 with WithTop empty-hit wait.'),
 17:('EXACT_RETAINED_DEFINITION',[48,49,50,51,52,53,54,55,56,57,58,59,60,61],'Initialized live record, top-stop, stopped absorption, post-wait bounce and top eventTime retained.'),
 18:('EXACT_RETAINED_OUTPUT',[67,68,69,70,77,78,79,80,81],'Half-open live arcs/local NNReal elapsed; top next time preserves final infinite-wait live arc.'),
 19:('INHERITED_ACTUAL_PARENT_OBLIGATION',[75,76,77,78,79,80,81,82],'Nonaccumulation manifests as fixed-parameter AE finite-time coverage; consume actual83 rather than assume generic process.'),
 20:('EXACT_RETAINED_OUTPUT_AND_NEW_CONSUMER',[63,64,121],'Joint actual Z measurability retained and consumed for state expectation.'),
 21:('EXPLICIT_RETAINED_ASTIS_ADAPTER',[71,72,73,74,75,82],'Source failed-limit zero vs ASTIS uncovered-z0 convention disclosed in source freeze; fixed-parameter AE initialization retained.'),
 22:('EXACT_RETAINED_OUTPUT',[86,87,88,89,90],'Measurable actual phase-vs-flow defect bounded by source first-event probability.'),
 23:('EXACT_RETAINED_PARENT_OUTPUT',[98,99,100,101,102,103,104,105,106,107,108],'Every fixed state actual83 expectation producer retained inside same witness, no arbitrary convergence premise.'),
 24:('SOURCE_SPECIALIZATION_BOUNDARY',[12,117,118],'Source C_c compact support implies a finite bound; candidate source consumer explicitly bounded representative subclass.'),
 25:('EXPLICIT_ASTIS_TEST_CLASS_EXTENSION',[12,99,100,117,118],'Real continuous globally bounded tests, arbitrary admissible real M>=0; no extra dynamics premise.'),
 26:('EXACT_NEW_DEFINITION',[119,120],'A_t(z)=actual Z clock expectation under canonical P; no supplied law-family/operator.'),
 27:('NEW_PUBLIC_OUTPUT',[121],'State measurability for each finite t; proof must use joint measurability and finite/SFinite P.'),
 28:('REQUIRED_INTERNAL_NORMALIZATION_INGREDIENT',[24,25,26,28,116],'Base Gibbs integrability/positive mass must be derived internally via existing parents, not assumed; proof absent at prospective stage.'),
 29:('PERMITTED_PREFERRED_INTERNAL_ROUTE',[3,114,116],'Conditional kernel on derived base Gibbs probability + tilted_tilted can prove exact q probability; no claim of BODY consumption yet.'),
 30:('PERMITTED_OPTIONAL_ALTERNATIVE',[114,116],'Direct density domination may replace preferred normalization route; header imposes neither route as extra premise.'),
 31:('EXACT_LAW_AND_REQUIRED_BACKGROUND',[115,116],'Momentum is stdGaussian E, not eta-scaled; existing Gaussian probability gives product normalization.'),
 32:('EXACT_PRODUCT_BOUNDARY',[115,120,125],'Independent phase components; iterated outer-nu and inner-P integrals are product-compatible only, not arbitrary correlated clocks.'),
 33:('EXACT_RETAINED_INTEGRABILITY_OUTPUT',[102,103],'Actual inner integrability retained, prevents integral_undef shortcut.'),
 34:('REQUIRED_INTERNAL_BOUND_INGREDIENT',[100,103,118,123],'P probability and |f|<=M give |A_t f|<=M and discrepancy<=2M; internal proof obligation, no supplied premise.'),
 35:('DERIVABLE_INTERNAL_MEASURABILITY',[117,121,122],'A_t measurable and f continuous make real squared discrepancy measurable; no public ingredient premise needed.'),
 36:('NEW_PUBLIC_BOUND_AND_INTERNAL_DOMINATION',[116,118,123],'Pointwise squared discrepancy<=4M^2, exact nu probability makes constant integrable; no invariance needed.'),
 37:('REQUIRED_INTERNAL_LIMIT_INGREDIENT',[107,108,119,120,124,125],'Actual83 every-state expectation limit yields squared limit; not an almost-sure inference from stochastic convergence.'),
 38:('NEW_PUBLIC_LIMIT_WITH_INTERNAL_DCT',[121,122,123,124,125],'NNReal nhds0 countably generated + measurable dominated discrepancy + pointwise limit -> outer limit.'),
 39:('NEW_PUBLIC_INTEGRABILITY_OUTPUT',[122],'Squared discrepancy integrable for every finite t under exact nu_y.'),
 40:('EXACT_RETAINED_ENDPOINT_AND_NEW_LIMIT',[75,82,94,95,107,108,124,125],'NNReal ordinary nhds0 includes0; initialization AE per state. No punctured-only/negative-time/full positive-time continuity claim.'),
 41:('RETAINED_DEGENERATE_CONVENTIONS',[21,22,30,36,37,38,43,53,58,67,68,75,82,118],'Rank0,M0,zero normal/hazard/raw threshold,infinite wait and stopped dummy preserved; positivity of raw thresholds never imposed for every sample.'),
 42:('EXCLUDED_OPEN',[13,75,117,120,125],'No uniform-parameter AE, correlated random initialization, random y/reference or full initialized all-time path law conclusion.'),
 43:('EXCLUDED_OPEN',[13],'Invariance/Jensen contraction neither supplied premise nor conclusion; not required for bounded finite outer DCT.'),
 44:('EXCLUDED_OPEN',[13,117,119],'Pointwise real tests do not constitute well-defined all-L2 equivalence-class operator.'),
 45:('EXCLUDED_OPEN_WITH_SEPARATE_DENSITY_NODE',[13],'Full density+contraction extension remains OPEN, independent G84-23 density ingredient preserved.'),
 46:('EXCLUDED_OPEN',[13],'No global Markov/restart/semigroup/invariance/main claim inferred from square-integral limit.'),
 47:('EXCLUDED_OPEN',[13],'No ideal-H implementation/approximate sampler/query-cost/main/SPHMC/composition claim.')}
item_coverage=[]
for item in inventory['items']:
 n=int(item['id'].split('-')[-1]);disp,refs,why=imap[n]
 item_coverage.append({'inventory_id':item['id'],'source_ids':item['source_ids'],
  'graph_nodes':item['graph_nodes'],'disposition':disp,'header_lines':refs,'evidence':why})

node_specs={
 1:('EXACT_PUBLIC_BINDERS',[21,22,23,24,25,26,27,28]),2:('EXACT_RETAINED_DEFINITIONS',[29,30,31,32,36,39,41,43,48,56,59]),
 3:('EXACT_RETAINED_OUTPUTS',[62,63,64,65,71,75,82]),4:('EXACT_RETAINED_ACTUAL83_OUTPUTS',[98,99,100,101,102,103,104,107,108]),
 5:('EXACT_TEST_CLASS',[117,118]),6:('REQUIRED_INTERNAL_NO_BODY',[24,25,26,28,116]),
 7:('PERMITTED_NORMALIZATION_ROUTE_NO_BODY',[3,114,116]),8:('OPTIONAL_ALTERNATIVE_NOT_ADDITIONAL_PREMISE',[114,116]),
 9:('NEW_EXACT_NORMALIZATION_OUTPUT',[113,114,116]),10:('EXACT_GAUSSIAN_BACKGROUND',[115]),11:('NEW_EXACT_PRODUCT_PROBABILITY_OUTPUT',[115,116]),
 12:('REQUIRED_INTERNAL_JOINT_TEST_MEASURABILITY',[63,64,117,121]),13:('NEW_MEASURABILITY_OUTPUT',[119,120,121]),
 14:('REQUIRED_INTERNAL_ABS_EXPECTATION_BOUND',[100,103,118,123]),15:('NEW_INTEGRABILITY_BOUND_WITH_DERIVABLE_MEASURABILITY',[121,122,123]),
 16:('REQUIRED_INTERNAL_EVERY_STATE_LIMIT',[107,108,124,125]),17:('NEW_OUTER_LIMIT_OUTPUT',[124,125]),
 18:('SOURCE_CC_SPECIALIZATION_OF_DECLARED_CB',[12,117,118,124,125]),19:('EXCLUDED_OPEN',[13]),20:('EXCLUDED_OPEN',[13]),
 21:('EXCLUDED_OPEN',[13]),22:('EXCLUDED_OPEN',[13]),23:('EXCLUDED_OPEN_SEPARATE_DENSITY',[13])}
node_coverage=[{'node_id':n['id'],'source_node_status':n['status'],'disposition':node_specs[int(n['id'].split('-')[-1])][0],
 'header_lines':node_specs[int(n['id'].split('-')[-1])][1],
 'proof_credit':False} for n in g['nodes']]
edge_coverage=[]
for e in g['edges']:
 n=int(e['id'].split('-')[-1])
 if not e['dependency_edge']:disp='EXCLUDED_BOUNDARY_ASSOCIATION_NO_INFERENCE'
 elif e['status']=='OPEN_NOT_USED':disp='FUTURE_OPEN_NOT_CANDIDATE_REQUIREMENT'
 elif e['route']=='NORMALIZE_DIRECT':disp='OPTIONAL_COMPLETE_NORMALIZATION_ROUTE_NO_BODY'
 elif e['route']=='NORMALIZE_CONDITIONAL':disp='PERMITTED_COMPLETE_NORMALIZATION_ROUTE_NO_BODY'
 else:disp='REQUIRED_PUBLIC_CONTRACT_OR_INTERNAL_INGREDIENT_NO_BODY'
 edge_coverage.append({'edge_id':e['id'],'from':e['from'],'to':e['to'],'dependency_edge':e['dependency_edge'],
  'junction_group':e['junction_group'],'disposition':disp,'ingredient':e['ingredient'],
  'header_target_lines':node_specs[int(e['to'].split('-')[-1])][1],
  'source_fidelity':'Preserved as an obligation/route/boundary; no compilation or BODY coverage claimed.'})
assert len(item_coverage)==47 and len(node_coverage)==23 and len(edge_coverage)==39
assert sum(x['disposition']=='FUTURE_OPEN_NOT_CANDIDATE_REQUIREMENT' for x in edge_coverage)==5

def slot(original,reconstructed,evidence,relation='equivalent-after-elaboration'):
 return {'original':original,'reconstructed':reconstructed,'evidence':evidence,'relation':relation}
slots={
 'objects':slot('Actual initialized Exp1 stopped recurrence and harmonic phase; q_y exact Gibbs quadratic tilt, nu=q_y x N(0,I).',
  'Same eleven literal actual definitions and one Z, exact q and nu definitions, actual clock expectation A.',
  'Header29-61 matches actual83 literal prefix;113-120 exact laws/clock expectation. No arbitrary law/process input.'),
 'domains':slot('R^d x R^d phase, nonnegative physical time, independent exponential clocks; real bounded tests.',
  'Finite-dimensional real inner-product Borel E including rank0, NNReal finite time, real test, M>=0.',
  'Header21-23,29-30,62,99-100,117-120. Rank0 extension and C_b generalization explicit.'),
 'quantifiers':slot('For each fixed deterministic y/reference, initialized phase and actual clock construction; source compact test and zero-time limit.',
  'One joint Z; every y/reference/state; common AE all finite t for each fixed triple; every continuous real f and admissible M; every finite t; outer limit for fixed y/reference.',
  'Header62-82,98-108,116-125. No quantifier exchange to a uniform-parameter null set or arbitrary correlated random state.'),
 'assumptions':slot('0<alpha<=beta, V C2, two-sided Hessian,0<eta<=1/beta; bounded continuity defines test class.',
  'Exactly six analytic binders plus finite-dimensional real Borel structure; f continuous and global |f|<=M,M>=0; no supplied normalizer/invariance/process/convergence.',
  'Header24-28 and117-118. Probability, state measurability, integrability and convergence occur in outputs.'),
 'conclusion':slot('Source p6.2 DCT yields compact-test L2 continuity before separate density/contraction extension.',
  'Retains all83 clauses, adds exact law probabilities, state expectation measurability, outer square integrability,4M^2 bound and squared integral limit0.',
  'Header113-125 expresses a substantive bounded actual-input outer consumer. Source C_c is included in explicit ASTIS C_b extension; no all-L2 quotient/operator theorem.'),
 'scopes':slot('Bounded representative DCT ingredient; source fullL2 extension additionally uses density/contraction and existing Markov operator.',
  'Doc13 excludes all-L2 AE operator/invariance/Jensen/contraction/density/Markov/main/cost. Original exact header has stray standalone command at111 interrupting final conjunction.',
  'All futureOPEN5 dependency rows and2 excluded associations preserved. Mathematical scope is faithful, but original exact header cannot be sealed until separately reviewed syntax-only successor.',
  'scope-faithful-with-syntax-blocker'),
 'constant_dependencies':slot('Exact eta quadratic scale and standard momentum covariance; finite global test bound for DCT.',
  'q uses2eta; momentum stdGaussian unscaled; pointwise2M parent estimate retained; square bound4M^2 independent of time/state for fixed test. No integrated hazard moment needed.',
  'Header34-40,90,106,114-115,118,123. Both normalization routes remain permitted OR, not extra AND assumptions.')}
independence={'reviewer':'/root/fresh_source78','original_source_extraction_author':True,
 'independent_topology_overlay_proposer':False,'proving_owner':False,
 'scope':'Prospective exact source-facing header review only; no BODY/decoder/full-source-verdict/verification credit.',
 'source_first':'Primary parsed/read first; all26 frozen anchors matched before reading header. Unchanged own inventory/graph and distinct-reviewed topology overlay reused.',
 'other_math_or_header_reviewer_verdicts_read':False,
 'root_adoption_as_mathematical_evidence':False,
 'original_graph_self_validation':False,
 'writes':'Owned preread84/header-source-review84 only; originalheader and freeze unchanged.'}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
inputs=[PRIMARY]+[BASE+n for n in frozen]+[HEADER,parent]
evidence={'schema':'astis.prospective-header-source-review84.run-evidence.v1','status':'closed','created_utc':now,
 'raw_inputs':[pin(p) for p in inputs],'primary_anchor_count':26,'all_frozen_primary_anchor_hashes_match':True,
 'exact_header_raw_sha256':pin(HEADER)['raw_sha256'],'exact_header_bytes':7652,
 'whole_private_prop_header_regions':header_regions,
 'literal_actual83_prefix':{'exact_after_private_name_change':True,'source_prefix_lf_sha256':sha(prefix.encode()),
  'header_prefix_lf_sha256':sha(target_prefix.encode()),'all_eleven_definitions_retained':True,'all83clauses_retained':True},
 'source_coverage_counts':{'inventory':47,'nodes':23,'relations':39,'dependency_edges':37,'future_open_dependencies':5,'excluded_associations':2},
 'syntax_blocker':{'line':111,'exact_line':lines[110],'classification':'stray standalone control command; separately reviewed successor required'},
 'independence':independence,
 'noncircularity':'Run evidence does not bind result/manifest. Result binds exact evidence RAW; final manifest binds result and evidence, omitting its own hash.'}
def emit(name,obj):
 p=OUT/name;assert not p.exists(),p;p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
emit('header-source.run-evidence84.json',evidence)
result={'schema':'astis.prospective-whole-header-source-review84.v1','status':'closed','created_utc':now,
 'verdict':'SOURCE_SCOPE_ACCEPT_WITH_SYNTAX_BLOCKER','source_scope_verdict':'FAITHFUL_BOUNDED_ASTIS_ELABORATION',
 'statement_seal_ready_for_exact_original_header':False,
 'verdict_reason':'All mathematical binders, literal actual83 prefix and new exact-law outer bounded-test obligations faithfully refine the source p6.2 DCT ingredient. Exact original header includes a standalone control command at111 before final conjunction, so a distinct-reviewed syntax-only successor is required before StatementSeal. No mathematical/source repair identified.',
 'exact_header_raw_sha256':pin(HEADER)['raw_sha256'],'primary_raw_sha256':pin(PRIMARY)['raw_sha256'],
 'review_run_sha256':sha((OUT/'header-source.run-evidence84.json').read_bytes()),
 'semantic_slots':slots,
 'deltas':[{'id':'H84-SYNTAX-001','slot':'scopes','classification':'SYNTAX_CONTROL_COMMAND','blocking':True,
  'description':'Original header line111 set_option maxHeartbeats1600000 in occurs between inherited Prop and final conjunction. Remove only this line via separately reviewed exact overlay; preserve original bytes and all mathematical tokens. This review does not silently audit a changed header.'},
  {'id':'H84-CLASS-002','slot':'domains','classification':'EXPLICIT_ASTIS_GENERALIZATION','blocking':False,
  'description':'Source C_c Euclidean tests are generalized to real bounded C_b tests on finite-dimensional real inner-product phase space including rank0, with explicit M>=0. Finite actual probability supplies domination; no new dynamics assumption.'},
  {'id':'H84-ADAPTER-003','slot':'objects','classification':'EXPLICIT_INHERITED_EXCEPTIONAL_VERSION_ADAPTER','blocking':False,
  'description':'Source failed-terminal-limit zero convention is inherited as ASTIS uncovered-z0 version; header retains per-fixed-parameter common AE finite-time arc/init semantics. No uniform-parameter or arbitrary correlation substitution.'}],
 'mathematical_repairs':[],'no_required_mathematical_repairs':True,
 'pending_separate_overlay_review':'Only exact one-line syntax correction, if proposed by another agent; this run does not adopt or mutate it.',
 'inventory_coverage':item_coverage,'source_graph_coverage':{'nodes':node_coverage,'relations':edge_coverage,
  'counts':evidence['source_coverage_counts'],'junctions':g['junctions'],'gaps':[],
  'interpretation':'Coverage of prospective obligations/routes/exclusions only, never actual proof coverage.'},
 'whole_header_coverage':{'expected_private_prop_lines':[20,125],'regions':header_regions,'gaps':[],
  'overlaps':[],'syntax_blocker_explicitly_included':True,'body_reviewed':False,'body_exists_claimed':False},
 'truth_boundary':['No invariant law or contraction premise required for this bounded finite-probability DCT.',
  'Exact tilt normalization must be derived internally; probability outputs exclude zero-totalized-tilt closure.',
  'Actual83 and normalization/generic measurability/DCT APIs are required future BODY consumers, not currently certified uses.',
  'All-L2 equivalence-class operator, independent C_c density, contraction/invariance, Markov/restart/semigroup/main/cost/composition remain OPEN.',
  'No AS-DCT shortcut, arbitrary correlated clocks, random y/reference or uniform-parameter AE claim.'],
 'independence':independence,'source_completion_credit':False,'proof_or_verification_credit':False}
emit('header-source.decision84.json',result)
outputs=['review_header_source84.py','header-source.run-evidence84.json','header-source.decision84.json']
manifest={'schema':'astis.prospective-header-source-review84.raw-manifest.v1','status':'closed','created_utc':now,
 'raw_inputs':evidence['raw_inputs'],'raw_outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs],
 'selfhash_convention':'Manifest omits own hash; final RAW reported externally. Acyclic evidence -> result -> manifest.',
 'owned_directory':OUT.relative_to(ROOT).as_posix(),'frozen_originals_and_header_unchanged':True,
 'no_shared_or_state_writes':True,'source_completion_credit':False}
emit('header-source.run-manifest84.json',manifest)
print(json.dumps({'verdict':result['verdict'],'source_scope_verdict':result['source_scope_verdict'],
 'outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs+['header-source.run-manifest84.json']]},indent=2))
