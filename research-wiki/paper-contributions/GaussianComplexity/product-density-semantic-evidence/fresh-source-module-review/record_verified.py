from pathlib import Path
import datetime,gzip,hashlib,json,subprocess,sys
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'lean-toolchain').exists())
sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
BASE=Path(__file__).resolve().parent
TARGET='ASTIS-SA-20261106-GaussianComplexityProductDensity'
DECL='AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density'
OWNER='huanjian_gc_20261106_ex70'
VERIFIER='/root/ex70_fresh_source_module_review'
COMMIT='a83254ef00c8e6fd0548a25fae03f07e2a82e2b7'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
def sha(data): return hashlib.sha256(data).hexdigest()
def canon(d): return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(name,d):
 p=BASE/name;p.write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n');return p

def entry(p):
 if not p.exists(): return {'exists':False}
 b=p.read_bytes();return {'exists':True,'sha256':sha(b),'bytes':len(b)}
def archive(name,data):
 p=BASE/name;p.write_bytes(gzip.compress(data,mtime=0));assert gzip.decompress(p.read_bytes())==data
 return {'path':str(p.relative_to(ROOT)),'raw_sha256':sha(data),'raw_bytes':len(data),'archive_sha256':sha(p.read_bytes()),'archive_bytes':p.stat().st_size,'lossless_verified':True}
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()

assert head()==COMMIT
expected={
'AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean':'a75340883fb065e782a802f6dc8184f52d25fa96930e681d89dfc97fe87bd228',
'Tests/GaussianComplexityProductDensity.lean':'ad9d4fa4048a2fb88b5eaade4a7bc202f05e0a4b48a13790893f8cc768fbfccd',
'research-wiki/paper-contributions/GaussianComplexity/product-density-semantic-evidence/fresh-source-module-review/raw-source-prefreeze.json':'aaa072cd25c8bb7e26c8093d3e707bfd3b387c6e2be5a9fa598ef52ee1f51b33',
'research-wiki/paper-contributions/GaussianComplexity/product-density-semantic-evidence/fresh-source-module-review/source-versus-reconstruction-prefreeze.json':'248da9707ed4dc2ed1eb96ada44f2747f23813ba5756e8039bbebf6cfbe885ae',
'.astis/huanjian-resume-20261103/2610.20492v1.html':'6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'}
for p,h in expected.items():assert entry(ROOT/p)['sha256']==h,(p,'hash changed')
auditpath=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-product-density.json';audit=json.loads(auditpath.read_text())
assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
assert audit['source_review']['reviewer']==VERIFIER
assert audit['source_review']['review_run_sha256']=='b43f2397046a87e55fe78100f1267321bf39867ac29d9825e35561c9e72999f7'
assert audit['source_review']['reviewer_packet_sha256']=='ccddfa8578a18a0836e5230663ad02e2459796078c7e7a5db9589c78b2a6502a'
assert audit['publication_binding_sha256']=='f764e7b080de73ded904fb5a89d6424878a1b2c2b292ca9648d70ed3ce19eca8'
assert sha((BASE/'review-run.json').read_bytes())==audit['source_review']['review_run_sha256']
packetpath=BASE.parent/'fresh-reviewer-packet.json';packet=json.loads(packetpath.read_text());packet_claim=packet.pop('packet_sha256')
assert packet_claim==audit['source_review']['reviewer_packet_sha256']==sha(canon(packet))
assert sha(packetpath.read_bytes())=='c3a6a792edfe36b5c3e04bf8687a49297103ca805087a4d4456a44af15ad1231'
gater=BASE/'verifier-current-reviewed-gate.receipt.json';gate=json.loads(gater.read_text())
assert gate['returncode']==0 and gate['head_before']==gate['head_after']==COMMIT
assert sha((ROOT/gate['log']).read_bytes())==gate['log_sha256']
run=json.loads((BASE/'review-run.json').read_text())
for c in run['commands']:
 d=c['data'];assert sha((ROOT/d['log']).read_bytes())==d['log_sha256']
assert all(c['data']['returncode']==0 for c in run['commands'] if 'coordinate-r0-probe.receipt.json' not in c['receipt_path'])
closure=json.loads((BASE/'local-dependency-closure.json').read_text())
assert not any(m['fake_closure_hits'] for m in closure['modules'].values())
for m in closure['modules'].values():assert entry(ROOT/m['path'])['sha256']==m['sha256']

