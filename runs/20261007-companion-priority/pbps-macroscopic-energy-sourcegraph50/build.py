# coding: utf-8
import pathlib, json, hashlib, copy, re, datetime, sys
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib'); BASE=ROOT/'runs/20261007-companion-priority'
OUT=BASE/'pbps-macroscopic-energy-sourcegraph50'; OLD=BASE/'pbps-outer-gradient-topology-overlay49'
PRE=BASE/'pbps-macroscopic-energy-preproof50'
PRIMARY=BASE/'next-ready-preread47/primary-pbps.raw.snapshot.html'
def sha(x): return hashlib.sha256(x).hexdigest()
def lf(x): return x.replace(b'\r\n',b'\n')
def readj(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def writej(name,x): (OUT/name).write_bytes((json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 b=p.read_bytes(); return dict(path=str(p),raw_sha256=sha(b),lf_sha256=sha(lf(b)),raw_bytes=len(b),lf_bytes=len(lf(b)))
inputs=[]
def snap(p,label):
 b=p.read_bytes(); (OUT/(label+'.raw')).write_bytes(b);(OUT/(label+'.lf')).write_bytes(lf(b));inputs.append(dict(pin(p),snapshot=label));return b
for rel,label in [('prospective-statement.txt','candidate'),('root.statement-proposal.json','proposal'),('parent-public-contracts.json','parent-contracts'),('statement-seals.accepted.json','statement-seal')]: snap(PRE/rel,label)
for rel,label in [('pbps-after-energy-preread50/sourcecontract.json','historical-preread50-contract'),('pbps-after-energy-preread50/run.json','historical-preread50-run'),('pbps-after-energy-preread50/lease.json','historical-preread50-lease'),('phase-pbps-primary-preread50/primary.contract.json','independent-primary50-contract'),('phase-pbps-primary-preread50/reviewer.primary.lease.json','independent-primary50-lease'),('pbps-outer-gradient-source-topology-review49/source-topology-review.repaired.json','accepted49-source-topology'),('pbps-outer-gradient-source-topology-review49/reviewer.topology.repaired.lease.json','accepted49-source-topology-lease'),('pbps-outer-gradient-source-topology-review49/source-topology-review.json','original49-negative'),('pbps-outer-gradient-topology-overlay49/run.json','historical49-overlay-run'),('pbps-outer-gradient-topology-overlay49/lease.json','historical49-overlay-lease')]: snap(BASE/rel,label)
seal=readj(PRE/'statement-seals.accepted.json'); contracts=readj(PRE/'parent-public-contracts.json'); candidate=lf((PRE/'prospective-statement.txt').read_bytes())
assert len(candidate)==2907 and sha(candidate)=='478a899effcc46585270420c4db9c42052a5fcfe3adfd8098ea9548d26c61170'
assert seal['signatures'][0]['signature_lf_sha256']==sha(candidate)
oldgraph=readj(OLD/'source-proof-graph.after.json'); graph=copy.deepcopy(oldgraph)
for filename,label in [('source-proof-graph.after.json','inherited49-graph'),('source-coverage.after.json','inherited49-coverage'),('caller-inventory.after.json','inherited49-callers'),('selected-token-inventory.after.json','inherited49-tokens'),('selected-providers.after.json','inherited49-providers'),('original-primary-balanced-inventory.json.lf','inherited49-primary-inventory')]: snap(OLD/filename,label)
oldcoverage=readj(OLD/'source-coverage.after.json'); oldcallers=readj(OLD/'caller-inventory.after.json'); oldtokens=readj(OLD/'selected-token-inventory.after.json'); oldproviders=readj(OLD/'selected-providers.after.json')
oldanchors=readj(OLD/'original-primary-balanced-inventory.json.lf')['anchors']
raw=PRIMARY.read_bytes(); text=raw.decode(); assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
inputs.append(dict(pin(PRIMARY),snapshot='existing immutable primary47; no duplicate full snapshot'))
rawlines=raw.splitlines(keepends=True); lineoffsets=[0]
for line in rawlines: lineoffsets.append(lineoffsets[-1]+len(line))
charstarts=[0]
for m in re.finditer('\n',text): charstarts.append(m.end())
selected_ids=['A2.E1','A2.E2','A2.SS1.p1.4','A2.SS1.p1.5','A2.SS1.p2.1','A2.E3','A2.SS1.p2.2','A2.SS1.p3.1','A2.E4','A2.SS1.p3.2','A2.Ex3','A2.SS1.p3.3','A2.E5']
class Balanced(HTMLParser):
 def __init__(self): super().__init__(convert_charrefs=False); self.stack=[]; self.results={}
 def position_offset(self): l,c=self.getpos(); return charstarts[l-1]+c
 def handle_starttag(self,tag,attrs):
  if tag in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'): return
  self.stack.append((tag,dict(attrs).get('id'),self.position_offset()))
 def handle_startendtag(self,tag,attrs): pass
 def handle_endtag(self,tag):
  if not self.stack: return
  # Well-formed selected fragments are balanced; nonselected HTML metadata only.
  ix=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i][0]==tag),None)
  if ix is None:return
  t,i,start=self.stack[ix];del self.stack[ix:]
  if i in selected_ids:self.results[i]=(start,self.position_offset()+len('</'+tag+'>'))
