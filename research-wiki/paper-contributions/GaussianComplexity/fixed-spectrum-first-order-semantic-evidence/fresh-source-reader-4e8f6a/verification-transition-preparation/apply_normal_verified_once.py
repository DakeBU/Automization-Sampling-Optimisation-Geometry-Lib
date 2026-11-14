"""Prepared one-shot sourceV helper. Defaults to read-only prospective checks.

Execution requires a new exact root authorization. This file is not itself
authorization. It never edits frontier/model/README/discovery state or commits.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,os,sys,traceback
sys.dont_write_bytecode=True
from transition_common import *

def bindings():
 return {
  'proposal_sha256':sha((PREP/'proposed-accepted-audit.json').read_bytes()),
  'helper_sha256':sha(Path(__file__).read_bytes()),
  'common_sha256':sha((PREP/'transition_common.py').read_bytes()),
  'baseline_sha256':sha((PREP/'preservation-baseline.json').read_bytes()),
  'normal_evidence_sha256':sha((PREP/'normal-verification-evidence.json').read_bytes()),
  'prospective_preflight_sha256':sha((PREP/'prospective-preflight.json').read_bytes())
 }

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--execute',action='store_true')
 parser.add_argument('--authorization-file',type=Path)
 args=parser.parse_args()
 baseline=readjson(PREP/'preservation-baseline.json')
 proposal=readjson(PREP/'proposed-accepted-audit.json')
 evidence=readjson(PREP/'normal-verification-evidence.json')
 assert sha(AUDIT.read_bytes())==AUDIT_BEFORE
 current=assert_protected(baseline)
 assert current[ADVANCE]==baseline['own_state']
 assert current[ADVANCE]['state']=='PROVED_LOCAL'
 assert current[ADVANCE]['publication_declarations']==[DECL]
 assert evidence['verifier_id']==ACTOR and evidence['verified_commit']==HEAD
 assert proposal['lean']['formalizer']==OWNER
 assert proposal['source_review']['reviewer']==ACTOR
 assert proposal['source_review']['scope'].endswith('STATIC source-review reader only.')
 assert ACTOR!=OWNER and ACTOR!=proposal['reconstruction']['decoder']
 oldprefix=(PREP/'substantive_advances.before.jsonl').read_bytes()
 assert LEDGER.read_bytes()==oldprefix
 advance._validate_transition_evidence('VERIFIED',evidence,schema_version=4)
 pre=prospective(proposal)
 assert not pre['schema_errors'] and not pre['publication_errors'],pre
 if not args.execute:
  receipt={'mode':'PREPARATION_ONLY_READ_ONLY_PREFLIGHT','checked_utc':datetime.now(timezone.utc).isoformat(),
   'bindings':bindings(),'prospective':pre,'canonical_audit_written':False,'normal_transition_API_called':False,
   'sau_count':len(current),'foreign_sau_count':len(current)-1,'frontier_artifacts':len(baseline['frontier_hashes'])}
  writejson(PREP/'helper-dry-preflight.json',receipt)
  print(json.dumps(receipt,ensure_ascii=False,indent=2))
  return 0
 # A template, prior process authorization, or preparation-only permission
 # cannot satisfy this independently supplied exact authorization guard.
 assert args.authorization_file is not None,'Separate exact root authorization file required'
 auth=readjson(args.authorization_file)
 assert auth.get('authorization')=='EXECUTE_ONCE_NORMAL_PROVED_LOCAL_TO_VERIFIED'
 assert auth.get('authorized_by')=='/root'
 assert auth.get('checked_candidate_commit')==HEAD
 assert auth.get('actor')==ACTOR and auth.get('proof_owner')==OWNER
 assert auth.get('advance_id')==ADVANCE
 assert auth.get('bindings')==bindings()
 assert sorted(auth.get('allowed_tracked_mutation_paths',[]))==sorted(baseline['allowed_tracked_mutation_paths'])
 assert auth.get('no_STAB_no_frontier_no_model_no_remote') is True
 execution=PREP/'execution';execution.mkdir(exist_ok=True)
 assert not (execution/'normal-verification-success.json').exists(),'One-shot helper already completed'
 # Recheck immediately before the first canonical write.
 assert_protected(baseline)
 try:
  temp=execution/'accepted-audit-install.tmp'
  temp.write_bytes((PREP/'proposed-accepted-audit.json').read_bytes())
  os.replace(temp,AUDIT)
  assert sha(AUDIT.read_bytes())==bindings()['proposal_sha256']
  # The sole normal state-changing API call; no monkeypatch/bypass or alternate
  # transition implementation is used. The normal publication gate runs here.
  advance.transition_advance(ADVANCE,'VERIFIED',worker_id=ACTOR,
    modes=['independent-verification'],evidence=evidence)
  afterraw=LEDGER.read_bytes()
  assert afterraw.startswith(oldprefix)
  appended=afterraw[len(oldprefix):]
  assert appended.endswith(b'\n') and len(appended.splitlines())==1
  event=json.loads(appended)
  assert event['schema_version']==4 and event['event']=='transition'
  assert event['advance_id']==ADVANCE and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
  assert event['worker_id']==ACTOR and event['evidence']==evidence
  assert event['modes']==['independent-verification']
  after=assert_protected(baseline,after=True)
  assert after[ADVANCE]['state']=='VERIFIED' and after[ADVANCE]['last_actor']==ACTOR
  assert after[ADVANCE]['publication_declarations']==[DECL]
  allowed_own_fields={'state','last_actor','modes','latest_evidence','updated_at'}
  assert {k:v for k,v in after[ADVANCE].items() if k not in allowed_own_fields}=={
    k:v for k,v in baseline['own_state'].items() if k not in allowed_own_fields}
  receipt={'mode':'NORMAL_API_EXECUTED_ONCE_AFTER_SEPARATE_EXACT_ROOT_AUTHORIZATION',
   'checked_code_commit':HEAD,'actor':ACTOR,'proof_owner':OWNER,'bindings':bindings(),
   'authorization_file_sha256':sha(args.authorization_file.read_bytes()),
   'accepted_audit_sha256':sha(AUDIT.read_bytes()),'ledger_old_prefix_sha256':sha(oldprefix),
   'ledger_appended_event':event,'ledger_exactly_one_append':True,
   'foreign_284_SAU_states_unchanged':True,'all_444_frontier_artifacts_unchanged':True,
   'discovery_and_foreign_audits_unchanged':True,'all_frozen_review_originals_unchanged':True,
   'tracked_diff_exactly_own_audit_and_ledger':tracked_changes(),
   'chronology':'Checked code and blind-audit tree at 9d306d preceded this sourceV metadata/ledger successor in the worktree. No claim accepted audit existed at checked commit. Any later sourceV commit is distinct.',
   'no_STAB_no_frontier_no_model_no_rootGate_no_site_no_remote':True}
  writejson(execution/'normal-verification-success.json',receipt)
  print(json.dumps(receipt,ensure_ascii=False,indent=2))
 except BaseException:
  writejson(execution/'normal-verification-failure.json',{
   'error':traceback.format_exc(),'checked_candidate_commit':HEAD,
   'current_audit_sha256':sha(AUDIT.read_bytes()),'current_ledger_sha256':sha(LEDGER.read_bytes()),
   'instruction':'STOP. No second API call or automatic shared rollback. Root must inspect partial state and separately authorize any recovery.'})
  raise
 return 0

if __name__=='__main__':raise SystemExit(main())
