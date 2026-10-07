from pathlib import Path
import hashlib, json, re, datetime

ROOT = Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/gaussian-compact-lsi-preread'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def dump(name, obj):
    b = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with (OUT / name).open('xb') as f: f.write(b)
    return {'path': str((OUT/name).relative_to(ROOT)).replace('\\','/'), 'raw_sha256': sha(b), 'lf_sha256': sha(lf(b)), 'bytes': len(b)}
paths = [
 ('primary_whole','runs/20261007-companion-priority/gaussian-transport-preread/source-primary.raw.snapshot.html'),
 ('primary_first','runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html'),
 ('primary_explanation','runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html'),
 ('primary_contract','runs/20261007-companion-priority/gaussian-compact-lsi-preread/primary.contract.json'),
 ('parent34_signature','runs/20261007-companion-priority/bernoulli-function-lsi/preproof/bernoulli.signature.txt'),
 ('parent34_verified_provenance','runs/20261007-companion-priority/bernoulli-function-lsi/verified.json'),
 ('parent36_signature','runs/20261007-companion-priority/gaussian-compact-entropy/preproof/signature.prospective.txt'),
 ('parent36_verified_provenance','runs/20261007-companion-priority/gaussian-compact-entropy/verified.json'),
 ('prospective37_signature_only','.astis/flip-energy37/signature.prospective.txt'),
 ('local_order_limit','.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean'),
 ('local_multiplication_limit','.lake/packages/mathlib/Mathlib/Topology/Algebra/Monoid/Defs.lean'),
 ('local_square_sign','.lake/packages/mathlib/Mathlib/Algebra/Ring/Commute.lean'),
 ('local_zero_mass_continuity','.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean'),
 ('local_gaussian_definition','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Real.lean'),
 ('local_bookkeeping_only','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/LogSobolev.lean'),
 ('local_interface_only','AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CanonicalLogSobolev.lean'),
 ('local_toolchain','lean-toolchain'), ('local_mathlib_pin','lake-manifest.json'),
 ('external_compact_lsi','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__OneDimGLSICompSmo.lean.raw.snapshot'),
 ('external_entropy_definition','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__Entropy.lean.raw.snapshot'),
 ('external_C2_definition','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot'),
 ('external_gaussian_definition','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianPoincare__Limit.lean.raw.snapshot'),
 ('external_closure_historical','runs/20261007-companion-priority/gaussian-functional-availability/import-closure-audit.json'),
 ('external_license','runs/20261007-companion-priority/gaussian-functional-availability/LICENSE.raw.snapshot'),
 ('external_toolchain','runs/20261007-companion-priority/gaussian-functional-availability/lean-toolchain.raw.snapshot'),
 ('external_mathlib_pin','runs/20261007-companion-priority/gaussian-functional-availability/lake-manifest.json.raw.snapshot'),
 ('closed_preread_provenance','runs/20261007-companion-priority/gaussian-flip-energy-preread/source-detail-packet.json'),
]
inputs=[]; data={}
for i,(role,path) in enumerate(paths):
    b=(ROOT/path).read_bytes(); data[role]=b
    rawname='input.%03d.raw.snapshot'%i; lfname='input.%03d.lf.snapshot'%i
    for name,value in [(rawname,b),(lfname,lf(b))]:
        with (OUT/name).open('xb') as f:f.write(value)
    inputs.append({'role':role,'path':path,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b),'raw_snapshot':rawname,'lf_snapshot':lfname})
