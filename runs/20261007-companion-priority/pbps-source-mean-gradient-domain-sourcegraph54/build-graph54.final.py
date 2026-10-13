from pathlib import Path
import json,re,hashlib,datetime,sys
sys.stdout.reconfigure(encoding="utf-8")
R=Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority'; O=B/'pbps-source-mean-gradient-domain-sourcegraph54'; M=R/'.lake/packages/mathlib/Mathlib'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def J(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
N=[]; E=[]; P=[]; node={}; texts={}
def n(id,kind,contract,q=None,**kw):
 if id not in node:
  x=dict(id=id,kind=kind,contract=contract,qualified_id=q,compiled54=False,proof_body_expanded=False,**kw);N.append(x);node[id]=x
 return id
def e(a,b,kind,reason,caller=None):
 x=dict(id='E54.'+str(len(E)),ingredient=a,consumer=b,kind=kind,reason=reason,compiled54call=False)
 if caller is not None:x['caller_index0']=caller
 E.append(x)
def span(id,nid,path,a,z,kind='public-header',end=None):
 path=Path(path);raw=path.read_bytes();ls=raw.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));end=end if end is not None else sum(map(len,ls[:z]));b=raw[start:end]
 (O/(id+'.raw.snapshot')).write_bytes(b);(O/(id+'.lf.snapshot')).write_bytes(LF(b));x=dict(id=id,node=nid,kind=kind,path=str(path),physical_lines1=[a,z],start_utf8_byte0=start,end_utf8_byte0_exclusive=end,fragment_raw_sha256=H(b),fragment_lf_sha256=H(LF(b)),whole_raw_sha256=H(raw),whole_lf_sha256=H(LF(raw)),body_selected=False,external_expansion_boundary=kind.startswith('external'),header_complete=not kind.startswith('context'))
 P.append(x);texts[id]=b.decode('utf-8');return x
# Exact ordinary declaration boundaries; := in let/priority/default parameter is not the final declaration assignment.
def header_end(raw,a,default_z):
 ls=raw.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));pos=start;depth=0
 if not re.match(r'\s*(?:protected\s+|noncomputable\s+|irreducible_def\s+|abbrev\s+)*(?:theorem|lemma|def|class|structure|instance|abbrev|irreducible_def)\b',ls[a-1].decode('utf-8')):return sum(map(len,ls[:default_z])),default_z
 for i in range(a-1,len(ls)):
  t=ls[i].decode('utf-8');linebase=pos
  for k,ch in enumerate(t):
   if ch in '([{':depth+=1
   if ch in ')]}':depth-=1
   if t[k:k+2]==':=' and depth==0 and not t.strip().startswith('let '):return linebase+len(t[:k].encode('utf-8')),i+1
   if t[k:k+5]=='where' and depth==0:return linebase+len(t[:k+5].encode('utf-8')),i+1
  pos+=len(ls[i])
  if i+1>=default_z and t.strip() and (t.strip().startswith('class ') or t.strip().startswith('structure ')):pass
 return sum(map(len,ls[:default_z])),default_z
