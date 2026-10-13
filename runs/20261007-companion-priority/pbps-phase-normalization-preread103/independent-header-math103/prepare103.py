from pathlib import Path
import hashlib,json,subprocess,os,time
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;PRE=O.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes()
 return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
header=PRE/'Header103.lean';assert info(header)['raw_sha256']=='af63f42611e180b198e069c2e636ddf48ee529524ecf3a292c51bf28111fb60d'
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
regions=[]
for a,b,label in [(257,258,'fixed source license'),(350,363,'original curvature assumptions'),(1395,1422,'conditional Gibbs potential and phase law (3.1)'),(3200,3227,'future normalized averaging consumer')]:
 part=b''.join(raw.splitlines(keepends=True)[a-1:b]);regions.append(dict(path=info(primary)['path'],line_start=a,line_end=b,raw_sha256=sha(part),bytes=len(part),interpretation=label))
local=['AutoSamplingTheory/TechnicalLemmas/Analysis/HessianStrongConvexity.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/StrongConvexGibbsIntegrability.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/Integrability.lean','AutoSamplingTheory/TechnicalLemmas/Measure/IsotropicGaussianDensity.lean','AutoSamplingTheory/TechnicalLemmas/Measure/Gibbs.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Gaussian/FourierTransform.lean']
route=[
 'Use genuine C2 lower Hessian bound to obtain StrongConvexOn univ alpha V, then existing positive-modulus Gibbs integrability. No critical point or minimizing point is needed.',
 'For fixed y, eta>0 gives Vy(y,x)>=V(x), hence 0<exp(-Vy)<=exp(-V). Continuity supplies measurability; Integrable.mono\' gives integrability. integral_exp_pos over nonzero canonical volume yields Zx>0.',
 'Use existing Gaussian integral at coefficient 1/2: integral exp(-norm(p)^2/2)=C=(sqrt(2*pi))^finrank>0. Equivalently specialize the existing isotropic Gaussian density theorem at variance 1.',
 'Split exp(-U)=exp(-Vy)*exp(-norm(p)^2/2). Tonelli on position-first volume.prod volume gives Zphase=ofReal(Zx*C), using nonnegativity and the real/ENNReal integral bridge.',
 'Zx>0 and C>0 give Zphase>0; ofReal of a real number is finite. The existing normalized Gibbs withDensity theorem then gives IsProbabilityMeasure nu.',
 'Expand Measure.tilted at -Vy, giving density ofReal(exp(-Vy)/Zx); specialize stdGaussian density at variance 1 giving ofReal(C^(-1)*exp(-norm(p)^2/2)). Derive both as measurable exact representatives.',
 'Use prod_withDensity and positivity-compatible ofReal multiplication/division/inverse identities to identify the product density with Zphase^(-1)*ofReal(exp(-U)). No process, event-simplex, sector substitution or invariance lemma is needed.'
]
save('source-first-route103.native.json',dict(status='FROZEN_INDEPENDENT_PRE_GRAPH_RECONSTRUCTION',reviewer='/root/exact_verifier96',header=info(header),primary=info(primary),source_regions=regions,inputs=[info(x) for x in local],creator_graph_read_before_freeze=False,creator_recommendation_read_before_freeze=False,implementation_exists=False,legitimate_route_at_most_seven_steps=route,independent_dependency_edges=['Hessian lower bound + C2 -> strong convexity of V -> exp(-V) integrable','eta positive + exp(-V) integrable -> exp(-Vy) integrable -> Zx positive','Gaussian integral + product factorization + position integrability -> exact finite positive phase mass','finite positive phase mass -> probability nu','tilted representative + Gaussian density + exact phase mass + product-density theorem -> product-law identification'],optional_alternative='QuadraticRegularization can instead derive strong convexity of Vy. It is not required by the smaller domination route.',not_a_dependency='SAU102 weighted-sector substitution is analytically independent of normalization; both meet only at a future normalized averaging consumer.',zero_dimension='Canonical volume on the zero vector space has mass 1, C=1, Zx=exp(-V(0))>0, phase normalization cancels that scalar, and both marginals are the unit atom.',six_hypotheses='hAlpha>0, hAlphaBeta, hV C2, two-sided genuine Hessian hH, hEta>0, hBetaEta. Upper bound/order/upper scale are retained source binders but not needed for this smaller normalization argument.',no_hidden_provider='No supplied minimizer, gradient zero, lower envelope, finite normalizer, probability assumption or density provider.',scope='Prospective header and dependency feasibility only; no proof, claim, seal, VERIFIED or process invariance.'))
(O/'Header103.exact.lean').write_bytes(header.read_bytes())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(O/'Header103.exact.lean')]
start=time.time()
with (O/'typecheck.stdout.log').open('xb') as out,(O/'typecheck.stderr.log').open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-typecheck103.native.json',dict(exit_code=p.returncode,command=argv,seconds=time.time()-start,header=info(header),exact_private_copy=info(O/'Header103.exact.lean'),toolchain=info(R/'lean-toolchain'),lake_manifest=info(R/'lake-manifest.json'),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip(),proof_of_candidate=False))
assert p.returncode==0
print('PASS independent source-first route frozen and exact header typecheck')