p=Balanced();p.feed(text); assert set(p.results)==set(selected_ids)
anchors=[]; selected_dir=OUT/'fragments';selected_dir.mkdir(exist_ok=True)
for i in selected_ids:
 start,end=p.results[i]; bstart=len(text[:start].encode());bend=len(text[:end].encode());fragment=raw[bstart:bend]
 label=i.replace('.','-');(selected_dir/(label+'.raw')).write_bytes(fragment);(selected_dir/(label+'.lf')).write_bytes(lf(fragment))
 anchors.append(dict(id=i,path=str(PRIMARY),start_character0=start,end_character0_exclusive=end,start_utf8_byte0=bstart,end_utf8_byte0_exclusive=bend,physical_lines1=[text.count('\n',0,start)+1,text.count('\n',0,end-1)+1],fragment_raw_sha256=sha(fragment),fragment_lf_sha256=sha(lf(fragment)),fragment_bytes=len(fragment),balanced_outer=True,snapshot='fragments/'+label))
writej('primary-balanced-inventory.json',dict(whole=pin(PRIMARY),new_anchors=anchors,inherited_anchor_inventory=str(OLD/'original-primary-balanced-inventory.json.lf'),full_primary_semantic_scan=False))
nodes=graph['nodes']; edges=graph['edges']; N={n['id']:n for n in nodes}; newnodes=[]; newedges=[]
def node(id,kind,contract,anchors=None,**kw):
 n=dict(id=id,kind=kind,contract=contract,**kw)
 if anchors:n['primary_anchors']=anchors
 assert id not in N;N[id]=n;nodes.append(n);newnodes.append(n);return id
def edge(a,b,relation='mathematical-ingredient',**kw):
 e=dict(from_node=a,to_node=b,relation=relation,component='50-new-source-only',compiled50caller=False,**kw);edges.append(e);newedges.append(e)
