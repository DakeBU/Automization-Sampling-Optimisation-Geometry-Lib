import pathlib,json,hashlib,re,copy,datetime
R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-sourcegraph55';H=O.parent/'pbps-rough-gradient-density-preread55';D=O.parent/'pbps-source-mean-gradient-domain-topology-overlay54';P=O.parent/'pbps-l2-macroscopic-mean-preproof55'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def readj(p):return json.loads(p.read_text(encoding='utf8'))
def write(n,d):(O/n).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
inputs=readj(O/'draft-input-bindings.json')
def pin(p,role):
 p=pathlib.Path(p);b=p.read_bytes();assert b'\r' not in lf(b)
 if not any(x['path']==str(p) for x in inputs):inputs.append({'path':str(p),'role':role,'raw_bytes':len(b),'lf_bytes':len(lf(b)),'raw_sha256':sha(b),'lf_sha256':sha(lf(b))})
 return b
candidate=pin(P/'prospective-statement.txt','exact prospective2526 only after primary freeze');assert len(lf(candidate))==2526 and sha(lf(candidate))=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
pin(P/'root.statement-proposal.json','prospective proposal status; no proof')
pin(O.parent/'next-ready-preread47/primary-pbps.raw.snapshot.html','fixed PBPSv1 primary whole byte pin; selected slices only')
for f in ['source-proof-graph.json','selected-providers.json','run.json','lease.json']:pin(D/f,'previous own source-only primitive/repair carrier; no implementation54 or verdict read')
dg=readj(D/'source-proof-graph.json');dp=readj(D/'selected-providers.json');dn={x['id']:x for x in dg['nodes']}
registry={};registrycontext=[]
for pr in dp:
 n=dn.get(pr['node']);q=n.get('qualified_id') if n else None
 if q and pr['kind'] not in ['primary-source','prospective-statement','opaque-parent-public-header','incidental-excluded']:
  if 'context' in pr['id'] or pr['kind']=='context-public':registrycontext.append((q,pr))
  else:registry.setdefault(q,pr)
(O/'final-fragments').mkdir(exist_ok=True)
nodes=[];edges=[];providers=[];coverage=[];callers=[];lex=[];external=[]
def node(nid,kind,contract,q=None):
 if not any(x['id']==nid for x in nodes):nodes.append({'id':nid,'kind':kind,'contract':contract,'qualified_id':q,'compiled55':False,'proof_body_expanded':False})
def edge(a,b,kind,reason,**kw):
 e={'id':'E55.'+str(len(edges)),'ingredient':a,'consumer':b,'kind':kind,'reason':reason,'compiled55call':False};e.update(kw);edges.append(e)
qid={}
def qnode(q,kind='external-unexpanded-primitive'):
 if q not in qid:
  nid='D55.'+re.sub(r'[^\w]+','_',q);qid[q]=nid;node(nid,kind,'Exact selected public primitive '+q+'; proof/deeper implementation unexpanded',q)
 return qid[q]
def capture(pid,nid,path,lo,hi,kind='public-header',semantic=False,headertrim=True,**extra):
 data=pin(path,'selected public API/definition/context source; other bytes pin only');a=data.splitlines(keepends=True);start=sum(map(len,a[:lo-1]));end=sum(map(len,a[:hi]));frag=data[start:end]
 if headertrim:
  # Ignore := inside balanced default/priority slots and actual let-expression binders.
  depth=0;k=-1;i=0
  while i<len(frag)-1:
   ch=frag[i]
   if ch in b'([{':depth+=1
   elif ch in b')]}':depth-=1
   if frag[i:i+2]==b':=' and depth==0:
    line=frag[frag.rfind(b'\n',0,i)+1:i]
    if not re.match(rb'\s*let\b',line):k=i;break
   i+=1
  frag=frag[:k] if k>=0 else frag;end=start+len(frag)
 # Actual final selected line derives from byte endpoint after header trim.
 endline=lo+frag.count(b'\n')-(1 if frag.endswith(b'\n') else 0);endline=max(lo,endline)
 (O/'final-fragments'/(pid+'.raw.txt')).write_bytes(frag);(O/'final-fragments'/(pid+'.lf.txt')).write_bytes(lf(frag))
 v={'id':pid,'node':nid,'kind':kind,'path':str(path),'physical_lines1':[lo,endline],'start_utf8_byte0':start,'end_utf8_byte0_exclusive':end,'fragment_raw_sha256':sha(frag),'fragment_lf_sha256':sha(lf(frag)),'whole_raw_sha256':sha(data),'whole_lf_sha256':sha(lf(data)),'definition_semantics_selected':semantic,'proof_body_selected':False,'body_expansion_boundary':True};v.update(extra);providers.append(v);return v

