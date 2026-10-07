import hashlib, json, pathlib, re, subprocess
from datetime import datetime, timezone
ROOT=pathlib.Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52/whole-proof-review52'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
freeze=OUT.parent/'math-freeze.json'
frozen=json.loads(freeze.read_text(encoding='utf-8'))
actual=[pin(ROOT/e['path']) for e in frozen['inputs']]
assert len(actual)==333 and len(set(e['path'] for e in actual))==333
assert actual==frozen['inputs']
write(OUT/'final.input-bindings.json',{'checked_utc':now(),'freeze':pin(freeze),'count':333,'strict_all_pins_pass':True,'actual_inputs':actual,'errors':[]})
prod=ROOT/'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean'
test=ROOT/'Tests/ProximalBPSGaussianReflectedMean.lean'
body=prod.read_text(encoding='utf-8')
signature=body[body.index('theorem gaussian_reflected_mean_c1'):].split('\n := by',1)[0]+'\n'
prospective=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean-preproof52/prospective-statement.txt'
assert signature==prospective.read_text(encoding='utf-8') and len(signature.encode())==497
status=json.loads((OUT/'compiler.status.json').read_text())
log=(OUT/'compiler.log').read_text(encoding='utf-8')
assert status['exit_code']==0 and 'Build completed successfully (3893 jobs).' in log
fake=[]
for p in [prod,test]:
    for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
        if re.search(r'\b(axiom|sorry|admit|unsafe)\b|Prop\s*:=\s*True|:=\s*trivial',line):fake.append({'path':str(p),'line':i,'text':line})
assert not fake
assert 'local instance' not in body and 'private' not in body
git=lambda args:subprocess.check_output(['git']+args,cwd=ROOT).decode().strip()
base=git(['rev-parse','HEAD'])
mathlib=git(['-C','.lake/packages/mathlib','rev-parse','HEAD'])
assert base==frozen['checked_base_commit'] and mathlib=='db584cd6d46c92f209a44c0f1c829460d327499d'

