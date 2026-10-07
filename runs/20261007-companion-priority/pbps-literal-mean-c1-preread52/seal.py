# coding: utf-8
import pathlib,json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
R=pathlib.Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-literal-mean-c1-preread52';M='.lake/packages/mathlib/Mathlib/'
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def txt(n,s):(O/n).write_bytes(s.encode())
assert json.loads((O/'lease.json').read_text(encoding='utf-8-sig'))['status']=='OPEN'
(O/'lease.open.historical.raw').write_bytes((O/'lease.json').read_bytes())
selections=[
 ('dominated-differentiation',M+'Analysis/Calculus/ParametricIntegral.lean',210,217,':= by','public Mathlib contract only'),
 ('parametric-context',M+'Analysis/Calculus/ParametricIntegral.lean',66,71,None,'typing; instantiated E=real output, H=finiteHilbert parameter'),
 ('dominated-continuity',M+'MeasureTheory/Integral/Bochner/Basic.lean',444,447,':= by','public Mathlib contract only'),
 ('C1-characterization',M+'Analysis/Calculus/ContDiff/Defs.lean',1179,1180,':= by','public Mathlib contract only'),
 ('C1-fderiv-continuity',M+'Analysis/Calculus/ContDiff/Defs.lean',1272,1273,None,'public Mathlib contract only'),
 ('C1-quotient',M+'Analysis/Calculus/ContDiff/Operations.lean',834,836,':= by','public Mathlib contract only'),
 ('compact-derivative',M+'Analysis/Calculus/FDeriv/Const.lean',388,389,None,'public Mathlib contract only'),
 ('compact-bounded',M+'Analysis/Normed/Group/Bounded.lean',158,159,':= by','public Mathlib contract only'),
 ('normalized-law',M+'MeasureTheory/Measure/Tilted.lean',42,43,None,'actual definition'),
 ('tilt-composition',M+'MeasureTheory/Measure/Tilted.lean',251,252,':= by','public contract; requires genuine exp(-V) integrability produced internally'),
 ('posterior-mean-integral',M+'MeasureTheory/Measure/Tilted.lean',230,231,':= by','public literal integral of normalized measure'),
 ('map-integral',M+'MeasureTheory/Integral/Bochner/Basic.lean',1067,1068,None,'public measurable-equivalence integral contract'),
 ('Haar-scaling',M+'MeasureTheory/Measure/Lebesgue/EqHaar.lean',336,338,':= by','actual volume affine Jacobian API'),
 ('equiv-density','AutoSamplingTheory/TechnicalLemmas/Measure/RadonNikodym.lean',193,198,':= by','real public ASTIS map-withDensity producer; no mapTilt exported theorem inferred'),
 ('Gaussian-weight-bound-private','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',68,70,':= by','PRIVATE contract only; not callable from new module; existing mathematical substrate, must factor/re-establish minimal needed bound'),
 ('Gaussian-first-bound-private','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',83,84,':= by','PRIVATE contract only; not callable producer'),
 ('Gaussian-derivative-private','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',38,43,':= by','PRIVATE definitions/contract, not public producer'),
 ('pointwise-existing-local','AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScore.lean',58,151,None,'EXPOSURE: minimum existing local mapTilt/smulTilt/reflectionAffine/actualReflectedDensity bodies inspected; not exported declarations'),
 ('incidental-parametric-body',M+'Analysis/Calculus/ParametricIntegral.lean',218,226,None,'EXCLUDED incidental proof snippet exposure from earlier context read'),
 ('incidental-private-bound-body','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',71,72,None,'EXCLUDED incidental private proof snippet'),
 ('incidental-private-first-body','AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',85,87,None,'EXCLUDED incidental private proof snippet'),
 ('actual50-laws-prob','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean',23,41,None,'public actual sameμ/J/ν and probability portion only'),
 ('actual50-S-density','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean',42,49,None,'public actual R/S pointwise density portion only'),
 ('actual50-Lp','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean',56,66,None,'public actual Tf and truegradient Lp portion only')]
