import pathlib,json,hashlib,re,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path('E:/Samplinglib');O=ROOT/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain-preread54'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n')
def js(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode()
def dump(n,o):(O/n).write_bytes(enc(o))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return dict(path=str(p),raw_bytes=len(b),lf_bytes=len(lf(b)),raw_sha256=sha(b),lf_sha256=sha(lf(b)))
api=js(O/'public-header-bindings.json')
qnames={'parent50':'AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks','parent51':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalGradient.gaussian_marginal_gradient_closable','parent53':'AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean.reflected_gibbs_mean_c1','c1-adapter':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedC1GradientDomain.c1_in_closed_gradient'}
for a in api:a['qualified_id']=qnames[a['label']]
def select(label,path,a,b,q=None,kind='public-API-header',trim_assignment=False):
 p=ROOT/path;raw=p.read_bytes();lines=raw.splitlines(keepends=True);start=sum(map(len,lines[:a-1]));end=sum(map(len,lines[:b]));f=raw[start:end]
 if trim_assignment:
  i=f.find(b':=');assert i>=0;end=start+i;f=f[:i]
 (O/(label+'.raw')).write_bytes(f);(O/(label+'.lf')).write_bytes(lf(f));d=dict(label=label,qualified_id=q,kind=kind,physical_lines1=[a,b],start_utf8_byte0=start,end_utf8_byte0_exclusive=end,fragment_raw_sha256=sha(f),fragment_lf_sha256=sha(lf(f)),body_selected=kind in ['definition-semantics','disclosed-incidental-existing-body'],**pin(p));api.append(d);return d
select('adapter-typing','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',11,11,kind='public-typing-context')
select('adapter-innerproduct-typing','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',95,95,kind='public-typing-context')
for lab,a,b,q in [('toLp-definition',106,109,'MeasureTheory.MemLp.toLp'),('toLp-AE',111,111,'MeasureTheory.MemLp.coeFn_toLp'),('toLp-congr',115,116,'MeasureTheory.MemLp.toLp_congr'),('toLp-eq-iff',120,121,'MeasureTheory.MemLp.toLp_eq_toLp_iff')]:
 select(lab,'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',a,b,q,kind='definition-semantics' if lab=='toLp-definition' else 'public-API-header',trim_assignment=lab!='toLp-definition')
for lab,a,b,q,kind,trim in [('closed-definition',63,64,'LinearPMap.IsClosed','definition-semantics',False),('closable-definition',70,71,'LinearPMap.IsClosable','definition-semantics',False),('closure-definition',97,98,'LinearPMap.closure','definition-semantics',False),('closure-graph-public',107,108,'LinearPMap.IsClosable.graph_closure_eq_closure_graph','public-API-header',True)]:select(lab,'.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean',a,b,q,kind,trim)
select('graph-definition','.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean',735,736,'LinearPMap.graph','definition-semantics')
select('domain-of-graph','.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean',833,834,'LinearPMap.mem_domain_of_mem_graph',trim_assignment=True)
select('smooth-to-C1','.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/Defs.lean',1141,1141,'ContDiff.of_le',trim_assignment=True)
# Preserve every actual incidental existing API/body locator exposure; none is a proposed proof dependency.
select('incidental-Lp-locator','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',91,98,kind='disclosed-incidental-existing-body')
select('incidental-closure-locator','.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean',100,105,kind='disclosed-incidental-existing-body')
select('incidental-domain-proof-prefix','.lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean',827,828,kind='disclosed-incidental-existing-body')
select('incidental-adapter-private-header','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedC1GradientDomain.lean',12,12,kind='disclosed-incidental-header-no-proof')
select('incidental-toLp-API-body','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean',111,121,kind='disclosed-incidental-existing-body')
dump('API-bindings.json',api)
public53=lf((O/'parent53.raw').read_bytes()).rstrip()+b'\n';assert len(public53)==758 and sha(public53)=='43d2831fa373729dc44cfd575fa4e1b68b2462688db8445320f13e433ddbe23e'
target='''TEXT-ONLY prospective source/API recommendation; not a Lean declaration, typecheck or admission.
Proposed namespace AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain
Proposed name literal_source_mean_in_closed_gradient
Proposed file AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean

Bind finite real Hilbert/Borel E; V:E->R; alpha beta:R>=0; eta:R;
alpha>0, alpha<=beta, ContDiff R 2 V,
forall x a, alpha*norm(a)^2 <= D²V(x)[a,a] <= beta*norm(a)^2,
eta>0 and beta*eta<=1. No extra Lp/probability/core/closure/derivative premises.

let mu := volume.tilted(-V)
let J := map (p->(p.1,p.1+sqrt(eta)*p.2)) (mu.prod (stdGaussian E))
let nu := J.snd
let sourceS := y->volume.tilted(u->-V(half*(y+u))-norm(y-u)^2/(8*eta))

IsProbabilityMeasure nu AND exists G:Lp R 2 nu ->linear-partial Lp E 2 nu,
  Dense G.domain AND G.IsClosable AND G.closure.IsClosed AND
  (forall u v, (u,v) in G.graph IFF exists phi:E->R,
      ContDiff R infinity phi AND HasCompactSupport phi AND
      u =AE[nu] phi AND v =AE[nu] gradient phi) AND
  forall f:E->R, ContDiff R infinity f -> HasCompactSupport f ->
    let Tf := y->integral f(u) sourceS(y)(du)
    exists hT:MemLp Tf 2 nu, exists hGrad:MemLp (gradient Tf) 2 nu,
      (hT.toLp Tf, hGrad.toLp (gradient Tf)) in G.closure.graph.

G is chosen once before forall f and is the true source compact-gradient core.
It is distinct from50's lower-right block D. hT/hGrad are produced outputs,
not public assumptions; their toLp pair is the actual canonical AE class pair.
No compact support is required of Tf, no centering/positivity of f is assumed.
''' 
(O/'prospective-target-shape.txt').write_bytes(target.encode())
contract=dict(schema='source-mean-gradient-domain-preread54/v1',decision='RECOMMEND ONE source-specific compact literal-mean closed-gradient integration after53 independently VERIFIED',declaration='AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain.literal_source_mean_in_closed_gradient',file='AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean',result_kind_if_later_proved='integration-node',exact_target_shape='prospective-target-shape.txt TEXTONLY no declaration/typecheck/admission',source_first=pin(O/'source-before-API.json'),primary=dict(revision='PBPS2609.06905v1 fixed d81e9294...',anchors=dict(standing=[351,361],actual_joint_outer=[614,640],rough_B13=[3777,3786],compact_reduction=[4573,4576],source_density=[4581,4587],source_score=[4589,4595],normalized_derivative=[4597,4604],formula_C2_inside_C1=[4654,4664])),parents=dict(parent50='VERIFIED864ff305; current LF science exactly equal; true mu/J/nu probability, chosenS every-y source density, actual Tf and gradientTf MemLp on same nu; source smoothcompact f',parent51='VERIFIED19f7e6be; current LF science exactly equal; actual mu probability +eta>0 internally gives one dense closable G with full compact-gradient graph character and closed closure',adapter='VERIFIEDd3936f55; current LF science exactly equal; public c1_in_closed_gradient takes finite measure, actual closable core+graph character, true C1 and2MemLp. All those premises are supplied by parents inside proposed source target.',parent53='Prospective opaque exact758 header43d2831f only. Root reports focusedTests.1PASS3895; NOT independently VERIFIED at task assignment/current evidence. No body/verdict/decoder read. Proof/claim scheduling must await independent53 verification.'),assumptions=dict(source='V C2,positive alpha<=beta,full two-sided Hessian,eta>0,beta*eta<=1; signed C_c infinity f',authored='Finite real Hilbert/Borel including rank0, exact repository partial-gradient closure interpretation of compact smooth source branch',f_domain='Retain smoothcompact f because50 public producer requires ContDiff infinity. Do not silently extend to C1compact observers without new Lp/energy producer.',forbidden_extra_binders=['TfC1','Tf compact support','Tf/gradientTf Lp','rho/W density','probability/normalizer','gradient-core/closure/hgraph','pointwiseS identity','AE derivative certificate','desired domain/energy bound']),actual_semantics=dict(mu='literal volume.tilted(-V), genuine probability produced inside50',J='same (mu.prod standardGaussian).map generator; namespace receiver vs Measure.map definitionally same actual map',nu='J.snd actual Gaussian outer law, not conditional fiber S_y',sourceS='every-y actual source-volume normalized reflected density; same source law as50 chosen S by its forall-y output',Tf='literal sourceS mean; exact entire function equality transports C1 and gradient identity',G='one uniform actual compact-gradient LinearPMap on Lp(nu), uniquely pinned at graph level by smoothcompact representative characterization, never50 block D',canonical_classes='MemLp.toLp outputs agree AE with Tf/actual gradientTf; toLp_congr/eq_iff establish representative independence only after proper function/AE facts',closure='LinearPMap.closure chooses the closed graph extension only under true IsClosable;51 supplies that. Graph pair entails domain membership by mem_domain_of_mem_graph.',dimension='Finite position E does not imply finite-dimensional Lp(nu) or Lp(J); no such premise/finite-dimensional CFC shortcut.',weighted_H1='Conclusion is actual G.closure.graph pair/domain, not an invented weightedH1 structure or Differentiable+Lp automatic closure claim.'),route=[
 '1 Apply50 under originalsource alpha/beta/Hessian/eta-cap to obtain actual same mu/J/nu probability and a trueS whose every-y source density is the literal sourceS. Keep its smoothcompact Tf/gradientTf MemLp outputs; no private proof copy.',
 '2 Use produced mu probability andeta>0 with51; choose G once, retaining dense domain/closability/closed closure and exact smoothcompact AE graph characterization. J/nu definitions are the same actual generator/snd.',
 '3 For each signed smoothcompact f, ContDiff.of_le gives C1 f. After53 verification, apply its exact public law/C1 theorem using alpha cast and lower-Hessian projection. The50 forall-y density output gives equality of entire literal sourceS and chosenS mean FUNCTIONS, permitting C1 and true gradient transfer, not AE differentiation.',
 '4 Obtain both real MemLp witnesses from50 for the same literal Tf and gradientTf after that exact function rewrite; nu probability supplies IsFiniteMeasure nu internally. Tf need not be compactly supported.',
 '5 Invoke public WeightedC1GradientDomain.c1_in_closed_gradient on nu, G, its produced closability/graph characterization, actual C1Tf andboth actualLp witnesses. It produces the canonical toLp pair in G.closure.graph.',
 '6 Publish this one uniform-G compact-domain join; MemLp.coeFn_toLp fixes actual representatives and mem_domain_of_mem_graph gives domain interpretation. Existing50 AE macro Ag=Tfp2 coherence is a real downstream consumer; it does not replace pointwise C1 transport.'
],smallest_new_delta='Actual literal source mean to closed-gradient graph membership. No energy-coefficient wrapper, no50block replay, no abstract caller certificate route.',real_consumer='PBPS C.1 compact reduction and formula(C.2): actual50 Ag macro representative/literalTf now has genuine outer gradient domain. Needed before passing source smoothcompact approximation toward full B13.',rank0='Canonical nu unitDirac, noncentered constant1 allowed; actual mean1 and true gradient0 give nonempty closed graph pair (class1,class0), not empty/zero-observer certificate.',residual=['53 independent verification is pending parent-admission gate; this preread gives no theorem truth.', 'Fullrough arbitrary L2 observer smoothing/closedness+density passage and energy limits remain separate; compact membership does not finish everyL2H1/B13.', 'Gamma positive-root/halfturn/main/invariance/nonexplosion/error/caps/cost/composition/fullreader/fullGoal remain open.'],exposure=['Historical own49/50 whole proofs,51-53 source/API and53graph/overlay exposures retained; not freshblind.', 'For54 primary exactsource read and source-before-API contract written before public header retrieval; no54root candidate yet.', 'Only public758 parent53 header extracted; whole-file bytehash is provenance, no53body/verdict/decoder/other independent reviews opened.', 'Verified50/51/C1adapter bodies not expanded; git blobs hashed for exactLF science equality without outputting or semantically inspecting proofs.', 'Public adapter locator emitted private bounded_coefficient_memLp declaration header12 but no privateproof. Small Mathlib definition bodies and incidental existing closure/toLp/domain proof prefixes are disclosed and pinned as exposure only.', 'Initial guessed FunctionalInequalities.md and Analysis/Normed/Operator/LinearPMap.lean paths failed; actual rg--files paths recovered. Lp91-98 range was an incidental existing Lp structure-body locator, not toLp definition; actualtoLp106-109 pinned separately. No whole-library absence claim.'],truth_boundary='SOURCE/API scheduling recommendation only; no compiler/proof/claim/Goal/canonical/SAU/seal/sourcegraph54/theorem admission',failure_policy='If53 admission fails or actual sameS/Lp interface changes, stop and repair the exact contract; do not add TfC1/Lp/closure premises. Fullrough target must be diagnosed independently, not smuggled into compact join.')
dump('source-contract.json',contract)
dump('failed-retrievals.json',[dict(type='PATH_NOT_FOUND',path='research-wiki/sampling-sde-library/cards/FunctionalInequalities.md',correction='Actual AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.md card',mathematical_failure=False),dict(type='PATH_NOT_FOUND',path='.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/LinearPMap.lean',correction='Pinned Topology/Algebra/Module/LinearPMap and LinearAlgebra/LinearPMap',mathematical_failure=False),dict(type='WRONG_LOCATOR_RANGE',path='LpSpace/Basic91-98',correction='Actual MemLp.toLp106-109; incidental old body snapshot retained',mathematical_failure=False)])
inputs=[pin(ROOT/'lean-toolchain'),pin(ROOT/'lake-manifest.json'),pin(ROOT/'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.md')]
for a in api:
 p=pathlib.Path(a['path']);q=pin(p)
 if q not in inputs:inputs.append(q)
inputs.append(pin(ROOT/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html'))
dump('input-bindings.json',inputs)
lease=js(O/'lease.json');lease.update(read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_filesystem_operation='Actual CLOSED lease write after all native artifact pins/capsule/run; no subsequent filesystem operation',theorem_credit=False);lb=enc(lease);lh=sha(lb)
caps='''Preread54 CLOSED: recommend ONE literal-source-mean closed-gradient integration, after53 independent verification.

Proposed SourceMeanGradientDomain.literal_source_mean_in_closed_gradient keeps source alpha/beta/two-sidedHessian/eta-cap and signed smoothcompact f. Choose one true dense closable compact-gradient core G for SAME canonical outernu, uniformly before allf. Internally combine50 real Tf/gradientTf MemLp,53 EVERY-y literal-source meanC1,51 actualG graph and the verified public C1 adapter. New conclusion is the canonical toLp mean/gradient pair in G.closure.graph; no new probability/Lp/C1/closure/normalizer certificates as premises. G is distinct from50 lower-right blockD.

The exact source-volume S must transfer entire mean functions and their true derivatives. AE conditional/Lp representative equality alone cannot transfer pointwise C1. Tf itself need not be compact. Finite positionE does not make Lp finite-dimensional. Rank0/noncentered mean1-gradient0 remains allowed.

Public50/51/WeightedC1GradientDomain currentLF bytes match VERIFIED864ff305/19f7e6be/d3936f55. Only53 exact758 publicheader43d2831f read; root focusedTests3895 is recorded without VERIFIED credit. No parentproof expansion. Sixstep route, text-only prospective binder/conclusion shape, source assumptions/residuals/exposure and exactrawLF API/input pins are in source-contract.json/prospective-target-shape.txt/API-bindings.json/input-bindings.json.

Fullrough everyL2/H1/B13, Gamma/halfturn/main/cost remain open. No compiler/proof/claim/seal/sourcegraph/canonical/Goal changes. Actual CLOSEDlease SHA256 '''+lh+'\n'
(O/'capsule.md').write_bytes(caps.encode())
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['run.json','lease.json']]
run=dict(schema='native-source-API-preread54-run/v1',result='CLOSED_BOUNDED_SOURCE_RECOMMENDATION_NOT_ADMITTED',inputs=inputs,outputs=outputs,exact_public53_header_lf_sha256=sha(public53),parent53_status='PENDING_INDEPENDENT_VERIFICATION_rootfocused3895_only',compiler_invocations=0,theorem_credit=False,source_admission=False,actual_lease=dict(path=str(O/'lease.json'),raw_bytes=len(lb),lf_bytes=len(lb),raw_sha256=lh,lf_sha256=lh,status='CLOSED'),hash_recipe='Physical SHA256 exactraw; LFCRLF->LF only. Logical run SHA256 UTF8 sortedcompact entireobjectminusrun_sha256 ensure_ascii=False allow_nan=False no newline; exactraw byte offsets0-based/end-exclusive andphysical lines1-based.')
run['run_sha256']=sha(json.dumps(run,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode());dump('run.json',run)
receipt=dict(CLOSED=True,contract=pin(O/'source-contract.json'),run=pin(O/'run.json'),logical_run_sha256=run['run_sha256'],actual_lease_rawLF_sha256=lh)
(O/'lease.json').write_bytes(lb)
print(json.dumps(receipt,ensure_ascii=False))
