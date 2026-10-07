exec(open('runs/20261007-companion-priority/gaussian-product-entropy/whole-proof-review/freeze.py',encoding='utf-8').read().split('freeze=j(')[0])
import sys,re
sys.path.insert(0,str(Path('tools').resolve()))
import astis,astis_publication as pub
V='picard_commit_verifier_20261005'
C=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
freeze=j(R/'math-freeze.json'); initial=j(O/'input-bindings.initial.json')
assert C==freeze['checked_base_commit']
M=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],text=True).strip()
assert M=='db584cd6d46c92f209a44c0f1c829460d327499d'
for row in initial['inputs']:
 assert d(row['path'])['raw_sha256']==row['raw_sha256'] and d(row['path'])['lf_sha256']==row['lf_sha256'],row
 assert Path(row['raw_snapshot']).read_bytes()==Path(row['path']).read_bytes()
 assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
P=Path(freeze['inputs'][0]['path']); T=Path(freeze['inputs'][1]['path'])
sig=Path(freeze['inputs'][8]['path']).read_bytes()
assert len(sig)==1029 and sig.rstrip()+b' := by' in P.read_bytes()
extras=['.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',
 '.lake/packages/mathlib/Mathlib/Order/Filter/AtTopBot/Basic.lean',
 '.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Basic.lean',
 '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Real.lean',
 'AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean']
extra_rows=[]
for i,p in enumerate(extras):
 a=O/f'extra.{i:03d}.raw.snapshot';b=O/f'extra.{i:03d}.lf.snapshot';raw=Path(p).read_bytes()
 assert not a.exists() and not b.exists();a.write_bytes(raw);b.write_bytes(raw.replace(b'\r\n',b'\n'))
 extra_rows.append(dict(d(p),raw_snapshot=a.as_posix(),lf_snapshot=b.as_posix()))
apis=[
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean',419,438,'Fixed-point measurable pair maps used for every slice'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/HasFiniteIntegral.lean',198,205,'Bounded actual finite-measure L1'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',60,96,'Strong measurability of actual parameter integrals under SFinite'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',294,303,'Integrable.mul_prod'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',442,472,'Genuine L1 Fubini in both orders'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',531,547,'Product integral multiplication; active factor/product L1 established first'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',316,326,'Actual product probability instance'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',800,810,'Actual Dirac product stress law'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',1097,1117,'Dirac integrals stress'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',45,67,'All measurable/domination/integrable-bound/AE limit premises'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',31,54,'Scalar logsum inequality and continuous tlogt at zero'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/Basic.lean',125,142,'Log product/division nonzero premises'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/Basic.lean',370,385,'Log continuous away from zero'),
 ('.lake/packages/mathlib/Mathlib/Analysis/Normed/Group/Bounded.lean',96,107,'Compact-continuous bounded image'),
 ('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean',69,74,'epsilon_n=1/(n+1) true limit'),
 ('.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean',462,481,'Closed-order limit, genuine NeBot'),
 ('.lake/packages/mathlib/Mathlib/Order/Filter/AtTopBot/Basic.lean',53,67,'Nat atTop NeBot'),
 ('.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Basic.lean',280,294,'Reviewer finite Bool measurable function API'),
 ('AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean',38,100,'Actual smooth compact plateau Test producer'),
 ('.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Real.lean',211,260,'Actual variance1 Gaussian probability consumer')]
regions=[]
for i,(p,a,b,note) in enumerate(apis):
 data=b''.join(Path(p).read_bytes().splitlines(keepends=True)[a-1:b]);snap=O/f'api.{i:03d}.raw.snapshot'
 assert not snap.exists();snap.write_bytes(data)
 regions.append(dict(path=p,lines=[a,b],source_file=d(p),snapshot=d(snap),contract_checked=note))
