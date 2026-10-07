# coding:utf-8
import pathlib,json,hashlib,re,sys,datetime,copy
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority'; O=B/'pbps-gaussian-reflected-mean-sourcegraph52'; H=B/'pbps-literal-mean-c1-preread52'; M=R/'.lake/packages/mathlib/Mathlib'
def h(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n')
def jr(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def jw(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert jr(O/'lease.json')['status']=='OPEN'
nodes=[]; edges=[]; providers=[]; rows=[]; calls=[]; lexical=[]; formulas=[]; inputs={}; registry={}
def pin(p):
 b=p.read_bytes(); d=dict(path=str(p),bytes=len(b),raw_sha256=h(b),lf_sha256=h(lf(b)));inputs[str(p)]=d;return b
def node(i,k,c,q=None):
 if not any(x['id']==i for x in nodes):nodes.append(dict(id=i,kind=k,contract=c,qualified_id=q,compiled52=False,proof_body_expanded=False))
def edge(a,b,k,reason,span=None,caller=None):
 d=dict(id='E52.'+str(len(edges)),ingredient=a,consumer=b,kind=k,reason=reason,compiled52call=False)
 if span:d['source_span']=span
 if caller is not None:d['caller_index0']=caller
 edges.append(d)
def select(i,n,p,a,z,k='public-header',stripproof=False):
 b=pin(p);ls=b.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));frag=b''.join(ls[a-1:z])
 if stripproof:
  # The bounded range ends at declaration proof assignment; earlier := may be literal let binders.
  pos=frag.rfind(b':=');frag=frag[:pos] if pos>=0 else frag
 end=start+len(frag)
 provider=dict(id=i,node=n,path=str(p),kind=k,whole_raw_sha256=h(b),whole_lf_sha256=h(lf(b)),physical_lines1=[a,z],start_utf8_byte0=start,end_utf8_byte0_exclusive=end,fragment_raw_sha256=h(frag),fragment_lf_sha256=h(lf(frag)),body_selected=k=='definition-body',external_expansion_boundary=k=='primitive-anchor')
 providers.append(provider);(O/(i+'.raw')).write_bytes(frag);(O/(i+'.lf')).write_bytes(lf(frag))
 off=start
 for j,line in enumerate(frag.splitlines(keepends=True),a):
  s=line.decode('utf-8');text=s.strip();semantic=True
  if k=='primary-source':semantic=bool(re.search(r'<p |<math |<td.*<math|closedness of|which proves|B\.13.*It suffices|given ',s))
  else:semantic=bool(text) and not text.startswith(('--','/-','*/'))
  rows.append(dict(provider=i,path=str(p),physical_line1=j,start_utf8_byte0=off,end_utf8_byte0_exclusive=off+len(line),classification='NODE' if semantic else 'EXCLUDED',node=n if semantic else None,reason='Actual selected mathematical declaration/formula/text; body outside selection remains unexpanded' if semantic else 'Selected layout/blank/comment only; no mathematical ingredient',raw_line_sha256=h(line),partial_physical_line=not line.endswith(b'\n')))
  off+=len(line)
 return provider,frag
def anchor(i,q,p,ln,token,contract):
 b=pin(p);ls=b.splitlines(keepends=True);base=sum(map(len,ls[:ln-1]));line=ls[ln-1];pos=line.decode().index(token);start=base+len(line.decode()[:pos].encode());frag=token.encode()
 node(i,'external-unexpanded-primitive',contract,q)
 provider=dict(id=i,node=i,path=str(p),kind='primitive-declaration-token-anchor',physical_lines1=[ln,ln],start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(frag),whole_raw_sha256=h(b),whole_lf_sha256=h(lf(b)),fragment_raw_sha256=h(frag),fragment_lf_sha256=h(lf(frag)),body_selected=False,external_expansion_boundary=True,selection_boundary='Exact declaration-name token only; remaining actual declaration signature/body is unexpanded. No full-header/body coverage asserted.')
 providers.append(provider);(O/(i+'.raw')).write_bytes(frag);(O/(i+'.lf')).write_bytes(frag)
 rows.append(dict(provider=i,path=str(p),physical_line1=ln,start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(frag),classification='NODE',node=i,reason='Actual declaration token anchor; rest of header/body external-unexpanded',raw_line_sha256=h(frag),partial_physical_line=True))
 lexical.append(dict(provider=i,caller_node=i,path=str(p),physical_line1=ln,start_utf8_byte0=start,end_utf8_byte0_exclusive=start+len(frag),token=token,classification='own-declaration-label-not-call',resolved_node=None))
def api(i,q,path,a,z,c):
 node(i,'opaque-public-library-contract',c,q);return select(i,i,path,a,z,stripproof=True)
primary=B/'next-ready-preread47/primary-pbps.raw.snapshot.html'
for i,n,a,z,c in [('primary-compact','S52.compact',4573,4576,'Source signed smooth compact test reduction and omitted density/closedness toward B13'),('primary-density','S52.density',4579,4587,'Source every-y normalized reflected conditional Gibbs density; proportional exp(-V((y+u)/2)-norm(y-u)^2/(8eta))'),('primary-score','S52.score',4588,4595,'Source directional parameter score; requires source V C2 and genuine normalized law'),('primary-covariance','S52.covariance',4596,4604,'Source differentiating normalized conditional density gives covariance; does not print derivative continuity'),('primary-energy','S52.energy',4654,4664,'Exact formula(C.2) insideC.1; downstream sharp eta energy coefficient and norm defect'),('primary-B13','S52.B13',3779,3786,'Full rough L2 B13 consumer, not current52 conclusion')]:
 node(n,'primary-source',c);p,f=select(i,n,primary,a,z,'primary-source')
 for match in re.finditer(r'alttext="([^"]*)"',f.decode()):
  tex=match.group(1); st=p['start_utf8_byte0']+len(f.decode()[:match.start(1)].encode());formulas.append(dict(provider=i,node=n,start_utf8_byte0=st,end_utf8_byte0_exclusive=st+len(tex.encode()),tex=tex,kind='exact-source-alttext',source_statement_not52=True))
 for match in re.finditer(r'href="#(A2\.E13)"',f.decode()):
  token=match.group(1);st=p['start_utf8_byte0']+len(f.decode()[:match.start(1)].encode());ci=len(calls);calls.append(dict(index0=ci,provider=i,caller_node=n,path=str(primary),physical_line1=a+f[:st-p['start_utf8_byte0']].count(b'\n'),start_utf8_byte0=st,end_utf8_byte0_exclusive=st+len(token),token=token,resolved_node='S52.B13',qualified_id=None,classification='source-internal-reference',compiled52call=False));edge('S52.B13',n,'source-reference','Exact href to source rough theorem, retained residual boundary',caller=ci)
candidate=B/'pbps-gaussian-reflected-mean-preproof52/prospective-statement.txt'
node('T52','sealed-prospective-target','Actual literal reflected Gaussian posterior mean C1, every y; no proof or claim','AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1')
select('candidate','T52',candidate,1,8)
parent=R/'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean'
api('A52.C2','AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2',parent,255,262,'Real probability input eta>0 gives literal Gaussian Z C2 and C Z>0; actual output law/negative-logC2 included but source EXCESS for52; opaque verified parent, no body selected')
select('C2-context','A52.C2',parent,33,33);select('C2-context-borel','A52.C2',parent,144,144)
api('P52.diff','MeasureTheory.hasFDerivAt_integral_of_dominated_of_fderiv_le',M/'Analysis/Calculus/ParametricIntegral.lean',210,216,'Actual local derivative dominance, AES meas, real F x0 L1, F prime x0 AES, integrable bound and actual AE all-neighborhood derivatives imply derivative of integral')
select('diff-context','P52.diff',M/'Analysis/Calculus/ParametricIntegral.lean',67,71)
api('P52.cont','MeasureTheory.continuous_of_dominated',M/'MeasureTheory/Integral/Bochner/Basic.lean',444,447,'All parameters AES measurable integrands and uniform AE integrable norm bound plus AE parameter continuity yield continuous Bochner integral')
select('continuous-context','P52.cont',M/'MeasureTheory/Integral/Bochner/Basic.lean',415,415)
select('Bochner-context','P52.cont',M/'MeasureTheory/Integral/Bochner/Basic.lean',152,152)
api('P52.C1','contDiff_one_iff_hasFDerivAt',M/'Analysis/Calculus/ContDiff/Defs.lean',1179,1180,'C1 iff exists continuous actual Frechet derivative field')
select('ContDiff-context','P52.C1',M/'Analysis/Calculus/ContDiff/Defs.lean',108,109)
api('P52.fderivCont','ContDiff.continuous_fderiv',M/'Analysis/Calculus/ContDiff/Defs.lean',1272,1273,'C1 implies continuous fderiv, n nonzero')
api('P52.quotient','ContDiff.div',M/'Analysis/Calculus/ContDiff/Operations.lean',834,835,'C1 numerator and denominator and pointwise nonzero denominator imply C1 quotient')
api('P52.compactDeriv','HasCompactSupport.fderiv',M/'Analysis/Calculus/FDeriv/Const.lean',388,389,'Actual compact support of f implies compact support of fderiv; derivative continuity still required separately')
api('P52.compactBound','Continuous.bounded_above_of_compact_support',M/'Analysis/Normed/Group/Bounded.lean',158,159,'Continuous compact observer or derivative gives actual global norm bound')
api('P52.tiltIntegral','MeasureTheory.integral_tilted',M/'MeasureTheory/Measure/Tilted.lean',230,231,'Literal normalized exp-weight Bochner integral identity; mathematical integrability and denominator positivity produced internally even though formula is total')
api('P52.mapIntegral','MeasureTheory.integral_map_of_stronglyMeasurable',M/'MeasureTheory/Integral/Bochner/Basic.lean',1032,1033,'True measurable reflection map and StronglyMeasurable f give actual map integral formula; no bijection certificate premise')
api('P52.smulIntegral','MeasureTheory.integral_smul',M/'MeasureTheory/Integral/Bochner/Basic.lean',275,276,'Scalar factor moves out of Bochner integral, actual Module/NormSMul/SMulComm typing required')
api('P52.constL1','MeasureTheory.integrable_const',M/'MeasureTheory/Function/L1Space/Integrable.lean',163,163,'Finite measure implies genuine constant bound integrable; probability input internally supplies finite measure')
api('P52.innerNorm','innerSL_apply_norm',M/'Analysis/InnerProductSpace/LinearMap.lean',228,228,'Norm of actual inner product functional equals norm of vector, including rankzero; not the Nontrivial-only norm of whole innerSL operator')
api('P52.normSq','HasFDerivAt.norm_sq',M/'Analysis/InnerProductSpace/Calculus.lean',211,212,'True derivative norm-square uses innerSL composition, without rank positivity')
api('P52.expDeriv','HasFDerivAt.exp',M/'Analysis/SpecialFunctions/ExpDeriv.lean',353,354,'True derivative exponential of scalar map')
api('P52.chain','HasFDerivAt.comp',M/'Analysis/Calculus/FDeriv/Comp.lean',105,106,'Actual Frechet chain rule through actual CLM composition')
api('P52.product','HasFDerivAt.mul',M/'Analysis/Calculus/FDeriv/Mul.lean',205,206,'Actual derivative product of real scalar functions')
api('P52.expBound','Real.mul_exp_neg_le_exp_neg_one',M/'Analysis/SpecialFunctions/Exp.lean',215,215,'Actual t exp(-t) bound supports internal global Gaussian derivative norm bound')
for i,q,path,a,z,c in [('D52.tilt','MeasureTheory.Measure.tilted','MeasureTheory/Measure/Tilted.lean',42,43,'Actual normalized exp tilt withDensity, not arbitrary conditional kernel')]:
 node(i,'actual-definition',c,q);select(i,i,M/path,a,z,'definition-body')
# All named/notation primitive nodes have literal declaration anchors. Their signatures/bodies are external-unexpanded, not selected proofs.
old=B/'pbps-gaussian-marginal-gradient-sourcegraph51';oldproviders=jr(old/'selected-providers.json');oldnodes={x['id']:x for x in jr(old/'source-proof-graph.json')['nodes']}
reuse={'D51.NAC':'NormedAddCommGroup','D51.IP':'InnerProductSpace','D51.FD':'FiniteDimensional','D51.MS':'MeasurableSpace','D51.Borel':'BorelSpace','D51.Measure':'Measure','D51.prob':'IsProbabilityMeasure','D51.CD':'ContDiff','D51.AEStrong':'AEStronglyMeasurable','D51.Integrable':'Integrable','P51.stdG':'stdGaussian','P51.map':'map','P51.prod':'prod','P51.wd':'withDensity','P51.ofReal':'ofReal','D51.volume':'volume','D51.integral':'integral'}
for oldid,tok in reuse.items():
 pr=next(x for x in oldproviders if x['id']==oldid);p=pathlib.Path(pr['path']);ln=pr['physical_lines1'][0]
 if oldid=='D51.volume':ln=356
 new='D52.'+oldid.split('.')[1];q=oldnodes[oldid]['qualified_id'];anchor(new,q,p,ln,tok,oldnodes[oldid]['contract']+' External-unexpanded primitive identity, not proof credit.');registry[tok]=(new,q)
for i,q,path,ln,tok,c in [
 ('Real','Real','Data/Real/Basic.lean',36,'Real','Actual real scalar type'),('Norm','Norm.norm','Analysis/Normed/Group/Defs.lean',62,'norm','Actual Norm.norm field projection; surrounding class/body external-unexpanded'),('Module','Module','Algebra/Module/Defs.lean',54,'Module','Actual global scalar-module class, not Module.finrank'),('NormedSpace','NormedSpace','Analysis/Normed/Module/Basic.lean',40,'NormedSpace','Compatible normed module scalar action'),('RCLike','RCLike','Analysis/RCLike/Basic.lean',60,'RCLike','Real/complex scalar background for parametric differentiation'),('Continuous','Continuous','Topology/Defs/Basic.lean',155,'Continuous','Actual topological continuous function structure'),('HasFDerivAt','HasFDerivAt','Analysis/Calculus/FDeriv/Defs.lean',121,'HasFDerivAt','Actual Frechet derivative via continuous linear map'),('fderiv','fderiv','Analysis/Calculus/FDeriv/Defs.lean',158,'fderiv','Actual total Frechet derivative, supplies true derivative where differentiable'),('CLM','ContinuousLinearMap','Topology/Algebra/Module/ContinuousLinearMap/Basic.lean',61,'ContinuousLinearMap','Actual continuous linear map, not abstract derivative certificate'),('finrank','Module.finrank','LinearAlgebra/Dimension/Finrank.lean',62,'finrank','Actual finite module rank in Gaussian prefactor'),('sqrt','Real.sqrt','Analysis/Real/Sqrt.lean',112,'sqrt','Actual nonnegative real square root'),('pi','Real.pi','Analysis/SpecialFunctions/Trigonometric/Basic.lean',127,'pi','Actual real pi'),('exp','Real.exp','Analysis/Complex/Exponential.lean',80,'exp','Actual real exponential'),('log','Real.log','Analysis/SpecialFunctions/Log/Basic.lean',44,'log','Actual real logarithm; parent surplus negative-log output'),('nhds','nhds','Topology/Defs/Filter.lean',130,'nhds','True parameter neighborhood filter'),('Eventually','Filter.Eventually','Order/Filter/Defs.lean',281,'Eventually','Actual filter eventual proposition for AE/eventual-neighborhood API clauses'),('ae','MeasureTheory.ae','MeasureTheory/OuterMeasure/AE.lean',49,'ae','Actual measure almost-everywhere filter'),('TopologicalSpace','TopologicalSpace','Topology/Defs/Basic.lean',73,'TopologicalSpace','Actual topology class'),('FirstCountable','FirstCountableTopology','Topology/Bases.lean',695,'_root_.FirstCountableTopology','Actual first-countability required by integral continuity; finite Hilbert is metrizable'),('NormSMul','NormSMulClass','Analysis/Normed/MulAction.lean',95,'NormSMulClass','Norm-scalar compatibility in integral scalar extraction'),('SMulComm','SMulCommClass','Algebra/Group/Action/Defs.lean',148,'SMulCommClass','Real/scalar action commutation'),('FiniteMeasure','MeasureTheory.IsFiniteMeasure','MeasureTheory/Measure/Typeclasses/Finite.lean',35,'IsFiniteMeasure','True finite measure required by bound integrability')]:
  new='D52.'+i;anchor(new,q,M/path,ln,tok,c);registry[q]=(new,q);registry[q.split('.')[-1]]=(new,q)
for i,q,path,ln,tok,c in [('NontrivialNormed','NontriviallyNormedField','Analysis/Normed/Field/Basic.lean',166,'NontriviallyNormedField','Actual nontrivial scalar norm for C1 Frechet characterization; real scalar supplies instance'),('Measurable','Measurable','MeasureTheory/MeasurableSpace/Defs.lean',493,'Measurable','Actual measurable reflection, derived from continuous affine map'),('Strong','MeasureTheory.StronglyMeasurable','MeasureTheory/Function/StronglyMeasurable/Basic.lean',64,'StronglyMeasurable','Actual strongly measurable observer, derived from C1 continuity and finite dimensional second countability'),('innerSL','innerSL','Analysis/InnerProductSpace/LinearMap.lean',167,'innerSL','Actual real inner-product continuous linear functional used in Gaussian derivative'),('CLMcomp','ContinuousLinearMap.comp','Topology/Algebra/Module/ContinuousLinearMap/Basic.lean',460,'comp','Actual CLM composition; not HasFDerivAt.comp theorem or selfwrapper')]:
 new='D52.'+i;anchor(new,q,M/path,ln,tok,c);registry[q]=(new,q);registry[q.split('.')[-1]]=(new,q)
anchor('D52.compact','HasCompactSupport',M/'Topology/Algebra/Support.lean',216,'HasCompactMulSupport','HasCompactSupport is actual additive declaration generated by adjacent to_additive attribute from this source; generated identity not a theorem call.')
registry['HasCompactSupport']=('D52.compact','HasCompactSupport')
anchor('P52.ofle','ContDiff.of_le',M/'Analysis/Calculus/ContDiff/Defs.lean',1141,'ContDiff.of_le','Actual lowering derivative order; C2Z -> C1Z')
anchor('P52.continuous','ContDiff.continuous',M/'Analysis/Calculus/ContDiff/Defs.lean',1151,'ContDiff.continuous','Actual C1 observer -> continuous observer')
anchor('D52.SMul','HSMul.hSMul',pathlib.Path('C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Prelude.lean'),1437,'hSMul','Actual fixedLean4.33.0 scalar multiplication field; concrete real module action supplied by InnerProductSpace/NormedSpace typing, core body unexpanded')
anchor('D52.Set','Set',M/'Data/Set/Defs.lean',51,'Set','Actual Set H definition is predicate H -> Prop; set-membership syntax remains external-unexpanded')
registry.update({'ℝ':('D52.Real','Real'),'→L':('D52.CLM','ContinuousLinearMap'),'∫':('D52.integral','MeasureTheory.integral'),'𝓝':('D52.nhds','nhds'),'∀ᶠ':('D52.Eventually','Filter.Eventually'),'∀ᵐ':('D52.Eventually','Filter.Eventually'),'‖':('D52.Norm','Norm.norm'),'•':('D52.SMul','HSMul.hSMul'),'Set':('D52.Set','Set'),'μ.tilted':('D52.tilt','MeasureTheory.Measure.tilted'),'tilted':('D52.tilt','MeasureTheory.Measure.tilted'),'ENNReal.ofReal':('D52.ofReal','ENNReal.ofReal'),'Module.finrank':('D52.finrank','Module.finrank'),'μ.prod':('D52.prod','MeasureTheory.Measure.prod'),'μ.withDensity':('D52.wd','MeasureTheory.Measure.withDensity'),'Measure.map':('D52.map','MeasureTheory.Measure.map'),"g'.comp":('D52.CLMcomp','ContinuousLinearMap.comp')})
# Scanner covers every Unicode identifier and selected analytic notation in selected Lean fragments; declaration anchors handled explicitly above.
pat=re.compile(r'∀ᶠ|∀ᵐ|→L|[∫𝓝ℝ‖•]|[^\W\d][\w\u2080-\u209f\u1d62-\u1d6a]*(?:[\'′]*)(?:\.[^\W\d][\w\u2080-\u209f\u1d62-\u1d6a]*[\'′]*)*',re.UNICODE)
lang=set('theorem lemma protected def irreducible_def variable let fun Type Prop in where by noncomputable ℕ u uE uF uG uX'.split())
unknown=[]
for pr in providers:
 if pr['kind'] in ['primary-source','primitive-declaration-token-anchor']:continue
 frag=(O/(pr['id']+'.raw')).read_bytes();text=frag.decode();own=next((x['qualified_id'] for x in nodes if x['id']==pr['node']),None)
 decls=set(re.findall(r'(?:theorem|lemma|def)\s+([\w.]+)',text))
 for mt in pat.finditer(text):
  tok=mt.group();start=pr['start_utf8_byte0']+len(text[:mt.start()].encode());end=start+len(tok.encode());line=pr['physical_lines1'][0]+text[:mt.start()].count('\n');base=dict(provider=pr['id'],caller_node=pr['node'],path=pr['path'],physical_line1=line,start_utf8_byte0=start,end_utf8_byte0_exclusive=end,token=tok)
  if tok in decls:classification='own-declaration-label-not-call';resolved=None
  elif tok in registry:
   resolved,q=registry[tok];classification='definition-or-typing-reference';ci=len(calls);c=dict(base,index0=ci,caller_index0=ci,resolved_node=resolved,qualified_id=q,classification=classification,compiled52call=False,provider_body_selected=pr['body_selected']);calls.append(c);edge(resolved,pr['node'],'definition-or-typing-reference','Exact selected global token; primitive/class fields not implementation wrapper',caller=ci);base['caller_index0']=ci
   if tok=='∀ᵐ':
    ci=len(calls);calls.append(dict(base,index0=ci,caller_index0=ci,resolved_node='D52.ae',qualified_id='MeasureTheory.ae',classification='notation-subexpression-reference',compiled52call=False));edge('D52.ae',pr['node'],'notation-subexpression-reference','AE notation uses actual measure filter as well as Eventually',caller=ci)
  else:
   resolved=None;classification='binder-local-or-language-symbol'
   if tok not in lang and (tok[0].isupper() or '.' in tok) and tok not in ['E','F','G','H','X','F′','F\'','R','S','C','Z','Fintype'] and not re.match(r'^(?:p|R|F|μ)\.',tok):unknown.append(dict(base,reason='needs explicit scope/primitive classification'))
  lexical.append(dict(base,classification=classification,resolved_node=resolved))
jw('unresolved-scope-checks.json',unknown)
jw('selected-providers.json',providers);jw('source-coverage.json',dict(scope='Exhaustive physical selected-fragment rows including partial declaration anchors; no whole-library claim',rows=rows));jw('caller-inventory.json',dict(scope='Every selected named global reference, source href and listed analytic notation; binder locals/declaration labels not calls',entries=calls));jw('lexical-inventory.json',dict(scope='Every identifier token and listed analytic notation within selected Lean fragments; source HTML formula/href inventory separate. Punctuation/operator desugaring and external primitive bodies unexpanded.',entries=lexical,requires_classification=unknown));jw('primary-formula-inventory.json',formulas)
jw('source-proof-graph.partial.json',dict(schema_version='source52-v1',status='AUTHORING_SOURCE_ONLY_NOT_ADMITTED',edge_orientation='ingredient -> consumer',nodes=nodes,edges=edges));jw('input-bindings.partial.json',dict(files=list(inputs.values())))
print(json.dumps(dict(nodes=len(nodes),providers=len(providers),rows=len(rows),callers=len(calls),lexemes=len(lexical),unresolved=unknown),ensure_ascii=False,indent=2))
