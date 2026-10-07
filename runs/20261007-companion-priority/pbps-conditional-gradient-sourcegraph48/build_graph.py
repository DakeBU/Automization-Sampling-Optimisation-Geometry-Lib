# -*- coding: utf-8 -*-
"""Independent mathematical source graph, not a Lean implementation or compiler graph."""
from pathlib import Path
import re,json,hashlib,datetime,sys,html
sys.stdout.reconfigure(encoding='utf-8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-conditional-gradient-sourcegraph48';P47=R/'runs/20261007-companion-priority/next-ready-preread47'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(n,x):(O/n).write_bytes(enc(x))
assert json.loads((O/'lease.json').read_text(encoding='utf-8-sig'))['state']=='OPEN'
assert json.loads((O/'source-before-target.contract.json').read_text(encoding='utf-8'))['candidate_text_read'] is False
inputs=[]; selected=[];nodes=[];edges=[];coverage=[];callers=[]
def input_range(sid,path,ranges,kind,stop_column=None):
 raw=(R/path).read_bytes();rows=raw.splitlines(keepends=True)
 if stop_column:
  a,b=ranges[0];part=b''.join(rows[a-1:b-1])+rows[b-1][:stop_column-1]
 else:part=b''.join(b''.join(rows[a-1:b]) for a,b in ranges)
 (O/(sid+'.raw.snapshot.txt')).write_bytes(part);(O/(sid+'.lf.snapshot.txt')).write_bytes(lf(part))
 inp=dict(id=sid,path=path,kind=kind,whole_raw_sha256=sha(raw),whole_lf_sha256=sha(lf(raw)),selected_physical_ranges=ranges,fragment_raw_sha256=sha(part),fragment_lf_sha256=sha(lf(part)),fragment_raw_bytes=len(part),end_column_exclusive=stop_column)
 inputs.append(inp);selected.append(dict(id=sid,path=path,ranges=ranges,kind=kind,stop_column=stop_column))
 return inp
def node(n,kind,formula,source=None,**extra):
 nodes.append(dict(id=n,kind=kind,formula=formula,source=source,status='SOURCE_OR_PLANNED_OBLIGATION_NOT_NEW_COMPILED_TRUTH',**extra))
def edge(a,b,reason,kind='mathematical-dependency',**extra):edges.append(dict(from_id=a,to_id=b,kind=kind,reason=reason,**extra))
def cov(sid,a,b,n=None,why=None,sub=None):
 for line in range(a,b+1):coverage.append(dict(input_id=sid,physical_line=line,classification='NODE' if n else 'EXCLUDED',node_ids=[n] if n else [],reason=why or 'Exact selected mathematical source or contract',subclause_exclusions=sub or []))
def call(callee,caller,sid,a,b,role='planned-mathematical-use',note=''):
 callers.append(dict(callee=callee,caller_node=caller,input_id=sid,exact_caller_span=[a,b],role=role,note=note,compiled_call_claim=False))
# Freeze the exact target text; the declaration is still prospective at creator time.
target='runs/20261007-companion-priority/pbps-conditional-gradient-preproof48/prospective-statement.txt'
raw=(R/target).read_bytes();assert len(lf(raw))==1356 and sha(lf(raw))=='770bb0bac75b2f2c94fc72e68c1a5a19a1d4642cd2fcf15ea71b9aa608a65e61'
input_range('target',target,[(1,len(raw.splitlines()))],'prospective-statement-only')
primary='runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'
for sid,ranges in [('primary-global',[(348,363)]),('primary-augmentation',[(615,652)]),('primary-curvature',[(668,695)]),('primary-macro',[(3714,3735)]),('primary-C1',[(4566,4653)])]:input_range(sid,primary,ranges,'primary-proof-source')
parent_specs=[('score','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScore.lean','reflected_conditional_covariance',[36,57]),('variance','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScoreVariance.lean','conditional_centered_domain_and_score_variance',[11,43])]
for sid,path,name,span in parent_specs:
 raw=(R/path).read_bytes();rows=raw.splitlines(keepends=True);col=rows[span[1]-1].index(b':=')+1;pin=input_range('parent-'+sid,path,[span],'opaque-verified-producer-public-contract',col)
 frozen=(P47/(sid+'.public.raw.txt')).read_bytes();assert (O/('parent-'+sid+'.raw.snapshot.txt')).read_bytes()==frozen
 p47=json.loads((P47/'public-input-bindings.json').read_text(encoding='utf-8'));prior=next(x for x in p47 if x['id']==sid);assert sha(raw)==prior['whole_raw_sha256']
# Existing47 primitive contracts are reused, with original physical source locations.
p47prim=json.loads((P47/'primitive-input-bindings.json').read_text(encoding='utf-8'))
primitive_ids=['memLp-two-sq','L2-inner','Cauchy-Schwarz','CLM-integral','dual-norm-bound','bounded-L2','covariance-algebra']
for sid in primitive_ids:
 i=next(x for x in p47prim if x['id']==sid);path=i['path'];a,b=i['physical_ranges'][0];rows=(R/path).read_bytes().splitlines(keepends=True);col=rows[b-1].index(b':=')+1
 input_range('api-'+sid,path,[[a,b]],'external-unexpanded-Mathlib-public-contract',col)
 assert (O/('api-'+sid+'.raw.snapshot.txt')).read_bytes()==(P47/(sid+'.raw.txt')).read_bytes()
input_range('def-variance','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',[(28,29)],'selected-definition-body')
input_range('def-admissible','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',[(36,39)],'selected-definition-body')
input_range('def-gradient','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Gradient/Basic.lean',[(82,83)],'selected-definition-body')
input_range('def-tilted','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',[(42,43)],'selected-definition-body')
path='.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Dual.lean';rows=(R/path).read_bytes().splitlines(keepends=True);input_range('api-Riesz',path,[(135,135)],'external-unexpanded-definition-type-contract',rows[134].index(b':=')+1)
for sid,path,span in [('norm-map','.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/LinearIsometry.lean',[525,525]),('actual-fderiv','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Basic.lean',[415,419]),('differentiable','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Basic.lean',[221,222])]:
 rows=(R/path).read_bytes().splitlines(keepends=True)
 # Find proof delimiter inside the bounded public declaration, without exposing its body.
 tail=b''.join(rows[span[0]-1:span[1]]);pos=tail.index(b':=');before=tail[:pos];end=span[0]+before.count(b'\n');col=len(before.split(b'\n')[-1])+1
 input_range('api-'+sid,path,[(span[0],end)],'external-unexpanded-Mathlib-public-contract',col)
# Source assumptions, separately typed from generated outputs.
for n,f,s in [('H.space','Source R^d Euclidean; target finite realHilbert/Borel E including rank0',('primary-global',350,352)),('H.alpha','alpha>0',('primary-global',351,352)),('H.order','alpha<=beta, beta>=0',('primary-global',351,352)),('H.C2','V is globally C2',('primary-global',351,352)),('H.lower','alpha I <= Hess V',('primary-global',354,359)),('H.upper','Hess V <= beta I',('primary-global',354,359)),('H.eta','eta>0',('primary-augmentation',616,616)),('H.cap','beta eta<=1',('primary-augmentation',616,616)),('H.observer','f in C-infinity compact; all y',('primary-C1',4574,4576))]:node(n,'source-hypothesis',f,dict(input_id=s[0],span=list(s[1:])))
defs=[('D.mu','literal mu=volume.tilted(-V)','primary-augmentation',[617,624]),('D.gaussian','independent covariance-I Gaussian Z','primary-augmentation',[627,634]),('D.J','J=map(x,g -> x,x+sqrt eta*g)(mu.prod stdGaussian E)','primary-augmentation',[627,634]),('D.R','actual conditional X|Y kernel R','primary-augmentation',[641,650]),('D.S','S_y=map(x ->2x-y)R_y, literal normalized reflected density','primary-C1',[4580,4587]),('D.W','W_y(u)=V((y+u)/2)+norm(u-y)^2/(8eta)','primary-C1',[4581,4586]),('D.score','s_y(u)=-(1/2)DV((y+u)/2)-(1/(4eta))innerSL(y-u)','primary-C1',[4588,4594]),('D.T','T_f(y)=integral f dS_y = source U_PP f(y)','primary-macro',[3729,3735]),('D.variance','variance(S_y,f)=integral (f-integral f)^2 dS_y','def-variance',[28,29]),('D.gradient','gradient T=toDual.symm(fderiv T)','def-gradient',[82,83]),('D.normalization','tilted law=withDensity ofReal(exp(g)/integral exp(g))','def-tilted',[42,43]),('D.admissible','actual score L1, centered-square L1, gradient-energy L1','def-admissible',[36,39])]
for n,f,s,span in defs:node(n,'definition-semantics',f,dict(input_id=s,span=span))
source_steps=[('S.pair','Y+=X+sqrt eta Z; Y-=X-sqrt eta Z; Y-=2X-Y+','primary-macro',[3714,3724]),('S.derivative','normalized conditional density derivative equals actual score covariance','primary-C1',[4595,4604]),('S.curvature','Hess W_y >=(alpha+eta^-1)I/4','primary-C1',[4605,4614]),('S.PI','conditional Poincare gives unit score variance <=4/(alpha+eta^-1)*score-gradient energy','primary-C1',[4615,4625]),('S.score-gradient','beta eta<=1 implies norm D_u s_y <=(eta^-1-alpha)/4','primary-C1',[4626,4634]),('S.score-variance','unit score variance <=C=(eta^-1-alpha)^2/(4(alpha+eta^-1))','primary-C1',[4635,4643]),('S.CS','conditional scalar covariance Cauchy-Schwarz','primary-C1',[4644,4645]),('S.sup','take supremum over norm a=1, no dimension factor','primary-C1',[4644,4645]),('S.Ex7','norm gradient U_PP f(y)^2 <= C*actual conditional variance f','primary-C1',[4646,4653])]
for n,f,s,span in source_steps:node(n,'printed-source-proof-ingredient',f,dict(input_id=s,span=span),expansion_boundary='PI/differentiation analytic constructions are inherited opaque verified producers; printed source step remains separately represented.')
node('P.score','opaque-verified-production-interface','actual conditional R/S, literal normalized density, dual score L1 and true HasFDerivAt covariance',dict(input_id='parent-score',span=[36,57]),qualified_name='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore.reflected_conditional_covariance',verification='current47 DAG independently_verified; source interface unchanged, no fresh compiler')
node('P.variance','opaque-verified-production-interface','same literal reflected density, real score Admissible and all-direction variance <= C norm a^2',dict(input_id='parent-variance',span=[11,43]),qualified_name='AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScoreVariance.conditional_centered_domain_and_score_variance',verification='current47 DAG exact verified292878b81db3f6d6ff46bdf59ba98539f05ce87f, no fresh compiler')
node('S.unreflected-curvature','printed-source-proof-ingredient','alpha+eta^-1 <= Hess V_y <= beta+eta^-1, before reflected factor1/4',dict(input_id='primary-curvature',span=[687,694]))
node('I.source-dual-score','source-definition-correspondence','Actual dual s_y(u)(a) is inner product with the printed vector score; C2 DV/gradient and Riesz representation preserve norms/signs',dict(input_id='parent-score',span=[46,47]))
internal=[('I.sameS','Choose score-parent R/S; identify variance S-prime_y=S_y by both actual density formulas, norm-sub symmetry and negation algebra'),('I.domains','Markov S -> actual probability; compact continuous f bounded/L2; actual score Admissible and continuity produce centered score L2; all products genuinely integrable'),('I.evaluate','Evaluate true dual covariance derivative on any a by integral_apply, retaining normalized mean centering'),('I.scalar-CS','Real centered L2 CS gives |DT_f(y)[a]|^2 <= Var(f)*Var(s_y(a))'),('I.constant','alpha+1/eta>0; C>=0; exact quarter algebra and coefficient, not a desired-bound premise'),('I.directional','Insert actual parent directional score variance C norm(a)^2; a=0/zero variance included'),('I.dual-norm','All-direction homogeneous bound gives actual dual operator norm^2 <=C Var(f); replaces source unit sup without unit-existence premise'),('I.gradient','HasFDerivAt -> actual fderiv; isometric Riesz inverse -> literal gradient same norm'),('I.rank0','Rank0 has zero dual derivative/gradient; no positive-dimension or Nontrivial input'),('T.bound','Exact prospective1356 outputs R/S/literal law and all-f all-y DifferentiableAt plus actual gradient variance bound')]
for n,f in internal:node(n,'internally-derived-source-obligation',f,dict(input_id='target',span=[1,len((R/target).read_bytes().splitlines())]))
api_names={
 'memLp-two-sq':'MeasureTheory.memLp_two_iff_integrable_sq','L2-inner':'MeasureTheory.L2.inner_def','Cauchy-Schwarz':'real_inner_mul_inner_self_le','CLM-integral':'ContinuousLinearMap.integral_apply','dual-norm-bound':'ContinuousLinearMap.opNorm_le_bound','bounded-L2':'MeasureTheory.MemLp.of_bound','covariance-algebra':'ProbabilityTheory.covariance_eq_sub','norm-map':'LinearIsometryEquiv.norm_map','actual-fderiv':'HasFDerivAt.fderiv','differentiable':'HasFDerivAt.differentiableAt','Riesz':'InnerProductSpace.toDual'}
for sid,q in api_names.items():
 i=next(x for x in inputs if x['id']=='api-'+sid);node('A.'+sid,'external-unexpanded-primitive-contract',q,dict(input_id=i['id'],span=i['selected_physical_ranges'][0]),qualified_name=q,proof_body_selected=False)
for n,q in [('A.integral','MeasureTheory.integral'),('A.map','MeasureTheory.Measure.map'),('A.prod','MeasureTheory.Measure.prod'),('A.stdGaussian','ProbabilityTheory.stdGaussian'),('A.tilted','MeasureTheory.Measure.tilted'),('A.withDensity','MeasureTheory.Measure.withDensity'),('A.ofReal','ENNReal.ofReal'),('A.exp','Real.exp'),('A.fderiv','fderiv'),('A.symm','LinearIsometryEquiv.symm'),('A.innerSL','innerSL'),('A.norm_sub_rev','norm_sub_rev')]:
 node(n,'external-unexpanded-primitive-or-definition',q,qualified_name=q,contract='Foundational definition/identity; body not expanded, not a new theorem credit')
# Printed source topology, mathematically independent of future implementation.
for a,b,r in [('H.C2','S.derivative','smooth source density'),('D.S','S.derivative','differentiate actual normalized conditional density'),('D.score','S.derivative','true parameter-y score'),('H.lower','S.curvature','reflected scaling factor1/4'),('D.W','S.curvature','differentiate reflected potential'),('S.curvature','S.PI','genuine conditional PI background, inherited parent'),('H.upper','S.score-gradient','Hessian spectral upper and cap'),('H.lower','S.score-gradient','Hessian spectral lower'),('H.cap','S.score-gradient','eta^-1 >= beta'),('D.score','S.score-gradient','differentiate true score in u'),('S.PI','S.score-variance','apply unit directional PI'),('S.score-gradient','S.score-variance','bound energy exactly, including quarter'),('S.derivative','S.CS','true normalized covariance'),('S.score-variance','S.CS','actual score variance factor'),('S.CS','S.sup','all unit directions'),('S.sup','S.Ex7','Euclidean norm duality'),('D.T','S.Ex7','actual macro conditional expectation identification'),('S.pair','D.S','Y-=2X-Y+ actual reflection'),('D.J','S.pair','actual independent Gaussian augmentation'),('D.R','D.S','backward conditional fiber map')]:edge(a,b,r,'printed-source-dependency')
for a,b,r in [('S.unreflected-curvature','S.curvature','Reflection u->(y+u)/2 gives quarter factor'),('D.score','I.source-dual-score','literal dual score'),('H.C2','I.source-dual-score','actual DV and true gradient representation'),('A.Riesz','I.source-dual-score','isometric Riesz correspondence'),('I.source-dual-score','S.derivative','vector source vs dual parent derivative'),('I.source-dual-score','S.score-variance','unit projection matches actual directional score')]:edge(a,b,r,'source-correspondence')
for h in ['H.space','H.alpha','H.C2','H.lower','H.upper','H.eta']:edge(h,'P.score','Exact actual public parent premise')
for h in ['H.space','H.alpha','H.order','H.C2','H.lower','H.upper','H.eta','H.cap']:edge(h,'P.variance','Exact actual public parent premise')
for a,b,r in [('P.score','I.sameS','actual score witness choice'),('P.variance','I.sameS','actual alternate reflected law only'),('D.S','I.sameS','literal density equality'),('I.sameS','I.domains','transport actual score domains to chosen S'),('P.score','I.domains','actual integrable dual score and f-score'),('P.variance','I.domains','actual Admissible directional score'),('H.observer','I.domains','compact continuous f, no extra L2 premise'),('P.score','I.evaluate','actual true HasFDerivAt'),('I.domains','I.evaluate','legitimate evaluation/integral and centered products'),('I.evaluate','I.scalar-CS','exact scalar covariance'),('I.domains','I.scalar-CS','true centered L2 classes'),('I.scalar-CS','I.directional','CS scalar estimate'),('P.variance','I.directional','true directional score bound'),('I.sameS','I.directional','identical actual law'),('H.alpha','I.constant','positive denominator'),('H.eta','I.constant','positive eta'),('I.constant','I.directional','constant arithmetic'),('I.directional','I.dual-norm','all-vector estimate'),('I.constant','I.dual-norm','nonnegative norm bound'),('I.dual-norm','I.gradient','actual derivative operator norm'),('P.score','I.gradient','true derivative identification'),('I.gradient','T.bound','literal gradient result'),('P.score','T.bound','retain actual kernels and differentiability'),('I.rank0','T.bound','rank0 internal branch'),('H.space','I.rank0','authored finite-Hilbert extension'),('S.Ex7','T.bound','exact source pointwise coefficient/scope correspondence')]:edge(a,b,r)
uses=[('A.bounded-L2','I.domains','api-bounded-L2'),('A.memLp-two-sq','I.domains','api-memLp-two-sq'),('A.CLM-integral','I.evaluate','api-CLM-integral'),('A.covariance-algebra','I.evaluate','api-covariance-algebra'),('A.L2-inner','I.scalar-CS','api-L2-inner'),('A.Cauchy-Schwarz','I.scalar-CS','api-Cauchy-Schwarz'),('A.dual-norm-bound','I.dual-norm','api-dual-norm-bound'),('A.actual-fderiv','I.gradient','api-actual-fderiv'),('A.Riesz','I.gradient','api-Riesz'),('A.norm-map','I.gradient','api-norm-map'),('A.differentiable','T.bound','api-differentiable')]
for a,b,sid in uses:
 edge(a,b,'Exact primitive contract, planned mathematical use, no implementation call claim','planned-primitive-use');i=next(x for x in inputs if x['id']==sid);call(next(x['qualified_name'] for x in nodes if x['id']==a),b,sid,*i['selected_physical_ranges'][0],note='Span is provider contract, not nonexistent48 proof caller; planned target obligation is separately named.')
for a,b,r in [('A.norm_sub_rev','I.sameS','literal norm(u-y)=norm(y-u)'),('A.integral','D.variance','two real integrals in variance definition'),('A.Riesz','D.gradient','toDual'),('A.symm','D.gradient','isometric inverse'),('A.fderiv','D.gradient','actual total fderiv'),('A.withDensity','D.normalization','normalized density'),('A.ofReal','D.normalization','ENNReal density'),('A.exp','D.normalization','real exponential'),('A.integral','D.normalization','actual real partition'),('A.integral','D.T','actual kernel integral'),('A.map','D.J','Gaussian pushforward'),('A.prod','D.J','independent product'),('A.stdGaussian','D.J','literal varianceI Gaussian'),('A.tilted','D.mu','normalized Gibbs definition'),('A.tilted','D.S','normalized reflected density'),('A.fderiv','D.score','literal dual derivative'),('A.innerSL','D.score','literal parameter score pairing'),('D.variance','D.admissible','centered-square integrability'),('D.gradient','D.admissible','gradient-energy integrability')]:edge(a,b,r,'definition-reference')
# Exact selected-definition callers. Generated record fields/type constructors are not theorem calls.
for q,n,sid,a,b in [('MeasureTheory.integral','D.variance','def-variance',29,29),('InnerProductSpace.toDual','D.gradient','def-gradient',83,83),('LinearIsometryEquiv.symm','D.gradient','def-gradient',83,83),('fderiv','D.gradient','def-gradient',83,83),('MeasureTheory.Measure.withDensity','D.normalization','def-tilted',43,43),('ENNReal.ofReal','D.normalization','def-tilted',43,43),('Real.exp','D.normalization','def-tilted',43,43),('MeasureTheory.integral','D.normalization','def-tilted',43,43),('gradient','D.admissible','def-admissible',39,39),('MeasureTheory.Integrable','D.admissible','def-admissible',37,39)]:call(q,n,sid,a,b,'direct-selected-definition-reference','Real definition body, not generated structure field or compiled48 call')
# Exhaustive physical source partition. HTML presentation rows and out-of-scope clauses are explicit.
for sid,a,b in [('primary-global',348,363),('primary-augmentation',615,652),('primary-curvature',668,695),('primary-macro',3714,3735),('primary-C1',4566,4653)]:
 rows=(R/primary).read_bytes().splitlines()
 mapping={}
 def mark(x,y,n):
  for j in range(x,y+1):mapping[j]=n
 if sid=='primary-global':mark(351,352,'H.C2');mark(354,359,'H.lower')
 if sid=='primary-augmentation':mark(616,616,'H.eta');mark(617,624,'D.mu');mark(625,634,'D.J');mark(635,638,'D.J');mark(640,650,'D.R')
 if sid=='primary-curvature':mark(674,686,'D.R');mark(687,694,'S.unreflected-curvature')
 if sid=='primary-macro':mark(3714,3724,'S.pair');mark(3729,3735,'D.T')
 if sid=='primary-C1':
  for x,y,n in [(4574,4576,'H.observer'),(4577,4587,'D.S'),(4588,4594,'D.score'),(4595,4604,'S.derivative'),(4605,4614,'S.curvature'),(4615,4625,'S.PI'),(4626,4634,'S.score-gradient'),(4635,4643,'S.score-variance'),(4644,4645,'S.CS'),(4646,4652,'S.Ex7')]:mark(x,y,n)
 for line in range(a,b+1):
  text=rows[line-1].decode('utf-8');n=mapping.get(line)
  # Pure table/div wrappers and equation labels do not hide mathematical ingredients.
  math_or_text=bool(re.search(r'<math\b|<annotation|class="ltx_p"|class="ltx_text"|[A-Za-zαβη].*</a>.*[^<>]$',text))
  if n and math_or_text:
   sub=[]
   if line==4575:sub=['Tail: general case by density/closedness is a future rough-domain extension, not48.']
   if line==3732:sub=['B.9 second identity norm(U_perpP f)^2=E conditionalVar is downstream integrated theorem; only first T_f=U_PP identity contributes.']
   cov(sid,line,line,n,sub=sub)
  else:cov(sid,line,line,why='Out-of-scope theorem/heading/prose or HTML presentation/empty/label row; no mathematical dependency assigned.' if line not in [4653] else 'Beginning of integration in y toward formula(C.2), outside pointwise48.')
# Complete contract/definition coverage. Every selected physical row is classified exactly once.
for i in selected:
 sid=i['id']
 if sid.startswith('primary-'):continue
 for a,b in i['ranges']:
  for line in range(a,b+1):
   if sid=='target':n='T.bound'
   elif sid=='parent-score':n='P.score'
   elif sid=='parent-variance' and 31<=line<=37:n=None
   elif sid=='parent-variance':n='P.variance'
   elif sid=='def-variance':n='D.variance'
   elif sid=='def-admissible':n='D.admissible'
   elif sid=='def-gradient':n='D.gradient'
   elif sid=='def-tilted':n='D.normalization'
   else:n='A.'+sid[4:]
   cov(sid,line,line,n,why='Opaque parent additional original-closure/centered-domain outputs31-37 are unused by48; not extra hypotheses.' if n is None else None)
# Add needed references in selected public contract formulas, distinct from theorem calls.
for sid,n,spans in [('parent-score','P.score',[(43,45),(46,47),(49,52),(55,57)]),('parent-variance','P.variance',[(19,24),(26,30),(38,43)]),('target','T.bound',[(10,12),(14,17),(19,23)])]:
 for a,b in spans:
  rows=(R/next(x['path'] for x in inputs if x['id']==sid)).read_bytes().splitlines()
  text='\n'.join(x.decode('utf-8') for x in rows[a-1:b])
  refs=[('stdGaussian','ProbabilityTheory.stdGaussian'),('Measure.map','MeasureTheory.Measure.map'),('.map','MeasureTheory.Measure.map'),('.prod','MeasureTheory.Measure.prod'),('.tilted','MeasureTheory.Measure.tilted'),('fderiv','fderiv'),('innerSL','innerSL'),('gradient','gradient'),('Poincare.Admissible','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible'),('Poincare.variance','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance'),('∫','MeasureTheory.integral')]
  for token,q in refs:
   if token in text:call(q,n,sid,a,b,'public-contract-definition-reference','Named definition in selected public formula; proof bodies and generated fields are unexpanded.')
for row in coverage:
 if row['input_id']=='primary-global' and row['physical_line'] in [351,352] and row['classification']=='NODE':row['node_ids']=list(dict.fromkeys(row['node_ids']+['H.space','H.alpha','H.order','H.C2']))
 if row['input_id']=='primary-global' and row['physical_line']==358 and row['classification']=='NODE':row['node_ids']=list(dict.fromkeys(row['node_ids']+['H.lower','H.upper']))
 if row['input_id']=='primary-augmentation' and row['physical_line']==616 and row['classification']=='NODE':row['node_ids']=list(dict.fromkeys(row['node_ids']+['H.eta','H.cap']))
 if row['input_id']=='primary-C1' and row['physical_line']==4645 and row['classification']=='NODE':row['node_ids']=list(dict.fromkeys(row['node_ids']+['S.CS','S.sup']))
 if row['input_id']=='primary-C1' and row['physical_line']==4576:row['subclause_exclusions'].append('Source density/closedness continuation is excluded rough-domain theorem scope.')
keys=[(x['input_id'],x['physical_line']) for x in coverage];assert len(keys)==len(set(keys))
expected={(i['id'],j) for i in selected for a,b in i['ranges'] for j in range(a,b+1)};assert set(keys)==expected
ids={x['id'] for x in nodes};assert all(e['from_id'] in ids and e['to_id'] in ids for e in edges);assert all(c['caller_node'] in ids for c in callers)
graph=dict(schema_version=1,graph_id='PBPS48-independent-source-pointwise-gradient-variance',creator='gaussian_noncompact_preread_42',status='CREATED_AWAITING_DISTINCT_TOPOLOGY_REVIEW',statement_lf_bytes=1356,statement_lf_sha256=sha(lf((R/target).read_bytes())),primary_whole_raw_sha256=sha((R/primary).read_bytes()),nodes=nodes,edges=edges,source_expansion_boundary='Bounded printed C.1 through Ex7, essential standing2.7/2.8/B.8/B.9-first definitions; actual verified parents opaque, mathematical ingredients not conflated with parent status; no C.2 formula integration, subsection C.2 halfturn, rough-domain or fullpaper expansion.',implementation_used=False,compiled_edge_claims=False,source_topology_admitted=False)
write('source-proof-graph.json',graph);write('source-coverage.json',dict(schema_version=1,selected_inputs=selected,rows=coverage,total_rows=len(coverage),NODE=sum(x['classification']=='NODE' for x in coverage),EXCLUDED=sum(x['classification']=='EXCLUDED' for x in coverage),completeness='Every selected physical input row exactly once; same-row out-of-scope subclaims explicitly listed; no wholepaper coverage claim'))
write('caller-inventory.json',dict(schema_version=1,selected_provider_proof_bodies=0,records=callers,interpretation='Exact selected definition callers/public formula references, plus planned mathematical primitive uses. Provider contract spans are not fabricated48 implementation caller spans. Generated attributes/structure fields/typeclass/record projections are not mathematical theorem calls.'))
# Occurrence-complete selected Lean token inventory; remaining identifiers are local/type/record syntax.
tokens=[]
known=[('stdGaussian','ProbabilityTheory.stdGaussian'),('Measure.map','MeasureTheory.Measure.map'),('.map','MeasureTheory.Measure.map'),('.prod','MeasureTheory.Measure.prod'),('.tilted','MeasureTheory.Measure.tilted'),('withDensity','MeasureTheory.Measure.withDensity'),('ENNReal.ofReal','ENNReal.ofReal'),('exp','Real.exp'),('toDual','InnerProductSpace.toDual'),('symm','LinearIsometryEquiv.symm'),('fderiv','fderiv'),('gradient','gradient'),('innerSL','innerSL'),('Poincare.Admissible','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.Admissible'),('Poincare.variance','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance'),('Integrable','MeasureTheory.Integrable'),('∫','MeasureTheory.integral')]
for i in selected:
 if i['kind']=='primary-proof-source':continue
 raw=(R/i['path']).read_bytes();rows=raw.splitlines(keepends=True)
 for a,b in i['ranges']:
  for line in range(a,b+1):
   text=rows[line-1].decode('utf-8');text=text[:i['stop_column']-1] if i['stop_column'] and line==b else text
   for token,q in known:
    for m in re.finditer(re.escape(token),text):
     if token in ['gradient','exp','fderiv','toDual','symm','Integrable'] and ((m.start()>0 and (text[m.start()-1].isalnum() or text[m.start()-1]=='_')) or (m.end()<len(text) and (text[m.end()].isalnum() or text[m.end()]=='_'))):continue
     tokens.append(dict(input_id=i['id'],physical_line=line,column_start=m.start()+1,column_end_exclusive=m.end()+1,token=token,qualified_name=q,classification='selected-defined-name-occurrence',compiled_call_claim=False))
write('selected-token-inventory.json',dict(schema_version=1,records=tokens,scope='Every occurrence of the explicitly enumerated mathematical definition vocabulary across all selected Lean contracts/definition bodies. Other typeclasses, declarations, local variables and generated structure fields are not theorem calls. No provider proof body selected.',vocabulary=known))
write('input-bindings.json',dict(schema_version=1,inputs=inputs,prior47_history='Separate immutable source-before-target contract/pins; not current implementation evidence'))
print(json.dumps(dict(nodes=len(nodes),edges=len(edges),coverage_rows=len(coverage),NODE=sum(x['classification']=='NODE' for x in coverage),EXCLUDED=sum(x['classification']=='EXCLUDED' for x in coverage),caller_records=len(callers),inputs=len(inputs),status='AUTHORED_NOT_TOPOLOGY_ADMITTED')))
