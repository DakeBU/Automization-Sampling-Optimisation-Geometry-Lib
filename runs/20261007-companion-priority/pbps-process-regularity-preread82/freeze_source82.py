"""Primary-only prospective PBPS process-regularity source freeze82; no Lean input."""
from html.parser import HTMLParser
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-process-regularity-preread82'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
SOURCE_SHA='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(PRIMARY)==SOURCE_SHA

class PrimaryParser(HTMLParser):
    def __init__(self):
        super().__init__();self.stack=[];self.nodes={}
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.stack.append([tag,attrs.get('id'),[]])
        if tag=='math' and attrs.get('alttext'):
            for frame in self.stack:frame[2].append(' '+attrs['alttext']+' ')
        if tag in ['meta','link','img','br','hr','input','source','wbr']:self.handle_endtag(tag)
    def handle_data(self,data):
        if not any(f[0]=='math' for f in self.stack):
            for frame in self.stack:frame[2].append(data)
    def handle_endtag(self,tag):
        k=next((i for i in range(len(self.stack)-1,-1,-1)if self.stack[i][0]==tag),None)
        if k is None:return
        for frame in self.stack[k:]:
            if frame[1]:self.nodes[frame[1]]=' '.join(''.join(frame[2]).split())
        del self.stack[k:]

parser=PrimaryParser();parser.feed(PRIMARY.read_text('utf8'))
now=datetime.now(timezone.utc).isoformat()
def write(name,data):
    p=OWN/name;assert not p.exists(),str(p)
    p.write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}

