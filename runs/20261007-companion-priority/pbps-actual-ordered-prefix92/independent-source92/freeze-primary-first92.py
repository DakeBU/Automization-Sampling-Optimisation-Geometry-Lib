from pathlib import Path
import datetime, hashlib, json, re

ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/independent-source92'
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=PRIMARY.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
def bind(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(n,d):
 p=OUT/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
 return bind(p)
OUT.mkdir(parents=True,exist_ok=True)
ids=['S1.p1','S2.SS2.p1','S2.E4','S3.SS2.p4','A1.SS1.p1','A1.SS1.p2','A1.E1','A1.E2','A1.SS1.p3','A1.SS1.SSS0.Px1.p4.1','A1.Ex19','A1.SS1.SSS0.Px1.p4.2','A1.E7','A1.SS1.SSS0.Px1.p4.3','A1.SS2','A1.SS2.p1','A1.SS2.p2','A1.Thmtheorem2','A1.SS2.p3','A1.SS2.p4','A1.SS2.p5']
slices=[]
for ident in ids:
 m=re.search(rb'<([A-Za-z0-9]+)\b[^>]*\bid="'+ident.encode()+rb'"[^>]*>',raw)
 assert m,ident
 depth=1;end=None
 for k in re.finditer(rb'</?'+m.group(1)+rb'\b[^>]*>',raw[m.end():]):
  depth+=-1 if k.group().startswith(b'</') else 1
  if depth==0:end=m.end()+k.end();break
 assert end
 part=raw[m.start():end]
 slices.append({'html_id':ident,'byte_start':m.start(),'byte_end_exclusive':end,'bytes':len(part),'raw_sha256':sha(part),'line_start':raw[:m.start()].count(b'\n')+1,'line_end':raw[:end].count(b'\n')+1})
slice_binding=write('primary-source-slices92.native.json',{'record_kind':'fixed-primary-byte-slice-bindings','source':bind(PRIMARY),'regions':slices,'indexing':'Zero-based bytes, exclusive end; one-based lines. Extracted afresh from fixed primary tags, not inherited from a previous graph or verdict.','raw_source_republished':False})
expectation={
 'record_kind':'primary-first-mathematical-expectation','reviewer':'/root/primary_source91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'stage':'FROZEN_BEFORE_NEW_CANONICAL_PACKET','primary':bind(PRIMARY),'slice_binding':slice_binding,
 'chronology':[
 'Parent assigned renewed primary-only preread for production SAU92. New canonical reviewer packet not supplied at assignment.',
 'Rehashed fixed primary and located source tags afresh. Reread standing assumptions, literal dynamics, A1/A2, energy/nonaccumulation paragraph, strict simplex, prescribed path/iteration sentence, A7, series convergence and entire Appendix A2.',
 'Read primary reflection formula S2.E4 to expand the literal bounce convention.',
 'Wrote this source-derived expectation before opening any current production Lean, lesson, reconstruction, current mathematical reviewer verdict, old source verdict or repair overlay.',
 'Earlier source recommendation/header review exposure in this conversation is disclosed; it is not erased. This is a fresh primary-first comparison expectation, not a claim of lifetime blindness. No prior decision is evidence for the current source verdict.' ],
 'version_license':{'version':'arXiv:2609.06905v1','license':'arXiv non-exclusive distribution license','status':'Fixed source/license unchanged per assignment; earlier official verification retained, no duplicate web fetch. This output contains mathematical paraphrase and hashes rather than a republished source snapshot.'},
 'six_original_analytic_assumptions':[
 {'assumption':'V is globally C2 on R^d','source':'S1.p1'},
 {'assumption':'0<alpha','source':'S1.p1'},
 {'assumption':'alpha<=beta','source':'S1.p1'},
 {'assumption':'For every x and v, alpha norm(v)^2 <= Hess V(x)[v,v] <= beta norm(v)^2','source':'S1.p1'},
 {'assumption':'0<eta','source':'S2.SS2.p1'},
 {'assumption':'eta<=1/beta','source':'S2.SS2.p1'} ],
 'source_objects':{
 'space':'Source position and momentum are Euclidean R^d, with Borel structures. y, reference r and initial phase z0=(x0,p0) are fixed arbitrarily for the path law.',
 'center_and_residual':'c=y-eta gradV(r), h_r(x)=gradV(x)-gradV(r).',
 'flow':'Phi_t(x,p)=(c+(x-c)cos t+sqrt(eta)p sin t, -(x-c)sin t/sqrt(eta)+p cos t).',
 'rate':'lambda_r(x,p)=sqrt(eta) max(<p,h_r(x)>,0).',
 'bounce':'S_r(x,p)=(x,R_(h_r(x))p), R_v p=p-2<p,v>v/norm(v)^2 for v!=0; R_0 p=p. Borel reflection is sufficient; it need not be continuous. At zero residual the rate vanishes.',
 'clocks':'Independent Exp(1) variables E_1,E_2,...; literal initial T0=0 and phase z0.',
 'hazard':'L_z(u)=integral from 0 to u of lambda_r(Phi_s(z)) ds, u>=0; continuous nondecreasing in u and jointly Borel in finite parameters.',
 'crossing':'tau_z(e)=inf{u>=0:L_z(u)>=e}; closed threshold, empty crossing infinity. Zero threshold yields zero elapsed time.',
 'actual_recursion':'If current record is (T_k,z_k) and tau_zk(E_(k+1))=s<infinity, then T_(k+1)=T_k+s and z_(k+1)=S_r(Phi_s(z_k)). At infinity the source stops recursion. Between finite jumps it flows on half-open intervals.',
 'measurability':'Appendix A2 derives joint Borel dependence of finite times/poststates in y,x0,p0,r and the clock sequence. It then separately uses nonexplosion for a terminal version, and separately averages reference/momentum/clocks for kernels.'},
 'ASTIS_explicit_completions_expected':[
 'A canonical product probability space of real unit-exponential coordinates may realize the source iid law; clipping raw negative coordinates to zero is a null-input totalization, not an assumption of positive raw inputs.',
 'Rec=(NNReal x Phase) sum Unit with absorbing stopped tag is a faithful totalization of stopped recursion. Hist_n=Fin(n+1)->Rec retains every record. A stopped tag is never a finite event or a phase at infinity.',
 'Finite-dimensional real Hilbert carrier including rank zero is an explicit extension of the printed Euclidean formulation, not an author-stated assumption.',
 'Simplex subtype and its restricted product Lebesgue measure are formal representations. Comap by its Borel inclusion is suitable only with the exact restricted-measure identification established.',
 'Unbounded nonnegative ENNReal whole-history tests extend the printed bounded whole-path test language; declare this mathematical completion, retain every record, and do not use extra integrability/positive-mass premises.' ],
 'strict_finite_prefix_target':{
 'indices':'Every n>=0 and finite T>=0; no randomized index.',
 'simplex':'Delta_n(T)={t in R^n:0<t1<...<tn<T}; n=0 singleton with empty-product measure mass one, even T=0.',
 'prescribed_recursion':'t0=0,z0^t=z0; for j=1..n, delta_j=tj-t_(j-1), z_j^-=Phi_delta_j(z_(j-1)^t), z_j^t=S_r(z_j^-). K_n(t) records live(0,z0), then every live(tj,z_j^t).',
 'actual_event':'B_n(T) requires actual first n successor records live and 0<T1<...<Tn<T. Initial record is fixed live(0,z0). It imposes no condition on next record or next time. B0 is the whole clock space.',
 'weight':'qReal_n(t)=product_(j=1)^n lambda_r(z_j^-) exp(-L_(z_(j-1)^t)(delta_j)); q_n=ofReal(qReal_n), empty product 1. This includes survival along each completed inter-event segment only.',
 'law':'For every Borel F:Hist_n->ENNReal, integral_(B_n(T)) F(H_n(w)) P(dw) = integral_(Delta_n(T)) F(K_n(t)) q_n(t) dt. Equivalent pushforward equality of unnormalized restricted measures; integral q_n=P(B_n(T))<=1.',
 'structural_conclusions':'Borel actual history/event; jointly Borel K and q in y,r,z0,t for fixed V,eta,n,T; nonnegative qReal; on B_n actual observed time tuple lies in the simplex and actual whole history equals K at that tuple pointwise.',
 'count_boundary':'A strict first-n event count interpretation requires positive clocks almost surely and suitable endpoint conventions. It is not a pointwise statement on all raw zero-clock totalizations. No exactly-n count at T follows from prefix law alone.'},
 'source_derived_route':[
 {'step':1,'claim':'Establish Borel flow, rate and reflection under the original assumptions; integrate the actual rate to get a continuous nondecreasing hazard and measurable closed-threshold crossing.','source':'A1.SS2.p3','classification':'Printed ingredient with formal details to supply'},
 {'step':2,'claim':'Use the literal clock realization and finite stopped recursion to establish Borel actual complete histories. Measurability must depend on the exact actual recurrence, not a replacement process.','source':'A1.E1/A1.E2 and A1.SS2.p3','classification':'Printed finite-recursion measurability plus ASTIS totalization'},
 {'step':3,'claim':'Derive the finite next-time law from a fresh independent unit-exponential threshold. Conditional on actual prefix ending at (a,z), density at absolute u>a is lambda(Phi_(u-a)z) exp(-L_z(u-a)); retain actual appended poststate and every old record. Infinite wait mass is excluded by finite strict interval.','source':'A1.E1/A1.E2 and iteration sentence','classification':'Omitted clock-law proof expansion; conclusion/dependency, not added assumption'},
 {'step':4,'claim':'Construct K and q by prescribed positive gaps, prove joint Borel maps, positivity of qReal, and literal actual/prescribed append agreement on strict prefix.','source':'Prescribed trajectory in A1.SS1.SSS0.Px1.p4.2','classification':'ASTIS finite-history expansion'},
 {'step':5,'claim':'Start induction at n=0: deterministic initial record, singleton simplex, empty product one, probability mass one.','source':'n=0 in A1.E7','classification':'Implicit convention made explicit'},
 {'step':6,'claim':'For successor use actual next-time law with complete appended-history test, restrict previous history to strict prefix, substitute the n-level law using a measurable nonnegative parameter-integral test, and multiply by the new pre-bounce rate/survival factor.','source':'Iteration sentence before A1.E7','classification':'Core omitted induction'},
 {'step':7,'claim':'Identify Delta_(n+1)(T) with pairs (t,u) where t in Delta_n(T) and last(t)<u<T, last(empty)=0. Exact finite-product coordinate splitting, subtype/restriction measures and Tonelli turn the nested integral into the next simplex integral.','source':'A1.Ex19 and A1.E7','classification':'Background measure theory needed for omitted iteration, not a source hypothesis'},
 {'step':8,'claim':'Obtain all whole-history nonnegative tests, pushforward equality and mass bound without normalizing a zero-probability event.','source':'Iteration toward A1.E7','classification':'ASTIS bounded finite-prefix conclusion'} ],
 'route_logic':{
 'AND':'Preferred absolute-coordinate induction requires Borel actual and prescribed objects, actual one-step whole-history law, base case, append identity, measurable parameter tests, and exact simplex/product integration.',
 'OR':'A relative-wait-vector induction followed by exact triangular cumulative-time transport is a possible alternative. Do not demand it in addition to absolute-coordinate induction or insert an unproved general shear theorem as a public premise.',
 'no_topology_from_current_Lean':True,
 'source_hypothesis_equals_binder':'Retain original six assumptions; measurability, density, independent clocks from canonical law, product-coordinate formulas, append agreement, and any nonaccumulation facts are proof ingredients/conclusions, not new source-facing premises.'},
 'full_A7_printed_boundary':{
 'functional':'Every bounded measurable functional Psi of the entire path [0,T], not merely final position or last poststate.',
 'identity':'Expectation Psi(actual path) equals sum over n>=0 of integral_Delta_n(T) Psi(prescribed path) times exp(-integral_0^T lambda(prescribed path_s) ds) times product_j lambda(prescribed path_(tj-)) dt.',
 'terminal_survival':'At fixed n multiply prefix density by exp(-L_(z_n^t)(T-tn)), with t0=0 in the no-event term. Its absence from prefix law is intentional; without it one does not have the A7 nth count-event term.',
 'remaining_AND_dependencies':['Compose final survival at remaining horizon using next fresh clock and measurable actual history.','Identify segment hazard sum, including terminal segment, with full-path integrated rate, and each rate factor with pre-jump state.','Reconstruct actual and prescribed entire paths from complete histories on appropriate count events; prove measurable full-path test composition.','Use actual-input nonaccumulation/coverage to exhaust probability one by finite count events; reconcile strict horizon endpoint conventions only with appropriate justification.','Sum fixed-count identities and justify bounded signed tests.'],
 'remaining_OR_routes':'Printed rate cap plus simplex volume T^n/n! gives absolute convergence. A separately justified nonnegative count-mass/Tonelli route plus bounded signed decomposition is an alternative ASTIS completion, not an additional printed hypothesis.',
 'existing_results_boundary':'Source nonaccumulation follows from conserved energy, beta-Lipschitz residual rate cap and divergent exponential sums; it is separate from full path-law identification. Existing verified actual-input nonaccumulation/coverage may be consumed later but are not reread or re-awarded in this primary freeze.',
 'not_claimed':'No full A7, terminal survival composition, exact-count law, physical-time restart/Markov proof, invariance, averaged half-turn kernel, main complexity claim, actual-input paper composition or whole-paper completion.'},
 'source_coverage_dispositions':[
 {'source':'S1.p1/S2.SS2.p1','disposition':'NODE','reason':'Original six analytic assumptions retained.'},
 {'source':'S2.E4/A1.SS1.p1/S3.SS2.p4','disposition':'NODE','reason':'Literal dynamics, reflection convention and zero-normal zero-rate. Residual Lipschitz estimate is source consequence feeding energy/rate cap.'},
 {'source':'S3.SS2.p4','disposition':'EXCLUDED','reason':'Full-force recombination and randomized-reference expected-bounce motivation are not required for fixed-reference prefix induction.'},
 {'source':'A1.SS1.p1 involution','disposition':'EXCLUDED','reason':'Bounce inverse/reversal algebra is not required to construct forward prefix density.'},
 {'source':'A1.E1/A1.E2','disposition':'NODE','reason':'Actual clock and cumulative finite-event recursion.'},
 {'source':'A1.SS1.p2 stopped recursion','disposition':'SOURCE_GAP','reason':'Total deterministic-depth tagged representation and null-input conventions must be explicit.'},
 {'source':'A1.Ex19','disposition':'NODE','reason':'Strict simplex and finite-product reference measure.'},
 {'source':'A1.SS1.SSS0.Px1.p4.2 iteration sentence','disposition':'SOURCE_GAP','reason':'Conditional density, actual whole-history induction, parameter integration and simplex section proof are suppressed.'},
 {'source':'A1.E7','disposition':'NODE','reason':'Full entire-path functional identity is genuine consumer, still larger than prefix target.'},
 {'source':'A1.E7 terminal/count/path details','disposition':'SOURCE_GAP','reason':'Final survival, count partition, endpoint bookkeeping and actual/prescribed path test composition require separate completion.'},
 {'source':'A1.SS1.p3 and p4.3 convergence paragraph','disposition':'NODE','reason':'Energy bound, nonaccumulation and printed cap/simplex series route concern full path/count assembly, not extra prefix assumptions.'},
 {'source':'A1.SS1.p3 Markov assertion','disposition':'EXCLUDED','reason':'Physical-time memoryless restart is a separate result; deterministic-index independence suffices here.'},
 {'source':'A1.SS2.p3 finite recursion','disposition':'NODE','reason':'Joint Borel objects expected as dependencies/conclusions.'},
 {'source':'A1.SS2 terminal version, reference averaging and operator conclusions','disposition':'EXCLUDED','reason':'These downstream full-terminal/kernel/operator results are not established by finite prefix law.'} ],
 'edge_cases':['n=0 and T=0 preserved.','For n>0,T=0 the strict simplex and actual strict event are empty.','Infinite waits produce stopped records, not fabricated finite time0 events.','Zero clocks may produce time-zero or coincident events; strict-prefix guard removes them as needed, while probability statements rely on actual positive-clock support a.e.','Zero rate and zero residual normal require no positive hazard or eventual hit premise.','No continuity of bounce, initial stationary law, positive event probability, finite-all-waits or hidden integrability premise.'],
 'next_action':'Wait for new canonical anti-anchored packet and decoder before production theorem/reader/source-coverage comparison.',
 'current_stage_verdict':None,'canonical_mutation':False,'proof_or_VERIFIED_claim':False}
freeze_binding=write('primary-first-expectation92.native.json',expectation)
manifest=write('primary-first-RAW92.native.json',{'record_kind':'primary-first-frozen-RAW-manifest','reviewer':'/root/primary_source91','input':[bind(PRIMARY)],'outputs':[slice_binding,freeze_binding,bind(OUT/'freeze-primary-first92.py')],'closure':'Immutable primary-first expectation before current reviewer packet. Hashes are raw file bytes; manifest excludes itself. No production/reader/decoder/old-verdict/repair file opened for this stage.','wait_for_packet':True})
print(json.dumps({'freeze':freeze_binding,'slices':slice_binding,'manifest':manifest},indent=2))
