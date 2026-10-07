from reviewer import *
import re
sys.path.insert(0,str(ROOT/'tools'))
import astis
f=j(R/'math-freeze.json'); initial=j(O/'initial-input-bindings.json')
for x in initial['inputs']:
 assert d(ROOT/x['original']['path'])==x['original']
 assert (ROOT/x['snapshot']['path']).read_bytes()==(ROOT/x['original']['path']).read_bytes()
assert head()==f['checked_base_commit']
code=(ROOT/f['inputs'][0]['path']).read_bytes().replace(b'\r\n',b'\n')
sig=(ROOT/f['inputs'][12]['path']).read_bytes().replace(b'\r\n',b'\n')
assert len(sig)==678 and sig.rstrip()+b' := by' in code
assert b'import Tests' not in code
extra_paths=['.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Pi.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LocallyIntegrable.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean','.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Real.lean','runs/20261007-companion-priority/gaussian-product-entropy/whole-proof-review/math.review.json','runs/20261007-companion-priority/gaussian-product-entropy/whole-proof-review/input-bindings.json','runs/20261007-companion-priority/gaussian-compact-lsi/whole-proof-review/math.review.json']
extras=[]
for n,p in enumerate(extra_paths):
 snap=O/f'extra.{n:02}.raw.snapshot';assert not snap.exists();snap.write_bytes((ROOT/p).read_bytes());extras.append(dict(original=d(ROOT/p),snapshot=d(snap)))
