from verify import *
import gzip
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
from tools import astis_advance
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==SCI
claim=load(R/'proved-local.json');before=load(D/'before-admin.json');checks=load(D/'native-checks.json');gates=load(D/'gates.json');assert gates['status']=='PASS'
admin={sig(x['original']):x for x in before['canonical_mappings']}
def ensure_input(row):
 p=path(row['path'])
 if matches(row,p):return dict(expected=row,actual=pin(p),mapping=None)
 assert sig(row) in admin,('post-gates input mismatch',row)
 m=admin[sig(row)];assert matches(row,path(m['exactraw_snapshot']['path']));return dict(expected=row,actual=m['exactraw_snapshot'],mapping=m)
pre=load(D/'inputs.pretransition.json');prechecks=[ensure_input(v) for v in pre['inputs']]
for x in load(R/'math-freeze.json')['inputs']:assert matches(x,path(x['path']))
git=load(D/'science.git.json');assert git['count']==1185
for x in git['entries']:
 r=ensure_input(x['current']);assert r['actual']['lf_sha256']==x['git_lf_sha256']
def diff(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):
  return sum([diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):
  return [p] if len(a)!=len(b) else sum([diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[])
 return [] if a==b else [p]
current_admin=[]
for m in before['canonical_mappings']:
 p=path(m['original']['path']);a=load(path(m['exactraw_snapshot']['path']));b=load(p);d=diff(a,b)
 allowed=[]
 if p.name=='ASTIS-SHARED-l2-pullback-range.json':allowed=['/route']
 if p.name=='ASTIS-SW-PBPS-centered-macro-defect-gap.json':allowed=['/reuse_plan/reused_declarations']
 assert d==allowed,(p,d,allowed);current_admin.append(dict(path=p.as_posix(),exact_before=m,actual_pretransition=pin(p),authorized_diff_pointers=d))
ledger=ROOT/'runs/substantive_advances.jsonl';assert matches(before['ledger_original'],ledger)
state=astis_advance.current_advances();aid='ASTIS-SA-20261008-PBPSMacroscopicCenteredRange';assert state[aid]['state']=='PROVED_LOCAL' and state[aid]['owner_id']!=ACTOR
scoped=load(D/'scoped-checks.json');assert scoped['status']=='PASS'
wd=load(R/'whitespace-diagnosis58/diagnosis.json');gp=path(wd['gzip']['path']);gb=gp.read_bytes();raw=gzip.decompress(gb);assert sha(raw)==wd['full_negative_raw_sha256'] and sha(gb)==wd['gzip']['raw_sha256'] and gb[4:8]==bytes(4)
paths=sorted(set(m.group(1) for m in re.finditer(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF)',raw.decode('utf8'),re.M)))
assert wd['full_staged_exit']==2 and wd['authored_check_exit']==0
write(D/'whitespace-boundary.json',dict(status='IMMUTABLE_FULL_STAGED_NEGATIVE_AUTHORED_COMPLEMENT_ONLY_PASS',retained_diagnosis=pin(R/'whitespace-diagnosis58/diagnosis.json'),retained_gzip=pin(gp),lossless_raw_sha256=sha(raw),gzip_mtime=0,findings=wd['findings'],exact_diagnostic_path_count=len(paths),exact_diagnostic_paths=paths,authored_check_exit=wd['authored_check_exit'],not_full_staged_PASS=True))
payload=dict(verifier_id=ACTOR,checked_commit=SCI,result_kind='integration-node',declarations=claim['lean_declarations'],signature_binding=pin(D/'signatures.json'),unchanged_complete_math_receipt=pin(R/'whole-math58/receipt.json'),unchanged_complete_math_run=pin(R/'whole-math58/run.json'),complete_math_run_sha256=load(R/'whole-math58/run.json')['run_sha256'],distinct_math_payload_sha256=load(R/'whole-math58/run.json')['review_binding_payload_sha256'],source_review_binding=pin(D/'scoped-checks.json'),source_audits=[v['canonical_audit'] for v in scoped['source_reviews']],source_native_reviews=[v['native_review'] for v in scoped['source_reviews']],fake_closure_scan=dict(files=7,findings=0,actual_scan=pin(D/'scoped-checks.json')),focused_Lean=load(D/'focused.status.json'),all_required_noncompiler_gates=pin(D/'gates.json'),science_entries=1185,math_freeze_inputs=72,native_pin_checks=checks['actual_pin_checks'],native_self_component_checks=len(checks['native_self_checks']),historical_mapping_checks=len(checks['historical_before_mappings']),before_transition_maps=before['canonical_mappings'],ledger_prefix=before['ledger_prefix'],remaining_boundary=claim['truth_boundary'],shared_integration_deferred=True,no_PURIFIED_or_main_live_claim=True)
payloadsha=sha(canon(payload));write(D/'verifier-payload.json',dict(payload=payload,verifier_binding_payload_sha256=payloadsha,recipe='Sorted compact UTF8 JSON of ONLY payload value; distinct from complete run self hash.'))
receipt=dict(schema_version=1,status='INDEPENDENT_EXACT_SCIENCE_GATES_PASS',verdict='ACCEPT_SCOPED_NO_MATHEMATICAL_OR_SOURCE_BLOCKER',verifier_id=ACTOR,checked_commit=SCI,result_kind='integration-node',declarations=claim['lean_declarations'],verifier_binding_payload_sha256=payloadsha,verifier_payload=pin(D/'verifier-payload.json'),science_entries=1185,strict_math_originals=72,actual_native_pin_checks=checks['actual_pin_checks'],distinct_pretransition_inputs=len(pre['inputs']),native_self_component_checks=len(checks['native_self_checks']),source_reviews=3,semantic_slots=21,source_verdict='equivalent-after-elaboration',source0_addendum='Only overall schema classification corrected; original exact verdict and seven semantic slots preserved unchanged; no theorem/source repair.',source_decoder='Native source-TEXT and source-identity blind, no invented identity claim.',fake_scan_files=7,fake_closure_findings=0,standard_axiom_closures=3,actual_compiler_PID=load(D/'focused.status.json')['actual_PID'],actual_compiler_exit_code=0,focused_invocations=1,Lean_toolchain='leanprover/lean4:v4.33.0',Mathlib_pin='db584cd6d46c92f209a44c0f1c829460d327499d',all_required_noncompiler_gates=pin(D/'gates.json'),complete_mathematical_reasons_reused=pin(R/'whole-math58/mathematical-reasons.json'),mathematical_summary='Actual AE real pullback factorization and pushforward MemLp produce onto range; actual Gibbs joint probability and canonical conditional projection yield whole centered macro image and true integral preservation. SAME55 M/T and57 conditional mean identify via actual AE action/S source law before all inputs. The real Test transports sharp contraction and squares actual B variance defect; alphaeta=1 and rank0 require no division by 1-alphaeta and no infinite-L2 premise.',retained_negatives=pin(D/'native-reader-negatives.json'),authorized_admin=pin(D/'administrative-correction.json'),before_admin=pin(D/'before-admin.json'),whitespace_debt=pin(D/'whitespace-boundary.json'),truth_boundary=claim['truth_boundary'],sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',no_shared_aggregate_or_live_claim=True,recipe='Entire complete receipt minus ONLY receipt_sha256; sorted compact UTF8 JSON.')
receipt['receipt_sha256']=sha(canon(receipt));write(D/'receipt.json',receipt)
evidence=dict(gate='Independent exact-commit lake build Tests.ProximalBPSMacroscopicRange PASS3908 plus reviewed publication/source/semantic/frontier/contributor gates; standard3 only.',verifier_id=ACTOR,verified_commit=SCI,checked_commit=SCI,source_audit=[v['canonical_audit']['path'] for v in scoped['source_reviews']],fake_closure_scan='Actual comment/string-stripped scan7 source files, 0 findings; exact3 successful standard axioms closures; failed-only elaboration sorryAx retained.',receipt=str((D/'receipt.json').relative_to(ROOT)).replace('\\','/'),receipt_raw_sha256=pin(D/'receipt.json')['raw_sha256'],verifier_binding_payload_sha256=payloadsha,science_entries=1185,math_inputs=72,remaining_truth_boundary=claim['truth_boundary'])
astis_advance.transition_advance(aid,'VERIFIED',worker_id=ACTOR,modes=('independent-exact-commit-verification',),evidence=evidence)
for cellid in claim['active_cells']:
 p=ROOT/f'research-wiki/frontier-cells/{cellid}.json';q=load(p);assert q['status']=='proved_locally';q['status']='independently_verified';q['evidence']['independent_verification']=str((D/'receipt.json').relative_to(ROOT)).replace('\\','/');q['evidence']['independent_verification_details']=dict(verifier_id=ACTOR,checked_commit=SCI,verifier_binding_payload_sha256=payloadsha,receipt_raw_sha256=pin(D/'receipt.json')['raw_sha256'],focused_build='PASS3908',source_audit='Accepted scoped three native source results, original negatives preserved',fake_closure_scan='7 actual files zero findings',shared_integration='Deferred to original serialized lane');write(p,q)
state=astis_advance.current_advances();assert state[aid]['state']=='VERIFIED';assert [k for k,v in state.items() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
assert ledger.read_bytes().startswith(path(before['ledger_prefix']['path']).read_bytes())
command('gate.verified.frontier',[sys.executable,'-B','-X','utf8','tools/astis_frontier_cells.py','check'])
postmaps=[]
for m in before['canonical_mappings']:
 p=path(m['original']['path']);d=diff(load(path(m['exactraw_snapshot']['path'])),load(p))
 allowed=['/status','/evidence/independent_verification','/evidence/independent_verification_details'] if '/frontier-cells/' in p.as_posix() else []
 if p.name=='ASTIS-SHARED-l2-pullback-range.json':allowed+=['/route']
 if p.name=='ASTIS-SW-PBPS-centered-macro-defect-gap.json':allowed+=['/reuse_plan/reused_declarations']
 assert sorted(d)==sorted(allowed),(p,d);postmaps.append(dict(original=m['original'],exactraw_snapshot=m['exactraw_snapshot'],current_after_verified=pin(p),actual_diff_pointers=d))
write(D/'transition.json',dict(status='VERIFIED_BY_DISTINCT_INDEPENDENT_VERIFIER',checked_commit=SCI,verifier_id=ACTOR,actual_PID=os.getpid(),advance_id=aid,ledger_prefix=before['ledger_prefix'],ledger_after=pin(ledger),independent_evidence=evidence,cells_current=[pin(ROOT/f'research-wiki/frontier-cells/{n}.json') for n in claim['active_cells']],exact_verified_admin_before_mappings=postmaps,sole_STABILIZING='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'))
verified=dict(schema_version=1,status='VERIFIED',advance_id=aid,checked_commit=SCI,verified_commit=SCI,verifier_id=ACTOR,receipt=pin(D/'receipt.json'),run_artifact=str((D/'run.json').relative_to(ROOT)).replace('\\','/'),run_binding_rule='Final complete run binds this actual verified artifact; final CLOSED lease binds complete run raw/LF plus run_sha256 and distinct verifier_binding_payload_sha256. No circular run/verified hashing.',verifier_binding_payload_sha256=payloadsha,verifier_payload=pin(D/'verifier-payload.json'),transition=pin(D/'transition.json'),exact_verified_admin_before_mappings=postmaps,ledger_prefix=before['ledger_prefix'],scope=claim['truth_boundary'],shared_integration_pending=True,verified_self_recipe='Entire complete object minus ONLY verified_sha256; sorted compact UTF8 JSON.')
verified['verified_sha256']=sha(canon(verified));write(R/'verified.json',verified)
inputs={v['path']:v for v in pre['inputs']}
for f in ['tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py','tools/astis_contributor_contract.py','tools/astis.py','lean-toolchain','lake-manifest.json']:
 inputs[(ROOT/f).as_posix()]=pin(ROOT/f)
for m in postmaps:inputs[m['exactraw_snapshot']['path']]=m['exactraw_snapshot']
inputs[before['ledger_prefix']['path']]=before['ledger_prefix']
write(D/'inputs.final.json',dict(status='PASS',checked_commit=SCI,inputs=list(inputs.values()),count=len(inputs),math_freeze_count=72,science_git_count=1185,exact_verified_admin_before_mappings=postmaps,ledger_prefix=before['ledger_prefix'],recipe='Every raw/LF pin checked at exact science before transition; changed ONLY authorized cell admin pins resolve to exact before snapshots matching all original hashes/lengths; ledger old pin resolves to exact prefix snapshot and current ledger prefix equality.'))
run=dict(schema_version=1,status='VERIFIED_SCOPED_EXACT_SCIENCE',verifier_id=ACTOR,checked_commit=SCI,inputs=load(D/'inputs.final.json')['inputs'],input_manifest=pin(D/'inputs.final.json'),science_git=pin(D/'science.git.json'),native_checks=pin(D/'native-checks.json'),receipt=pin(D/'receipt.json'),verified=pin(R/'verified.json'),transition=pin(D/'transition.json'),verifier_binding_payload=payload,verifier_binding_payload_sha256=payloadsha,actual_focused_compiler_PID=load(D/'focused.status.json')['actual_PID'],actual_focused_compiler_exit_code=0,actual_finalizer_worker_PID=os.getpid(),focused_invocations=1,native_run_recipe='Entire complete object minus ONLY top-level run_sha256; sorted compact UTF8 JSON, ensure_ascii=False, allow_nan=False, no newline.',named_component_recipe='Hash ONLY verifier_binding_payload value by sorted compact UTF8 JSON; distinct from complete run hash.',source_math_blockers=0,shared_aggregate_deferred=True,remaining_boundary=claim['truth_boundary'])
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==SCI
print(json.dumps(dict(status='PASS_VERIFIED_WORKER',checked_commit=SCI,actual_worker_PID=os.getpid(),run_sha256=run['run_sha256'],verifier_binding_payload_sha256=payloadsha,input_count=len(inputs),science_entries=1185,actual_compiler_PID=load(D/'focused.status.json')['actual_PID']),sort_keys=True))