# Each scoped source ingredient or excluded consumer is independently accounted for.
rows=[
('license-tr','PROVENANCE','arXiv perpetual non-exclusive license; retain private paraphrases and minimal formulas; no new full raw duplicate.',[]),
('S1.p1','STANDING','V is C2 on Euclidean finite dimension; source target exp(-V) is context, not a conclusion of the next edge.',[1]),
('S1.E1','STANDING','Hessian sandwich alpha I <= Hess V <= beta I with 0<alpha<=beta.',[1]),
('S2.SS2.p1.1','STANDING','Source scale 0<eta<=1/beta, retain all six analytic binders even where the small-time subproof uses fewer.',[1]),
('S3.Thmtheorem1.p1.1','PARTIAL_CONTEXT_REST_OPEN','Fixed y,r,z0 actual event dynamics are the source process; full uniqueness/Markov/stationarity package remains OPEN.',[5,6,12]),
('A1.SS1.p1.1','INCLUDED_LITERAL','Fix auxiliary y and reference r; reference remains fixed along path.',[2,3]),
('A1.Ex1','INCLUDED_LITERAL','Actual residual-gradient rate sqrt(eta) positive-part inner product, nonnegative.',[3]),
('A1.Ex2','INCLUDED_LITERAL','Literal harmonic flow with center y-eta grad V(r), eta square-root scales and Phi_0=id.',[2]),
('A1.Ex3','INCLUDED_LITERAL','Actual momentum reflection; zero residual normal gives identity.',[5]),
('A1.SS1.p1.3','BOUNDARY','Bounce is an involution but possibly discontinuous at zero normal; do not require bounce continuity for small-time result.',[5,13]),
('A1.SS1.p2.1','INCLUDED_LITERAL','Independent Exp1 clocks, initial phase z0 and T0=0; source E_(n+1) is coordinate n.',[4,5]),
('A1.E1','INCLUDED_LITERAL','First integrated-hazard wait inf{u>=0:Lambda(u)>=E1}; empty hit is infinite.',[3,4]),
('A1.E2','INCLUDED_LITERAL','Finite event updates to postbounce phase; no phase evaluated at infinite time.',[5]),
('A1.SS1.p2.2','INCLUDED_LITERAL','Half-open arcs include left endpoint and exclude next event. An infinite wait retains current last live arc for all finite offsets.',[5,6,7]),
('A1.SS1.p3.1','INHERITED_NONACCUMULATION','Shifted harmonic energy used for actual pathwise rate cap.',[6,9]),
('A1.Ex4','INHERITED_NONACCUMULATION','Energy E=(eta^-1 norm(x-c)^2+norm(p)^2)/2.',[6,9]),
('A1.SS1.p3.2','INHERITED_NONACCUMULATION','Flow/bounce preserve energy; every live record stays on the same layer.',[6,9]),
('A1.Ex5','INHERITED_NONACCUMULATION','Momentum and centered-position layer bounds.',[6,9]),
('A1.SS1.p3.3','INHERITED_NONACCUMULATION','Global beta Lipschitz gradient bounds actual rate along flow.',[3,9]),
('A1.Ex6','OPTIONAL_QUANTITATIVE_INGREDIENT','Finite state-dependent cap C=sqrt(eta) beta sqrt(2E)(sqrt(2etaE)+norm(c-r)); optional defect bound <=C t.',[9]),
('A1.Ex7','OPTIONAL_QUANTITATIVE_INGREDIENT','Lambda(t)<=C t for every nonnegative finite t.',[3,9]),
('A1.SS1.p3.5','BOUNDARY','Zero cap means no jumps; positive-cap division must be guarded. Small-time defect bound itself needs no division by C.',[4,9,13]),
('A1.Ex8','INHERITED_NONACCUMULATION','Positive cap finite waiting time lower bound E_(n+1)/C.',[6]),
('A1.Ex9','INHERITED_NONACCUMULATION','Continuing clocks escape every finite horizon via divergent Exp sums.',[6]),
('A1.SS1.p3.7','PARTIAL_REST_OPEN','Nonaccumulation supplies allfinite source realization. Source direct mean1 Exp SLLN distinct from alternative sufficient routes. Memoryless Markov/Davis restart not supplied by present edge.',[6,13]),
('A1.Thmtheorem1.p1.1','EXCLUDED_GLOBAL_OPERATOR','Transition operators are those of the already established source Markov process; a probability kernel alone does not identify that process.',[12,13]),
('A1.E3','EXCLUDED_REVERSAL','Momentum-reversed adjoint identity remains OPEN.',[12]),
('A1.I1.i1.p1','EXCLUDED_INVARIANCE','Invariance is a separate parent of full L2 continuity, not a result of stochastic continuity.',[12]),
('A1.I1.i2.p1','CONSUMER_OPEN','Strongly continuous L2 contraction semigroup is genuine downstream source consumer; full claim requires invariance/contractivity and Markov/semigroup in addition.',[12]),
('A1.SS1.SSS0.Px1.p2.1','BOUNDARY_HEURISTIC_GENERATOR','Source rejects merely formal generator exponentiation because bounce may be discontinuous; use actual path/event law.',[13]),
('A1.E7','EXCLUDED_PATH_EXPANSION','Ordered n-event path-density expansion and path reversal need separate work, not first-event estimate alone.',[13]),
('A1.SS1.SSS0.Px1.p6.1','INCLUDED_EXPLICIT_CONSUMER','For compactly supported continuous test F, flow tends identity and first-event probability tends zero; source uses this after invariance/Jensen for strong continuity.',[2,8,9,10,11,12]),
('A1.Ex22','INCLUDED_EXACT_SOURCE_FORMULA','First-event probability is 1-exp(-Lambda(t)), tending to zero as t decreases to0.',[4,8,9]),
('A1.SS1.SSS0.Px1.p6.2','CONSUMER_PARTIAL_REST_OPEN','Dominated convergence gives source L2 convergence for Cc; density and contractivity extend to L2. Present candidate contributes actual small-time control only.',[10,11,12]),
('A1.SS2.p3.1','INHERITED_MEASURABLE_REPRESENTATIVE','Joint Borel flow/rate/bounce/hazard/records give terminal version; source failed-limit zero versus ASTIS uncovered z0 must remain distinct.',[3,5,6,8]),
('A1.SS2.p4.1','EXCLUDED_ALREADY_PRIOR_LAW_BOUNDARY','Exact q_y/Gaussian/clocks terminal integration motivates existing ideal H. Do not repeat probability-kernel existence or use it to infer process Markovness.',[13]),
]
inventory=[]
for i,(sid,scope,desc,ns) in enumerate(rows,1):
    assert sid in parser.nodes,sid
    inventory.append({'id':'I82-%02d'%i,'source_id':sid,'scope':scope,'paraphrase':desc,
                      'primary_node_text_sha256':hashlib.sha256(parser.nodes[sid].encode('utf8')).hexdigest(),
                      'source_graph_nodes':['G82-%02d'%n for n in ns]})
