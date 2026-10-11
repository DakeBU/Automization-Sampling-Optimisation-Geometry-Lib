from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json

root=Path('E:/Samplinglib')
out=root/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/primary-first'
primary=root/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=primary.read_bytes();source=raw.decode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):return {'path':str(p).replace('\\','/'),'raw_sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def write(name,obj):
    with (out/name).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
old_hashes={'recommendation92.md':'65be1648d45ed8316fe0bf06179693584c4c18ad33b550dd8416018997ed376e','recommendation92.native.json':'f613531e8b5f6fc3c02d6d151716ccab8225552f5d2898a9599add9ee0f41fce','closed-RAW92.native.json':'4ce38186002a058cb77d88206931fe2adbb5bfd78bc2de90ec1805359302a713'}
for n,h in old_hashes.items():assert sha((out/n).read_bytes())==h

selected=['S1.p1','S2.SS2.p1','S3.SS2.p4','A1.SS1.p1','A1.SS1.p2','A1.E1','A1.E2','A1.SS1.p3','A1.SS1.p4','A1.Thmtheorem1','A1.SS1.SSS0.Px1.p1','A1.SS1.SSS0.Px1.p2','A1.SS1.SSS0.Px1.p3','A1.SS1.SSS0.Px1.p4','A1.Ex19','A1.SS1.SSS0.Px1.p4.2','A1.E7','A1.SS1.SSS0.Px1.p4.3','A1.E8','A1.SS1.SSS0.Px1.p4.4','A1.SS1.SSS0.Px1.p5','A1.SS1.SSS0.Px1.p6','A1.SS1.SSS0.Px1.p7','A1.SS2.p1','A1.SS2.p2','A1.Thmtheorem2','A1.SS2.p3','A1.SS2.p4','A1.SS2.p5']
line_starts=[0]
for i,c in enumerate(source):
    if c=='\n':line_starts.append(i+1)
class Spans(HTMLParser):
    void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self):super().__init__();self.stack=[];self.spans={}
    def position(self):
        line,col=self.getpos();return line_starts[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag not in self.void:self.stack.append((tag,dict(attrs).get('id'),self.position()))
    def handle_startendtag(self,tag,attrs):pass
    def handle_endtag(self,tag):
        matches=[i for i,x in enumerate(self.stack) if x[0]==tag]
        if not matches:return
        i=matches[-1];_,id,start=self.stack[i];self.stack=self.stack[:i]
        if id not in selected:return
        end=source.index('>',self.position())+1
        bs=len(source[:start].encode());be=len(source[:end].encode())
        self.spans[id]={'html_id':id,'byte_start':bs,'byte_end_exclusive':be,'line_start':source.count('\n',0,start)+1,'line_end':source.count('\n',0,end)+1,'bytes':be-bs,'raw_sha256':sha(raw[bs:be])}
p=Spans();p.feed(source)
assert set(selected)==set(p.spans)
spans={k:p.spans[k] for k in selected}

nodes=[]
def node(id,kind,claim,anchors,status='CANDIDATE_PROOF_OBLIGATION',boundary=None):
    nodes.append({'id':id,'kind':kind,'claim':claim,'source_regions':anchors,'status':status,'boundary':boundary or ''})
node('H92','original-standing-assumptions','V in C2(R^d); 0<alpha<=beta; Hessian quadratic-form bounds alpha,beta; 0<eta<=1/beta.',['S1.p1','S2.SS2.p1'],'SOURCE_INPUT')
node('O92','literal-source-objects','Fixed y,r,z0; center y-eta gradV(r), residual gradient, harmonic flow Phi, rate sqrt(eta)[p dot h]+, reflection B with R0=I.',['S3.SS2.p4','A1.SS1.p1'],'SOURCE_DEFINITION')
node('I92','literal-source-randomness-and-recursion','Independent Exp(1) clocks; A1 closed threshold infimum; A2 cumulative time plus wait and reflected flowed poststate; stop at empty threshold set.',['A1.SS1.p2','A1.E1','A1.E2'],'SOURCE_DEFINITION')
node('T92','ASTIS-representation-convention','Complete finite histories use all time/poststate records, with an explicit absorbing stopped tag only to totalize the stopped source recursion.',['A1.SS1.p2'],'CANDIDATE_ENCODING','Time-zero auxiliary observations, if chosen later, are not source infinite event times; live tags guard event claims. No encoding fixed by this graph.')
node('M92','author-measurability-ingredient','Jointly Borel flow/rate/bounce, integrated hazard, threshold time and finite actual recursion.',['A1.SS2.p3'],'REQUIRED_INGREDIENT_REUSE_CANDIDATE','Continuity of bounce is not required; exact threshold equality/empty-set cases remain part of the actual input law.')
node('W92','ASTIS-source-implicit-one-step','At deterministic index n, actual complete-history/fresh-clock restricted next absolute event-time law with density lambda(Phi_(u-a)z) exp(-L_z(u-a)) on a<u<T.',['A1.SS1.p2','A1.SS1.SSS0.Px1.p4.2','A1.E7'],'REQUIRED_INGREDIENT_REUSE_CANDIDATE','This is a source-derived interface demand, not a new assumption or a recompilation/acceptance claim about phase91.')
node('D92','literal-source-simplex','Delta_n(T) has strict 0<t1<...<tn<T; empty tuple at n=0 carries product mass one.',['A1.Ex19','A1.E7'],'SOURCE_DEFINITION_PLUS_EMPTY_PRODUCT_CONVENTION')
node('K92','ASTIS-explicit-prescribed-prefix','For t in Delta_n(T), recursively construct z_j^- = Phi_(t_j-t_(j-1))(z_(j-1)), z_j=B(z_j^-), retaining all (t_j,z_j); prove joint Borel dependence in y,r,z0,t.',['A1.SS1.p2','A1.SS1.SSS0.Px1.p4.2','A1.SS2.p3'])
node('Q92','ASTIS-explicit-prefix-weight','q_n(t)=product_j lambda(z_j^-)exp(-L_(z_(j-1))(t_j-t_(j-1))); q0=1; jointly Borel in source parameters and simplex coordinates.',['A1.E7','A1.SS1.SSS0.Px1.p4.2','A1.SS2.p3'],'CANDIDATE_PROOF_OBLIGATION','No survival from t_n to T yet.')
node('E92','ASTIS-actual-prefix-event','E_n(T): first n actual events live and strictly ordered in (0,T); E0=Omega. Measurable event representing at least n interior events, not exactly n.',['A1.SS1.p2','A1.Ex19','A1.E7'])
node('B92','ASTIS-induction-base','At n=0 actual history and prescribed history equal the deterministic one-record history; empty-simplex integral has mass one.',['A1.SS1.p2','A1.E7'])
node('A92','ASTIS-actual-prescribed-append','On the restricted event the next actual complete history appends (u,B(Phi_(u-t_n)z_n)); all older records agree with the prescribed prefix.',['A1.E2','A1.SS1.SSS0.Px1.p4.2'])
node('J92','ASTIS-induction-successor','Apply the actual one-step law to nonnegative appended-history tests and restrict the old history to E_n(T); use induction and parameter integration to multiply q_n by the next factor.',['A1.SS1.SSS0.Px1.p4.2','A1.E7'])
node('FUB92','canonical-measure-theory-ingredient','Nonnegative parameter integration/Tonelli and finite-product coordinate splitting turn nested simplex sections into product Lebesgue measure; n=0 product convention included.',['A1.Ex19','A1.E7'],'REQUIRED_BACKGROUND_INGREDIENT','Not an extra source binder and not an assertion of a new general shear theorem.')
node('SEC92','ASTIS-simplex-section-identification','Delta_(n+1)(T) is {(t,u): t in Delta_n(T), t_n<u<T}, with previous time 0 for n=0. Exact product coordinate identification preserves Lebesgue measure.',['A1.Ex19','A1.E7'])
node('PREFIX92','ASTIS-recommended-target','For every n,T and nonnegative Borel complete-history F, integral_E_n(T) F(H_n)dP = integral_Delta_n(T) F(K_n(t))q_n(t)dt; Borel objects and unnormalized mass<=1.',['A1.SS1.p2','A1.Ex19','A1.SS1.SSS0.Px1.p4.2','A1.E7'],'CANDIDATE_TARGET_NOT_SEALED','One finite-prefix history law; all six original analytic conditions retained. Full path-functional A7 not closed.')
node('REL92','alternative-ASTIS-prefix-route','First derive finite positive relative-wait vector density and complete-state recursion under iid clocks.',['A1.E1','A1.E2','A1.E7'],'ALTERNATIVE_OPEN')
node('TRI92','alternative-ASTIS-coordinate-route','Transport relative durations to ordered absolute times by the finite cumulative-sum triangular map with its exact Lebesgue/product-domain proof.',['A1.E2','A1.Ex19','A1.E7'],'ALTERNATIVE_OPEN')
node('SURV92','ASTIS-final-survival-composition','At the actual last live history use fresh-clock survival exp(-L_z(T-T_n)); compose with PREFIX92 to obtain the final factor at prescribed histories.',['A1.E1','A1.E7'],'FUTURE_CONSUMER','Underlying survival result may already be available; the new finite-prefix composition is distinct. Not a parent for PREFIX92.')
node('ALG92','ASTIS-full-hazard-identification','Segment hazards through all n jumps plus terminal duration equal the integral of lambda along the prescribed complete path; rate factors equal pre-jump rates.',['A1.E7','A1.SS1.p2'],'FUTURE_CONSUMER')
node('END92','conditional-endpoint-obligation','Prove any required equality of strict and non-strict horizon event conventions for actual finite jumps; stopped zero observers and deterministic T0 are excluded from finite-jump atom reasoning.',['A1.Ex19','A1.E7'],'FUTURE_CONDITIONAL','Needed only when an endpoint convention is changed, not an extra assumption for strict PREFIX92.')
node('ENERGY92','author-energy-rate-cap','The harmonic flow and reflection preserve shifted harmonic energy; beta smoothness then bounds the rate on every actual or prescribed trajectory from fixed z0.',['A1.SS1.p3'],'SOURCE_PROOF_INGREDIENT','Separate from the almost-sure divergence argument, so the cap route does not falsely require nonexplosion as its mathematical input.')
node('N92','author-nonexplosion-substrate','Energy/rate cap and divergence of exponential sums imply no finite accumulation and finite bounded-horizon event count almost surely.',['A1.SS1.p3'],'EXISTING_SUBSTRATE_NOT_REOPENED','The preread preserves tracked actual-input nonaccumulation78/coverage79. No new implementation-status audit or proof is claimed.')
node('PATH92','ASTIS-full-path-test-identification','Relate actual trajectory on each finite-count event to prescribed entire trajectory; establish measurable composition for path functionals, retaining all event records.',['A1.SS1.p2','A1.SS1.SSS0.Px1.p4.2','A1.E7','A1.SS2.p3'],'FUTURE_CONSUMER','A terminal-position law alone is insufficient. Exact path-space sigma-algebra/representative must be specified when formalized.')
node('COUNT92','ASTIS-exhaustive-count-partition','Use actual-input nonaccumulation and half-open coverage to partition trajectories by finite event count; connect to strict simplex and final no-event interval.',['A1.SS1.p3','A1.Ex19','A1.E7'],'FUTURE_CONSUMER')
node('TERM92','ASTIS-fixed-count-path-law','For each n, combine PREFIX92, final survival and path/hazard identification to get the nth full path-functional term of A7.',['A1.E7'],'FUTURE_CONSUMER')
node('CAP92','author-absolute-convergence-route','Preserved energy bounds each rate, and simplex volume T^n/n! bounds the absolute bounded-test series.',['A1.SS1.p3','A1.SS1.SSS0.Px1.p4.3'],'FUTURE_SOURCE_ROUTE')
node('MASS92','alternative-ASTIS-summation-route','Nonnegative fixed-count identities plus exhaustive probability-one count partition imply mass one; Tonelli and bounded signed decomposition give A7 without a separate cap/simplex summability proof.',['A1.E7','A1.SS1.SSS0.Px1.p4.3'],'ALTERNATIVE_OPEN')
node('A7','printed-author-full-path-functional-identity','For every bounded measurable functional of the full path [0,T], expectation equals the infinite simplex sum with all pre-jump rates and survival through T, including n=0.',['A1.E7','A1.SS1.SSS0.Px1.p4.2'],'FUTURE_PRINTED_TARGET_NOT_CLOSED')

edges=[]
def edge(a,b,use):edges.append({'from':a,'to':b,'consumer_use':use,'relation':'source-proof-ingredient-not-Lean-edge'})
for a,b,use in [
('M92','K92','Finite composition supplies joint Borel prescribed-history dependence.'),
('M92','Q92','Joint Borel hazard and rate supply Borel prefix weight.'),
('FUB92','SEC92','Finite product-coordinate splitting supplies the exact Lebesgue section identification.'),
('K92','PATH92','Prescribed complete records reconstruct every deterministic arc.'),
('M92','PATH92','Borel recursion supports measurable prescribed-path observables.'),
('N92','PATH92','Actual global path and finite-count representation use nonaccumulation/coverage.'),
('K92','ALG92','Consecutive flow segments identify each hazard integral and pre-bounce rate.'),
('I92','SURV92','Fresh exponential clock gives no-next-event probability at remaining duration.'),
('M92','SURV92','Measurable history-dependent remaining duration permits survival composition.'),
('H92','ENERGY92','Beta smoothness and positive eta bound residual rate on energy shells.'),
('O92','ENERGY92','Harmonic flow and orthogonal reflection preserve shifted energy.'),
('ENERGY92','N92','Rate cap yields wait lower bound before exponential-sum divergence.'),
('I92','N92','Actual iid exponential input supplies almost-sure divergence.'),
('ENERGY92','CAP92','Prescribed-path rate cap and simplex volume bound each signed-test term.')]:edge(a,b,use)
for a,b,use in [
('H92','O92','Define source dynamics under positive scale and source regularity.'),('O92','I92','Use actual rate, harmonic flow and reflection in the event recursion.'),('I92','T92','Represent stopped source histories at arbitrary deterministic depth.'),('H92','M92','Continuity of gradient and positive eta supply source Borel/hazard arguments.'),('O92','M92','Zero-normal reflection convention and explicit flow supply actual Borel maps.'),('I92','W92','Fresh iid exponential threshold drives the conditional one-step law.'),('M92','W92','Borel complete-history/fresh-clock observables permit integration.'),('O92','K92','Construct actual prescribed states at each supplied time gap.'),('D92','K92','Strict order guarantees positive finite gaps.'),('K92','Q92','Evaluate pre-bounce rate and segment integrated hazard at prescribed states.'),('M92','E92','Borel actual record/time maps define strict prefix event.'),('T92','E92','Live tags exclude terminated histories.'),('I92','B92','Initial actual record is deterministic at time zero.'),('D92','B92','Empty tuple measure and empty product yield base case.'),('W92','A92','One-step actual poststate is reflected flowed old poststate.'),('K92','A92','Prescribed snoc prefix uses the identical flow/bounce update.'),('W92','J92','Apply one-step absolute law at fixed deterministic event index.'),('A92','J92','Keep full prefix when changing actual to prescribed appended history.'),('Q92','J92','Multiply old density by next conditional density factor.'),('E92','J92','Restrict previous history to E_n; next strict guard is equivalent to E_(n+1).'),('FUB92','J92','Obtain measurable parameter-integral test for inductive substitution.'),('D92','SEC92','Compute exact strict simplex sections, including n=0.'),('SEC92','J92','Convert the nested (t,u) support to the next simplex.'),('B92','PREFIX92','Natural-number induction base.'),('J92','PREFIX92','Natural-number induction step; induction hypothesis is schematic, not a new theorem assumption.'),('I92','REL92','Alternative iteration in positive elapsed durations.'),('REL92','TRI92','Transport the alternative relative-vector density and full history.'),('TRI92','PREFIX92','Alternative sufficient absolute-time construction, not an extra mandatory parent.'),('PREFIX92','SURV92','Integrate history-dependent remaining-horizon survival against finite prefix law.'),('SURV92','TERM92','Add missing final no-event factor; prefix event alone is at least n.'),('ALG92','TERM92','Replace sum of segment hazards with whole-path integral and rate left limits.'),('PATH92','TERM92','Evaluate arbitrary full-path functional, not merely terminal coordinate.'),('PREFIX92','TERM92','Supply finite ordered jump-density product and prescribed complete histories.'),('N92','COUNT92','Exhaustion by finite event counts from actual-input nonaccumulation/coverage.'),('PATH92','COUNT92','Identify each actual trajectory and prescribed path on its count event.'),('END92','COUNT92','Conditional dependency only when strict/non-strict endpoint conventions are identified.'),('TERM92','A7','Supply each summand for its actual count event.'),('COUNT92','A7','Sum disjoint events exhausting probability one.'),('CAP92','A7','Printed sufficient absolute-convergence route for bounded signed tests.'),('TERM92','MASS92','Alternative nonnegative exact count-event mass identity.'),('COUNT92','MASS92','Alternative total probability and Tonelli summation.'),('MASS92','A7','Alternative bounded signed assembly; not simultaneous mandatory cap bound.')]:edge(a,b,use)

graph={'schema_version':1,'record_kind':'candidate-primary-derived-proof-graph','author':'/root/primary_source91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'CANDIDATE_NOT_ACCEPTED_NOT_STATEMENT_SEALED_NOT_PROVED','source':info(primary),'recommendation':info(out/'recommendation92.native.json'),'source_regions':spans,'scope':'Actual first-n complete-history strict-simplex law and its genuine full-A7 consumer boundary; no whole-paper coverage claim.','topology_inputs':'Fixed primary source and this reviewer primary-derived recommendation only. No production Lean read to choose topology. Prior phase91 exposure disclosed in unchanged recommendation.','nodes':nodes,'edges':edges,
'AND_routes':[{'target':'PREFIX92','route':'preferred absolute-coordinate induction','parents':['B92','J92'],'note':'J92 includes genuine one-step law, complete append, Borel tests, simplex sections and product integration; the n-level induction hypothesis is internal to the induction proof.'},{'target':'PREFIX92','route':'alternative relative-vector induction then triangular transport','parents':['REL92','TRI92','K92','E92','FUB92']},{'target':'TERM92','route':'full fixed-count path-functional summand','parents':['PREFIX92','SURV92','ALG92','PATH92']},{'target':'A7','route':'printed cap/simplex series assembly','parents':['TERM92','COUNT92','CAP92']},{'target':'A7','route':'alternative probability-mass/Tonelli assembly','parents':['TERM92','COUNT92','MASS92']}],
'OR_routes':[{'target':'PREFIX92','alternatives':['preferred absolute-coordinate induction','relative-vector induction then triangular transport'],'rule':'Choose one sufficient route; do not make full triangular transport or a standalone unweighted shear an extra premise of the preferred route.'},{'target':'A7','alternatives':['printed cap/simplex absolute-convergence route','nonnegative count-partition/mass-one route with bounded signed decomposition'],'rule':'Retain source route provenance; alternative completion is not an additional source assumption.'}],
'source_hypothesis_equals_binder':{'analytic':['V globally C2','0<alpha','alpha<=beta','Hessian quadratic-form lower/upper bounds everywhere','eta>0','eta<=1/beta'],'typing':['finite Euclidean phase space with Borel sigma algebra','fixed y,r,z0','n natural and T finite nonnegative','Borel ENNReal complete-history test'],'not_binders':['Borel recursion conclusion','conditional density identity','prefix/path correspondence','Tonelli/coordinate certificate','nonexplosion provider','no-atom provider','positive probability of history event','normalization of restricted law']},
'source_vs_ASTIS':{'printed':['H92','O92','I92','D92 strict simplex','A7'],'source_proof_ingredients':['M92','N92','CAP92'],'ASTIS_completion':['T92','W92','K92','Q92','E92','B92','A92','J92','SEC92','PREFIX92','SURV92 composition','ALG92','PATH92','COUNT92','TERM92'],'general_background':['FUB92'],'no_change_to_source':'No additional regularity, continuity of bounce, finite-wait assumption, or whole-path weakening introduced.'},
'genuine_consumer':'PREFIX92 -> TERM92 -> A7 retains arbitrary full-path test dependence via complete histories, terminal survival and actual/prescribed path identification. A terminal-position marginal cannot replace PATH92.',
'canonical_state_mutated':False,'creator_self_independent_approval':False,'needs_distinct_topology_review':True}

rows=[]
def cover(id,region,description,disposition,nodes=None,reason=None):
    row={'id':id,'source_region':spans[region],'source_content':description,'disposition':disposition,'nodes':nodes or []}
    if reason:row['reason']=reason
    rows.append(row)
cover('C92-01','S1.p1','C2 potential, positive ordered curvature constants and global Hessian sandwich.','NODE',['H92'])
cover('C92-02','S2.SS2.p1','Positive eta with eta<=1/beta.','NODE',['H92'])
cover('C92-03','S2.SS2.p1','Augmented joint law, conditional density and Gibbs interpretation.','EXCLUDED',reason='Background setting; this fixed-input prefix law neither draws the reference nor proves augmented invariance.')
cover('C92-04','S3.SS2.p4','Reference center and gradient residual; conditional reference draw is held fixed for the phase-space evolution.','NODE',['O92'])
cover('C92-05','S3.SS2.p4','Expected bounce reduction from a randomized localized reference and generator motivation.','EXCLUDED',reason='Stationary/random-reference cost consumer, not a dependency of a fixed-reference prefix law.')
cover('C92-06','A1.SS1.p1','Actual residual bounce rate, explicit harmonic flow, reflection and zero-normal convention.','NODE',['O92'])
cover('C92-07','A1.SS1.p2','Independent Exp1 clocks and initial record at time zero.','NODE',['I92','B92'])
cover('C92-08','A1.E1','Nonnegative elapsed integrated-hazard closed threshold crossing.','NODE',['I92','W92'])
cover('C92-09','A1.E2','Actual cumulative next time and reflected flowed poststate for finite wait.','NODE',['I92','A92'])
cover('C92-10','A1.SS1.p2','Empty-set infinite wait stops recursion; finite deterministic-depth total record encoding is not specified.','SOURCE_GAP',['T92'],reason='Representational detail omitted by source: explicit absorbing tag may totalize the stopped recursion, but must not invent a finite event after termination.')
cover('C92-11','A1.SS1.p2','Between-event flow on half-open intervals.','NODE',['PATH92'],reason='Future entire-path consumer; preserving full records prepares it but does not itself prove path identity.')
cover('C92-12','A1.SS1.p3','Shifted energy conservation, rate cap, waiting-time lower bound and exponential-sum nonaccumulation.','NODE',['ENERGY92','N92','CAP92'],reason='Required for eventual count exhaustion/source convergence; existing actual-input nonaccumulation78/coverage79 are preserved, not reopened by this preread.')
cover('C92-13','A1.SS1.p3','Memoryless exponential argument for physical-time Markov property and Davis citation.','EXCLUDED',reason='Separate physical-time restart theorem. Deterministic-index fresh-clock prefix induction does not need it.')
cover('C92-14','A1.SS1.p4','Phase density and momentum reversal definitions.','EXCLUDED',reason='Downstream path-reversal/stationarity context; fixed-initial-point prefix law has no initial equilibrium requirement.')
cover('C92-15','A1.Thmtheorem1','Printed reversed-adjoint, invariance, semigroup and averaged-position operator conclusions.','EXCLUDED',reason='Strictly downstream of full A7 and the reversal argument; none is a prefix-law premise.')
cover('C92-16','A1.SS1.SSS0.Px1.p1','Formal generator adjoint heuristic.','EXCLUDED',reason='Source explicitly does not use this heuristic as the rigorous pathwise proof route.')
cover('C92-17','A1.SS1.SSS0.Px1.p2','Warning that the bounce can be discontinuous.','NODE',['O92','M92'],reason='Confirms Borel rather than continuous reflection requirement; forbids adding bounce continuity for convenience.')
cover('C92-18','A1.SS1.SSS0.Px1.p3','A4 density derivative, reversal/flow commutation, A5 reversed jump rates and A6 volume preservation.','EXCLUDED',reason='Ingredients for reversing the completed path law; no need to prove them as parents of finite-prefix density.')
cover('C92-19','A1.Ex19','Strict ordered absolute-time simplex.','NODE',['D92','SEC92'])
cover('C92-20','A1.SS1.SSS0.Px1.p4.2','Prescribed path from initial phase and prescribed ordered times.','NODE',['K92','PATH92'])
cover('C92-21','A1.SS1.SSS0.Px1.p4.2','Iteration sentence suppresses conditional finite-history density induction and Borel parameter tests.','SOURCE_GAP',['W92','Q92','E92','A92','J92','PREFIX92'],reason='Omitted proof expansion, not a claimed false theorem or missing analytic assumption; complete-history strict-prefix identity is the proposed next delta.')
cover('C92-22','A1.Ex19','Simplex-section and finite-product coordinate/Fubini argument is implicit.','SOURCE_GAP',['FUB92','SEC92'],reason='Actual nested integral must be transported to n-fold Lebesgue measure; no supplied Jacobian/certificate binder.')
cover('C92-23','A1.E7','All n pre-bounce rates and survival over the full path horizon, for every bounded measurable path functional.','NODE',['Q92','SURV92','ALG92','PATH92','TERM92','A7'])
cover('C92-24','A1.E7','Empty n=0 term and finite-prefix total-history tests require explicit bookkeeping.','SOURCE_GAP',['B92','PREFIX92'],reason='Empty-product/simplex convention and complete-history measurable tests are ASTIS elaborations; do not silently drop no-event paths.')
cover('C92-25','A1.E7','Last segment survival from t_n to T is implicit in the full-path exponential.','SOURCE_GAP',['SURV92','ALG92'],reason='Separate real composition obligation after prefix law; q_n without this factor describes at least n interior events, not exactly n.')
cover('C92-26','A1.E7','Count-event exhaustion, actual/prescribed full-path agreement and horizon endpoint conversion are suppressed.','SOURCE_GAP',['COUNT92','PATH92','END92'],reason='Need existing actual-input coverage plus new path/count identification; endpoint no-atom proof only if strict and non-strict conventions are equated.')
cover('C92-27','A1.SS1.SSS0.Px1.p4.3','Absolute convergence from bounded test, rate cap and simplex volume.','NODE',['CAP92','A7'])
cover('C92-28','A1.SS1.SSS0.Px1.p4.3','Integration against stationary phase law and reversal preparation.','EXCLUDED',reason='Subsequent A8 consumer; proposed joint Borel dependence prepares integration but does not prove reversal.')
cover('C92-29','A1.E8','Full path and ordered-time reversal.','EXCLUDED',reason='Downstream of A7, not a density-induction prerequisite.')
cover('C92-30','A1.SS1.SSS0.Px1.p4.4','Borel measure-preserving endpoint change of variables despite discontinuous bounce.','EXCLUDED',reason='Supports reversal, not the next strict-prefix simplex law.')
cover('C92-31','A1.SS1.SSS0.Px1.p5','Forward/reversed path weight matching, termwise integration and L2 adjoint extension.','EXCLUDED',reason='Requires completed A7 plus reversal ingredients; no prefix closure credit.')
cover('C92-32','A1.SS1.SSS0.Px1.p6','Contraction and strong continuity.','EXCLUDED',reason='Downstream operator theorem.')
cover('C92-33','A1.SS1.SSS0.Px1.p7','Gaussian momentum averaging removes reversal.','EXCLUDED',reason='Downstream position-operator theorem.')
cover('C92-34','A1.SS2.p1','Averaging over independent conditional reference gives reversible position kernel.','EXCLUDED',reason='Prefix law fixes reference; no averaged-kernel claim.')
cover('C92-35','A1.SS2.p2','Motivation for joint measurability before augmented-space integration.','NODE',['M92','K92'],reason='Joint source-parameter Borel dependence is retained as a conclusion, not a new premise.')
cover('C92-36','A1.Thmtheorem2','Printed jointly measurable half-turn kernel and augmented L2 Markov contraction.','EXCLUDED',reason='Full terminal-kernel/operator theorem is outside prefix target.')
cover('C92-37','A1.SS2.p3','Joint Borel flow/rate/bounce, hazard, rational threshold argument and finite recursive times/poststates.','NODE',['M92','K92','Q92','E92'])
cover('C92-38','A1.SS2.p3','Borel terminal version from nonexplosive finite-jump approximations, default zero where limit fails.','EXCLUDED',reason='Full terminal-state limit construction is not needed for the finite-prefix law; this stated terminal fallback does not silently authorize arbitrary live jump records.')
cover('C92-39','A1.SS2.p4','Integration over conditional reference, Gaussian momentum and clocks to get measurable kernel.','EXCLUDED',reason='Later kernel consumer; prefix target keeps fixed y,r,z0.')
cover('C92-40','A1.SS2.p5','Conditional operator contraction/self-adjointness integrated over y.','EXCLUDED',reason='Downstream functional analysis, no prefix dependency.')
cover('C92-41','A1.E7','Alternative nonnegative count partition and mass-one summation can replace a separate cap summability proof.','SOURCE_GAP',['MASS92'],reason='ASTIS optional alternative route, not an additional printed claim or mandatory source premise. Preserve printed CAP92 route independently.')
cover('C92-42','A1.SS1.p3','The nonexplosive recursion gives a unique process for all nonnegative physical times.','EXCLUDED',reason='Global well-posedness is beyond the finite-prefix theorem. Actual global path/coverage interfaces are later used by PATH92 and COUNT92, without awarding a new global uniqueness proof here.')

nodeids={x['id'] for x in nodes}
assert all(e['from'] in nodeids and e['to'] in nodeids for e in edges)
assert all(n in nodeids for r in rows for n in r['nodes'])
assert set(r['source_region']['html_id'] for r in rows)==set(selected)-{'A1.SS1.SSS0.Px1.p4'}
graph['structural_checks']={'node_ids_unique':len(nodes)==len(nodeids),'edge_endpoints_valid':True,'node_count':len(nodes),'edge_count':len(edges),'is_formal_Lean_graph':False,'induction_cycle_policy':'No graph edge asserts PREFIX92 implies itself. J92 represents a schematic successor proof using the n-level induction hypothesis; B92 and J92 suffice by natural-number induction.'}
write('candidate-source-proof-graph92.native.json',graph)
coverage={'schema_version':1,'record_kind':'candidate-exact-source-coverage-table','author':'/root/primary_source91','status':'CANDIDATE_NOT_INDEPENDENTLY_ACCEPTED','primary':info(primary),'graph':info(out/'candidate-source-proof-graph92.native.json'),'source_regions':spans,'coverage':rows,'coverage_count':len(rows),'source_gap_meaning':'SOURCE_GAP means an omitted proof/representation detail requiring ASTIS completion; it does not assert that the printed author theorem is false or needs stronger assumptions.','bounded_exhaustiveness':'Every mathematical portion of the selected A1 construction, A7 path-iteration neighborhood and A2 measurability/terminal neighborhood is assigned NODE, SOURCE_GAP or EXCLUDED(reason). Source-wide main convergence, implementation and costs are outside this bounded inventory; no whole-paper coverage or compilation claim.','overlap_policy':'Parent paragraph spans intentionally overlap individual equation/paragraph spans. Each row describes its semantic portion; hashes identify exact immutable source bytes, not artificial nonoverlapping line coverage.','uncovered_selected_regions':[],'review_requirements':'Distinct source-topology review should challenge omissions, false AND dependencies, endpoint conventions and complete-path scope before any statement seal. Creator makes no acceptance decision.','prior_native_files_unchanged':old_hashes,'no_canonical_state_change':True}
write('candidate-source-coverage92.native.json',coverage)
manifest={'schema_version':1,'record_kind':'RAW','closed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author':'/root/primary_source91','inputs':[info(primary),info(out/'recommendation92.md'),info(out/'recommendation92.native.json'),info(out/'closed-RAW92.native.json'),info(root/'docs/proof-digestion-protocol.md'),info(root/'.agents/skills/astis-semantic-roundtrip/SKILL.md')],'outputs':[info(out/'candidate-source-proof-graph92.native.json'),info(out/'candidate-source-coverage92.native.json'),info(out/'build-candidate-source-graph92.py')],'stage':'source-derived-candidate-graph-only','production_Lean_read_this_stage':False,'no_prior_files_modified':True,'no_status_or_ledger_write':True,'closure':'This new manifest hashes only new graph/coverage/script outputs and its inputs; prior closed artifacts remain immutable. This manifest excludes itself.'}
write('candidate-graph-closed-RAW92.native.json',manifest)
for n in ['candidate-source-proof-graph92.native.json','candidate-source-coverage92.native.json','candidate-graph-closed-RAW92.native.json']:print(n,sha((out/n).read_bytes()))
