"""Owned SOURCE-ONLY preread; never loads any candidate84 implementation or verdict."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, datetime

ROOT = Path('E:/Samplinglib')
OUT = Path(__file__).resolve().parent
PRIMARY = 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
PRIMARY_SHA = 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(rel):
    p = ROOT / rel
    b = p.read_bytes()
    return {'path': rel, 'raw_sha256': sha(b), 'bytes': len(b)}
assert pin(PRIMARY)['raw_sha256'] == PRIMARY_SHA

class SourceHTML(HTMLParser):
    void = {'br','hr','meta','link','img','input','source','wbr','area','base','col','embed','param','track'}
    def __init__(self):
        super().__init__(); self.stack=[]; self.text={}; self.math=0
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag not in self.void: self.stack.append((tag,a.get('id')))
        if tag=='math':
            self.math+=1
            if self.math==1:
                for _, i in self.stack:
                    if i: self.text.setdefault(i,[]).append(a.get('alttext',''))
    def handle_endtag(self,tag):
        if tag=='math': self.math-=1
        for k in range(len(self.stack)-1,-1,-1):
            if self.stack[k][0]==tag:
                self.stack=self.stack[:k]; break
    def handle_data(self,s):
        if not self.math:
            for _, i in self.stack:
                if i: self.text.setdefault(i,[]).append(s)
    def normalized(self,i):
        return ' '.join(' '.join(self.text[i]).split())

h=SourceHTML(); h.feed((ROOT/PRIMARY).read_text(encoding='utf-8'))
anchor_ids=['license-tr','infobox','S1.p1.1','S1.E1','S2.SS2.p1.1','S2.E8','S2.E9',
 'S3.E1','S3.Thmtheorem1','A1.Ex1','A1.Ex2','A1.Ex3','A1.E1','A1.E2',
 'A1.SS1.p1.1','A1.SS1.p2.1','A1.SS1.p2.2','A1.SS1.p3.1','A1.SS1.p3.6','A1.SS1.p3.7',
 'A1.Thmtheorem1','A1.SS1.SSS0.Px1.p6.1','A1.Ex22','A1.SS1.SSS0.Px1.p6.2',
 'A1.SS2.p3.1','A1.SS2.p4.1']
anchors=[{'source_id': i, 'normalized_anchor_sha256':sha(h.normalized(i).encode('utf-8')),
          'raw_authority':PRIMARY, 'normalization':'stdlib HTMLParser; math alttext once; whitespace collapsed'} for i in anchor_ids]
assert 'perpetual non-exclusive' in h.normalized('license-tr')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()

items=[]
def I(num,title,kind,ids,content,nodes):
    items.append({'id':f'I84-{num:02d}','title':title,'classification':kind,'source_ids':ids,
                  'content':content,'graph_nodes':nodes})
I(1,'Pinned source and license','SOURCE_CONTEXT',['license-tr','infobox'],
 'Chen/Chewi/Lu/Zhang arXiv2609.06905v1, perpetual non-exclusive arXiv license. Exact raw remains authoritative; this freeze contains paraphrases/minimal formulas only.',[])
I(2,'Phase space and fixed parameters','SOURCE_WITH_ASTIS_GENERALIZATION',['S3.E1','A1.SS1.p1.1'],
 'Source R^d x R^d, fixed y and reference r. ASTIS finite real inner-product Borel space E, including rank0. No randomized parameter binder or uniform-parameter null set.', ['G84-01','G84-02'])
I(3,'Positive lower curvature','SOURCE_ASSUMPTION',['S1.p1.1','S1.E1'],'0 < alpha, genuine positive scalar; no zero-curvature substitution.', ['G84-01','G84-06'])
I(4,'Curvature order','SOURCE_ASSUMPTION',['S1.p1.1','S1.E1'],'alpha <= beta.', ['G84-01'])
I(5,'Regularity','SOURCE_ASSUMPTION',['S1.p1.1'],'V is C^2 everywhere.', ['G84-01','G84-06'])
I(6,'Both Hessian inequalities','SOURCE_ASSUMPTION',['S1.E1'],'For all x,v: alpha||v||^2 <= D^2V(x)[v,v] <= beta||v||^2.', ['G84-01','G84-06'])
I(7,'Positive proximal scale','SOURCE_ASSUMPTION',['S2.SS2.p1.1'],'0 < eta.', ['G84-01','G84-07','G84-08'])
I(8,'Upper scale','SOURCE_ASSUMPTION',['S2.SS2.p1.1'],'beta*eta <=1. Retain all six original analytic binders even where a normalization subproof needs fewer.', ['G84-01'])
I(9,'Conditional potential','SOURCE_DEFINITION',['S2.E9'],'V_y(x)=V(x)+||x-y||^2/(2eta).', ['G84-07','G84-08','G84-09'])
I(10,'Exact conditional position law','SOURCE_DEFINITION',['S2.E8'],
 'q_y = volume.tilted(-V(x)-||x-y||^2/(2eta)); normalized exact conditional Gibbs law, not unnormalized density, arbitrary law, or approximate sampler q-hat.', ['G84-07','G84-08','G84-09'])
I(11,'Actual outer phase law','SOURCE_DEFINITION',['S3.E1'],
 'nu_eta,y = q_y.prod(stdGaussian E). Position and momentum independent; phase density proportional to exp(-V_y(x)-||p||^2/2). Reference r does not enter nu.', ['G84-10','G84-11'])
I(12,'Harmonic flow','SOURCE_DEFINITION',['A1.Ex2'],
 'c=y-eta grad V(r); Phi_t(x,p)=(c+cos(t)(x-c)+sqrt(eta)sin(t)p, -sin(t)/sqrt(eta)(x-c)+cos(t)p). Phi_0=id.', ['G84-02'])
I(13,'Bounce with vanishing normal','SOURCE_DEFINITION',['A1.Ex3'],
 'h_r(x)=grad V(x)-grad V(r); bounce reflects momentum, R_0=I. ASTIS total division by zero agrees with identity normal convention.', ['G84-02'])
I(14,'Rate and hazard','SOURCE_DEFINITION',['A1.Ex1','A1.E1','A1.Ex22'],
 'rate=sqrt(eta)[<p,h_r(x)>]_+; Lambda_t(z)=integral_0^t rate(Phi_s z)ds.', ['G84-02','G84-04'])
I(15,'Actual clock law','SOURCE_DEFINITION',['A1.SS1.p2.1'],
 'Independent iid Exp(1), canonical infinite product P; Real.toNNReal coordinate adapter. ASTIS zero-index e_n corresponds to source E_(n+1). P is derived probability, not a supplied arbitrary clock law.', ['G84-02'])
I(16,'Threshold wait','SOURCE_DEFINITION',['A1.E1'],
 'Wait is inf{u>=0: Lambda_u >= E_(n+1)}; empty set gives infinite wait, not an undefined finite value.', ['G84-02'])
I(17,'Initialized actual recursion','SOURCE_DEFINITION',['A1.E2','A1.SS1.p2.1','A1.SS1.p2.2'],
 'Start live at (0,z0), add finite wait then bounce flowed state. Infinite wait stops subsequent records; stopped dummy carries no physical phase.', ['G84-02'])
I(18,'Physical interpolation','SOURCE_DEFINITION',['A1.SS1.p2.2'],
 'Half-open arcs T_n<=t<T_(n+1), local elapsed t-T_n>=0. Last live record with infinite next wait covers every later finite time; do not discard it with stopped dummy.', ['G84-02','G84-03'])
I(19,'Nonaccumulation prerequisite','SOURCE_INGREDIENT_ALREADY_PARENT',['A1.SS1.p3.1','A1.SS1.p3.6','A1.SS1.p3.7'],
 'Energy/cap/wait comparison and direct iid Exp mean1/SLLN give nonaccumulation; stopped alternative included. This84 does not reprove it or substitute a new global process claim.', ['G84-02','G84-03'])
I(20,'Joint measurable actual version','SOURCE_IMPLICIT_ASTIS_PARENT',['A1.SS2.p3.1','A1.SS1.p2.2'],
 'Source proves Borel terminal version at pi. Existing actual80/82/83 elaborates joint fixed-parameter/phase/finite-time/clock map and actual live-arc semantics; needed for state-parameter expectation measurability.', ['G84-03','G84-12','G84-13'])
I(21,'Exceptional convention and initialization','SOURCE_WITH_EXPLICIT_ADAPTER',['A1.SS2.p3.1','A1.SS1.p2.1'],
 'Source failed terminal-limit convention is zero. ASTIS uncovered-arc fallback z0 differs only on exceptional clock outcomes for each fixed y,r,z0, and retains AE initialization and common AE all finite times for those fixed parameters.', ['G84-03'])
I(22,'First-event source estimate','SOURCE_DIRECT',['A1.SS1.SSS0.Px1.p6.1','A1.Ex22'],
 'No-first-event branch is Phi_t z; event probability 1-exp(-Lambda_t z) tends0 as t decreases0. Existing82 supplies actual measurable defect inequality, including infinite wait and zero-threshold null exceptions.', ['G84-04'])
I(23,'Actual fixed-state clock expectation producer','EXISTING_PARENT_ASTIS_ELABORATION',['A1.Ex22','A1.SS1.SSS0.Px1.p6.1'],
 'actual83 derives inner measurability/integrability, explicit 2M first-event expectation defect and A_t f(z)->f(z) at ordinary NNReal nhds0 for every fixed y,r,z and bounded continuous real f. Consume actual83 internally, not assume an arbitrary process/convergence premise.', ['G84-04','G84-16'])
I(24,'Literal source test class','SOURCE_DIRECT',['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2'],
 'The source uses C_c(R^(2d)); compact support gives a finite global bound. Its DCT paragraph is the real outer L2 consumer.', ['G84-18'])
I(25,'Bounded continuous test extension','ASTIS_ELABORATION',['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2'],
 'ASTIS C_b real-valued extension: Continuous f and any real M>=0 with every z |f(z)|<=M. Bound/continuity define test class, not extra dynamics hypotheses. Includes M=0.', ['G84-05'])
I(26,'Pointwise expectation definition','ASTIS_EXPLICIT_DEFINITION',['A1.Ex22','A1.Thmtheorem1'],
 'A_t f(z)=integral_clock f(Z(y,r,z,t,clock)) dP. Pointwise representatives before any L2 equivalence-class operator. Fixed deterministic y,r only.', ['G84-12','G84-13','G84-14'])
I(27,'Parameterized expectation measurability','ASTIS_MEASURE_THEORY_INGREDIENT',['A1.SS2.p3.1','A1.SS2.p4.1'],
 'Joint measurability of actual Z and continuous real f gives joint strong measurability; SFinite probability P allows integral_prod_right, so z->A_t f(z) is measurable each finite t. This is a real added consumer of actual joint measurability.', ['G84-12','G84-13'])
I(28,'Base Gibbs mass derived','EXISTING_BACKGROUND_INGREDIENT',['S1.p1.1','S1.E1'],
 'Positive Hessian lower bound/C^2 => strong convexity => Gaussian quadratic envelope => integral exp(-V) finite and positive. Existing GibbsAugmentation/StrongConvexGibbsIntegrability derive mu=volume.tilted(-V) probability without assumed minimizer or normalization.', ['G84-06'])
I(29,'Preferred exact conditional normalization route','EXISTING_BACKGROUND_ROUTE',['S2.E8'],
 'Apply GaussianConditionalKernel to derived base mu probability, obtain everywhere probability quadratic tilt R_y; tilted_tilted with exp(-V) integrability identifies R_y=q_y. Kernel Markov here means normalized fibers only, not actual phase-process Markov.', ['G84-07','G84-09'])
I(30,'Alternative direct conditional normalization route','OPTIONAL_BACKGROUND_ROUTE',['S2.E8','S2.E9'],
 'exp(-V-quadratic)<=exp(-V), with joint continuity and eta>0, yields integrability and positive q normalizer; isProbabilityMeasure_tilted then q_y probability. This complete route is OR with preferred route, never additional AND requirement.', ['G84-08','G84-09'])
I(31,'Gaussian normalization','EXISTING_BACKGROUND_INGREDIENT',['S3.E1'],
 'stdGaussian E probability from finite product of standard real Gaussians and measurable orthonormal-basis transport, valid rank0; covariance identity, no eta scaling in momentum.', ['G84-10'])
I(32,'Outer product and clock independence','SOURCE_WITH_ASTIS_EXPLICIT_PRODUCT',['S3.E1','A1.SS1.p2.1','A1.SS2.p4.1'],
 'nu_y=q_y.prod gamma is probability, clocks independently P if an initialized interpretation is made: nu_y.prod P. Iterated expectation does not license arbitrary correlated phase-clock law.', ['G84-11'])
I(33,'Inner integrability is derived','EXISTING_PARENT_AND_BOUND',['A1.SS1.SSS0.Px1.p6.1'],
 'For every state/time, actual83 bounded-test integrability under true P; not assumed as public premise and not integral_undef zero.', ['G84-04','G84-14'])
I(34,'Expectation absolute bound','ASTIS_INGREDIENT',['A1.SS1.SSS0.Px1.p6.2'],
 'P probability + true integrability + |f|<=M => |A_t f(z)|<=M, hence |A_t f(z)-f(z)|<=2M.', ['G84-14'])
I(35,'Squared discrepancy measurability','ASTIS_INGREDIENT',['A1.SS1.SSS0.Px1.p6.2'],
 'g_t(z)=(A_t f(z)-f(z))^2 measurable by expectation measurability, continuous f and real square.', ['G84-15'])
I(36,'Finite outer domination','ASTIS_INGREDIENT',['S3.E1','A1.SS1.SSS0.Px1.p6.2'],
 '0<=g_t(z)<=4M^2; constant 4M^2 integrable under derived probability nu_y. Neither invariance nor Jensen contraction needed for this domination.', ['G84-15','G84-17'])
I(37,'Pointwise squared limit','ASTIS_INGREDIENT',['A1.Ex22','A1.SS1.SSS0.Px1.p6.2'],
 'Actual83 A_t f(z)->f(z), every fixed state; continuity of subtraction/square yields g_t(z)->0. No almost-sure pathwise convergence is inferred from convergence in probability.', ['G84-16'])
I(38,'Outer filter dominated convergence','SOURCE_DCT_WITH_ASTIS_FILTER_ADAPTER',['A1.SS1.SSS0.Px1.p6.2'],
 'Ordinary NNReal nhds0 is countably generated. Measurable g_t, uniform integrable constant and every-state limit imply integral g_t dnu_y ->0 via filter DCT.', ['G84-17'])
I(39,'Squared discrepancy outer integrability','ASTIS_INGREDIENT',['A1.SS1.SSS0.Px1.p6.2'],
 'Each g_t integrable under nu_y by measurable bounded domination, making squared L2 discrepancy integral genuine.', ['G84-15'])
I(40,'Time and initialization boundary','SOURCE_WITH_ASTIS_ADAPTER',['A1.SS1.p2.1','A1.Ex22'],
 'All finite times NNReal, nonpunctured nhds0 limit includes0; fixed-state AE initialization gives A_0 f(z)=f(z). No real negative-time, uniform-in-time, positive-time Feller or path continuity conclusion.', ['G84-03','G84-16','G84-17'])
I(41,'Degenerate cases preserved','SOURCE_WITH_ASTIS_ADAPTER',['A1.Ex3','A1.E1','A1.SS1.p2.2'],
 'Rank0, M0, zero normal, zero hazard/cap, infinite first/last wait, zero raw thresholds and stopped dummy retain parent semantics. Strictly positive iid Exp thresholds AE; no positive wait/cap assumed for every raw clock.', ['G84-02','G84-03'])
I(42,'Quantifier and correlation boundary','EXCLUDED_OPEN',['A1.SS2.p3.1','A1.SS2.p4.1'],
 'No uniform-parameter AE set, arbitrary correlated random initialization substitution, random y/reference, or full initialized all-time path law/version-uniqueness theorem. Independent nu_y x P only.', ['G84-22'])
I(43,'Invariance and Jensen','SOURCE_OPEN_BEYOND_CANDIDATE',['A1.Thmtheorem1','A1.SS1.SSS0.Px1.p6.1'],
 'Source invariance+Jensen establish contraction. This84 bounded outer DCT uses only finite actual nu; normalization does not establish invariance. Full contraction stays OPEN.', ['G84-20'])
I(44,'L2 representatives/operator','OPEN_BEYOND_CANDIDATE',['A1.Thmtheorem1'],
 'No well-defined bounded operator on L2 equivalence classes from this real pointwise test map alone; AE-representative preservation and full integrability/contraction require separate work.', ['G84-19'])
I(45,'Density and all L2 extension','SOURCE_OPEN_BEYOND_CANDIDATE',['A1.SS1.SSS0.Px1.p6.2'],
 'Source C_c density plus contraction extends strong continuity to all L2. Candidate closes only bounded representative squared-discrepancy ingredient; not this density argument.', ['G84-21'])
I(46,'Global process and semigroup','EXCLUDED_OPEN',['S3.Thmtheorem1','A1.Thmtheorem1'],
 'Restart/Markov/time-homogeneity/Chapman-Kolmogorov/path reversal/invariance/semigroup/hypocoercivity/full L2 remain OPEN; no inference from bounded L2 limit to any of them.', ['G84-22'])
I(47,'Ideal auxiliary kernel and costs','EXCLUDED_OPEN',['A1.SS2.p4.1','S3.Thmtheorem1'],
 'Existing ideal H_y and exact reference law are distinct from implemented approximate reference sampler; candidate has no sampler production, Algorithm1 query costs, main mixing result, SPHMC or multi-paper composition claim.', ['G84-22'])

nodes=[]
def N(n,title,status,formula='',kind='DEPENDENCY'):
    nodes.append({'id':f'G84-{n:02d}','title':title,'status':status,'kind':kind,'formula_or_contract':formula})
N(1,'Six analytic conditions and deterministic parameters','SOURCE_CONTRACT','0<alpha; alpha<=beta; C2; two-sided Hessian; 0<eta; beta eta<=1')
N(2,'Literal actual clock construction','EXISTING_PARENT','P iidExp1; Phi/S/rate/Lambda/tau/next/record/eventTime; initialized live half-open finite-time arcs')
N(3,'Actual joint measurable phase and fixed-parameter AE initialization','EXISTING_PARENT','Z jointly measurable; every fixed y,r,z common AE all finite t live-arc coverage and Z_0=z; uncovered fallback z')
N(4,'Actual83 fixed-state bounded-test expectation limit','EXISTING_PARENT','inner integrability; |A_t f(z)-f(Phi_t z)|<=2M(1-exp(-Lambda_t z)); A_t f(z)->f(z)')
N(5,'Continuous bounded real test','TEST_CLASS','Continuous f; M>=0; forall z |f(z)|<=M; source C_c specializes')
N(6,'Base Gibbs integrability and genuine normalization','EXISTING_PARENT_ROUTE','0<integral exp(-V)<infinity; mu=volume.tilted(-V) probability')
N(7,'Conditional-kernel exact quadratic tilt route','DEPENDENCY_READY_ROUTE','GaussianConditionalKernel(mu,eta) + tilted_tilted => q_y probability; preferred')
N(8,'Direct quadratic-density domination route','OPTIONAL_ALTERNATIVE_ROUTE','exp(-V-quadratic)<=exp(-V) => positive integrable exact tilt')
N(9,'Exact conditional Gibbs law normalized','PROSPECTIVE_INTEGRATION','q_y=volume.tilted(-V-quadratic) probability; G07 OR G08')
N(10,'Actual standard Gaussian momentum probability','EXISTING_PARENT','gamma=stdGaussian E; no eta scale; rank0 allowed')
N(11,'Actual normalized outer phase product','PROSPECTIVE_INTEGRATION','nu_y=q_y.prod gamma probability; independent phase/clocks nu_y.prod P only')
N(12,'Joint state-clock tested phase measurable','PROSPECTIVE_INGREDIENT','(z,clock)->f(Z(y,r,z,t,clock)) jointly strongly measurable')
N(13,'State-clock-expectation map measurable','PROSPECTIVE_INGREDIENT','z->A_t f(z) measurable for each NNReal t')
N(14,'Clock expectation bounded by test bound','PROSPECTIVE_INGREDIENT','|A_t f(z)|<=M')
N(15,'Squared discrepancy measurable integrable dominated','PROSPECTIVE_INGREDIENT','g_t=(A_t f-f)^2; measurable; integrable(nu_y); 0<=g_t<=4M^2')
N(16,'Every-state squared discrepancy tends zero','PROSPECTIVE_INGREDIENT','forall z, g_t(z)->0 at NNReal nhds0')
N(17,'Outer bounded-square filter DCT','PROSPECTIVE_CANDIDATE','integral g_t(z) dnu_y ->0 at NNReal nhds0')
N(18,'Literal C_c source consumer specialization','PROSPECTIVE_SCOPE','C_c tests are bounded; bounded squared-integral convergence supplies source p6.2 DCT ingredient')
N(19,'Well-defined L2 equivalence-class transition operator','OPEN','AE representative preservation, operator-domain/integrability contracts not supplied here')
N(20,'True phase invariance and Jensen contraction','OPEN','nu invariant + Jensen => ||T_t F||_2<=||F||_2')
N(21,'Density and all-L2 strong continuity','OPEN','C_c density + genuine L2 contraction/operator + C_c continuity')
N(22,'Global process/law/cost and correlated-input boundary','EXCLUDED_OPEN','Markov/restart/semigroup/path reversal/invariance/main/cost/composition and arbitrary correlation remain unclaimed','BOUNDARY')

edges=[]
def E(a,b,ingredient,route='MAIN',group=None,dep=True,status='DEPENDENCY_READY'):
    edges.append({'id':f'E84-{len(edges)+1:02d}','from':f'G84-{a:02d}','to':f'G84-{b:02d}',
       'ingredient':ingredient,'route':route,'junction_group':group,'dependency_edge':dep,'status':status})
E(1,2,'All six source dynamics binders preserved')
E(2,3,'Actual finite-time nonaccumulating live-arc producer and stopped alternative')
E(1,3,'Regularity and literal parameters for measurable actual realization')
E(3,4,'Actual82 measurable first-event defect and parent83 expectation producer')
E(5,4,'Continuous globally bounded real test, M>=0')
E(1,6,'Only positive lower curvature/C2 used by Gibbs normalization subproof')
E(6,7,'Derived base Gibbs probability and exp(-V) integrability','NORMALIZE_CONDITIONAL', 'NORMALIZE_KERNEL_AND')
E(1,7,'eta>0; exact quadratic scale','NORMALIZE_CONDITIONAL','NORMALIZE_KERNEL_AND')
E(6,8,'Base Gibbs integrable domination','NORMALIZE_DIRECT','NORMALIZE_DIRECT_AND')
E(1,8,'eta>0 and continuous exact weighted density','NORMALIZE_DIRECT','NORMALIZE_DIRECT_AND')
E(7,9,'Complete conditional-kernel/tilt identification route','NORMALIZE_CONDITIONAL','NORMALIZE_OR')
E(8,9,'Complete direct density route, optional alternative','NORMALIZE_DIRECT','NORMALIZE_OR')
E(9,11,'Exact normalized q_y','MAIN','PHASE_PRODUCT_AND')
E(10,11,'Standard Gaussian probability','MAIN','PHASE_PRODUCT_AND')
E(3,12,'Actual joint measurable Z','MAIN','TESTED_JOINT_AND')
E(5,12,'Continuous real f is Borel and strongly measurable','MAIN','TESTED_JOINT_AND')
E(12,13,'StronglyMeasurable.integral_prod_right','MAIN','PARAM_INTEGRAL_AND')
E(2,13,'Actual P probability => SFinite; finite-time clock slice','MAIN','PARAM_INTEGRAL_AND')
E(2,14,'Actual P probability','MAIN','INNER_BOUND_AND')
E(4,14,'Actual test integrability, avoiding undefined-integral shortcut','MAIN','INNER_BOUND_AND')
E(5,14,'Global abs f<=M with nonnegative M','MAIN','INNER_BOUND_AND')
E(13,15,'Expectation measurability','MAIN','SQUARE_AND')
E(5,15,'f measurable and bounded','MAIN','SQUARE_AND')
E(14,15,'Triangle inequality yields |A_t f-f|<=2M','MAIN','SQUARE_AND')
E(11,15,'Finite probability nu gives integrable constant 4M^2','MAIN','SQUARE_AND')
E(4,16,'Actual83 every-state expectation convergence','MAIN','POINTWISE_SQUARE_AND')
E(5,16,'Fixed f(z); continuity of real subtraction/square','MAIN','POINTWISE_SQUARE_AND')
E(15,17,'All-time measurable g_t and constant domination','MAIN','OUTER_DCT_AND')
E(16,17,'Every-state pointwise limit implies AE outer limit','MAIN','OUTER_DCT_AND')
E(11,17,'Exact probability outer law; no invariance premise','MAIN','OUTER_DCT_AND')
E(17,18,'Bounded-subclass squared-integral convergence','MAIN','SOURCE_CC_AND')
E(5,18,'Compactly supported continuous source tests are bounded','MAIN','SOURCE_CC_AND')
E(20,19,'Future true invariance supports AE-representative/operator well-definedness','FUTURE_OPEN',None,True,'OPEN_NOT_USED')
E(18,21,'Future C_c continuity ingredient only','FUTURE_OPEN','ALL_L2_AND',True,'OPEN_NOT_USED')
E(19,21,'Future well-defined L2 operator','FUTURE_OPEN','ALL_L2_AND',True,'OPEN_NOT_USED')
E(20,21,'Future invariance/Jensen contraction; plus independent C_c density theorem','FUTURE_OPEN','ALL_L2_AND',True,'OPEN_NOT_USED')
E(11,22,'Normalization is not phase invariance or process Markov; exclusion association only','EXCLUDED_BOUNDARY',None,False,'EXCLUDED_BOUNDARY_ASSOCIATION')
E(17,22,'Bounded outer L2 limit implies no Markov/restart/global law/cost conclusion','EXCLUDED_BOUNDARY',None,False,'EXCLUDED_BOUNDARY_ASSOCIATION')
junctions=[
 {'id':'NORMALIZE_KERNEL_AND','operation':'AND','edges':['E84-07','E84-08'],'background':['GaussianConditionalKernel.exists_tilted_isCondKernel','MeasureTheory.tilted_tilted']},
 {'id':'NORMALIZE_DIRECT_AND','operation':'AND','edges':['E84-09','E84-10'],'background':['positive exponential weighted density','MeasureTheory.isProbabilityMeasure_tilted']},
 {'id':'NORMALIZE_OR','operation':'OR','edges':['E84-11','E84-12'],'note':'Each incoming route is complete; direct route optional, not an additional required premise.'},
 {'id':'PHASE_PRODUCT_AND','operation':'AND','edges':['E84-13','E84-14']},
 {'id':'TESTED_JOINT_AND','operation':'AND','edges':['E84-15','E84-16']},
 {'id':'PARAM_INTEGRAL_AND','operation':'AND','edges':['E84-17','E84-18']},
 {'id':'INNER_BOUND_AND','operation':'AND','edges':['E84-19','E84-20','E84-21']},
 {'id':'SQUARE_AND','operation':'AND','edges':['E84-22','E84-23','E84-24','E84-25']},
 {'id':'POINTWISE_SQUARE_AND','operation':'AND','edges':['E84-26','E84-27']},
 {'id':'OUTER_DCT_AND','operation':'AND','edges':['E84-28','E84-29','E84-30'],'background':['NNReal nhds0 countably generated','filter dominated convergence']},
 {'id':'SOURCE_CC_AND','operation':'AND','edges':['E84-31','E84-32']},
 {'id':'ALL_L2_AND','operation':'AND_OPEN','edges':['E84-34','E84-35','E84-36'],'background':['independent C_c density; not yet credited'],'note':'Not traversed in candidate84.'}]

inputs=[PRIMARY,
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedTestContinuity.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean',
 'AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGibbsIntegrability.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean']
raw_inputs=[pin(p) for p in inputs]
assert raw_inputs[1]['raw_sha256']=='0a88a2071df983f791899b01b0de40f52241b06ba452eea3751e471396adec6b'
independence={'role':'independent source-only prospective extractor; not proving owner',
 'source_first':True,'first_read_this_edge':PRIMARY,'candidate84_read':False,'candidate84_constructed':False,
 'prior_source_or_math_verdicts_used_as_source_evidence':False,
 'allowed_background':'Existing exact producer/API statements and bodies, after primary source; no proposed84 implementation or review.',
 'state_credit':'none; prospective only; no SAU/proof/verification transition',
 'writes':'owned pbps-outer-bounded-l2-preread84 only',
 'chronology':'Primary RAW verified/read first this84 turn, including source p6.1/Ex22/p6.2 and actual q/phase law; then existing exact normalization/measurability/DCT APIs inspected; source inventory/topology frozen before any84 header or proof.'}
inventory={'schema':'astis.source-only-inventory84.v1','created_utc':now,'primary':raw_inputs[0],
 'license':{'anchor':'license-tr','normalized_text':h.normalized('license-tr'),
            'normalized_text_sha256':sha(h.normalized('license-tr').encode()),
            'reproduction_policy':'No whole rawsource copy; short formulas/paraphrases in owned prospective artifacts only.'},
 'scope':'Actual finite-clock-expectation measurability and bounded-continuous-test outer squared discrepancy under exact normalized conditional phase law.',
 'source_anchor_coverage':anchors,'inventory_count':len(items),'items':items,'independence':independence}
graph={'schema':'astis.source-only-proof-graph84.v1','created_utc':now,'nodes':nodes,'edges':edges,'junctions':junctions,
 'counts':{'inventory':len(items),'nodes':len(nodes),'relations':len(edges),
           'dependency_edges':sum(e['dependency_edge'] for e in edges),
           'excluded_associations':sum(not e['dependency_edge'] for e in edges)},
 'topology_contract':'Ingredient is a dependency edge; optional complete normalization routes join by OR, simultaneous proof ingredients by AND; exclusion associations are not dependencies. OPEN future source edges carry no candidate credit.',
 'scope_coverage':[{'inventory_id':i['id'],'graph_nodes':i['graph_nodes'],
                    'disposition':'LICENSE_CONTEXT' if not i['graph_nodes'] else i['classification']} for i in items],
 'source_boundary':'Full source PropositionA.1 remains OPEN; only bounded representative DCT ingredient proposed.'}
candidate={'schema':'astis.prospective-source-candidate84.v1','created_utc':now,'status':'SOURCE_ONLY_FROZEN_NO_HEADER_NO_PROOF',
 'candidate':'Actual clock-expectation state measurability and outer bounded-test squared-integral convergence',
 'actual_source_reason':{'anchors':['S2.E8','S3.E1','A1.SS1.SSS0.Px1.p6.1','A1.Ex22','A1.SS1.SSS0.Px1.p6.2'],
   'missing_consumer':'Actual83 closes fixed-state clock expectation; source p6.2 still needs integration of its squared discrepancy over the actual phase law. This candidate derives that outer step and the state measurability making the integral legitimate.'},
 'objects':{'q_y':'volume.tilted(x -> -V(x)-||x-y||^2/(2eta))',
   'gamma':'stdGaussian E','nu_y':'q_y.prod gamma','P':'infinitePi(Exp1)',
   'A_t_f_z':'integral_clock f(Z(y,r,z,t,clock)) dP',
   'squared_discrepancy':'g_t(z)=(A_t f(z)-f(z))^2'},
 'retained_contract':'All six analytic source binders, literal eleven actual definitions, joint Z measurability, half-open arc clause, uncovered-z0 fallback, fixed-parameter AE all finite times/init, measurable actual defect/tail and all83 bounded-test clauses.',
 'prospective_new_conclusions':[
   'For each fixed deterministic y,r and finite NNReal t, state z -> A_t f(z) is measurable.',
   'For every continuous real f and every M>=0 with global |f|<=M, every finite t squared discrepancy is integrable under derived exact nu_y.',
   'For each such fixed y,r,f,M, integral_z (A_t f(z)-f(z))^2 dnu_y tends0 at ordinary NNReal nhds0.' ],
 'proof_ingredient_contract':[
   'Consume actual83 internally; do not supply arbitrary-process pointwise convergence/integrability as premises.',
   'Derive q_y probability from true strong-convex Gibbs integrability and exact conditional tilt; derive gamma and nu_y probability. Do not accept a supplied law/normalizer premise.',
   'Joint measurable actual phase + continuous real test + SFinite P => measurable parameterized expectation.',
   'P probability and bounded integrable test => |A_t f|<=M => squared discrepancy <=4M^2.',
   'Actual83 every-state expectation limit => every-state squared limit; derived nu_y probability makes constant 4M^2 integrable.',
   'Use filter DCT for countably-generated NNReal nhds0. No AS-DCT shortcut from stochastic continuity.' ],
 'normalization_routes':{'preferred':'derived base mu probability -> GaussianConditionalKernel -> tilted_tilted identification -> actual q_y probability',
   'optional_alternative':'direct continuous weighted density dominated by exp(-V), positive integrable normalizer -> exact tilt probability',
   'junction':'OR between complete routes; both retain exact eta and q_y'},
 'source_vs_extension':'Source uses C_c(R^(2d)); bounded C_b real tests with explicit nonnegative M are a valid ASTIS elaboration because outer law is a derived finite probability. This does not extend to arbitrary L2 tests.',
 'readiness':{'mathematical_status':'DEPENDENCY_READY_PROSPECTIVE',
   'invariant_law_required':False,
   'reason':'Bounded outer DCT needs actual finite probability nu_y, not stationarity. Source invariance/Jensen enter contraction and full L2 density extension separately.',
   'existing_parents':['ActualBoundedTestContinuity.actual_bounded_test_expectation_continuity',
      'GibbsAugmentation.normalized_augmentation_density',
      'StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn',
      'GaussianConditionalKernel.exists_tilted_isCondKernel',
      'MeasureTheory.tilted_tilted','MeasureTheory.isProbabilityMeasure_tilted',
      'ProbabilityTheory.isProbabilityMeasure_stdGaussian',
      'MeasureTheory.StronglyMeasurable.integral_prod_right',
      'MeasureTheory.tendsto_integral_filter_of_dominated_convergence'],
   'normalization_visibility':'IdealHalfTurnKernel BODY already derives same exact q normalization, but private local facts are not new callable exports. Reuse public Gibbs/conditional-kernel APIs and derive identification; do not assume a private proof-local witness as theorem API.',
   'no_new_proof_claim':True},
 'smaller_options':[{'option':'State-expectation measurability only','assessment':'Valid but omits real source p6.2 consumer; combine with bounded outer DCT as one bounded integration edge.'},
   {'option':'Direct no-first-event bound integrated in state','assessment':'Possible after exact nu normalization; pointwise actual83 plus constant DCT is smaller and uses real compiled producer without repeating82/83.'},
   {'option':'Generic convergence-in-probability to bounded-expectation theorem','assessment':'Actual83 already closes inner step; no need repeat or use AS-DCT.'},
   {'option':'All-L2 strong continuity now','assessment':'Not dependency-ready: true contraction, AE-representative operator/domain and density remain separate OPEN obligations.'}],
 'excluded_open':['arbitrary correlated phase-clock initialization','random y or reference substitution/uniform-parameter AE',
   'full initialized all-time path law and version uniqueness','L2 equivalence-class transition operator',
   'true phase invariance/Jensen contraction','all-L2 density extension','Markov/restart/semigroup/Chapman-Kolmogorov',
   'path reversal/hypocoercivity/main mixing','implemented reference sampler and query costs','SPHMC and full four-paper composition'],
 'boundary_checks':['rank0 allowed','M=0 allowed','zero normal R0=I','zero hazard/cap and infinite wait allowed',
   'zero raw thresholds not excluded pointwise; actual Exp positive AE','stopped dummy has no phase; last live infinite arc retained',
   'time0 included by AE initialization; no negative/punctured-only time','no process invariance inferred from normalized phase probability'],
 'independence':independence}

def emit(name,data):
    p=OUT/name
    assert not p.exists(), f'Frozen file already exists: {p}'
    p.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
emit('source_inventory84.json',inventory)
emit('source_proof_graph84.json',graph)
emit('bounded_candidate84.json',candidate)
note='''# Prospective PBPS bounded outer-state L2 ingredient84

Source-only extraction, before any84 header/proof. The pinned primary is the authority; no theorem admission or verification is claimed.

For fixed deterministic y,r, use the actual83 phase Z and iid Exp1 clock probability P. Write A_t f(z)=integral f(Z(y,r,z,t,clock)) dP. The next real source consumer is AppendixA.1 p6.2: integrate the squared error of this pointwise clock expectation over the actual phase law nu_y=q_y x N(0,I). Source tests are C_c; the bounded real C_b extension with M>=0 is explicit ASTIS elaboration.

Joint actual-phase measurability makes z -> A_t f(z) measurable at each finite time. True P-probability and global |f|<=M give |A_t f|<=M, hence squared discrepancy <=4M^2. Actual83 supplies its every-state zero-time limit. Derive exact q_y normalization from positive-curvature Gibbs integrability plus the existing exact quadratic conditional kernel (or alternatively direct weighted-density domination); standard Gaussian and product probability then make the constant integrable. Filter DCT gives integral (A_t f-f)^2 dnu_y ->0 at ordinary NNReal nhds0.

No true invariant law is needed for this bounded finite-probability argument. Source invariance/Jensen are used for contraction, then C_c density for all-L2 continuity; those remain OPEN, along with the L2 equivalence-class operator itself. No Markov/semigroup/restart, arbitrary correlated phase-clocks, uniform random-parameter AE, sampler/cost, or full paper/composition conclusion follows. Exact phase density normalization is not phase invariance.

All six original dynamics assumptions and actual construction conventions remain: zero-index/source E_(n+1), initialized live record, half-open intervals, last live infinite-wait arc, stopped dummy without phase, raw zero thresholds with AE positive Exp clocks, uncovered-z0 exceptional adapter, fixed-parameter common AE all finite times/init, rank0 and M0. The new source graph marks complete normalization routes OR, simultaneous ingredients AND, and excluded boundary associations as nondependencies. No original freeze or shared truth is modified.
'''
p=OUT/'source_preread84.md'; assert not p.exists(); p.write_bytes(note.encode('utf-8'))
outputs=['freeze_source84.py','source_inventory84.json','source_proof_graph84.json','bounded_candidate84.json','source_preread84.md']
seal={'schema':'astis.source-first-freeze84.v1','status':'SOURCE_ONLY_IMMUTABLE_FROZEN','created_utc':now,
 'primary_sha256':PRIMARY_SHA,'license_text_sha256':inventory['license']['normalized_text_sha256'],
 'source_inventory_sha256':sha((OUT/'source_inventory84.json').read_bytes()),
 'source_graph_sha256':sha((OUT/'source_proof_graph84.json').read_bytes()),
 'candidate_scope_sha256':sha((OUT/'bounded_candidate84.json').read_bytes()),
 'counts':graph['counts'],'independence':independence,
 'meaning':'Source-first prospective source topology only; no84 statement seal/Lean header/proof/verdict/state credit.',
 'bound_owned_outputs':[pin(str((OUT/n).relative_to(ROOT)).replace('\\','/')) for n in outputs]}
emit('source_freeze84.seal.json',seal)
outputs.append('source_freeze84.seal.json')
manifest={'schema':'astis.source-preread84.raw-manifest.v1','status':'closed','created_utc':now,
 'raw_inputs':raw_inputs,'raw_outputs':[pin(str((OUT/n).relative_to(ROOT)).replace('\\','/')) for n in outputs],
 'selfhash_convention':'Manifest omits its own hash to avoid circularity; caller reports exact manifest RAW externally.',
 'chronology':independence['chronology'],'writes_outside_owned_directory':False,
 'source_only':True,'candidate84_lean_read_or_written':False}
emit('source_freeze84.raw-manifest.json',manifest)
print(json.dumps({'counts':graph['counts'], 'manifest_raw_sha256':sha((OUT/'source_freeze84.raw-manifest.json').read_bytes()),
 'outputs':[{'file':n,'raw_sha256':sha((OUT/n).read_bytes())} for n in outputs]},indent=2))
