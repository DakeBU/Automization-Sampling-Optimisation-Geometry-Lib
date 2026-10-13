"""Independent source/decoder/full BODY review84. Writes only immutable owned receipts."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,datetime,copy,re
ROOT=Path('E:/Samplinglib');OUT=Path(__file__).resolve().parent
R='runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84/'
S='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/'
PRIMARY='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
MODULE='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean'
LESSON='website/content/declaration_lessons/pbps-actual-outer-bounded-l2-continuity.json'
PUBLICATION='website/content/publications/pbps-actual-outer-bounded-l2-continuity.json'
PACKET=R+'source-review84.packet.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def digest(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def pin(p):
 b=(ROOT/p).read_bytes();return {'path':p,'raw_sha256':sha(b),'bytes':len(b)}
def load(p):return json.loads((ROOT/p).read_bytes())
expected={PRIMARY:'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760',
 S+'source_inventory84.json':'c9e17b30fd27cc9c2b30f4707d9e63c11404a6642bd6348a4bd1c5605cec6265',
 S+'source_proof_graph84.json':'d05d7fd9b77f49acd939d31fa858585552956a6793dc4c3e0ab3063d944fafcb',
 S+'source_inventory84.reviewed-effective.json':'5ac25472d2e3b78944ee1d52093d945230c5f3163ffc253a57713f2e0f02ff09',
 S+'source_proof_graph84.reviewed-effective.json':'65306373dad98344a7cab842ceeb0105125efa69bfcdab09a2bd9b5b10f3e213',
 S+'overlay-review84/topology-overlay.decision84.json':'eafcb63f0d819023fa1f68d303e997e936c7d6939f9576c6e0ec98bf57cb9035',
 S+'overlay-review84/topology-overlay.run-evidence84.json':'150a06b4cdcc117187af1303db4c7875b25d63ae62aa108cfb68532074dad60a',
 S+'overlay-review84/topology-overlay.run-manifest84.json':'5548e80396c8a3a9285a09075e34a4dd7300ed1acbeb21c03575a84e957933f5',
 S+'header-source-review84/header-source.corrected-decision84.json':'0be52a718f4b715256d3f9db018dfae10e2a350b6c2dd6ff20b07ee236597ee9',
 S+'header-source-review84/header-source.corrected-run-evidence84.json':'f82ad9673b5a2bfe8e9b8b6edd8ccfaf65193aa53b90803722c876b1702c5133',
 S+'header-source-review84/header-source.corrected-run-manifest84.json':'3ee5b6f8ac5679fc9adc2ba59c5b79ad26ec0a1ba3cfa606f25f2b580a9845fb',
 R+'header-review84/header84.syntax-only-proposed.lean':'5c4e379caa337d1ac903d509eca30ef7db7b1905715c7a65b878afb33f9d2ded',
 R+'independent-source84/prepacket-preparation84.json':'8ff8b3cb4b5dcf682a6a0d698009ccdbb0ffb1bb31c66591a43f5206f4acd329',
 MODULE:'8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd',
 LESSON:'9a2c0fbb1d3918daec0bc21c00e429b33aab8002ace37ff2a192899fcdf48190',
 PUBLICATION:'d65e7ca24babc0933d74ac6559cc847a16f692fc9ff79d2d7c29fdc033817f45',
 PACKET:'4da1354b990170822021d78471df480a7aab021accadaf0bc0bf303070b646bb'}
# Primary first, then frozen source topology; only then exact implementation and canonical packet.
assert pin(PRIMARY)['raw_sha256']==expected[PRIMARY]
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
inventory=load(S+'source_inventory84.reviewed-effective.json');graph=load(S+'source_proof_graph84.reviewed-effective.json')
for a in inventory['source_anchor_coverage']:
 assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
for p,v in expected.items():assert pin(p)['raw_sha256']==v,p
module=(ROOT/MODULE).read_text(encoding='utf-8');mlines=(ROOT/MODULE).read_bytes().splitlines(keepends=True)
unit=load(LESSON)['units'][0];pub=load(PUBLICATION)['items'][0];packet=load(PACKET)
p0={k:v for k,v in packet.items() if k!='packet_sha256'}
assert digest(p0)==packet['packet_sha256']=='cae491f32e464f9f75e2a5a080b4a68c7439cbbd26fb2bfc1659fc4bf2d6bb76'
assert all(v is False for v in packet['anti_anchoring'].values())
assert packet['blind_reconstruction']['source_text_visible'] is False
for field,key in [('source','original_text'),('lean','statement'),('blind_reconstruction','text')]:
 assert sha(packet[field][key].encode())==packet[field]['statement_sha256' if field=='lean' else 'text_sha256']
context=packet['candidate_publication_context'];assert context['current_lean_module']==module
assert context['lesson']=={k:v for k,v in unit.items() if k!='boundary'}
assert context['statement']==pub['statement']==unit['statement']==unit['lean_statement']
assert context['assumptions']==pub['assumptions']==unit['assumptions']
assert context['formulae']==pub['formulae']
payload={k:v for k,v in context.items() if k!='candidate_assumptions'}
payload['lesson']=unit
payload['binding']={k:v for k,v in pub['bindings'][0].items() if k not in {'audit_id','legacy_audit_debt'}}
assert digest(payload)==packet['publication_binding_sha256']=='9653eee231ec71293839aae14374a183c8ebe01441817e44a08736ec3cd02636'
for path,key in [('lean-toolchain','toolchain'),('lake-manifest.json','dependencies')]:
 assert sha((ROOT/path).read_text(encoding='utf-8').encode())==context[key]
# Exact retained83 prefix and preproof reviewed privateProp are immutable mathematical contract.
oldheader=(ROOT/(R+'header-review84/header84.syntax-only-proposed.lean')).read_text(encoding='utf-8')
start=module.index('private def ');stop=module.index('\n\n\nset_option maxHeartbeats')
header_prop=oldheader[oldheader.index('private def '):oldheader.index('\n\nend')]
assert module[start:stop]==header_prop
assert not re.search(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial',module)
assert len(mlines)==221

step_reasons=[
 'Literal q/nu/P definitions and actual83 theorem call produce the same Z with all inherited phases/AE/defect/test clauses; actual state producer is consumed, never assumed.',
 'Positive Gibbs integral from lower Hessian/C2 parent implies true integrability; base tilt probability and exact conditional-kernel identity yield every q_y probability. Kernel Markov is normalized conditional fibers, not phase-process Markov.',
 'stdGaussian probability plus q_y produces nu_y probability; actual iidExp1 P probability instantiated; unchanged actual83 clauses returned, then deterministic y/reference/f/admissible M fixed.',
 'The explicit measurable insertion maps (state,clock) into full joint Z arguments; continuous f gives joint strong measurability and SFinite P parameter-integral theorem gives measurable A_t.',
 'True actual clock probability and uniform |f|<=M imply |A_t|<=M; two nonnegative2M factors bound the discrepancy square by4M^2. Genuine inner integrability is independently retained from actual83, despite the generic bound API not requesting it as explicit argument.',
 'Measurable squared discrepancy plus pointwise4M^2 bound under the derived probability nu_y gives genuine Integrable output; no invariance or unbounded transfer is used.',
 'htest.2 is the actual83 expectation limit for every fixed state, at ordinary NNReal nhds0. Subtracting a constant then squaring yields everywhere squared limit0; no AS path inference.',
 'Filter DCT consumes exact nu_y, measurable square at every time, integrable constant4M^2, and everywhere pointwise limit. NNReal neighborhood countable generation is the metric-space background instance; integral0=0 closes only bounded subclass.'
]
steps=[];prev=141
for k,s in enumerate(unit['steps'],1):
 r=s['lean_source_region'];a=r['start_line'];b=r['end_line'];code=b''.join(mlines[a-1:b])
 assert a==prev+1;prev=b
 assert r['path']==MODULE and r['source_raw_sha256']==expected[MODULE]
 assert sha(code)==r['exact_code_raw_sha256'] and code.decode()==s['lean']
 steps.append({'step':k,'title':s['title'],'formula':s['formula'],'body_start_line':a,'body_end_line':b,
  'body_code_raw_sha256':sha(code),'formula_body_exact_match':True,'source_formula_body_semantics':step_reasons[k-1]})
assert len(steps)==8 and prev==218
assert set(range(142,219))==set(n for s in steps for n in range(s['body_start_line'],s['body_end_line']+1))

header_review=load(S+'header-source-review84/header-source.corrected-decision84.json')
node_data={
 1:('SOURCE_BINDERS_RETAINED',[24,28,136,140,147,149],'All six analytic binders survive private/public statements and actual83 call. Normalization uses only required lower-bound subdata, without deleting any source binder.'),
 2:('LITERAL_ACTUAL_PARENT_CONSUMED',[29,61,143,147,149,173,175],'Eleven literal definitions retained; actual83 supplies recurrence-dependent Z; canonical UnitExp P probability reinstantiated.'),
 3:('ACTUAL_PARENT_RETAINED_AND_USED',[63,82,147,149,175,180,184],'Same Z joint measurability used for A_t; half-open/fallback/commonAE/init returned verbatim, including final infinite-wait live arc.'),
 4:('ACTUAL83_PARENT_CONSUMED',[98,108,147,149,175,204,210],'Actual htest retained and htest.2 consumed for every-state expectation limit; true inner Integrable certificate remains in result.'),
 5:('EXPLICIT_ASTIS_CB_TEST_CLASS',[116,117,177,185,196],'Every continuous real f and every global real nonnegative bound M; source C_c subset and M0 included.'),
 6:('DERIVED_VIA_EXISTING_PARENT',[150,155],'Positive true Gibbs normalizer from existing C2/lower-Hessian augmentation theorem; Integrable.of_integral_ne_zero is valid because parent proves strict positivity.'),
 7:('SELECTED_COMPLETE_NORMALIZATION_ROUTE',[156,168],'Derived mu probability -> exact GaussianConditionalKernel -> tilted_tilted -> R_y=q_y -> q_y probability.'),
 8:('OPTIONAL_ALTERNATIVE_NOT_SELECTED',[],'Direct weighted-density domination remains a valid optional complete route; not used by this BODY and not an extra premise or missing required coverage.'),
 9:('EXACT_PROBABILITY_OUTPUT_PROVED',[112,115,144,145,159,168,176],'Actual q_y exact volume tilt normalized for every y, excludes zero-totalized tilt.'),
 10:('EXISTING_GAUSSIAN_PROBABILITY_USED',[114,146,169,172],'stdGaussian E probability instance used for exact nu product; identity covariance, no eta scale, rank0 valid.'),
 11:('EXACT_PRODUCT_PROBABILITY_PROVED',[169,179],'q_y.prod stdGaussian normalized; P actual independent clocks. Iterated integration uses these separate laws, no arbitrary correlated joint law.'),
 12:('JOINT_TEST_MEASURABILITY_PROVED',[180,184],'Measurable explicit insertion hargs, joint hZM, continuous hf; yields strong measurability of state-clock tested phase.'),
 13:('PARAMETER_INTEGRAL_MEASURABILITY_PROVED',[180,184],'StronglyMeasurable.integral_prod_right prime with actual SFinite probability P; no Fubini identity/correlation inference.'),
 14:('ABS_EXPECTATION_BOUND_PROVED',[185,190],'Generic finite-measure bound with actual P probability and pointwise abs f bound gives abs A<=M. Inner integrability already retained from actual83; not an explicit argument to this generic inequality.'),
 15:('SQUARE_MEASURABILITY_INTEGRABILITY_BOUND_PROVED',[191,203],'Triangle/algebra square bound4M^2, hsM measurable square, Integrable.of_bound with nu probability; returned for all finite t.'),
 16:('EVERY_STATE_SQUARED_LIMIT_PROVED',[204,210],'Actual htest.2 limit subtracts f(z) and squares at nonpunctured NNReal0.'),
 17:('OUTER_FILTER_DCT_PROVED',[211,218],'All-time measurability, all-state domination, integrable constant and every-state zero limit yield exact nu squared integral tending0.'),
 18:('SOURCE_CC_SPECIALIZATION_BY_CLASS_INCLUSION',[12,116,117,211,218],'Bounded C_b extension includes literal source C_c via compact-support boundedness; no full-L2 quotient operator or density theorem is claimed.'),
 19:('OPEN_EXCLUDED_NOT_PROVED',[13],'Well-defined all-L2 AE-quotient transition operator remains separate.'),
 20:('OPEN_EXCLUDED_NOT_PROVED',[13],'True phase invariance/Jensen contraction remains separate; conditional-kernel fiber probability is not it.'),
 21:('OPEN_EXCLUDED_NOT_PROVED',[13],'Full all-L2 density/contraction extension remains separate.'),
 22:('EXCLUDED_BOUNDARY_NOT_INFERRED',[13],'No Markov/restart/semigroup/main/cost/composition/uniform random-parameter/correlated-clock law consequence.'),
 23:('OPEN_INDEPENDENT_DENSITY_NOT_PROVED',[13],'Distinct reviewed G84-23 and E84-39 density ingredient remains futureOPEN, separate from contraction.')}
node_coverage=[{'node_id':n['id'],'source_status':n['status'],'disposition':node_data[int(n['id'].split('-')[-1])][0],
 'module_lines':node_data[int(n['id'].split('-')[-1])][1],'evidence':node_data[int(n['id'].split('-')[-1])][2]} for n in graph['nodes']]
item_coverage=[]
for item in inventory['items']:
 hr=next(x for x in header_review['inventory_coverage'] if x['inventory_id']==item['id'])
 evidence=[next(x for x in node_coverage if x['node_id']==n) for n in item['graph_nodes']]
 item_coverage.append({'inventory_id':item['id'],'classification':item['classification'],'source_ids':item['source_ids'],
  'graph_nodes':item['graph_nodes'],'literal_private_prop_lines':hr['header_lines'],
  'scope_evidence':hr['evidence'],'current_body_coverage':evidence,
  'disposition':'LICENSE_CONTEXT_PINNED' if not evidence else 'COVERED_BY_EXACT_CONTRACT_BODY_OR_EXPLICIT_OPEN_OR_OPTIONAL_BOUNDARY'})
edge_coverage=[]
for e in graph['edges']:
 target=next(n for n in node_coverage if n['node_id']==e['to'])
 if not e['dependency_edge']:disp='EXCLUDED_ASSOCIATION_NO_INFERENCE';reason='Nondependency boundary association; no proof credit or process-law inference.'
 elif e['status']=='OPEN_NOT_USED':disp='FUTURE_OPEN_NOT_TRAVERSED';reason='Independent future source obligation, excluded from bounded candidate proof; exact AND_OPEN junction preserved.'
 elif e['route']=='NORMALIZE_DIRECT':disp='UNSELECTED_OPTIONAL_COMPLETE_ROUTE';reason='Alternative direct-density route remains OR; selected conditional route suffices. No AND addition or false coverage gap.'
 elif e['id']=='E84-20':
  disp='RETAINED_TRUE_PARENT_CERTIFICATE';reason='Actual83 integrability certificate retained in htest and returned at175; generic norm_integral_le_of_norm_le_const at190 does not take it as explicit argument. Genuine expectation semantics established independently, not by integral_undef.'
 elif e['id'] in ['E84-31','E84-32']:
  disp='SOURCE_CC_SUBCLASS_SPECIALIZATION';reason='Continuous compactly supported source tests lie in explicit bounded real test class; this records source scope specialization, not an extra density/operator theorem.'
 else:disp='ACTUAL_COMPILED_BODY_INGREDIENT';reason=target['evidence']
 edge_coverage.append({'edge_id':e['id'],'from':e['from'],'to':e['to'],'dependency_edge':e['dependency_edge'],
  'route':e['route'],'junction_group':e['junction_group'],'source_ingredient':e['ingredient'],
  'disposition':disp,'module_lines':target['module_lines'],'evidence':reason})
assert len(item_coverage)==47 and len(node_coverage)==23 and len(edge_coverage)==39
assert sum(e['disposition']=='FUTURE_OPEN_NOT_TRAVERSED' for e in edge_coverage)==5
assert sum(e['disposition']=='EXCLUDED_ASSOCIATION_NO_INFERENCE' for e in edge_coverage)==2

def slot(original,reconstructed,evidence,relation):return {'original':original,'reconstructed':reconstructed,'evidence':evidence,'relation':relation}
slots={
 'objects':slot('Source actual iid Exp1 stopped recurrence, harmonic flow/bounce/rate, half-open arcs and exact conditional phase law q_y x N(0,I).',
  'Blind A-E recovers literal clock product, total threshold/stop records, one joint Z, exact normalized q/nu and A_t actual clock expectation.',
  'Compared primary A1.Ex1-3/E1-2 andS2.E8/S3.E1 directly with module29-82,112-124 and BODY143-184. Same actual83 witness consumed, source-terminal failed-limit zero versus inherited ASTIS uncovered-z0 version is explicit.', 'explicit-elaboration'),
 'domains':slot('Source Euclidean phase R^(2d), finite nonnegative physical times; compactly supported continuous real tests in p6.1-p6.2.',
  'Blind recovers finite-dimensional real inner-product Borel E, including rank0; NNReal finite times; bounded continuous real f with every M>=0.',
  'Module21-28,116-124; publication explicitly attributes E/rank0 and C_b extension. Real square integrands use literal product phase topology; no unbounded or all-L2 test binder.', 'explicit-elaboration'),
 'quantifiers':slot('Fixed deterministic y/reference and actual initialized construction; source first-event limit and compact-test outer DCT.',
  'Blind recovers one existential Z before all parameter choices/tests; per-fixed y/reference/z common AE all finite t/init, all-sample covered/fallback clauses; all fixed y/reference tests/bounds and times; ordinary NNReal0 limits.',
  'Module62-108,115-124,147-149,175-179,204-218 checked. No uniform-parameter AE exchange, arbitrary correlated random state, randomized y/reference or uniform-in-test limit.', 'explicit-elaboration'),
 'assumptions':slot('Six analytic standing assumptions: alpha>0,alpha<=beta,V C2,two-sided Hessian everywhere,eta>0,beta eta<=1. Continuity/boundedness describe selected test class.',
  'Blind reconstructs exactly six hypotheses/coercions and only test continuity/global nonnegative bound. Normalization, measurable phase, integrability and limits are conclusions.',
  'Private/public binders24-28/136-140 match source; actual83 call149 passes them literally. BODY150-174 derives normalization internally, no supplied minimizer, law/probability, invariance, convergence or moment certificate.', 'equivalent'),
 'conclusion':slot('Source p6.2 bounded compact-test DCT ingredient; later density and contraction extend to allL2 separately.',
  'Blind E recovers q_y/nu probability outputs, measurable state clock expectation, integrable squared discrepancy with pointwise4M^2 bound, outer squared integral tending0.',
  'Module115-124 and eight regions142-218 prove exactly this bounded actual-input integration. Source C_c is included in explicitly attributed C_b extension. No general AE-operator or all-L2 conclusion is claimed.', 'explicit-elaboration'),
 'scopes':slot('Source PropA.1 also contains invariance, contraction, density, semigroup and momentum compression; bounded DCT is one isolated ingredient.',
  'Blind expressly excludes fullL2, semigroup, invariance, reversibility, uniqueness/generator and positive-time continuity; publication also excludes full process/main/cost/composition.',
  'Independent effective graph five futureOPEN edges33-36/39 andtwo excluded associations37-38 all retain status. Selected normalization route is OR with optional direct route; no process Markov inferred from IsMarkovKernel of exact conditional R.', 'equivalent'),
 'constant_dependencies':slot('Exact eta scale in potential and harmonic flow/rate, unit covariance momentum; finite test bound supports domination. Source p6.1 first-event factor1-exp(-Lambda).',
  'Blind recovers exact2 and4 constants, eta and2eta, standard unscaled momentum Gaussian, every M>=0 including0, no dimension-dependent constant/extra derivative or moment bound.',
  'Module31-42,106,113-114,185-203 preserves all factors. Uniform4M^2 integrable under derived probability at211-217; no need integrated-hazard moment or actual invariance.', 'explicit-elaboration')}
assert set(slots)==set(packet['review_contract']['semantic_slots'])
assert all(x['relation'] in packet['review_contract']['slot_relations'] for x in slots.values())
deltas=[
 {'id':'SR84-D01','slot':'domains','classification':'EXPLICIT_ASTIS_CB_AND_FINITE_SPACE_ELABORATION','blocking':False,
  'description':'Source C_c Euclidean tests are extended to bounded continuous real tests on finite-dimensional real inner-product Borel E including rank0. Exact global M>=0 is explicit; finite actual probability makes this extension valid.'},
 {'id':'SR84-D02','slot':'objects','classification':'EXPLICIT_INHERITED_MEASURABLE_VERSION_ADAPTER','blocking':False,
  'description':'Source uses failed-terminal-limit zero; retained actual phase uses uncovered-z0 convention with fixed-parameter common AE live-arc/init semantics. Publication discloses adapter and prohibits uniform/correlated AE substitution.'},
 {'id':'SR84-D03','slot':'conclusion','classification':'SOURCE_IMPLICIT_BOUNDED_OUTER_DCT_INGREDIENT_EXPLICIT','blocking':False,
  'description':'New measurable state expectation and exact-law squared-integral limit explicitly close source p6.2 bounded-test DCT ingredient. Actual83 and exact normalization producers are genuinely consumed; this is not supplied-measurability wrapper churn.'},
 {'id':'SR84-D04','slot':'scopes','classification':'EXPLICIT_FIVE_OPEN_DEPENDENCIES_TWO_EXCLUDED_ASSOCIATIONS','blocking':False,
  'description':'True phase invariance/Jensen contraction, all-L2 quotient operator and independent C_c density remain OPEN. Optional direct q normalization is unselected OR route, not missing required ingredient. No Markov/invariance/cost credit from normalized laws.'}]
independence={'reviewer':'/root/fresh_source78','formalizer':packet['roles']['formalizer'],
 'blind_decoder':packet['roles']['blind_decoder'],'independent_from_formalizer':True,'independent_from_decoder':True,
 'original_source_inventory_extractor':True,'distinct_topology_overlay_proposer':False,'original_graph_self_validation':False,
 'source_first_chronology':'Original47item source inventory/22node topology frozen before candidate; distinct proposer exact_verify77 density overlay independently reviewed to effective23node/39relation. Current full BODY review reparsed all26 primary anchors before BODY/publication; prepacket-preparation84 RAW fixes that chronology. Fresh reconstruction read only via exact canonical packet afterwards.',
 'other_math_review_verdicts_read':False,'root_adoption_reports_read':False,'blind_files_outside_canonical_packet_read':False,
 'own_prior_header_scope_use':'Unchanged source scope mappings and distinct exact syntax-only correction reused; final BODY/decoder/publication comparison performed independently anew.',
 'writes':'Owned independent-source84 native receipts only; no production/audit/ledger/cell/site/state mutation.',
 'verification_credit':'Source fidelity review only; no self VERIFIED, exact-commit/compiler gate, PURIFIED/live/full-Goal credit.'}
extra_inputs=['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
 'lean-toolchain','lake-manifest.json','tools/astis_publication.py']
raw_inputs=[pin(p) for p in list(expected)+extra_inputs]
assert pin(extra_inputs[0])['raw_sha256']=='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
evidence={'schema':'astis.independent-source-review84.run-evidence.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'reviewer_packet_sha256':packet['packet_sha256'],'reviewer_packet_raw_sha256':pin(PACKET)['raw_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':pin(MODULE)['raw_sha256'],
 'source_first_primary_anchor_pins':inventory['source_anchor_coverage'],'all26_primary_anchor_hashes_match':True,
 'exact_private_prop_matches_preproof_reviewed_successor':True,'full_module_lines_reviewed':221,
 'source_graph_counts':graph['counts'],'future_open_dependencies':5,'excluded_associations':2,
 'authored_step_coverage':{'expected_steps':8,'reviewed_steps':8,'gaps':[],'overlaps':[],
  'formula_body_exact_matches':8,'body_line_range':[142,218],'steps':steps},
 'publication_checks':{'full_statement_read':True,'all12_condition_explanation_rows_read':True,
  'four_public_formula_rows_and_eight_lesson_formula_rows_checked':True,'statement_and_assumptions_identical_to_packet_and_lesson':True,
  'publication_binding_independently_recomputed':True,'fake_closure_scan':False,
  'toolchain_and_lake_manifest_lf_hashes_match_context':True},
 'toolchain_hash_convention':'RAW inputs retain exact CRLF bytes; publication file_digest uses read_text UTF8 newline-normalized LF. Both verified, never silently substituted.',
 'graph_vs_actual_body_detail':'E84-20 inner integrability is a retained true actual83 result, not an explicit argument of the generic norm integral bound. Coverage distinguishes semantic certificate availability from direct Lean argument use. No fake integral_undef closure occurs.',
 'independence':independence,'noncircularity':'Evidence excludes result/manifest hashes; result binds exact evidence RAW; final manifest binds all owned outputs including result, omitting selfhash.'}
def emit(n,obj):
 p=OUT/n;assert not p.exists(),p;p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode())
emit('source-review.run-evidence84.json',evidence)
result={'schema':'astis.independent-source-review84.v1','status':'closed','created_utc':now,
 'verdict':'equivalent-after-elaboration',
 'verdict_reason':'The exact full module, fresh blind reconstruction and every authored formula/BODY region preserve the independently frozen bounded source consumer: actual83 Z and exact q_y x standard-Gaussian probability yield measurable state clock expectations and outer bounded-square convergence at ordinary NNReal0. Source C_c vs explicit ASTIS C_b extension and exceptional representative adapter are disclosed. All47items/23nodes/39relations are covered or explicitly optional/OPEN/excluded. No substantive mathematical/source repair required.',
 'semantic_slots':slots,'deltas':deltas,'repairs':[],'no_required_mathematical_repairs':True,
 'reviewer':'/root/fresh_source78','independent_from_formalizer':True,'independent_from_decoder':True,
 'reviewer_packet_sha256':packet['packet_sha256'],'reviewer_packet_raw_sha256':pin(PACKET)['raw_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':pin(MODULE)['raw_sha256'],
 'review_run_sha256':sha((OUT/'source-review.run-evidence84.json').read_bytes()),
 'review_evidence':'Whole exact221line module, actual83 parent BODY, exact normalization and actual clock parent APIs, parameter-integral/norm-bound/filterDCT APIs, full public statement/conditions, all8 contiguous authored formula/BODY regions and canonical source-blind reconstruction independently compared with primary and preproof source graph.',
 'authored_step_coverage':evidence['authored_step_coverage'],
 'source_graph_coverage':{'inventory_expected':47,'inventory_reviewed':47,'inventory':item_coverage,
  'nodes_expected':23,'nodes_reviewed':23,'nodes':node_coverage,
  'relations_expected':39,'relations_reviewed':39,'relations':edge_coverage,
  'dependency_edges':37,'future_open_dependency_ids':['E84-33','E84-34','E84-35','E84-36','E84-39'],
  'excluded_association_ids':['E84-37','E84-38'],'selected_normalization_route':'G84-06 -> G84-07 -> G84-09',
  'unselected_optional_route_ids':['G84-08','E84-09','E84-10','E84-12'],'junctions':graph['junctions'],
  'gaps':[],'missing_required_ingredients':[]},
 'publication_coverage':{'full_statement':True,'all_assumption_rows':12,'public_formula_rows':4,'lesson_formula_steps':8,
  'support_binding':'actual-bounded-outer only; full-l2-process obligation unsupported/OPEN',
  'source_not_publication_text_authority':'Pinned primary RAW and independent inventory control the review; packet source/publication text treated as candidate claims, not source authority.'},
 'truth_boundary':['Bounded continuous real representative squared-integral convergence only; source C_c subclass is included, not full all-L2 equivalence-class transition operator.',
  'Normalized actual nu_y is not proved invariant. True phase invariance/Jensen contraction and separate C_c density remain OPEN.',
  'Conditional-kernel IsMarkovKernel means probability fibers, not Markov/restart/semigroup dynamics.',
  'Fixed deterministic y/reference; no arbitrary correlated phase-clock initialization or uniform-parameter AE event.',
  'Rank0/M0/zero normal/zero hazard/raw zero thresholds/infinite first or last wait/stopped dummy retain inherited actual conventions.',
  'No AS-DCT shortcut or new unbounded moment/cost, implemented sampler, hypocoercivity/main/composition/PURIFIED/live/full-Goal claim.'],
 'independence':independence,'no_state_transition':True}
assert result['verdict'] in packet['review_contract']['verdicts']
emit('source-review.result84.json',result)
outputs=['prepacket-preparation84.json','close_source_review84.py','source-review.run-evidence84.json','source-review.result84.json']
manifest={'schema':'astis.independent-source-review84.raw-manifest.v1','status':'closed','created_utc':now,
 'reviewer_packet_sha256':packet['packet_sha256'],'reviewer_packet_raw_sha256':pin(PACKET)['raw_sha256'],
 'publication_binding_sha256':packet['publication_binding_sha256'],'full_module_sha256':pin(MODULE)['raw_sha256'],
 'raw_inputs':raw_inputs,'raw_outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs],
 'selfhash_convention':'Omit manifest selfhash to avoid circularity. Exact final manifest RAW reported externally; result binds preexisting run-evidence RAW.',
 'source_first_chronology':independence['source_first_chronology'],'owned_directory':OUT.relative_to(ROOT).as_posix(),
 'original_source_freezes_unchanged':True,'production_and_shared_truth_writes':False,'proof_state_or_verification_transition':False}
emit('source-review.run-manifest84.json',manifest)
print(json.dumps({'verdict':result['verdict'],'outputs':[pin((OUT/n).relative_to(ROOT).as_posix()) for n in outputs+['source-review.run-manifest84.json']]},indent=2))