assert len({r['source_id']for r in inventory})==len(inventory)
binders=[{'id':'hα','formula':'0<alpha','source_id':'S1.p1'},
         {'id':'hαβ','formula':'alpha<=beta','source_id':'S1.p1'},
         {'id':'hV','formula':'V in C2','source_id':'S1.p1'},
         {'id':'hH','formula':'forall x,v, alpha norm(v)^2 <= Hess V(x)[v,v] <= beta norm(v)^2','source_id':'S1.E1'},
         {'id':'hη','formula':'0<eta','source_id':'S2.SS2.p1.1'},
         {'id':'hβη','formula':'beta eta<=1','source_id':'S2.SS2.p1.1'}]
invfile=write('source_inventory82.json',{'schema':'independent-primary-only-prospective-inventory-v1','created_utc':now,
 'primary':raw(PRIMARY),'source':'Chen/Chewi/Lu/Zhang arXiv2609.06905v1','license':'arXiv.org perpetual non-exclusive license',
 'candidate_lean_or_reviews_seen':False,'analytic_binders':binders,'items':inventory,'item_count':len(inventory),
 'scope':'Actual fixed-reference phase small-time regularity at0 from exact first-event law; source path/Markov/invariance consumers distinguished.',
 'coverage_rule':'Every chosen source ingredient and immediate global consumer is mapped below; not an exhaustive audit of all paper results.'})

node_specs=[
('Six standing source analytic conditions and fixed y,r,z0','SOURCE_STANDING',['S1.p1','S1.E1','S2.SS2.p1.1']),
('Actual harmonic Phi joint continuous, Phi0=id and finite elapsed','SOURCE_LITERAL',['A1.Ex2']),
('Actual nonnegative continuous rate and integrated hazard Lambda: Lambda0=0, continuous in finite time','SOURCE_LITERAL_PLUS_ELEMENTARY_REGULARITY',['A1.Ex1','A1.E1','A1.SS2.p3.1']),
('Actual first threshold Exp1 and firstwait survival P[t<tau]=exp(-Lambda_t)','SOURCE_EX22_INTEGRATED_HAZARD_LAW',['A1.SS1.p2.1','A1.E1','A1.Ex22']),
('Initialized stopped first record, T0=0, finite versus infinite nextwait','SOURCE_ACTUAL_RECURRENCE',['A1.E2','A1.SS1.p2.2']),
('One actual measurable physical Z agreeing halfopen arcs; source fixedparam nonaccumulation supports allfinite construction','SOURCE_REPRESENTATIVE_INGREDIENT',['A1.SS1.p2.2','A1.SS1.p3.7','A1.SS2.p3.1']),
('No first event by t implies actual Z_t=Phi_t(z0)','SOURCE_HALFOPEN_ADAPTER',['A1.SS1.p2.2']),
('Measurable actual defect event and P[Z_t!=Phi_t z0]<=1-exp(-Lambda_t)','BOUNDED_ACTUAL_INPUT_INTEGRATION',['A1.Ex22','A1.SS2.p3.1']),
('First-event probability tends0 at0; optional upper bound <=C(z0)t','SOURCE_EXPLICIT_SMALLTIME_BOUND',['A1.Ex6','A1.Ex7','A1.Ex22']),
('Actual stochastic continuity at physical0: for every delta>0, P[norm(Z_t-z0)>=delta]->0 as t downarrow0','SOURCE_IMPLICIT_SMALLTIME_REGULARITY_CANDIDATE',['A1.SS1.SSS0.Px1.p6.1','A1.Ex22']),
('Bounded continuous test observable expectation tends its initial value, pointwise fixed z0','DOWNSTREAM_CONSUMER_OPEN_NOT_CURRENT_CANDIDATE',['A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']),
('Full invariant L2 contraction strongly continuous semigroup','DOWNSTREAM_OPEN_REQUIRES_INVARIANCE_AND_SEMIGROUP',['A1.I1.i1.p1','A1.I1.i2.p1','A1.SS1.SSS0.Px1.p6.2']),
('Alltime cadlag/rightcontinuity, conditional restart/Markov, full path density/reversal and ideal H/composition/cost','EXCLUDED_OPEN_OR_DISTINCT_CANDIDATE',['A1.SS1.p3.7','A1.E7','A1.SS2.p4.1'])]
nodes=[{'id':'G82-%02d'%i,'obligation':o,'classification':c,'source_ids':ids,'status':'SOURCE_ONLY_PROSPECTIVE_NOT_FORMALIZED'}for i,(o,c,ids)in enumerate(node_specs,1)]
edge_specs=[
(1,2,'C2 gives continuous gradient and actual center; explicit harmonic flow continuous.'),
(1,3,'Actual gradient residual/rate continuous and nonnegative; integrate over finite intervals.'),
(3,4,'Nondecreasing continuous hazard and Exp1 survival give actual firstwait law, including infinity.'),
(4,5,'Coordinate0 realizes source E1 at initialized first record; no later threshold independence needed for the estimate.'),
(2,5,'Finite guarded update uses actual harmonic flow and reflection; no infinity phase.'),
(5,6,'Actual stopped finite records and halfopen interval cover define source phase.'),
(2,6,'Continuous finite flow gives actual arc values and initialization.'),
(5,7,'At n=0 record=(0,z0); if t<T1 then source halfopen first interval is active.'),
(6,7,'Actual covered-arc equality, not a supplied arbitrary phase process.'),
(7,8,'Defect event subset of first-event-by-t event; zero/trivial bounce does not invalidate an upper bound.'),
(4,8,'Canonical first-coordinate Exp1 law turns firstwait event into exact 1-exp(-Lambda_t).'),
(6,8,'Actual joint measurability makes norm/equality defect events measurable.'),
(3,9,'Lambda continuous with Lambda0=0 implies exp(-Lambda_t)->1.'),
(1,9,'Source finite energy/cap optionally gives Lambda_t<=C t and elementary 1-exp(-u)<=u; no cap positivity needed.'),
(2,10,'Phi_t(z0)->z0; for small t its distance is less than prescribed delta.'),
(8,10,'Then actual distance defect >=delta is contained in flow-disagreement event.'),
(9,10,'Small-time firstevent probability bounds the stochastic-continuity probability.'),
(10,11,'Future bounded continuous test convergence follows actual convergence in probability or split expectation bound.'),
(11,12,'Future pointwise bounded-test convergence contributes DCT after separately proved invariance and contractivity; does not itself prove these.'),
(10,13,'Future substrate only: stochastic continuity at0 does not establish restart/Markov/path law or alltime cadlag.'),
]
edges=[{'id':'E82-%02d'%i,'ingredient':'G82-%02d'%a,'consumer':'G82-%02d'%b,'reason':why,
        'kind':'future-substrate-not-implication'if b in [11,12,13]else'source-proof-ingredient',
        'status':'SOURCE_ONLY_PROSPECTIVE_NOT_COMPILED'}for i,(a,b,why)in enumerate(edge_specs,1)]
