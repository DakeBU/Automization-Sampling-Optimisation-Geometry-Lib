from pathlib import Path
import hashlib, importlib.util, json, os, re, sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
REL='runs/20261007-companion-priority/pbps-recursive-path-preread76'
OUT=ROOT/REL
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def dump(name,o):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n')
 return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l),'LF_recipe':'Only bytewise CRLF -> LF; preserve bare CR and all other bytes.'}
def main():
 b=PRIMARY.read_bytes();assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 helper=ROOT/'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/parse_primary75.py'
 spec=importlib.util.spec_from_file_location('readonly_primary_parser75',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 s=b.decode();parser=m.Parser(s);nodes=parser.nodes
 def offsets(n):return len(s[:n.start].encode()),len(s[:n.end].encode())
 byid={n.id:n for n in nodes if n.id}
 bib=byid.get('bib.bib12')
 assert bib is not None
 ranges=[('standing-original',47160,50640),('eta-domain',95559,96221),('augmentation-same-J',98826,100299),('Qy-reference',103211,105641),('actual-center-residual',254460,255851),('algorithm1',271833,281012),('prop31-consumer',281534,283809),('A1-recursion-and-nonexplosion',534026,564876),('Davis12-bibliographic',*offsets(bib))]
 regions=[];coverage=[];readviews=[]
 for label,lo,hi in ranges:
  dest=OUT/f'source/{label}.exactraw.html';dest.parent.mkdir(exist_ok=True);dest.write_bytes(b[lo:hi])
  region={'id':label,'primary_RAW_range':[lo,hi],'primary_RAW_line_range':[b[:lo].count(b'\n')+1,b[:hi].count(b'\n')+1],'input':pin(dest),'source_url':'https://arxiv.org/html/2609.06905v1'};regions.append(region)
  clo=len(b[:lo].decode());chi=len(b[:hi].decode())
  for n in nodes:
   if not(clo<=n.start and n.end<=chi):continue
   eligible=n.tag in ['p','math'] or n.id.startswith('alg1.l') or (label=='Davis12-bibliographic' and n is bib)
   if not eligible:continue
   if n.id.startswith('alg1.l') and n.tag=='math':pass
   text=n.text();a,z=offsets(n);cls='NODE';role='source definition, condition or deterministic dependency';reason='Required literal context for actual fixed-reference finite recursion; no proof credit.'
   if label=='Davis12-bibliographic':cls='EXCLUDED';role='bibliographic';reason='Only the citation was read; Davis Section 2 is not retrieved or a proof certificate.'
   elif label=='prop31-consumer':cls='EXCLUDED';role='full theorem consumer';reason='Unique nonexplosive homogeneous Markov process, stationarity and output law require later stochastic/path producers.'
   elif n.id in ['alg1.l2','alg1.l8'] or any(x.id in ['alg1.l2','alg1.l8'] for x in n.ancestors()):
    cls='EXCLUDED';role='outer initialization or terminal output';reason='Random reference/Gaussian initialization and x_pi output are outer algorithm consumers; this edge fixes actual y,xRef,z0.'
   elif n.id in ['A1.SS1.p2.m1','A1.SS1.p2.m2']:
    cls='EXCLUDED';role='future stochastic law';reason='Independent Exp(1) realization is deferred; selected structural recursion accepts nonnegative deterministic threshold coordinates.'
   elif n.id in ['A1.SS1.p3.6','A1.Ex8.m1','A1.Ex9.m1','A1.SS1.p3.7','A1.SS1.p3.m6']:
    cls='EXCLUDED';role='future nonaccumulation/Markov result';reason='Finite-wait lower bound, iid sum divergence, all-time process and memorylessness are separate downstream edges.'
   elif n.id in ['A1.SS1.p3.5','A1.SS1.p3.m5']:
    cls='EXCLUDED';role='qualified stochastic zero-cap conclusion';reason='C=0 implies positive-threshold infinite wait, but arbitrary deterministic e=0 still gives tau=0; no unconditional no-jumps claim.'
   elif label in ['augmentation-same-J','Qy-reference']:
    cls='EXCLUDED';role='existing outer conditional-law interface';reason='Q_y and same augmentation J are reusable initialization context, not a premise or dependency of fixed-reference deterministic recursion.'
   elif n.id=='A1.SS1.p2.1':reason='Initial z0,T0 and recursive threshold family are context; iid Exp law is separately excluded by its child rows and remains downstream.'
   elif n.id in ['A1.SS1.p2.m7','A1.SS1.p2.m8']:
    role='finite-arc interface';reason='Record-indexed arc_n(t)=Phi_t(z_n) on the finite outgoing interval. Source zeta_(T_n+t) interpretation requires a later globally stitched source-law path, and is not asserted for arbitrary zero thresholds.'
   elif n.id in ['A1.SS1.p3.3','A1.SS1.p3.m2','A1.SS1.p3.m3','A1.SS1.p3.m4','A1.Ex5.m1','A1.Ex6.m1','A1.SS1.p3.4','A1.Ex7.m1']:
    role='existing energy-cap consumer interface';reason='Lift compiled 73/74 energy preservation and same-energy cap to produced finite states/arcs; no iid nonaccumulation conclusion.'
   elif n.id=='S1.E1.m1':reason='Original Hessian conditions retained; kappa=beta/alpha is source notation and neither a new caller nor a needed recursion premise.'
   row={'item':n.id or f'{label}:{n.tag}:{a}','region':label,'tag':n.tag,'classification':cls,'role':role,'reason':reason,'primary_RAW_range':[a,z],'RAW_bytes':z-a,'RAW_sha256':sha(b[a:z]),'literal':text,'formula_alttext':n.attrs.get('alttext') if n.tag=='math' else None,'source_url':f'https://arxiv.org/html/2609.06905v1#{n.id}' if n.id else 'https://arxiv.org/html/2609.06905v1'}
   coverage.append(row);readviews.append(f"[{row['classification']}] {row['item']} RAW[{a},{z})\n{text}\n")
  # Full exact region bytes partitioned into semantic-bearing intervals and structural residue.
  intervals=sorted((r['primary_RAW_range'] for r in coverage if r['region']==label))
  cuts=sorted(set([lo,hi]+[x for q in intervals for x in q]));parts=[]
  for a,z in zip(cuts,cuts[1:]):
   owners=[r['item'] for r in coverage if r['region']==label and r['primary_RAW_range'][0]<=a and z<=r['primary_RAW_range'][1]]
   parts.append({'primary_RAW_range':[a,z],'kind':'semantic-containing' if owners else 'structural-markup-or-whitespace','semantic_items':owners,'RAW_sha256':sha(b[a:z])})
  region['complete_byte_partition']=parts
 assert len({r['item'] for r in coverage})==len(coverage)
 counts={'regions':len(regions),'items':len(coverage),'math_items':sum(r['tag']=='math' for r in coverage),'NODE':sum(r['classification']=='NODE' for r in coverage),'EXCLUDED':sum(r['classification']=='EXCLUDED' for r in coverage)}
 dump('source.regions.json',{'schema':'finite-exact-source-regions-v1','primary':pin(PRIMARY),'range_convention':'zero-based RAW byte half-open, before LF normalization','regions':regions,'scope':'Only these finite regions; no full-paper coverage claim.'})
 dump('source.coverage.json',{'schema':'source-only-typed-finite-coverage-v1','counts':counts,'classification_credit':'NODE means source-side dependency or finite consumer interface, never proved/completed. EXCLUDED has a local reason. Overlapping paragraph/math rows are semantic granularity, not duplicated byte-coverage claims.','items':coverage})
 (OUT/'source.readable.txt').write_bytes(('\n'.join(readviews)).encode())
 api_specs=[
 ('actual73-flow','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',20,69,'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws','existing deterministic API; no rerun'),
 ('actual74-bounce-cap','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',16,72,'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws','existing deterministic API; no rerun'),
 ('actual-Qy-same-J','AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',28,44,'AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel','existing initial-reference conditional law; not terminal algorithm kernel'),
 ('actual-augmentation-J','AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianAugmentation.lean',18,33,'AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianAugmentation.augmentation_eq_withDensity','joint density relative to mu.prod volume; Gibbs density insertion separate'),
 ('measurable-piecewise-iteration','.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Basic.lean',293,330,'Measurable.iterate; Measurable.ite','retrieved API source only; no recursion implementation'),
 ('measurable-threshold-sequence','.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean',578,600,'measurable_pi_iff; measurable_pi_apply; measurable_pi_lambda','retrieved API source only'),
 ('iid-product-deferred','.lake/packages/mathlib/Mathlib/Probability/Independence/InfinitePi.lean',125,137,'ProbabilityTheory.iIndepFun_infinitePi','later stochastic interface only, not selected edge')]
 apis=[]
 for label,path,start,end,decl,credit in api_specs:
  p=ROOT/path;raw=p.read_bytes();lines=raw.splitlines(keepends=True);frag=b''.join(lines[start-1:end]);dest=OUT/f'API/{label}.exactraw.fragment';dest.parent.mkdir(exist_ok=True);dest.write_bytes(frag)
  apis.append({'name':label,'declaration':decl,'start_line':start,'end_line':end,'whole_source':pin(p),'fragment':pin(dest),'credit':credit})
 dump('API.regions.json',{'schema':'bounded-existing-API-fragments-v1','regions':apis,'searched_but_not_certified':['Measurable finite/top branch and finite extraction from WithTop NNReal: exact adapter remains internal obligation.','Natural-number indexed measurable recursion can be proved by induction; Measurable.iterate only applies after choosing a homogeneous extended state.','Exp mean/integrability and almost-sure sum divergence are deferred, not inferred from iIndepFun_infinitePi.'],'negative_searches':['No reusable finite/top adapter or Option-recursion theorem was located in the narrowly searched source files. This is not a repository-wide absence claim.','Continuous-time clock may not use hittingAfter_le_iff requiring WellFoundedLT; Nat induction here is on jump index only.']})
 original_inputs=[
 {'name':'hα','meaning':'0 < alpha','class':'SOURCE'}, {'name':'hαβ','meaning':'alpha <= beta','class':'SOURCE'},
 {'name':'hV','meaning':'V is C^2 on the whole finite-dimensional real Hilbert space','class':'SOURCE'},
 {'name':'hH','meaning':'for every x,v, alpha*||v||^2 <= HessV(x)[v,v] <= beta*||v||^2','class':'SOURCE'},
 {'name':'hη','meaning':'0 < eta','class':'SOURCE'}, {'name':'hβη','meaning':'beta*eta <= 1','class':'SOURCE'}]
 route=[
 'Fix the original analytic data and actual y,xRef,z0. Define a stopped finite-event record, base (T0,z0)=(0,z0); document which stored fields are merely inactive bookkeeping.',
 'At an active record use the prospective actual75 tau(y,xRef,z_n,e_(n+1)); test tau=top. A top wait stops further postjump production and never evaluates Phi at infinity.',
 'For a finite wait s, set T_(n+1)=T_n+s and z_(n+1)=S_xRef(Phi_s^(y,xRef)(z_n)); prove the guarded update jointly Borel from actual75 joint Borel tau, actual73 joint continuous Phi and actual74 joint Borel S.',
 'Recurse on the natural jump index for every finite n. Prove joint Borel dependence on y,xRef,z0 and the product-Borel nonnegative threshold sequence by induction; stopped records stay stopped.',
 'Inductively preserve H_y,xRef(z_n)=H_y,xRef(z0) on actual active records, using actual73 flow preservation and actual74 bounce preservation. Lift the existing same-energy envelope to actual produced arcs.',
 'Expose exact finite-arc and stop interfaces, zero-threshold legality and positive-threshold zero-cap infinite wait. No strict event-time growth or single physical-time phase function is asserted for arbitrary threshold sequences with zero waits.',
 'Stop at the finite recursive skeleton. Supply its exact original-energy invariant to a separate future iid-Exp/product-law plus nonaccumulation edge; full all-time path and Markov/invariance consumers remain open.'
 ]
 contract={
 'schema':'bounded-prospective-source-contract-v1','task':'PBPS recursive actual finite postjump skeleton preread76','status':'SOURCE_PLAN_ONLY_NO_HEADER_NO_PROOF_NO_SAU',
 'selected_single_edge':'Actual fixed-reference finite stopped postjump recursion with joint Borel dependence and inherited same-initial-energy invariant.',
 'not_selected':'iid Exp thresholds plus actual uniform cap imply nonaccumulation; that needs this actual recursive-state producer first.',
 'selection_reason':'A.2 updates the actual state entering the next A.1 hazard. Compiled73/74 and prospective75 do not yet produce that recursive state. A waiting-time sum theorem on assumed states/caps would leave the algorithm producer missing.',
 'proposed_declaration_semantics':{'suggested_name':'actual_fixed_reference_finite_jump_recursion','not_a_statement_seal':True,'analytic_callers':original_inputs,'typing':'E finite-dimensional real inner-product space with its Borel measurable structure; rank zero is admitted; alpha,beta nonnegative reals; no Nontrivial E or alpha*eta<1.','data_universally_quantified_inside_conclusion':['y : E','xRef : E','z0 : E x E','e : Nat -> NNReal','n : Nat'],'random_law_binder':None,'definitions':['c=y-eta*gradient V xRef','h(x)=gradient V x-gradient V xRef','Phi_t is exactly actual73/A1.Ex2','S(x,p)=(x,R_h(x)p), R_0=identity, exactly actual74/A1.Ex3','lambda=sqrt(eta)*max(0,inner(p,h(x)))','H=(eta^(-1)*||x-c||^2+||p||^2)/2','tau is the actual75 integrated-hazard threshold time in WithTop NNReal, conditional on that future edge being compiled/admitted'],'record_semantics':'Any reviewed total representation may carry an active finite (time,state) and a stopped marker. A stopped marker has event time infinity and no postjump phase at infinity; preserving the last finite anchor for later flow is bookkeeping, never an actual zeta_infinity. No representation or Lean signature is sealed here.','conclusions':['Base T0=0,z_0=z0.','At every active finite n, finite tau gives exact A.2 next time and actual S(Phi_tau z_n); top tau stops and every subsequent event record remains stopped.','For each finite n, the record/event-time map is jointly Borel in y,xRef,z0,e with product Borel on threshold coordinates, for fixed V,eta and analytic data.','Every active postjump state and each actual outgoing finite flow arc has the original energy H(z0); existing74 cap therefore applies uniformly with C computed from z0, not a newly assumed state/cap.','Record-indexed outgoing arc_n(t)=Phi_t(z_n) for 0<=t<tau. Source zeta_(T_n+t) interpretation is deferred to a stitched source-law path; arbitrary zero thresholds may share event times, so this edge asserts no global phase function.'],'forbidden_extra_public_premises':['arbitrary Phi/S/rate/tau law providers','Lipschitz gradient as caller','joint continuity of S','nonexplosion/invariance or a terminal Markov kernel','unbounded hazard or almost-sure finite waits','uniform cap assumed for an arbitrary sequence of states','iid or integrable arbitrary random variables as added original analytic callers','refresh mechanism','strictly positive thresholds for this deterministic structural edge']},
 'source_anchors':['A1.E1','A1.E2','A1.SS1.p2.2','A1.Ex4','A1.SS1.p3.2','A1.Ex6','A1.Ex7','alg1'],
 'true_parents':[{'declaration':apis[0]['declaration'],'status':'existing current deterministic API inspected, not recompiled here'},{'declaration':apis[1]['declaration'],'status':'existing current deterministic API inspected, not recompiled here'},{'declaration':'prospective75 actual integrated-hazard single-clock result','status':'SOURCE/MATH/SEAL prospective acceptance reported by root; NOT claimed/proved/compiled. Candidate76 cannot begin implementation until available or separately authorized.'}],
 'outer_initialization_reuse':{'declaration':apis[2]['declaration'],'same_J':'J = map ((x,z)->(x,x+sqrt(eta) z)) (mu.prod stdGaussian); (J.map swap).IsCondKernel R','exact_fiber':'R(y)=mu.tilted(x -> -||x-y||^2/(2eta)); for source Gibbs mu this yields Q_y density proportional to exp(-V(x)-||x-y||^2/(2eta)), with Gibbs density substitution kept explicit.','not_formal_parent':'Fixed-reference finite recursion needs no Q_y draw. Q_y enters outer Algorithm1 initialization, and is not its returned x_pi/half-turn kernel.'},
 'constants_and_domains':{'times':'finite waits and local arc times in NNReal; event/wait infinity in WithTop NNReal; Phi accepts real finite coe only','E0':'H_y,xRef(z0)>=0, including E0=0','C0':'sqrt(eta)*beta*sqrt(2E0)*(sqrt(2eta E0)+||c-xRef||)>=0','zero_cap':'C0=0 and e_(n+1)>0 gives infinite wait, using future75. With e=0, tau=0 even when C0=0; no deterministic no-jumps conclusion.','rank_zero':'E may have rank0. Actual residual and rate then vanish; positive thresholds wait forever, zero thresholds may produce zero-time identity updates.','boundary_alpha_eta':'alpha*eta=1 allowed; no strict-boundary exclusion.','threshold_index':'Source E_1 generates first successor; a zero-based Lean sequence e n denotes source E_(n+1).','integrability':'Finite-interval integrability of the actual lambda(Phi_s z) must come from actual continuous-rate/flow plus future75 internal bridge. No initial-law moments are needed for deterministic finite skeleton.'},
 'route_at_most_seven_steps':route,
 'separable_next_interface':{'inputs':'Produced finite records, exact H=H0, actual75 lower wait bound and its zero-cap branch; canonical iid Exp(1) coordinates with law/support/integrability proved internally.','future_result':'On the source iid realization, either recursion stops with infinite wait or T_n tends to infinity a.s.; only then stitch a process for all t>=0.','conditions_not_added_to_original_callers':'iid, unit mean, integrability, positivity a.s. and SLLN are construction/library proof ingredients. C0=0 is a separate case, not excluded by a C0>0 binder.'},
 'remaining_boundary':['75 actual single-clock proof/compile is pending.','Selected76 has no candidate Lean/header, proof search, implementation or compile.','Measurable finite/top extraction and stopped-record representation require internal adapters.','iid Exp law, positive support, integrability/mean and SLLN nonaccumulation remain separate.','Full all-time path evaluation, uniqueness, cadlag/PDMP and memoryless homogeneous Markov property remain open.','Stationarity/reversal, Algorithm1 returned x_pi, real H/K/r_rho/B27/B28, mixing/main/error/cost/composition and full Exposition/PURIFIED/Goal remain uncredited.','Davis[12] is bibliographic only; its Section2 mathematical text was not read.']}
 dump('selected.contract.json',contract)
 # Source-side topology: paper dependency and missing bridge labels, not a Lean import/declaration graph.
 node_specs=[
 ('N01','original standing analytic data','SOURCE', ['S1.p1.1','S1.E1.m1','S2.SS2.p1.1']),
 ('N02','fixed y,xRef and initial z0,T0','SOURCE',['A1.SS1.p1.1','A1.SS1.p2.m3','A1.SS1.p2.m4']),
 ('N03','actual center and residual h','SOURCE',['S3.E4.m1']),
 ('N04','actual harmonic Phi','SOURCE',['A1.Ex2.m2']),
 ('N05','actual zero-safe bounce S','SOURCE',['A1.Ex3.m2','A1.SS1.p1.3']),
 ('N06','actual continuous rate lambda','SOURCE',['A1.Ex1.m1']),
 ('N07','actual integrated hazard single clock','FUTURE75_UNPROVED',['A1.E1.m2']),
 ('N08','finite/top stopped update semantics','INTERNAL_BRIDGE_OPEN',['A1.E2.m2','A1.SS1.p2.2']),
 ('N09','joint Borel guarded postjump update','INTERNAL_BRIDGE_OPEN',['A1.E2.m2']),
 ('N10','all finite-index stopped recursion and joint Borel dependence','SELECTED_MISSING_PRODUCER',['A1.E2.m2','A1.SS1.p2.2']),
 ('N11','same original weighted energy H','SOURCE',['A1.Ex4.m1']),
 ('N12','flow and bounce energy preservation','EXISTING73_74',['A1.SS1.p3.2']),
 ('N13','produced active records/arcs preserve H(z0)','SELECTED_INDUCTION_INVARIANT',['A1.SS1.p3.2']),
 ('N14','same-energy uniform C0 and finite-arc bound','EXISTING74_CONSUMER_INTERFACE',['A1.Ex5.m1','A1.Ex6.m1','A1.Ex7.m1']),
 ('N15','iid Exp(1) thresholds and positive/integrable unit law','DEFERRED_STOCHASTIC_CONSTRUCTION',['A1.SS1.p2.m1','A1.SS1.p2.m2']),
 ('N16','finite waiting lower bound and iid sum divergence','DEFERRED_NONACCUMULATION',['A1.Ex8.m1','A1.Ex9.m1']),
 ('N17','nonaccumulation plus globally stitched path','DEFERRED_PROCESS',['A1.SS1.p3.7']),
 ('N18','homogeneous Markov, stationarity and Algorithm1 output','EXCLUDED_FULL_CONSUMER',['A1.SS1.p3.7','alg1.l8']),
 ('N19','same J and Q_y initial-reference kernel','EXISTING_OUTER_INITIALIZATION',['S2.E7.m1','S2.E8.m1','alg1.l2'])]
 graph_nodes=[{'id':i,'meaning':meaning,'status':status,'source_items':anchors,'public_extra_binder':False} for i,meaning,status,anchors in node_specs]
 edge_specs=[('N01','N03','gradient regularity under original callers'),('N02','N03','fixed reference/center data'),('N03','N04','same c in harmonic flow'),('N03','N05','same h in actual reflection'),('N03','N06','same h in rate'),('N04','N07','hazard integrates actual flow'),('N06','N07','hazard integrates actual rate'),('N07','N08','finite or infinite actual wait'),('N04','N08','finite flow only'),('N05','N08','actual reflection after finite flow'),('N08','N09','guarded branch/extraction adapter'),('N04','N09','joint Borel from joint continuous Phi'),('N05','N09','joint Borel S, not continuous S'),('N07','N09','joint Borel actual tau from future75'),('N02','N10','base actual input state'),('N08','N10','Nat recursion at event index'),('N09','N10','finite-index measurable induction'),('N03','N11','same centered energy'),('N04','N12','flow preserves H'),('N05','N12','bounce preserves H'),('N11','N12','exact weighted sum convention'),('N10','N13','active actual states produced'),('N12','N13','induction, not a new caller'),('N13','N14','same initial-energy envelope along produced arcs'),('N07','N16','future75 wait lower bound'),('N14','N16','uniform actual C0'),('N15','N16','iid support/moments and SLLN'),('N10','N17','actual finite histories to be stitched'),('N16','N17','rules out finite-time accumulation'),('N17','N18','well-defined all-time process needed'),('N19','N18','outer reference initialization only')]
 graph_edges=[{'id':f'E{k:02d}','producer':a,'consumer':z,'meaning':why,'truth':'source dependency/required bridge, not new formal Lean implication'} for k,(a,z,why) in enumerate(edge_specs,1)]
 graph={'schema':'source-proof-graph-bounded-preread-v1','nodes':graph_nodes,'edges':graph_edges,'counts':{'nodes':len(graph_nodes),'edges':len(graph_edges)},'selected_nodes':['N08','N09','N10','N13'],'stochastic_downstream_separate':['N15','N16','N17','N18'],'no_rewrite_of_prior_graphs':True,'source_vs_Lean':'Source-side semantic requirements and paper omissions are recorded independently. Existing compiled APIs are candidates supplying parts; no map promotes the entire graph to Lean truth.'}
 dump('source-proof-graph.json',graph)
 obligations=[
 ('O01','Exact actual c,h,Phi,S,rate,H/tau identity with73/74/future75; same original y,xRef and eta.','OPEN_INTERNAL_IDENTITY_ADAPTER'),
 ('O02','Choose and expose a total stopped record without treating any default finite value or cemetery field as zeta_infinity.','OPEN_INTERNAL_REPRESENTATION'),
 ('O03','Measurable {tau=top}, finite extraction/coercion under guard, and measurable branch/state encoding.','OPEN_INTERNAL_BOREL_ADAPTER'),
 ('O04','Joint Borel S(Phi_tau z) on finite branch; do not request joint S continuity.','OPEN_SELECTED_MEASURABILITY'),
 ('O05','Natural-index recursion with exact first-threshold indexing and absorbing stopped branch.','OPEN_SELECTED_PRODUCER'),
 ('O06','Joint Borel finite records in all initial/reference data and threshold sequence coordinates.','OPEN_SELECTED_INDUCTION'),
 ('O07','H(record_n)=H(z0) on active records and outgoing arcs from actual73/74; no assumed arbitrary-state invariant.','OPEN_SELECTED_INVARIANT'),
 ('O08','Apply existing74 C0 bound to produced same-energy arcs, finite integrability/primitive from future75, preserving all factors.','OPEN_CONSUMER_ADAPTER'),
 ('O09','Explicit e=0, zero-rank, zero-energy and C0=0/+threshold versus zero-threshold branches.','OPEN_BOUNDARY_OBLIGATION'),
 ('O10','Future75 actual single-clock theorem must be proved/admitted before implementation relying on it.','PENDING_TRUE_PARENT'),
 ('O11','iid Exp product realization, support positivity, mean/integrability and SLLN, not analytic caller additions.','DEFERRED_STOCHASTIC_EDGE'),
 ('O12','Nonaccumulation/stitching/all-time path and memoryless Markov/uniqueness.','DEFERRED_PROCESS_EDGE')]
 expectations={'schema':'independent-source-first-expectations-v1','frozen_before_any76_header_or_body':True,'exposure':{'prior_exposure':'Reviewer has reviewed70-74 whole modules and75 prospective source/header, including source A1 and current deterministic parents. This is not source-blind.','current_75_implementation':'No75 BODY exists as an authorized input; no75 proof/compile credit.','future76':'No candidate header, implementation, other reviewer verdict or proof is an input.'},'single_scope':contract['selected_single_edge'],'original_six_callers':original_inputs,'obligations':[{'id':i,'meaning':meaning,'status':status,'must_be_public_binder':False} for i,meaning,status in obligations],'source_coverage':counts,'source_graph':graph['counts'],'required_review_rules':['actual-input finite recursion, not a tuple of arbitrary state/clock providers','source ingredient remains internal bridge/dependency, never new original public hypothesis','time top guard prohibits evaluating Phi at infinity','all nonnegative threshold sequences allowed; arbitrary zeros disprove any claimed unconditional strict-increase/nonaccumulation','stochastic construction and fixed-reference deterministic data kept separate','original weighted SUM energy, not product norm or newly variable cap','source zero-cap no-jumps statement is interpreted on positive Exp thresholds/a.s. source realization'],'unit_threshold_api':'Actual Exp(1) is ProbabilityTheory.expMeasure (1 : Real), but selected edge carries deterministic NNReal coordinates and no probability law.','route':route}
 dump('source-first.expectations.json',expectations)
 negatives={'schema':'bounded-observer-negatives-v1','retained':['Initial guessed AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianConditionalKernel.lean path absent; corrected by rg --files to TechnicalLemmas/Probability/GaussianConditionalKernel.lean.','Guessed own old close_baseline75.py path absent; not read. Old bundle untouched.','Targeted measurable Option/untop search returned no matching adapter in the bounded files; no global absence claim.'],'actual_PID_for_shell_locator_negatives':'Not exposed by tool; not guessed.','no_failed_proof_attempts':True,'no_background_execution':True}
 dump('observer-negatives.json',negatives)
 # Finite pins only for reusable native contracts; do not embed or recursively copy their payloads.
 reused_paths=[
 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/lease.final.json',
 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/source-first.expectations75.json',
 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75/source-literal-vs-inherited-bridges75.json',
 'runs/20261007-companion-priority/pbps-clock-construction-preread75/source.regions.json',
 'runs/20261007-companion-priority/pbps-clock-construction-preread75/API.regions.json',
 'runs/20261007-companion-priority/pbps-clock-construction-preread75/API/continuous-time-API-limit.exactraw.lean-fragment',
 'runs/20261007-companion-priority/pbps-clock-construction-preread75/API/SLLN-contract.exactraw.lean-fragment']
 reused=[]
 for path in reused_paths:
  p=ROOT/path
  if p.exists():reused.append({**pin(p),'role':'read-only finite prior source/API context; not prior mathematical acceptance evidence'})
  else:print('OPTIONAL_REUSED_LOCATOR_ABSENT',path)
 inputs={'schema':'finite-source-planning-inputs-v1','primary':pin(PRIMARY),'primary_parser':pin(helper),'source_slices':[r['input'] for r in regions],'API_fragments':[a['fragment'] for a in apis],'API_whole_sources_opaque_pins':[a['whole_source'] for a in apis],'reused_native_finite_pins':reused,'no_recursive_payloads':True,'current_mutable_75_or_76_inputs':[],'logical_scope':'source-side preread, not current global ledger/admin/site state'}
 dump('inputs.manifest.json',inputs)
 decision={'schema':'bounded-source-preread-decision-v1','verdict':'SELECT_ACTUAL_FINITE_STOPPED_POSTJUMP_RECURSION_ONLY','selected_contract':f'{REL}/selected.contract.json','readiness':'Conditional future planning only;75 not proved/compiled,76 not claimed or sealed.','source_inventory_counts':counts,'source_graph_counts':graph['counts'],'obligation_count':len(obligations),'selected_new_stochastic_results':0,'selected_new_headers_or_Lean_bodies':0,'original_analytic_callers':6,'new_analytic_callers':0,'future_route_steps':len(route),'no_compile_credit':True,'no_source_header_acceptance':True,'no_verified_or_reader_or_purified_or_goal_credit':True,'blocking_before_any76_implementation':'The actual75 single-clock producer must be available; selected76 also needs internally proved finite/top and recursion measurability adapters.','remaining_boundary':contract['remaining_boundary']}
 dump('decision.json',decision)
 review={'schema':'complete-named-source-preread-review-v1','bounded_synthesis':'Select actual A.2 finite stopped postjump recursion, with joint Borel dependence and the inherited same-initial-energy invariant. The deterministic73/74 APIs and prospective75 single-clock do not themselves produce the recursively updated actual states. iid nonaccumulation is a later consumer of this exact producer.','source_precision':{'source_formula':'T_(n+1)=T_n+S_(n+1); z_(n+1)=S_xRef(Phi_(S_(n+1))^(y,xRef)(z_n)) only for finite wait.','stop_formula':'Empty hitting set gives next wait/eventtime infinity and stops recursion; no phase at infinity.','rate':'sqrt(eta)*max(0,inner(p,gradient V x-gradient V xRef))','energy':'(eta^-1*||x-c||^2+||p||^2)/2','cap':'sqrt(eta)*beta*sqrt(2H(z0))*(sqrt(2eta H(z0))+||c-xRef||)','positive_threshold_zero_cap':'infinite wait; e=0 remains legal and gives zero wait','horizon':'Algorithm1 asks for phase evolution until pi and returns x_pi, a full-path consumer not provided by a finite recursive skeleton'},'existing_vs_open':{'existing':'actual73 full joint continuous/Borel harmonic flow and conservation; actual74 joint Borel zero-safe bounce, continuous rate and same-energy envelope; existing selected Q_y disintegration of same J','prospective_only':'75 single-clock source/header/seal acceptance, no proof/compile','selected_open':'finite/top guarded postjump producer and measurable natural-index recursion, active-state energy induction','deferred':'iid Exp realization/support/moments/SLLN, nonaccumulation and all-time path, memorylessness/Markov/invariance/main/cost'},'source_vs_implementation':'The new graph is a source planning graph, independently identified from fixed RAW A1.1/A1.2 and algorithm boundaries. Current parent signatures only supply named pieces; no76 candidate or BODY exists in this review.','coverage':counts,'source_graph_counts':graph['counts'],'finite_input_manifest':f'{REL}/inputs.manifest.json','contract':f'{REL}/selected.contract.json','expectations':f'{REL}/source-first.expectations.json','all_obligations':expectations['obligations'],'bounded_API_result':apis,'Davis':'Only bibliographic entry/citation was read. No Davis Section2 source, license or theorem is used as proof.','exposure':expectations['exposure'],'negative_observers':negatives,'truth_boundary':decision['remaining_boundary']}
 dump('review.json',review)
 synthesis='''Selected next edge: actual finite stopped postjump recursion (A.2), with joint Borel dependence and the same initial weighted energy.\n\nThe earliest missing producer is the actual next state S(Phi_tau(z_n)), guarded by a finite actual75 wait, and its natural-index recursion. A source-correct arbitrary-sequence structural result permits e=0 and therefore cannot assert strict event-time growth or nonaccumulation. tau=top stops postjump production; it never supplies a phase at infinity.\n\n73 and74 supply the deterministic actual flow/bounce/rate/energy pieces. 75 is prospective only, not compiled. The existing Q_y kernel disintegrates the same Gaussian augmentation J and serves only outer initialization; it is neither a formal fixed-reference recursion parent nor the returned x_pi kernel.\n\nAfter this edge, a separate iid Exp(1) construction can consume its actual H(z0) invariant and uniform cap, handle C=0, use positivity/integrability/SLLN, and prove no finite-time accumulation. Only then may a full all-time process be stitched. No refresh, arbitrary terminal kernel, extra caller, new Statement Seal, Lean proof, reader/VERIFIED/PURIFIED/main/cost/Goal credit is given here.\n'''
 (OUT/'bounded-synthesis.txt').write_bytes(synthesis.encode())
 dump('build.receipt.json',{'schema':'actual-foreground-terminal-receipt-v1','actual_PID':os.getpid(),'actual_EXIT':0,'command':'python -B build76.py','source_coverage_counts':counts,'source_graph_counts':graph['counts'],'API_whole_content_files':len(apis),'route_steps':len(route),'write_scope':REL,'old_closed_writes':0,'canonical_writes':0,'compilations':0,'background_processes':0})
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'counts':counts,'graph':graph['counts'],'API_files':len(apis),'obligations':len(obligations),'contract_RAW':pin(OUT/'selected.contract.json')['RAW_sha256']},ensure_ascii=False))
if __name__=='__main__':main()
