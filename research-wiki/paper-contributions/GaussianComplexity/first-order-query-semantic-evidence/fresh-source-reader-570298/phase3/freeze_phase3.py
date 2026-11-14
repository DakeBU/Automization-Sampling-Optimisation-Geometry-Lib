from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(name,v):(OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
assert not (OUT/'manifest.json').exists()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
assert head=='214b6214c5b08bd52b6faa59a3ccd6ca35998420'
receipt=json.loads((OUT/'verified-transition-receipt.json').read_bytes())
assert receipt['status']=='PASS' and receipt['to_state']=='VERIFIED'
audit_receipt=json.loads((OUT/'audit-update-receipt.json').read_bytes())
assert sha((ROOT/audit_receipt['path']).read_bytes())==audit_receipt['new_sha256']
inputs=json.loads((OUT/'input-pins-and-chain.json').read_bytes())
for record in inputs['files']:
 if record['path']!=audit_receipt['path']:
  assert sha((ROOT/record['path']).read_bytes())==record['sha256'],record['path']
changed=subprocess.check_output(['git','diff','--name-only'],cwd=ROOT).decode().splitlines()
assert set(changed)=={'runs/substantive_advances.jsonl',audit_receipt['path']},changed
whitespace=subprocess.run(['git','diff','--check'],cwd=ROOT,capture_output=True)
assert whitespace.returncode==0,whitespace.stdout.decode()+whitespace.stderr.decode()
for stage,digest in [('phase1','bc44863244c183b086f3c14f1f43a7e6fa5efc3e221a392fb5006ba2e8d985e6'),('phase2','b4ced2e2b379bd11d4b66826abef03c5735e8af99bd3550f2627c44e1aedc3c8')]:
 assert sha((OUT.parent/stage/'manifest.json').read_bytes())==digest
dump('outcome.json',{'status':'PASS','reviewer':'/root/reader_570298','checked_commit':head,
 'verdict':'equivalent-after-elaboration','seven_slots_complete':True,'blocking_deltas':[],
 'whole_module_and_static_reader_review':'PASS','all_fresh_focused_gates':'PASS',
 'review_run_sha256':sha((OUT/'review-run.json').read_bytes()),'review_result_sha256':sha((OUT/'review-result.json').read_bytes()),
 'canonical_reviewer_packet_sha256':'1a1b7d8c5ce75da07ba11554e311dafcbff27eb84792fa4b66560efbec1696ea',
 'publication_binding_sha256':'e8418238a48de3365b59035dc005bce611ec93a257f47229c54a6b847a1452aa',
 'audit':audit_receipt,'normal_verifier_api_receipt_sha256':sha((OUT/'verified-transition-receipt.json').read_bytes()),
 'advance_state':'VERIFIED','proof_owner_preserved':'huanjian_gc_20261107_first_order_query',
 'exact_ledger_prefix_preserved':True,'foreign_advance_states_preserved':279,
 'discovery_ledger_frontiers_foreign_audits_registry_unchanged':True,
 'only_tracked_changed_files':changed,'git_diff_check':'PASS',
 'frontier_projection':'Left to root; own and all foreign frontiers are byte-unchanged.',
 'checked_tree_vs_review_metadata':'Immutable214b has the blind-reconstructed audit; accepted audit9010f395... is a later dirty working-tree update and is not claimed part of214b.',
 'remaining_boundary':json.loads((OUT/'review-result.json').read_bytes())['remaining_boundary'],
 'browser_limit':'Static stock reader/source review only. Root separately owns authorized HTTP/Chrome, canonical root/integration gates and later publication.',
 'stop_writes':True})
records=[]
for path in sorted(OUT.rglob('*')):
 if path.is_file() and path.name!='manifest.json':
  b=path.read_bytes();records.append({'path':str(path.relative_to(OUT)),'bytes':len(b),'sha256':sha(b)})
dump('manifest.json',{'schema':1,'phase':'phase3-complete-independent-source-verification','reviewer':'/root/reader_570298',
 'frozen_utc':datetime.now(timezone.utc).isoformat(),'checked_commit':head,
 'phase1_manifest_sha256':'bc44863244c183b086f3c14f1f43a7e6fa5efc3e221a392fb5006ba2e8d985e6',
 'phase2_manifest_sha256':'b4ced2e2b379bd11d4b66826abef03c5735e8af99bd3550f2627c44e1aedc3c8',
 'reviewer_packet_sha256':'1a1b7d8c5ce75da07ba11554e311dafcbff27eb84792fa4b66560efbec1696ea',
 'review_run_sha256':sha((OUT/'review-run.json').read_bytes()),
 'review_result_sha256':sha((OUT/'review-result.json').read_bytes()),'files':records,
 'manifest_hash_convention':'Manifest byte count/SHA-256 are reported separately; no self-hash.',
 'authorized_mutations_complete':'Only own semantic audit review fields and one normal API PROVED_LOCAL→VERIFIED event. No mathematical edits, frontier changes, STABILIZING/MERGED or root/browser/remote acceptance claims.',
 'next_action':'STOP WRITES and report exact pins/preservation receipts to root.'})
m=json.loads((OUT/'manifest.json').read_bytes())
for f in m['files']:
 b=(OUT/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],f['path']
for n in ['manifest.json','review-run.json','review-result.json','audit-update-receipt.json','verified-transition-receipt.json','outcome.json']:
 b=(OUT/n).read_bytes();print(n,len(b),sha(b))
print('Frozen files',len(records),'STOP WRITES.')