ingredients=[
 {'labels':['K','K\'','F','G','N','D','Z'],'reason':'K(y,x)=exp(-||y-x||^2/(2 eta)); F=K f(2x-y); K\' v=-(K/eta)<y-x,v>; G v=-K Df(2x-y)v+f(2x-y)K\'v. N,D,Z are the actual mu integrals. This is the correct derivative in the y parameter, including both the reflected observer negative sign and Gaussian likelihood term.'},
 {'labels':['hdfC','Mf','hMf','Md','hMd','hMf0'],'reason':'C1 gives continuous fderiv; compact support of f implies compact support of its fderiv. Continuous compactly supported f and fderiv have global norm bounds Mf and Md. Mf nonnegative follows by evaluating the norm bound at 0. All are produced within the body, not certificates in the public assumptions.'},
 {'labels':['hK'],'reason':'K>0 by exp positivity; K<=1 because eta>0 and squared norm nonnegative. The elementary t exp(-t)<=exp(-1)<=1 with t=r^2/(2 eta) gives K r^2<=2 eta. No moment, dimension positivity or input density is used.'},
 {'labels':['hKderiv'],'reason':'Differentiate squared Hilbert norm after z-x, multiply by -1/(2 eta), exponentiate. Extensionality and ring normalization identify the resulting linear functional with K\'. The analytic Gaussian sign and factor eta are correct.'},
 {'labels':['hKbound'],'reason':'r<=1+r^2 gives Kr<=K+Kr^2<=1+2 eta. The dual inner product functional has norm r, so ||K\'||=(K/eta)r<=(1+2 eta)/eta. Strict eta positivity justifies absolute-value and division steps. This global bound works also at rank zero.'},
 {'labels':['hGbound'],'reason':'Triangle inequality and scalar-operator norm multiplication give ||G||<=K||Df||+|f|||K\'||<=Md+Mf(1+2 eta)/eta. The only needed nonnegative upper factor Mf is explicitly proved; derivative and Gaussian bounds give the other order premises. The dominating function is constant in x and y.'},
 {'labels':['hFmeas','hGmeas'],'reason':'For fixed y, all Gaussian, affine-reflection, f and fderiv factors are continuous in x, including the innerSL operator valued factor; hence they are AE strongly measurable for the Borel probability law. Standard finite dimensional real Hilbert topology supplies the usual second countability/measurability instances.'},
 {'labels':['hFI'],'reason':'|F(y,x)|=K|f(2x-y)|<=Mf and the constant Mf is integrable under a probability law. Thus the numerator Bochner integral is genuine, not its undefined fallback.'},
 {'labels':['hFderiv','ha','ho','ho\''],'reason':'The affine map z -> 2x-z has derivative -id; chain rule gives -Df at 2x-y. convert closes only definitional structure equalities and then linear-map extensionality. Multiplying with the actual K derivative yields G. The preserved small chain reproducer verifies this route; production retains no exploratory local real scalar instance.'},
 {'labels':['hdN'],'reason':'Mathlib hasFDerivAt_integral_of_dominated_of_fderiv_le is instantiated with neighborhood univ. Its six substantive conditions are supplied: eventual F measurability, F(y) integrability, G(y) measurability, mu-AE uniform all-z norm bound, integrable constant bound, and actual all-z pointwise HasFDerivAt. The order of AE and forall neighborhoods is stronger than needed, so no parameter-dependent exceptional set is hidden.'},
 {'labels':['hDC'],'reason':'Mathlib continuous_of_dominated receives G measurability at every y, a common integrable constant bound and for every x continuity in y. The latter follows from continuous fderiv, affine reflection and Gaussian dual factors. D is therefore continuous as an operator-valued integral; no derivative-continuity premise was supplied.'},
 {'labels':['hNC'],'reason':'contDiff_one_iff_hasFDerivAt uses the actual continuous derivative candidate D and hdN at each point to conclude N is C1. This is stronger evidence than isolated differentiability or an assumed derivative identity.'},
 {'labels':['hparent','hZC','hZ'],'reason':'The sole ASTIS production theorem call is gaussian_convolution_potential_c2 mu h_eta. The proof extracts exactly its C2Z conjunct and positive C_eta*Z(y) conjunct. If Z(y)=0, that strictly positive product is zero, contradiction. No density identity, posterior score, covariance or additional parent conclusion is required. C2 lowers to C1 in the final quotient.'},
 {'labels':['hKI','hlike'],'reason':'The same K<=1 domination proves likelihood integrability for every y; norm_sub_rev identifies the x-y posterior weight with the y-x K. Probability implies nonzero mu, so isProbabilityMeasure_tilted applies genuinely at every y.'},
 {'labels':['hmean','hobs','hmapI','hw'],'reason':'The bounded reflected observer is integrable under the genuine tilted probability. Affine reflection is measurable; integrable_map_measure yields f integrable under its map. integral_map then pulls the integral back, integral_tilted exposes the literal normalized likelihood, norm_sub_rev aligns K, and integral_div/ring gives exactly N(y)/Z(y). No AE disintegration version or AE derivative transfer is used.'},
 {'labels':['final change','simp_rw hmean','hNC.div'],'reason':'The final goal is the displayed literal R and reflected pushforward S. Pointwise hmean rewrites this entire function at every parameter to N/Z; global C1 division uses hNC, lowered hZC and hZ. It proves exactly the sealed 497-byte statement, with no extra assumptions or helper theorem churn.'}
]
apis=[
 {'role':'compact-observer bounds and regularity','names':['ContDiff.continuous_fderiv','HasCompactSupport.fderiv','HasCompactSupport.exists_bound_of_continuous','ContDiff.continuous','ContDiff.differentiable_one'],'files':['.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/Defs.lean','.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Const.lean','.lake/packages/mathlib/Mathlib/Analysis/Normed/Group/Bounded.lean'],'audit':'Reviewed the exact hypotheses. No extra smoothness order or support derivative assumption is needed.'},
 {'role':'Gaussian and affine calculus','names':['hasFDerivAt_id','HasFDerivAt.sub_const','HasFDerivAt.norm_sq','HasFDerivAt.const_mul','HasFDerivAt.exp','HasFDerivAt.const_sub','HasFDerivAt.comp','HasFDerivAt.mul','Real.exp_pos','Real.exp_le_one_iff','Real.mul_exp_neg_le_exp_neg_one','innerSL_apply_norm','innerSL_apply_apply'],'audit':'The usual Hilbert real Frechet calculus plus elementary exponential inequality. All conversions identify genuine derivatives; ring/ext are algebraic transports, not theorem certificates.'},
 {'role':'integration and domination','names':['Continuous.aestronglyMeasurable','integrable_const','Integrable.mono\'','hasFDerivAt_integral_of_dominated_of_fderiv_le','continuous_of_dominated','contDiff_one_iff_hasFDerivAt','integrable_map_measure','integral_map','integral_tilted','integral_div','integral_congr_ae','isProbabilityMeasure_tilted'],'files':['.lake/packages/mathlib/Mathlib/Analysis/Calculus/ParametricIntegral.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean'],'audit':'Exact parameter/AE quantifier order, strong measurability, integrability, true positive normalization and map premises are matched in the body. Quotient and tilted integral APIs cannot hide a fallback here because all relevant integrability and nonzero conditions are produced.'},
 {'role':'quotient regularity','names':['ContDiff.of_le','ContDiff.div'],'files':['.lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/Operations.lean'],'audit':'The global nonvanishing denominator requirement is explicitly discharged from parent positivity.'},
 {'role':'elementary proof infrastructure','names':['norm_nonneg','sq_nonneg','neg_nonpos','div_nonpos_of_nonpos_of_nonneg','mul_le_mul','mul_le_mul_of_nonneg_left','add_le_add','norm_add_le','norm_mul','norm_smul','norm_neg','abs_div','abs_neg','abs_of_pos','div_le_iff₀','div_le_div_iff_of_pos_right','Filter.Eventually.of_forall','filter_upwards','fun_prop','ring','nlinarith','simp','norm_num','positivity','ext','convert'],'audit':'Order/absolute-value/division facts use eta positivity, K positivity, norm nonnegativity or bound certificates proved locally. Automation closes these displayed geometric/algebraic and measurability obligations; no custom tactic, unsafe evaluation, theorem assumption closure or private provider appears.'}
]
additional=[
 'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianConvolutionRegularity.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean']