primary=readj(O/'primary-selected-providers.before-signature.json');oldcov=readj(O/'primary-selected-coverage.before-signature.json')
for pr in primary:
 nid='S55.'+pr['id'].split('.',1)[1];node(nid,'primary-source-consumer' if 'consumer' in nid else 'primary-source','Exact fixed PBPS source selected unit; no compiled55 credit')
 v=dict(pr,node=nid,kind='primary-source',definition_semantics_selected=False,proof_body_selected=False,body_expansion_boundary=True);providers.append(v)
for row in oldcov:
 row=dict(row);row['path']=str(O.parent/'next-ready-preread47/primary-pbps.raw.snapshot.html');row['utf8_column_start0']=0;row['utf8_column_end0_exclusive']=row['utf8_byte_end0_exclusive']-row['utf8_byte_start0'];coverage.append(row)
target='T55';node(target,'prospective-target','Actual all-L2 same-law macroscopic mean bridge; statement typed/sealed status handled separately','AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean.actual_macroscopic_l2_mean')
capture('prospective',target,P/'prospective-statement.txt',1,len(candidate.splitlines()),'prospective-statement',headertrim=False)

# Actual provider plan is after frozen primary and before future implementation55.
slots=readj(O/'public-provider-slots.current.draft.json')
drop=['P55.conditionalUnique','P55.variance-scope','P55.conditionalUniqueScope']
for s in slots:
 if s['id'] in drop:continue
 q=s['qualified_id'];nid=qnode(q,'opaque-admitted-producer' if s['id'] in ['P55.energy50','P55.core51','P55.reflection','P55.reflectionLaw'] else 'external-unexpanded-primitive')
 capture(s['id'],nid,s['path'],s['physical_lines1'][0],s['physical_lines1'][1],kind='opaque-producer-public-header' if s['id'] in ['P55.energy50','P55.core51','P55.reflection','P55.reflectionLaw'] else 'public-definition' if s['body_semantics_expanded'] else 'public-header',semantic=s['body_semantics_expanded'],headertrim=not s['body_semantics_expanded'])