pins=[]
for label,rel,a,z,cut,role in selections:
 p=R/rel;b=p.read_bytes();ls=b.splitlines(keepends=True);start=sum(map(len,ls[:a-1]));end=sum(map(len,ls[:z]));f=b[start:end]
 if cut and cut.encode() in f:end=start+f.index(cut.encode());f=b[start:end]
 (O/(label+'.raw')).write_bytes(f);(O/(label+'.lf')).write_bytes(f.replace(b'\r\n',b'\n'));pins.append(dict(path=str(p),physical_lines1=[a,b[:max(start,end-1)].count(b'\n')+1],start_utf8_byte0=start,end_utf8_byte0_exclusive=end,whole_raw_sha256=sha(b),whole_lf_sha256=sha(b.replace(b'\r\n',b'\n')),fragment_raw_sha256=sha(f),fragment_lf_sha256=sha(f.replace(b'\r\n',b'\n')),label=label,role=role))
put('input-bindings.json',{'schema':'pbps-literal-mean-c1-preread52-rawLF-v1','primary_before_api':json.loads((O/'primary-before-api.json').read_text()),'public_headers':json.loads((O/'public-contracts.bindings.json').read_text()),'selected_api_and_exposure':pins,'coordinate_recipe':'one-based physical inclusive ranges; zero-based UTF8 start inclusive/end exclusive. Terminal public header cut before :=by. SHA256 exact raw; LF replaces CRLF with LF only. Whole-file identity never implies whole-body inspection.'})
txt('prospective-shape.txt','''SOURCE/API RECOMMENDATION ONLY: no Lean declaration, prototype, typecheck, StatementSeal or proof.
Suggested file: AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean
Suggested name: AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1
Minimal producer imports: GaussianConvolutionRegularity; ParametricIntegral;
Bochner.Basic; ContDiff.Operations; FDeriv.Const; Normed.Group.Bounded.

{E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
[FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
(μ : Measure E) [IsProbabilityMeasure μ] {η : ℝ} (hη : 0 < η)
{f : E → ℝ} (hf : ContDiff ℝ 1 f) (hc : HasCompactSupport f) :
let R := fun y : E => μ.tilted (fun x => -‖x-y‖^2/(2*η))
let S := fun y : E => (R y).map (fun x : E => (2:ℝ) • x-y)
ContDiff ℝ 1 (fun y : E => ∫ u, f u ∂S y)

No caller bound on f/fderiv, input moment, C1Tf, gradient closure,
derivative domination, transport certificate or desired energy bound is a premise.
These are actual explicitly defined measures at every y, not an arbitrary AE
conditional-kernel representative. fC1 compact is an authored strengthening
of source fC∞ compact; source actual50 specialization retains all paper V/α/β/η conditions.
''')
contract={
 'schema':'literal-mean-C1-preread52-v1',
 'decision':'RECOMMEND genuine generic reflected Gaussian posterior mean C1 producer, using actual explicitly defined tilted/pushforward laws. Numerator C1 is the substantive missing mathematical ingredient; quotient/literal-mean normalization is internal.',
 'primary':'Fixed PBPSv1 C.1 4573-4576 compact reduction; 4579-4589 conditional density A3.Ex1; 4591-4599 score A3.Ex2; 4601-4609 normalized-density differentiation A3.E1 (C.1). Formula(C.2) 4654-4664 lies insideC.1, not subsectionC.2. Source does not print a C1 regularity theorem for arbitrary μ; this is authored background needed for its claimed closed-gradient passage.',
 'literal_laws':'R_y=μ.tilted(-||x-y||²/(2η)); S_y=(R_y).map(x↦2x-y), all y. GaussianConditionalKernel.exists_tilted_isCondKernel produces a genuine Markov R with this identity pointwise, not merely AE. For actualGibbs μ, reflection/normalization gives S_y=volume.tilted(-V((y+u)/2)-||y-u||²/(8η)), exactly actual50 S density at every y.',
 'numerator_route':{'K':'Kη(y,x)=exp(-||y-x||²/(2η))','Z':'Z(y)=∫Kη(y,x)dμ(x)>0; public GaussianConvolutionRegularity producesZ C2 andC Z>0, C>0 internally.','N':'N(y)=∫f(2x-y)Kη(y,x)dμ(x)','derivative':'G(y,x)=-Kη(y,x)•fderivℝ f(2x-y) -(f(2x-y)*Kη(y,x)/η)•innerSLℝ(y-x). Negative fderiv term comes from y↦2x-y; Gaussian term is also negative.','dominator':'Infer finite Mf,Mf′ bounding norms of f and fderiv globally fromC1+compactness. K≤1 and ||D_yK||≤(1+2η)/η imply ||G||≤Mf′+Mf(1+2η)/η uniformly inx,y. This inferred constant is probability-integrable without μ moments or neighborhoods depending onx.','continuity':'G(·,x) continuous from C1f/fderiv continuity and smoothGaussian. Bochner continuous_of_dominated applies to CLM-valuedG with same constant; dominated parameter differentiation gives actual derivativeN′=∫G. contDiff_one_iff_hasFDerivAt givesC1N.','literal_mean':'integral_map plus integral_tilted gives literal mean=N/Z for all y; positivityC2Z allows C1 quotient. Normalizing prefactorC cancels, no f-sign restriction and no division byzero.'},
 'availability':{'real_public_producers':['GaussianConvolutionRegularity.gaussian_convolution_potential_c2: positive density, ZC2; no inputmoment/density premise.','GaussianConditionalKernel.exists_tilted_isCondKernel: posteriorR genuine Markov and pointwise tilt identity.','ConditionalScore.reflected_conditional_covariance: actual source-densityS and HasFDerivAt literalMean for source compact∞f; no continuity of derivative exported.','WeightedC1GradientDomain.c1_in_closed_gradient: finite actualν, genuine Dgraph/hDclosable, C1Tf, actualtwoLp outputs => actualclosure graph.','RadonNikodym.measurableEquiv_map_withDensity and pinned Haar/map/tilt APIs support actual pointwise transport.'],
 'private_not_callable':'Gaussian weight bounds/first derivative bound and ConditionalScore map_tilt/smul_tilt/reflection_affine/actual_reflected_density are PRIVATE or local have blocks. No new module may call them as exported APIs. Their exact small mathematical exposure is recorded; needed derivative/bound and pointwise law transport must be factored or reproduced internally under the unchanged real hypotheses, never added as certificate premises.'},
 'same50_transport':'The exact actual50 S has a pointwise volume-tilt density. For actual μ=volume.tilted(-V), finite positive ZV and Integrable exp(-V) are already real producer outputs. Tilt composition, affine measurable equivalence u=2x-y, volume Jacobian2^-finrank and normalization cancel give EVERY-y posterior reflected law=that same volumeTilt. Hence actualTf equals genericliteralMean as a FUNCTION by extensionality. C1 transfers through this pointwise function identity. Conditional-kernel AE uniqueness is not used for derivative/regularity transport.',
 'seven_step_route':[
 '1. C1compactf yields actual global bounds onf and fderiv, via fderiv compact support and continuous_fderiv.',
 '2. Establish pointwiseGaussian derivative and its uniform (1+2η)/η bound; combine into exactG and probability-integrable constantdominator.',
 '3. Supply genuine measurability/integrability and apply dominated parameter differentiation toN.',
 '4. Use the same globaldominator for continuity of∫G; C1 characterization givesN C1.',
 '5. PositiveC2Z from trueexistingproducer, quotientC1 and true normalizedintegral/map formulas produce actualgenericMeanC1.',
 '6. Paper integration: internally produce pointwise affine Gibbs-posterior/volume-tilt equality, then SAME50S and functionextensionalTf identity; no AE derivative substitution.',
 '7. After51D is actually independentlyverified, combine actual50TfL2/truegradientL2, finiteν and C1Tf with c1_in_closed_gradient for literalTf graph membership. This is a later consumer, not an already verified output.'
 ],
 'strictly_smaller_fallback':'If target is too large for one SAU, first produce gaussian_reflected_numerator_c1 with exactly μprob, η>0, C1compactf and conclusion C1N. It retires the sole dominated-differentiation/derivative-continuity uncertainty, with the same genuine normalizedMean/Tf consumer. Do not substitute a theorem assuming continuity of∫G or caller domination.',
 'truth_boundary':['No proof/typecheck/compiler/claim/newcanonical declaration or source verdict. Candidate52 is source/API-only.','51closure has only sealedstatement/sourcegraph stage in this packet; not promoted to a compiled parent.','No fullroughL2/H1/B13/Γ/halfturn/main/cost/composition claim. Existing50sharp energy coefficient is untouched.','Source finiteEuclidean → finiteHilbert/rank0 extension and generic anyprobability/C1compact observer are authored. Rank0 yieldsconstantmean andtruezero derivative, withZ=1; no positive dimension or zero-mean hypothesis.'],
 'exposure':['Known49/50 whole-body and51sourcegraph/selectedparent exposure retained; not a sourceblind role. No52implementation exists or was read.','New public headers were extracted before proof. Then only ConditionalScore local58-151 pointwise law transport was read to resolve representative uncertainty; not a whole-parent audit and not an exported producer.','Locator read emitted privateGaussian names and tiny weight-bound/ParametricIntegral proof snippets; pinned separately as exposure, not callable mathematical producers.','Several guessed obsolete filenames returned rg errors; corrected via actual scoped rg--files. No whole-library negative inference.','No51topology reviewer/blind/finalsource verdict, no50newreviews, no compiler outputs read for this uncertainty.'
 ]}
