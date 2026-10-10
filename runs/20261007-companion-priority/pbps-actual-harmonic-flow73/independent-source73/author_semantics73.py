from pathlib import Path
import hashlib,json,os,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=BASE/'independent-source73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def write(n,x):
 p=OWN/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not(OWN/'lease.final.json').exists()
packet=load(BASE/'source-review.packet.json');reconstruction=load(BASE/'anonymous-decoder/reconstruction.json')
assert reconstruction['reconstructed_theorem_text']==packet['blind_reconstruction']['text']
assert sha(reconstruction['reconstructed_theorem_text'].encode())==packet['blind_reconstruction']['text_sha256']
P=OWN.relative_to(ROOT).as_posix()+'/'
slots={
 'objects':{
  'original':'The actual finite Euclidean/Hilbert state and given C2 potential V; actual center c=y−η∇V(xRef), literal two-coordinate harmonic map Φ and H=(η^-1||x−c||²+||p||²)/2.',
  'reconstructed':'A finite-dimensional real inner-product Borel E, real Hilbert gradient representing DV, actual same c, Φ and real weighted sum H on unrestricted z=(q,p); the decoder q renames source x.',
  'relation':'equivalent',
  'evidence':P+'caller-definition-nine-conclusion-review73.json and whole178-line-coverage73.json; actual literal20–56 and duplicate definitions69–75. Frozen primary S3.E4/S4.E5/A1.EGx1/A1.Ex4. Gradient convention matches the independently source-checked canonical local producer.'},
 'domains':{
  'original':'Finite Euclidean state with real vectors, fixed positive eta, arbitrary y,xRef,x,p and real time. Source-derived continuity/Borel completion is on the complete joint product domain, with separate E component norms.',
  'reconstructed':'E finite-dimensional real Hilbert with its norm topology and Borel measurable structure, including rank0. F has domain (E×E)×(R×(E×E)) and codomain E×E; individual E norms only. No continuity in eta through0.',
  'relation':'explicit-elaboration',
  'evidence':P+'caller-definition-nine-conclusion-review73.json; literal21–23/36–39, production104–110 and hcont.measurable173. Coordinate-free finite-Hilbert/Borel and rank0 elaboration was frozen before implementation; no positive-dimension assumption.'},
 'quantifiers':{
  'original':'The selected source arc fixes arbitrary y,xRef and arbitrary initial position/momentum. Each identity is at these same parameters; source-derived explicit formula/group completion extends to all real s,t.',
  'reconstructed':'All ambient structures/V/alpha/beta/eta satisfying the six conditions; independent arbitrary y,xRef and z=(q,p), local universal real times in each conjunct. Both inverse orders and derivatives occur under each same displayed scope.',
  'relation':'explicit-elaboration',
  'evidence':P+'caller-definition-nine-conclusion-review73.json; source S3.Prop3.1 fixed inputs, S4.E5 restart and A1 literal; current literal36–56 and hzero/hgroup/hinverse/hode/hnonneg/henergy/hpi111–172. No Gaussian-support restriction or additional relation on reference/state.'},
 'assumptions':{
  'original':'Original six standing analytic callers: 0<alpha, alpha<=beta, V in C2 globally, both global Hessian quadratic bounds, eta>0, beta*eta<=1. Real finite-dimensional Borel typing. Ingredient continuities/scale/trig/norm-cancellation must be internal.',
  'reconstructed':'Exact same global regularity and both bounds for all x,v, nonnegative modulus carriers, strict positive alpha/eta and non-strict cap. No provider/flow law/ODE/energy theorem or extra smoothness premise.',
  'relation':'same',
  'evidence':P+'caller-definition-nine-conclusion-review73.json: private and public caller prefixes byte-equal to source-reviewed prospective header. BODY101–103 uses hV,98–100/146–148 uses hη; hα,hαβ,hH,hβη are retained but not invoked in the deterministic proof.'},
 'conclusion':{
  'original':'Source exact harmonic coordinates, ODE, flow energy conservation and pi endpoint, with independently frozen elementary completion to joint continuity/Borel, initial/group/two inverse and nonnegativity. Exactly the selected deterministic ingredient, not stochastic Proposition3.1.',
  'reconstructed':'All nine conclusions simultaneously: full joint continuous/Borel map, zero/group/both inverse identities, both exact norm derivatives, nonnegative weighted sum H, conserved same H and Phi_pi=(2c−q,−p). No sampling, stationarity, convergence or cost result.',
  'relation':'explicit-elaboration',
  'evidence':P+'source-proof-implementation-coverage73.json (all23nodes/37edges/7bridge productions), source79-current-coverage73.json and six-step-formula-exposition-review73.json. Full proof final tuple173 contains every conjunct; formula and constant/sign checks completed.'},
 'scopes':{
  'original':'Same V,eta, actual center and fixed xRef throughout each composition, energy equality and time derivative. c/Phi/H are source definitions; stochastic bounce/hazard/clock/kernel and full paper remain excluded.',
  'reconstructed':'Three successive local lets scope the complete conjunction. E,V,alpha,beta,eta are fixed outer data; continuity varies y,xRef,t,z only. gradV stays at xRef. Private literal is specification/nonprovider; public theorem proves it.',
  'relation':'same',
  'evidence':P+'whole178-line-coverage73.json; unchanged complete private literal20–56, public58–67, definitionally exact change69–97 and final173. All55 source exclusions remain explicitly excluded; lesson helper is full private literal identity and boundary expressly distinguishes deterministic pi from stochastic terminal law.'},
 'constant_dependencies':{
  'original':'Given alpha,beta,eta; c depends on y−eta gradVxRef, Phi on same eta via sqrt/reciprocal and same center, H on eta^-1 and same center. Only fixed0,1,2,pi; no hidden cost, dimension, energy or nonzero-normal constant.',
  'reconstructed':'Identical eta and gradient dependencies. Alpha/beta enter only the preserved hypotheses, no existential constants. The coefficient−sin(t)/sqrtη and derivative−(sqrtη)^-1(X−y)−sqrtη gradVxRef have the printed signs.',
  'relation':'same',
  'evidence':P+'caller-definition-nine-conclusion-review73.json and six-step-formula-exposition-review73.json; sqrt scale98–100, derivative135–145, energy151–165 and endpoint166–172. Rank0/alphaeta1/zero-energy cases require no extra dependency.'}}