before=LEDGER.read_bytes();assert before.endswith(b'\n')
state_before=advance.current_advances();assert LEDGER.read_bytes()==before
current=state_before[TARGET]
assert current['state']=='PROVED_LOCAL' and current['owner_id']==OWNER
assert current['target_declarations']==[DECL] and current['publication_declarations']==[DECL]
foreign_before={k:v for k,v in state_before.items() if k!=TARGET};assert len(foreign_before)==276
tracked=[x.decode() for x in subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).split(b'\0') if x]
protected_paths=set(tracked)-{'runs/substantive_advances.jsonl'}
protected_paths.update(expected)
protected_paths.update(str(p.relative_to(ROOT)) for p in [BASE/'review-run.json',BASE/'review-result.json',BASE/'post-review-validation.json',packetpath])
protected_before={p:entry(ROOT/p) for p in sorted(protected_paths)}
frontiers={str(p.relative_to(ROOT)):entry(p) for p in sorted((ROOT/'research-wiki/frontier-cells').rglob('*.json'))}
oldfrontiers={p:v for p,v in frontiers.items() if p!='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-product-density.json'}
prefix_archive=archive('verified-ledger-before.jsonl.gz',before)
foreign_archive=archive('verified-foreign-states-before.json.gz',canon(foreign_before))
protected_archive=archive('verified-protected-inputs-before.json.gz',canon(protected_before))
frontier_archive=archive('verified-frontiers-before.json.gz',canon(frontiers))
pre={'candidate_commit':COMMIT,'target':TARGET,'state':'PROVED_LOCAL','owner':OWNER,'verifier':VERIFIER,'ledger_sha256':sha(before),'ledger_bytes':len(before),'ledger_records':len(before.splitlines()),'foreign_states':len(foreign_before),'old_frontier_files':len(oldfrontiers),'all_frontier_files':len(frontiers),'protected_input_files':len(protected_before),'archives':{'ledger_prefix':prefix_archive,'foreign_states':foreign_archive,'protected_inputs':protected_archive,'frontiers':frontier_archive},'current_reviewed_gate':{'receipt':str(gater.relative_to(ROOT)),'receipt_sha256':sha(gater.read_bytes()),'log_sha256':gate['log_sha256']},'audit_sha256':sha(auditpath.read_bytes()),'review_run_sha256':audit['source_review']['review_run_sha256'],'packet_sha256':packet_claim,'publication_binding_sha256':audit['publication_binding_sha256']}
prepath=write('verified-preflight.json',pre)
evidence={
'verifier_id':VERIFIER,'verified_commit':COMMIT,'publication_declarations':[DECL],'lean_declarations':[DECL],
'gate':{'status':'passed-current-reviewed-source-and-local-Lean','scope':'Target-only reviewed publication admission plus exact-candidate focused build/direct Lean; not global root gate. API internally reruns check_advance(reviewed=True).','current_reviewed_receipt':str(gater.relative_to(ROOT)),'current_reviewed_receipt_sha256':sha(gater.read_bytes()),'current_reviewed_log_sha256':gate['log_sha256'],'focused_build':str((BASE/'focused-build.receipt.json').relative_to(ROOT)),'focused_build_mode':'3137-job cache replay','direct_production':str((BASE/'direct-production.receipt.json').relative_to(ROOT)),'direct_tests':str((BASE/'direct-tests.receipt.json').relative_to(ROOT)),'independent_probe':str((BASE/'coordinate-r0-probe-v2.receipt.json').relative_to(ROOT))},
'source_audit':{'status':'accepted','audit':str(auditpath.relative_to(ROOT)),'audit_sha256':sha(auditpath.read_bytes()),'verdict':audit['verdict'],'review_run':str((BASE/'review-run.json').relative_to(ROOT)),'review_run_sha256':audit['source_review']['review_run_sha256'],'reviewer_packet_sha256':packet_claim,'publication_binding_sha256':audit['publication_binding_sha256'],'independent_raw_prefreeze_sha256':expected[str((BASE/'raw-source-prefreeze.json').relative_to(ROOT))],'independent_reconstruction_prefreeze_sha256':expected[str((BASE/'source-versus-reconstruction-prefreeze.json').relative_to(ROOT))]},
'fake_closure_scan':{'status':'passed','local_module_count':closure['count'],'record':str((BASE/'local-dependency-closure.json').relative_to(ROOT)),'record_sha256':sha((BASE/'local-dependency-closure.json').read_bytes()),'hits':[],'axioms_log':str((BASE/'coordinate-r0-probe-v2.log').relative_to(ROOT)),'axioms_log_sha256':sha((BASE/'coordinate-r0-probe-v2.log').read_bytes()),'only_axioms':['propext','Classical.choice','Quot.sound']},
'preservation_preflight':{'path':str(prepath.relative_to(ROOT)),'sha256':sha(prepath.read_bytes())},
'proof_owner_retained':OWNER,
'remaining_truth_boundary':'Actual Ex70 density/coordinate-volume/L1/mass1 and actual ambient/split measurable-set consumers only. Ex71/72, main query bounds, root integration/gate, browser/Chrome/live/public/remote publication, purification and main/Goal completion remain open. No cell self-edit; reader projection is a separate integration operation.'}
write('verified-transition-evidence.json',evidence)
print('PREFLIGHT PASS: exact candidate, PROVED_LOCAL owner, sole publication target, accepted source audit and current reviewed gate; preserved inputs archived.',flush=True)
try:
 advance.transition_advance(TARGET,'VERIFIED',worker_id=VERIFIER,modes=('independent-verification',),evidence=evidence)