# Necessary explicit ambient scopes, not blanket library expansion.
m=R/'.lake/packages/mathlib/Mathlib'
scope_specs=[('gaussian-scope','AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean',24,25),('pullback-context','MeasureTheory.Lp.compMeasurePreservingₗᵢ',m/'MeasureTheory/Function/LpSpace/Basic.lean',67,68),('pullback-measure-context','MeasureTheory.Lp.compMeasurePreservingₗᵢ',m/'MeasureTheory/Function/LpSpace/Basic.lean',558,558),('pullback-scalar-context','MeasureTheory.Lp.compMeasurePreservingₗᵢ',m/'MeasureTheory/Function/LpSpace/Basic.lean',621,621),('conditional-projection-context','MeasureTheory.condExpL2',m/'MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',44,48),('conditional-projection-measure-context','MeasureTheory.condExpL2',m/'MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',61,61),('conditional-integral-context','MeasureTheory.Integrable.condKernel_ae',m/'Probability/Kernel/Disintegration/Integral.lean',219,221),('conditional-unique-context','ProbabilityTheory.eq_condKernel_of_measure_eq_compProd',m/'Probability/Kernel/Disintegration/Unique.lean',34,39),('variance-context','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance',R/'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean',21,22),('Lp-complete-context','MeasureTheory.Lp.instCompleteSpace',m/'MeasureTheory/Function/LpSpace/Complete.lean',23,23),('Lp-complete-add-context','MeasureTheory.Lp.instCompleteSpace',m/'MeasureTheory/Function/LpSpace/Complete.lean',108,108),('L2-inner-context','MeasureTheory.L2.inner_def',m/'MeasureTheory/Function/L2Space.lean',102,103),('isometry-closed-context','Isometry.isClosedEmbedding',m/'Topology/MetricSpace/Isometry.lean',204,204),('inverse-range-context','LinearIsometry.equivRange',m/'Analysis/Normed/Operator/LinearIsometry.lean',35,43)]
scope_specs[-1]=('inverse-range-context','LinearIsometry.equivRange',m/'Analysis/Normed/Operator/LinearIsometry.lean',35,47)
scope_specs.extend([('stdGaussian-context','ProbabilityTheory.stdGaussian',m/'Probability/Distributions/Gaussian/Multivariate.lean',55,56),('lpMeas-context','MeasureTheory.lpMeas',m/'MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',61,68),('Integrable-context','MeasureTheory.Integrable',m/'MeasureTheory/Function/L1Space/Integrable.lean',48,50),('mono-exponent-context','MeasureTheory.MemLp.mono_exponent',m/'MeasureTheory/Function/LpSeminorm/CompareExp.lean',28,30),('projection-primitive-context','Submodule.orthogonalProjectionOnto',m/'Analysis/InnerProductSpace/Projection/Basic.lean',38,40),('projection-submodule-context','Submodule.orthogonalProjectionOnto',m/'Analysis/InnerProductSpace/Projection/Basic.lean',52,52),('projection-existence-context','Submodule.orthogonalProjectionOnto',m/'Analysis/InnerProductSpace/Projection/Basic.lean',110,110)])
for pid,q,path,lo,hi in scope_specs:capture(pid,qnode(q),path,lo,hi,'inherited-public-context',headertrim=False)
additional=[('MeasureTheory.Measure.condKernel','Probability/Kernel/Disintegration/StandardBorel.lean',360,362,False),('MeasureTheory.Lp.memLp','MeasureTheory/Function/LpSpace/Basic.lean',185,185,False),('MeasureTheory.MemLp.mono_exponent','MeasureTheory/Function/LpSeminorm/CompareExp.lean',115,116,False),('MeasureTheory.memLp_one_iff_integrable','MeasureTheory/Function/L1Space/Integrable.lean',66,66,False),('real_inner_self_eq_norm_sq','Analysis/InnerProductSpace/Basic.lean',396,396,False)]
additional.extend([('MeasureTheory.MeasurePreserving','Dynamics/Ergodic/MeasurePreserving.lean',45,49,False),('Isometry','Topology/MetricSpace/Isometry.lean',40,40,False),('IsClosedEmbedding','Topology/Defs/Induced.lean',159,159,False),('Submodule.orthogonalProjectionOnto','Analysis/InnerProductSpace/Projection/Basic.lean',113,113,False),('MeasureTheory.Lp.compMeasurePreserving','MeasureTheory/Function/LpSpace/Basic.lean',561,562,False),('MeasureTheory.MemLp.comp_measurePreserving','MeasureTheory/Function/LpSeminorm/Basic.lean',880,881,False)])
for q,rel,lo,hi,semantic in additional:capture('api-'+q.replace('.','_'),qnode(q),m/rel,lo,hi,semantic=semantic)
capture('Gaussian-posterior-public',qnode('AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel','opaque-admitted-producer'),R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',35,42,kind='opaque-producer-public-header')
capture('Gaussian-posterior-context',qnode('AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel'),R/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',29,30,kind='inherited-public-context',headertrim=False)
capture('MeasurePreserving-definition',qnode('MeasureTheory.MeasurePreserving'),m/'Dynamics/Ergodic/MeasurePreserving.lean',45,48,kind='public-definition',semantic=True,headertrim=False)
capture('condKernel-scope',qnode('MeasureTheory.Measure.condKernel'),m/'Probability/Kernel/Disintegration/StandardBorel.lean',75,76,'inherited-public-context',headertrim=False)
capture('condKernel-finite',qnode('MeasureTheory.Measure.condKernel'),m/'Probability/Kernel/Disintegration/StandardBorel.lean',356,356,'inherited-public-context',headertrim=False)
prelude=pathlib.Path('C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Prelude.lean')
capture('Prod-carrier',qnode('Prod'),'C:/Users/admin/.elan/toolchains/leanprover--lean4---v4.33.0/src/lean/Init/Prelude.lean',563,563,headertrim=False)
capture('Prod-fst-field',qnode('Prod.fst','generated-structure-field'),prelude,569,569,headertrim=False)
capture('Prod-snd-field',qnode('Prod.snd','generated-structure-field'),prelude,571,571,headertrim=False)
edge(qnode('Prod'),qnode('Prod.fst'),'generated-field-provenance','Actual Prod declaration carrier, field access not proof call')
edge(qnode('Prod'),qnode('Prod.snd'),'generated-field-provenance','Actual Prod declaration carrier, field access not proof call')

# Source mathematics authored independently; every ingredient has an explicit edge.
author={
'A55.laws':'Actual50 source Gibbs/Gaussian laws, probabilities, literal every-y S and actual disintegration; no supplied normalizer.',
'A55.posterior':'Internal R needed: actual50 posterior disintegration and all-L2 ReflectionL2 normalized Gaussian posterior, aligned AE by true uniqueness. No returned R does not erase this ingredient.',
'A55.marginals':'Lambda.fst=nu from50; Lambda.snd=nu derived from actual F#J=J and map/projection algebra. Both sides SAME law.',
'A55.M':'Canonical actual snd pullback linear isometry; AE-J Mu=u o snd; complete L2 input gives closed M range. E finite does not imply finite L2.',
'A55.dense':'51 dense original smoothcompact input graph gives dense observers, using50 compact coherence on SAME M/P/A/S. Only density/full core consumed; no54 or gradient mean membership.',
'A55.invariant':'Continuity plus dense compact identities produces PM=M and A(range M) subset range M. Real internal source-bookkeeping obligation.',
'A55.T':'Use M.equivRange inverse on A M to produce one bounded linear T before forall u; MT=AM, norm Tu<=norm u by actual projection contraction and true U isometry.',
'A55.mean':'All-L2 ReflectionL2 P formula, internal posterior AE alignment, U full class reflection and actual S reflected law imply Tu AE-nu literal S integral. AE laws transfer means/classes only, never derivatives.',
'A55.fibers':'u real L2 gives u L1 and u² L1; Lambda.snd=nu and true Lambda disintegration give AE-nu fiber L1 and square L1 for actual S. No every-y rough integrability.',
'A55.variance':'Actual centered-square variance plus finite probability and true fiber L1/square L1. Integrate square expansion/Fubini on SAME Lambda/nu; produces integrable variance and integralVar=norm u²-norm Tu², no caller certificate.',
'A55.defect':'Actual50 block defect on PMu=Mu, canonical M norm equality and MT=AM give norm BMu²=norm u²-norm Tu²; combine with genuine integral variance.',
'A55.ambient':'Internally real L2 spaces carry normed Hilbert/complete structures, finite probability, measurable pullback, StandardBorel E and Nonempty from zero; deep instance implementation externally unexpanded, no public premise.',
'X55.rough':'Downstream B13 all-L2 weakH1/closed-gradient/difference-limit route and54 compact graph membership excluded from55 producer.',
'X55.Gamma':'Gamma positive-root, full hypocoercive/mixing/dynamics/halfturn/main/query cost remain separate excluded consumers.'}
for nid,c in author.items():node(nid,'excluded-residual' if nid.startswith('X55') else 'authored-internal-source-obligation',c)
routes=[('S55.standing','A55.laws','source-hypothesis'),('S55.actual-law','A55.laws','source-law'),(qnode('AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks'),'A55.laws','opaque-real-producer'),('A55.laws','A55.posterior','internal-posterior'),(qnode('AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionL2.actual_reflection_block_identities'),'A55.posterior','opaque-real-producer'),(qnode('ProbabilityTheory.eq_condKernel_of_measure_eq_compProd'),'A55.posterior','AE-kernel-alignment'),('A55.laws','A55.marginals','same-law'),(qnode('AutoSamplingTheory.ExampleCases.ProximalBPS.GaussianReflection.reflection_preserves_augmentation'),'A55.marginals','true-reflection'),('S55.reflection','A55.marginals','source-reflection'),(qnode('MeasureTheory.Measure.snd'),'A55.M','definition-semantics'),(qnode('MeasureTheory.Lp.compMeasurePreservingₗᵢ'),'A55.M','actual-pullback-producer'),(qnode('MeasureTheory.Lp.coeFn_compMeasurePreserving'),'A55.M','actual-AE-representative'),(qnode('MeasureTheory.Lp.norm_compMeasurePreserving'),'A55.M','actual-isometry-norm'),(qnode('Isometry.isClosedEmbedding'),'A55.M','closed-range'),(qnode('MeasureTheory.Lp.instCompleteSpace'),'A55.M','actual-completeness'),('A55.laws','A55.dense','same-law-compact'),(qnode('AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient.gaussian_marginal_gradient_closable'),'A55.dense','dense-core-opaque'),('S55.projection','A55.invariant','source-projection'),('A55.dense','A55.invariant','actual-density-lift'),('A55.M','A55.invariant','closed-macroscopic-range'),('S55.block-definition','A55.invariant','source-block-definition'),('A55.invariant','A55.T','actual-invariance'),(qnode('LinearIsometry.equivRange'),'A55.T','inverse-isometry-range'),(qnode('MeasureTheory.norm_condExpL2_coe_le'),'A55.T','actual-projection-contraction'),('A55.posterior','A55.mean','actual-posterior-needed'),('A55.T','A55.mean','coherent-mean-class'),('A55.marginals','A55.mean','same-nu-AE'),('S55.rough-mean-variance','A55.mean','source-B9-mean'),('S55.compact-density','A55.mean','literal-source-S-definition'),(qnode('MeasureTheory.Lp.memLp'),'A55.fibers','real-L2-domain'),(qnode('MeasureTheory.MemLp.mono_exponent'),'A55.fibers','finite-L2-to-L1'),(qnode('MeasureTheory.memLp_one_iff_integrable'),'A55.fibers','actual-L1'),(qnode('MeasureTheory.MemLp.integrable_sq'),'A55.fibers','actual-square-L1'),('A55.marginals','A55.fibers','both-marginals'),(qnode('MeasureTheory.Measure.IsCondKernel'),'A55.fibers','actual-disintegration'),(qnode('MeasureTheory.Integrable.condKernel_ae'),'A55.fibers','actual-AE-fiber'),('A55.posterior','A55.fibers','AE-kernel-version'),('A55.fibers','A55.variance','actual-finite-fiber-domains'),('A55.mean','A55.variance','true-conditional-mean'),(qnode('AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance'),'A55.variance','actual-centered-square-definition'),(qnode('MeasureTheory.Integrable.integral_condKernel'),'A55.variance','actual-integrable-conditional-mean'),(qnode('MeasureTheory.L2.inner_def'),'A55.variance','actual-L2-square-integral'),(qnode('real_inner_self_eq_norm_sq'),'A55.variance','true-real-norm-square'),('A55.T','A55.defect','same-MT-AM'),('A55.invariant','A55.defect','PM-fixed'),('A55.M','A55.defect','canonical-M-norm'),('A55.laws','A55.defect','real-block-defect'),('S55.rough-mean-variance','A55.defect','source-B9-variance'),('A55.variance','A55.defect','integrated-variance'),('A55.defect','X55.rough','genuine-downstream-source-consumer'),('S55.rough-consumer','X55.rough','source-full-rough-boundary'),('S55.smooth-energy-consumer','X55.rough','source-C2-limit-consumer')]
for a,b,k in routes:edge(a,b,k,'Independent primary/API reconstruction; internally produced obligation, not compiled55 call')
edge(qnode('AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel'),'A55.posterior','opaque-real-posterior-producer','Actual public R with literal posterior and real disintegration; ReflectionL2 header alone omits this output')
edge(qnode('MeasureTheory.MeasurePreserving'),'A55.M','actual-measurable-map-law','Canonical snd measurable and J.map snd=nu; true measure-preserving certificate produced internally')
for a in ['A55.laws','A55.marginals','A55.M','A55.T','A55.mean','A55.fibers','A55.variance','A55.defect','A55.ambient']:edge(a,target,'produced-conclusion','Actual returned object/domain/coherence, not extra public hypothesis')
for a in ['A55.M','A55.T','A55.fibers','A55.variance']:edge('A55.ambient',a,'internal-ambient-contract','Standard real/L2/Borel/finite-probability slots internally derived')

# Token provider registry uses actual old checked public identities, not guessed wrapper calls.
alias={'variance':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.Poincare.variance','condKernel':'MeasureTheory.Measure.condKernel','IsCondKernel':'MeasureTheory.Measure.IsCondKernel','snd':'MeasureTheory.Measure.snd','fst':'MeasureTheory.Measure.fst','map':'MeasureTheory.Measure.map','comap':'MeasurableSpace.comap','subtypeL':'Submodule.subtypeL','toContinuousLinearMap':'LinearIsometry.toContinuousLinearMap','IsClosed':'LinearPMap.IsClosed','IsClosable':'LinearPMap.IsClosable','closure':'LinearPMap.closure','graph':'LinearPMap.graph','comap_le':'Measurable.comap_le'}
for q in list(registry)+list(qid):alias.setdefault(q,q);alias.setdefault(q.split('.')[-1],q)
alias.update({'UniformSpace':'UniformSpace','Module':'Module','Norm':'Norm','Star':'Star','star':'Star.star'})
alias.update({'MeasurePreserving':'MeasureTheory.MeasurePreserving','orthogonalProjectionOnto':'Submodule.orthogonalProjectionOnto','compMeasurePreserving':'MeasureTheory.Lp.compMeasurePreserving','comp_measurePreserving':'MeasureTheory.MemLp.comp_measurePreserving','toLinearMap':'LinearIsometry.toLinearMap','LinearMap.range':'LinearMap.range'})
keywords=set('theorem def noncomputable irreducible_def protected class structure instance where Prop Type variable namespace open scoped local notation fun let in by haveI inferInstance forall Exists Fact extends True False Set'.split())
keywords.update('abbrev add_decl_doc alias attr irreducible lemma section semiOutParam simps wikidata apply_coe _ℝ SL ₗᵢ ₛₗᵢ'.split())
keywords.discard('Set');keywords.discard('Fact')
localnames=set('E F G R S T U P A B D V J Lambda alpha beta eta f g x y u v p q c a hf hμ hη hα hαβ hV hH hβη hpq hm μ ν Λ α β η ρ κ ε Ω 𝕜 𝕜\' E\' σ₁₂ σ₂₁ σ₁₃ σ₃₁ σ₁₄ σ₄₁ σ₂₃ σ₃₂ σ₂₄ σ₄₂ σ₃₄ σ₄₃ R₂ R₃ R₄ E₂ E₃ E₄ 𝓕 μb m m0 mα mβ mΩ s t hp_ne_zero hp_ne_top hκ hf_int hp u v w'.split())
localnames.update(["G'",'_hη','h_mem_ℒp','hfq','hg','mγ','ρCond'])
localnames.update(['μa',"ε'","ε''",'δ'])
# These are public type/class hierarchy slots with implementation outside one-hop scope, never local binders.
externaltypes=set('RCLike NormedRing NormedField IsBoundedSMul IsFiniteKernel IsSFiniteKernel StandardBorelSpace Nonempty Semiring Ring CommRing DivisionRing NormedSpace SeminormedAddCommGroup SeminormedAddGroup Inner AddCommGroup AddCommMonoid OuterMeasure MeasureSpace Filter UniformSpace MetricSpace PseudoMetricSpace EMetricSpace PseudoEMetricSpace NormedSpace DistribMulAction Star RingHomInvPair TopologicalSpace ContinuousAdd ContinuousSMul ContinuousENorm HSMul SMul Add One Zero ContinuousLinearMapClass LinearMap RingHomInvPair'.split())
externaltypes.update('AddCommSemigroup AddGroup AddGroupWithOne AddMonoid AddSubmonoid CommMonoid CommSemigroup DenselyNormedField Dist Distrib DivInvMonoid IsDedekindFiniteMonoid MeasurableSpace.CountablyGenerated Monoid MonoidWithZero MulAction NNRatCast NonAssocSemiring NonUnitalSemiring Nontrivial NormedAlgebra RatCast RingHomCompTriple SetLike StarRing SubMulAction'.split())
externaltypes.update(['IsEmbedding','Fact','ENorm','ESeminormedAddMonoid','Submodule.HasOrthogonalProjection'])
rx=re.compile(r'[^\W\d]\w*(?:\.[^\W\d]\w*)*\'?')
captured_q={n['qualified_id'] for n in nodes if n.get('qualified_id')}
def ensure(q):
 nid=qnode(q)
 if any(p['node']==nid for p in providers):return nid
 if q in registry:
  pr=registry[q];lo,hi=pr['physical_lines1']
  if q=='Submodule':hi=42
  v=capture('primitive-'+q.replace('.','_'),nid,pr['path'],lo,hi,kind='external-unexpanded-public-primitive',headertrim=True)
  if q=='Measurable.comap_le':
   providers.pop();capture('primitive-Measurable_comap_le',nid,pr['path'],191,191,kind='generated-alias-carrier',headertrim=False)
   edge(ensure('measurable_iff_comap_le'),nid,'generated-alias-definition','Actual alias carrier191; sibling output name not a mathematical call')
  for scopeq,scopepr in registrycontext:
   if scopeq==q and scopepr['id'] not in ['adapter-context','adapter-hilbert-context'] and not any(x['id']=='inherited-'+scopepr['id'] for x in providers):
    capture('inherited-'+scopepr['id'],nid,scopepr['path'],scopepr['physical_lines1'][0],scopepr['physical_lines1'][1],kind='inherited-public-context',headertrim=False)
  if q=='HasCompactSupport':
   # Generation carrier is selected whole; body217 excluded explicitly, not implementation call inventory.
   providers.pop();v=capture('primitive-HasCompactSupport',nid,pr['path'],213,217,kind='generated-additive-carrier',headertrim=False,carrier='HasCompactMulSupport',generated_output='HasCompactSupport',excluded_body_lines=[217]);
   carrier=qnode('HasCompactMulSupport');edge(carrier,nid,'generated-additive-definition','Actual to_additive carrier213-217, no new source hypothesis');ensure('HasCompactMulSupport')
  return nid
 # Explicit deep hierarchy boundary only; no guessed provider header or theorem producer.
 external.append({'qualified_or_scope_token':q,'node':nid,'reason':'Exact named type/class in selected inherited header; deeper provider/instance implementation explicitly outside bounded expansion','provider_selected':False})
 return nid
def classify(token,consumer,providerid,decl):
 if token==decl:return 'declaration-name-binding',consumer,[]
 if providerid=='primitive-Measurable_comap_le' and token in ['Measurable.comap_le','Measurable.of_comap_le']:return 'generated-alias-name-binding',None,[]
 if providerid=='MeasurePreserving-definition' and token in ['measurable','map_eq']:return 'structure-field-declaration-not-mathematical-call',None,[]
 if token.startswith('Q') and token[1:].isdigit():return 'attribute-metadata-not-mathematical-call',None,[]
 if token=='Measurable.of_comap_le':return 'generated-alias-name-binding',None,[]
 if token in keywords:return 'bound-identifier-or-syntax',None,[]
 if token=='to_additive':return 'generation-attribute-syntax',None,[]
 if token in alias:
  q=alias[token];return 'primitive-public-reference',ensure(q),[]
 if '.' in token:
  base,tail=token.rsplit('.',1)
  if tail in alias:
   primary=ensure(alias[tail]);parts=[]
   if tail=='comap_le' and base=='measurable_snd':parts=[ensure('measurable_snd')]
   if tail=='graph' and base.endswith('.closure'):parts=[ensure('LinearPMap.closure')]
   return 'primitive-public-reference',primary,parts
 if token in externaltypes:
  return 'explicit-external-unexpanded-type-hierarchy-boundary',ensure(token),[]
 if token in localnames or len(token)==1 or token in ['volume_tac','re','𝓝','support','mulTSupport']:
  return 'bound-identifier-or-syntax' if token not in ['volume_tac','mulTSupport'] else 'explicit-external-unexpanded-elaborator-or-definition-boundary',None,[]
 return 'UNRESOLVED',None,[]

processed=set();unresolved=[]
while len(processed)<len(providers):
 for pr in list(providers):
  if pr['id'] in processed:continue
  processed.add(pr['id']);data=pathlib.Path(pr['path']).read_bytes();frag=data[pr['start_utf8_byte0']:pr['end_utf8_byte0_exclusive']]
  if pr['kind']=='primary-source':
   # Exact selected href occurrences as source reference/consumer edges; source math binders separately hypothesis map.
   for match in re.finditer(rb'href="(#[^"]+)"',frag):
    t=match.group(1).decode();at=pr['start_utf8_byte0']+match.start(1);end=pr['start_utf8_byte0']+match.end(1);nid='X55.href.'+re.sub(r'\W','_',t);node(nid,'source-reference-boundary','Exact printed internal/cited source reference '+t);line=1+data[:at].count(b'\n');col=at-(data.rfind(b'\n',0,at)+1)
    c={'index0':len(callers),'provider':pr['id'],'consumer':pr['node'],'token':t,'physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':at,'utf8_byte_end0_exclusive':end,'utf8_column_start0':col,'utf8_column_end0_exclusive':col+end-at,'classification':'source-direct-reference','resolution':nid};callers.append(c);edge(nid,pr['node'],'source-reference','Exact physical printed reference; source boundary not compiled dependency',caller_index0=c['index0'])
   continue
  lines=frag.splitlines(keepends=True);start=pr['start_utf8_byte0'];physical=pr['physical_lines1'][0];comment=False
  fulltext=frag.decode('utf8'); dm=re.search(r'\b(?:theorem|lemma|def|class|structure|instance)\s+(?:_root_\.)?([^\s(:]+)',fulltext);decl=dm.group(1) if dm else None
  for k,lb in enumerate(lines):
   line=physical+k;lineb=lb.rstrip(b'\r\n');s=lineb.decode('utf8');excluded=line in pr.get('excluded_body_lines',[])
   stripped=s.strip();doc=comment or stripped.startswith(('--','/--','/-!'))
   if stripped.startswith(('/--','/-!')) and '-/' not in stripped:comment=True
   if '-/' in stripped and comment:doc=True;comment=False
   if not any(r['provider']==pr['id'] and r['physical_line1']==line for r in coverage):coverage.append({'provider':pr['id'],'path':pr['path'],'physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':start,'utf8_byte_end0_exclusive':start+len(lineb),'utf8_column_start0':0,'utf8_column_end0_exclusive':len(lineb),'classification':'EXCLUDED' if doc or excluded or not stripped else 'NODE','node':None if doc or excluded or not stripped else pr['node'],'reason':'Documentation/layout or explicitly unexpanded carrier body' if doc or excluded or not stripped else 'Actual selected entire public header/context/definition','raw_sha256':sha(lineb)})
   if doc or excluded:start+=len(lb);continue
   if pr['id']=='primitive-HasCompactSupport' and line in [213,214,215]:
    if line==213:
     at=start+s.index('to_additive');lex.append({'index0':len(lex),'provider':pr['id'],'consumer':pr['node'],'token':'to_additive','physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':at,'utf8_byte_end0_exclusive':at+11,'utf8_column_start0':at-start,'utf8_column_end0_exclusive':at-start+11,'classification':'generation-attribute-syntax','resolution':None,'composite_projections':[]})
    start+=len(lb);continue
   for mm in rx.finditer(s):
    t=mm.group();at=start+len(s[:mm.start()].encode('utf8'));end=start+len(s[:mm.end()].encode('utf8'));cl,res,parts=classify(t,pr['node'],pr['id'],decl)
    l={'index0':len(lex),'provider':pr['id'],'consumer':pr['node'],'token':t,'physical_line1':line,'physical_line0':line-1,'utf8_byte_start0':at,'utf8_byte_end0_exclusive':end,'utf8_column_start0':at-start,'utf8_column_end0_exclusive':end-start,'classification':cl,'resolution':res,'composite_projections':parts};lex.append(l)
    if cl=='UNRESOLVED':unresolved.append(l)
    if cl=='primitive-public-reference' or cl=='explicit-external-unexpanded-type-hierarchy-boundary':
     c=dict(l);c['index0']=len(callers);callers.append(c);edge(res,pr['node'],'public-header-or-context-reference' if cl=='primitive-public-reference' else 'explicit-external-type-slot','Actual named header/context reference; not implementation call',caller_index0=c['index0'])
     for part in parts:edge(part,pr['node'],'composite-definition-reference','Actual composite projection context; closure/graph or measurable_snd/comap_le distinct',caller_index0=c['index0'])
   start+=len(lb)

graph={'schema_version':'bounded-source-proof-graph55/v1','status':'SOURCE_ONLY_PROSPECTIVE_NOT_SELF_ADMITTED','edge_orientation':'ingredient -> consumer; named source/provider calls and internal obligations, not compiled55 edges','nodes':nodes,'edges':edges,'source_expansion_boundary':'Opaque actual50/51/ReflectionL2/GaussianReflection proofs. Public one-hop headers/necessary scopes selected; explicit deep type/instance expansion boundaries. No54 proof, full roughH1/Gamma/main/cost.','compiled_graph_created':False,'candidate_LF_sha256':sha(lf(candidate)),'primary_before_candidate_freeze_sha256':sha((O/'primary-before-signature.freeze.json').read_bytes()),'implementation55_seen':False,'topology_admitted':False}
write('source-proof-graph.json',graph);write('selected-providers.json',providers);write('source-coverage.json',coverage);write('caller-inventory.json',callers);write('lexical-inventory.json',lex);write('selected-token-inventory.json',lex);write('external-unexpanded-boundaries.json',external);write('unresolved-lexemes.draft.json',unresolved);write('input-bindings.json',inputs)
write('counts.json',{'nodes':len(nodes),'edges':len(edges),'providers':len(providers),'coverage':len(coverage),'callers':len(callers),'lexemes':len(lex),'unresolved':len(unresolved),'external_deep_boundaries':len(external)})
print(json.dumps({'counts':readj(O/'counts.json'),'unresolved_unique':sorted({x['token'] for x in unresolved})}))
