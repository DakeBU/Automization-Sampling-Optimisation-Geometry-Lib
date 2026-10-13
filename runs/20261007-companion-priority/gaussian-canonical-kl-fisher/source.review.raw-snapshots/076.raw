from pathlib import Path
import json, hashlib, re, datetime

D=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def put(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    (D/name).write_bytes(data)
def txt(name): return (D/name).read_text(encoding='utf-8-sig')
inputs=json.loads(txt('inputs.json'))
correction=next(i for i in inputs if i['id']=='primitive-integrable-congr')
old=(D/'primitive-integrable-congr.raw.snapshot').read_bytes()
if b"congr'_enorm" in old:
    (D/'primitive-integrable-congr.initial-misbound.raw.snapshot').write_bytes(old)
    (D/'primitive-integrable-congr.initial-misbound.lf.snapshot').write_bytes((D/'primitive-integrable-congr.lf.snapshot').read_bytes())
iraw=Path(correction['path']).read_bytes()
iline=iraw.decode('utf-8').splitlines()[122]
assert iline.startswith('theorem Integrable.congr {')
isig=iline.split(' :=')[0]+'\n'
(D/'primitive-integrable-congr.raw.snapshot').write_bytes(isig.encode())
(D/'primitive-integrable-congr.lf.snapshot').write_bytes(isig.encode())
correction.update(raw_sha256=sha(isig.encode()),lf_sha256=sha(isig.encode()),selected_ranges=[[1,1]],actual_source_public_range=[123,123],whole_file_raw_sha256=sha(iraw),correction='Initial neighboring105-106 congr_enorm excerpt was mechanically mislabeled; preserved as initial-misbound snapshot, excluded, corrected to exact123 congr public contract before :=')
ap=Path('.lake/packages/mathlib/Mathlib/Order/Filter/Basic.lean')
raw=ap.read_bytes(); lines=raw.decode('utf-8').splitlines(keepends=True)
sig=lines[654].split(' :=')[0]+'\n'
(D/'primitive-AE-all.raw.snapshot').write_bytes(sig.encode())
(D/'primitive-AE-all.lf.snapshot').write_bytes(sig.replace('\r\n','\n').encode())
inputs.append({'id':'primitive-AE-all','path':str(ap),'raw_sha256':sha(sig.encode()),'lf_sha256':sha(sig.replace('\r\n','\n').encode()),'selected_ranges':[[1,1]],'actual_source_public_range':[655,655],'qualified_identifier':'Filter.Eventually.of_forall','whole_file_raw_sha256':sha(raw),'expansion':'exact contract only, proof opaque'})
route=txt('authored-route.md').splitlines()
inputs.append({'id':'authored-route','path':'authored-route.md','raw_sha256':sha((D/'authored-route.md').read_bytes()),'lf_sha256':sha(txt('authored-route.md').replace('\r\n','\n').encode()),'selected_ranges':[[1,len(route)]],'kind':'independent mathematical source reconstruction, not implementation'})
put('source-inputs.json',inputs)
nodes=[]; edges=[]; coverage=[]; uses=[]
def node(id,kind,claim,**kw):
    nodes.append(dict(id=id,kind=kind,claim=claim,**kw))
def edge(a,b,site,reason,kind='planned-mathematical-use'):
    eid='edge:%03d'%(len(edges)+1)
    edges.append(dict(id=eid,prerequisite=a,consumer=b,caller=site,reason=reason,kind=kind))
    uses.append(dict(id='use:%03d'%(len(uses)+1),edge=eid,caller=site,callee=a,kind=kind,resolution='source/API contract or explicit mathematical obligation; no43Lean observed'))
def cov(src,line,nid=None,why=None,**kw):
    coverage.append(dict(source=src,line=line,classification='NODE' if nid else 'EXCLUDED',node=nid,reason=why,**kw))
def span(src,a,b,nid,why=None):
    for l in range(a,b+1): cov(src,l,nid,why)
N='paper:2609.06906v1:'
node(N+'standing','SOURCE','C² normalized potential; kappa^-1 I <= Hessian V <= I; beta=1',physical_lines=[606,609])
node(N+'prox','SOURCE','Positive-step proximal minimizer of V(x)+norm(x-y)^2/(2eta)',physical_lines=[612,618])
node(N+'RGO','SOURCE','Actual RGO proportional exp(-V-quadratic)',physical_lines=[627,632])
node(N+'KL','SOURCE','KL=integral log(dP/dQ) dP; +infinity without AC',physical_lines=[657,660],semantic_exclusions=['W2 definition on mixed physical line657'])
node(N+'proxalias','SOURCE','x_y^+=prox_etaV(y)',physical_lines=[1182,1188])
node(N+'stationarity','SOURCE','gradient V(p)=(y-p)/eta',physical_lines=[1289,1290])
node(N+'rho-law','SOURCE','rho uses negative linear term; standardized actual RGO density exp(-norm u²/2-rho)',physical_lines=[1295,1300],semantic_exclusions=['Hessianrho bound on line1298 is context, not separately used'])
node(N+'FIRSTcontext','CONTEXT_ONLY','Paper FIRST4.6 W2/Fisher/moment chain; no43 completion of this chain',physical_lines=[1306,1308])
node(N+'LSI-T2-invocation','SOURCE','First FIRST inequality combines Gaussian Talagrand and Gaussian LSI',physical_lines=[1310,1311],chosen_leaf='LSI/canonical KL component only')
node('source-gap:standalone43','SOURCE_GAP','Paper does not print standalone canonical KL<=Fisher/2 or formal32/33 witness composition; internally authored obligations R03-R12 close this interface gap, without extra public premise')
node('boundary:GaussianT2','EXTERNAL_UNEXPANDED','Gaussian Talagrand/T2 source invocation; not a43 prerequisite; remains separate unexpanded source branch')
node('boundary:GaussianLSI','OPAQUE_PARENT_BOUNDARY','Source-invoked Gaussian LSI supplied by accepted42 public contract;42 analytic proof expansion excluded')
edge('boundary:GaussianT2',N+'FIRSTcontext',{'source':'primary','lines':[1310,1311]},'Source names Talagrand for FIRST; context branch only','source-prose-named-use')
edge('boundary:GaussianLSI',N+'FIRSTcontext',{'source':'primary','lines':[1310,1311]},'Source names Gaussian LSI for FIRST; bound expanded only through opaque42','source-prose-named-use')
pmap={606:N+'standing',607:N+'standing',608:N+'standing',609:N+'standing',612:N+'prox',613:N+'prox',618:N+'prox',620:N+'prox',627:N+'RGO',632:N+'RGO',652:N+'KL',657:N+'KL',660:N+'KL',1182:N+'proxalias',1183:N+'proxalias',1188:N+'proxalias',1289:N+'stationarity',1290:N+'stationarity',1295:N+'rho-law',1298:N+'rho-law',1299:N+'rho-law',1300:N+'rho-law',1301:N+'FIRSTcontext',1306:N+'FIRSTcontext',1308:N+'FIRSTcontext',1310:N+'LSI-T2-invocation',1311:N+'LSI-T2-invocation'}
for inp in inputs:
    if inp['id']=='primary':
        for a,b in inp['selected_ranges']:
            for l in range(a,b+1):
                cov('primary',l,pmap.get(l),None if l in pmap else ('separate query-cost/TV/W2/gradient-growth/moment branch' if l in [635,650,651,661,1312,1313,1314] else 'HTML structure/spacing/proof marker without mathematical ingredient'))
parents=json.loads(txt('preread-detail.lf.snapshot'))['parents']
for sid,idx in [('032consumer',0),('033consumer',1),('042signature',2)]:
    node('parent:'+sid,'OPAQUE_VERIFIED_PUBLIC_PARENT',parents[idx]['full_declaration'],qualified_identifier=parents[idx]['full_declaration'],contract_snapshot=sid+'.lf.snapshot',status_basis='32/33 verified and42 VERIFIED13556ea per root; public contracts inspected independently; not own proof verification',body_selected=False)
node('interface:standing','BINDER_CONTRACT','Exact32/33/43 shared carrier, C², kappa>=1, Hessian sandwich, measurable eta/y, eta>0')
node('interface:literal-definitions','DEFINITION_CONTRACT','rho,mu,R,r,gamma,Z,q,f are literal32/33 lets; p-dependent rho/Z/q/f/r all transported; mu/R/gamma independent of p')
node('slot32:stationarity','DERIVED_OUTPUT','forall s,p32+eta*gradient V(p32)=y')
node('slot32:domains','DERIVED_OUTPUT','C²f,MemLp f2 gamma,MemLp gradient f2 gamma,MemLp gradientrho2 r,Integrable qlogq gamma')
node('slot32:mass-square','DERIVED_OUTPUT','Pointwise f²=q; integral_gamma q=1; actual r probability')
node('slot32:quarter-energy','DERIVED_OUTPUT','integral_gamma norm gradient f²=(1/4)*integral_r norm gradientrho²; same literal p/rho/r')
node('slot32:score-meaning','INTERPRETATION_ONLY','Pointwise gradient(log q)=-gradientrho identifies actual smooth relative score; no differentiation of canonical llr')
node('slot33:unique','DERIVED_OUTPUT','Measurable stationary p33; every stationary z=p33')
node('slot33:finite-KL','DERIVED_OUTPUT','Actual r AC gamma and canonical klDiv(r,gamma) != top')
node('slot33:KL-entropy','DERIVED_OUTPUT','Canonical KL.toReal=integral_gamma qlogq; finite KL established separately')
node('interface:llr-AE','INTERPRETATION_ONLY','33 canonical llr=logq only AE under r; not pointwise, never differentiated')
node('target:43','SEALED_TARGET','Exact1368 LF theorem unique proximal witness and canonical KL.toReal <= (1/2)*actual rho-gradient energy',lf_sha256='6560113333ab09326b0d02e0e3f4bf628457fa92bb21756fbc8b27d65d5d8000',statement_only=True)
mapping32={**{i:'interface:standing' for i in range(2,10)},10:'parent:032consumer',11:'slot32:stationarity',**{i:'interface:literal-definitions' for i in range(12,21)},24:'slot32:mass-square',25:'slot32:mass-square',26:'slot32:mass-square',27:'slot32:domains',28:'slot32:domains',29:'slot32:domains',31:'slot32:score-meaning',32:'slot32:quarter-energy',33:'slot32:quarter-energy',1:'parent:032consumer'}
mapping33={**{i:'interface:standing' for i in range(2,10)},10:'slot33:unique',11:'slot33:unique',12:'slot33:unique',**{i:'interface:literal-definitions' for i in range(13,21)},21:'slot33:finite-KL',22:'slot33:finite-KL',23:'interface:llr-AE',24:'interface:llr-AE',26:'slot33:KL-entropy',27:'slot33:KL-entropy',1:'parent:033consumer'}
for i in range(1,34): cov('032consumer',i,mapping32.get(i),None if i in mapping32 else 'Unused normalization/tilted-withDensity/explicit gradientf clause; already opaque parent output, not separately needed')
for i in range(1,30): cov('033consumer',i,mapping33.get(i),None if i in mapping33 else 'Unused rho L1/alternate minus-rho-logZ representation; canonical identity sufficient')
for parent,slot,loc in [
 ('032consumer','slot32:stationarity',[11,11]),('032consumer','slot32:domains',[27,29]),('032consumer','slot32:mass-square',[24,26]),('032consumer','slot32:quarter-energy',[32,33]),('032consumer','slot32:score-meaning',[31,31]),
 ('033consumer','slot33:unique',[10,12]),('033consumer','slot33:finite-KL',[21,22]),('033consumer','slot33:KL-entropy',[26,27]),('033consumer','interface:llr-AE',[23,24])]:
    edge('parent:'+parent,slot,{'source':parent,'lines':loc},'Exact public output clause projection; generated projection syntax is not a new mathematical call','public-contract-output-projection')
for paper,consumer in [(N+'standing','interface:standing'),(N+'prox','interface:literal-definitions'),(N+'RGO','interface:literal-definitions'),(N+'proxalias','interface:literal-definitions'),(N+'rho-law','interface:literal-definitions'),(N+'KL','slot33:KL-entropy'),(N+'LSI-T2-invocation','source-gap:standalone43')]:
    edge(paper,consumer,{'source':'primary','lines':next(n['physical_lines'] for n in nodes if n['id']==paper)},'Source correspondence/evidence relation; not compiled parent implication','source-correspondence')
span('042signature',1,13,'parent:042signature')
span('043signature',1,23,'target:43')
for inp in inputs:
    if inp['id'].startswith('primitive-'):
        node('api:'+inp['id'],'EXTERNAL_UNEXPANDED_API',txt(inp['id']+'.lf.snapshot').strip(),qualified_identifier=inp['qualified_identifier'],provider_path=inp['path'],provider_lines=inp['actual_source_public_range'],proof_selected=False)
        for a,b in inp['selected_ranges']: span(inp['id'],a,b,'api:'+inp['id'])
node('primitive:funext','FOUNDATIONAL_CONTRACT','For f,g:S->E,(forall s,f s=g s)->f=g; kernel function extensionality, no Lean implementation/QName claim')
node('primitive:equality-transport','FOUNDATIONAL_CONTRACT','Equality substitution transports any dependent expression/claim; equality of rho functions also transports true gradient, integrals and domains')
node('primitive:real-arithmetic','FOUNDATIONAL_CONTRACT','For every I:real,2*((1/4)*I)=(1/2)*I; rational-field identity including I=0; not a compiled43 edge')
steps={}
for line,text in enumerate(route,1):
    m=re.match(r'R(\d\d) ',text)
    if m:
        id='obligation:R'+m[1]; steps[m[1]]=id
        node(id,'INTERNAL_OBLIGATION' if int(m[1])<13 else 'SCOPE_CONTRACT',text,caller_lines=[line,line],compiled=False)
        cov('authored-route',line,id)
    else: cov('authored-route',line,None,'heading/spacing')
def dep(src,step,why): edge(src,steps[step],{'source':'authored-route','lines':next(n['caller_lines'] for n in nodes if n['id']==steps[step])},why)
for src,st,why in [
 ('parent:032consumer','01','Apply exact public32 under sealed input assumptions'),('interface:standing','01','Public inputs exactly shared'),
 ('parent:033consumer','02','Apply exact public33, choose its witness'),('interface:standing','02','Same source inputs'),
 ('slot32:stationarity','03','Antecedent for uniqueness at z=p32'),('slot33:unique','03','Conclusion p32(s)=p33(s)'),('primitive:funext','03','Pointwise to family equality'),
 ('obligation:R01','03','Obtains p32 and stationarity'),('obligation:R02','03','Obtains p33 and uniqueness'),
 ('obligation:R03','04','Use actual witness equality'),('interface:literal-definitions','04','Transport every literal p-dependent let'),('primitive:equality-transport','04','Dependent transport including r'),
 ('obligation:R04','05','Coherent all32/33 outputs'),('slot33:unique','05','Retain measurable unique stationary witness'),('slot33:finite-KL','05','Retain actual AC and finite canonical KL'),('slot32:domains','05','Transport actualrho-gradient L2'),('slot32:mass-square','05','Retain probability'),
 ('obligation:R04','06','Domains and functions share chosen witness'),('slot32:domains','06','Analytic42 domains produced internally'),('slot32:mass-square','06','Pointwise f²=q'),('api:primitive-AE-all','06','Pointwise equality gives AE integrand equality'),('api:primitive-integrable-congr','06','Transport qlogq integrability to Phi(f²)'),
 ('obligation:R06','07','All42 inputs discharged'),('parent:042signature','07','Opaque verified actual Gaussian LSI coefficient2'),
 ('slot32:mass-square','08','Pointwise square identity and unit mass'),('obligation:R04','08','Same p/q/f/r'),('api:primitive-AE-all','08','AE identities from pointwise'),('api:primitive-integral-congr','08','Both integrals agree'),('api:primitive-square-L1','08','Actual fL2 supplies integrable square if required by Lean route'),
 ('obligation:R07','09','Homogeneous entropy inequality'),('obligation:R08','09','Mass1 and entropy identity'),('api:primitive-log-one','09','Unit masslogmass vanishes'),
 ('obligation:R09','10','qlogq bounded by twice energy'),('slot33:KL-entropy','10','Canonical KL.toReal entropy identity'),('slot32:quarter-energy','10','Actual quarter Fisher identity'),('obligation:R04','10','Same literal witness/law'),
 ('obligation:R10','11','Canonical KL<=2*(quarter energy)'),('primitive:real-arithmetic','11','Exact coefficienthalf'),
 ('obligation:R05','12','Required witness/probability/AC/finiteKL/L2 outputs'),('obligation:R11','12','Exact KLhalfFisher'),('target:43','12','Exact statement shape checked for output assembly'),
 ('source-gap:standalone43','13','Explicit source omission rather than new assumption'),('interface:llr-AE','13','Representative boundary'),
 ('boundary:GaussianT2','14','Not included in chosen43 route'),(N+'FIRSTcontext','14','RemainingFIRST outside leaf')]: dep(src,st,why)
edge(steps['12'],'target:43',{'source':'authored-route','lines':[14,14]},'Authored route intended to establish exact sealed target; no compiled claim','intended-conclusion')
# Direction above target -> assembly is specification, not prerequisite: avoids artificial cycle.
for e in edges:
    if e['prerequisite']=='target:43' and e['consumer']==steps['12']:
        e['kind']='specification-reference'
        next(u for u in uses if u['edge']==e['id'])['kind']='specification-reference'
for inp in inputs:
    if inp['id'] in ['043seal','043proposal','preread-detail']:
        for a,b in inp['selected_ranges']:
            for l in range(a,b+1): cov(inp['id'],l,None,'metadata/provenance source-before-candidate or statement admission; not mathematical source ingredient')
put('sourcegraph.json',{'schema':'bounded-source-graph43-v1','schema_contract':{'edges':'prerequisite -> consumer; specification-reference excluded from mathematical DAG','caller_inventory':'every direct named planned use in selected authored mathematical route or selected paper prose; public parent/API bodies opaque','slots':'interface clauses are outputs/typing/definitions, not invented mathematical calls','status':'independent source reconstruction; creator cannot admit topology; no43compiled edge','alternative_routes':'one sufficient AND route; no distinct meaningful OR route claimed'},'source_ids':['arxiv:2609.06906v1','mathlib:db584cd6d46c92f209a44c0f1c829460d327499d'],'nodes':nodes,'edges':edges,'OR_nodes':[]})
put('source-coverage.json',{'unit':'physical pinned LF line; parent excerpts have original physical offsets recorded in source-inputs; terminal :=by/body suffix excluded','rows':coverage,'mixed_line_semantic_exclusions':{'primary:657':'W2 half of mixed physical line is context outside selected canonical KL leaf','primary:1298':'rhoHessian statement context only','primary:1306':'entireFIRSTchain context only, no theorem credit'},'expansion_boundary':'public-only parent and primitive signatures; no provider proof bodies selected or inferred'})
put('caller-inventory.json',{'kind':'planned independent source mathematical uses, not implementation calls','uses':uses,'interface_token_inventory':{'math_terms':['gradient = actual Hilbert/Riesz gradient','fderiv = second Frechet derivative input sandwich','Measure.tilted = normalized tilted actual laws via literal parent lets','Measure.map = actual affine pushforward','stdGaussian E = actual Gaussian parent carrier','Real.exp/log/sqrt = literal density/entropy constants','MemLp/Integrable = finite domain contracts','InformationTheory.klDiv = actual canonical KL, finite before toReal','llr AE = only representative identity; no differentiation'],'type_or_generated_fields_not_calls':['carrier instances','conjunction projections','existential witnesses','let bindings','attributes','structure fields'],'external_unexpanded':'terms fixed by exact reviewed32/33/42 public contracts; not independently rederived or advertised as new43 calls'}})
put('sourcecontract.json',{'actor':'gaussian_noncompact_preread_42','role':'independent sourcegraph creator, distinct from root futureformalizer and Gauss topology validator','status':'SOURCE_GRAPH_AUTHORED_AWAIT_DISTINCT_TOPOLOGY_REVIEW','source_first':{'historical_preread_detail_sha256':'1527b40ca0cc0003bb98c7b0e1e55220f23e3a21280de6796b87d663986ba08a','historical_run_sha256':'ba484dec759fb649b3f4e27aa2243e0987e64b1021a1adda94338e47fb8b81ef','primary_before_candidate':'closed43 preread originals remain immutable; prior42 metadata exposure is explicitly retained'},'chosen_route':'single AND32/33/42 contract joining; no42DCT proof expansion','same_witness':'choosep33;33uniqueness applied to32stationarity; funext; transport rho/Z/q/f/r including affine map; mu/R/gamma independent','normalizations':{'source':'beta1,kappa>=1,Hessian kappa^-1I<=H<=I,eta>0 allsteps','constants':['32mass1','42LSI2','32energyquarter','43canonicalhalf'],'zero_sign_rank':'42 actual signedC2 theorem includes zeros;32fpositive is output;rank0 carrier extension requires no division bydimension,scalar identity holdsI0'},'binder_classes':{'source_inputs':'V C2/kappa/Hessian normalized standing assumptions/positiveeta','typing_extensions':'finite real complete Hilbert Borel; measurable S/eta/y, Unit recovers fixedsource;rank0 authored extension','internal_outputs':'samep,probability,AC,finiteKL,rho-gradientL2,C2f,fL2,gradientfL2,qlogqL1,mass1,energyquarter','excess_if_public':'witnesscoherence,domains,LSI/KLbound,T2,law/energy/limitcertificates'},'source_gap':'source invokesGaussianLSI+Talagrand but omits standalonecanonicalKLleaf/formal witnessjoin; internallyauthoredR03-R12, no theoremassumptionrepair','exposure':{'prior_accidental':'Earlier41 metadata/decoder-binding originaltext and32 body236-249 exposure recorded in42preread; notfreshblind','current':'own43preread,primary selectedslices,32/33 exact publicheader before :=by,42 exact691TXT,43seal/proposal/signature, narrowMathlibAPIcontracts and nearbyAPIlookup context','read42body_DCTgraph_reviewer_blind_Test':False,'read_or_write43implementation':False,'compiler_or_claim_or_canonical_write':False,'administrative':'root reported42VERIFIED13556ea/shared01a09f2d; not source-proof evidence examined by this actor'},'remaining':['distinct topology admission','root43 implementation and independent exactcompiler/blind/source review','GaussianT2/W2/restFIRST4.6/momentbound parent31/separatealgorithm/mains/errorcost/expositionPURIFIED']})
expected={(i['id'],l) for i in inputs for a,b in i['selected_ranges'] for l in range(a,b+1)}
actual=[(r['source'],r['line']) for r in coverage]
ids={n['id'] for n in nodes}
errors=[]
if len(actual)!=len(set(actual)): errors.append('duplicate coverage')
if set(actual)!=expected: errors.append('coverage mismatch')
if any(e['prerequisite'] not in ids or e['consumer'] not in ids for e in edges): errors.append('danglingedge')
if any(r['classification']=='NODE' and r['node'] not in ids for r in coverage): errors.append('danglingcoverage')
if len(uses)!=len(edges): errors.append('calleredgecount')
adj={i:[] for i in ids}
for e in edges:
    if e['kind']!='specification-reference': adj[e['prerequisite']].append(e['consumer'])
seen=set(); active=set()
def visit(i):
    if i in active: errors.append('cycle:'+i);return
    if i in seen:return
    active.add(i)
    for j in adj[i]: visit(j)
    active.remove(i);seen.add(i)
for i in ids:visit(i)
put('structural-check.json',{'status':'PASS' if not errors else 'FAIL','errors':errors,'nodes':len(nodes),'edges':len(edges),'planned_named_uses':len(uses),'coverage_rows':len(coverage),'NODE_rows':sum(r['classification']=='NODE' for r in coverage),'EXCLUDED_rows':sum(r['classification']=='EXCLUDED' for r in coverage),'claim':'bookkeeping consistency only; not independent topology admission/theorem approval/compiler evidence'})
if errors: raise RuntimeError(errors)
check=json.loads(txt('structural-check.json'))
check['caller_records']=len(uses)
check['planned_named_uses']=sum(u['kind'] in ['planned-mathematical-use','source-prose-named-use'] for u in uses)
check['generated_projections_counted_as_calls']=False
put('structural-check.json',check)
contract=json.loads(txt('sourcecontract.json'))
contract['API_correction']=correction['correction']
contract['historical_inputs_manifest']='inputs.json remains original capture manifest; source-inputs.json binds current corrected exact contract. Initial misbound excerpt is preserved and excluded from chosen graph.'
put('sourcecontract.json',contract)
put('qualified-api-resolution.json',{'status':'source-level contract and enclosing namespace checked; no compiler resolution claimed','opaque_parents':[n for n in nodes if n['kind']=='OPAQUE_VERIFIED_PUBLIC_PARENT'],'primitive_contracts':[n for n in nodes if n['kind']=='EXTERNAL_UNEXPANDED_API'],'namespace_evidence':{'Filter.Eventually.of_forall':['Mathlib/Order/Filter/Basic.lean',143,655,1270],'MeasureTheory.Integrable.congr':['Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',52,123,1178],'MeasureTheory.MemLp.integrable_sq':['Mathlib/MeasureTheory/Function/L2Space.lean',36,42,301],'MeasureTheory.integral_congr_ae':['Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',137,299,1354],'Real.log_one':['Mathlib/Analysis/SpecialFunctions/Log/Basic.lean',35,107,518]},'foundational_non_API_contracts':['function extensionality','equality substitution','real rational arithmetic'],'excluded':'No manufactured43 implementation/QName/call; public generated conjunction projections not mathematical calls'})