assert sha(data['primary_whole'])=='ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d'
assert sha(data['parent36_signature'])=='d0adc2bfa9a83b8389706c10b31d10c64b5f7b6dba8c7454cd370a738ac7100e'
assert len(data['prospective37_signature_only'])==877
assert sha(data['external_compact_lsi'])=='ebe756ab83c2439881aa3805fd1de5073c5166f94fa7fbb6e641506502cc13c1'
manifest = dump('inputs.json',{'schema_version':1,'inputs':inputs,'scope':'Sealed interfaces only for34/36/37; no production bodies, Tests, blind or current compiler evidence read. Verified receipts are provenance, not a new proof review.'})
regions=[]
for role,a,b,purpose in [
 ('local_order_limit',420,424,'OrderClosedTopology and Preorder/TopologicalSpace context'),
 ('local_order_limit',466,482,'Genuine real limit order; NeBot filter, eventual inequality, no monotonicity'),
 ('local_multiplication_limit',112,139,'Tendsto.const_mul and separately continuous multiplication'),
 ('local_square_sign',199,215,'CommRing sub_sq_comm changes flip sign only'),
 ('local_zero_mass_continuity',29,63,'Actual continuous x log x through zero'),
 ('local_gaussian_definition',209,233,'gaussianReal mean/variance and degenerate variance convention'),
 ('external_compact_lsi',1,82,'External compact scalar theorem and all actual consumer proof lines'),
 ('external_compact_lsi',84,101,'EXCLUDED: fderiv rewrite/wrapper not needed for deriv target'),
 ('external_entropy_definition',34,49,'Actual homogeneous entropy definition'),
 ('external_C2_definition',44,48,'Actual C2 AND compact support'),
 ('external_gaussian_definition',38,40,'Gaussian standard variance1 ProbabilityMeasure'),
 ('external_gaussian_definition',149,151,'Gaussian measure alias and probability instance'),
]:
    rb=b''.join(lf(data[role]).splitlines(keepends=True)[a-1:b])
    name='region.%03d.lf.snapshot'%len(regions)
    with (OUT/name).open('xb') as f:f.write(rb)
    regions.append({'role':role,'start_line':a,'end_line':b,'purpose':purpose,'raw_LF_sha256':sha(rb),'snapshot':name})
regionmanifest=dump('regions.json',{'scope':'Selected prerequisite and literal source-consumer regions only; not an exhaustive Source Proof Graph or whole-project scan','regions':regions})
signature='''theorem compact_gaussian_logSobolev
    (f : ℝ → ℝ) (hf : ContDiff ℝ 2 f) (hs : HasCompactSupport f) :
    let γ : Measure ℝ := gaussianReal 0 1
    (∫ x, (f x)^2 * Real.log ((f x)^2) ∂γ) -
      (∫ x, (f x)^2 ∂γ) * Real.log (∫ x, (f x)^2 ∂γ) ≤
    2 * ∫ x, (deriv f x)^2 ∂γ
'''
with (OUT/'signature.prospective.txt').open('xb') as f:f.write(signature.encode('utf-8'))
parent34='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev.bernoulli_function_logSobolev'
parent36='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy.compact_count_gaussian_entropy_limits'
parent37='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit'
provenance={}
for key,role in [('34','parent34_verified_provenance'),('36','parent36_verified_provenance')]:
    x=json.loads(data[role].decode('utf-8'))
    provenance[key]={k:x.get(k) for k in ['verification_status','verified_commit','checked_working_head','verifier_id','lean_declarations']}
directscan={}
for role in ['external_compact_lsi','external_entropy_definition','external_C2_definition','external_gaussian_definition']:
    # Direct text scan only; no claim of compilation or transitive soundness.
    text=data[role].decode('utf-8')
    directscan[role]={'hits':[(i+1,s) for i,s in enumerate(text.splitlines()) if re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)],'imports':re.findall(r'^import\s+(.+)$',text,re.M)}
