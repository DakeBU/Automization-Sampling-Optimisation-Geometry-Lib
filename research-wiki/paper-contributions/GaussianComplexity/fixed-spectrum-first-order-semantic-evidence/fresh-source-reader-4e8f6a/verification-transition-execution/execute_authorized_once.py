from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time,traceback
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a'
PREP=BASE/'verification-transition-preparation'
OUT=BASE/'verification-transition-execution'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-first-order.json'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
AUTH=PREP/'root-authorization.json'
HEAD='9d306d837fbddf1518b0035494baaf5c21c24488'
ACTOR='/root/source_reader_4e8f6a'
OWNER='huanjian_gc_20261108_fixed_spectrum_first_order'
ADVANCE='ASTIS-SA-20261108-GaussianComplexityFixedSpectrumFirstOrder'
H=lambda b:hashlib.sha256(b).hexdigest()
def dump(name,obj):
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def pincheck(pins):
 actual={rel:H((ROOT/rel).read_bytes()) for rel in pins}
 assert actual==pins,(actual,pins)
 return actual
def prepcheck():
 raw=(PREP/'preparation-manifest.json').read_bytes()
 assert H(raw)=='b8621af58567edcf9579ff4b50fb970d5a8c1cdbdf9abc05ab319439e5a2471b'
 m=json.loads(raw)
 assert len(m['artifacts'])==18
 for a in m['artifacts']:
  b=(PREP/a['path']).read_bytes()
  assert len(b)==a['bytes'] and H(b)==a['sha256'],a['path']
 assert H((BASE/'phase3/freeze_manifest.json').read_bytes())=='46fee361f6798fb8577c75479a563de2d30dbb2241059af624a29b3fbc4227a7'
 return H(raw)

assert not (OUT/'execution-started.json').exists(),'Do not rerun: inspect existing actual execution state.'
authraw=AUTH.read_bytes()
assert H(authraw)=='d2e298bcd1a5d1f3ec708af6180d45450bc54f55b529525697762e9c678de844'
auth=json.loads(authraw)
assert auth['authorization']=='EXECUTE_ONCE_NORMAL_PROVED_LOCAL_TO_VERIFIED'
assert auth['actor']==ACTOR and auth['proof_owner']==OWNER and auth['advance_id']==ADVANCE
assert auth['checked_candidate_commit']==HEAD
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert not git('diff','--name-only',HEAD).strip()
prepcheck()
beforepins=pincheck(auth['additional_raw_preservation_pins'])
beforeledger=LEDGER.read_bytes();beforeaudit=AUDIT.read_bytes()
assert beforeledger==(PREP/'substantive_advances.before.jsonl').read_bytes()
assert H(beforeaudit)=='ff19477ff58f2bedfb7790b6edd006d05b0386185011e6d21a9fa47f28651e4e'
proposal=(PREP/'proposed-accepted-audit.json').read_bytes()
assert H(proposal)==auth['bindings']['proposal_sha256']
(OUT/'root-authorization.actual.json').write_bytes(authraw)
(OUT/'canonical-audit.before.json').write_bytes(beforeaudit)
(OUT/'substantive_advances.before.jsonl').write_bytes(beforeledger)
command=[
 'python3',
 '.astis/semantic-neutral-20261108/src_4e8f6a/verification-transition-preparation/apply_normal_verified_once.py',
 '--execute','--authorization-file',
 '.astis/semantic-neutral-20261108/src_4e8f6a/verification-transition-preparation/root-authorization.json']