put('source-contract.json',contract)
txt('capsule.md','''Recommend gaussian_reflected_mean_c1 for actual posterior/reflection laws, with μ probability, η>0, C1 compact f only. The real new ingredient is C1 of N(y)=∫f(2x−y)exp(−||y−x||²/(2η))dμ. No moment or supplied derivative/domination/closure certificate is needed.

Compact C1 f and fderiv have global finite bounds Mf,Mf′. Exact parameter derivative G is bounded uniformly by Mf′+Mf(1+2η)/η. Pinned dominated differentiation and dominated continuity yield C1N; existing true Gaussian convolution producer gives positive C2Z, and literal normalized posterior/reflection mean=N/Z gives C1 actualmean. PrivateGaussian bounds are not callable exports: the needed calculus bound must be produced/factored internally.

Actual50 SAME-S connection is pointwise, not AE: its every-y volume-tilt density equals reflection of the actual Gibbs posterior. Existing ConditionalScore local58–151 contains the exact normalization/affine-Haar argument using real public APIs, but the helper is local, so it is an internal integration obligation. Function extensionality then transfers C1 to literalTf. This also reconciles the source score-covariance derivative with the authored Gaussian numerator route without changing the law or sharp coefficient.

c1_in_closed_gradient requires only actualfiniteν, genuineclosableD/exactgraph, C1Tf and the two trueLp outputs. Actual50 supplies the latter; independentlyverified51D will supply the former. It needs no extra compactness ofTf or H1 certificate. 51is still pending, and fullroughB13 remains excluded.

The complete ≤7-step route, exact prospective shape, source anchors, actual/rawLF APIs and all parent/private exposures are recorded. No compiler/proof/claim/canonical changes or formal truth admission. Strictly smaller fallback is C1N under the same real binders, not a wrapper assuming derivative continuity.
''')
outputs={p.name:{'bytes':p.stat().st_size,'raw_sha256':sha(p.read_bytes()),'lf_sha256':sha(p.read_bytes().replace(b'\r\n',b'\n'))} for p in O.iterdir() if p.is_file() and p.name not in ['run.json','lease.json']}
run={'schema':'literal-mean-preread52-run-v1','mode':'source/API only','outcome':'RECOMMEND_REAL_REFLECTED_POSTERIOR_MEAN_C1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'proof_search':False,'compiler':'NOT_STARTED_CLOSED','claim':False,'canonical_changes':False,'declaration_created':False,'source_verdict':False,'outputs':outputs,'run_recipe':'SHA256 whole object excluding run_sha256, sortedcompact UTF8 ensure_ascii=False; raw/LF exactbytes, LF CRLF→LF only; actual final lease separately hashed to avoid circularity.'};run['run_sha256']=sha(json.dumps(run,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode());put('run.json',run)
for n in ['source-contract.json','capsule.md','run.json']:print(n,sha((O/n).read_bytes()))
print('LOGICAL_RUN',run['run_sha256'])
# Actual lease closure is the final filesystem operation.
lease=json.loads((O/'lease.json').read_text(encoding='utf-8-sig'));lease.update(status='CLOSED',read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),final_operation='Actual own lease final write; no filesystem reads after closure.')
b=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode();(O/'lease.json').write_bytes(b);print('ACTUAL_CLOSED_LEASE_RAW_LF',sha(b))