node('S50.P','source-definition','Actual P conditional expectation given Y on H=L2(J); macro y-dependent subspace, Pperp=I-P.',['A2.E1','A2.E2','A2.SS1.p1.4','A2.SS1.p1.5'])
node('S50.blocks','source-definition','First block subscript target, second source; source generic T in B.3 is not later T=U_PP.',['A2.SS1.p2.1','A2.E3','A2.SS1.p2.2'])
node('S50.U','source-producer','Actual F(x,y)=(x,2x-y); pullback selfadjoint unitary on actual joint L2 quotient.',['A2.SS1.p3.1','A2.E4','A2.SS1.p3.2','A2.Ex3'])
node('S50.ABD','source-identity','Source U_PP=PUP, U_perpP=Pperp UP, U_perpperp=Pperp UPperp; A/B/D are authored aliases. U_perpP*U_perpP=I-U_PP² ON ranP, and U_perpP*U_perpperp=-U_PP U_perpP*.',['A2.SS1.p3.3','A2.E5'])
node('S50.norm','source-identity','B.9 same Y+=X+sqrtη Z and Y-=X-sqrtη Z, common ν; T f=E[f(Y-)|Y+], residual f(Y-)-Tf(Y+), ||U_perpP f||²=E Var(f(Y-)|Y+)=||f||ν²-||Tf||ν².',['A2.E8','A2.E9'])
node('S50.consumer','source-conclusion','C.1 formula(C.2): smooth compact f, η∫||true gradient Tf||²ν ≤ cη ∫Var_S(f)ν = cη||U_perpP f||², cη=(1-αη)²/[4(1+αη)].',['A3.SS1.p3.6','A3.E2','A3.SS1.p3.7'])
node('R50.rough','source-gap-outside-target','B.13 allL2→weightedH1 needs outer compact density/closedness and genuine outer gradient domain; fiber domain D_y is distinct. 49 Differentiable+gradient L2 does not identify repository closed weightedH1.',['A2.E13','A3.SS1.p1.1'])
node('R50.Gamma','source-adapter-outside-target','Actual Γ=(I-T²)^(1/2) on macroscopic space needs genuine positive-root construction/domain. Full joint starB B=P-A², not I-A² on whole L2.',['A2.E10','A2.E11'])
node('R50.halfturn','source-outside-target','B.6/B.7 and subsection C.2 halfturn are separate joint-transition/spectral ingredients; no use in bounded smooth block energy.',['A2.E6','A2.E7'])
PARENTS=[('A50.energy49','ConditionalGradientEnergy','reflected_conditional_gradient_energy'),('A50.rep','MacroscopicRepresentative','macroscopic_reflection_smooth_representative'),('A50.blocks','ReflectionL2','actual_reflection_block_identities')]
providers=[]
def provider(id,path,start,end,nodeid,kind,qualified=None):
 b=path.read_bytes(); fragment=b[start:end]; stem=id.replace('.','-')
 (selected_dir/(stem+'.raw')).write_bytes(fragment);(selected_dir/(stem+'.lf')).write_bytes(lf(fragment))
 before=b[:start];endbefore=b[:max(start,end-1)]
 rec=dict(id=id,path=str(path),kind=kind,node_id=nodeid,whole_raw_sha256=sha(b),whole_lf_sha256=sha(lf(b)),whole_bytes=len(b),start_utf8_byte0=start,end_utf8_byte0_exclusive=end,physical_lines1=[before.count(b'\n')+1,endbefore.count(b'\n')+1],fragment_raw_sha256=sha(fragment),fragment_lf_sha256=sha(lf(fragment)),fragment_bytes=len(fragment),snapshot='fragments/'+stem,qualified_id=qualified,provider_mathematical_proof_body_selected=False)
 providers.append(rec);inputs.append(dict(pin(path),selection=id,whole_hash_identity_only=True));return rec
for index,(id,module,name) in enumerate(PARENTS):
 c=contracts['parents'][index] if 'parents' in contracts else contracts['contracts'][index]
 path=ROOT/c['file'];b=path.read_bytes();st=b.index(('theorem '+name).encode());en=b.index(b':= by',st);fragment=b[st:en]
 h=lf(fragment).rstrip()+b'\n';assert sha(h)==c['public_header_lf_sha256'];assert sha(b)==c['whole_raw_sha256'] and sha(lf(b))==c['whole_lf_sha256']
 node(id,'opaque-admitted-public-producer',c['public_header'],qualified_id=c['declaration'],whole_raw_sha256=sha(b),whole_lf_sha256=sha(lf(b)),public_header_lf_sha256=sha(h),parent_body_semantically_expanded=False)
 rec=provider('parent-'+module,path,st,en,id,'opaque-admitted-public-header',c['declaration']);rec['public_header_normalization']='LF, rstrip terminal whitespace, append one LF; raw selected prefix remains unmodified';rec['public_header_lf_sha256']=sha(h)
# Exact minimal external contracts. Header-only selections end before proof bodies.
ML=ROOT/'.lake/packages/mathlib/Mathlib'
def select_lines(id,rel,a,b,nodeid,contract,qualified,kind='selected-external-primitive-contract',proof=False):
 path=ML/rel;data=path.read_bytes();ls=data.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));end=sum(map(len,ls[:b]));node(nodeid,kind,contract,qualified_id=qualified,external_provider_proof_expanded=False);return provider(id,path,start,end,nodeid,kind,qualified)