graphfile=write('source_proof_graph82.json',{'schema':'independent-source-proof-graph-prospective-v1','created_utc':now,
 'primary_raw_sha256':SOURCE_SHA,'source_inventory_raw_sha256':sha(invfile),'nodes':nodes,'edges':edges,
 'node_count':len(nodes),'edge_count':len(edges),'candidate_implementation_seen':False,
 'truth_contract':'Source topology only, not a compiled Lean DAG. No theorem admission, proof, source-review verdict or verification credit.'})

candidate={
 'schema':'source-only-bounded-candidate-v1','created_utc':now,'selected_candidate':'Actual fixed-reference physical phase stochastic continuity at zero, via exact first-event defect bound',
 'source_reason':'A1.SS1.SSS0.Px1.p6.1 and A1.Ex22 explicitly use deterministic flow convergence and small firstevent probability to establish the strong-continuity ingredient in Proposition A.1. This consumes the actual phase beyond merely constructing H at pi.',
 'anchors':['A1.Ex22','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2','A1.E1','A1.SS1.p2.2'],
 'assumptions':binders,
 'objects':{'P':'countable independent Exp(1) product on real sequences; epsilon_n=max(sample_n,0) with coordinate n=source E_(n+1)',
            'Z':'Actual80-type single jointly Borel physical phase with literal covered/fallback clauses, fixedparams common AE allfinite arcs/init; no arbitrary supplied process certificate',
            'parameters':'Fixed V,alpha,beta,eta,y,reference r and initial phase z0; deterministic physical t>=0',
            'firstwait':'tau(y,r,z0,epsilon_0), top if no threshold hit; eventTime1 equals this wait because T0=0',
            'Lambda':'integral_0^t sqrt(eta)*max(0,<p_s,gradV(x_s)-gradV(r)>) ds along actual harmonic Phi_s(z0)'},
 'prospective_formulas':[
   'P{omega: Z(y,r,z0,t,omega) != Phi_t(y,r,z0)} <= 1-exp(-Lambda(y,r,z0,t))',
   'forall delta>0, lim_(t downarrow 0) P{omega: delta<=norm(Z(y,r,z0,t,omega)-z0)} = 0'],
 'optional_quantitative_refinement':'1-exp(-Lambda_t)<=Lambda_t<=C(y,r,z0)t, with source finite energy cap C; not required for basic candidate and never divide by zero cap.',
 'proof_ingredients':['Actual first-coordinate Exp marginal and firstwait survival law','Initialized first record T0=0,z0 and exact finite/top guards','Actual covered first-arc equality for t<T1','Actual Z measurability for event measurability','Phi_t(z0)->z0 and Lambda_t->0','Event inclusion plus probability monotonicity and squeeze'],
 'dependency_readiness':{'status':'source-level dependency-ready subject to root checking exact current parent APIs; no new missing mathematical hypothesis identified',
  'expected_existing_parent_roles':['Actual73 harmonic continuity/Phi0','Actual76 initialized recursion and eventTime1 guards','Actual77 actual wait law/hazard continuity','Actual80 actual Z measurability/covered firstarc','UnitExponentialProduct actual coordinate law'],
  'readiness_limit':'No Lean implementation read during this source-only run; current compiled/admission status is deliberately not asserted from source reading.'},
 'why_not_wrapper':'Construct an actual measurable phase-defect event, relate it to the real first jump, integrate against actual Exp input, and obtain stochastic continuity. Neither result follows from generic kernel existence or repeats81 terminal pushforward.',
 'smaller_options':[
  {'option':'Actual nofirstevent coupling bound only','scope':'First prospective formula for every finite t. Smallest reusable core; source Ex22 immediate consumer.', 'missing_parent':'No new analysis parent beyond actual firstwait law/firstarc realization; exact first-coordinate product pullback must be proved.'},
  {'option':'AE alltime path right-continuity','scope':'For each fixed y,r,z0, on one good sample event every finite t has a right-neighborhood staying on its active harmonic arc; therefore right-continuous phase path.', 'classification':'Source-implicit consequence of halfopen cover, not an explicitly named source theorem.', 'missing_parent':'Actual common AE allfinite cover, positive threshold/finite gap conventions and flow continuity; no Markov premise needed. Does not directly establish no fixed-time jump or two-sided stochastic continuity.'},
  {'option':'Deterministic-time restart / Chapman-Kolmogorov','scope':'Conditioned future given actual past equals fresh process from Z_s with fixed y,r; yields time-homogeneous Markov/semigroup.', 'classification':'Source explicit memoryless assertion A1.SS1.p3.7 but substantially larger.', 'missing_parent':'Measurable past filtration, adapted event records, conditional residual Exp law on survival, fresh unused clocks independent of history, and actual restart identity. Kernel mass one is insufficient.'}],
 'boundaries':{'rank0':'Degenerate phase is point space; zero rate and infinite firstwait give defect0, stochastic continuity trivial but still allowed.',
               'zero_thresholds':'Deterministic zero waits may own immediate postbounce at0; actual Exp coordinate positive AE. Firstevent defect inclusion remains valid even on exceptional raw sequences; init law at0 is not asserted uniformly over all raw samples.',
               'last_live_infinitewait':'No event by any finite t on first infinite wait; actual first live arc used, not stopped dummy. Later infinite waits do not enter firstevent estimate.',
               'endpoint':'Use t<T1 as survival and T1<=t as firstevent-by-t. Source prose before-time versus at-or-before can be reconciled via Exp/hazard atomlessness at fixed finite t, not assumed pathwise.',
               'fallback':'Retain actual80 z0 uncovered fallback distinct from source failed-limit zero. Covered firstinterval identity is deterministic; any further version transfer needs explicit AE equality.',
               'initialization':'z0 fixed; no new q_y/Gaussian/reference integration or arbitrary correlated substitution. No uniform over y,r,z0 probability limit or null event claimed.'},
 'open_obligations':['Full phase Markov/restart/strong Markov/Chapman-Kolmogorov','Full invariant L2 semigroup/adjoint/reversibility/contraction','Alltime cadlag and two-sided stochastic continuity unless separately proved','Full random-initialized alltime path law and universal version uniqueness','Ordered event density/path reversal','Implemented reference sampler/cap approximation/error/query costs','H_y invariance/augmented/reflection composition/hypocoercivity/main theorem/full Goal'],
 'status':'SOURCE_ONLY_PROSPECTIVE_NO_STATEMENT_SEAL_PROOF_ADMISSION_OR_VERIFICATION'}