api_receipt=put(O/'parent-api-review.json',dict(actor=V,regions=regions,actual_ASTIS_production_parents=[],actual_ASTIS_Test_parent=d(extras[-1]),Mathlib=M,scope='No project theorem is used by production. All invoked probability/product/Fubini/logsum/DCT APIs inspected; Test uses actual existing cutoff. API region snapshots supplement whole-file raw/LF pins.'))
names=re.findall(r'^private (?:def|theorem) (\w+)',P.read_text(encoding='utf-8'),re.M)
assert len(names)==15
edges={
 'bounded_product_entropy_subadditivity':['product_domains','bounded_product_inequality'],
 'bounded_product_inequality':['product_domains','phi_regularization_limit','positive_product_entropy','epsilon','epsilon_bounds','epsilon_limit','continuous_phi'],
 'phi_regularization_limit':['phi_bound','epsilon_bounds','epsilon_limit','continuous_phi','phi'],
 'positive_product_entropy':['product_domains','log_bound','scalar_logsum','bounded_integrable','phi'],
 'product_domains':['bounded_phi_domains','integral_bounds','phi'],
 'bounded_phi_domains':['phi_bound','bounded_integrable','continuous_phi','phi'],
 'phi_bound':['continuous_phi','phi'], 'continuous_phi':['phi'],
 'scalar_logsum':['phi'],'epsilon_bounds':['epsilon'],'epsilon_limit':['epsilon']}
reached=set();todo=['bounded_product_entropy_subadditivity']
while todo:
 n=todo.pop()
 if n in reached:continue
 reached.add(n);todo+=edges.get(n,[])
