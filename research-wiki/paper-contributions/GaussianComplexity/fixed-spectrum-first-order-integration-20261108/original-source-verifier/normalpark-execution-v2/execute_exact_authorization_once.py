from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,time,sys,traceback
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261108/src_4e8f6a'
PREP=BASE/'normalpark-preparation-v2'
OUT=BASE/'normalpark-execution-v2'
R=ROOT/'.astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108'
AUTH=R/'root-exact-normalpark-v2-execution-authorization.json'
BUNDLE=R/'actual-accepted-normalpark-bundle-v2.json'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-first-order.json'
CORE='9b1e90d25711668203c6e252cfe5a748f95c8ad4'
ACTOR='/root/source_reader_4e8f6a'
OWNER='huanjian_gc_20261108_fixed_spectrum_first_order'
ADV='ASTIS-SA-20261108-GaussianComplexityFixedSpectrumFirstOrder'
AUDIT_SHA='a14867ad5fd8723933500d4c264c91c05d6b11ef510090c3b6da216fcb402b57'
H=lambda data:hashlib.sha256(data).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def dump(name,obj):(OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def check_preparation():
 data=(PREP/'preparation-manifest.json').read_bytes()
 assert H(data)=='b3b518fde0cab9876668bffc4ee8dbc075cb5c48d6f6abc7d17c8dc6adeb190a'
 m=json.loads(data);assert len(m['artifacts'])==23
 for a in m['artifacts']:
  raw=(PREP/a['path']).read_bytes()
  assert len(raw)==a['bytes'] and H(raw)==a['sha256'],a['path']
 return H(data)

assert not (OUT/'foreground-wrapper-started.json').exists(),'Do not retry an actual one-shot command.'
assert not (OUT/'execution-started.json').exists(),'Frozen helper already started; stop and inspect.'
authraw=AUTH.read_bytes();bundleraw=BUNDLE.read_bytes()
assert H(authraw)=='59288f654ecdbf7874bb05eb3d3018c7567aff6ae6c2a0c3b73512c1f81b64ec'
assert H(bundleraw)=='17d74c0c32834a12de098e1da0253c2cb22a13536334bf1c57324b0435356475'
auth=json.loads(authraw);bundle=json.loads(bundleraw)
assert auth['actor']==ACTOR and auth['proof_owner']==OWNER and auth['advance_id']==ADV
assert auth['authorization']=='EXECUTE_ONCE_EXISTING_VERIFIED_POST_INTEGRATION_NORMALPARK_V2'
assert auth['allowed_tracked_mutation_paths']==['runs/substantive_advances.jsonl']
assert git('rev-parse','HEAD').decode().strip()==CORE
assert not git('diff','--name-only',CORE).strip()
check_preparation()
baseline=json.loads((PREP/'preservation-baseline.json').read_bytes())
before=LEDGER.read_bytes();auditbefore=AUDIT.read_bytes()
assert before==(PREP/'ledger-before-park.exact.jsonl').read_bytes()
assert H(auditbefore)==AUDIT_SHA
originalraw=(PREP/'original-V306.exact.jsonl').read_bytes()
assert H(originalraw)=='306b3ebcc5e659b5f2877a9ebe8ff010c09183a47c4b65be767b4ed489e9a99f'
original=json.loads(originalraw);assert len(original['evidence'])==10
inputs={}
raw_inputs=OUT/'actual-inputs';raw_inputs.mkdir(exist_ok=True)
for role,ref in {'browser_context':bundle['browser_context'],**bundle['artifacts']}.items():
 p=(ROOT/ref['path']).resolve();assert p.is_relative_to(ROOT)
 raw=p.read_bytes();assert H(raw)==ref['sha256']
 inputs[p.relative_to(ROOT).as_posix()]=H(raw)
 (raw_inputs/(role+'.json')).write_bytes(raw)
reportref=bundle['artifacts']['browser_report']
report=json.loads((ROOT/reportref['path']).read_bytes())
for row in report['screenshots']:
 p=(ROOT/reportref['path']).parent/row['file'];assert H(p.read_bytes())==row['sha256']
 inputs[p.relative_to(ROOT).as_posix()]=row['sha256']
receipt=json.loads((ROOT/bundle['artifacts']['browser_command_receipt']['path']).read_bytes())
log=Path(receipt['log']).resolve();assert log.is_relative_to(ROOT)
assert H(log.read_bytes())==receipt['log_sha256'];inputs[log.relative_to(ROOT).as_posix()]=receipt['log_sha256']
(OUT/'root-authorization.actual.json').write_bytes(authraw)
(OUT/'acceptance-bundle.actual.json').write_bytes(bundleraw)
(OUT/'wrapper-before-ledger.exact.jsonl').write_bytes(before)
(OUT/'source-audit.before.json').write_bytes(auditbefore)
command=['python3',
 '.astis/semantic-neutral-20261108/src_4e8f6a/normalpark-preparation-v2/normalpark_once.py',
 '--acceptance-bundle',
 '.astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108/actual-accepted-normalpark-bundle-v2.json',
 '--execute','--authorization-file',
 '.astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108/root-exact-normalpark-v2-execution-authorization.json',
 '--authorization-sha256','59288f654ecdbf7874bb05eb3d3018c7567aff6ae6c2a0c3b73512c1f81b64ec']
dump('foreground-wrapper-started.json',{
 'started_utc':now(),'command':command,'actor':ACTOR,'proof_owner':OWNER,
 'accepted_core':CORE,'root_authorization_sha256':H(authraw),'actual_bundle_sha256':H(bundleraw),
 'original_V306_sha256':H(originalraw),'ledger_before_sha256':H(before),
 'source_audit_before_sha256':H(auditbefore),'runtime_actual_input_raw_pins':inputs,
 'scope':'Execute frozen exact helper once only. No independent new source or pixel verdict; consume actual native reviews and exact root authority.'})
start=time.time()
try:
 run=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 elapsed=time.time()-start
 (OUT/'normalpark.actual.raw.log').write_bytes(run.stdout)
 dump('foreground-command-receipt.json',{
  'command':command,'returncode':run.returncode,'elapsed_seconds':elapsed,'completed_utc':now(),
  'raw_log':'normalpark.actual.raw.log','raw_log_sha256':H(run.stdout),'raw_log_bytes':len(run.stdout),
  'root_authorization_raw_sha256':H(authraw),'actual_bundle_raw_sha256':H(bundleraw),
  'helper_executions':1,'accepted_immutable_core':CORE})
 after=LEDGER.read_bytes();auditafter=AUDIT.read_bytes()
 (OUT/'wrapper-after-ledger.exact.jsonl').write_bytes(after)
 (OUT/'source-audit.after.json').write_bytes(auditafter)
 if after.startswith(before):
  (OUT/'wrapper-exact-normalpark-append.jsonl').write_bytes(after[len(before):])
 if run.returncode:raise RuntimeError('Frozen normalpark helper failed; STOP, no retry or rollback.')
 assert before== (OUT/'before-ledger.exact.jsonl').read_bytes()
 assert after==(OUT/'after-ledger.exact.jsonl').read_bytes()
 assert after.startswith(before)
 append=after[len(before):];assert append.endswith(b'\n') and len(append.splitlines())==1
 assert append==(OUT/'normalpark-append.exact.jsonl').read_bytes()
 event=json.loads(append)
 assert event['advance_id']==ADV and event['worker_id']==ACTOR
 assert event['from_state']=='STABILIZING' and event['to_state']=='VERIFIED'
 evidence=event['evidence']
 assert set(evidence)==set(original['evidence'])|{'post_integration_normalpark'}
 assert {k:v for k,v in evidence.items() if k!='post_integration_normalpark'}==original['evidence']
 assert evidence['verified_commit']=='9d306d837fbddf1518b0035494baaf5c21c24488'
 assert evidence['verifier_id']==ACTOR
 assert auditafter==auditbefore and H(auditafter)==AUDIT_SHA
 assert git('rev-parse','HEAD').decode().strip()==CORE
 assert git('diff','--name-only',CORE).decode().splitlines()==['runs/substantive_advances.jsonl']
 check_preparation()
 for rel,h in inputs.items():assert H((ROOT/rel).read_bytes())==h,rel
 for group in ['critical_raw_pins','frozen_originals']:
  for rel,h in baseline[group].items():assert H((ROOT/rel).read_bytes())==h,rel
 for rel,h in baseline['frontier_raw_hashes'].items():assert H((ROOT/rel).read_bytes())==h,rel
 success=json.loads((OUT/'normalpark-success.json').read_bytes())
 assert success['foreign_284_SAU_states_unchanged']
 assert success['foreign_443_frontier_bytes_unchanged'] and success['own_frontier_also_unchanged']
 dump('wrapper-postconditions.json',{
  'completed_utc':now(),'actor':ACTOR,'proof_owner':OWNER,'accepted_core':CORE,
  'original_checked_source_commit_unchanged':evidence['verified_commit'],
  'original_V306_evidence_all10_fields_values_exact':True,'only_added_evidence_key':'post_integration_normalpark',
  'source_audit_unchanged_sha256':AUDIT_SHA,'old_ledger_prefix_exact':True,
  'one_append_sha256':H(append),'ledger_before_sha256':H(before),'ledger_after_sha256':H(after),
  'event_created_at':event['created_at'],'normal_API_calls':1,
  'foreign284_states_preserved':True,'foreign443_frontiers_and_own_frontier_preserved':True,
  'all501_frozen_originals_preserved':len(baseline['frozen_originals'])==501,
  'all40_critical_raw_pins_preserved':len(baseline['critical_raw_pins'])==40,
  'all38_actual_original_images_and_native_input_bytes_unchanged':True,
  'original_v2_prep23_payloads_unchanged':True,
  'HEAD_and_index_unchanged':True,'tracked_diff':['runs/substantive_advances.jsonl'],
  'sole_STAB_empty':True,'new_source_verdict':False,'further_API_called':False,
  'browser_or_OS_or_commit_or_remote_called_by_this_execution':False,
  'receipt_ambient_note':'Actual external browser receipt contains an ASTIS_ATLAS_ROOT metadata path. This actor did not access .atlas-upstream or use it as mathematical evidence.'})
 print(json.dumps({'status':'EXACT_NORMALPARK_V2_EXECUTED_ONCE_PRESERVATION_PASSED',
  'returncode':run.returncode,'event_created_at':event['created_at'],'append_sha256':H(append),
  'ledger_after_sha256':H(after),'original_V_all10_fields_exact':True,'sole_STAB_empty':True,
  'tracked_diff':['runs/substantive_advances.jsonl'],'further_API_called':False},indent=2))
except BaseException:
 dump('foreground-wrapper-failure.json',{
  'failed_utc':now(),'traceback':traceback.format_exc(),
  'current_ledger_sha256':H(LEDGER.read_bytes()),'current_source_audit_sha256':H(AUDIT.read_bytes()),
  'actual_tracked_diff':git('diff','--name-only',CORE).decode().splitlines(),
  'instruction':'STOP. No second API, retry, automatic rollback or further canonical mutation. Report actual partial state.'})
 raise