# Literal primary coverage: all requested bounded fragments, including excluded old50 ingredients/rough consumer.
primary=B/'next-ready-preread47/primary-pbps.raw.snapshot.html'
source=[('standing','S54.standing',351,361,'Source V C2,0<alpha<=beta, two actual Hessian bounds'),('augmentation','S54.laws',614,640,'Source eta cap, actual mu/J/nu Gaussian smoothing'),('rough-consumer','X54.rough',3777,3786,'Real B13 all-L2/H1/Gamma residual; NOT54 conclusion'),('compact-branch','S54.compact',4573,4665,'Source C1 compact test density/score/true derivative and C2 compact energy; larger old50 proof substeps remain inherited source context')]
for label,nid,a,z,c in source:n(nid,'primary-source' if not nid.startswith('X') else 'typed-residual',c);span('primary-'+label,nid,primary,a,z,'primary-source')
for id,c in [('S54.density','Actual every-y normalized source reflected density'),('S54.score','Actual score source definition'),('S54.covariance','True gradient normalized conditional mean source C1'),('S54.energy','Sharp integrated actual gradient energy on SAME outer nu from prior50 compact branch'),('X54.old50','Conditional Hessian/Poincare/Jacobian/CS proof subgraph already underlying50; outside new54 expansion'),('X54.Gamma','Actual source Gamma/root and fullrough norm/coercivity residual outside54'),('A54.core','Authored compact-gradient closure realization on actual nu; uniform G, not50 blockD'),('A54.pointwise','Literal whole source mean function equality; AE kernel equality does not transfer derivatives'),('A54.C1','Actual literal Tf is C1'),('A54.L2','Actual Tf/true gradient both MemLp on SAME nu'),('A54.prob','Actual mu/J/nu probability -> finite nu inside target'),('A54.domain','Canonical toLp pair in actual uniform G.closure.graph'),('A54.extension','Finite real Hilbert/Borel inclrank0; finite position never finiteL2'),('X54.omitted','Source omitted C1 continuity/closure realization details filled by genuine admitted background parents, not extra paper premises')]:n(id,'authored-adapter' if id.startswith('A') else 'source-definition' if id.startswith('S') else 'typed-residual',c)
pre=B/'pbps-source-mean-gradient-domain-preproof54';candidate=(pre/'prospective-statement.txt').read_bytes();assert H(LF(candidate))=='19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'
n('T54','prospective-target','Uniform true dense closable core and canonical literal compact-mean graph pair; statement admission pending', 'AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain.literal_source_mean_in_closed_gradient');span('prospective','T54',pre/'prospective-statement.txt',1,len(candidate.splitlines()))
# Four opaque ASTIS producers (full selected actual public headers plus all inherited contexts).
old=json.loads((B/'pbps-source-mean-gradient-domain-preread54/API-bindings.json').read_text(encoding='utf-8'))
parents={'parent50':'P54.p50','parent51':'P54.p51','parent53':'P54.p53','c1-adapter':'P54.C1'}
for x in old:
 if x['label'] in parents:
  id=parents[x['label']];n(id,'opaque-admitted-parent',x['label']+' actual public production contract; proof/source expansion inherited, no implementation-based54 topology',x['qualified_id']);raw=Path(x['path']).read_bytes();end,z=header_end(raw,x['physical_lines1'][0],x['physical_lines1'][1]);span(x['label']+'-public',id,x['path'],x['physical_lines1'][0],z,'opaque-public-header',end)