dump('execution-started.json',{
 'started_utc':now(),'command':command,'checked_candidate_commit':HEAD,
 'authorization_raw_sha256':H(authraw),'actor':ACTOR,'proof_owner':OWNER,
 'proposal_sha256':H(proposal),'canonical_audit_before_sha256':H(beforeaudit),
 'ledger_before_sha256':H(beforeledger),'ledger_before_bytes':len(beforeledger),
 'additional_raw_pins_before':beforepins,
 'scope':'Exactly one frozen helper execution and its one normal API call. Wrapper adds only authorized pre/post checks and owned evidence; no rollback or retry.'
})
start=time.time()
try:
 run=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 elapsed=time.time()-start
 (OUT/'normal-api.actual.raw.log').write_bytes(run.stdout)
 dump('foreground-command-receipt.json',{
  'command':command,'returncode':run.returncode,'elapsed_seconds':elapsed,
  'completed_utc':now(),'raw_log':'normal-api.actual.raw.log',
  'raw_log_sha256':H(run.stdout),'raw_log_bytes':len(run.stdout),
  'checked_candidate_commit':HEAD,'authorization_raw_sha256':H(authraw)})
 # Always preserve actual post-command bytes before deciding success/failure.
 afterledger=LEDGER.read_bytes();afteraudit=AUDIT.read_bytes()
 (OUT/'substantive_advances.after.jsonl').write_bytes(afterledger)
 (OUT/'canonical-audit.after.json').write_bytes(afteraudit)
 if afterledger.startswith(beforeledger):
  (OUT/'normal-api.exact-append.jsonl').write_bytes(afterledger[len(beforeledger):])
 if run.returncode:
  raise RuntimeError('Frozen helper failed with return code '+str(run.returncode)+'. STOP; no retry or automatic rollback.')
 assert afteraudit==proposal
 assert afterledger.startswith(beforeledger)
 append=afterledger[len(beforeledger):]
 assert append.endswith(b'\n') and len(append.splitlines())==1
 event=json.loads(append)
 assert event['event']=='transition' and event['schema_version']==4
 assert event['advance_id']==ADVANCE and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
 assert event['worker_id']==ACTOR
 expected_evidence=json.loads((PREP/'normal-verification-evidence.json').read_bytes())
 assert event['evidence']==expected_evidence
 assert event['evidence']['verified_commit']==HEAD
 assert event['evidence']['verifier_id']==ACTOR
 afterpins=pincheck(auth['additional_raw_preservation_pins'])
 prepcheck()
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 changed=sorted(git('diff','--name-only',HEAD).decode().splitlines())
 assert changed==sorted(auth['allowed_tracked_mutation_paths']),changed
 actual_helper_receipt=PREP/'execution/normal-verification-success.json'
 assert actual_helper_receipt.is_file()
 helper_receipt=json.loads(actual_helper_receipt.read_bytes())
 assert helper_receipt['foreign_284_SAU_states_unchanged']
 assert helper_receipt['all_444_frontier_artifacts_unchanged']
 assert helper_receipt['all_frozen_review_originals_unchanged']
 (OUT/'frozen-helper.actual-success.json').write_bytes(actual_helper_receipt.read_bytes())
 dump('execution-preservation-receipt.json',{
  'completed_utc':now(),'checked_code_commit':HEAD,
  'actor':ACTOR,'proof_owner':OWNER,'advance_id':ADVANCE,
  'normal_API_event_count':1,'from_state':'PROVED_LOCAL','to_state':'VERIFIED',
  'canonical_audit_before_sha256':H(beforeaudit),'accepted_successor_audit_sha256':H(afteraudit),
  'ledger_old_prefix_sha256':H(beforeledger),'ledger_after_sha256':H(afterledger),
  'ledger_old_prefix_exact':True,'appended_event_raw_sha256':H(append),'appended_event_bytes':len(append),
  'appended_event_file':'normal-api.exact-append.jsonl',
  'ledger_before_archive':'substantive_advances.before.jsonl','ledger_after_archive':'substantive_advances.after.jsonl',
  'all_additional_raw_preservation_pins_unchanged':beforepins==afterpins,
  'additional_raw_pins_before':beforepins,'additional_raw_pins_after':afterpins,
  'foreign_284_SAU_states_unchanged':True,'all_444_frontier_artifacts_unchanged':True,
  'original_18_preparation_payloads_unchanged':True,'frozen_Phase1_2_3_and_public_provenance_unchanged':True,
  'discovery_and_foreign_audits_unchanged':True,'git_index_and_HEAD_unchanged':True,
  'actual_tracked_diff_exactly_two_paths':changed,
  'chronology':'Checked 9d306d contains blind predecessor. After separate root authorization d2e298, exact accepted successor bytes were adopted in the worktree and the real API appended its actual later transition time. No retroactive checked-commit or accepted-source-at-9d306d claim.',
  'not_performed':['Any second normal API','STAB','Frontier/model/README/source/config mutation','Commit/stage/remote','Browser/rootGate/site/pixel acceptance','Automatic rollback']
 })
 dump('execution-result.json',{
  'status':'NORMAL_VERIFIED_EXECUTED_ONCE_AND_PRESERVATION_PASSED',
  'normal_API_event_created_at':event['created_at'],
  'checked_candidate_commit':HEAD,'actor':ACTOR,'proof_owner':OWNER,
  'source_review_verdict':'equivalent-after-elaboration',
  'scope':'Selected local producer/private forward consumer, source/module/freshLean/owned STATIC reader; no integration/runtime/root acceptance.',
  'further_API_authorized':False
 })
 print(json.dumps({'status':'NORMAL_VERIFIED_EXECUTED_ONCE_AND_PRESERVATION_PASSED',
  'returncode':run.returncode,'event_created_at':event['created_at'],
  'accepted_audit_sha256':H(afteraudit),'exact_append_sha256':H(append),
  'ledger_after_sha256':H(afterledger),'tracked_diff':changed,'further_API_run':False},indent=2))
except BaseException:
 dump('execution-failure.json',{
  'failed_utc':now(),'traceback':traceback.format_exc(),
  'actual_audit_sha256':H(AUDIT.read_bytes()),'actual_ledger_sha256':H(LEDGER.read_bytes()),
  'actual_tracked_diff':git('diff','--name-only',HEAD).decode().splitlines(),
  'policy':'STOP. No further API, no retry and no automatic rollback. Report actual partial state to root.'})
 raise
