import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
import pathlib

ROOT=pathlib.Path.cwd()
RUN=ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread49'
def h(b):return hashlib.sha256(b).hexdigest()
def canon(o):return h(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8'))
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(p,o):p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n')),'bytes':len(b)}

lease=json.loads((RUN/'reviewer.primary.lease.json').read_text(encoding='utf-8'));assert lease['status']=='OPEN'
source=ROOT/'runs/20261007-companion-priority/phase-pbps-primary-preread48/primary.raw.snapshot.html'
b=source.read_bytes();assert h(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
text=b.decode('utf-8');lines=text.splitlines(keepends=True);offsets=[0]
for l in lines:offsets.append(offsets[-1]+len(l))
class Spans(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.spans={}
 def pos(self):l,c=self.getpos();return offsets[l-1]+c
 def handle_starttag(self,tag,attrs):
  if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:return
  self.stack.append((tag,dict(attrs).get('id'),self.pos()))
 def handle_startendtag(self,tag,attrs):
  sid=dict(attrs).get('id')
  if sid:self.spans[sid]=(self.pos(),self.pos()+len(self.get_starttag_text()))
 def handle_endtag(self,tag):
  index=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i][0]==tag),None)
  if index is None:return
  items=self.stack[index:];self.stack=self.stack[:index]
  end=text.index('>',self.pos())+1
  for _,sid,start in items:
   if sid:self.spans[sid]=(start,end)
parser=Spans();parser.feed(text)

groups={
 'standing-normalization-curvature':['S1.p1.1','S1.E1'],
 'actual-augmentation-and-outer-marginal':['S2.SS2.p1.1','S2.E6','S2.SS2.p1.2','S2.E7','S2.SS2.p1.3','S2.E8'],
 'reflection-involution-law':['S2.E14','S2.SS2.Thmtheorem1.p3.1'],
 'actual-operator-and-macro-identification':['A2.SS1.p1.3','A2.E1','A2.SS1.p1.4','A2.E2','A2.SS1.p1.5','A2.E3','A2.SS1.p3.1','A2.E4','A2.SS1.p3.2','A2.E5','A2.SS2.p1.1','A2.E8','A2.SS2.p2.2','A2.E9','A2.SS2.p3.1','A2.E10','A2.SS2.p3.2','A2.E11'],
 'printed-B13-full-L2-H1':['A2.Thmtheorem1.p1.1','A2.Thmtheorem1.p2.1','A2.E13'],
 'smooth-proof-and-integrated-C2':['A3.SS1.p1.1','A3.SS1.p2.1','A3.Ex1','A3.SS1.p2.2','A3.Ex2','A3.SS1.p2.3','A3.E1','A3.SS1.p3.1','A3.Ex3','A3.SS1.p3.2','A3.EGx24','A3.SS1.p3.3','A3.Ex5','A3.SS1.p3.4','A3.Ex6','A3.SS1.p3.5','A3.Ex7','A3.SS1.p3.6','A3.EGx25','A3.E2','A3.SS1.p3.7']}
# Locate the literal reflection preservation paragraph by its printed source text;
# do not invent an ID from a subsection naming guess.
groups['reflection-involution-law']=['S2.E14']+[sid for sid,(lo,hi) in parser.spans.items() if sid.startswith('S2.') and text[lo:hi].startswith('<p ') and 'preserves' in text[lo:hi] and 'involution' in text[lo:hi]]
records=[]
for family,ids in groups.items():
 for sid in ids:
  assert sid in parser.spans,sid
  lo,hi=parser.spans[sid];raw=text[lo:hi].encode('utf-8')
  path=RUN/('primary.span.'+sid+'.raw.html');assert not path.exists();path.write_bytes(raw)
  from_line=text.count('\n',0,lo)+1;to_line=text.count('\n',0,hi)+1
  records.append({'source_item_id':sid,'source_url':'https://arxiv.org/html/2609.06905v1#'+sid,'edition':'arXiv:2609.06905v1','role':family,'full_outer_balanced_fragment':True,'source_whole_raw_sha256':h(b),'start_byte':len(text[:lo].encode('utf-8')),'end_byte_exclusive':len(text[:hi].encode('utf-8')),'physical_lines':[from_line,to_line],'fragment':pin(path),'raw_fragment_sha256':h(raw),'lf_fragment_sha256':h(raw.replace(b'\r\n',b'\n'))})
