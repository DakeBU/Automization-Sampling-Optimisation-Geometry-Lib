from pathlib import Path
from collections import Counter
import json,hashlib,re,html,os,sys,base64
from parse_primary75 import primary,Node
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib'); OWN=Path(__file__).resolve().parent
PRE=ROOT/'runs/20261007-companion-priority/pbps-clock-construction-preread75'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def dump(name,x):
 p=OWN/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());return pin(p)
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def load(p):return json.loads(p.read_bytes())
def main():
 assert not (OWN/'lease.final.json').exists(),'Never reopen CLOSED'
 raw=PRIMARY.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760' and len(raw)==1482128
 s,p=primary();byid={n.id:n for n in p.nodes if n.id}
 lease=load(PRE/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['owned_count']==86
 for e in lease['all_owned_outputs_except_only_self']:
  assert pin(ROOT/e['path'])==e,e['path']
 oldrun=load(PRE/'run.json');oldclaimed=oldrun.pop('run_sha256');assert sha(canon(oldrun))==oldclaimed==lease['whole_logical_run_sha256']
 inputs=[]
 def inputfile(path,kind,snapshot=True):
  a=pin(path);a['kind']=kind
  if snapshot:
   target=OWN/'inputs'/f'{len(inputs):02d}.{path.name}.RAW';target.parent.mkdir(exist_ok=True);target.write_bytes(path.read_bytes());a['snapshot']=pin(target)
  inputs.append(a);return a
 inputfile(PRIMARY,'fixed_full_primary_reference_only',False)
 for name in ['selected.contract.json','source-first.expectations.json','source.regions.json','API.regions.json','decision.json','run.json','lease.final.json']:
  inputfile(PRE/name,'CLOSED86_prospective_source_or_provenance',True)
 api=load(PRE/'API.regions.json')['regions']
 api_review=[]
 api_uses={
 'hitting-definition':('DEFINITION_ONLY','Canonical hittingAfter explicitly branches to top when the hit set is empty. Its general definition has no WellFoundedLT requirement.'),
 'continuous-time-API-limit':('FORBIDDEN_ROUTE','hittingAfter_le_iff shown here assumes WellFoundedLT; NNReal/Real continuous time is not a permissible instance for this route.'),
 'discrete-stopping-limit':('EXCLUDED','Discrete WellFoundedLT stopping-time bridge is not a continuous-time first-crossing producer.'),
 'joint-hazard-continuity':('POSSIBLE_INTERNAL_API','continuous_parametric_primitive_of_continuous requires joint continuity; supply it from SAME actual rate composed with SAME actual flow, never a caller.'),
 'integral-cap':('POSSIBLE_INTERNAL_API','integral_mono_on requires ordered endpoints and IntervalIntegrable actual integrand/constant; derive these on compact finite intervals.'),
 'Borel-clock-criterion':('POSSIBLE_INTERNAL_API','measurable_of_Iic can use independently proved finite-time clock sublevel identity, with separate trivial top sublevel. Order/Borel typeclass requirements must be discharged.'),
 'closed-first-crossing':('POSSIBLE_INTERNAL_API','IsClosed.csInf_mem/isLeast_csInf require nonempty and bounded below crossing set; NNReal lower bound0 and continuity supply them. This is a missing local bridge, not a supplied source premise.'),
 'actual-Exp-law':('DEFINITION_ONLY','Actual pinned API is expMeasure (1 : Real), not a declaration named expMeasure1 in this slice. Positivity of rate1 is internal; no original caller added.'),
 'Exp-CDF':('POSSIBLE_INTERNAL_API','cdf_expMeasure_eq at rate1 gives support/zero atom/survival after real-to-nonnegative threshold transport; no iid/moment/integrability premise needed for the one-clock law.'),
 'iid-clock-realization':('EXCLUDED_FUTURE','Product-space iid realization is needed only for the future event recursion, not for one actual Exp marginal pushforward.'),
 'SLLN-contract':('EXCLUDED_FUTURE','strong_law_ae_real needs integrability, pairwise independence and identical laws. Those are future internally discharged probabilistic obligations; not new original callers.')}
 for a in api:
  q=ROOT/a['literal_RAW_span']['path'];assert pin(q)==a['literal_RAW_span']
  src=ROOT/a['whole_source']['path'];assert pin(src)==a['whole_source']
  fragment=b''.join(src.read_bytes().splitlines(keepends=True)[a['start_line']-1:a['end_line']]);assert fragment==q.read_bytes()
  inp=inputfile(q,'CLOSED86_bounded_API_signature')
  status,reason=api_uses[a['name']];api_review.append({**a,'classification':status,'independent_reason':reason,'whole_API_opaque_pin_verified':True,'exact_line_recipe':'RAW splitlines(keepends=True)[start_line-1:end_line], no newline normalization before slicing','input':inp})
 regions=[]
 for r in load(PRE/'source.regions.json')['regions']:
  lo=sum(map(len,raw.splitlines(keepends=True)[:r['start_line']-1]));hi=sum(map(len,raw.splitlines(keepends=True)[:r['end_line']]))
  assert raw[lo:hi]==(ROOT/r['literal_RAW_slice']['path']).read_bytes()
  inp=inputfile(ROOT/r['literal_RAW_slice']['path'],'CLOSED86_exact_primary_region')
  regions.append({'region_id':r['anchor'],'RAW_range':[lo,hi],'RAW':inp,'origin':'CLOSED86 exact RAW primary line slice independently rechecked','source_URL':'https://arxiv.org/html/2609.06905v1#'+('S3' if r['anchor']=='algorithm-and-prop31' else 'A1' if r['anchor']=='appendixA1-construction' else 'bib.bib16')})
 for nodeid in ['S1.p1.1','S1.E1','S2.SS2.p1.1']:
  n=byid[nodeid];lo=len(s[:n.start].encode());hi=len(s[:n.end].encode());d=raw[lo:hi]
  q=OWN/'source-supplements'/f'{nodeid}.RAW.html';q.parent.mkdir(exist_ok=True);q.write_bytes(d)
  regions.append({'region_id':nodeid,'RAW_range':[lo,hi],'RAW':pin(q),'origin':'Independent minimal original standing-condition supplement from SAME fixed primary','source_URL':'https://arxiv.org/html/2609.06905v1#'+nodeid})
 # The source graph is hand authored from RAW mathematics, before any75 candidate.
 nd=[
 ('N01','SOURCE_HYPOTHESES','Original six analytic callers and finite real Hilbert/Borel carrier',['S1.p1.1','S1.E1','S2.SS2.p1.1'],'Six source standing assumptions retained; dimension may be0 and alpha*eta=1.'),
 ('N02','SOURCE_DEFINITION','SAME actual center and residual gradient',['S3.E4'],'c=y-eta gradV(xRef); h(x)=gradV(x)-gradV(xRef).'),
 ('N03','SOURCE_INGREDIENT','SAME actual harmonic flow',['A1.Ex2','S3.E8'],'Exact two-component flow for all real times, joint continuity; future reuse of actual73 is a proof edge, not a public parameter.'),
 ('N04','SOURCE_INGREDIENT','SAME actual residual bounce rate',['A1.Ex1','S3.E9','A1.SS1.p1.3'],'sqrt(eta)*max(inner(p,h(x)),0); nonnegative, jointly continuous; zero residual gives zero instantaneous rate.'),
 ('N05','SOURCE_CONTEXT','Actual bounce with R0=I',['A1.Ex3','alg1.l7'],'No refresh event; discontinuous S at zero normal is allowed; this is not a continuity premise for clock.'),
 ('N06','SOURCE_DEFINITION','SAME weighted SUM harmonic energy',['A1.Ex4'],'H=((1/eta)*norm(x-c)^2+norm(p)^2)/2>=0; not product norm or arbitrary supplied energy.'),
 ('N07','SOURCE_INGREDIENT','Actual flow conserves H',['A1.SS1.p3.2'],'One deterministic orbit conserves its starting energy; this alone is not global random-path conservation.'),
 ('N08','SOURCE_INGREDIENT','Exact cap on a SAME energy layer',['A1.Ex5','A1.Ex6'],'C_E=sqrt(eta)*beta*sqrt(2E)*(sqrt(2eta E)+norm(c-xRef)); no unknown multiplicative constant.'),
 ('N09','ASTIS_INTERNAL_BRIDGE','Actual hazard integrand',['A1.E1'],'q(a,s)=lambda_xRef(Phi_s^(y,xRef)(z)); joint continuous/nonnegative from actual producers.'),
 ('N10','ASTIS_INTERNAL_BRIDGE','Finite-interval integrability and joint primitive',['A1.E1'],'Lambda(a,t)=integral_0^t q(a,s) ds on nonnegative time; joint continuous/Borel and real finite at every finite t.'),
 ('N11','ASTIS_INTERNAL_BRIDGE','Zero/nonnegative/nondecreasing hazard',['A1.E1','A1.Ex7'],'Lambda(a,0)=0; 0<=Lambda(a,t); monotone only in nonnegative time.'),
 ('N12','ASTIS_INTERNAL_DEFINITION','Extended nonnegative clock and threshold',['A1.E1','A1.SS1.p2.2'],'e:NNReal (or equivalent real e>=0); tau in WithTop NNReal; inf empty=top through explicit branch.'),
 ('N13','ASTIS_INTERNAL_BRIDGE','Closed nonempty threshold set has least crossing',['A1.E1'],'{u>=0:e<=Lambda(a,u)} closed and bounded below; no WellFoundedLT/discrete-time reasoning.'),
 ('N14','ASTIS_INTERNAL_BRIDGE','Clock infinity/attainment/zero/positivity laws',['A1.E1','A1.SS1.p2.2'],'tau=top iff crossing set empty; finite tau gives Lambda(tau)=e; e=0 gives tau=0; e>0 implies tau>0 including infinity.'),
 ('N15','ASTIS_INTERNAL_BRIDGE','Exact finite-time threshold equivalence',['A1.E1'],'tau(a,e)<=t iff e<=Lambda(a,t) for t>=0; use attained infimum and monotonicity.'),
 ('N16','ASTIS_INTERNAL_BRIDGE','Joint Borel clock',['A1.E1'],'Finite sublevels equal closed/measurable threshold preimages; top sublevel is all. No joint clock continuity assertion.'),
 ('N17','ASTIS_INTERNAL_BRIDGE','Actual starting-energy cap along one flow segment',['A1.SS1.p3.2','A1.Ex6'],'C(a)=C_(H(a,z)); H(Phi_s z)=H(z) supplies the exact74 energy-layer cap internally.'),
 ('N18','ASTIS_INTERNAL_BRIDGE','Actual integrated hazard cap',['A1.Ex7'],'Lambda(a,t)<=C(a)*t, finite nonnegative C(a), all finite nonnegative times.'),
 ('N19','ASTIS_INTERNAL_BRIDGE','Extended wait lower bound and zero-cap branch',['A1.Ex8','A1.SS1.p3.5'],'If C>0, (e/C:WithTop NNReal)<=tau; if C=0 and e>0, tau=top. e=0 still gives0.'),
 ('N20','SOURCE_PROBABILISTIC_INPUT','Actual Exp(1) threshold marginal',['A1.SS1.p2.1'],'Canonical fixed law expMeasure(1); not arbitrary probability space/rv premise. Independent sequence excluded at this one-clock stage.'),
 ('N21','ASTIS_INTERNAL_BRIDGE','Real Exp support and threshold carrier transport',['A1.SS1.p2.1'],'Use rate1 CDF internally: e>=0 a.s., e=0 mass0; real.toNNReal collapse of negative null set preserves threshold law.'),
 ('N22','ASTIS_INTERNAL_DEFINITION','One-clock pushforward probability law',['A1.E1','A1.SS1.p2.1'],'map (e |-> tau(a,Real.toNNReal(e))) (expMeasure1 in descriptive notation); use actual declaration expMeasure(1).'),
 ('N23','ASTIS_INTERNAL_BRIDGE','Exact one-clock survival law',['A1.E1','A1.SS1.p2.1'],'P(tau>t)=exp(-Lambda(a,t)); ENNReal.ofReal if expressed as measure, or explicit toReal probability convention.'),
 ('N24','ASTIS_INTERNAL_BRIDGE','Degenerate branches remain legal',['A1.Ex4','A1.Ex6','A1.SS1.p3.5'],'Rank0 and H=0 imply zero-rate orbit; e>0 waits infinity and e=0 waits0. C>0 never licenses finite tau without crossing.'),
 ('N25','OPEN_SOURCE_CONSUMER','Actual A.1 clock substituted at postjump state',['A1.E1'],'Selected single-clock laws are consumed at actual zeta_Tn and E_(n+1); production of those states is not supplied here.'),
 ('N26','OPEN_SOURCE_CONSUMER','A.2 measurable event/path recursion',['A1.E2','A1.SS1.p2.2'],'Finite/empty branch, between-jump path, initial draws and actual postbounce states remain open.'),
 ('N27','OPEN_SOURCE_CONSUMER','Global initial-energy cap across stochastic recursion',['A1.SS1.p3.2','A1.SS1.p3.3'],'Requires actual path recursion and bounce plus flow energy conservation, not just an arbitrary r/state cap.'),
 ('N28','OPEN_SOURCE_CONSUMER','iid Exp sum/nonexplosion and wellposed process',['A1.Ex9','A1.SS1.p3.7','S3.Thmtheorem1'],'Requires product clocks, support/moment/SLLN and path construction; no current proof credit.'),
 ('N29','OPEN_SOURCE_CONSUMER','Memorylessness/time-homogeneous Markov property',['A1.SS1.p3.7'],'Measurable recursive construction and exponential memorylessness are still distinct obligations.'),
 ('N30','EXCLUDED_SOURCE_CONTEXT','Stationarity/reversal/semigroup/terminal/main/cost',['A1.E3','A1.Ex10','A1.Ex11','S3.Thmtheorem1'],'All excluded from selected single-clock mathematics; Davis bibliography is attribution, not inspected theorem evidence.'),
 ('N31','SOURCE_INGREDIENT','beta-Lipschitz/continuous gradient internally produced',['S1.E1','S3.Ex7','A1.SS1.p3.3'],'C2 plus Hessian upper bound gives gradient beta-Lipschitz; no new regularity/integrability premise.'),
 ('N32','SOURCE_CONTEXT','Algorithm1 has no refresh clock',['S3.E5','alg1'],'Initial Gaussian momentum/reference draws are not ongoing refresh. No refresh intensity enters Lambda or tau.')]
 nodes=[]
 def anchor(nid):
  n=byid[nid];lo=len(s[:n.start].encode());hi=len(s[:n.end].encode());d=raw[lo:hi]
  return {'id':nid,'source_URL':'https://arxiv.org/html/2609.06905v1#'+nid,'RAW_range':[lo,hi],'RAW_bytes':len(d),'RAW_sha256':sha(d),'LF_sha256':sha(d.replace(b'\r\n',b'\n'))}
 for nid,kind,label,aa,meaning in nd:
  nodes.append({'id':nid,'kind':kind,'label':label,'meaning':meaning,'source_anchors':[anchor(x) for x in aa],'status':'OPEN consumer' if kind.startswith('OPEN') else 'SOURCE projection / obligation only; no75 theorem credit'})
 ee=[
 ('N01','N02','definition'),('N01','N03','source ingredient'),('N01','N06','definition'),('N01','N31','source ingredient'),('N31','N04','source ingredient'),('N02','N03','definition'),('N02','N04','definition'),('N02','N05','definition'),('N02','N06','definition'),('N03','N07','source ingredient'),('N06','N07','definition'),('N31','N08','source ingredient'),('N06','N08','definition'),('N02','N08','definition'),('N04','N08','source ingredient'),('N03','N09','internal completion'),('N04','N09','internal completion'),('N09','N10','internal completion'),('N09','N11','internal completion'),('N10','N11','internal completion'),('N10','N12','definition'),('N11','N13','internal completion'),('N10','N13','internal completion'),('N12','N13','internal completion'),('N12','N14','internal completion'),('N13','N14','internal completion'),('N11','N14','internal completion'),('N13','N15','internal completion'),('N11','N15','internal completion'),('N15','N16','internal completion'),('N10','N16','internal completion'),('N07','N17','internal completion'),('N08','N17','internal completion'),('N06','N17','definition'),('N17','N18','internal completion'),('N10','N18','internal completion'),('N14','N19','internal completion'),('N18','N19','internal completion'),('N20','N21','internal completion'),('N16','N22','internal completion'),('N20','N22','definition'),('N21','N22','internal completion'),('N15','N23','internal completion'),('N21','N23','internal completion'),('N22','N23','internal completion'),('N19','N24','internal completion'),('N06','N24','internal completion'),('N04','N24','internal completion'),('N14','N24','internal completion'),('N14','N25','open actual substitution'),('N16','N25','open actual substitution'),('N19','N25','open actual substitution'),('N23','N25','open actual substitution'),('N25','N26','open recursive consumer'),('N05','N26','open recursive consumer'),('N07','N27','open recursive consumer'),('N05','N27','open recursive consumer'),('N26','N27','open recursive consumer'),('N27','N28','open stochastic consumer'),('N19','N28','open stochastic consumer'),('N20','N28','open stochastic consumer'),('N26','N28','open stochastic consumer'),('N26','N29','open stochastic consumer'),('N20','N29','open stochastic consumer'),('N28','N30','excluded downstream consumer'),('N29','N30','excluded downstream consumer'),('N32','N09','scope constraint')]
 edges=[{'id':f'E{i:02d}','producer':a,'consumer':b,'kind':k,'source_anchors':list(dict.fromkeys([q['id'] for q in next(n for n in nodes if n['id']==b)['source_anchors']])),'credit':'source-topological dependency only, not a Lean implication'} for i,(a,b,k) in enumerate(ee,1)]
 graph={'schema':'pbps75-independent-source-proof-graph/v1','actor':'/root/independent_primary69','frozen_before_any75_header_body':True,'not_Lean_dependency_graph':True,'node_count':len(nodes),'edge_count':len(edges),'nodes':nodes,'edges':edges,'topology_scope':'One actual fixed-reference integrated-hazard first clock and its explicit open A.1/A.2 consumers; source evidence and ASTIS internal bridges typed separately.','no_credit':['75 header','implementation','Lean compile','SAU','VERIFIED','nonexplosion','Markov','invariance','kernel','reader','Exposition','PURIFIED','main','cost','whole Goal']}
 graphpin=dump('source-proof-graph75.json',graph)
 # Explicit classifications. No candidate Lean informed these source assignments.
 def classify(n,reg):
  k=n.id
  if reg in ('S1.p1.1','S1.E1','S2.SS2.p1.1'):
   if k=='S1.p1.m1':return 'EXCLUDED',[],'Normalized target density is standing paper background, not a hazard/clock input or conclusion.'
   return 'NODE',['N01'],'Original source standing condition/type context; not a new clock hypothesis.'
  if reg=='davis-reference':return 'EXCLUDED',['N30'],'Bibliographic attribution/adjacent bibliography only; no Davis theorem content inspected or credited.'
  if k.startswith('S3.SS2.p3'):return 'EXCLUDED',[],'Earlier full-gradient generator discussion; selected rate uses actual residual gradient.'
  if k=='S3.SS2.p4.m2' or k.startswith('alg1.l2'):return 'EXCLUDED',['N32'],'Random reference/Gaussian initial draw is algorithm context for later process, not a single fixed-reference clock premise.'
  if k in ('S3.SS2.p4.m4',):return 'EXCLUDED',[],'Full conditional-force/generator identity is not proved by a single clock.'
  if k.startswith('S3.SS2.p4.5') or k=='S3.SS2.p4.m8':return 'EXCLUDED',['N30'],'Expected bounce-query complexity outside selected clock boundary.'
  if k.startswith(('S3.SS2.p5.2','S3.SS2.p5.3','S3.E7')) or k in ('S3.SS2.p5.m4','S3.SS2.p5.m5','S3.SS2.p5.m6','S3.SS2.p5.m7','S3.SS2.p5.m8','S3.SS2.p5.m9','S3.SS2.p6.m1','alg1.l5.m2') or k.startswith('alg1.l8'):
   return 'EXCLUDED',['N30'],'Fixed pi half-turn endpoint/returned-position claim is a downstream process consumer, not one-clock mathematics.'
  if k in ('S3.Thmtheorem1.p1.m1','S3.Thmtheorem1.p1.m2','S3.Thmtheorem1.p1.m3'):return 'NODE',['N01','N02','N25'],'Every fixed original reference and initial phase point is permitted; process conclusions remain open.'
  if k.startswith('S3.Thmtheorem1') or k.startswith('S3.SS2.p7'):return 'EXCLUDED',['N28','N29','N30'],'Full Proposition3.1 wellposedness/stationarity is a real source consumer, not established by source baseline or a clock leaf.'
  if k.startswith('S3.E4'):return 'NODE',['N02'],'Exact actual center/residual definition with unchanged sign/coefficient.'
  if k.startswith(('S3.Ex6','S3.SS2.p4.2')) or k=='S3.SS2.p4.m3':return 'NODE',['N02'],'Fixed-reference gradient decomposition supplies actual residual identity.'
  if k.startswith('S3.Ex7') or k in ('S3.SS2.p4.m6','S3.SS2.p4.m7'):return 'NODE',['N31'],'beta-Lipschitz residual bound must be internally produced from original analytic callers.'
  if k.startswith(('S3.E8','S3.E6','S3.SS2.p5.1')) or k.startswith('S3.SS2.p5.m') or k=='alg1.l5.m1':return 'NODE',['N03'],'SAME actual harmonic flow, not freely supplied dynamics; endpoint/horizon claims explicitly excluded.'
  if k.startswith('S3.E9') or k.startswith('alg1.l6'):return 'NODE',['N04','N32'],'Only residual bounce intensity; no refresh term.'
  if k.startswith('alg1.l7'):return 'NODE',['N05','N32'],'Actual source bounce is retained as algorithm context; no path or S continuity conclusion.'
  if k.startswith('alg1.l1'):return 'NODE',['N01'],'Original state carrier; no initial-law premise for a fixed-state clock.'
  if k.startswith('alg1.l3'):return 'NODE',['N02'],'SAME reference gradient defines center/residual; query costs excluded.'
  if k.startswith('alg1.l4'):return 'NODE',['N06','N17'],'Arbitrary original initial state supplies SAME initial-energy expression, not an independent cap.'
  if k.startswith('alg1.l5'):return 'NODE',['N03','N32'],'Actual deterministic evolution is retained; within-clause pi horizon not part of selected conclusion.'
  if k.startswith('S3.E5') or k.startswith('S3.SS2.p4.3'):return 'NODE',['N03','N04','N32'],'Generator records actual drift/rate and absence of refresh; no generator/Markov theorem credited.'
  if k.startswith('S3.SS2.p4'):
   return 'NODE',['N02','N31'],'Selected fixed-reference/smoothness context only; conditional sampling and expected cost excluded separately.'
  if k.startswith('S3.SS2.p6') or n.tag=='figcaption':return 'NODE',['N32'],'Algorithm1 source identity/no refresh scope; process completion phrase is not a clock proof.'
  if k.startswith('A1.SS1.p1'):
   return 'NODE',['N01','N03','N04','N05'],'Fixed real state, actual flow/rate/bounce and zero-normal instantaneous-rate convention; joint S continuity not added.'
  if k.startswith('A1.Ex1.'):return 'NODE',['N04'],'Exact positive-part rate and sqrt eta factor.'
  if k.startswith('A1.Ex2.'):return 'NODE',['N03'],'Exact two-component harmonic flow used inside hazard.'
  if k.startswith('A1.Ex3.'):return 'NODE',['N05'],'Actual bounce and R0 identity context, not an extra clock input.'
  if k=='A1.SS1.p2.m1':return 'EXCLUDED',['N28'],'Independent infinite sequence is a future recursion input; one clock uses only the fixed Exp1 marginal.'
  if k=='A1.SS1.p2.m2':return 'NODE',['N20','N21'],'Actual Exp(1) marginal; support/zero mass must be derived, not supplied.'
  if k=='A1.SS1.p2.m3':return 'NODE',['N06','N17'],'SAME actual initial phase point for segment energy; no random-path realization assumed.'
  if k=='A1.SS1.p2.m4':return 'NODE',['N11'],'Initial nonnegative time starts at0.'
  if k=='A1.SS1.p2.1':return 'NODE',['N12','N20','N25'],'One threshold/initial-state fragment selected; sequence independence and actual recursion explicitly future.'
  if k.startswith('A1.E1.'):return 'NODE',['N09','N10','N12','N25'],'Literal (A.1) actual integral/first-crossing definition; measurable/attainment lemmas are separate internal bridges.'
  if k.startswith('A1.E2.') or k in ('A1.SS1.p2.m7','A1.SS1.p2.m8'):return 'EXCLUDED',['N26'],'Timestamp/postbounce/between-jumps recursion is not produced by a universal one-clock leaf.'
  if k.startswith('A1.SS1.p2.2') or k in ('A1.SS1.p2.m5','A1.SS1.p2.m6'):return 'NODE',['N12','N14','N25'],'Explicit finite-wait/empty-set infinity branch preserved; between-jump path part excluded separately.'
  if k.startswith('A1.Ex4.') or k.startswith('A1.SS1.p3.1'):return 'NODE',['N06'],'Exact shifted harmonic weighted SUM energy with half and eta inverse.'
  if k=='A1.SS1.p3.m1':return 'NODE',['N17'],'Initial energy evaluated on SAME actual state, not an independent caller.'
  if k=='A1.SS1.p3.2':return 'NODE',['N07','N17','N27'],'Flow energy conservation used only on a single orbit; full recursive path/bounce propagation remains open N27.'
  if k.startswith('A1.Ex5.'):return 'NODE',['N08'],'Exact energy radii on SAME H layer, supplied internally.'
  if k in ('A1.SS1.p3.m2','A1.SS1.p3.m3'):return 'NODE',['N31'],'Source beta-Lipschitz gradient is an internal proof ingredient from standing Hessian bounds.'
  if k=='A1.SS1.p3.m4' or k=='A1.SS1.p3.3':return 'NODE',['N08','N17','N27'],'Pointwise/SAME-orbit cap selected; wording throughout recursive path is a separate open consumer.'
  if k.startswith('A1.Ex6.'):return 'NODE',['N08','N17'],'Exact finite cap expression with actual E=H(z), unchanged factors.'
  if k.startswith('A1.Ex7.') or k=='A1.SS1.p3.4':return 'NODE',['N18'],'Actual integrated hazard <=C_E*u; all finite interval integrability internally produced.'
  if k.startswith('A1.Ex8.') or k=='A1.SS1.p3.5' or k=='A1.SS1.p3.m5':return 'NODE',['N19','N24'],'Positive-cap lower bound and positive-threshold zero-cap infinity branch; e=0 separately gives0.'
  if k.startswith('A1.Ex9.') or k in ('A1.SS1.p3.6','A1.SS1.p3.7','A1.SS1.p3.m6'):return 'EXCLUDED',['N28','N29'],'iid SLLN/nonaccumulation/unique process/Markov claims and Davis cited route are open, not a clock conclusion.'
  if k.startswith(('A1.SS1.p4','A1.Ex10','A1.Ex11','A1.Thmtheorem1','A1.E3','A1.I1')):return 'EXCLUDED',['N30'],'Reversal/invariance/L2 semigroup/averaged-kernel results outside selected scope.'
  if n.tag.startswith('h'):return 'EXCLUDED',[],'Source heading/title only; no theorem/clock implication.'
  raise AssertionError(('Unclassified source row',reg,n.tag,k))
 rows=[];partitions=[];regionreports=[]
 for r in regions:
  lo,hi=r['RAW_range'];clo=len(raw[:lo].decode());chi=len(raw[:hi].decode());local=[]
  for n in p.nodes:
   semantic=n.tag in ('math','p','figcaption','h1','h2','h3','h4','h5','h6') or (n.tag=='div' and 'ltx_listingline' in n.attrs.get('class','')) or (n.tag=='li' and 'ltx_bibitem' in n.attrs.get('class',''))
   if not semantic or n.start>=chi or n.end<=clo:continue
   a=max(lo,len(s[:n.start].encode()));b=min(hi,len(s[:n.end].encode()))
   status,linked,reason=classify(n,r['region_id']);chunk=raw[a:b];rowid=f'S{len(rows)+1:03d}'
   row={'item_id':rowid,'region_id':r['region_id'],'source_id':n.id or f'{n.tag}@{a}','kind':'math' if n.tag=='math' else 'source_block','source_tag':n.tag,'RAW_range':[a,b],'RAW_bytes':b-a,'RAW_sha256':sha(chunk),'LF_sha256':sha(chunk.replace(b'\r\n',b'\n')),'clipped_at_region_boundary':n.start<clo or n.end>chi,'classification':status,'nodes':linked,'reason':reason,'formula':n.attrs.get('alttext') if n.tag=='math' else None,'text':n.text(),'source_URL':r['source_URL'] if not n.id else 'https://arxiv.org/html/2609.06905v1#'+n.id}
   rows.append(row);local.append(row)
  boundaries=sorted({lo,hi}|{x for q in local for x in q['RAW_range']});pieces=[]
  for a,b in zip(boundaries,boundaries[1:]):
   active=[q for q in local if q['RAW_range'][0]<=a and q['RAW_range'][1]>=b]
   active.sort(key=lambda q:(q['kind']!='math',q['RAW_bytes']))
   owner=active[0] if active else None
   pieces.append({'RAW_range':[a,b],'RAW_sha256':sha(raw[a:b]),'item_id':owner['item_id'] if owner else None,'classification':owner['classification'] if owner else 'EXCLUDED','reason':owner['reason'] if owner else 'Markup, equation label, citation wrapper or region boundary syntax; semantic source blocks and all math separately enumerated.'})
  assert sum(b-a for a,b in (x['RAW_range'] for x in pieces))==hi-lo
  gotmath=[q for q in local if q['kind']=='math'];expected=raw[lo:hi].count(b'<math ')
  assert len(gotmath)==expected,(r['region_id'],len(gotmath),expected)
  partitions.append({'region_id':r['region_id'],'RAW_range':[lo,hi],'partition':pieces,'all_RAW_bytes_partitioned_once':True})
  regionreports.append({'region_id':r['region_id'],'math_items':len(gotmath),'source_blocks':len(local)-len(gotmath),'counts':dict(Counter(q['classification'] for q in local)),'RAW_bytes':hi-lo})
 inventory={'schema':'pbps75-independent-finite-source-coverage/v1','universe':'Every math element plus every intersecting paragraph, heading, algorithm line/caption and bibliography item in the exact3 prior primary regions+3 minimal original-standing supplements. Typed blocks/math are different rows, not a count of independent theorems. Exact per-region RAW partition additionally covers all syntax/labels/boundaries once.','whole_paper_coverage':False,'regions':regions,'region_reports':regionreports,'item_count':len(rows),'math_count':sum(q['kind']=='math' for q in rows),'block_count':sum(q['kind']=='source_block' for q in rows),'classifications':dict(Counter(q['classification'] for q in rows)),'items':rows,'all_items_classified':True,'no_candidate_seen':True}
 inventorypin=dump('source-coverage-inventory75.json',inventory)
 partitionpin=dump('source-RAW-partition75.json',{'schema':'pbps75-byte-partition/v1','partitions':partitions,'no_mathematical_credit_from_byte_partition':True})
 dump('API-bounded-review75.json',{'schema':'pbps75-bounded-API-source-context/v1','API_regions':api_review,'no_compile_or_new_proof_credit':True,'Exp1_literal_not_declared_in_pinned_slice':'The contract shorthand expMeasure1 must be elaborated as ProbabilityTheory.expMeasure (1 : Real) or an independently checked exact definition; no new caller/provider.'})
 formulaids=['S1.p1.m4','S1.E1.m1','S2.SS2.p1.m1','S3.E4.m1','S3.Ex7.m1','S3.E8.m1','S3.E9.m1','A1.Ex1.m1','A1.Ex2.m1','A1.Ex2.m2','A1.Ex3.m1','A1.Ex3.m2','A1.SS1.p2.m2','A1.E1.m1','A1.E1.m2','A1.SS1.p2.m6','A1.Ex4.m1','A1.SS1.p3.m1','A1.Ex5.m1','A1.Ex6.m1','A1.Ex7.m1','A1.Ex8.m1','A1.SS1.p3.m5']
 formulas=[{**anchor(k),'literal_source_alttext':byid[k].attrs['alttext'],'credit':'Exact source formula only; not a proved Lean clause'} for k in formulaids]
 dump('exact-source-formulas75.json',{'source_formulas':formulas,'source_formula_count':len(formulas),'not_invented_source_formula':['joint continuity/Borel clock','first-crossing exact sublevel equivalence','finite-clock equality','one-clock survival formula','real-to-NNReal support adapter'],'derived_formulas_are_required_internal_bridges':True})
 callers=[
 {'id':'hα','source_kind':'STANDING','meaning':'0<alpha','source':'S1.p1.m4'},
 {'id':'hαβ','source_kind':'STANDING','meaning':'alpha<=beta','source':'S1.p1.m4'},
 {'id':'hV','source_kind':'SOURCE','meaning':'V in C2 on whole real carrier','source':'S1.p1.m3'},
 {'id':'hH','source_kind':'SOURCE','meaning':'Every x and v: alpha*norm(v)^2 <= inner(Hess V(x) v,v) <= beta*norm(v)^2; Lean derivative-of-gradient convention must represent this SAME Hessian','source':'S1.E1.m1'},
 {'id':'hη','source_kind':'STANDING','meaning':'0<eta','source':'S2.SS2.p1.m1'},
 {'id':'hβη','source_kind':'STANDING','meaning':'beta*eta<=1 (equivalent eta<=1/beta under beta>0)','source':'S2.SS2.p1.m1'}]
 obs=[
 ('O01','Original public input contract','Only original six analytic callers; all other proof ingredients internal, with no arbitrary flow/rate/cap/clock/provider supplied.'),
 ('O02','Exact state/type/domain','Finite real Hilbert carrier with canonical Borel structure, y/xRef/x/p arbitrary same carrier; d=0 permitted. Complete/separable/standard Borel adapters are type consequences when needed.'),
 ('O03','Exact definitions','Same V,eta,y,xRef in c,h,Phi,rate,H,C,Lambda,tau; no RHS-defined surrogate clock or arbitrary hazard.'),
 ('O04','Exact harmonic coefficients','c+(x-c)cos t+sqrteta*p*sin t; -sin t/sqrteta*(x-c)+cos t*p; negative sign and inverse sqrteta retained.'),
 ('O05','Exact rate/no refresh','sqrteta*max(inner(p,gradVx-gradVxref),0); no refresh intensity, randomized resets or full-gradient replacement.'),
 ('O06','Regularity producer','C2/Hessian -> beta-Lipschitz/continuous gradient internally; no gradient continuity/Lipschitz caller or higher derivative.'),
 ('O07','Exact energy','H=((1/eta)||x-c||²+||p||²)/2 and E=H(z), not product norm/unknown path energy.'),
 ('O08','Exact cap','C=sqrteta*beta*sqrt(2H(z))*(sqrt(2etaH(z))+||c-xRef||); finite nonnegative internal expression.'),
 ('O09','True actual orbit cap','Use actual flow energy conservation to bound actual q(s), not a caller assuming q<=C or source theorem nonexplosion.'),
 ('O10','Finite interval integrability','Every finite nonnegative interval is internally integrable from joint continuity, no global time integrability/domination premise.'),
 ('O11','Hazard normalization','Lebesgue time integral0..t of actual rate composed with actual flow; unit rate Exp1; no missing sqrteta or sign/max.'),
 ('O12','Time quantification','All t in NNReal or equivalent real t>=0; no negative-time monotonicity/cap claim and no integer-time substitution.'),
 ('O13','Joint primitive','Lambda jointly continuous/Borel in y,xRef,z,time, finite at finite time, Lambda0=0/nonnegative/monotone.'),
 ('O14','Clock definition','tau is first nonnegative u with e<=Lambda(u); empty set explicitly infinity, not Real/NNReal sInf empty=0.'),
 ('O15','Closed first crossing','Prove nonempty set attainment by continuous closedness and lower bound0; WellFoundedLT/discrete hittingAfter lemmas are forbidden.'),
 ('O16','Finite-time exact equivalence','tau<=t iff e<=Lambda(t), including e=0 and empty-crossing branch; not only one implication.'),
 ('O17','Finite clock equality','Finite tau implies Lambda(tau)=e; show continuity + minimality, not merely >=e.'),
 ('O18','Threshold0/positive','All nonnegative e legal. e=0 ->tau=0; e>0 ->tau>0, infinity allowed.'),
 ('O19','Joint clock Borel','Measurability jointly in all parameters+e into extended nonnegative time; no unnecessary joint continuity or finite-hit caller.'),
 ('O20','Actual Exp marginal','Use actual expMeasure(1:Real) or checked equivalent; one threshold law has no iid/independence or moment premise.'),
 ('O21','Carrier/support adapter','Derive nonnegative support and zero atom for actual Exp1 and justify real.toNNReal; negative null inputs need no public restriction.'),
 ('O22','Survival identity','Under actual threshold law, P(tau>t)=exp(-Lambda(t)); real probability versus ENNReal measure convention explicit and exact.'),
 ('O23','Lower wait branch','C>0 ->cast(e/C)<=tau in extended time; handle tau=top and finite equality. C>0 is a branch, not a theorem caller.'),
 ('O24','Zero cap branch','C=0,e>0 ->tau=top; deterministic e=0 remains0. Source no jumps statement is a.s. positive Exp threshold semantics.'),
 ('O25','Degenerate legal cases','H=0 or rank0: orbit/rate0, positive threshold infinity; alphaeta=1 permitted, no positive-energy/nontrivial-space premise.'),
 ('O26','No unjustified finite waiting','Do not require unbounded hazard, positive C, finite/a.s. finite tau, positive rate or globally nonzero residual; positive cap is not sufficient for finite crossing.'),
 ('O27','Pointwise zero warning','A zero initial rate/residual normal alone does not prove zero rate along the orbit or infinite waiting; require derived full zero hazard branch.'),
 ('O28','Actual source consumer','Universal fixed-state clock may be substituted at zeta_Tn only once a true measurable recursive path producer exists; arbitrary state is not that producer.'),
 ('O29','Stochastic boundary','iid sequence, support/moments/SLLN, path recursion/energy propagation, nonexplosion, memorylessness/Markov/invariance/reversal/kernel all remain separate.'),
 ('O30','Representation and public scope','Full complete statement must be available to readers; private literal if used is definition/nonprovider. No proof/semantic certificate or premise replay.'),
 ('O31','Attribution and graph truth','Exact A1.E1, A1.Ex7/8 and standing anchors; source graph != Lean dependencies; inferred completion bridges not literal paper claims.'),
 ('O32','Admission boundary','This baseline accepts no nonexistent75 header, no source semantic roundtrip/Lean/VERIFIED/reader/Exposition/PURIFIED/main/cost/wholeGoal.')]
 obligations=[{'id':a,'label':b,'required_standard':c,'status':'FUTURE HEADER/IMPLEMENTATION OBLIGATION; no75 candidate read'} for a,b,c in obs]
 internal=[n['id'] for n in nodes if n['kind']=='ASTIS_INTERNAL_BRIDGE']
 expectations={'schema':'pbps75-independent-source-first-expectations/v1','actor':'/root/independent_primary69','source_before_75_header_body':True,'exposure':{'previous_source_wholemodule':[70,71,72,73,74],'previous_prospective_headers':[70,71,72,73,74],'CLOSED86_source_plan_and_decision_visible':True,'future75_header_hash_statement_body_seen':False,'source_blind_claim':False,'independence':'Distinct source reviewer; independently re-read RAW primary, classified source universe and authored topology, not adopted another mathematical verdict.'},'original_callers':callers,'typing_not_extra_analytic_callers':['real normed inner product carrier','finite dimensional (rank0 legal)','Borel measurable structure','canonical NNReal/WithTop time and Borel order adapters'],'meaning_and_domains':{'parameters':'a=(y,xRef,z), z=(x,p); arbitrary same real carrier','time':'NNReal (or real t>=0 with explicit guards), not Nat or WellFoundedLT','threshold':'e>=0 including0','clock':'WithTop NNReal or reviewed order-isomorphic extended nonnegative time; top is a real output, not an error','hazard':'Lambda(a,t)=integral_0^t lambda_xRef(Phi_s^(y,xRef)(z)) ds wrt Lebesgue time','cap':'C(a)=source C_E at E=SAME H_y,xRef(z)','probability':'Fixed actual rate1 exponential marginal on real thresholds, mapped via toNNReal before tau; no arbitrary RV/certificate'},'conclusion_standard':['joint continuous/Borel finite-interval Lambda; zero, nonnegative, monotone','exact first crossing/top iff empty/finite equality/e0=0/positive threshold positive wait','joint Borel tau','exact actual Exp1 survival law','same-initial-energy Lambda<=C*t and extended lower-bound/zero-cap branches','legal rank0/zero energy/alphaeta1, no unbounded hazard or a.s. finite waiting premise'],'retained_vs_used':'Keep all six original standing analytic callers. Local flow/clock uses eta>0 and C2; exact quantitative cap uses Hessian upper bound/beta nonnegative. Lower alpha bound/alpha<=beta/betaeta<=1 may be retained beyond the strictly used local fragment; none becomes a fabricated dependency edge. All required derivatives, continuity, finite-interval integrability, clock attainment and Exp support adapters internal.','source_evidence_vs_completion':{'literal_source_formulas':pin(OWN/'exact-source-formulas75.json'),'internal_bridge_nodes':internal,'all_bridge_requirements_are_obligations_not_binders':True,'Davis':'Only original citation/bibliography inspected; no theorem/hypotheses inferred from unseen external text.'},'future_header_obligations':obligations,'source_graph':graphpin,'finite_coverage':inventorypin,'no_granted_credit':graph['no_credit']}
 expectpin=dump('source-first.expectations75.json',expectations)
 decisions={'schema':'pbps75-independent-source-baseline-decision/v1','actor':'/root/independent_primary69','status':'SOURCE_FIRST_BASELINE_FROZEN_ONLY','decision':'Ready for a future separately frozen prospective75 header comparison; no header supplied or accepted.','not_a_source_fidelity_verdict_on75':True,'source_graph':graphpin,'source_coverage':inventorypin,'expectations':expectpin,'counts':{'regions':len(regions),'source_math':inventory['math_count'],'source_blocks':inventory['block_count'],'source_items':len(rows),'NODE':inventory['classifications'].get('NODE',0),'EXCLUDED':inventory['classifications'].get('EXCLUDED',0),'source_nodes':len(nodes),'source_edges':len(edges),'exact_source_formulas':len(formulas),'future_obligations':len(obligations),'internal_bridge_nodes':len(internal),'bounded_API_regions':len(api)},'independent_source_findings':['A.1 explicitly gives empty crossing infinity; therefore no unbounded-hazard/finite-wait premise can be added.','The source zero-cap/no-jumps phrase uses positive Exp thresholds a.s.; all-e deterministic extension must retain e0->tau0.','hittingAfter definition itself is generic; displayed hittingAfter_le_iff is WellFoundedLT and inadmissible for continuous time.','Canonical expMeasure1 in planning is shorthand; actual pinned declaration is expMeasure(1). Support/toNNReal/CDF convention are internal adapter obligations.','Only one actual flow-segment clock/cap is selected. Recursive global-energy cap and iid nonexplosion cannot be inferred from it.'],'required_source_repair':[],'future_candidate_not_seen':True,'old_plan_historical_status':'CLOSED86 statement that74 was sealed-only is historical. No current74 compile/SCI credit is created or rechecked here.','remaining_truth_boundary':graph['no_credit'],'scope_writes':'Only fresh independent-source-baseline75; oldCLOSED86 verified read-only, no canonical/Git/ledger/Goal writes.'}
 decisionpin=dump('decision75.json',decisions)
 dump('observer-negatives75.json',{'schema':'pbps75-source-observer-negatives/v1','negatives':[{'actual_PID':48580,'actual_EXIT':1,'tool_session':32938,'type':'observer-performance-termination','description':'Initial read-only HTML-tree probe repeatedly UTF8-encoded every source prefix for every node; manually terminated own process after bounded diagnosis. No theorem/source conclusion or frozen output used.','original_helper_version':'Before two explicit narrowing patches; code change recorded in session tool patches, no claim original bytes were captured before termination.','replacement_actual_PID':26964,'replacement_actual_EXIT':0},{'actual_PID':29884,'actual_EXIT':0,'type':'observer-intermediate-range-optimization','description':'Intermediate guessed char/byte window omitted early A1 blocks in displayed probe. No finite-coverage claim used this probe; final builder computes exact char boundaries from RAW bytes and asserts every math count independently.','replacement_actual_PID':26964,'replacement_actual_EXIT':0}], 'no_candidate_or_primary_change':True,'no_false_EXIT0_credit':True})
 dump('source-provenance-verification75.json',{'fixed_primary':pin(PRIMARY),'prior_CLOSED86_lease':pin(PRE/'lease.final.json'),'prior_native_owned_count':86,'all85lease_members_RAW_LF_verified':True,'wholelogical_delete_only_top_run_sha256_verified':oldclaimed,'all3source_slices_equal_fixed_primary_RAW':True,'all11API_slices_equal_pinned_parent_RAW_line_ranges':True,'parent_API_whole_files_hash_checked_opaque_except_allowed_fragment_content':True,'no_recursive_prior_payload_copy':True,'original_read_probe_actual_PID':47688,'original_read_probe_actual_EXIT':0})
 im={'schema':'pbps75-finite-input-manifest/v1','LF_recipe':'ONLY replace CRLF bytes 0d0a with LF0a; preserve bareCR/all other bytes. RAW is authority; line slices formed before LF conversion.','input_count':len(inputs),'inputs':inputs,'source_regions':regions,'not_copied':'Full fixed primary and prior86 whole native are finite pinned references. Exact selected source regions/API signatures+explicit source planning/provenance JSON inputs have local finite RAW snapshots. Supplemental regions are exact RAW primary slices, not external inputs.','no_future75_header_or_implementation_input':True}
 inputpin=dump('inputs.manifest75.json',im)
 readme='''# Independent source-first75 baseline\n\nThis is an independently authored prospective source contract, not a theorem, SAU, compile or75 semantic acceptance. The fixed PBPSv1 RAW primary and CLOSED86 finite source/API slices are the authority. The graph is reconstructed from source, not implementation Lean. All mathematical completions are typed internal obligations; the original six analytic callers alone remain public.\n\nThe selected edge is the actual integrated hazard of the same fixed-reference harmonic flow and residual rate, its extended first-crossing clock, exact Exp(1) survival law, and same-starting-energy clock bound. Empty crossing means infinity. For all nonnegative deterministic thresholds e, e=0 gives clock0; zero cap with e>0 gives infinity. Source no-jumps language is a.s. positive-Exp semantics. Neither C>0 nor zero initial rate alone licenses finite/infinite waiting. Continuous time must not use WellFoundedLT hitting lemmas.\n\nA.2 recursive paths, global energy propagation, iid/SLLN/nonexplosion, memorylessness/Markov, stationarity/reversal, terminal kernels, main/error/query costs and composition stay open. Algorithm1 has no ongoing momentum refresh. Source typing/generalization and mathematical bridges are visible in the expectation/graph/coverage.\n\nEarlier70–74 source/header/BODY exposure and the visible CLOSED86 plan are honestly recorded. No75 header/hash/BODY/proof or other future verdict was read. An inefficient first RAW probe was terminated and a flawed intermediate display range was superseded; both remain negative observer evidence, never source/proof credit.\n\nOnly this new owned scope is written. Final lease is the last owned write; postclose verifier is read-only. No canonical, Goal, ledger or Git mutations.\n'''
 (OWN/'bounded-synthesis75.md').write_bytes(readme.encode())
 receipt={'schema':'pbps75-terminal-receipt/v1','phase':'independent source baseline build','actual_PID':os.getpid(),'actual_EXIT':0,'counts':decisions['counts'],'current_inputs_verified':len(inputs),'candidate_read':False,'compile_or_background_execution':False,'owned_scope_only':True}
 dump('terminal.build75.json',receipt)
 print(json.dumps(receipt,ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
