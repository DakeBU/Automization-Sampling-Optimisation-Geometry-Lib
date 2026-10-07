from pathlib import Path
import json,hashlib,sys,re,subprocess,datetime
sys.path.insert(0,'tools');import astis
R=Path('runs/20261007-companion-priority/gaussian-compact-entropy');O=R/'whole-proof-review';V='picard_commit_verifier_20261005'
def j(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def h(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return {'path':Path(p).as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def put(name,obj):
 p=O/name;assert not p.exists(),p;p.write_bytes((json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
C=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();initial=j(O/'input-bindings.initial.json');assert C==initial['checked_base_commit']=='a63df065f186e0363a5393622c242dc6b9fc1434'
assert initial['decoder_or_source_verdict_read'] is False
rows=initial['inputs']
for row in rows:
 assert d(row['path'])['raw_sha256']==row['raw_sha256'] and d(row['path'])['lf_sha256']==row['lf_sha256']
 assert Path(row['raw_snapshot']).read_bytes()==Path(row['path']).read_bytes()
 assert Path(row['lf_snapshot']).read_bytes()==Path(row['path']).read_bytes().replace(b'\r\n',b'\n')
source=Path(rows[0]['path']);test=Path(rows[1]['path']);s=source.read_bytes().replace(b'\r\n',b'\n')
seal=(R/'preproof/signature.prospective.txt').read_bytes();assert len(seal)==1581 and h(seal)=='d0adc2bfa9a83b8389706c10b31d10c64b5f7b6dba8c7454cd370a738ac7100e'
start=s.index(b'theorem compact_count_gaussian_entropy_limits');end=s.index(b' := by',start);assert s[start:end]+b'\n'==seal
private=re.findall(r'^private (?:noncomputable )?(?:def|theorem) (\w+)',s.decode(),re.M);assert private==['countLaw','normalizedSum','compact_observer']
assert b'import Tests.' not in s
parent='AutoSamplingTheory/TechnicalLemmas/Probability/BalancedRademacherCLT.lean'
assert d(parent)['raw_sha256']=='f71959bc946c8c401568d9aaeff424b21db9f8df50cb59a518ebbbdf15c85aad'
prior='runs/20261007-companion-priority/balanced-rademacher-clt/verified.json';assert d(prior)['raw_sha256']=='164e71d95b58a9d0a499a67d5c0ca2fe3ff34d5778c66ed3a1bc28404704dd86'
assert j(prior)['verified_commit']=='4d9e71a6b835b54453a5cfd2d132f9a51f66f69c'
additional=['.lake/packages/mathlib/Mathlib/Topology/Algebra/Support.lean','AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean','.lake/packages/mathlib/Mathlib/Analysis/Calculus/Deriv/Mul.lean',prior,R.as_posix()+'/claim.json']
for p in additional:
 i=len(rows);raw=O/f'input.{i:03}.raw.snapshot';lf=O/f'input.{i:03}.lf.snapshot';assert not raw.exists() and not lf.exists();b=Path(p).read_bytes();raw.write_bytes(b);lf.write_bytes(b.replace(b'\r\n',b'\n'))
 rows.append({**d(p),'raw_snapshot':raw.as_posix(),'lf_snapshot':lf.as_posix(),'role':'reviewed parent API / immutable earlier independent parent admission / own canonical claim'})
regions=[
 ('Mathlib/MeasureTheory/Measure/ProbabilityMeasure.lean',343,352,'ProbabilityMeasure.tendsto_iff_forall_integral_tendsto: exactly every bounded continuous Real observable'),
 ('Mathlib/Topology/ContinuousMap/BoundedCompactlySupported.lean',79,96,'actual ofCompactSupport preserves g pointwise and constructs the bounded continuous observer'),
 ('Mathlib/MeasureTheory/Function/LocallyIntegrable.lean',552,625,'OpensMeasurableSpace / finite-on-compacts continuous compact support gives actual L1; probability supplies finite-on-compacts'),
 ('Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',354,369,'Integrable.comp_measurable relies on genuine integrable_map_measure equivalence, not integral_undef'),
 ('Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',1032,1041,'integral_map_of_stronglyMeasurable can totalize; both sides are independently genuine L1 in this implementation'),
 ('Mathlib/Topology/Algebra/Support.lean',275,289,'HasCompactSupport.comp_left generated via to_additive; postcomposition maps zero to zero'),
 ('Mathlib/Topology/Algebra/Support.lean',475,486,'stress product support containment: compact cutoff times identity remains compact'),
 ('Mathlib/Analysis/Calculus/ContDiff/Deriv.lean',108,110,'C2 supplies continuous actual scalar derivative with 1<=2'),
 ('Mathlib/Analysis/Calculus/Deriv/Support.lean',32,62,'derivative vanishes outside topological support; HasCompactSupport.deriv uses actual support inclusion'),
 ('Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',44,59,'continuous x*log x at zero including real totalized log; no positive mass premise'),
 ('Mathlib/Analysis/Calculus/Deriv/Mul.lean',287,296,'independent nonzero derivative stress uses real product derivative')]
apir=[]
for i,(p,lo,hi,why) in enumerate(regions):
 p=Path('.lake/packages/mathlib')/p;b=b''.join(p.read_bytes().splitlines(keepends=True)[lo-1:hi]);snap=O/f'parent-region.{i:03}.raw.snapshot';assert not snap.exists();snap.write_bytes(b)
 apir.append({'path':p.as_posix(),'source_file':d(p),'lines':[lo,hi],'snapshot':d(snap),'contract_checked':why})
api=put('parent-api-review.json',{'actor':V,'regions':apir,'prior_ASTIS_parent_reuse':{'exact_mathematical_module':d(parent),'independent_exact_verification':d(prior),'reuse':'Earlier full actual law14-private review and exact35 admission reused solely by unchanged raw/LF module and receipt. No old decoder/source verdict substituted for current36 mathematics.'}})
checks=j(O/'fresh-checks.json');assert len(checks['checks'])==2 and all(x['exit_code']==0 for x in checks['checks'])
for row in checks['checks']:assert d(row['log'])['raw_sha256']==row['raw_sha256']
axioms=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",(O/'direct-test-axioms.log').read_text(encoding='utf-8'),re.S)
assert len(axioms)==3 and all(set(x.strip() for x in a.split(','))=={'propext','Classical.choice','Quot.sound'} for _,a in axioms)
stress=O/'nonzero-n0-stress.attempt2.log';reports=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",stress.read_text(encoding='utf-8'),re.S)
assert len(reports)==1 and set(x.strip() for x in reports[0][1].split(','))=={'propext','Classical.choice','Quot.sound'}
assert ': error:' not in stress.read_text(encoding='utf-8') and 'sorryAx' not in stress.read_text(encoding='utf-8')
stress_status=put('nonzero-n0-stress.attempt2.status.json',{'exit_code':0,'scope':'independent meaningful actual compact probe(x)=x*smoothUnitCutoff(x), C2/compact constructed, deriv probe0=1; actual N0 probability energy integral1 and genuine L1','command':['lake','env','lean',(O/'nonzero-n0-stress.attempt2.lean').as_posix()],'source':d(O/'nonzero-n0-stress.attempt2.lean'),'log':d(stress),'standard_axioms':['propext','Classical.choice','Quot.sound'],'initial_error_preserved':d(O/'nonzero-n0-stress.attempt1.status.json'),'initial_error_credit':'No mathematical acceptance for failed attempt1 or its sorryAx report. Failure was own syntactic id/lambda rewrite inference; explicit c/d/x arguments succeeded once.'})
closure=[source,Path(parent),test];scans=[]
for p in closure:
 clean=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8'));assert not astis.FORBIDDEN_REGEX.search(clean)
 assert not re.search(r'\bunsafe\b|@\[implemented_by',clean)
 scans.append({**d(p),'forbidden_hits':[]})
assert not astis.forbidden_pattern_hits();full_count=len(astis.lean_source_files())
reach=put('reachability-fake-closure.json',{'actor':V,'current_ASTIS_production_closure':[source.as_posix(),parent],'new_private_providers':private,'provider_edges':{'compact_count_gaussian_entropy_limits':['compact_observer'],'compact_observer':['countLaw','normalizedSum','BalancedRademacherCLT.balanced_count_sum_tendsto_gaussian','Continuous.integrable_of_hasCompactSupport','Integrable.comp_measurable','integral_map_of_stronglyMeasurable','ProbabilityMeasure.tendsto_iff_forall_integral_tendsto','ofCompactSupport']},'prior_private14_API_by_unchanged_exact_proof':True,'actual_ASTIS_parent_not_binder':True,'all_new_private_providers_used':True,'selected_sources':scans,'full_canonical_files':full_count,'fake_closure_hits':0,'production_imports_Tests':False,'supplied_final_certificates':False})
for name in ['fresh-checks.json','focused.log','direct-test-axioms.log','nonzero-n0-stress.lean','nonzero-n0-stress.log','nonzero-n0-stress.attempt1.status.json','nonzero-n0-stress.attempt2.lean','nonzero-n0-stress.attempt2.log','nonzero-n0-stress.attempt2.status.json']:
 rows.append({**d(O/name),'role':'own foreground compiler/stress evidence; attempt1 failure explicitly excluded from proof credit'})
for row in rows:assert d(row['path'])['raw_sha256']==row['raw_sha256'] and d(row['path'])['lf_sha256']==row['lf_sha256']
bindings=put('input-bindings.final.json',{'actor':V,'checked_base_commit':C,'original_frozen21_unchanged':True,'inputs':rows,'input_count':len(rows),'new_source_decoder_or_source_fidelity_verdict_read':False})
audit=[
 {'component':'countLaw / normalizedSum','verdict':'sound','reason':'Literal inverse actual finite carrier card and same sqrt(N)^-1 signed sum as the compiled35 producer. All-N incl0 is retained; no nominal iid law or arbitrary pushforward supplied.'},
 {'component':'compact_observer law choice','verdict':'sound','reason':'Consumes internally constructed actual laws and same count-map equality from genuine35, obtaining actual probability eachN and unit variance Gaussian weak limit. Choice only selects a proved family; no probability/CLT premise added.'},
 {'component':'genuine domains','verdict':'sound','reason':'Continuous compact g is L1 on every genuine probability law and on gaussianReal0,1 using finite-on-compacts. Map identity rewrites true L1 to the actual map measure; Integrable.comp_measurable produces actual count-law L1 for eachN, including0. Integral-map equality follows separately; totalized map lemma is not used as an L1 substitute.'},
 {'component':'observer transport','verdict':'sound','reason':'ofCompactSupport has toFun=g exactly. The canonical weak convergence implies BCF integral convergence. hI(n+1) converts BOTH finite-law observer and same target Gaussian integral; successor indexing and variance1 are unchanged.'},
 {'component':'A=f² / B=f²logf²','verdict':'sound','reason':'A continuous and compact because t² sends0to0. Continuous_mul_log composed with A handles zeros; its postcomposition also sends0to0, so B compact and genuinely L1. No nonzero function or positive integral-mass premise.'},
 {'component':'C=(deriv f)²','verdict':'sound','reason':'ContDiffR2 gives continuous actual derivative (needs1<=2); support_deriv_subset ensures derivative compact, then square compact. No C∞ f, domain certificate, support assumption on derivative or final limit supplied.'},
 {'component':'homogeneous entropy','verdict':'sound','reason':'tB - (continuous_mul_log composed with tA) gives precisely logenergy-minus-mass*logmass; continuity at mass0 makes zero mass included. No normalized mass1, division by mass or dimension change.'},
 {'component':'Tests and independent stress','verdict':'meaningful','reason':'Zero function proves zero-mass homogeneous entropy limit via actual public eight-conjunction result. N0 test derives count L1 and actual derivative-at-zero integral through literal map and Dirac0. Independently constructed signed compact probe=x*cutoff has derivative0=1 and actual N0 energy1; normalized sum0 does not force derivative observer zero.'}]
review=put('math.review.json',{'actor':V,'advance_id':'ASTIS-SA-20261007-GaussianCompactEntropy','verification_status':'passed-scoped','verdict':'ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF','blockers':[],'checked_base_commit':C,'exact_commit_VERIFIED':False,'all_private_providers_reviewed':3,'full_modules_reviewed':[d(source),d(test)],'input_bindings':bindings,'actual_parent_API_review':api,'reachability_fake_closure':reach,'exact_statement':{'bytes':1581,'raw_LF_sha256':h(seal),'production_extracted_signature_matches_full_terminal_newline_seal':True,'public_binders':['f:Real->Real','ContDiff Real2 f','HasCompactSupport f'],'eight_conjunctions':['Gaussian L1 f²','Gaussian L1 f²logf²','Gaussian L1 derivative²','allN count three L1 domains','successor mass observer integral limit','successor logenergy observer integral limit','successor derivative² observer integral limit','successor homogeneous entropy integral limit']},'body_mathematical_audit':audit,'fresh_focused_direct_checks':checks,'axiom_reports':[{'declaration':a,'axioms':['propext','Classical.choice','Quot.sound']} for a,_ in axioms],'independent_substantive_stress':stress_status,'nonblocking_diagnostics':['Two unnecessarySimpa linter warnings in actual Test retained; neither affects declaration or mathematics.','Initial read used wrong Probability folder; actual frozen file is FunctionalInequalities/GaussianCompactEntropy.lean. No code/source mutation.','Own stress attempt1 syntactic id/lambda rewrite error retained; only terminal attempt2 with standard3 is accepted.'],'source_boundary':'Authored scalar compact C2 Gaussian entropy core prerequisite, not literal noncompact SPHMC sqrt-density result or printed GaussianLSI. Exact source topology/seal pins bound as external independent preproof evidence only; no self topology or final source fidelity verdict.','exposure':{'independent_from_root_proofwriter':True,'earlier36_primary_preread_and_statement_review_authored_by_me':True,'36_sourcegraph_authored_or_self_validated':False,'36_anonymous_decoder_or_final_source_verdict_read':False,'old35_wholeproof_and_own_exact_proof_review_reused_by_bytes':True},'remaining_truth_boundary':['Full coordinate-flip energy factor4 limit separate from derivative observer convergence.','GaussianLSI, finite-Hilbert/tensorization and literal noncompact actual sqrtRN cutoff/domain extension open.','GaussianT2/FIRST4.6/W2/bias/fullLemma/paper main/querywork/composition open.','PROVED_LOCAL, fresh blind/source admission, exact committed VERIFIED, shared integration/repository/exposition/purification remain separate; none claimed in this math-only review.'],'compiler':'CLOSED; fresh focused3162/direct three standard axioms, independent substantive stress attempt2 one standard3 declaration','canonical_mutations':False,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
material={'actor':V,'review':review,'bindings':bindings,'parent_API':api,'reachability_scan':reach,'verdict':'ACCEPTED_SCOPED_WHOLE_MATHEMATICAL_PROOF','self_source_validation':False,'compiler_terminal':True};runhash=h(json.dumps(material,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
run=put('run.json',{**material,'deterministic_run_sha256':runhash,'status':'CLOSED','hash_recipe':'Exclude deterministic_run_sha256, status and hash_recipe; canonical compact sorted JSON material.'})
(O/'lease.json').write_bytes((json.dumps({'status':'CLOSED','actor':V,'checked_base_commit':C,'read':'CLOSED','write':'CLOSED','compiler':'CLOSED','Python':'CLOSED','review':review,'run':run,'deterministic_run_sha256':runhash,'canonical_mutations':False},ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'verdict':'passed-scoped','review':review,'run':run,'runhash':runhash,'all_leases':'CLOSED','inputs':len(rows),'private_providers':3,'full_canonical_fake_scan_files':full_count},ensure_ascii=False))