assert groups['reflection-involution-law']!=['S2.E14']
copy=RUN/'primary.raw.snapshot.html';assert not copy.exists();copy.write_bytes(b)
inventory={'schema_version':1,'scope':'Independent primary49 anchor inventory, not an implementation/source-topology admission. Complete outer fragments for the exact source objects and two different domain levels needed for C.2/B.13; no claim of whole-paper exhaustive coverage.','primary':pin(source),'source_copy':pin(copy),'selected_groups':groups,'anchors':records,'anchor_count':len(records),'fragment_hash_rule':'Exact UTF8 balanced outer HTML bytes, separate from whole-file raw/LF SHA; byte offsets are zero-based, end exclusive.','source_section_disambiguation':'A3.E2 equation(C.2) lies inside Appendix C.1; subsection C.2 starts physical4897 and concerns half-turn, not this estimate.'}
inventory['inventory_run_sha256']=canon(inventory);write(RUN/'primary.inventory.json',inventory)

slots={
 'objects':'Target mu(dx)=Z^-1 exp(-V(x))dx; original joint pi_eta of X~mu, Z~N(0,I) independent and Y+=X+sqrt(eta)Z; Y-=X-sqrt(eta)Z, same marginal nu=pi_eta^Y=mu*N(0,eta I). The actual macro operator T=U_PP has Tf(y)=E[f(Y-)|Y+=y]. U_perpP is the microscopic reflection component, Gamma_P=(I-T^2)^(1/2) on the macro subspace.',
 'domains':'Printed source is R^d. Smooth proof begins with f in C_c^infinity(R^d). Norms of f and Tf are real scalar L2(nu) norms; gradient energy is norm-squared integrated against the SAME nu. B.13 separately prints arbitrary f in L2(nu) and Tf in weighted H1(nu). This source block does not spell out a formal graph-closure realization or a separate scalar-field declaration; a future real-valued representation and finite-Hilbert/rank-zero extension must be explicit, not inferred as a new theorem here.',
 'quantifiers':'Standing admissible V,alpha,beta,eta determine the actual law before observables. Source smooth estimate applies to every smooth compact f and integrates the pointwise y estimate over nu; B.13 then quantifies over every L2(nu) equivalence class via density and closedness. No mean-zero hypothesis on f. A valid future implementation must keep the SAME produced S, outer marginal nu and T throughout, not choose fresh unrelated witnesses after f.',
 'assumptions':'Global V in C2(R^d), 0<alpha<=beta, alpha I<=Hess V<=beta I everywhere, eta in (0,1/beta]. These are standing source hypotheses. Smooth compact f is the proof test class, not a hidden restriction on the printed all-L2 B.13. Normalization, conditional domains, gradient measurability/integrability and closedness are proof obligations, not public inequality/law certificates.',
 'conclusion':'For smooth compact f: eta*integral norm(grad Tf)^2 dnu <= A_eta*E Var(f(Y-)|Y+) where A_eta=(1-alpha*eta)^2/[4(1+alpha*eta)]; B.9 identifies EVar=normf_L2nu^2-normTf_L2nu^2=normU_perpP f^2=normGamma_P f^2. Printed B.13 for all f in L2(nu): Tf in H1(nu) and 4eta*energy<=normf^2-normTf^2=normGamma_Pf^2=normU_perpPf^2. No sampler contraction conclusion belongs to this precursor.',
 'scopes':'C.2 is the integrated smooth compact intermediate formula in Appendix C.1. The full L2-to-H1 B.13 extension invokes density and gradient closedness in only one sentence, requiring actual outer-law gradient-domain adapters. Fiberwise original D_y from score-variance is not automatically the outer nu gradient closure. Subsequent spectral bounds/C.3/B.14/B.15, affine half-turn subsectionC.2, main results/error/work/cost remain outside.',
 'constant_dependencies':'Pointwise coefficient C_eta=(eta^-1-alpha)^2/[4(alpha+eta^-1)] gives eta*C_eta=A_eta. From source eta>0, 0<alpha<=beta and beta*eta<=1 derive 0<alpha*eta<=1; hence 0<=A_eta<=1/4. Reflected W_y=V((y+u)/2)+norm(y-u)^2/(8eta), curvature lower (alpha+eta^-1)/4, parameter score factors -1/2 and -1/(4eta). No dimension factor or extra centering. At alpha*eta=1 A_eta=0.'}