select_lines('api-condunique','Probability/Kernel/Disintegration/Unique.lean',82,84,'P50.condunique','Finite ρ, StandardBorel nonempty Ω; finite kernel κ and equality ρ=ρ.fst⊗κ produce κ=ρ.condKernel AE under ρ.fst. Compare two kernels via same canonical condKernel; no every-y equality.','ProbabilityTheory.eq_condKernel_of_measure_eq_compProd')
select_lines('typing-condunique','Probability/Kernel/Disintegration/Unique.lean',32,40,'P50.condunique-context','α,β measurable; Ω StandardBorel/nonempty; ρ finite. Real finite Hilbert supplies standardBorel/nonempty, probability supplies finiteness.','ProbabilityTheory.eq_condKernel_of_measure_eq_compProd:section-context','selected-typing-context')
select_lines('api-aemap','MeasureTheory/Measure/Map.lean',248,249,'P50.aemap','AEMeasurable map φ and predicate AE under μ.mapφ produce predicate(φ x) AE under μ.','MeasureTheory.ae_of_ae_map')
select_lines('api-mapmap','MeasureTheory/Measure/Map.lean',203,204,'P50.mapmap','Both maps measurable; successive pushforwards equal pushforward of composition.','MeasureTheory.Measure.map_map')
select_lines('api-Lpext','MeasureTheory/Function/LpSpace/Basic.lean',146,146,'P50.Lpext','Two actual Lp elements with AE equal representatives are equal in quotient.','MeasureTheory.Lp.ext')
select_lines('api-L2inner','MeasureTheory/Function/L2Space.lean',137,137,'P50.L2inner','True L2 inner product = integral pointwise inner product; norm² from real inner-self identity, not an arbitrary norm certificate.','MeasureTheory.L2.inner_def')
select_lines('typing-L2inner','MeasureTheory/Function/L2Space.lean',102,103,'P50.L2inner-context','Measurable underlying space, real/complex scalar and inner-product codomain; ancillary F unused by inner_def is typing-only.','MeasureTheory.L2.inner_def:section-context','selected-typing-context')
select_lines('api-realnorm','Analysis/InnerProductSpace/Basic.lean',396,396,'P50.realnorm','Real inner-self equals true squared norm.','real_inner_self_eq_norm_sq')
select_lines('api-integralAE','MeasureTheory/Integral/Bochner/Basic.lean',299,299,'P50.integralAE','AE-equal integrands have equal actual totalized Bochner integrals; separately supplied actual L2/L1 prevents using totalization as fake domain.','MeasureTheory.integral_congr_ae')
select_lines('api-integralmap','MeasureTheory/Integral/Bochner/Basic.lean',1043,1045,'P50.integralmap','AEMeasurable phi and AEStronglyMeasurable integrand under actual pushed law; actual Bochner integral pushforward formula.','MeasureTheory.integral_map')
select_lines('definition-condExpL2','MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',68,70,'D50.condExpL2','condExpL2 hm is actual orthogonalProjectionOnto lpMeas, with internal Fact(m≤m0). Complete Hilbert codomain real satisfies type contracts.','MeasureTheory.condExpL2','selected-real-definition')
select_lines('typing-condExpL2','MeasureTheory/Function/ConditionalExpectation/CondexpL2.lean',44,61,'P50.condexp-context','RCLike field, complete Hilbert codomain; m≤m0 supplied by measurable_snd.comap_le. Eprime/F/G ancillary section variables unused by exact condExpL2 definition are EXCLUDED/incidental context, not mathematical premises.','MeasureTheory.condExpL2:section-context','selected-typing-context')
select_lines('definition-lpMeas','MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',88,93,'D50.lpMeas','Actual submodule of Lp consisting of AEStronglyMeasurable with respect to sub-sigma-algebra; zero/add/scalar closure fields are structure witnesses, not extra theorem hypotheses.','MeasureTheory.lpMeas','selected-real-definition')
select_lines('typing-lpMeas','MeasureTheory/Function/ConditionalExpectation/AEMeasurable.lean',61,66,'P50.lpmeas-context','Measurable α, real normed scalar/codomain, exponents and measures; lpMeas is not an arbitrary assumed projection.','MeasureTheory.lpMeas:section-context','selected-typing-context')
select_lines('definition-IsCondKernel','Probability/Kernel/Disintegration/Basic.lean',53,59,'D50.IsCondKernel','Measure.IsCondKernel is equality ρ.fst⊗κ=ρ, not a chosen pointwise conditional density.','MeasureTheory.Measure.IsCondKernel','selected-class-definition')
select_lines('api-disintegrate','Probability/Kernel/Disintegration/Basic.lean',63,63,'P50.disintegrate','Projection from actual IsCondKernel yields true disintegration equality; class field generated witness, not a theorem proof edge.','MeasureTheory.Measure.disintegrate')
select_lines('definition-MemLp','MeasureTheory/Function/LpSeminorm/Defs.lean',118,119,'D50.MemLp','MemLp f p μ means AEStronglyMeasurable f μ and finite eLpNorm; all actual f/Tf/gradient domains produced by49.','MeasureTheory.MemLp','selected-real-definition')
select_lines('definition-subtypeL','Topology/Algebra/Module/ContinuousLinearMap/Restrict.lean',44,48,'D50.subtypeL','Actual continuous inclusion of a submodule into the ambient normed space; the structure field toLinearMap is not an extra mathematical theorem call.','Submodule.subtypeL','selected-real-definition')
select_lines('definition-isometryCLM','Analysis/Normed/Operator/LinearIsometry.lean',276,277,'D50.isometryCLM','Actual continuous linear map obtained from linear isometry toLinearMap and continuity; no supplied operator.','LinearIsometry.toContinuousLinearMap','selected-real-definition')
select_lines('definition-comap','MeasureTheory/MeasurableSpace/Basic.lean',82,83,'D50.comap','Actual pullback measurable space, sets inverse images of measurable sets; generated measurability closure fields remain unexpanded.','MeasurableSpace.comap','selected-real-definition')
select_lines('api-AEcongr','MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean',195,195,'P50.AEcongr','AEStronglyMeasurable is preserved under AE equal integrands.','MeasureTheory.AEStronglyMeasurable.congr')
select_lines('api-AEsmul','MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean',360,361,'P50.AEsmul','AEStronglyMeasurable is closed under constant scalar multiplication with continuous constant scalar action.','MeasureTheory.AEStronglyMeasurable.const_smul')
select_lines('generator-AEadd','MeasureTheory/Function/StronglyMeasurable/AEStronglyMeasurable.lean',299,301,'P50.AEadd','to_fun/to_additive generator of actual AEStronglyMeasurable.add: continuous addition and two AE strongly measurable functions. Generator attributes are not mathematics calls.','MeasureTheory.AEStronglyMeasurable.add','selected-generated-public-contract')
for id,line,q,c in [('Lpzero',190,'MeasureTheory.Lp.coeFn_zero','Actual zero Lp representative AE zero.'),('Lpadd',198,'MeasureTheory.Lp.coeFn_add','Actual sum Lp representative AE sum.'),('Lpsmul',436,'MeasureTheory.Lp.coeFn_smul','Actual scalar Lp representative AE scalar product.')]:select_lines('api-'+id,'MeasureTheory/Function/LpSpace/Basic.lean',line,line,'P50.'+id,c,q)
node('P50.measzero','external-unexpanded-generated-primitive','stronglyMeasurable_zero is generated from stronglyMeasurable_one via to_additive; zero constant is strongly measurable. Header/generator source pin below; no primitive proof expansion.','',qualified_id='MeasureTheory.stronglyMeasurable_zero')
path=ML/'MeasureTheory/Function/StronglyMeasurable/Basic.lean';bb=path.read_bytes();ls=bb.splitlines(keepends=True);st=sum(map(len,ls[:109]));en=sum(map(len,ls[:110]))+ls[110].index(b':=');provider('generator-measzero',path,st,en,'P50.measzero','selected-generated-public-header','MeasureTheory.stronglyMeasurable_zero')
node('P50.orthProj','external-unexpanded-primitive','Actual orthogonalProjectionOnto requires K.HasOrthogonalProjection; complete closed lpMeas supplies the instance inside the already compiled condExpL2 parent construction, not a new public premise. Definition right-hand side exposed by narrow locator but proof/providers not expanded.','',qualified_id='Submodule.orthogonalProjectionOnto')
path=ML/'Analysis/InnerProductSpace/Projection/Basic.lean';bb=path.read_bytes();ls=bb.splitlines(keepends=True);st=sum(map(len,ls[:112]));en=st+ls[112].index(b':=');provider('api-orthProj',path,st,en,'P50.orthProj','selected-definition-header-only','Submodule.orthogonalProjectionOnto')
select_lines('typing-orthProj','Analysis/InnerProductSpace/Projection/Basic.lean',110,110,'P50.orthProj-context','Exact K.HasOrthogonalProjection class context; instance internally present in real condExpL2 construction.','Submodule.HasOrthogonalProjection','selected-typing-context')
provider('target-signature',PRE/'prospective-statement.txt',0,len((PRE/'prospective-statement.txt').read_bytes()),'I50.target','sealed-statement-only',seal['signatures'][0]['full_declaration'])
for id,contract,q in [('P50.operator-types','Lp, scalar continuous linear maps, linear isometries, composition/product, powers, star/selfadjoint and subtype inclusion are standard unexpanded operator primitives. Generated coercion/structure fields are not fabricated theorem calls.','MeasureTheory.Lp; ContinuousLinearMap; LinearIsometry; IsSelfAdjoint; Submodule.subtypeL'),('P50.outer-integral','Marginal norm transport uses integral_map and actual scalar L2 inner-self; measurable snd and genuine squared integrability are internal.','MeasureTheory.integral_map'),('P50.measurable','measurable_snd/comap_le and AE strongly measurable composition are actual measurable structure requirements, not externally supplied desired inequalities.','measurable_snd; Measurable.comap_le; MeasurableSpace.comap'),('P50.domain-types','ContDiff, Differentiable, HasCompactSupport and finite Hilbert/Borel typing have their usual pinned definitions, no positive dimension or centering.','ContDiff; Differentiable; HasCompactSupport; NormedAddCommGroup; InnerProductSpace; FiniteDimensional; MeasurableSpace; BorelSpace'),('P50.AE','Filter.EventuallyEq under MeasureTheory.ae; representative equality is AE in actual indicated law.','Filter.EventuallyEq; MeasureTheory.ae')]:node(id,'external-unexpanded-primitive',contract,qualified_id=q,expansion_boundary='Standard typed primitive; no primitive proof expansion or compiled50 edge asserted')
INTERNAL=[('I50.sameS','Internally derive Λ.IsCondKernel S for49 SAME S from actual R disintegration plus every-y reflected map; preserve literal ν=J.snd and Λ.fst=ν. Finite measure/Markov kernels and measurable reflection supply real product domains, not a public certificate.'),('I50.uniqueS','Compare49 S with representative parent S0 by uniqueness of Λ disintegration: S=S0 AEν only. Thus conditional integrals agree AEν; never assert equality for every y or transfer derivatives.'),('I50.sameU','Parent U0/U1 are actual F-pullbacks on SAME J. For every g use both AE statements and Lp.ext to identify maps; preserve isometry/involution/selfadjoint and actual P. Extra R0 from ReflectionL2 is unused, not identified globally with49 R.'),('I50.meanlift','For smooth compact f, parent gives g=[f∘snd], Pg=g, Ag=[∫f S0∘snd]. Lift AEν equality of conditional means to AEJ along measurable snd. This changes quotient representative only; true differentiability stays49 literal Tf.'),('I50.normtransport','Use actual f/Tf L2ν and AE representatives to express ||g||²=∫f²ν, ||Ag||²=∫Tf²ν. Actual J.snd pushforward and L2 integral inner product supply every squared-domain/integrability premise internally.'),('I50.defect','Combine actual parent macro norm-defect ||Bg||²=||g||²-||Ag||² with49 SAMEν variance identity. Conclude ∫Var_Sf ν=||Bg||²; no supplied norm/variance or energy certificate.'),('I50.energy','49 literal Tf differentiability, actual gradient L2, variance L1 and sharp η energy inequality survive unchanged. Substitute actual defect norm², preserve cη exactly even at αη=1.'),('I50.target','Exact2907 bounded smooth compact actual-joint L2 integration statement; awaiting future proof and independent topology review.'),('I50.extension','Finite real Hilbert including rank0 extends printed R^d; measurable/Borel law semantics explicit. No finite-dimensional claim about full L2(J), no positive dimension, no normalization/mean-zero observer premise.')]
for id,c in INTERNAL:node(id,'candidate-conclusion' if id=='I50.target' else ('authored-extension' if id=='I50.extension' else 'internal-obligation'),c)
for a,b in [('S.J','S50.P'),('S.R','S50.P'),('S50.P','S50.blocks'),('S.reflection','S50.U'),('S50.P','S50.ABD'),('S50.U','S50.ABD'),('S50.blocks','S50.ABD'),('S50.ABD','S50.norm'),('S.T','S50.norm'),('S.nu','S50.norm'),('S50.norm','S50.consumer'),('S.C2','S50.consumer'),('S.compact','S50.consumer')]:edge(a,b,'printed-source-ingredient')
routes={'I50.sameS':['A50.energy49','D50.IsCondKernel','P50.disintegrate','P50.mapmap','S.J','S.S'], 'I50.uniqueS':['I50.sameS','A50.rep','P50.condunique','P50.condunique-context'], 'I50.sameU':['A50.rep','A50.blocks','P50.Lpext','S50.U','S50.ABD'], 'I50.meanlift':['I50.uniqueS','I50.sameU','A50.rep','A50.energy49','P50.aemap','P50.measurable'], 'I50.normtransport':['I50.meanlift','A50.energy49','P50.L2inner','P50.outer-integral','D50.MemLp'], 'I50.defect':['I50.normtransport','I50.sameU','A50.blocks','A50.energy49','S50.norm'], 'I50.energy':['I50.defect','A50.energy49','S50.consumer'], 'I50.target':['I50.sameS','I50.sameU','I50.meanlift','I50.normtransport','I50.defect','I50.energy','I50.extension'], 'D50.condExpL2':['D50.lpMeas','P50.condexp-context','P50.operator-types'], 'D50.lpMeas':['P50.lpmeas-context','D50.MemLp','P50.AE']}
for b,aa in routes.items():
 for a in aa:edge(a,b,'candidate-internal-ingredient' if b.startswith('I50.') else 'selected-definition-ingredient')