for row in apis: additional+=row.get('files',[])
additional=sorted(set(additional))
receipt={
 'schema_version':1,'reviewer':'whole_math52','role':'independent-whole-mathematical-proof-review','advance_id':frozen['advance_id'],'verdict':'ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER',
 'checked_base_commit':base,'candidate_commit_boundary':'New production and Test are untracked frozen candidate files on the named base commit; acceptance binds exact raw/LF source hashes, not an invented candidate commit.',
 'reviewed_declarations':frozen['mathematical_declarations'],'strict_frozen_input_count':333,'strict_pin_validation':['pre.input-bindings.json','post.input-bindings.json','final.input-bindings.json'],'math_freeze':pin(freeze),'source_inputs':[pin(prod),pin(test)],
 'sealed_signature':{'LF_bytes':497,'LF_sha256':sha(signature.encode()),'exact_match_to_prospective_and_accepted_signature':True},
 'independence':{'formalizer':'companion_root_20261005','verifier':'whole_math52','source_blind':False,'source_reviewer':False,'decoder_output_inspected':False,'later_source_verdict_inspected':False,'canonical_edits':False,'VERIFIED_transition_authored':False},
 'scope':'For any Borel probability law on a finite-dimensional real Hilbert space (including rank zero), eta>0 and signed compact C1 observer f, the literal normalized quadratic posterior mu.tilted(-||x-y||^2/(2 eta)) pushed forward by x -> 2x-y has a globally C1 f-mean. Authored analytic generalization serving PBPSv1 Appendix C.1; not a printed paper theorem.',
 'proof_ingredient_audit':ingredients,'api_audit':apis,'additional_reviewed_dependencies':[pin(ROOT/p) for p in additional],
 'hidden_contract_audit':{'integrability':'All likelihood, numerator, derivative domination, posterior observer and mapped observer integrability are derived internally from probability and Gaussian/compact bounds. No input moments or density required.','positivity':'Positive eta and strictly positive Gaussian weight, and parent positive normalizer product prevent zero-normalizer fallback at every y.','measurability':'Continuous f, fderiv, likelihood, dual and affine reflection yield the actual required strong/AE measurability. Borel finite-dimensional Hilbert structure supplies standard topology/measure instances.','differentiation':'Genuine parameter Frechet derivative with correct reflection sign; common univ neighborhood and mu-AE all-parameter domination; derivative continuity derived separately.','boundary':'No integration by parts, boundary decay, representative differentiability transfer, higher derivatives of f or V, or input density assumption enters the new production theorem.','rank_zero':'No Nontrivial, finrank positivity, centering or zero-mean premise; zero-dimensional constants are compactly supported and genuine posterior/map probability yields nonzero mean 1.'},
 'tests':[
  {'name':'Tests.ProximalBPSGaussianReflectedMean.actual_pbps_reflected_kernel_mean','reason':'Uses the SAME actual Gibbs mu=volume.tilted(-V) and independent Gaussian joint J, under alpha>0, alpha<=beta, V C2, original two-sided Hessian bounds, eta>0 and beta*eta<=1. MacroscopicEnergy produces mu probability internally; inspection traces it to positive Gibbs normalizer/integrability in ConditionalGradientEnergy, not a caller certificate. GaussianConditionalKernel constructs an everywhere equal literal posterior Markov kernel and IsCondKernel for J.map swap. The new C1 result is consumed after all-y fiber rewriting for every smooth compact f. It does not transfer derivatives from an AE version or assert the source-volume S_y identity.'},
  {'name':'Tests.ProximalBPSGaussianReflectedMean.rank_zero_noncentered_mean','reason':'Instantiates E=EuclideanSpace R (Fin 0), stdGaussian, eta=1 and f=1. Uses new theorem for C1; separately proves the actual tilted posterior is a probability by all-y kernel equality, its affine pushforward is a probability, integral 1 is 1 at each y, and exact function equality gives fderiv=0. This is a noncentered actual posterior consumer, not a zero observer or vacuous premise.'}
 ],
 'production_parent_usage':{'only_ASTIS_call':'AutoSamplingTheory.TechnicalLemmas.Measure.GaussianConvolutionRegularity.gaussian_convolution_potential_c2','used_conjuncts':['positive C_eta*Z','ContDiff R 2 Z'],'parent_proof_check':'Inspected the relevant whole parent producer and its internal Gaussian normalizer proof: probability-based positive integral, internally dominated first/second derivatives and continuous second derivative. Parent existing private scalar structures are outside new module; new module retains no exploratory instance.'},
 'fake_closure_scan':{'files':[str(prod.relative_to(ROOT)),str(test.relative_to(ROOT))],'forbidden_matches':fake,'new_private_providers':[],'new_local_structure_instances':[],'axioms_for_all_three':'[propext, Classical.choice, Quot.sound]','proof_body_ingredients_all_consumed':True,'note':'Unused-variable warnings in constant-observer binders and replayed parent lint/info messages do not signal a mathematical closure; final compiler success and axiom inventories are authoritative for this focus.'},
 'compiler':status,'build_interpretation':'One fresh independent lake build invocation; Lake replayed current checked artifacts and completed 3893 jobs successfully. This is a focused compilation gate, not the aggregate tools/astis.py check or new source-fidelity admission.',
 'toolchain':{'ELAN_TOOLCHAIN_unset':True,'repository_lean':'leanprover/lean4:v4.33.0','actual_mathlib_commit':mathlib,'manifest_mathlib_rev':mathlib,'lake_manifest':pin(ROOT/'lake-manifest.json'),'LEAN_NUM_THREADS':2,'PYTHONUTF8':1},
 'retired_route_review':'Preserved failed prod3/4/5 fingerprint and successful small chain-diagnosis0 establish an API structure-equality obstruction, resolved by explicit definitional conversion. Frozen negative evidence is preserved and hashed; production6 uses the converted chain rule with unchanged binders, no ad hoc real structure instances.',
 'remaining_boundary':['Independent decoder and anti-anchored source-review/publication admission are separate and not certified here.','The printed PBPS source-volume S_y identity still needs the actual all-y adapter; no claim that every conditional version is pointwise equal.','Literal Tf closed-gradient membership, compact-test density/closedness and arbitrary rough B.13 remain separate.','Gamma, half-turn/hypocoercivity, invariance, main results, algorithm errors, nonexplosion, expected query cost and four-paper actual-input composition are not established by this leaf.','Aggregate project gate, Registry/site graph and human-reader publication/purification are stabilization-owner work.'],
 'blockers':[],'decision_reason':'Complete numerator calculus, common domination and derivative continuity are genuinely proved; denominator regularity/nonvanishing joins the one admitted producer; actual integral identity is everywhere and integrable; genuine Gibbs/kernel and rank-zero noncentered Tests consume the result. No added analytic hypothesis, fake closure, hidden certificate, circular assumption or wrapper-only delta was found in this exact scoped candidate.',
 'completed_utc':now()
}
write(OUT/'receipt.json',receipt)
outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ('lease.json','run.json')]
run={'schema_version':1,'reviewer':'whole_math52','advance_id':frozen['advance_id'],'status':'COMPLETE','verdict':receipt['verdict'],'checked_base_commit':base,'freeze':pin(freeze),'strict_input_count':333,'receipt':pin(OUT/'receipt.json'),'outputs':outputs,'compiler_pid':status['process_id'],'compiler_exit_code':status['exit_code'],'hash_contract':'run_sha256 = SHA256 of UTF8 json.dumps(run without run_sha256, ensure_ascii=False, sort_keys=True, separators=(comma,colon)); stored file raw/LF is pinned by closed lease.','completed_utc':now()}
run['run_sha256']=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
write(OUT/'run.json',run)
lease=json.loads((OUT/'lease.json').read_text())
lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',reviewer='CLOSED',closed_utc=now(),compiler_pid=status['process_id'],compiler_exit_code=status['exit_code'],run_sha256=run['run_sha256'],actual_final_outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'],closure_order='This actual closed lease is written last after receipt and logical/raw/LF run bindings.')
write(OUT/'lease.json',lease)
assert all(json.loads((OUT/n).read_text())['status']=='CLOSED' for n in ['lease.json','compiler.lease.json'])
print(json.dumps({'verdict':receipt['verdict'],'compiler_pid':status['process_id'],'strict_pins':333,'receipt':pin(OUT/'receipt.json'),'run':pin(OUT/'run.json'),'run_sha256':run['run_sha256'],'lease':pin(OUT/'lease.json')}))