binders=[
 {'item':'R^d and Euclidean gradients/L2 laws','classification':'SOURCE+TYPING','anchor':'S1.p1.1;A2.E2'},
 {'item':'V globally C2, positive ordered alpha/beta and evaluated global Hessian bounds','classification':'STANDING','anchor':'S1.p1.1;S1.E1'},
 {'item':'eta>0 and beta*eta<=1','classification':'SOURCE+STANDING','anchor':'S2.SS2.p1.1;A2.Thmtheorem1.p1.1'},
 {'item':'f globally smooth compact','classification':'SOURCE proof-test class','anchor':'A3.SS1.p1.1','boundary':'Must not turn into a public restriction while claiming the full all-L2 B.13.'},
 {'item':'f in actual L2(nu)','classification':'SOURCE full-theorem domain','anchor':'A2.Thmtheorem1.p2.1'},
 {'item':'normalized mu, actual joint, reflected conditional law, exchangeability, Tf and variance identities','classification':'DEFINED+DERIVED proof ingredients','anchor':'S2.E6/S2.E7/S2.SS2.p1.3;A2.E8/A2.E9','boundary':'Not supplied laws, selectors, kernel equality, variance or marginal-law certificates.'},
 {'item':'Tf L2, gradTf L2/measurable, H1 outer domain, approximation and closed gradient','classification':'DERIVED analytic obligations','anchor':'A3.SS1.p1.1;A2.E13','boundary':'No public gradient-domain/desired-energy certificate.'},
 {'item':'f mean zero, global input position moment, C-infinity V, extra positivity/covariance/PI inputs','classification':'EXCESS if added as source binders','anchor':'Absent from C.2/B.13 source hypotheses'},
 {'item':'finite real Hilbert/Borel incl rank0 or explicit kernel representatives','classification':'AUTHORED representation extension requiring later exact seal/proof','anchor':'not a separately printed binder in this source block'}]
sequence=[
 {'step':1,'source':'S2.E6/E7, S2.SS2.p1.3, S2.E14;A2.E8','obligation':'Produce true normalized augmentation law, reflection preservation and exchangeable Y+/Y- with common nu. No half-turn process or RGO law identification.'},
 {'step':2,'source':'A2.E1/E2/E4/E9','obligation':'Identify T on macro observables as literal conditional expectation. Establish actual measurability, L2 contraction and observer domain; the microscopic norm is expected conditional variance.'},
 {'step':3,'source':'A3.Ex1/Ex2/A3.E1/Ex3-Ex7','obligation':'Conditional density/parameter derivative normalization, real covariance, quarter-curvature Poincare and score variance yield genuine pointwise gradient bound for smooth compact f. All analytic domains derived.'},
 {'step':4,'source':'A3.SS1.p3.6;A3.E2','obligation':'Establish outer joint measurability and true L1 products/gradient energy, then integrate over nu using Tonelli/Fubini/disintegration. A pointwise totalized integral or fiber L2 fact is insufficient.'},
 {'step':5,'source':'A2.E9/A2.E11;A3.SS1.p3.7','obligation':'Use the actual common marginal and conditional second moment to obtain EVar=int f² dnu-int(Tf)² dnu. Recover Gamma and microscopic norm equalities only from actual operator construction, not a supplied norm-gap certificate.'},
 {'step':6,'source':'standing restrictions;A3.E2;A2.E13','obligation':'Exact eta coefficient algebra; 0<alpha*eta<=1 bounds A_eta by1/4 and gives4eta energy<=gap for smooth compact f.'},
 {'step':7,'source':'A3.SS1.p1.1;A2.Thmtheorem1.p2.1','obligation':'Full B.13 needs actual compact-smooth density in L2(nu), continuity of SAME T, Cauchy/weakly controlled gradient and closed outer gradient to produce H1 membership and pass the energy inequality. This omitted bridge is not granted by the source preread.'}]
