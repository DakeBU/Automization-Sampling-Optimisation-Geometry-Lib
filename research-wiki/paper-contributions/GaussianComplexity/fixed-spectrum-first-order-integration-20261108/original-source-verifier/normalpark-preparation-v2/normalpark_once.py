"""Preparation only by default. No browser, source verdict, audit copy or commit.

Only a separate future exact root authorization plus actual bound acceptance
artifacts can enable the one normal STABILIZING -> VERIFIED API call.
"""
from datetime import datetime,timezone
from pathlib import Path
import argparse,copy,json,sys,traceback
sys.dont_write_bytecode=True
from park_common import *

def bindings():
 return {'helper_sha256':sha(Path(__file__).read_bytes()),
  'common_sha256':sha((PREP/'park_common.py').read_bytes()),
  'baseline_sha256':sha((PREP/'preservation-baseline.json').read_bytes()),
  'original_V_raw_sha256':sha((PREP/'original-V306.exact.jsonl').read_bytes()),
  'original_STAB_raw_sha256':sha((PREP/'original-STAB621.exact.jsonl').read_bytes())}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--acceptance-bundle',type=Path,default=PREP/'acceptance-inputs.template.json')
 p.add_argument('--execute',action='store_true')
 p.add_argument('--authorization-file',type=Path)
 p.add_argument('--authorization-sha256')
 args=p.parse_args()
 b=readjson(PREP/'preservation-baseline.json')
 assert sha((PREP/'original-V306.exact.jsonl').read_bytes())==V_SHA
 assert sha((PREP/'original-STAB621.exact.jsonl').read_bytes())==STAB_SHA
 original=json.loads((PREP/'original-V306.exact.jsonl').read_bytes())
 assert original['worker_id']==original['evidence']['verifier_id']==ACTOR
 assert original['evidence']['verified_commit']==CHECKED
 assert original['evidence']['source_audit']['proposed_successor_sha256']==AUDIT_SHA
 assert original['from_state']=='PROVED_LOCAL' and original['to_state']=='VERIFIED'
 s=protected(b);own=s[ADV]
 assert own==b['own_STAB_state'] and own['state']=='STABILIZING'
 assert own['latest_evidence']['integration_owner']==INTEGRATOR and own['last_actor']==INTEGRATOR
 assert [k for k,v in s.items() if v['state']=='STABILIZING']==[ADV]
 before=(PREP/'ledger-before-park.exact.jsonl').read_bytes()
 assert LEDGER.read_bytes()==before and sha(before)==b['ledger_before_sha256']
 bundle_raw=args.acceptance_bundle.read_bytes();bundle=json.loads(bundle_raw)
 try:
  post=validated_acceptance(bundle)
 except (AssertionError,KeyError,FileNotFoundError,TypeError,ValueError) as exc:
  if args.execute:raise
  print(json.dumps({'status':'FAIL_CLOSED_EXTERNAL_ACCEPTANCE_NOT_READY',
   'reason':str(exc),'acceptance_bundle_sha256':sha(bundle_raw),
   'normal_API_called':False,'canonical_mutation':False},indent=2))
  return 3
 evidence=copy.deepcopy(original['evidence'])
 assert 'post_integration_normalpark' not in evidence
 post['acceptance_bundle']={'path':args.acceptance_bundle.resolve().relative_to(ROOT).as_posix(),'sha256':sha(bundle_raw)}
 post['original_V_evidence_canonical_sha256']=sha(canonical(original['evidence']))
 evidence['post_integration_normalpark']=post
 assert {k:v for k,v in evidence.items() if k!='post_integration_normalpark'}==original['evidence']
 assert set(evidence)==set(original['evidence'])|{'post_integration_normalpark'}
 advance._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
 if not args.execute:
  print(json.dumps({'status':'READY_FOR_SEPARATE_EXACT_ROOT_AUTHORIZATION',
   'bindings':bindings(),'acceptance_bundle_sha256':sha(bundle_raw),
   'original_V_evidence_preserved_exactly':True,
   'normal_API_called':False,'canonical_mutation':False},indent=2))
  return 0
 assert args.authorization_file and args.authorization_sha256
 authraw=args.authorization_file.read_bytes();assert sha(authraw)==args.authorization_sha256
 auth=json.loads(authraw)
 assert auth['authorization']=='EXECUTE_ONCE_EXISTING_VERIFIED_POST_INTEGRATION_NORMALPARK_V2'
 assert auth['authorized_by']=='/root' and auth['actor']==ACTOR and auth['proof_owner']==OWNER
 assert auth['accepted_immutable_core']==CORE and auth['checked_source_commit_to_preserve']==CHECKED
 assert auth['advance_id']==ADV and auth['current_STAB_owner']==INTEGRATOR
 assert auth['bindings']==bindings()
 assert auth['acceptance_bundle_sha256']==sha(bundle_raw)
 assert auth['allowed_tracked_mutation_paths']==['runs/substantive_advances.jsonl']
 assert auth['new_source_verdict'] is False and auth['no_audit_frontier_model_README_source_config_commit_browser_remote_mutation'] is True
 execution=BASE/'normalpark-execution-v2'
 assert not (execution/'execution-started.json').exists(),'One-shot already started: stop, inspect; never retry API blindly'
 execution.mkdir(exist_ok=True)
 dump(execution/'execution-started.json',{'started_utc':datetime.now(timezone.utc).isoformat(),
  'actor':ACTOR,'proof_owner':OWNER,'integration_owner':INTEGRATOR,'bindings':bindings(),
  'authorization_raw_sha256':sha(authraw),'acceptance_bundle_sha256':sha(bundle_raw),
  'accepted_core':CORE,'checked_source_commit_preserved':CHECKED,'original_V_append_sha256':V_SHA,
  'source_V_first_carrying_commit':SOURCEV_COMMIT,'source_audit_unchanged_sha256':AUDIT_SHA})
 (execution/'before-ledger.exact.jsonl').write_bytes(before)
 (execution/'acceptance-bundle.actual.json').write_bytes(bundle_raw)
 dump(execution/'normalpark-evidence.actual.json',evidence)
 try:
  protected(b)
  advance.transition_advance(ADV,'VERIFIED',worker_id=ACTOR,
   modes=['post-integration-normalpark'],evidence=evidence)
  after=LEDGER.read_bytes();assert after.startswith(before)
  append=after[len(before):];assert append.endswith(b'\n') and len(append.splitlines())==1
  event=json.loads(append)
  assert event['advance_id']==ADV and event['from_state']=='STABILIZING' and event['to_state']=='VERIFIED'
  assert event['worker_id']==ACTOR and event['evidence']==evidence
  assert {k:v for k,v in event['evidence'].items() if k!='post_integration_normalpark'}==original['evidence']
  afterstates=protected(b,after=True)
  assert afterstates[ADV]['state']=='VERIFIED' and afterstates[ADV]['last_actor']==ACTOR
  assert afterstates[ADV]['owner_id']==OWNER
  assert afterstates[ADV]['latest_evidence']==evidence
  assert not any(v['state']=='STABILIZING' for v in afterstates.values())
  (execution/'after-ledger.exact.jsonl').write_bytes(after)
  (execution/'normalpark-append.exact.jsonl').write_bytes(append)
  dump(execution/'normalpark-success.json',{'status':'ONE_NORMAL_API_PARK_COMPLETE',
   'event_created_at':event['created_at'],'actor':ACTOR,'proof_owner':OWNER,
   'original_V_evidence_all_keys_values_exact':True,'only_new_evidence_key':'post_integration_normalpark',
   'checked_source_commit_preserved':CHECKED,'source_audit_unchanged_sha256':AUDIT_SHA,
   'accepted_immutable_core':CORE,'old_ledger_prefix_exact':True,
   'append_sha256':sha(append),'ledger_after_sha256':sha(after),
   'foreign_284_SAU_states_unchanged':True,'foreign_443_frontier_bytes_unchanged':True,
   'own_frontier_also_unchanged':True,'discovery_models_README_source_config_frozen_records_unchanged':True,
   'tracked_diff_exactly_one_ledger':True,'new_source_verdict':False,
   'no_more_API_commit_browser_or_remote':True})
  print(json.dumps({'status':'ONE_NORMAL_API_PARK_COMPLETE','append_sha256':sha(append),'new_source_verdict':False},indent=2))
 except BaseException:
  dump(execution/'normalpark-failure.json',{'error':traceback.format_exc(),
   'ledger_sha256':sha(LEDGER.read_bytes()),'source_audit_sha256':sha(AUDIT.read_bytes()),
   'instruction':'STOP; no second API, retry, automatic rollback, canonical mutation or invented acceptance.'})
  raise
 return 0

if __name__=='__main__':raise SystemExit(main())
