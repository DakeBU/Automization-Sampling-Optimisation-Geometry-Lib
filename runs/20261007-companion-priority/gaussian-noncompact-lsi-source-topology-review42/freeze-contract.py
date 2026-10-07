import datetime, hashlib, html, json, pathlib, re
ROOT=pathlib.Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-source-topology-review42'
PR=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-preread42'
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def rel(p):return p.relative_to(ROOT).as_posix()
def immutable(path,b):
 if path.exists():assert path.read_bytes()==b,'Immutable snapshot mismatch '+str(path)
 else:
  with path.open('xb') as f:f.write(b)
def save(n,j):
 with (OUT/n).open('xb') as f:f.write((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode())
pins=json.loads((PR/'inputs.json').read_text(encoding='utf-8'))
assert len(pins)==20
lease=json.loads((PR/'lease.json').read_text(encoding='utf-8'))
assert 'CLOSED' in json.dumps(lease)
inputs=[];coverage=[];policy_deltas=[]
for i,p in enumerate(pins):
 path=PR/(p['key']+'.raw.snapshot');raw=path.read_bytes();normalized=lf(raw)
 assert sha(raw)==p['raw_sha256'] and sha(normalized)==p['lf_sha256'],p['key']
 if p.get('path'):
  now=(ROOT/p['path']).read_bytes()
  if sha(now)!=p['raw_sha256'] or sha(lf(now))!=p['lf_sha256']:
   assert p['key'] in ['SLTreusePolicy','SLTbackgroundRegistry','TechnicalPolicy'],p['path']
   delta={'key':p['key'],'path':p['path'],'historical_raw_sha256':p['raw_sha256'],'historical_lf_sha256':p['lf_sha256'],'observed_current_raw_sha256':sha(now),'observed_current_lf_sha256':sha(lf(now)),'classification':'Administrative source/reuse-policy lifecycle, historical frozen policy retained as policy only; no new mathematical callability or admission inferred','current_snapshot':'policy-lifecycle.'+p['key']+'.raw.snapshot'}
   immutable(OUT/delta['current_snapshot'],now);policy_deltas.append(delta)
 prefix='reviewer.input.%03d'%i
 for suffix,b in [('.raw.snapshot',raw),('.lf.snapshot',normalized)]:
  immutable(OUT/(prefix+suffix),b)
 inputs.append(dict(p,read_path=rel(path),raw_snapshot=rel(OUT/(prefix+'.raw.snapshot')),lf_snapshot=rel(OUT/(prefix+'.lf.snapshot'))))
 coverage.append({'key':p['key'],'source_path_or_url':p.get('path',p.get('url')),'source_raw_sha256':sha(raw),'source_lf_sha256':sha(normalized),'required_ranges':p['ranges'],'line_count':sum(b-a+1 for a,b in p['ranges']),'future_disposition_rule':'Every selected physical line belongs to disjoint region partitions; every substantive declaration/definition/display/proof/citation gets NODE or EXCLUDED with reason. Imported primitives outside scope retain explicit unexpanded API boundaries, never invented selected-file providers.'})
extra=[
 ('OrderClosed','.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean',[[467,482]]),
 ('MemLpDefs','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/Defs.lean',[[64,70],[83,100],[116,123]]),
 ('HasFiniteIntegral','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/HasFiniteIntegral.lean',[[77,86]]),
 ('IntegrableDefs','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',[[54,61]])]
for key,path,ranges in extra:
 raw=(ROOT/path).read_bytes();normalized=lf(raw);prefix='reviewer.input.%03d'%len(inputs)
 for suffix,b in [('.raw.snapshot',raw),('.lf.snapshot',normalized)]:
  immutable(OUT/(prefix+suffix),b)
 inputs.append({'key':key,'path':path,'read_path':path,'raw_sha256':sha(raw),'lf_sha256':sha(normalized),'ranges':ranges,'raw_snapshot':rel(OUT/(prefix+'.raw.snapshot')),'lf_snapshot':rel(OUT/(prefix+'.lf.snapshot'))})
 coverage.append({'key':key,'source_path_or_url':path,'source_raw_sha256':sha(raw),'source_lf_sha256':sha(normalized),'required_ranges':ranges,'line_count':sum(b-a+1 for a,b in ranges),'future_disposition_rule':'Literal selected definitions/API sufficient for scope; typeclass/imported primitive boundaries must be honest and caller-anchored.'})
meta=[PR/'source-detail.json',PR/'source-detail.md',PR/'inputs.json',PR/'lease.json',
 ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-preproof42/signature.prospective.txt',
 ROOT/'.agents/skills/astis-source-dependency-audit/SKILL.md',ROOT/'docs/proof-digestion-protocol.md']
for path in meta:
 raw=path.read_bytes();normalized=lf(raw);prefix='reviewer.input.%03d'%len(inputs)
 for suffix,b in [('.raw.snapshot',raw),('.lf.snapshot',normalized)]:
  immutable(OUT/(prefix+suffix),b)
 inputs.append({'key':path.name,'path':rel(path),'read_path':rel(path),'raw_sha256':sha(raw),'lf_sha256':sha(normalized),'raw_snapshot':rel(OUT/(prefix+'.raw.snapshot')),'lf_snapshot':rel(OUT/(prefix+'.lf.snapshot')),'read_scope':'Preread provenance/policy or prospective exact statement identity, not graph or implementation'})
sig=(ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi-preproof42/signature.prospective.txt').read_bytes()
assert len(lf(sig))==691 and sha(lf(sig))=='ff9add5e7b7ce9ec01b1719574b8e80b843d3a469dd3026c6e40b831dab0a6ca'
primary=(OUT/'source-primary.raw.snapshot.html').read_bytes()
assert sha(primary)=='ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d'
anchor=[]
for path in sorted(OUT.glob('source-primary.*.raw.snapshot.html')):
 b=path.read_bytes();anchor.append({'path':rel(path),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)})
exposure={
 'prior_history':'Reviewer authored prior29 and41 source graphs and reviewed prior32/33 and41 mathematics. Prior41 whole body/Test/parent exposure is disclosed; it does not make this a fresh source-blind review. Current42 source topology author will be another actor, and proving root remains distinct.',
 'current_order':'Root task and CLOSED source-detail packet/manifest exposed intended42 target shape before deliberate primary source inspection. First mathematical raw-source inspection in this task was FIRST S4.E6/P4.3 plus Ex8 and true standardized law; standing/proximal source and canonical parent/API regions followed, then literal prospective691LF signature. No future42 graph existed or was read before this freeze.',
 'upstream_preread_caveats_preserved':'Source-detail actor recorded accidental41 metadata snippets and32shared proof236-249 exposure. These are historical disclosures, not independence erased by snapshot transport.',
 'current_incidental_reads':[{'what':'Primary raw HTML physical905-930 and1052-1083/1121-1136','reason':'Mistargeted line lookup exposed old Picard/recursive RGO context; not used to derive42 route and excluded from fresh mathematical dependency coverage'},
  {'what':'rg returned only semantic_slots key at line223 of current41 audit','reason':'Incidental schema-key lookup named an excluded41 final-audit file; no values, source verdict or lesson/blind content was opened or used. Seven slot names were read from semantic-roundtrip skill via independent schema search.'}],
 'no42_implementation_Test_blind_or_graph_exposure':True,'no41_lesson_blind_or_source_verdict_used':True,'no_compiler':True,
 'read_helper_failure':'A standing-source regex had bad escape\\k after primary anchors were already frozen; replaced by literal/source-id extraction. No mathematical target or source mutation.'}
save('reviewer.exposure.json',exposure)
save('reviewer.policy-lifecycle-delta.json',{'deltas':policy_deltas,'not_a_mathematical_source_change':True,'frozen_preread_policy_preserved':True,'not_a_new_port_status_or_theorem_certificate':True})
source_contract={
 'schema_version':1,'status':'FROZEN_PRIMARY_BEFORE_GRAPH','actor':'gaussian_domain_preproof_reviewer_29','role':'Independent future42 topology validator; contract preparation only, graph author distinct',
 'primary':{'id':'arXiv2609.06906v1','raw_sha256':sha(primary),'snapshot':'source-primary.raw.snapshot.html','fresh_core_anchors':[{'id':'S4.Ex8','lines':[1291,1297]},{'id':'S4.SS1.p4.2','lines':[1298,1301]},{'id':'S4.E6','lines':[1302,1309]},{'id':'S4.SS1.p4.3','lines':[1310,1314]}],
  'standing_and_characterized_context':[{'id':'S2.p1.1','lines':[606,609]},{'id':'S2.E1','lines':[614,621]},{'id':'S4.Ex3','lines':[1184,1190]}],
  'source_claim':'W2(r_y,N(0,I))<=sqrt(E_r_y norm(grad rho_y)^2), first inequality only; source invokes Talagrand plus Gaussian LSI, not a printed cutoff/LSI function proof.',
  'actual_objects':'rho_y(u)=V(p+sqrt(eta)u)-V(p)-sqrt(eta)<grad V(p),u>; p=prox_etaV(y); true r_y is law of (X-p)/sqrt(eta) for true RGO and has Lebesgue density proportional exp(-norm(u)^2/2-rho_y(u)).',
  'standing':'V is C2 and normalized kappa^-1 I<=Hessian V<=I, kappa>=1; eta>0 for the actual32/33 consumer. No numerical upper eta bound is added to this generic background.',
  'explicit_omissions':'Gaussian LSI and Talagrand analytic hypotheses/normalizations, cutoff approximations, KL/weak representative/metric adapters are omitted background. The later eta gradient-growth and eta sqrt(d) inequalities are distinct source steps.'},
 'prospective_target_identity':{'name':'gaussian_logSobolev_of_contDiff','raw_bytes':len(sig),'LF_bytes':len(lf(sig)),'raw_sha256':sha(sig),'lf_sha256':sha(lf(sig)),'signature_snapshot':[x['raw_snapshot'] for x in inputs if x.get('path','').endswith('preproof42/signature.prospective.txt')][0],
  'attribution':'Authored signed C2 finite-real-Hilbert domain extension sufficient for actual32. It is not printed SPHMC function LSI, not unrestricted weak-Sobolev LSI and not FIRST4.6 itself.',
  'statement_review_boundary':'Exact prospective StatementSeal is separately reviewed by another actor. This file is no signature-admission or proof certificate.'},
 'seven_semantic_slots':{
  'objects':'Arbitrary signed f:E->Real, gamma=actual ProbabilityTheory.stdGaussian E; literal gradient=_root_.gradient f. No arbitrary law/coordinate density or supplied gradient representative.',
  'domains':'Real finite-dimensional complete Hilbert, actual Borel measurable structure, f C2, true f and gradient f in MemLp2, true Phi(f²) Integrable. These explicit generic analytic domains are actual32 outputs at its consumer, not new V/eta paper premises.',
  'quantifiers':'All E/classes and every signed f satisfying genuine stated domains; no dimension>0, mass>0, compactness, pointwise positivity, normalization or eta binder in generic target. Cutoff existence/global C and radius limits are internal.',
  'assumptions':'NormedAddCommGroup/InnerProductSpace Real/CompleteSpace/FiniteDimensional/MeasurableSpace/BorelSpace are carrier/Riesz/law structures. C2/fL2/gradL2/PhiL1 specify authored generic function class. No desired inequality, cutoff, convergence, law, selector, norm or LSI certificate supplied.',
  'conclusion':'Homogeneous Ent_gamma(f²)=integral Phi(f²)-Phi(integral f²) <=2 integral norm(gradient f)^2. Actual square and energy L1 must be derived before integral comparison even though prospective691 statement exports only inequality.',
  'scopes_and_senses':'Actual real Bochner integrals with true L1, not totalized fallback; literal C2 gradient, not a weak RN representative; Phi(0)=0 and continuity at0; actual Gaussian variance1. No semantic equality from named similar carrier/law.',
  'constant_dependencies':'Dimension-free2; internally chosen global cutoff C>0 independent of radius R with C/R; radius R_n=n+1>=1; later actual32 energy=Fisher/4 gives intended canonicalKL<=Fisher/2 only after p32=p33 and same law/entropy rewriting. T2 factor2 remains separate.'},
 'definition_expansion':[
  {'name':'stdGaussian E','kind':'literal','meaning':'Pi independent gaussianReal0 1 pushed by canonical orthonormal basis; inherited actual41/32 law identity, not a public premise'},
  {'name':'gradient','kind':'literal','meaning':'Inverse real complete-Hilbert Riesz isometry on fderiv; C2 provides genuine pointwise differentiation and continuous gradient. Operator-norm equality must follow Riesz isometry, not Pi sup-norm/coordinate identification'},
  {'name':'MemLp f 2 gamma','kind':'literal domain predicate','meaning':'AEStronglyMeasurable f gamma AND eLpNorm f2 gamma<infinity; exponent2 is nonzero finite and means finite actual squared-norm integral'},
  {'name':'Integrable Phi(f²) gamma','kind':'literal domain predicate','meaning':'AE strongly measurable entropy integrand AND its nonnegative norm integral finite. Not a conditionally convergent/totalized real integral'},
  {'name':'Phi','kind':'literal','meaning':'t Real.log t with totalized log0 but Phi0=0; continuous zero-aware tlogt, no positive mass assumption'},
  {'name':'radialSmoothCutoff R','kind':'literal','meaning':'smoothUnitCutoff(norm(x)/R), values[0,1],1 on closed ball R,0 outside2R; support, C-infinity, global derivative bound and exhaustion are genuine existing ASTIS parents'},
  {'name':'p32/p33','kind':'characterized','meaning':'True proximal stationary equation;33 exports uniqueness. Future actual-paper integration must derive p32(s)=p33(s) from stat32 via unique33 before rewriting rho,Z,q,f,R,r; no selector equality binder'},
  {'name':'canonical llr','kind':'quotient/representative','meaning':'33 llr=logq only AE under r, for integrals/integrability. No pointwise derivative of canonical RN/llr is inferred'}],
 'authored_route_at_most7':[
  'Expand true fL2/gradientL2 to actual q=f² and G² L1; C2 supplies continuous/AE-measurable observers and gradient.',
  'Choose existing radial chi_R with global C/R bound, R_n=n+1; g_n=chi_Rn*f is actual C2 compact via existing cutoff and support product leaves; compact41 is a conditional genuine theorem parent, not a supplied inequality.',
  'Derive actual gradient product rule by fderiv multiplication and inverse Riesz isometry; obtain norm bound C/R and pointwise gradient g_n -> gradient f (including rank0).',
  'Mass DCT:0<=g_n²<=q and pointwise g_n²->q, with real qL1/measurability internally.',
  'Entropy DCT: a_n=chi_n² in[0,1], Phi(a_n*q)=a_n*Phi(q)+q*Phi(a_n), zero-aware identity and |Phi(a_n)|<=1 give |Phi(g_n²)|<=|Phi(q)|+q. Phi continuity at mass0 preserves homogeneous entropy limit.',
  'Energy DCT: norm(gradient g_n)^2<=2G²+2C²q for R_n>=1; integrable dominator and pointwise gradient limit imply exact energy integral limit, not merely boundedness.',
  'Apply compact41 to every g_n, combine three integral limits, Phi continuity and scalar2 multiplication; real closed-order limit gives unchanged coefficient2. Actual32/33/Fisher/T2 consumer coherence is a separate later adapter.'],
 'alternative_route_contract':'External SLT GaussianSobolevDense cutoff W12 and OneDimGLSI density/entropy passage/tensorized product route are external-source context, distinct from authored direct C2 plus entropy-L1 cutoff DCT. Their derivative carriers, law maps and imported unexpanded dependencies are explicit; no false AND requiring both routes.',
 'truth_boundary':['No42 graph or implementation exists or is reviewed','No41 mathematical outcome confers42 theorem truth','No full weakW12/density theorem or externalSLT callable certificate','p32=p33/same q/r and canonicalKL/Fisher integration remain separate residual','GaussianT2/metric/coupling/second-moment adapters and FIRST4.6 W2/bias remain open','Paper algorithms/main/work/cost/composition and reader/PURIFIED are open'],
 'exposure':'reviewer.exposure.json','input_bindings':'reviewer.inputs.json','no_compiler':True,'no_sourcegraph_authored_or_validated':True}
save('primary.contract.json',source_contract)
requirements={
 'schema_version':1,'status':'FROZEN_EXPECTATIONS_NO_GRAPH_REVIEW','validator':'gaussian_domain_preproof_reviewer_29',
 'source_coverage_expectations':coverage,'primary_additional_ranges':[[606,609],[614,621],[1184,1190]],
 'selected_line_inventory_requirement':'All declared primary/API/external selected ranges are exhaustive and disjointly classified NODE or justified EXCLUDED; full snapshots are byte pins, not a claim to fresh-cover an entire source file/project. Additional primary context outside these ranges has explicit exposure-only exclusion.',
 'required_ingredient_obligations':[
  {'ingredient':'Actual32/33 function/law/domain signatures','caller':'Consumer32 header41-53 and33 header33-52','required':'Treat domain facts as existing producer outputs before actual integration; generic target may state true analytic function class, source consumer may not add its desired output as hypothesis'},
  {'ingredient':'Actual41 compact sufficient theorem','caller':'Prospective cutoff g_n application','required':'Exact640 interface with actual stdGaussian/gradient and three L1 facts; genuine conditional parent boundary, not new42 compiled edge'},
  {'ingredient':'Cutoff C2/support/range/globalC/R/exhaustion','caller':'Cutoff.lean literal155-176/198-230/235-291/324-330/390-399 and authored cutoff uses','required':'Every actual primitive supporting cutoff regularity, global constant scope and rank0-safe norm bound has producer edge; unrelated second-derivative/plateau leaves may be excluded'},
  {'ingredient':'Gradient product/Riesz norm bridge','caller':'Mathlib FDeriv.Mul205-209/261-267; Gradient.Basic82-83/127-146/173-177; Dual135-139/174-179','required':'Differentiate C2 originals internally; inverse Riesz linearity/isometry imports remain exact API boundaries if unexpanded, not invented local declarations'},
  {'ingredient':'True square/energy L1','caller':'Mathlib L2Space42-55 and MemLpDefs118-123','required':'MemLp must expand to AE measurable plus finite norm; no totalized integral shortcut'},
  {'ingredient':'Three dominated limit applications','caller':'Mathlib DominatedConvergence57-64','required':'For each n actual AE strong measurability, actual boundL1, norm domination for all n/AE x and pointwise/AE Tendsto. Separate mass/Phi/energy vertices/consumer edges'},
  {'ingredient':'Zero-aware Phi scaling and dominator','caller':'NegMulLog44-63/177-184/234-237 plus authored a*q identity','required':'Phi at0, |Phi(a)|<=1 on[0,1], |Phi(q)|+qL1 and mass-Phi continuity; do not add positive f/q/mass premise'},
  {'ingredient':'Exact real closed-order passage','caller':'OrderClosed467-482','required':'Two actual limit functions, NeBot atTop and eventual/alln compact inequality; coefficient2 preserved and internal domains established before real comparison'},
  {'ingredient':'Actual32=p33 selector coherence','caller':'33 public uniqueness35 with32 stationarity31','required':'Later SOURCE_GAP/residual explicitly connected to same rho/Z/q/r/Fisher consumer, not part of generic42 theorem completion'},
  {'ingredient':'External source cutoff route','caller':'SLTcutoff331-337,340-361,482-530,827-1044','required':'Actual direct calls cutoff_gradient_error_bound and cutoff_gradient_extra_term at865-866 and W12/L2 calls elsewhere are recorded if this branch is selected. Body fragment does not claim imported primitive full closure. C2 authored alternative bypasses nondifferentiable branches rather than attributing that shortcut to SLT'},
  {'ingredient':'External LSI context','caller':'SLToneDim415-445/476-540 and TensorizedGLSI460-480','required':'Exact hf_diff/hf_grad_cont/PhiL1 and source entropy/grad coordinate definitions; scalar density/mollifier and productSubAddEnt calls retain external-only dependencies or explicit exclusions'}],
 'reject_representation_errors':['Substring matches mistaken for literal direct calls','Qualified API namespaces invented from import file prefixes','Typing imports treated as declaration providers','Producer conclusion silently added as public source premise','Conditional compact41 or externalSLT admission reported as42 completion','Authored directDCT and source externalW12 routes fused into false AND','Omitted zero/rank0/eta/no positive-mass cases','CanonicalAE llr differentiated pointwise'],
 'not_a_source_graph':True,'compiled_edges':[],'no_graph_exposure_before_contract_close':True}
save('reviewer.topology.coverage-expectations.json',requirements)
save('reviewer.inputs.json',{'schema_version':1,'inputs':inputs,'source_preread_pins':20,'total_bound_inputs':len(inputs),'primary_balanced_anchors':anchor,'raw_LF_distinct':True})
save('reviewer.source-api.checks.json',{'status':'BOUNDED_PREREAD_SOURCE_API_CONTRACT_ONLY','seven_slots_frozen':True,'signature_identity':source_contract['prospective_target_identity'],
 'mathematical_route_assessment':'Bounded C2+L2+gradientL2+PhiL1 direct radial cutoff/DCT route is mathematically sound with exact2 and the displayed dominators; no implementation/API elaboration approval is given',
 'missing_internal_producers':['Actual Hilbert gradient cutoff product and norm bridge','Zero-aware entropy domination instantiated for signed f','Mass/Phi/energy DCT leaves under actual stdGaussian','Final closed-order coefficient2 integration'],
 'downstream_coherence_residual':'p32=p33 from stationary32/unique33, then same rho,q,Z,r/f and energy1/4; only after that canonical finiteKL33 identity yields KL<=Fisher/2. AE llr never differentiated.',
 'external_source':{'commit':'d0f506f0a695018265dccb33bcb05e2f5ca1c876','license':'Apache2.0 headers in four pinned SLT source snapshots','truth':'external-reference only, no imports/compiler/port/callable badge','toolchain':'Historical policy snippets mention4.32 audited cutoff and legacy4.27-rc1 clone; exact upstream toolchain file not freshly pinned by this20-input packet, so no new toolchain or compile claim'},
 'no_statement_admission':True,'no_graph_review':True,'no_theorem_credit':True,'blockers_for_contract_freeze':[],'compiler_NEVER_STARTED':True,'canonical_mutations':[]})
outputs=['primary.contract.json','reviewer.topology.coverage-expectations.json','reviewer.inputs.json','reviewer.exposure.json','reviewer.source-api.checks.json','reviewer.policy-lifecycle-delta.json','freeze-contract.py']
payload={'inputs':[{k:i[k] for k in ['read_path','raw_sha256','lf_sha256']} for i in inputs],
 'primary_anchors':anchor,'outputs':[{'path':rel(OUT/n),'raw_sha256':sha((OUT/n).read_bytes()),'lf_sha256':sha(lf((OUT/n).read_bytes()))} for n in outputs]}
runsha=sha(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
save('reviewer.run.json',{'schema_version':1,'run_sha256':runsha,'deterministic_payload':payload,'status':'FROZEN_PRIMARY_BEFORE_GRAPH','all_leases_CLOSED':True,'compiler_NEVER_STARTED':True})
for i in inputs:
 raw=(ROOT/i['read_path']).read_bytes();assert sha(raw)==i['raw_sha256'] and sha(lf(raw))==i['lf_sha256']
leasepath=OUT/'reviewer.topology.lease.json';lease=json.loads(leasepath.read_text(encoding='utf-8'))
lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'run_sha256':runsha,'contract_raw_LF_sha256':sha((OUT/'primary.contract.json').read_bytes()),'all_inputs_rechecked_unchanged':True,'graph_exposed':False,'graph_authored':False,'implementation42_exposed':False})
leasepath.write_bytes((json.dumps(lease,indent=2)+'\n').encode());save('reviewer.topology.lease.closed.json',lease)
print(json.dumps({'contract_raw_LF_sha256':sha((OUT/'primary.contract.json').read_bytes()),'run_sha256':runsha,'inputs':len(inputs),'coverage_regions':sum(len(x['required_ranges']) for x in coverage)+3,'coverage_selected_physical_lines':sum(x['line_count'] for x in coverage)+19,'all_leases':'CLOSED','compiler':'NEVER_STARTED'}))