binding=put(O/'input-bindings.json',dict(checked_base_commit=head(),original_root_freeze=d(R/'math-freeze.json'),original_input_count=44,extra_input_count=len(extras),total_input_count=44+len(extras),inputs=initial['inputs']+extras,all_initial_44_raw_lf_unchanged=True,initial_exposure=initial['inputs'][0]['original'],exclusion='Root later authored publication/lessons/audit/decoder/source verdicts are outside this mathematical evidence.'))
api_specs=[('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean',290,323,'Actual finite/probability product, including empty-index mass one'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean',807,819,'True piFinSuccAbove pushforward and inverse Fin.cons'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',1077,1085,'Integral transport with actual MP and measurable embedding'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',381,397,'Real integrability transported by the same MP'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LocallyIntegrable.lean',612,625,'Continuous compact support gives true L1 for locally finite Borel law'),('.lake/packages/mathlib/Mathlib/Analysis/Calculus/FDeriv/Const.lean',374,395,'Directional derivative support is contained in original tsupport'),('.lake/packages/mathlib/Mathlib/Analysis/Calculus/Deriv/Pi.lean',19,38,'Update derivative is exactly Pi.single i 1'),('.lake/packages/mathlib/Mathlib/Topology/Algebra/Support.lean',280,302,'Compact composition along closed embedding and zero-preserving scalar map'),('.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Real.lean',219,234,'GaussianReal true mean/variance law and actual probability normalization'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',325,380,'Actual outer integrability and Fubini with joint L1')]
apirows=[]
for n,(p,a,b,reason) in enumerate(api_specs):
 raw=(ROOT/p).read_bytes(); lines=raw.splitlines(keepends=True);s=O/f'api.{n:02}.raw.txt';assert not s.exists();s.write_bytes(b''.join(lines[a-1:b]));apirows.append(dict(file=d(ROOT/p),start=a,end=b,checked_semantics=reason,raw_excerpt=d(s)))
parents=[]
for p,v in [('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactLogSobolev.lean','runs/20261007-companion-priority/gaussian-compact-lsi/verified.json'),('AutoSamplingTheory/TechnicalLemmas/InformationTheory/ProductEntropy.lean','runs/20261007-companion-priority/gaussian-product-entropy/verified.json')]:
 parent=j(ROOT/v); assert parent['verification_status']=='passed-scoped'
 parents.append(dict(module=d(ROOT/p),verified_receipt=d(ROOT/v),verified_commit=parent['verified_commit'],reuse='Previous independent complete body review bound to exact unchanged module bytes; actual invoked public interface read again. Scalar parent full body read again.'))
apireview=put(O/'parent-api-review.json',dict(pinned_mathlib=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT/'.lake/packages/mathlib').decode().strip(),parents=parents,api_regions=apirows,all_parent_review_input_hashes_equal_root_freeze=True))
names=re.findall(r'^private theorem (\w+)',code.decode(),re.M)
assert names==['compact_domains','original_slices','split_law','empty_entropy','coordinate_derivatives','split_square_class','split_entropy_bound','finite_lsi']
edges={'compact_gaussian_pi_logSobolev':['compact_domains','finite_lsi'],'finite_lsi':['empty_entropy','compact_domains','split_law','split_entropy_bound','original_slices','coordinate_derivatives','GaussianCompactLogSobolev.compact_gaussian_logSobolev'],'coordinate_derivatives':['original_slices'],'split_entropy_bound':['split_square_class','ProductEntropy.bounded_product_entropy_subadditivity']}
seen=set();todo=['compact_gaussian_pi_logSobolev']
while todo:
 a=todo.pop()
 if a in seen:continue
 seen.add(a);todo+=edges.get(a,[])
assert all(n in seen for n in names)
reachable=[];todo=[f['inputs'][0]['path']];done=set()
while todo:
 p=todo.pop()
 if p in done:continue
 done.add(p);t=(ROOT/p).read_text(encoding='utf-8');reachable.append(d(ROOT/p))
 for mod in re.findall(r'^(?:public )?import\s+(AutoSamplingTheory[\w.]*)',t,re.M):
  file=mod.replace('.','/')+'.lean'
  if (ROOT/file).exists():todo.append(file)
assert all('Tests/' not in x['path'] for x in reachable)
hits=astis.forbidden_pattern_hits();assert not hits,hits
fake=put(O/'reachability-fake-closure.json',dict(checked_base_commit=head(),canonical_files_scanned=len(astis.lean_source_files()),forbidden_hits=hits,scanner=d(ROOT/'tools/astis.py'),private_count=8,all_private_bodies_read=True,private_providers=names,actual_local_dependency_edges=edges,all_eight_reachable=True,dimension_IH='finite_lsi recurses only to n from n+1; no same-dimension hypothesis or public desired-bound certificate',reachable_canonical_module_count=len(reachable),reachable_canonical_modules=reachable,production_imports_Tests=False,standard_axioms=['propext','Classical.choice','Quot.sound'],failed_root_tests='tests.0 recovery sorryAx and tests.1 heartbeat failure are retained diagnostic logs only; no failed-output theorem admitted. Independent successful Test/std3 logs checked.'))
checks=j(O/'compiler-checks.json');assert len(checks['checks'])==4 and all(c['exit_code']==0 for c in checks['checks'])
for label in ['test-axioms','stress']:
 t=(O/f'{label}.log').read_text(encoding='utf-8');assert 'sorryAx' not in t and 'depends on axioms:' in t
audit=[
 dict(component='compact_domains',conclusion='True Gaussian probability/finite Borel law. f², tlogt(f²), each continuous directional square and finite sum have actual L1 by compact support. tlogt continuous at zero and derivative support inside original tsupport; no totalized integral is substituted for an L1 proof.'),
 dict(component='original_slices',conclusion='Only original fixed-coordinate f slices. Fin.consEquivL gives continuous linear/homeomorphic split; each fixed-coordinate inclusion is a closed embedding, so every slice is C2 and compact. No square-root marginal smoothness assumption.'),
 dict(component='split_law',conclusion='Actual Gaussian pi measure via inverse piFinSuccAbove at 0 and literal Fin.cons; every scalar/tail law has mass1, including Fin0. MP/embedding identities are for the same law.'),
 dict(component='empty_entropy',conclusion='Fin0 is singleton; any observer equals f0. Actual probability integrates constants to themselves, homogeneous entropy cancels, energy empty sum is zero. Supplementary signed -2 test independently checks nontrivial mass4 and 4log4, not log1=0 shortcut.'),
 dict(component='coordinate_derivatives',conclusion='Chain rules at genuine C2 points. Update derivative is Pi.single i1; Fin.cons_update identifies tail path and Function.update_eq_self identifies evaluation. Head ordinary deriv and tail Frechet directions equal exact full coordinate directions, including equality/order.'),
 dict(component='split_square_class',conclusion='Measurable actual fcons², nonnegative, internally bounded by max(D,0)² from original compact continuous f. No caller bound, positive mass/fiber, density or normalization certificate.'),
 dict(component='split_entropy_bound',conclusion='Parent39 joint Phi L1 and marginal Phi L1 give true outer conditional entropy L1 and legal integral subtraction/Fubini. J_A+J_B <= J_F+Phi(m) rearranges exactly to J_F-Phi(m) <= integral U+integral V, including m0; no division or positive-mass restriction.'),
 dict(component='finite_lsi',conclusion='Strict dimension induction. Tail original slices use IH constant2; head original slices use scalar38 constant2. Actual energy joint L1 transported with same split MP justifies integrated inequalities/Fubini. Fin.sum_univ_succ and legal integral_add identify full energy as head+tail. The entropy inequality yields exact2, no dimension factor or sup operator norm.'),
 dict(component='public and Test',conclusion='Sole public target takes only n,f,C2,compact and returns all four domains plus homogeneous entropy bound. Test derives actual support/smoothness for signed nonseparable n2 and signed n1 observers; genuine alln zero and n0 constant1. No copied premise/consumer closure. Actual sign test proves both signs.')]
remaining=['Independent freshblind/anti-anchored source admission, exact committed VERIFIED and serialized repository ProofSeal are not claimed by this mathematics-only review.','This is actual compact C2 finite Pi-law Gaussian LSI with coordinate-square-sum energy; finite Hilbert law/orthonormal-gradient Parseval and noncompact extension remain open.','Gaussian T2, SPHMC FIRST4.6/full paper algorithms/main results/warmness/bias/work/query cost/composition and PBPS obligations remain open.','Complete reader/Test inline/copy/download/browser/live/PURIFIED/merged delivery are not established.']
lease=j(O/'lease.json');put(O/'lease.open.raw.snapshot.json',lease);lease.update(status='CLOSED',read='CLOSED',write='CLOSED',compiler='CLOSED',python='CLOSED',sessions='CLOSED',compiler_checks=d(O/'compiler-checks.json'));(O/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
review=dict(actor=V,advance_id=f['advance_id'],verification_status='passed-scoped',verdict='ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF',blockers=[],checked_base_commit=head(),exact_commit_VERIFIED=False,all_private_providers_reviewed=8,full_modules_reviewed=[d(ROOT/f['inputs'][0]['path']),d(ROOT/f['inputs'][1]['path'])],input_bindings=binding,actual_parent_API_review=apireview,reachability_fake_closure=fake,exact_statement=dict(signature=d(ROOT/f['inputs'][12]['path']),bytes=678,body_prefix_matches_normalized_signature=True,caller_inputs=['n natural including0','f real Fin n observer','ContDiff R2 f','HasCompactSupport f'],outputs=['actual Gaussian pi f² L1','actual tlogt f² L1','each coordinate directional square L1','finite sum energy L1','homogeneous entropy <=2 actual coordinate-square-sum integral']),body_mathematical_audit=audit,fresh_focused=dict(jobs=3184,evidence=checks['checks'][0]),fresh_compiler_evidence=checks['checks'],standard_axioms=['propext','Classical.choice','Quot.sound'],meaningful_stress=dict(source=d(O/'stress.stdin.txt'),check=checks['checks'][3],semantics='True singleton probability and actual -2 observer: square mass4, Phi integral4log4, homogeneous entropy0 and energy0, genuine public theorem domain+inequality consumer.'),toolchain=d(ROOT/'lean-toolchain'),Mathlib=apireview,initial_freeze_before_after=dict(original_count=44,raw_LF_unchanged=44,production_Test_unchanged=True,all_owned_snapshots_exact=True),independence=dict(production_writer='companion_root_20261005',mathematical_reviewer=V,root_exposition_drafts_excluded=True,fresh_anonymous_packet_or_reconstruction_read=False,fresh_source_verdict_read=False,no_canonical_edits=True,no_VERIFIED_transition=True),remaining_boundary=remaining,leases=dict(status='CLOSED',read='CLOSED',write='CLOSED',compiler='CLOSED',python='CLOSED',sessions='CLOSED',receipt=d(O/'lease.json')))
r=put(O/'math.review.json',review)
payload=json.dumps(review,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();run=put(O/'math.review.run.json',dict(actor=V,status='CLOSED',review=r,input_bindings=binding,deterministic_review_run_sha256=hashlib.sha256(payload).hexdigest(),hash_recipe='sha256 UTF8 json sort_keys True separators comma/colon of full math.review payload; raw review digest separately named'))
print(json.dumps(dict(review=r,run=run,inputs=51,fake_files=len(astis.lean_source_files()),all_leases='CLOSED'),ensure_ascii=False),flush=True)