candidatefile=write('bounded_candidate82.json',candidate)

note=OWN/'source_preread82.md';assert not note.exists()
note.write_bytes(('''# PBPS source-only preread82

Pinned primary v1 was read before any candidate or review. This run reads no Lean implementation and creates no SAU/state change.

Selected bounded candidate: actual fixed-reference small-time stochastic continuity at zero, proved through the actual first-event defect bound

`P[Z_t != Phi_t(z0)] <= 1 - exp(-Lambda_t)`.

The exact source consumer is Appendix A.1, A1.SS1.SSS0.Px1.p6.1 / A1.Ex22 / p6.2: flow tends identity and firstevent probability tends zero, contributing to strong continuity after separately established invariance and Jensen contraction. The present candidate cannot prove the full L2 semigroup or Markov property.

Under the six standing source analytic assumptions, use actual Exp1 first-coordinate marginal/firstwait survival, initialized stopped recurrence, deterministic first half-open arc agreement and actual Z measurability. Flow continuity and Lambda_0=0 yield for every fixed y,r,z0 and delta>0:

`P[norm(Z_t-z0)>=delta] -> 0` as finite `t` decreases to zero.

The optional quantitative cap bound is `1-exp(-Lambda_t)<=C(z0)t`; zero cap is handled without division. No new energy/cap/law certificate may be a public source premise. An infinite firstwait preserves the first live arc. A stopped dummy is never a physical phase. Index0 clock is source E1. Exceptional zero thresholds do not justify uniform raw-sample initialization. Intrinsic rank0 is harmless if root retains it.

Smaller core: the defect bound alone. Alternative path regularity: fixedparams common-AE alltime right-continuity follows local active-interval margins, but is source-implicit and distinct from two-sided stochastic continuity. Restart is a larger source-explicit memoryless edge needing conditional residual exponential law, past filtration and fresh-clock independence; probability-kernel existence is not a substitute.

Fresh source inventory and graph list every scoped ingredient and immediate excluded consumer. Parent readiness is source-level only; root must check actual current APIs after81 integration. No new theorem, proof, review verdict, VERIFIED, invariance, cost or whole-paper credit is conferred.
''').encode('utf8'))
seal=write('source_freeze82.seal.json',{'schema':'source-first-prospective-seal-v1','created_utc':now,
 'primary':raw(PRIMARY),'inventory':raw(invfile),'graph':raw(graphfile),'candidate':raw(candidatefile),
 'source_item_count':len(inventory),'source_node_count':len(nodes),'source_edge_count':len(edges),
 'candidate_lean_seen':False,'other_review_verdicts_seen':False,'production_or_shared_writes':False,
 'only_input_primary':True,'status':'FROZEN_SOURCE_ONLY_PROSPECTIVE'})
manifest=write('source_freeze82.raw-manifest.json',{'schema':'noncircular-source-only-raw-manifest-v1','created_utc':now,
 'raw_inputs':[raw(PRIMARY)],'raw_outputs':[raw(p)for p in [Path(__file__).resolve(),invfile,graphfile,candidatefile,note,seal]],
 'self_hash_omitted':True,'no_public_rawsource_copy':True,'candidate_or_implementation_seen':False,
 'truth_contract':'Prerequisite source reading only; root selection remains pending.'})
print(json.dumps({'status':'source-only frozen','items':len(inventory),'nodes':len(nodes),'edges':len(edges),
 'raw_outputs':[raw(p)for p in [invfile,graphfile,candidatefile,note,seal,manifest]],'script':raw(Path(__file__).resolve())},indent=2))