assert set(names)<=reached
scope_hits=[]
for p in [P,T]:
 for no,line in enumerate(astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8')).splitlines(),1):
  if astis.FORBIDDEN_REGEX.search(line):scope_hits.append(dict(path=p.as_posix(),line=no,text=line))
hits=astis.forbidden_pattern_hits();assert not hits and not scope_hits
assert 'import Tests' not in P.read_text(encoding='utf-8')
fake=put(O/'reachability-fake-closure.json',dict(actor=V,checked_base_commit=C,private_providers=names,reviewed_provider_count=15,reachable_private_providers=sorted(set(names)&reached),dependency_edges=edges,scope_hits=scope_hits,canonical_files=len(astis.lean_source_files()),canonical_hits=hits,producer_has_Tests_import=False,axioms=['propext','Classical.choice','Quot.sound'],conceptual_or_wrapper_certificate_premises='none'))
checks=j(O/'compiler-checks.json')['checks'];retry=j(O/'stress.retry1.status.json')
assert all(x['exit_code']==0 for x in checks[:3]) and checks[3]['exit_code']==1 and retry['exit_code']==0
assert 'sorryAx' not in (O/'direct-axioms.log').read_text(encoding='utf-8')
assert 'sorryAx' not in (O/'stress.retry1.log').read_text(encoding='utf-8')
assert 'Build completed successfully (3123 jobs).' in (O/'focused.log').read_text(encoding='utf-8')
diagnosis=put(O/'stress-diagnosis.json',dict(actor=V,original=checks[3],repair=retry,typed_class='REVIEWER_HELPER_API_ERROR',exact_changes=['measurable_of_countable applied to q explicitly','actual Dirac product and Dirac integrals rewritten explicitly before norm_num'],mathematical_route_unchanged=True,production_change=False,failed_sorryAx_scope='Only Lean error-recovery output for original failed reviewer stdin. No admitted theorem, production/Test or successful stress uses sorryAx.',pressure_result='True two Dirac probability laws have integral q=0 while the x=true off-support slice integral=1. All slices genuinely L1 and the public entropy inequality holds.'))
bindings=put(O/'input-bindings.json',dict(actor=V,checked_base_commit=C,original_freeze=d(R/'math-freeze.json'),original26_unchanged=True,inputs=initial['inputs']+extra_rows,stable_input_count=31,signature=d(freeze['inputs'][8]['path']),api_review=api_receipt,compiler_checks=d(O/'compiler-checks.json'),stress_retry=retry,source_verdict_inputs_in_mathematical_readset=False,scope='Stable mathematical/source-only preproof/API pins. New mutable publication/lesson/audit/decoder/source-review not read or frozen here.'))
body=[
 ('Actual domains','Measurable pointwise bounded nonnegative F on arbitrary measurable probability spaces yields real joint/all-pointwise-slice/marginal F and phi(F) L1. Parameter integral measurability uses actual finite/SFinite measures, no supplied marginal or domain certificate.'),
 ('Positive internal stage','delta>0 derives positive A,B,m and nonnegative C internally. All F log A/F log B and real R=A B/m products have explicit L1 before Fubini/integral algebra. R has true integral m, not 1; m division occurs only in this strictly positive stage.'),
 ('Scalar algebra and signs','r=bc/m>0; multiply x-1<=x log x at x=a/r by r, expand nonzero real logs, obtain a-r<=phi(a)-a log b-a log c+a log m. Integrating cancels actual m-m and produces exactly J_A+J_B<=J_F+phi(m).'),
 ('Zero-safe regularization','epsilon_n=1/(n+1)>0, <=1, ->0. Probability mass1 and existing L1 give exact regularized marginals/mass A+epsilon/B+epsilon/m+epsilon. Continuous tlogt including zero and compact bound on [0,C+1] give a single integrable finite-measure dominating constant for each DCT.'),
 ('Limit and conclusions','Real closed order at actual Nat atTop NeBot combines convergent marginal/joint phi integrals and phi(m+epsilon), without logarithm/division of original zero mass or fibers. Final theorem returns eight domain components plus the inequality, nine conjunction components total.'),
 ('Actual signed compact Gaussian consumer','Test constructs g=x*smoothUnitCutoff and signed nonseparable g(x)g(y)+(g(x)g(y))^2. Actual bound/measurability for its square, C2 compact support, sign change and zero fiber are proved and call the same general theorem under gaussianReal 0 1.'),
 ('Complete private reachability','Both full files inspected; production has 2 private definitions and 13 private theorems, all reachable from the sole public declaration. Test has 3 genuine private functions used by concrete consumers. No copied final entropy certificate, desired-inequality premise, supplied normalization, fake closure or production Tests import.')]
math=put(O/'math.review.json',dict(actor=V,advance_id=freeze['advance_id'],verification_status='passed-scoped',verdict='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF',blockers=[],checked_base_commit=C,exact_commit_VERIFIED=False,all_private_providers_reviewed=15,full_modules_reviewed=[d(P),d(T)],input_bindings=bindings,actual_parent_API_review=api_receipt,reachability_fake_closure=fake,exact_statement=dict(bytes=1029,raw_LF_sha256=sha(sig),caller_inputs=['MeasurableSpace X,Y','actual probability measures mu,nu','F : X x Y -> Real measurable','F pointwise nonnegative','exists a global finite real upper bound'],conclusion='Actual joint/all-slice/marginal L1 and J_A+J_B<=J_F+phi(m), including zero fibers/zero mass.'),body_mathematical_audit=[dict(component=a,conclusion=b) for a,b in body],fresh_focused=dict(jobs=3123,evidence=checks[0]),fresh_compiler_evidence=checks[:3],standard_axioms=['propext','Classical.choice','Quot.sound'],meaningful_zero_mass_stress=dict(result='passed',evidence=retry,diagnosis=diagnosis),toolchain='leanprover/lean4:v4.33.0',Mathlib=M,initial_freeze_before_after=dict(inputs=26,unchanged=True),independence=dict(proving_writer='root',reviewer=V,new_blind_or_source_verdict_read=False,preproof_contract_source_topology='Frozen source-only scope pins; not substituted for mathematical proof or final source approval.'),remaining_boundary=['Only bounded heterogeneous binary product entropy producer; pointwise nonnegative bounded class is authored scope.','Unbounded entropy theorem and finite-product induction/tensorization not proved by this packet.','Multidimensional/Hilbert/noncompact Gaussian LSI, T2/FIRST4.6, both paper mains, query cost and composition remain open.','Final source-blind/source review, exact-commit VERIFIED and shared repository/reader/PURIFIED delivery not claimed by this mathematical review.'],leases=dict(read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED')))
run=dict(actor=V,advance_id=freeze['advance_id'],checked_base_commit=C,math_review=math,input_bindings=bindings,compiler=d(O/'compiler-checks.json'),stress_retry=d(O/'stress.retry1.status.json'),api_review=api_receipt,fake_closure=fake,verdict='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF')
run['deterministic_run_sha256']=pub.digest(run);run['hash_recipe']='astis_publication.digest all fields excluding deterministic_run_sha256/hash_recipe'
run_desc=put(O/'math.review.run.json',run)
opening=(O/'lease.json').read_bytes();op=O/'lease.open.raw.snapshot.json';assert not op.exists();op.write_bytes(opening)
closed=dict(status='CLOSED',actor=V,checked_base_commit=C,read='CLOSED',write='CLOSED',compiler='CLOSED',Python='CLOSED',math_review=math,run=run_desc,opening_manifest=d(op),new_decoder_source_verdict_read=False,canonical_mutations=[])
(O/'lease.json').write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(math_review=math,run=run_desc,input_bindings=bindings,private_providers=15,canonical_fake_files=len(astis.lean_source_files()),leases='ALL CLOSED'),indent=2))