gaps=[
 {'id':'OUTER-MARGINAL-LAW-AND-DISINTEGRATION','meaning':'True nu=J.snd is common Y+/Y- law and actual S integrates to it; exact same witness/order required.'},
 {'id':'GLOBAL-INTEGRAL-DOMAINS','meaning':'Kernel jointly measurable, f² and(Tf)² L1, actual gradTf AE-measurable and square L1; derived before real totalized integrals used. No moment premise for bounded smooth compact f.'},
 {'id':'ACTUAL-CONDITIONAL-VARIANCE-IDENTITY','meaning':'Fubini/disintegration with valid domains gives expected centered variance exactly as same-nu norm difference; operator Gamma equality needs unitary reflection plus P decomposition.'},
 {'id':'OUTER-L2-H1-CLOSED-GRADIENT','meaning':'Smooth compact density and weighted outer nu graph closure, with SAME T and AE reps. Pointwise source48 or existing fiber D_y cannot on their own establish all-L2 B.13.'},
 {'id':'SOURCE-H1-DEFINITION-AND-REPRESENTATION','meaning':'Source uses standard weighted H1 without a formal operator-definition realization here. Future seal must explicitly declare actual gradient-domain semantics and any real-field/finite-Hilbert/rank0 representation.'}]
contract={'schema_version':1,'reviewer':'phase_source_reviewer_20261005','status':'CLOSED_PRIMARY_ONLY_PREREAD_NOT_ADMISSION','created_utc':utc(),'primary':{**pin(source),'edition':'arXiv:2609.06905v1','url':'https://arxiv.org/html/2609.06905v1'},'source_copy':pin(copy),'primary_inventory':pin(RUN/'primary.inventory.json'),'chronology':{'lease_opened_before_source_reads':True,'historical_exposure':'Authorized prior PBPS/SPHMC source, preproof/topology and complete source48 actual ConditionalGradientVariance proof/Test/six-reader-step exposure is known. This49 contract is independently read from pinned primary after48 closure, not a claim of historical blindness.','source_only_current_task':True,'no49creator_capsule_candidate_target_API_or_implementation_read':True,'no_current_source48_exact_verifier_or_math_verdict_read':True,'compiler_started':False,'incidental_primary_only_context':'Read source B.1 full operator context and source search for H1; source A.1/A.2/A.3 and later C.1/C.2 H1 mentions partly surfaced while locating definitions. These are printed-primary exposure only, not candidate/API or future proof evidence; outside-slice claims remain excluded.'},'semantic_slots':slots,'recursive_binder_classification':binders,'actual_laws_and_gradients':{'mu':'normalized exp(-V) canonical Euclidean volume probability','joint':'law(X,X+sqrt(eta)Z), X~mu,Z~standard normal independent','outer':'nu=pi_eta^Y=mu*N(0,eta I), common lawY+ andY-, probability','conditional':'S_y=law(Y-|Y+=y), normalized exp(-W_y) reflected conditional; R unreflected X|Y is distinct','T':'Tf(y)=int f(u)S_y(du), macro PUP under literal source reflection','variance':'Var_{S_y}(f)=int(f-int f dS_y)^2 dS_y','energy':'int norm(grad Tf(y))² dnu(y); not volume or a single-fiber S_y integral','rough_domain':'Actual outer weighted H1(nu) via genuine weak/closed gradient; no claim that existing fiber D_y equals this domain'},'exact_formulas':{'pointwise':'norm(grad Tf(y))²<=C_eta*Var_{S_y}(f)','C_eta':'(eta^-1-alpha)^2/[4(alpha+eta^-1)]','integrated_C2':'eta*int norm(grad Tf)^2 dnu <= [(1-alpha*eta)^2/(4(1+alpha*eta))]*int Var_{S_y}(f)dnu(y)','variance_gap':'int Var_{S_y}(f)dnu = int f² dnu-int(Tf)² dnu = norm(U_perpP f)^2 = norm(Gamma_P f)^2','B13':'for all f in L2(nu): Tf in H1(nu), 4eta*int norm(grad Tf)^2 dnu<=int f² dnu-int(Tf)² dnu','coefficient_derivation':'eta*C_eta=(1-alpha*eta)^2/[4(1+alpha*eta)], 0<alpha*eta<=1 implies this in[0,1/4]','zero_endpoint':'alpha*eta=1 gives sharp integrated coefficient0; no unit-vector selection needed. Source rank-zero representation is prospective authored extension, not admitted here.'},'source_proof_dependency_order':sequence,'implicit_analytic_obligations':gaps,'smooth_vs_complete_boundary':{'smooth':'Actual pointwise differentiability plus derived global gradient-energy/variance L1 allows integrated C.2 under nu. This is substantive outer integration, not a restatement of a pointwise estimate.','full':'B.13 prints all-L2-to-H1. Source density/closedness line is an omitted analytic bridge requiring proof, not an input norm or domain certificate. No mean-zero f assumption.','strong_coefficient_extension':'A3.E2 is shown on the smooth proof test class; extending the sharper coefficient to allL2 would require the same genuine closure passage and should be declared separately in a later signature.'},'explicit_exclusions':['SubsectionC.2 half-turn begins4897, distinct from equationC.2 insideC.1','C.3 and subsequent spectral/centered macroscopic coercivity/B.14/B.15/secondpartLemmaB1','Actual samplerK/Hhalfturn/reversibility/contraction/composition','Outer-domain graph producer/complete B13 not proved by this contract','Main four papers/error/work/expectedcost/TV-cost/GaussianLSI/T2/PURIFIED/live reader completion'],'hypothesis_failure_boundaries':['Replacing nu by volume orS_y changes the source energy/norms.','Substituting a different existential kernel after f breaks same-law integration.','Totalized integrals do not certify L1/L2 or probability.','Centering f is not a source premise for C.2/B.13.','Fiberwise domain closure is not automatically outer-law H1.','Smoothcompact estimate alone is not the source completeL2→H1 claim.','Using source32RGO/unreflected posterior scaling loses reflectedquarter; no such law identification is justified here.'],'input_artifacts':[pin(source)],'review_run_hash_recipe':'SHA256 UTF8 json.dumps(entire object minus review_run_sha256,ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False)','no_theorem_or_source_admission':True,'final_leases':{'read':'CLOSED','write':'CLOSED','Python':'CLOSED','compiler':'CLOSED','compiler_started':False}}
contract['review_run_sha256']=canon(contract);write(RUN/'primary.contract.json',contract)
inputs={'input_artifacts':[pin(source)],'output_artifacts':[pin(copy),pin(RUN/'primary.inventory.json'),pin(RUN/'primary.contract.json'),*[r['fragment'] for r in records]],'only_primary_consumed':True,'no_API_candidate_math_verdict_or_compiler':True};inputs['input_run_sha256']=canon(inputs);write(RUN/'primary.inputs.json',inputs)
assert h(source.read_bytes())==contract['primary']['raw_sha256']
lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','closed_utc':utc(),'primary_contract':pin(RUN/'primary.contract.json'),'primary_review_run_sha256':contract['review_run_sha256'],'inputs':pin(RUN/'primary.inputs.json'),'outcome':'Independent primary49 contract frozen before target/API/candidate; no source completion/admission'})
lease['lease_run_sha256']=canon(lease);write(RUN/'reviewer.primary.lease.json',lease)
print(json.dumps({'contract':pin(RUN/'primary.contract.json'),'review_run_sha256':contract['review_run_sha256'],'inventory':pin(RUN/'primary.inventory.json'),'inputs':pin(RUN/'primary.inputs.json'),'lease':pin(RUN/'reviewer.primary.lease.json'),'anchor_count':len(records),'all_leases':'CLOSED'},ensure_ascii=False))