for a,b in [('S50.consumer','R50.rough'),('S50.ABD','R50.Gamma'),('S50.U','R50.halfturn')]:edge(a,b,'outside-target-residual-not-proof-prerequisite')
for a,b in [('P.fubini','I50.sameS'),('P.fubini-domain','I50.sameS'),('P.map-integral','I50.sameS'),('P.kernel-prod-meas','I50.sameS'),('P50.integralmap','I50.normtransport'),('P50.integralAE','I50.normtransport'),('P50.realnorm','I50.normtransport'),('P50.L2inner-context','P50.L2inner'),('D50.subtypeL','I50.sameU'),('D50.isometryCLM','I50.sameU'),('D50.comap','D50.condExpL2'),('D50.condExpL2','I50.meanlift')]:edge(a,b,'candidate-internal-ingredient')
graph.update(schema_version='pbps-macroscopic-sourcegraph50-v1',status='CREATOR_SOURCE_ONLY_AWAITING_DISTINCT_TOPOLOGY',edge_orientation='ingredient -> consumer; historical49 prefix is inherited source-only component; no compiled50 call graph',chosen_route='same-law actual conditional representative and L2 block/norm integration',or_routes=[],full_paper_completion=False)
graph['components']={'inherited49':dict(nodes_prefix=len(oldgraph['nodes']),edges_prefix=len(oldgraph['edges']),graph_sha256=sha((OLD/'source-proof-graph.after.json').read_bytes()),accepted_source_only_topology_sha256='98e2cedb5884783202748f9f8aa684edb3a84af8679bfb5bcd32f05a433e08fc',historical_node_status_unchanged=True,not_direct50_proof_dependencies=True),'new50':dict(nodes=len(newnodes),edges=len(newedges),three_immediate_opaque_parents=[x[0] for x in PARENTS])}
graph['source_expansion_boundary']='Selected printed B1-B5/B8-B9 and inherited49C1 formula(C2). Actual49/representative/block public contracts opaque. Internal transport and L2 algebra source adapters are obligations, not compiled edges. No50 implementation exists/read; roughH1/Gamma/halfturn separate.'
writej('selected-providers.json',dict(inherited_external=oldproviders,new=providers))
writej('source-proof-graph.json',graph)
writej('input-bindings.partial.json',inputs)
print(json.dumps(dict(nodes=len(nodes),edges=len(edges),new_nodes=len(newnodes),new_edges=len(newedges),new_providers=len(providers),new_balanced_anchors=len(anchors))))