deltas=[
 {'slot':'objects','severity':'informational','description':'Decoder q is the unrestricted source/current first coordinate x. Actual cached-gradient center, two coordinates and weighted SUM energy are preserved exactly.','evidence':slots['objects']['evidence']},
 {'slot':'domains','severity':'informational','description':'Finite real Hilbert/Borel and rank-zero presentation explicitly elaborates source Euclidean coordinates; full joint domain has five scalar/vector inputs packaged as four y,xRef,t,z arguments. No product norm is substituted.','evidence':slots['domains']['evidence']},
 {'slot':'quantifiers','severity':'informational','description':'All-real group/inverse/time scope is a frozen source-derived elementary extension of the explicit arc. It is proved from the same literal formula, not supplied as a caller.','evidence':slots['quantifiers']['evidence']},
 {'slot':'assumptions','severity':'informational','description':'NNReal modulus carriers and real quadratic-form expansion preserve original both Hessian bounds and non-strict cap. Six callers remain; only hV/hη are actually used in this deterministic BODY.','evidence':slots['assumptions']['evidence']},
 {'slot':'conclusion','severity':'informational','description':'Seven omitted deterministic bridges are produced internally, including the already existing canonical Gradient theorem. This completes the selected nine-clause contract without promoting any ingredient to a public premise.','evidence':slots['conclusion']['evidence']},
 {'slot':'conclusion','severity':'informational','description':'Energy is half the weighted sum of separate squared E norms. The proof expands both norm squares, cancels opposite real inner cross terms, preserves the exact weight and factor, and uses sin²+cos²=1.','evidence':P+'six-step-formula-exposition-review73.json step4; BODY149–165; primary A1.Ex4 and A1.SS1.p3.2.'},
 {'slot':'scopes','severity':'informational','description':'Complete private literal is definitionally unchanged from the source-reviewed header and acts as a proposition specification, not a provider. Public proof changes to exactly those nine clauses and supplies all of them.','evidence':slots['scopes']['evidence']},
 {'slot':'scopes','severity':'informational','description':'All55 stochastic/measure/kernel/cost exclusions remain excluded. The deterministic pi endpoint is not the actual bounced terminal H_y law, and no B27/B28 or full PBPS/SPHMC result follows here.','evidence':P+'source79-current-coverage73.json and exact lesson/binding boundaries.'},
 {'slot':'constant_dependencies','severity':'informational','description':'Positive eta supplies sqrt reciprocal identities internally. Same actual center gives the exact second ODE force with fixed xRef; no higher derivative, nonzero-energy/normal, positive dimension or strict endpoint condition is added.','evidence':slots['constant_dependencies']['evidence']},
 {'slot':'scopes','severity':'informational','description':'Source URL #A1 is an accurate broad AppendixA parent containing A.1; the independent fixed-RAW anchor check confirms exact source identity without a network refresh.','evidence':P+'StageB.source-URL-anchor-accuracy73.json'}]
assert set(slots)==set(packet['review_contract']['semantic_slots']) and len(slots)==7
for r in slots.values():assert r['relation'] in packet['review_contract']['slot_relations']
for d in deltas:assert set(d)=={'slot','severity','description','evidence'} and d['slot'] in slots
write('source.0.semantic-judgments73.frozen.json',{'status':'INDEPENDENT_MATHEMATICAL_SOURCE_COMPARISON_COMPLETE_FINAL_TRANSPORT_WAITING_DISTINCT_READER_METADATA_OVERLAY','official_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'verdict':'equivalent-after-elaboration','semantic_slots':slots,'deltas':deltas,'blocking_mathematical_deltas':0,'repairs':[],'mathematical_or_binder_repairs_required':False,'reader_metadata_repair_is_separate_not_self_approved':True,'decoder_native_text_and_seven_slots_read':True,'decoder_native_text_matches_official_packet':True,'source_identity_blindness_reported_and_not_inferred_as_source_acceptance':True,'previous_other_math_or_source_verdict_consumed':False,'reviewer':'/root/independent_primary69'})
write('semantic-authoring.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False})
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'slots':7,'deltas':len(deltas),'blocking_math':0,'verdict':'equivalent-after-elaboration','reader_process_overlay_final_authority_pending':True},indent=2))