except Exception as exc:
 after=LEDGER.read_bytes();refusal={'status':'API_REJECTED','exception_type':type(exc).__name__,'reason':str(exc),'ledger_before_sha256':sha(before),'ledger_after_sha256':sha(after),'ledger_unchanged':after==before,'bypass_attempted':False};write('verified-api-result.json',refusal);print(json.dumps(refusal));raise

after=LEDGER.read_bytes();state_after=advance.current_advances();assert LEDGER.read_bytes()==after
assert after.startswith(before),'old ledger prefix changed'
append=after[len(before):];rows=[json.loads(x) for x in append.splitlines() if x.strip()];assert len(rows)==1
row=rows[0];assert row['advance_id']==TARGET and row['from_state']=='PROVED_LOCAL' and row['to_state']=='VERIFIED' and row['worker_id']==VERIFIER
assert state_after[TARGET]['state']=='VERIFIED' and state_after[TARGET]['owner_id']==OWNER
assert state_after[TARGET]['publication_declarations']==[DECL]
foreign_after={k:v for k,v in state_after.items() if k!=TARGET};assert foreign_after==foreign_before
protected_after={p:entry(ROOT/p) for p in protected_before};assert protected_after==protected_before
frontiers_after={str(p.relative_to(ROOT)):entry(p) for p in sorted((ROOT/'research-wiki/frontier-cells').rglob('*.json'))};assert frontiers_after==frontiers
assert head()==COMMIT
appendpath=BASE/'verified-append.jsonl';appendpath.write_bytes(append)
result={'schema':'independent-normal-api-verification-transition-v1','status':'VERIFIED_BY_NORMAL_API','target':TARGET,'declaration':DECL,'publication_declarations':[DECL],'proof_owner':OWNER,'verifier_id':VERIFIER,'verified_commit':COMMIT,'api':'tools.astis_advance.transition_advance','api_owns_atomic_append':True,'before_state':'PROVED_LOCAL','after_state':'VERIFIED','ledger_before_sha256':sha(before),'ledger_after_sha256':sha(after),'ledger_before_bytes':len(before),'ledger_after_bytes':len(after),'exact_old_ledger_prefix_preserved':True,'unique_append_events':1,'append_path':str(appendpath.relative_to(ROOT)),'append_sha256':sha(append),'appended_event':row,'foreign_projected_states_preserved':len(foreign_before),'foreign_projected_states_canonical_sha256':sha(canon(foreign_before)),'old_frontier_files_preserved':len(oldfrontiers),'all_frontier_files_preserved':len(frontiers),'protected_inputs_preserved':len(protected_before),'protected_inputs_canonical_sha256':sha(canon(protected_before)),'target_frontier_unchanged':True,'protected_module_tests_bindings_unchanged':True,'preflight':str(prepath.relative_to(ROOT)),'preflight_sha256':sha(prepath.read_bytes()),'prefix_archive':prefix_archive,'no_other_state_changed':True,'no_frontier_cell_self_edit':True,'boundary':evidence['remaining_truth_boundary']}
write('verified-api-result.json',result)
print('VERIFIED normal API PASS: exactly one append, owner retained, 276 foreign states / '+str(len(oldfrontiers))+' old frontiers and '+str(len(protected_before))+' protected inputs unchanged.',flush=True)
print(json.dumps({k:result[k] for k in ['status','target','before_state','after_state','ledger_before_sha256','ledger_after_sha256','append_sha256','foreign_projected_states_preserved','old_frontier_files_preserved','protected_inputs_preserved']},ensure_ascii=False))
