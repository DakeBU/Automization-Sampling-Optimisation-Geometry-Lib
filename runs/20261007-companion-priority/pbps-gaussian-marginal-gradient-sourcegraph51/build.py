# coding: utf-8
import pathlib,re,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-sourcegraph51';M='.lake/packages/mathlib/Mathlib/'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def txt(n,x):(O/n).write_bytes(x.encode())
assert json.loads((O/'lease.json').read_text(encoding='utf-8-sig'))['status']=='OPEN'
(O/'lease.open.historical.raw').write_bytes((O/'lease.json').read_bytes())
nodes=[];edges=[];providers=[];coverage=[];callers=[];lexemes=[];cache={}
def node(i,k,c,q=None):
 if not any(x['id']==i for x in nodes):nodes.append(dict(id=i,kind=k,contract=c,qualified_id=q,compiled51=False,proof_body_expanded=False))
def edge(a,b,k,why,caller=None):edges.append(dict(id='E51.'+str(len(edges)),ingredient=a,consumer=b,kind=k,reason=why,caller_index0=caller,compiled51call=False))
def raw(rel):
 if rel not in cache:cache[rel]=(R/rel).read_bytes()
 return cache[rel]
def select(label,n,rel,a,z,kind,cut=None):
 b=raw(rel);ls=b.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));end=sum(map(len,ls[:z]));f=b[start:end]
 if kind in ['external-definition-header','external-abbrev-header','external-structure-header','external-class-header','external-instance-header']:
  marker=b':=' if b':=' in f else (b'where' if b'where' in f else None)
  if marker:end=start+f.index(marker);f=b[start:end]
 if cut and cut.encode() in f:end=start+f.index(cut.encode());f=b[start:end]
 (O/(label+'.raw')).write_bytes(f);(O/(label+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'))
 pr=dict(id=label,node=n,path=str(R/rel),kind=kind,whole_raw_sha256=sha(b),whole_lf_sha256=sha(b.replace(b'\r\n',b'\n')),start_utf8_byte0=start,end_utf8_byte0_exclusive=end,physical_lines1=[a,b[:max(start,end-1)].count(b'\n')+1],fragment_raw_sha256=sha(f),fragment_lf_sha256=sha(f.replace(b'\r\n',b'\n')),body_selected=kind in ['actual-definition-body','actual-generated-origin-body'],external_expansion_boundary=kind.startswith('external'))
 providers.append(pr)
 # All selected bytes represented exactly once per selected physical row. Terminal prefixes honest.
 pos=start
 comment_intervals=[(m.start(),m.end()) for m in re.finditer(rb'/\-.*?\-/',f,re.S)]
 for j,line in enumerate(f.splitlines(keepends=True),a):
  s=line.decode();visible=re.sub('<[^>]*>','',s).strip() if kind=='primary-source' else s.strip()
  mathhtml=('alttext=' in s or '<a href=' in s or ('<p ' in s and visible))
  excluded=(not visible) if kind!='primary-source' else (not mathhtml and not visible)
  if kind!='primary-source' and (visible.startswith('/-') or visible.startswith('--') or visible in ['noncomputable','@[simp]','@[fun_prop]','open scoped Classical in']):excluded=True
  if kind!='primary-source':
   q=pos-start;masked=bytearray(line)
   for ca,cz in comment_intervals:
    for v in range(max(q,ca),min(q+len(line),cz)):masked[v-q]=32
   code=bytes(masked).decode().strip()
   if not code or code.startswith('@[') or code==']':excluded=True
  coverage.append(dict(provider=label,path=pr['path'],physical_line1=j,start_utf8_byte0=pos,end_utf8_byte0_exclusive=pos+len(line),classification='EXCLUDED' if excluded else 'NODE',node=None if excluded else n,reason='layout/comment/empty/attribute; no theorem ingredient' if excluded else ('literal source mathematical statement/reference' if kind=='primary-source' else 'selected exact contract/definition/typing context'),raw_line_sha256=sha(line)))
  pos+=len(line)
 return pr
node('S51.model','source-model','Source normalized Gibbs probability μ on R^d, finite Euclidean setting; no finite moment assumption for authored background target.')
node('S51.J','source-definition','Source proximal augmentation πη and conditional Gaussian Y|X; actual J is Gaussian add-noise pushforward.')
node('S51.nu','source-definition','Source πηY=μ*N(0,ηI); same actual ν=J.snd.')
node('S51.gap','SOURCE_GAP','C.1 says density and closedness of gradient without constructing actual outer-law smooth compact graph. Supplied by independently compiled ASTIS analytic producers; not a printed full theorem proof.')
node('S51.B13','source-consumer-residual','Full all-L2 input T f∈H1 and 4η gradient norm²≤norm-defect, Γnorm²/Bnorm². Only actual outer-law closure prerequisite is assigned; Tf domain/rough extension/Γ remain residual.')
primary='runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'
for x in [('source-model','S51.model',351,353),('source-joint','S51.J',617,633),('source-marginal','S51.nu',635,640),('source-gap','S51.gap',4573,4576),('source-consumer','S51.B13',3779,3787)]:select(x[0],x[1],primary,x[2],x[3],'primary-source')
node('T51','authored-target','Exact697LF d7273526… actual Gaussian marginal genuine compact gradient graph: dense domain, closable, closed closure. No public potential/normalization/domain/desired-bound certificates.')
pre='runs/20261007-companion-priority/pbps-gaussian-marginal-gradient-preproof51/'
candidate=raw(pre+'prospective-statement.txt');assert sha(candidate.replace(b'\r\n',b'\n'))=='d7273526caa94ec518b790626edb6b289bdabfdd1104a196cd2e8eb110211e81';assert len(candidate.replace(b'\r\n',b'\n'))==697
select('candidate','T51',pre+'prospective-statement.txt',1,12,'candidate-contract')
for name in ['root.statement-proposal.json','statement-seals.accepted.json']:
 b=raw(pre+name);(O/(name+'.raw')).write_bytes(b);(O/(name+'.lf')).write_bytes(b.replace(b'\r\n',b'\n'))
parent1='AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean';parent2='AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean'
assert sha(raw(parent1))=='25394020514aba3d497bd91b498c06155e2e84675dc077c96466677c4860feb5'
assert sha(raw(parent2))=='c2495b6ab8a4c82cadf0d86b910d663e0e4f65f6b96bc4b449149112756d4690'
node('A51.C2','opaque-verified-ASTIS-producer','Any probability μ, η>0: actual Gaussian pushforward equals everywhere positive C Z volume density; Z and W=-log(C Z) globally C2. No moments or input density supplied.','AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2')
node('A51.D','opaque-verified-ASTIS-producer','C1 W and actual Integrable exp(-W) produce dense genuine compact-gradient graph for normalized tilt, closable with closed closure; rank0 included.','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradient.compact_gradient_closable')
select('C2-context','A51.C2',parent1,33,33,'public-typing-context');select('C2-context-measure','A51.C2',parent1,144,144,'public-typing-context');select('C2-public','A51.C2',parent1,255,262,'opaque-verified-public-header',':= by')
select('D-public','A51.D',parent2,31,41,'opaque-verified-public-header',':= by')
# External public contracts are selected; bodies stay beyond an explicit expansion boundary.
spec=[
 ('P51.stdG','ProbabilityTheory.stdGaussian','standard finiteHilbert Gaussian, covariance identity, true law',M+'Probability/Distributions/Gaussian/Multivariate.lean',66,66,'external-definition-header'),
 ('P51.stdGprob','ProbabilityTheory.isProbabilityMeasure_stdGaussian','stdGaussian E probability under finiteHilbert/Borel contexts',M+'Probability/Distributions/Gaussian/Multivariate.lean',72,72,'external-theorem-header'),
 ('P51.prod','MeasureTheory.Measure.prod','actual independent product measure',M+'MeasureTheory/Measure/Prod.lean',171,171,'external-definition-header'),
 ('P51.prodprob','MeasureTheory.Measure.prod.instIsProbabilityMeasure','probability product from two actual probability measures',M+'MeasureTheory/Measure/Prod.lean',322,324,'external-instance-header'),
 ('P51.map','MeasureTheory.Measure.map','actual a.e.-measurable pushforward; zero fallback not used because maps are continuous/measurable',M+'MeasureTheory/Measure/Map.lean',91,92,'external-definition-header'),
 ('P51.mapmap','MeasureTheory.Measure.map_map','composition of measurable measure maps',M+'MeasureTheory/Measure/Map.lean',203,204,'external-theorem-header'),
 ('P51.mapprob','MeasureTheory.Measure.isProbabilityMeasure_map','a.e.-measurable probability pushforward',M+'MeasureTheory/Measure/Typeclasses/Probability.lean',124,125,'external-theorem-header'),
 ('P51.snd','MeasureTheory.Measure.snd','literal marginal = ρ.map Prod.snd',M+'MeasureTheory/Measure/Prod.lean',1148,1149,'actual-definition-body'),
 ('P51.tilt','MeasureTheory.Measure.tilted','density of exp(f)/integral exp(f); normalized denominator1 internally',M+'MeasureTheory/Measure/Tilted.lean',42,43,'actual-definition-body'),
 ('P51.wd','MeasureTheory.Measure.withDensity','actual density measure; no integrability in definition, its finite mass is used',M+'MeasureTheory/Measure/WithDensity.lean',39,39,'external-definition-header'),
 ('P51.wdapply','MeasureTheory.withDensity_apply','measurable-set evaluation by lintegral',M+'MeasureTheory/Measure/WithDensity.lean',44,45,'external-theorem-header'),
 ('P51.ofReal','ENNReal.ofReal','nonnegative part coerced to ENNReal',M+'Data/ENNReal/Basic.lean',230,230,'external-definition-header'),
 ('P51.Igate','MeasureTheory.lintegral_ofReal_ne_top_iff_integrable','AEStronglyMeasurable and AE nonnegative real density: finite lintegral iff integrable',M+'MeasureTheory/Function/L1Space/Integrable.lean',934,936,'external-theorem-header'),
 ('P51.realI','MeasureTheory.ofReal_integral_eq_lintegral_ofReal','integrable AE nonnegative real density preserves actual lintegral',M+'MeasureTheory/Integral/Bochner/Basic.lean',702,703,'external-theorem-header'),
 ('P51.one','ENNReal.ofReal_eq_one','ofReal r=1 iff r=1 (no extra caller positivity premise needed)',M+'Data/ENNReal/Real.lean',254,254,'external-theorem-header'),
 ('P51.expLog','Real.exp_log','positive rho gives exp(log rho)=rho',M+'Analysis/SpecialFunctions/Log/Basic.lean',59,59,'external-theorem-header'),
 ('P51.C1','ContDiff.of_le','C2 to C1 by order of smoothness',M+'Analysis/Calculus/ContDiff/Defs.lean',1141,1141,'external-theorem-header'),
 ('P51.cont','ContDiff.continuous','C2/C1 implies actual continuity',M+'Analysis/Calculus/ContDiff/Defs.lean',1151,1151,'external-theorem-header'),
 ('P51.meas','Continuous.measurable','continuous maps Borel measurable under declared Borel spaces',M+'MeasureTheory/Constructions/BorelSpace/Basic.lean',492,492,'external-theorem-header'),
 ('P51.AEStrong','Continuous.aestronglyMeasurable','continuous density on Borel finiteHilbert domain, real range: actual AE strong measurability; all metrizability/countability contexts internal',M+'MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean',239,241,'external-theorem-header'),
 ('D51.integral','MeasureTheory.integral','actual Bochner integral, totalized when integrability absent; actual integrability is produced before normalization',M+'MeasureTheory/Integral/Bochner/Basic.lean',156,156,'external-definition-header'),
 ('D51.lintegral','MeasureTheory.lintegral','actual lower Lebesgue integral',M+'MeasureTheory/Integral/Lebesgue/Basic.lean',48,48,'external-definition-header'),
 ('D51.AEeq','Filter.EventuallyEq','actual AE equality is eventual equality along actual measure ae filter; no pointwise derivative transfer',M+'Order/Filter/Defs.lean',297,297,'external-definition-header'),
 ('D51.prob','MeasureTheory.IsProbabilityMeasure','class mass-univ=1; measure_univ is a generated class field, not a theorem wrapper',M+'MeasureTheory/Measure/Typeclasses/Probability.lean',64,65,'actual-definition-body'),
 ('D51.Lp','MeasureTheory.Lp','Lp AE classes with finite seminorm; definition body not expanded',M+'MeasureTheory/Function/LpSpace/Basic.lean',89,90,'external-definition-header'),
 ('D51.Integrable','MeasureTheory.Integrable','AEStronglyMeasurable and HasFiniteIntegral',M+'MeasureTheory/Function/L1Space/Integrable.lean',59,61,'actual-definition-body'),
 ('D51.AEStrong','MeasureTheory.AEStronglyMeasurable','AE strong measurability predicate',M+'MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean',66,67,'external-definition-header'),
 ('D51.AEmeas','MeasureTheory.AEMeasurable','AE-measurability predicate',M+'MeasureTheory/Measure/MeasureSpaceDef.lean',409,409,'external-definition-header'),
 ('D51.HFI','MeasureTheory.HasFiniteIntegral','finite norm lintegral',M+'MeasureTheory/Function/L1Space/HasFiniteIntegral.lean',80,81,'external-definition-header'),
 ('D51.D','LinearPMap','genuine partial linear map domain field, not globally bounded CLM',M+'LinearAlgebra/LinearPMap.lean',41,47,'external-structure-contract'),
 ('D51.graph','LinearPMap.graph','graph submodule of scalar/vector L2 product',M+'LinearAlgebra/LinearPMap.lean',735,735,'external-definition-header'),
 ('D51.closable','LinearPMap.IsClosable','closure of graph must remain a graph (single-valued)',M+'Topology/Algebra/Module/LinearPMap.lean',70,70,'external-definition-header'),
 ('D51.closed','LinearPMap.IsClosed','closedness of actual graph',M+'Topology/Algebra/Module/LinearPMap.lean',63,63,'external-definition-header'),
 ('D51.closure','LinearPMap.closure','chosen graph closure when closable; identity otherwise; closability is output',M+'Topology/Algebra/Module/LinearPMap.lean',97,97,'external-definition-header'),
 ('D51.Dense','Dense','domain dense in L2 topology',M+'Topology/Defs/Basic.lean',146,146,'external-definition-header'),
 ('D51.CD','ContDiff','Taylor smoothness predicate with stated ℝ order',M+'Analysis/Calculus/ContDiff/Defs.lean',1068,1068,'external-definition-header'),
 ('D51.compactMul','HasCompactMulSupport','literal multiplicative origin used by to_additive to generate HasCompactSupport; origin semantic calls kept distinct',M+'Topology/Algebra/Support.lean',213,217,'actual-generated-origin-body'),
 ('D51.gradient','gradient','literal true gradient=(toDual).symm(fderiv f); finiteHilbert complete',M+'Analysis/Calculus/Gradient/Basic.lean',82,83,'actual-definition-body'),
 ('D51.Measure','MeasureTheory.Measure','countably additive measure (structure contract)',M+'MeasureTheory/Measure/MeasureSpaceDef.lean',77,77,'external-structure-header'),
 ('D51.MS','MeasurableSpace','measurable-space structure typing',M+'MeasureTheory/MeasurableSpace/Defs.lean',49,49,'external-structure-header'),
 ('D51.NAC','NormedAddCommGroup','normed additive group typing',M+'Analysis/Normed/Group/Defs.lean',247,247,'external-class-header'),
 ('D51.IP','InnerProductSpace','real inner product norm typing',M+'Analysis/InnerProductSpace/Defs.lean',107,108,'external-class-header'),
 ('D51.FD','FiniteDimensional','finite-dimensional position space (not L2(J))',M+'LinearAlgebra/FiniteDimensional/Defs.lean',75,75,'external-abbrev-header'),
 ('D51.Borel','BorelSpace','actual Borel compatibility typing',M+'MeasureTheory/Constructions/BorelSpace/Basic.lean',113,113,'external-class-header'),
 ('D51.volume','MeasureTheory.MeasureSpace.volume','generated MeasureSpace class field, finiteHilbert canonical volume',M+'MeasureTheory/Measure/MeasureSpaceDef.lean',355,356,'external-class-field-origin')]
for i,q,c,p,a,z,k in spec:
 node(i,k,c,q);select(i,i,p,a,z,k,':= by' if k.startswith('external-theorem') else None)
select('stdGaussian-typing','P51.stdG',M+'Probability/Distributions/Gaussian/Multivariate.lean',54,55,'public-typing-context')
select('stdGaussian-prob-typing','P51.stdGprob',M+'Probability/Distributions/Gaussian/Multivariate.lean',70,70,'public-typing-context')
select('map-prob-typing','P51.mapprob',M+'MeasureTheory/Measure/Typeclasses/Probability.lean',116,116,'public-typing-context')
select('gradient-typing','D51.gradient',M+'Analysis/Calculus/Gradient/Basic.lean',51,52,'public-typing-context')
node('F51.domain','generated-structure-field','LinearPMap.domain : Submodule; generated field anchored at LinearPMap structure43. No implementation call to a parent theorem.','LinearPMap.domain')
node('D51.compact','generated-additive-definition','HasCompactSupport f=IsCompact(tsupport f), generated by declared to_additive origin; not literal source HasCompactMulSupport caller.','HasCompactSupport')
edge('D51.compactMul','D51.compact','generated-definition-origin','Explicit to_additive origin; generated attribute itself is not a mathematical call')
node('F51.mass','generated-class-field','IsProbabilityMeasure.measure_univ : μ univ=1; classfield access, not declaration-level wrapper call.','MeasureTheory.IsProbabilityMeasure.measure_univ')
edge('D51.D','F51.domain','field-origin','Real generated domain field from structure')
edge('D51.prob','F51.mass','field-origin','Real mass field from probability class')
for i,c in [('I51.laws','actual J and ν maps continuous/measurable; μ×γ, J and ν probability'),('I51.density','Actual ν=volume.withDensity(ofReal ρ), ρ=C Z>0; W=-logρ globallyC2'),('I51.mass','withDensity_apply univ and probability mass => lintegral(ofRealρ)=1'),('I51.integrable','ρ continuous hence AEStronglyMeasurable; nonnegative and mass1 => Integrableρ'),('I51.normalizer','ofReal_integral identity and ofReal_eq_one => ∫ρ=1'),('I51.exp','exp(-W)=ρ pointwise by positive exp_log; signs/zeros handled by actual strict density positivity'),('I51.tilt','actualν=volume.tilted(-W) from true density formula and normalizer1'),('I51.C1','actualW C2 impliesC1 internally'),('I51.output','Invoke true opaque weighted-gradient producer with internally produced W,C1,integrability; transport literal measure equality'),('X51.generic','Authored generalization: any probability μ, η>0; source uses Gibbsμ under curvature/step restrictions. No new paper premise.'),('X51.rank0','Authored finiteHilbert/rank0 extension: exact Gaussian density C uses finrank and has rank0 C=1; no positive dimension assumption.')]:node(i,'internal-source-obligation' if i.startswith('I') else 'authored-extension',c)
node('C51.actual50','opaque-compiled-consumer-contract','Actual MacroscopicEnergy public μ,J,ν probability outputs and literal same Gaussian laws. μprob/η>0 are produced/retained internally for paper application; generic target does not add them as new paper certificates.','AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks')
node('C51.rough','future-source-consumer-residual','Full B.13 extension may consume actual50 smooth energy plus actual outer-gradient closure51. Still needs literalTf graph membership and density/closedness limit argument; no proof of these or Γ is claimed.')
consumer='AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean';select('actual50-hypotheses-laws','C51.actual50',consumer,23,35,'opaque-consumer-public-subcontract');select('actual50-probability-output','C51.actual50',consumer,41,41,'opaque-consumer-public-subcontract')
# Actual source-derived analytic dependencies, independent of any future Lean implementation.
dep=[('S51.J','S51.nu'),('S51.nu','S51.gap'),('S51.gap','T51'),('P51.stdGprob','I51.laws'),('P51.prodprob','I51.laws'),('P51.mapprob','I51.laws'),('P51.snd','I51.laws'),('P51.mapmap','I51.density'),('A51.C2','I51.density'),('I51.laws','I51.density'),('I51.density','I51.mass'),('F51.mass','I51.mass'),('P51.wdapply','I51.mass'),('P51.cont','I51.integrable'),('P51.meas','I51.integrable'),('P51.Igate','I51.integrable'),('I51.mass','I51.integrable'),('I51.density','I51.integrable'),('I51.integrable','I51.normalizer'),('P51.realI','I51.normalizer'),('P51.one','I51.normalizer'),('I51.mass','I51.normalizer'),('P51.expLog','I51.exp'),('I51.density','I51.exp'),('I51.exp','I51.tilt'),('I51.normalizer','I51.tilt'),('P51.tilt','I51.tilt'),('I51.density','I51.tilt'),('P51.C1','I51.C1'),('I51.density','I51.C1'),('A51.D','I51.output'),('I51.C1','I51.output'),('I51.integrable','I51.output'),('I51.exp','I51.output'),('I51.tilt','I51.output'),('I51.output','T51'),('X51.generic','T51'),('X51.rank0','T51'),('T51','C51.rough'),('C51.actual50','C51.rough'),('S51.B13','C51.rough')]
dep.append(('P51.AEStrong','I51.integrable'))
for a,b in dep:edge(a,b,'source-ingredient','Selected source mathematical reconstruction; not a compiled51 call and not proof credit')
alias={q.split('.')[-1]:(i,q) for i,q,c,p,a,z,k in spec}
alias.update({q:(i,q) for i,q,c,p,a,z,k in spec})
alias.update({'HasCompactSupport':('D51.compact','HasCompactSupport'),'NormedAddCommGroup':('D51.NAC','NormedAddCommGroup'),'InnerProductSpace':('D51.IP','InnerProductSpace'),'FiniteDimensional':('D51.FD','FiniteDimensional'),'IsProbabilityMeasure':('D51.prob','MeasureTheory.IsProbabilityMeasure'),'domain':('F51.domain','LinearPMap.domain'),'measure_univ':('F51.mass','MeasureTheory.IsProbabilityMeasure.measure_univ'),'prod':('P51.prod','MeasureTheory.Measure.prod'),'map':('P51.map','MeasureTheory.Measure.map'),'snd':('P51.snd','MeasureTheory.Measure.snd'),'Prod.snd':('EXT.Prod.snd','Prod.snd'),'symm':('EXT.toDual.symm','LinearIsometryEquiv.symm'),'toDual':('EXT.toDual','InnerProductSpace.toDual'),'fderiv':('EXT.fderiv','fderiv'),'sqrt':('EXT.sqrt','Real.sqrt'),'Real.sqrt':('EXT.sqrt','Real.sqrt'),'Real.pi':('EXT.pi','Real.pi'),'Real.log':('EXT.log','Real.log'),'Real.exp':('EXT.exp','Real.exp'),'exp':('EXT.exp','Real.exp'),'log':('EXT.log','Real.log'),'Module.finrank':('EXT.finrank','Module.finrank'),'ENNReal.ofReal':('P51.ofReal','ENNReal.ofReal'),'topologicalClosure':('EXT.submoduleClosure','Submodule.topologicalClosure')})
# Explicit external boundaries: identities resolved from declaration contracts; bodies not selected.
for i,q,c in [('EXT.Prod.snd','Prod.snd','product second projection; Lean core primitive'),('EXT.toDual.symm','LinearIsometryEquiv.symm','inverse Riesz isometry; not a supplied gradient certificate'),('EXT.toDual','InnerProductSpace.toDual','Riesz dual isometry'),('EXT.fderiv','fderiv','Frechet derivative, totalized to0 when absent'),('EXT.sqrt','Real.sqrt','nonnegative real sqrt'),('EXT.pi','Real.pi','real pi constant'),('EXT.log','Real.log','real log; strictpositive density used'),('EXT.exp','Real.exp','real exponential'),('EXT.finrank','Module.finrank','position dimension used only Gaussian density prefactor'),('EXT.submoduleClosure','Submodule.topologicalClosure','topological closure submodule')]:node(i,'external-unexpanded-primitive',c,q)
for q in ['AddCommGroup','AddSubgroup','Continuous','DivisionRing','Inner','IsCompact','Measurable','MeasurableSet','MeasureTheory.MeasureSpace','MetricSpace','Norm','NormedSpace','MeasureTheory.OuterMeasure','RCLike','Ring','SeminormedAddCommGroup','Submodule','TopologicalSpace','mulTSupport','OpensMeasurableSpace','PseudoMetrizableSpace','SecondCountableTopologyEither','Filter','CompleteSpace']:
 i='TYPE.'+q.split('.')[-1];node(i,'external-unexpanded-typing-primitive','Standard primitive occurring in selected exact provider typing/origin; declaration body not selected; not an extra public mathematical assumption.',q);alias[q.split('.')[-1]]=(i,q)
kw=set('theorem lemma def class structure instance variable let fun forall where noncomputable protected irreducible_def abbrev match with if then else Prop Type Set True False by volume_tac ∞ scoped open in Real NNReal ENNReal Module extends local private'.split())
unknown=set()
for pr in providers:
 if pr['kind']=='primary-source':
  # Every direct source cross-reference is inventoried; math formulas are not Lean calls.
  b=pathlib.Path(pr['path']).read_bytes();f=b[pr['start_utf8_byte0']:pr['end_utf8_byte0_exclusive']]
  for m in re.finditer(rb'href="#([^"]+)"',f):
   ref=m.group(1).decode();resolved={'S2.E7':'S51.J','A2.E13':'S51.B13'}.get(ref)
   if resolved:
    st=pr['start_utf8_byte0']+m.start(1);ci=len(callers);callers.append(dict(index0=ci,provider=pr['id'],caller_node=pr['node'],path=pr['path'],physical_line1=b[:st].count(b'\n')+1,start_utf8_byte0=st,end_utf8_byte0_exclusive=st+len(m.group(1)),token=ref,resolved_node=resolved,qualified_id=None,classification='source-internal-reference',compiled51call=False));edge(resolved,pr['node'],'source-reference','Literal selected primary cross-reference',ci)
  continue
 b=pathlib.Path(pr['path']).read_bytes();f=b[pr['start_utf8_byte0']:pr['end_utf8_byte0_exclusive']].decode();comment_spans=[(m.start(),m.end()) for m in re.finditer(r'/\-.*?\-/',f,re.S)]
 for m in re.finditer(r'[A-Za-z_α-ωΑ-Ω][\w\u2080-\u2089]*(?:\.[A-Za-z_α-ωΑ-Ω][\w\u2080-\u2089]*)*',f):
  t=m.group();st=pr['start_utf8_byte0']+len(f[:m.start()].encode());last=t.split('.')[-1];line=b[:st].count(b'\n')+1;entry=dict(provider=pr['id'],caller_node=pr['node'],path=pr['path'],physical_line1=line,start_utf8_byte0=st,end_utf8_byte0_exclusive=st+len(t.encode()),token=t)
  before=f[:m.start()].splitlines()[-1] if f[:m.start()].splitlines() else ''
  ownqid=next(x for x in nodes if x['id']==pr['node']).get('qualified_id');label=(ownqid and t==ownqid.split('.')[-1] and any(w in before for w in ['theorem ','def ','class ','structure ','abbrev '])) or (pr['id']=='candidate' and t=='gaussian_marginal_gradient_closable')
  if any(a<=m.start()<z for a,z in comment_spans):entry.update(classification='EXCLUDED-comment-token',resolved_node=None)
  elif label:entry.update(classification='declaration-label-not-call',resolved_node=None)
  elif (pr['node']=='D51.D' and last in ['domain','toFun']) or (pr['node']=='D51.prob' and last=='measure_univ'):entry.update(classification='generated-field-declaration-or-local-field-binding-not-call',resolved_node=None)
  elif t in kw or len(t)==1 or t.startswith('h') and len(t)<6 or t in ['_m','hη','hfi','f_nn','hfm','hf','hmn','h','mα','mβ','mγ','m0','m₀','m','hs','hfp','n','q','univ','pi','ofReal_eq_one','volume_tac','to_additive','simp','fun_prop'] and t not in alias:entry.update(classification='binder-local-or-language-symbol',resolved_node=None)
  elif t in alias or last in alias:
   ni,qi=alias.get(t,alias.get(last));
   if ni==pr['node']:entry.update(classification='own-declaration-label-or-recursive-context-not-ingredient',resolved_node=ni)
   else:
    ci=len(callers);cl='generated-field-reference' if ni.startswith('F51.') else ('definition-reference' if next(x for x in nodes if x['id']==ni)['kind'].find('definition')>=0 else 'typed-public-contract-reference')
    entry.update(classification=cl,resolved_node=ni,qualified_id=qi,caller_index0=ci);callers.append(dict(entry,index0=ci,compiled51call=False,provider_body_selected=pr['body_selected']));edge(ni,pr['node'],'definition-or-typing-reference','Exact selected token; no wrapper/selfnode resolution',ci)
  else:entry.update(classification='REQUIRES_CLASSIFICATION',resolved_node=None);unknown.add(t)
  lexemes.append(entry)
 # Important semantic notations get exact callers as well; these are actual primitives, not guessed wrapper declarations.
 for m in re.finditer(r'∫⁻|∫|=ᵐ|≤ᵐ|→ₗ\.',f):
  t=m.group();ni,qi={'∫⁻':('D51.lintegral','MeasureTheory.lintegral'),'∫':('D51.integral','MeasureTheory.integral'),'=ᵐ':('D51.AEeq','Filter.EventuallyEq'),'≤ᵐ':('D51.AEeq','Filter.EventuallyEq'),'→ₗ.':('D51.D','LinearPMap')}[t]
  if t=='≤ᵐ':ni='EXT.AEle';qi='Filter.Eventually';node(ni,'external-unexpanded-notation','AE pointwise nonnegativity along measure filter; not eventual equality.',qi)
  st=pr['start_utf8_byte0']+len(f[:m.start()].encode());ci=len(callers);entry=dict(index0=ci,provider=pr['id'],caller_node=pr['node'],path=pr['path'],physical_line1=b[:st].count(b'\n')+1,start_utf8_byte0=st,end_utf8_byte0_exclusive=st+len(t.encode()),token=t,resolved_node=ni,qualified_id=qi,classification='semantic-notation-reference',compiled51call=False,provider_body_selected=pr['body_selected']);callers.append(entry)
  if ni!=pr['node']:edge(ni,pr['node'],'semantic-notation-reference','Actual integral/AE/partial-linear-map notation contract',ci)
put('source-proof-graph.json',dict(schema_version='gaussian-marginal-sourcegraph51-v1',status='CREATOR_SOURCE_ONLY_AWAITING_DISTINCT_TOPOLOGY',edge_orientation='ingredient -> consumer; source mathematical/API/header graph only; no compiled51 call graph',nodes=nodes,edges=edges))
put('selected-providers.json',providers);put('source-coverage.json',dict(scope='Exhaustive physical row partition within exact selected fragments only, including terminal prefix byte limits; external/provider bodies not selected remain explicit boundaries',rows=coverage));put('caller-inventory.json',dict(scope='Each direct recognized named mathematical/type reference in selected provider contexts/definition bodies, plus primary crossreferences. Generated fields separate; no future Lean caller claims.',entries=callers));put('lexical-inventory.json',dict(scope='Every selected non-HTML identifier token; classifications include binder/local/language, declaration labels and direct resolved calls',entries=lexemes,requires_classification=sorted(unknown)))
put('input-bindings.json',dict(schema='sourcegraph51-rawLF-v1',files=[dict(path=str(R/k),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n'))) for k,b in cache.items()],historical_preread_paths=['pbps-after-macroscopic-preread51/source-contract.json','pbps-after-macroscopic-preread51/lease.json','pbps-after-macroscopic-preread51/run.json'],new_actual_lease='lease.json OPEN until finalizer; historical leases never rewritten'))
print('COUNTS',len(nodes),len(edges),len(providers),len(coverage),len(callers),len(lexemes));print('UNCLASSIFIED',sorted(unknown))