for label,line in [('adapter-context',11),('adapter-hilbert-context',95)]:span(label,'P54.C1',R/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',line,line,'context-public')
# Reuse only exact primitive header anchors from independently repaired53 source-only graph, not its production proof/verdict.
oldg=json.loads((B/'pbps-reflected-density-topology-overlay53/source-proof-graph.json').read_text(encoding='utf-8'));oldn={x['id']:x for x in oldg['nodes']};oldp=json.loads((B/'pbps-reflected-density-topology-overlay53/selected-providers.json').read_text(encoding='utf-8'))
keep={'NAC','IP','FD','MS','Borel','Measure','prob','CD','Integrable','stdG','map','prod','volume','integral','Real','Norm','Module','fderiv','sqrt','compact','SMul','Set','AEStrong','Measurable','FiniteMeasure','CLM','Strong','Continuous','TopologicalSpace','wd','ofReal'}
for x in oldp:
 if x['node'].startswith('D53.') and x['node'].split('.')[-1] in keep:
  tail=x['node'].split('.')[-1];id='D54.'+tail;q=oldn[x['node']]['qualified_id'];n(id,'external-unexpanded-primitive','Actual pinned public primitive '+q+'; implementation unexpanded',q);raw=Path(x['path']).read_bytes();a,z=x['physical_lines1'];end,z=header_end(raw,a,z);span('primitive-'+tail,id,x['path'],a,z,'external-public-header',end)
# Actual definitions/public APIs on the new compact closure path. Definitions read semantically; their implementations are explicitly external-unexpanded here.
selected=[('tilt','MeasureTheory.Measure.tilted','MeasureTheory/Measure/Tilted.lean',42,43),('MemLp','MeasureTheory.MemLp','MeasureTheory/Function/LpSeminorm/Defs.lean',118,119),('eLpNorm','MeasureTheory.eLpNorm','MeasureTheory/Function/LpSeminorm/Defs.lean',85,86),('Lp','MeasureTheory.Lp','MeasureTheory/Function/LpSpace/Basic.lean',89,90),('toLp','MeasureTheory.MemLp.toLp','MeasureTheory/Function/LpSpace/Basic.lean',106,107),('gradient','gradient','Analysis/Calculus/Gradient/Basic.lean',82,83),('LPM','LinearPMap','LinearAlgebra/LinearPMap.lean',41,42),('graph','LinearPMap.graph','LinearAlgebra/LinearPMap.lean',735,736),('closed','LinearPMap.IsClosed','Topology/Algebra/Module/LinearPMap.lean',63,64),('closable','LinearPMap.IsClosable','Topology/Algebra/Module/LinearPMap.lean',70,71),('closure','LinearPMap.closure','Topology/Algebra/Module/LinearPMap.lean',97,98),('Dense','Dense','Topology/Defs/Basic.lean',146,147),('IsClosed','IsClosed','Topology/Defs/Basic.lean',107,107),('Complete','CompleteSpace','Topology/UniformSpace/Cauchy.lean',370,370),('NNReal','NNReal','Data/NNReal/Defs.lean',58,58),('Kernel','ProbabilityTheory.Kernel','Probability/Kernel/Defs.lean',55,55),('Markov','ProbabilityTheory.IsMarkovKernel','Probability/Kernel/Defs.lean',146,146),('CondKernel','MeasureTheory.Measure.IsCondKernel','Probability/Kernel/Disintegration/Basic.lean',58,58),('LI','LinearIsometry','Analysis/Normed/Operator/LinearIsometry.lean',51,52),('SelfAdjoint','IsSelfAdjoint','Algebra/Star/SelfAdjoint.lean',50,50),('lpMeas','MeasureTheory.lpMeas','MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',88,89),('condExp','MeasureTheory.condExpL2','MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',68,70),('snd','MeasureTheory.Measure.snd','MeasureTheory/Measure/Prod.lean',1148,1149),('of_le','ContDiff.of_le','Analysis/Calculus/ContDiff/Defs.lean',1141,1141),('toLpAE','MeasureTheory.MemLp.coeFn_toLp','MeasureTheory/Function/LpSpace/Basic.lean',111,111),('toLpCongr','MeasureTheory.MemLp.toLp_congr','MeasureTheory/Function/LpSpace/Basic.lean',115,116),('toLpEq','MeasureTheory.MemLp.toLp_eq_toLp_iff','MeasureTheory/Function/LpSpace/Basic.lean',120,121),('closureGraph','LinearPMap.IsClosable.graph_closure_eq_closure_graph','Topology/Algebra/Module/LinearPMap.lean',107,108),('domainGraph','LinearPMap.mem_domain_of_mem_graph','LinearAlgebra/LinearPMap.lean',833,834)]
for label,q,path,a,z in selected:
 id=('D54.' if label not in ['of_le','toLpAE','toLpCongr','toLpEq','closureGraph','domainGraph'] else 'P54.')+label;n(id,'external-unexpanded-primitive',q+' actual public contract/definition; selected definition meaning read, implementation unexpanded',q);raw=(M/path).read_bytes();end,z=header_end(raw,a,z);span('api-'+label,id,M/path,a,z,'external-public-header',end)
# Contexts are true inherited public variable scopes, no proof snippets masquerading as typing.
for label,nid,path,a,z in [('gradient-context','D54.gradient','Analysis/Calculus/Gradient/Basic.lean',51,53),('lp-context','D54.toLp','MeasureTheory/Function/LpSpace/Basic.lean',67,68),('closable-context','D54.closable','Topology/Algebra/Module/LinearPMap.lean',51,54),('graph-context','D54.graph','LinearAlgebra/LinearPMap.lean',53,55)]:span(label,nid,M/path,a,z,'context-public')
# Additional finite/probability instance and direct variance definition in50 header, all remain primitive/opaque.
for label,q,path,a,z in [('probFinite','MeasureTheory.IsZeroOrProbabilityMeasure.toIsFiniteMeasure','MeasureTheory/Measure/Typeclasses/Probability.lean',52,53),('variance','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance',str(R/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean'),28,29)]:
 id='D54.'+label;n(id,'external-unexpanded-primitive',q+' header-only expansion boundary; exact spelling subject to primitive inventory check',q);path=Path(path) if path.startswith('E:') else M/path;raw=path.read_bytes();end,z=header_end(raw,a,z);span('api-'+label,id,path,a,z,'external-public-header',end)

for label,q,path,a,z in [('ZeroProb','MeasureTheory.IsZeroOrProbabilityMeasure','MeasureTheory/Measure/Typeclasses/Probability.lean',33,33),('properReal','FiniteDimensional.proper_real','Analysis/Normed/Module/FiniteDimension.lean',562,563),('properComplete','complete_of_proper','Topology/MetricSpace/ProperSpace.lean',104,104),('Proper','ProperSpace','Topology/MetricSpace/ProperSpace.lean',39,39),('Differentiable','Differentiable','Analysis/Calculus/FDeriv/Defs.lean',168,168),('Involutive','Function.Involutive','Logic/Function/Basic.lean',1010,1010),('fst','MeasureTheory.Measure.fst','MeasureTheory/Measure/Prod.lean',1086,1087),('toCLM','LinearIsometry.toContinuousLinearMap','Analysis/Normed/Operator/LinearIsometry.lean',276,276),('comap','MeasurableSpace.comap','MeasureTheory/MeasurableSpace/Basic.lean',82,82),('measurableSnd','measurable_snd','MeasureTheory/MeasurableSpace/Constructions.lean',384,385)]:
 id='D54.'+label;n(id,'external-unexpanded-primitive',q+' exact named public boundary; no private proof expanded',q);raw=(M/path).read_bytes();end,z=header_end(raw,a,z);span('api-'+label,id,M/path,a,z,'external-public-header',end)
n('P54.probZeroInstance','anonymous-public-instance','Probability to IsZeroOrProbability actual priority100 anonymous instance, NOT guessed toIsFiniteMeasure');raw=(M/'MeasureTheory/Measure/Typeclasses/Probability.lean').read_bytes();end,z=header_end(raw,74,75);span('prob-zero-instance','P54.probZeroInstance',M/'MeasureTheory/Measure/Typeclasses/Probability.lean',74,z,'public-instance-header',end)
for label,nid,path,a,z in [('norm-field-context','D54.Norm','Analysis/Normed/Group/Defs.lean',60,60),('volume-field-context','D54.volume','MeasureTheory/Measure/MeasureSpaceDef.lean',355,355),('smul-field-context','D54.SMul','C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Prelude.lean',1434,1434)]:
 path=Path(path) if path.startswith('C:') else M/path;span(label,nid,path,a,z,'context-public')
for a,b,r in [('D54.prob','P54.probZeroInstance','actual probability class is produced inside50'),('P54.probZeroInstance','D54.probFinite','real IsZeroOrProbability class output'),('D54.probFinite','P54.C1','actual finite nu obligation for C1 adapter'),('D54.properReal','D54.properComplete','finite real normed E gives actual properness'),('D54.properComplete','D54.gradient','actual CompleteSpace E derived internally from finite-position E')]:e(a,b,'actual-typeclass-slot',r)
# These type/structure signatures are opaque leaves. Their class hierarchy/body is not expanded into this bounded graph.
leaf_contracts={'AddCommGroup':'Algebra/Group/Defs.lean','AddCommMonoid':'Algebra/Group/Defs.lean','AddCommMonoid':'Algebra/Group/Defs.lean','AddSubgroup':'Algebra/Group/Subgroup/Defs.lean','CommRing':'Algebra/Ring/Defs.lean','DivisionRing':'Algebra/Field/Defs.lean','Ring':'Algebra/Ring/Defs.lean','Semiring':'Algebra/Ring/Defs.lean','MetricSpace':'Topology/MetricSpace/Defs.lean','SeminormedAddCommGroup':'Analysis/Normed/Group/Defs.lean','Inner':'Analysis/InnerProductSpace/Defs.lean','NormedSpace':'Analysis/Normed/Module/Basic.lean','UniformSpace':'Topology/UniformSpace/Defs.lean','Submodule':'Algebra/Module/Submodule/Defs.lean','OuterMeasure':'MeasureTheory/OuterMeasure/Defs.lean','RCLike':'Analysis/RCLike/Basic.lean','DistribMulAction':'Algebra/GroupWithZero/Action/Defs.lean','Star':'Algebra/Notation/Defs.lean','PseudoMetricSpace':'Topology/MetricSpace/Pseudo/Defs.lean','HasCompactMulSupport':'Topology/Algebra/Support.lean','MeasureSpace':'MeasureTheory/Measure/MeasureSpaceDef.lean'}
leaf_names={}
for q,path in leaf_contracts.items():
 raw=(M/path).read_bytes();ls=raw.decode('utf-8').splitlines();a=next((i+1 for i,l in enumerate(ls) if re.search(r'\b(?:class|structure|def|abbrev)\s+'+re.escape(q)+r'\b',l)),None)
 if a:
  id=n('X54.type.'+q,'external-unexpanded-type-primitive',q+' exact actual declaration header; deeper inherited hierarchy and implementation outside bounded expansion',q);end,z=header_end(raw,a,a);span('type-leaf-'+q,id,M/path,a,z,'external-unexpanded-type-boundary',end);leaf_names[q]=id


for label,q,path,a,z in [('comapLe','Measurable.comap_le','MeasureTheory/MeasurableSpace/Basic.lean',191,191),('subtypeL','Submodule.subtypeL','Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean',47,47),('topologicalClosure','Submodule.topologicalClosure','Topology/Algebra/Module/Basic.lean',157,157),('StarOperation','Star.star','Algebra/Notation/Defs.lean',94,94)]:
 id='D54.'+label;n(id,'external-unexpanded-primitive',q+' exact alias/definition or structure-field boundary; no body proof expanded',q);raw=(M/path).read_bytes();end,z=header_end(raw,a,z);span('api-'+label,id,M/path,a,z,'external-public-header',end)
core=Path('C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init')
n('D54.swap','external-unexpanded-primitive','Actual public Prod.swap definition, selected only full header','Prod.swap');raw=(core/'Data/Prod.lean').read_bytes();end,z=header_end(raw,61,61);span('api-swap','D54.swap',core/'Data/Prod.lean',61,z,'external-public-header',end)
n('D54.HSMulClass','external-unexpanded-type-primitive','Actual global HSMul class header; hSMul field is separate primitive','HSMul');span('HSMul-class','D54.HSMulClass',core/'Prelude.lean',1434,1434,'external-unexpanded-type-boundary')


n('P54.measurableIff','external-unexpanded-primitive','Actual measurable iff comap inequality producer for generated Measurable.comap_le alias','measurable_iff_comap_le');raw=(M/'MeasureTheory/MeasurableSpace/Basic.lean').read_bytes();end,z=header_end(raw,187,188);span('api-measurableIff','P54.measurableIff',M/'MeasureTheory/MeasurableSpace/Basic.lean',187,z,'external-public-header',end)
span('subtypeL-context','D54.subtypeL',M/'Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean',44,44,'context-public')


n('D54.NormClass','external-unexpanded-type-primitive','Actual global Norm class; distinct from generated Norm.norm field','Norm');span('Norm-class','D54.NormClass',M/'Analysis/Normed/Group/Defs.lean',60,60,'external-unexpanded-type-boundary')

# Mathematical source graph; all four parents and actual inner obligations are explicit ingredients.
for a,b,k,r in [('S54.standing','P54.p50','source-assumption','actual original source binders supplied internally'),('S54.laws','P54.p50','same-law','literal mu/J/nu'),('S54.compact','P54.p50','compact-source','same signed smoothcompact f'),('S54.density','P54.p53','source-law','all-y literal reflected volume density'),('S54.standing','P54.p53','source-assumption','alpha cast, lower half of two Hessian bounds and same V C2'),('P54.p50','A54.prob','real-producer','actual mu/J/nu probability'),('A54.prob','P54.p51','internal-premise','mu probability and eta positivity supplied inside'),('P54.p51','A54.core','real-producer','uniform dense closable core/full graph/closed closure'),('P54.p53','A54.C1','real-producer','every-y literal source mean is C1'),('P54.p50','A54.pointwise','real-producer','all-y chosen S equals literal S; funext yields entire mean function identity'),('A54.pointwise','A54.L2','literal-transport','rewrite mean and true gradient by function equality, never AE derivative'),('P54.p50','A54.L2','real-producer','same nu MemLp of actual mean and actual gradient'),('A54.prob','P54.C1','internal-premise','finite nu from probability'),('A54.core','P54.C1','internal-premise','actual G closability and EXACT compact graph'),('A54.C1','P54.C1','internal-premise','true literal Tf C1'),('A54.L2','P54.C1','internal-premise','both canonical real MemLp witnesses'),('P54.C1','A54.domain','real-adapter','canonical toLp pair in same G.closure.graph'),('A54.core','T54','produced-conclusion','uniform G selected before forall f'),('A54.domain','T54','produced-conclusion','every signed smoothcompact f domain pair'),('A54.prob','T54','produced-conclusion','actual nu probability'),('D54.closable','D54.closure','definition-semantics','closure chooses actual extension only if closable'),('D54.closure','A54.domain','definition-semantics','actual closed operator, not original graph or50 blockD'),('D54.graph','A54.domain','definition-semantics','actual canonical pair membership'),('D54.toLp','A54.domain','definition-semantics','actual quotient representatives, no certificate input'),('D54.gradient','A54.L2','definition-semantics','true Riesz inverse fderiv gradient'),('S54.compact','X54.omitted','source-gap','source compact reduction omits actual C1/closure analytic details'),('A54.domain','X54.rough','typed-consumer','compact prerequisite ONLY; no allL2 limit yet'),('A54.extension','T54','authored-extension','finite-Hilbert/rank0 measurable source extension'),('S54.energy','A54.L2','inherited-producer-source','already compiled50 produces true gradient L2; not new54sharp proof'),('S54.covariance','S54.energy','inherited-source','source true derivative compact energy'),('S54.density','S54.covariance','source-definition-use','literal normalized density'),('S54.score','S54.covariance','source-definition-use','literal actual score')]:e(a,b,k,r)
# Coverage physical rows are exhaustive for the selected header/source fragments. Incidental old50 source math is honestly EXCLUDED.
coverage=[];formulas=[];callers=[];lex=[];unknown=[]
known={x['qualified_id']:x['id'] for x in N if x['qualified_id']}
for q,id in list(known.items()):known.setdefault(q.split('.')[-1],id)
known.update({'ℝ':'D54.Real','ℝ≥0':'D54.NNReal','ℝ≥0∞':'D54.eLpNorm','gradient':'D54.gradient','IsClosed':'D54.IsClosed','Module':'D54.Module','closure':'D54.closure','graph':'D54.graph','IsClosable':'D54.closable','NormedAddCommGroup':'D54.NAC','InnerProductSpace':'D54.IP','FiniteDimensional':'D54.FD','Lp':'D54.Lp','MemLp':'D54.MemLp','IsProbabilityMeasure':'D54.prob','ContDiff':'D54.CD','HasCompactSupport':'D54.compact','Measure':'D54.Measure','volume':'D54.volume','integral':'D54.integral','Set':'D54.Set','Norm':'D54.NormClass','ContinuousLinearMap':'D54.CLM','SMul':'D54.SMul'})
keywords=set('theorem lemma def abbrev irreducible_def noncomputable class structure extends where variable Type Prop Sort let fun in by forall exists if then else return open scoped section namespace end inferInstance volume_tac true false protected public expose instance irreducible alias implicit_reducible outParam SL w M L ᵐ ₗ ₗᵢ ₛₗ ₘ ₂ ℕ'.split())
known.update(leaf_names)
known.update({'U.toContinuousLinearMap':'D54.toCLM','Λ.fst':'D54.fst','f.domain':'D54.LPM','Function.Involutive':'D54.Involutive','Differentiable':'D54.Differentiable'})
# Composite graphical member chains require BOTH named definition edges, not just the last graph member.
known.update({'f.graph.topologicalClosure':'D54.topologicalClosure','measurable_snd.comap_le':'D54.comapLe','star':'D54.StarOperation','HSMul':'D54.HSMulClass','Prod.swap':'D54.swap','subtypeL':'D54.subtypeL'})
# Primitive headers use externally unexpanded inherited context. Their unexpanded symbols are inventoried as explicit boundary tokens, not fabricated type bindings.
for pr in P:
 raw=Path(pr['path']).read_bytes();ls=raw.splitlines(keepends=True);lo=pr['start_utf8_byte0'];hi=pr['end_utf8_byte0_exclusive'];pos=0;t=texts[pr['id']]
 bound=set()
 for mm in re.finditer(r'[({]\s*([^:{}()\[\]]+)\s*:',t):bound.update(re.findall(r'[^\W\d]\w*',mm.group(1),re.UNICODE))
 for mm in re.finditer(r'(?:∀|∃|fun)\s+([^,:()]+)\s*[:,]',t):bound.update(re.findall(r'[^\W\d]\w*',mm.group(1),re.UNICODE))
 bound.update(['E','F','R','S','T','𝕜','𝕜\u2032','𝕜\u2032\u2032','α','β','η','μ','ν','J','G','D','A','B','P','U','Λ','Tf','X','Y','γ','b','ω','f','g','u','v','x','y','a','H','φ','p','m','m0','ε','ε\u2032','q','n','σ','σ₁₂','R₂','E₂','Ω','κ','s','𝕜₁','𝕜₂','h_mem_ℒp'])
 for line1,line in enumerate(ls,1):
  lineStart=pos;pos+=len(line)
  if pos<=lo or lineStart>=hi:continue
  a=max(lo,lineStart);z=min(hi,pos);part=raw[a:z].decode('utf-8');consumer=pr['node'];role='NODE';reason='Exact selected actual public header/context, external body boundary explicitly retained'
  if pr['kind']=='primary-source':
   if line1 in range(4573,4577):consumer='S54.compact'
   elif line1 in range(4579,4588):consumer='S54.density'
   elif line1 in range(4588,4596):consumer='S54.score'
   elif line1 in range(4596,4605):consumer='S54.covariance'
   elif line1 in range(4607,4653):consumer='X54.old50';role='EXCLUDED';reason='Genuine old50 conditional coercivity/CS source mathematics;54 reuses admitted parent and does not expand this proof subgraph'
   elif line1 in range(4653,4662):consumer='S54.energy'
   elif line1 in range(4662,4665):consumer='X54.Gamma';role='EXCLUDED';reason='Genuine full source operator/Gamma/allrough consumer beyond54 compact closed-domain join'
   if not re.search(r'alttext=|<p\b|<a\b',part) and not re.sub('<[^>]*>','',part).strip():role='EXCLUDED';consumer=None;reason='Blank/table/cell layout; no mathematical proposition'
   for mm in re.finditer(r'alttext="([^"]*)"',part):formulas.append(dict(provider=pr['id'],physical_line1=line1,formula=mm.group(1),node=consumer,classification=role))
   for mm in re.finditer(r'href="([^"]*)"',part):
    token=mm.group(1);ref=token[1:] if token.startswith('#') else token;resolved={'A2.E13':'X54.rough','A3.E1':'S54.covariance','S2.E7':'S54.laws'}.get(ref)
    if not resolved:resolved=n('X54.href.'+re.sub(r'[^\w]','_',ref),'external-unexpanded-source-reference','Literal primary reference '+token+'; outside selected source expansion')
    start=a+len(part[:mm.start(1)].encode('utf-8'));idx=len(callers);callers.append(dict(index0=idx,provider=pr['id'],consumer=consumer or pr['node'],physical_line1=line1,physical_line0=line1-1,utf8_byte_start0=start,utf8_byte_end0_exclusive=start+len(token.encode('utf-8')),utf8_column_start0=start-lineStart,utf8_column_end0_exclusive=start-lineStart+len(token.encode('utf-8')),token=token,resolution=resolved,classification='source-direct-reference' if role=='NODE' else 'excluded-source-reference-boundary'))
    e(resolved,consumer or pr['node'],'source-reference' if role=='NODE' else 'excluded-source-reference-boundary','Literal exact primary href, not54 compiled call',idx)
  elif not part.strip():role='EXCLUDED';consumer=None;reason='Blank line'
  coverage.append(dict(provider=pr['id'],path=pr['path'],physical_line1=line1,physical_line0=line1-1,utf8_byte_start0=a,utf8_byte_end0_exclusive=z,utf8_column_start0=a-lineStart,utf8_column_end0_exclusive=z-lineStart,classification=role,node=consumer,reason=reason,raw_line_sha256=H(raw[a:z])))
  if pr['kind']=='primary-source':continue
  for mm in re.finditer(r'[^\W\d]\w*(?:\.[^\W\d]\w*)*',part,re.UNICODE):
   token=mm.group();start=a+len(part[:mm.start()].encode('utf-8'));res=known.get(token);classification='primitive-public-reference' if res else 'bound-identifier-or-syntax'
   tail=token.split('.')[-1]
   projections=[]
   if token=='measurable_snd.comap_le':projections=['D54.measurableSnd']
   if token=='f.graph.topologicalClosure':projections=['D54.graph']
   if token.endswith('.IsClosed'):res='D54.closed';projections=['D54.closure'] if '.closure.' in token else []
   if not res and '.' in token:
    for suffix in token.split('.')[1:]:
     if suffix in known:projections.append(known[suffix])
    res=known.get(tail)
   if not res and token not in bound and token not in keywords and tail not in bound and pr['kind']!='external-unexpanded-type-boundary' and not (token=='Measurable.of_comap_le' and pr['id']=='api-comapLe'):
    # No guessed APIs: named external boundary is recorded unresolved for creator follow-up, never called a local binder.
    classification='external-unexpanded-lexical-boundary';unknown.append(dict(provider=pr['id'],token=token,line1=line1))
   if not res and token not in bound and token not in keywords and pr['kind']=='external-unexpanded-type-boundary':classification='explicit-external-unexpanded-type-hierarchy-boundary'
   if token=='Measurable.of_comap_le' and pr['id']=='api-comapLe':classification='generated-alias-name-binding';res=None;projections=[]
   if token==node[pr['node']].get('qualified_id') or token==str(node[pr['node']].get('qualified_id')).split('.')[-1]:classification='declaration-name-binding';res=pr['node'];projections=[]
   record=dict(index0=len(lex),provider=pr['id'],consumer=pr['node'],physical_line1=line1,physical_line0=line1-1,utf8_byte_start0=start,utf8_byte_end0_exclusive=start+len(token.encode('utf-8')),utf8_column_start0=start-lineStart,utf8_column_end0_exclusive=start-lineStart+len(token.encode('utf-8')),token=token,classification=classification,resolution=res,composite_projections=projections)
   lex.append(record)
   if res and classification!='declaration-name-binding':
    # Field domain/subtype/etc is context, not a invented theorem call. Semantic named projections are explicit separate ingredient edges.
    ci=len(callers);callers.append(dict(record,index0=ci));e(res,pr['node'],'public-header-or-context-reference','Actual selected symbol occurrence; no54 implementation call',ci)
    for other in projections:
     if other!=res:e(other,pr['node'],'composite-definition-reference','Actual composite closure/graph projection in selected header',ci)
J('selected-providers.json',P);J('source-proof-graph.json',{'schema_version':'bounded-source-proof-graph54/v1','status':'CREATOR_SOURCE_RECONSTRUCTION_NOT_TOPOLOGY_ADMITTED','edge_orientation':'ingredient -> consumer','nodes':N,'edges':E,'scope':'Compact literal source Tf C1+actual L2+uniform Gaussian outer core -> canonical closed graph pair; no implementation54 exists','source_expansion_boundary':'Four opaque admitted ASTIS public producers, exact primitive public definitions/types; old50 coercivity math and allrough/Gamma genuinely excluded','compiled_graph_created':False})
J('source-coverage.json',coverage);J('primary-formula-inventory.json',formulas);J('caller-inventory.json',callers);J('lexical-inventory.json',lex);J('selected-token-inventory.json',lex);J('unresolved-lexemes.json',unknown);J('counts.json',dict(nodes=len(N),edges=len(E),providers=len(P),coverage=len(coverage),node_rows=sum(x['classification']=='NODE' for x in coverage),excluded_rows=sum(x['classification']=='EXCLUDED' for x in coverage),callers=len(callers),lexemes=len(lex),formulas=len(formulas),external_unexpanded_lexical_boundaries=len(unknown)))
print(json.dumps({'counts':json.loads((O/'counts.json').read_text(encoding='utf-8')),'unresolved':sorted(set(x['token'] for x in unknown))},ensure_ascii=False))