packet={
 'schema_version':1,'artifact_kind':'bounded-primary-first-source-API-preread','status':'CLOSED_SOURCE_DEPENDENCY_READINESS_ONLY',
 'actor':'gaussian_domain_preproof_reviewer_29','history':'Independent from root future compact-LSI writer. Earlier source graphs authored by this actor are not validated here; independently accepted parent states are provenance only.',
 'synthesis_first':'A genuine compact scalar Gaussian LSI follows from existing34 half Bernoulli LSI and36 entropy convergence after the still-unproved37 full flip-energy4 producer is independently admitted. Same literal count carrier means no product-law/AE adapter is needed. The only new integration mathematics is square-sign equality, constant multiplication of a real limit, and closed-order passage to limits.',
 'primary_first':{'contract':'primary.contract.json','primary_whole_raw_sha256':sha(data['primary_whole']),'anchors':['S4.E6 FIRST','S4.SS1.p4.3 first sentence'],'source_status':'SPHMC names Gaussian LSI plus separate Gaussian Talagrand, omitting this analytic background proof. Compact scalar target is an authored background prerequisite and is not the full printed FIRST inequality.'},
 'prospective_declaration':{'name':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev.compact_gaussian_logSobolev','module':'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactLogSobolev.lean','signature_file':'signature.prospective.txt','raw_LF_sha256':sha(signature.encode('utf-8')),'bytes':len(signature.encode('utf-8')),'status':'prospective shape only; not typechecked, not StatementSeal, not a theorem, no implementation or claim','public_inputs':['f : Real -> Real','hf : ContDiff Real 2 f','hs : HasCompactSupport f'],'no_public_certificate':['probability/law','normalized mass','positive f or positive mass','Integrable','LSI','weak convergence','entropy convergence','flip bound or limit']},
 'fixed_definitions':{
   'mu_N':'(Fintype.card (Fin N -> Bool) : ENNReal)^(-1) • Measure.count; genuine probability, total mass1 for allN includingN0',
   'S_N':'(Real.sqrt (N:Real))^-1 * sum_{j:Fin N} if eps j then1 else-1; exactly same in36/37',
   'gamma':'gaussianReal (0:Real) (1:NNReal); variance1, real Borel measure, not variance0 and not an arbitraryGaussian',
   'entropy':'integral f²*log(f²) - (integral f²)*log(integral f²); homogeneous function entropy, not canonical KL of a normalized RN representative',
   'energy':'integral (deriv f)^2; scalar real derivative, no extra Hessian/third derivative',
   'D37':'sum_j (f(S_N(update eps j(!eps j)))-f(S_N eps))² inside the actual integral',
   'D34':'sum_j (f(S_N eps)-f(S_N(update eps j(!eps j))))²; exact same pointwise function by sub_sq_comm'
 },
 'seven_slots':{
   'objects':'real f and actual fixed variance1Gaussian; finite count carrier is internal proof data',
   'domains':'C2compact implies real differentiability;36 produces true Gaussian L1 for f²,f²logf²,(deriv f)² and allN count L1,34/37 actual finite energies L1',
   'quantifiers':'every f satisfying C2compact; parent34 everyN and every signedh; parent36/37 limits overN=n+1 atTop',
   'assumptions':'Only C2 and compact support in public target; no probability/normalization/domain/inequality certificate',
   'conclusion':'literal homogeneous Gaussian entropy <=2 times actual derivative-square Bochner integral',
   'scopes':'compact scalar real background only; zero mass/signs included, no source-paper main or fullLSI credit',
   'constant_dependencies':'variance1; Bernoulli coefficient1/2 and full coordinate factor4 give exactly2; not normalized average energy'
 },
 'binder_classification':[{'binder':'f','kind':'DEFINITION/QUANTIFIED_OBSERVER'}, {'binder':'hf','kind':'SOURCE_EXTERNAL_COMPACT_BACKGROUND','scope':'C2 not C-infinity'}, {'binder':'hs','kind':'SOURCE_EXTERNAL_COMPACT_BACKGROUND','scope':'topological compact support'}, {'binder':'gamma let','kind':'DEFINITION','scope':'fixed actual variance1Gaussian'}, {'binder':'standard real measure/topology/order/field instances','kind':'TYPECLASS','scope':'canonical fixed Real; no new public assumption'}, {'binder':'all L1/probability/convergence facts','kind':'DERIVED_INTERNAL_PARENT_OUTPUT','scope':'must consume actual34/36/37 producers; not supplied certificate'}],
 'route_at_most_seven_steps':[
   '1. Fix literal mu_N,S_N and gamma exactly as parent36/37; set h_N(eps)=f(S_N eps).',
   '2. Use34 for every successorN=n+1 to produce actual count probability/L1 and homogeneous entropy inequality <=(1/2) integral D34.',
   '3. Internally identify D34=D37 by sub_sq_comm under each finite sum and integral; no finite sum/integral swap or real-product-law reconstruction needed.',
   '4. Consume36 for true Gaussian/allN observer L1 and the actual successor entropy limit including zero mass.',
   '5. AFTER37 is proved and independently admitted, consume its full energy L1 and successor integral limit4 times the same Gaussian derivative energy.',
   '6. Apply Filter.Tendsto.const_mul (1/2) and ring arithmetic to obtain half-energy limit2 times derivative energy.',
   '7. Apply le_of_tendsto_of_tendsto with NeBot atTop and Eventually.of_forall successor34 inequalities. No positive mass or monotonicity is needed.'
 ],
 'actual_parent_interfaces':{'34':{'declaration':parent34,'status':'existing verified producer','provenance':provenance['34']},'36':{'declaration':parent36,'status':'existing verified producer','provenance':provenance['36']},'37':{'declaration':parent37,'status':'prospective exact sealed interface only; root is proving, no compiled/admitted producer credit in this preread','raw_LF_sha256':sha(lf(data['prospective37_signature_only'])),'bytes':877}},
 'api_inventory':[
   {'name':'sub_sq_comm','path':'.lake/packages/mathlib/Mathlib/Algebra/Ring/Commute.lean','lines':[199,215],'hypotheses':'CommRing; specializes to Real','role':'literal D34/D37 equality'},
   {'name':'Filter.Tendsto.const_mul','path':'.lake/packages/mathlib/Mathlib/Topology/Algebra/Monoid/Defs.lean','lines':[112,139],'hypotheses':'TopologicalSpace, Mul, SeparatelyContinuousMul; genuine Tendsto; Real canonical','role':'half-energy convergence'},
   {'name':'le_of_tendsto_of_tendsto','path':'.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean','lines':[420,482],'hypotheses':'TopologicalSpace,Preorder,OrderClosedTopology on target; NeBot source filter; two genuine Tendsto and eventual order','role':'pass inequality to real limits'},
   {'name':"le_of_tendsto_of_tendsto'",'role':'equivalent all-index inequality variant at lines480-482'},
   {'name':'Real.continuous_mul_log','path':'.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean','lines':[29,63],'role':'zero-mass-safe convention already internal to36; no positive mass assumption added'}
 ],
 'hidden_domain_audit':{
   'gaussian_L1':'36 actually returns all three L1 facts; prospective final inequality can keep these internal rather than adding certificate binders. They may also be exposed as output conjuncts without changing the assumptions, but this recommended minimal signature is the inequality alone.',
   'count_L1':'34 returns h²,h²logh² and actualD34 integrability for all finiteN;36 returns observers and37 prospective returns true integral-of-full-sum D37 L1. Finite domains are not inferred from totalized integrals.',
   'same_law':'No arbitrary lambda_N or supplied weak law: identical literal inverse-card count and S_N lets reduce definitionally across34/36/37.',
   'limit_filter':'atTop on Nat is nontrivial; successor indices avoid sqrtN division arguments and retain allN domains separately.',
   'integral_convention':'Real-valued Bochner integrals are totalized in Lean but actual producer L1 facts are required and retained. Entropy is not replaced by a normalized probability density KL.',
   'missing_adapter':'None mathematically beyond37 admission and ordinary local elaboration. Carrier/square sign is pointwise algebra. No source sum-of-integrals conversion is reused silently.'
 },
 'boundary_cases':{
   'f_zero':'f=0 allowed. All entropy and Gaussian energy integrals0; no positive norm/mass hypothesis.',
   'zero_mass':'m=integral f²γ=0 is included; m logm=0 with Real.log0=0, and36 entropy convergence already uses continuous xlogx at0. No dividing bym or continuity of log alone.',
   'signed_f':'Squares make signed f admissible;34 holds for every realh, no positivity of f or absolute-value replacement.',
   'N0':'Finite count carrier Fin0->Bool is singleton with mass1; S0=0, h0 constant f0, homogeneous finite entropy0 and empty flip sum0.36 N0 derivative observer equals(deriv f0)² and need not be0. Only successors are used for limits.',
   'variance':'gamma varianceNNReal1;N0lawDirac0 is internalfiniteboundary, not targetGaussian degeneracy.',
   'regularity':'Only C2compact; no third derivative, global slope bound, cutoff certificate or positivity binder.'
 },
 'external_provenance':{'revision':'d0f506f0a695018265dccb33bcb05e2f5ca1c876','license':'Apache2 exact pinned LICENSE and source header','upstream_toolchain':'Lean4.32.0','upstream_mathlib':'81a5d257c8e410db227a6665ed08f64fea08e997','local_toolchain':'Lean4.33.0','local_mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d','external_theorem':'GaussianLSI.gaussian_logSobolev_CompSmo','source_lines':[45,82],'local_callable':False,'direct_text_scan':directscan,'historical_transitive_scan':'Existing static24file import-closure audit: no direct placeholder files/failures; historical static evidence only, no current external compilation/evaluation or whole-project rescan.'},
 'source_route_distinction':'SLT compact consumer uses real-product/sum-of-integrals/AE laws, source limits and Bernoulli_app. Authored ASTIS route uses identical Bool count parent34/36/37 and integral-of-full-sum, preserving the mathematical constant while avoiding unneeded source carrier adapters; not attributed to printed SPHMC proof.',
 'local_endpoint_boundary':'Existing LogSobolev exports bookkeeping and CanonicalLogSobolev consumes hLSI/admissibility/score/Dirichlet certificates. Neither is a variance1Gaussian analytic LSI producer nor Talagrand theorem. Current proposed compact theorem would add only the compact scalar analytic endpoint.',
 'typed_blockers':[{'class':'DEPENDENCY_NOT_YET_ADMITTED','first_unmet_dependency':parent37,'exact_residual':'Genuine allN full Bool flip-energy L1 and successor integral limit4, not its sealed signature or desired limit as a new binder. Root active37 proof was not read. This preread cannot schedule consumer proof credit until actual37 passes independent admission.'}],
 'intended_imports':['AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.BernoulliLogSobolev','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactEntropy','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy (future admitted37 only)','Mathlib.Topology.Order.OrderClosed','Mathlib.Topology.Algebra.Monoid.Defs','Mathlib.Algebra.Ring.Commute'],
 'remaining_open':['Actual37 proof and independent admission','Prospective compact-LSI theorem implementation/typecheck/independent review/publication','Noncompact W12/cutoff extension for literal32 positive sqrt-density','Finite-dimensional/Hilbert Gaussian LSI and tensorization','Canonical RN weak representative and pointwise derivative/score adapters','Genuine Gaussian Talagrand T2/metric/transport producer','SPHMC FIRST4.6 and remaining/bias/main/work/composition/cost claims'],
 'compiled_edges':[],'compiler_started':False,'proof_search':False,'claim':False,'new_statement_seal':False,
 'inputs':manifest,'regions':regionmanifest,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED'}
}
receipt=dump('source-detail-packet.json',packet)
synthesis='''The next minimal endpoint is compact scalar variance-1 Gaussian function LSI:
Ent_gamma(f^2) <= 2 integral (deriv f)^2, for f : Real -> Real,
ContDiff Real 2 f and HasCompactSupport f. No positivity or normalized-mass
input is needed. Existing34 and36 use the same actual inverse-card count
carrier as prospective37, so square-sign equality is the only flip adapter.
Once37 is genuinely admitted, half times full-energy4 and closed-order limit
give2. Until then37 is the first exact unmet dependency.

The entropy formula is literal homogeneous Bochner entropy. AllGaussian and
finite-count L1 domains are actual internal parent outputs, including zero
mass. N0 finite entropy/full flip energy vanish, whereas N0 derivative
observer need not vanish; the convergence clauses use successors only.

This packet is source/API readiness, not a StatementSeal or mathematical
completion. The external compact consumer is reference-only. Noncompact,
finite-dimensional/Hilbert LSI, T2 and the actual paper FIRST4.6 remain open.
'''
with (OUT/'bounded-synthesis.md').open('xb') as f:f.write(synthesis.encode('utf-8'))
core={'actor':packet['actor'],'artifact_kind':packet['artifact_kind'],'input_bindings':[{'role':x['role'],'path':x['path'],'raw_sha256':x['raw_sha256'],'lf_sha256':x['lf_sha256']} for x in inputs],'packet':receipt,'regions':regionmanifest,'prospective_signature_sha256':sha(signature.encode('utf-8'))}
runhash=sha(json.dumps(core,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
run=dump('run.json',{'deterministic_run_sha256':runhash,'deterministic_payload':core,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED'},'compiler_started':False})
for x in inputs:
    b=(ROOT/x['path']).read_bytes()
    assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'], x['path']
lease=json.loads((OUT/'lease.json').read_text(encoding='utf-8'))
lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':datetime.datetime.utcnow().isoformat()+'Z','deterministic_run_sha256':runhash,'all_input_bytes_rechecked_unchanged':True,'input_count':len(inputs),'scope':'Source/API prerequisite audit only; no37body/Test/blind exposure or proof/topology selfvalidation.'})
(OUT/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'packet':receipt,'run_sha256':runhash,'input_count':len(inputs),'regions':len(regions),'status':'CLOSED','compiler_started':False},indent=2))
