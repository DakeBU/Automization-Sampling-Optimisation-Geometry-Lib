"""Independent source-only prospective preread83; no Lean/state writes."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime,timezone
import hashlib,json
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-bounded-test-preread83'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
PIN='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def save(name,obj):
 p=OWN/name;assert not p.exists(),name
 p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
assert sha(PRIMARY)==PIN
class SourceParser(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.math_depth=0;self.by_id={}
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.stack.append((tag,d.get('id'),[]))
  if tag=='math':
   self.math_depth+=1
   if self.math_depth==1:
    for e in self.stack:e[2].append(' '+d.get('alttext','')+' ')
 def handle_data(self,data):
  if not self.math_depth:
   for e in self.stack:e[2].append(data)
 def handle_endtag(self,tag):
  if tag=='math':self.math_depth-=1
  for j in range(len(self.stack)-1,-1,-1):
   if self.stack[j][0]==tag:
    e=self.stack[j]
    if e[1]:self.by_id[e[1]]=' '.join(''.join(e[2]).split())
    self.stack=self.stack[:j];break
parser=SourceParser();parser.feed(PRIMARY.read_text('utf8'))
now=datetime.now(timezone.utc).isoformat()
rows=[
 ('infobox','provenance','Fixed v1, authors Chen/Chewi/Lu/Zhang, arXiv perpetual non-exclusive license. No new public bulk source copying.',['G83-01']),
 ('S1.p1.1','standing-binders','V is C2 and 0<alpha<=beta; two positivity/order binders plus smoothness.',['G83-01']),
 ('S1.E1','standing-binders','Everywhere alpha I <= Hess V <= beta I, one original Hessian sandwich binder.',['G83-01']),
 ('S2.SS2.p1.1','standing-binders','Scale 0<eta<=1/beta; retain positive eta and beta eta<=1. Together exactly six analytic binders.',['G83-01']),
 ('S3.E4','literal-definitions','Center c=y-eta gradV(r), gradient remainder h_r(x)=gradV(x)-gradV(r).',['G83-02','G83-04']),
 ('A1.SS1.p1.1','fixed-parameters','Work at deterministic fixed y,r; phase z0=(x0,p0). No random-state substitution.',['G83-01','G83-02']),
 ('A1.Ex1','literal-rate','Actual rate sqrt(eta) times positive part of pairing p,h_r(x).',['G83-02','G83-05']),
 ('A1.Ex2','literal-flow','Actual harmonic flow with c, sqrt(eta), reciprocal sqrt(eta), sin and cos; continuous at0 and Phi0=id.',['G83-02','G83-04']),
 ('A1.Ex3','literal-bounce','Actual phase reflection; R0=id, finite wait update only.',['G83-02']),
 ('A1.SS1.p1.3','exception-boundary','Bounce may be discontinuous where normal vanishes; no bounce continuity is used in proposed test limit.',['G83-02','G83-06']),
 ('A1.SS1.p2.1','actual-input','Independent Exp1 clocks, source E1 starts initial live phase at T0=0. Index0 implementation corresponds to source E_(n+1).',['G83-02','G83-03','G83-05']),
 ('A1.E1','actual-wait','Integrated-hazard first threshold hit, empty-hit wait infinity.',['G83-02','G83-05']),
 ('A1.E2','actual-recursion','Finite wait adds to time and applies bounce at endpoint; no flow evaluation at infinity.',['G83-02']),
 ('A1.SS1.p2.2','physical-interpolation','Half-open finite arcs; infinite next wait leaves final live arc at every finite elapsed time, stopped dummy is auxiliary.',['G83-02','G83-06']),
 ('A1.SS1.p3.7','nonaccumulation-boundary','Source direct Exp mean1 SLLN establishes nonaccumulation; memorylessness/Markov continuation is separate. Existing actual parents may realize an explicit sufficient SLLN alternative.',['G83-03','G83-17']),
 ('A1.SS2.p3.1','measurable-version','Source joint Borel recursion and almost-sure terminal limit; source failed-limit zero vs actual uncovered-z0 convention is an explicit exceptional adapter.',['G83-03','G83-09']),
 ('A1.SS1.SSS0.Px1.p6.1','real-consumer','Source C_c test flow converges to identity; first-event control is the immediate pointwise ingredient of later strong continuity.',['G83-04','G83-05','G83-14']),
 ('A1.Ex22','exact-smalltime','First-event probability 1-exp(-Lambda_t) tends to0. Phase-flow defect is a subset, not necessarily the same event.',['G83-05','G83-07','G83-10','G83-12']),
 ('A1.SS1.SSS0.Px1.p6.2','pointwise-hidden-step','Before integrating a squared pointwise operator difference over phase, one must establish pointwise expectation convergence. C_c is continuous and bounded in finite phase dimension.',['G83-08','G83-12','G83-14']),
 ('A1.SS1.SSS0.Px1.p6.2','DCT-open','DCT over initial phase requires its measurable probability measure, pointwise convergence and an integrable bound. This is distinct from stochastic convergence over clock samples.',['G83-15']),
 ('A1.SS1.SSS0.Px1.p6.1','Jensen-invariance-open','Source obtains L2 contraction from invariance plus Jensen, which the proposed fixed-state expectation edge neither assumes nor proves.',['G83-16']),
 ('A1.SS1.SSS0.Px1.p6.2','density-open','Extension from C_c to all L2 uses density plus an already established contractive operator family.',['G83-16']),
 ('A1.Thmtheorem1','global-open','Transition operators are introduced for the process of Prop3.1. Markov/semigroup/adjoint claims cannot follow from expectation convergence at0.',['G83-17']),
 ('S3.E1','outer-measure-context','nu_eta,y is exact conditional Gibbs position law times Gaussian momentum. No nu invariance premise is needed to integrate over clocks at fixed z0.',['G83-15','G83-16']),
 ('A1.SS1.SSS0.Px1.p5.3','invariance-source-gap','Source path reversal supplies invariance before contraction; do not import its conclusion from the word transition.',['G83-16','G83-17']),
 ('A1.E7','path-law-open','Full jump-number/path expansion and Tonelli change-of-variables are separate; first-wait split does not prove that expansion.',['G83-17']),
 ('A1.SS1.SSS0.Px1.p6.2','ASTIS-test-extension','General bounded continuous real test is an explicit conservative extension of source C_c pointwise ingredient; boundedness is a property of test, not an added potential/trajectory assumption.',['G83-08','G83-09','G83-11','G83-12']),
 ('A1.Ex22','ASTIS-integration-adapter','Actual82 defect bound can be integrated: bounded test discrepancy relative to deterministic free flow is at most 2M times defect probability. Produces genuine expectation estimate, no supplied estimate premise.',['G83-07','G83-09','G83-10']),
 ('A1.SS1.SSS0.Px1.p6.1','ASTIS-alternative-route','Actual82 convergence in probability plus local continuity and uniform boundedness gives expected absolute discrepancy convergence by epsilon/delta split. No a.s. convergence or samplewise DCT is inferred.',['G83-13']),
 ('A1.SS2.p4.1','prior-consumer-exclusion','Ideal exact-reference H_y averaging is separate; this fixed-reference clock expectation does not claim an implemented reference sampler or random-alltime law.',['G83-17'])]
items=[]
for i,(anchor,kind,paraphrase,nodes) in enumerate(rows,1):
 assert anchor in parser.by_id,anchor
 items.append({'id':f'I83-{i:02d}','source_id':anchor,'classification':kind,'paraphrase':paraphrase,'source_graph_nodes':nodes,
  'exact_anchor_text_sha256':hashlib.sha256(parser.by_id[anchor].encode('utf8')).hexdigest()})
inv=save('source_inventory83.json',{'schema':'source-only-inventory-v1','created_utc':now,'primary':raw(PRIMARY),
 'scope':'Actual fixed-state bounded-continuous-test expectation smalltime prerequisite immediately after actual82; not source theorem completion.',
 'parser':'stdlib html.parser, math alttext once per math subtree, whitespace-normalized solely for anchor digest; PRIMARY RAW remains authority.',
 'six_analytic_hypotheses':['0<alpha','alpha<=beta','V C2','everywhere Hessian alpha/beta sandwich','0<eta','beta*eta<=1'],
 'test_contract':'f:phase->R continuous and globally bounded; choose M>=0 with forall z,abs(f(z))<=M. Test-class definition, not source dynamical assumption.',
 'items':items,'candidate_or_Lean83_seen':False,'other_review_verdicts_used':False,
 'licensing':'arXiv perpetual non-exclusive; private minimal formulas/paraphrases, no full raw-source duplication.'})
node_specs=[
 ('Standing source hypotheses and fixed parameters','DIRECT_SOURCE','Six analytic binders; deterministic y,r,z0.',['S1.p1.1','S1.E1','S2.SS2.p1.1']),
 ('Actual initialized recurrence and physical interpolation','DIRECT_SOURCE','Source clock E1, live z0,T0=0, guarded finite bounce, half-open arcs and last live infinity wait.',['A1.E1','A1.E2','A1.SS1.p2.1','A1.SS1.p2.2']),
 ('Actual measurable realization over probability clocks','INHERITED_ACTUAL_ADAPTER','Use existing actual construction and probability clocks internally; fixed-parameter common AE allfinite/init. No arbitrary supplied Z.',['A1.SS2.p3.1','A1.SS1.p3.7']),
 ('Actual free-flow continuity at0','DIRECT_SOURCE_WITH_ACTUAL_PARENT','Phi_t z0 tends z0 and Phi0=id; finite NNReal times.',['A1.Ex2','A1.SS1.SSS0.Px1.p6.1']),
 ('Actual firstwait law and hazard smalltime control','DIRECT_SOURCE_WITH_ACTUAL_PARENT','P(t<firstwait)=exp(-Lambda_t); Lambda0=0 and continuity imply q_t=1-exp(-Lambda_t)->0.',['A1.E1','A1.Ex22']),
 ('First live arc agreement','DIRECT_SOURCE_WITH_ACTUAL_PARENT','For t<firstwait actual phase equals free flow, including firstwait infinity.',['A1.SS1.p2.2']),
 ('Measurable actual phase-flow defect bound','INHERITED_ACTUAL82_ADAPTER','Actual82 internally yields measurable D_t and P(D_t)<=q_t; ineffective bounce prevents event equality claim.',['A1.Ex22','A1.SS1.p2.2']),
 ('Bounded continuous real test','TEST_CLASS','f continuous, |f|<=M for some M>=0; source C_c contained in this class.',['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']),
 ('Actual test measurability and integrability','ASTIS_NEW_INTEGRATION','Composition f(Z_t) measurable and bounded over a probability measure, hence integrable; discrepancy also integrable.',['A1.SS2.p3.1','A1.SS1.SSS0.Px1.p6.2']),
 ('Integrated defect-to-test estimate','ASTIS_NEW_INTEGRATION','abs(E f(Z_t)-f(Phi_t z0)) <= E abs(f(Z_t)-f(Phi_t z0)) <= 2M q_t.',['A1.Ex22','A1.SS1.SSS0.Px1.p6.1']),
 ('Deterministic test-flow convergence','DIRECT_SOURCE_INGREDIENT','Continuity of f at z0 and Phi_tz0->z0 give f(Phi_tz0)->f(z0).',['A1.SS1.SSS0.Px1.p6.1']),
 ('Actual fixed-state test expectation convergence','BOUNDED_CANDIDATE_OUTPUT','E f(Z_t)->f(z0), nonpunctured NNReal nhds0; integrability every finite t, expectation0 correct AE init.',['A1.SS1.SSS0.Px1.p6.2']),
 ('Optional bounded-test probability route','OPTIONAL_OR_ALTERNATIVE','For eps>0 choose delta from continuity: E|f(Z_t)-f(z0)|<=eps+2M P(||Z_t-z0||>=delta); consume actual82 probability tails.',['A1.SS1.SSS0.Px1.p6.1','A1.Ex22']),
 ('Source C_c pointwise operator ingredient','GENUINE_IMMEDIATE_CONSUMER','Specialize to C_c before the source outer L2 DCT; interpret expectation as pointwise operator value without claiming Markov/semigroup laws.',['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']),
 ('Outer-state squared DCT','EXCLUDED_OPEN','Need joint/state measurability, exact finite probability nu and squared domination e.g.4M^2 to derive C_c L2 convergence. Not a clockwise DCT from probability convergence.',['S3.E1','A1.SS1.SSS0.Px1.p6.2']),
 ('Invariant Jensen contraction and dense L2 extension','EXCLUDED_OPEN','Invariance/Jensen establish contraction; C_c density and well-defined equivalence-class operators extend to all L2.',['A1.SS1.SSS0.Px1.p5.3','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']),
 ('Global process/kernel/composition boundaries','EXCLUDED_OPEN','Markov/restart/semigroup/invariance/reversal/path expansion/hypocoercivity/algorithm costs/main/composition and correlated random-state substitutions remain separate.',['A1.Thmtheorem1','A1.E7','A1.SS2.p4.1'])]
nodes=[{'id':f'G83-{i:02d}','title':s[0],'kind':s[1],'obligation':s[2],'source_ids':s[3]}for i,s in enumerate(node_specs,1)]
edge_specs=[
 (1,2,'Exact source dynamical context'),(1,3,'Existing actual construction under six binders'),(1,4,'Actual harmonic regularity'),(1,5,'Actual hazard regularity'),
 (2,3,'Measurable stopped recursion and nonaccumulation realization'),(2,6,'Initialized live first arc'),(5,6,'Strict nofirstevent clock interval'),
 (3,7,'Actual phase measurable'),(5,7,'Actual first-event survival'),(6,7,'Defect subset event complement'),
 (3,9,'Actual composition measurable, probability input'),(8,9,'Continuous bounded test integrability'),
 (7,10,'Measurable defect probability bound'),(8,10,'Outside defect equality, inside bound2M'),(9,10,'Absolute-integral inequality and bounded indicator integration'),
 (4,11,'Free flow tends to initial phase'),(8,11,'Test continuity at initial phase'),
 (5,12,'q_t tends0'),(10,12,'Actual expectation comparison estimate'),(11,12,'Deterministic test-flow convergence'),
 (3,13,'Fixed-parameter actual probability law'),(8,13,'Local continuity plus global boundedness'),(7,13,'Actual82 stochastic continuity tail is available alternative'),
 (13,12,'OPTIONAL OR alternative to integrated free-flow route; not mandatory AND'),
 (12,14,'Specialization bounded-continuous to source C_c'),(14,15,'Pointwise prerequisite only; no assertion outer DCT already proved'),
 (15,16,'Prospective C_c L2 convergence plus independent contraction and density; not current formal implication'),
 (16,17,'Global conclusions require independent process/operator laws; topology only, not theorem credit')]
edges=[{'id':f'E83-{i:02d}','ingredient':f'G83-{a:02d}','consumer':f'G83-{b:02d}','reason':s,
 'status':'OPTIONAL_OR'if 'OPTIONAL' in s else ('EXCLUDED_OPEN'if b>=15 else 'SCOPED_INGREDIENT')}for i,(a,b,s) in enumerate(edge_specs,1)]
graph=save('source_proof_graph83.json',{'schema':'independent-source-proof-graph-v1','created_utc':now,'primary':raw(PRIMARY),
 'truth_contract':'Source/adapter obligation topology frozen before any83 candidate; not Lean dependency graph or theorem proof. Optional alternative routes OR, excluded global edges OPEN.',
 'nodes':nodes,'edges':edges,'scope_coverage':{'inventory':len(items),'nodes':len(nodes),'edges':len(edges),
 'all_inventory_items_mapped':all(x['source_graph_nodes']for x in items),'excluded_nodes':['G83-15','G83-16','G83-17'],
 'optional_node':'G83-13','candidate_output_nodes':['G83-09','G83-10','G83-12','G83-14']}})
candidate=save('bounded_candidate83.json',{'schema':'prospective-source-only-bounded-candidate-v1','created_utc':now,
 'recommendation':'Proceed with one bounded actual fixed-reference test expectation integration consumer; not redundant82, provided actual82 is consumed internally rather than supplied as a premise.',
 'name':'Actual PBPS bounded-continuous-test expectation convergence at zero',
 'primary_consumer':['A1.Ex22','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2'],
 'source_reason':'The source passage from rare first event and continuous free flow to outer L2 DCT implicitly requires pointwise expectation convergence. Existing82 phase-tail convergence has not itself integrated a test function.',
 'analytic_binders':['0<alpha','alpha<=beta','V C2','Hessian sandwich everywhere','0<eta','beta*eta<=1'],
 'definition_test_binders':['f: E x E -> R continuous','exists M>=0, forall z, abs(f(z))<=M'],
 'quantifiers':'For every deterministic fixed y,r,z0 and each bounded continuous real test, every finite t in NNReal has integrable f(Z_t), and its actual clock expectation tends f(z0) at ordinary nonpunctured nhds0. No common nullset or rate uniform in parameters/test/state.',
 'actual_objects':'Actual canonical iid Exp1 probability input and existing physical realization witness obtained internally under six binders; retain actual recurrence/AE allfinite/init and exceptional conventions. No user-supplied arbitrary process, law or stochastic-continuity certificate.',
 'bounded_outputs':['Measurable and integrable actual f(Z_t) for every finite t',
 'abs(E f(Z_t)-f(Phi_t z0)) <= 2M(1-exp(-Lambda_t))',
 'E f(Z_t) -> f(z0) as finite NNReal t ->0'],
 'preferred_source_route':'Integrate actual82 phase-flow defect bound using bounded discrepancy<=2M indicator(D_t), then use actual hazard0 continuity and test/free-flow continuity. This mirrors source no-first-event split and exposes exact2M.',
 'alternative_route':'Actual82 convergence-in-probability plus continuity at z0 and global boundedness yields expected absolute difference convergence via eps/delta event split. No almost-sure convergence or naive samplewise dominated-convergence shortcut.',
 'smaller_options':[{'option':'Only integrability of f(Z_t)','assessment':'Necessary but alone too small to close real p6.2 pointwise gap; fold into actual expectation consumer.'},
 {'option':'Generic probability-to-bounded-test lemma only','assessment':'Potential reusable leaf, but cannot substitute for actual consumer. Requires actual instantiation within same bounded advance.'},
 {'option':'Only compactly supported continuous real tests','assessment':'Closest literal source class; bounded-continuous extension is conservative and useful, provided explicitly classified as ASTIS elaboration.'},
 {'option':'Immediately claim full L2 continuity','assessment':'Reject scope: outer-state DCT and operator equivalence-class/density/contraction/invariance obligations remain separate.'}],
 'dependency_readiness':'Source-level mathematically ready from actual82 defect probability and actual80 measurable probability realization plus actual harmonic/hazard continuity. Parent integration/compile status is root-reported context only, not newly verified here; no83 implementation inspected.',
 'genuine_delta_guard':'Retire if final theorem merely assumes the expected-value limit, arbitrary test integral bound, or arbitrary process stochastic-continuity certificates. Actual Z/P and integrability/estimate/limit must be derived via existing actual parents.',
 'remaining_gaps':{'outer_state_DCT':'Pointwise expectation difference squared measurable in z0 and dominated by4M^2 under exact normalized finite nu; needs actual integral-map measurability and outer dominated convergence.',
 'invariance_and_Jensen':'Source path reversal/invariance still required to establish L2 contraction, representative independence and bounded operators. No invariance needed for fixed-z0 clock expectation.',
 'density':'C_c dense in L2 and contraction extend to arbitrary L2 classes only after proper operators exist.',
 'Markov_semigroup':'Memoryless restart/conditional law, composition/ChapmanKolmogorov and time homogeneity not consequences of this limit.',
 'other':'Full reversal/path density/hypocoercivity, H_y invariance and actual composition/cost/main claims excluded.'},
 'boundary_cases':{'zero_threshold':'Raw zero waits allowed; actual input threshold positivity AE. At t0 use actual82 zero defect bound or retained AE initialization; no allraw Z0 claim.',
 'infinite_wait':'Initial/final infinite waiting time keeps last live finite-time arc; dummy stopped record never output phase.',
 'rank0':'Allowed singleton phase, tests constant on singleton; no positive-rank premise.',
 'exceptional_version':'Chosen uncovered z0 convention distinct from source failed-limit zero; under each fixed parameter AE actual coverage, integrals ignore that null exception. No uniform-parameter or arbitrary correlated random input substitution.',
 'boundedness':'Global boundM yields integrability on actual probability space and constant2M even for negative f; choose nonnegative M, M0 trivial. Unbounded continuous tests would need uniform integrability/moment bounds and are excluded.',
 'continuity':'Only limit at finite-time0 for fixed state/test; no Feller C0 preservation, continuity in initial state for positive time, uniformtime/state or full sample-path continuity.'},
 'no_statement_seal_or_proof':True,'no_SAU_or_VERIFIED_claim':True})
note=OWN/'source_preread83.md';assert not note.exists()
note.write_text('''# Source-only bounded-test preread83

The source Ex22/p6.1-p6.2 has a real next pointwise ingredient: for a fixed initial phase, the actual expectation of a bounded continuous real test tends to its initial value. This goes beyond82 by integrating an actual test; it must consume actual82 internally, not assume an abstract stochastic-continuity certificate.

Preferred route: with |f|<=M, integrate the actual phase-flow defect estimate to obtain |E f(Z_t)-f(Phi_t z0)|<=2M[1-exp(-Lambda_t)]. Continuity of f/Phi and Lambda0=0 close the smalltime limit. Measurability and integrability on the actual Exp probability input are derived. The alternative epsilon/delta route from convergence in probability is valid, but does not supply samplewise convergence for a direct clockwise DCT.

The paper uses C_c tests. Bounded continuous real tests are an explicit ASTIS extension of this pointwise step; the six original potential/scale hypotheses stay exact. No invariance is needed for the fixed-state clock expectation. Outer-state DCT for C_c L2 continuity, invariance/Jensen contraction, and density extension to all L2 remain separate. Markov/restart/semigroup, path regularity, ideal-kernel invariance, costs and composition remain OPEN.

All source anchors, edge ingredients and boundary conventions are frozen in the adjacent inventory/graph/candidate JSON. No proposed83 statement or Lean was read, no theorem or verification credit is claimed, and no shared state was changed.
''',encoding='utf8',newline='\n')
seal=save('source_freeze83.seal.json',{'schema':'source-first-freeze-seal-v1','created_utc':now,'primary':raw(PRIMARY),
 'outputs':[raw(x)for x in [inv,graph,candidate,note]],'inventory_count':len(items),'node_count':len(nodes),'edge_count':len(edges),
 'chronology':'Pinned primary read and independently parsed before new83 candidate graph; no proposed83 Lean/statement/header/proof or other source/reviewer verdict inspected.',
 'status':'prospective-source-only-frozen','no_shared_writes':True,'no_proof_or_verification_credit':True})
outputs=[Path(__file__).resolve(),inv,graph,candidate,note,seal]
manifest=save('source_freeze83.raw-manifest.json',{'schema':'noncircular-source-first-raw-manifest-v1','created_utc':now,'raw_inputs':[raw(PRIMARY)],
 'raw_outputs':[raw(x)for x in outputs],'self_hash_omitted':True,'status':'closed-source-only-preread',
 'independence':'Source mathematical content comes solely from exact pinned primary; administrative skill/memory routing reads supplied no mathematical premise or prior verdict. No proposed83 implementation exists in this read set.'})
for b in json.loads(manifest.read_text('utf8'))['raw_inputs']+json.loads(manifest.read_text('utf8'))['raw_outputs']:assert sha(Path(b['path']))==b['raw_sha256']
print(json.dumps({'status':'closed-source-only','counts':[len(items),len(nodes),len(edges)],'outputs':[raw(x)for x in outputs+[manifest]]},indent=2))
