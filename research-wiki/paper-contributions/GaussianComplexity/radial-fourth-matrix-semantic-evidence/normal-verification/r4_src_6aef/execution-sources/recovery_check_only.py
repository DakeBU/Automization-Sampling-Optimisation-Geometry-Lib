from pathlib import Path
import hashlib, json, os, stat, subprocess, sys

ROOT=Path.cwd();sys.path.insert(0,str(ROOT))
from tools.astis_advance import _replay_advances, _replay_discoveries
BASE=ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/normal-verification'
LOCAL=BASE/'local-only'
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence'
OUT=E/'normal-verification/r4_src_6aef'
ADV='ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix';ACTOR='/root/radial_fourth_fresh_source_6aef'
HEAD='3ba24f46ea74e4537e57824982dfee9f51aeac27';MATH='69a3336dde302c4a34dbd88708ff6226b2bd0e87'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def binding(p):
    p=Path(p);b=p.read_bytes();return {'path':str(p.relative_to(ROOT) if p.is_absolute() else p),'bytes':len(b),'sha256':sha(b)}
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,check=True,capture_output=True).stdout
baseline=json.loads((LOCAL/'baseline.full.local-only.json').read_bytes())
assert git('rev-parse','HEAD').decode().strip()==HEAD
prefix=(LOCAL/'advances.prefix.original.local-only.jsonl').read_bytes()
after=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert after.startswith(prefix)
added=after[len(prefix):];rows=[json.loads(x) for x in added.splitlines() if x.strip()];assert len(rows)==1
event=rows[0];assert event['advance_id']==ADV and event['event']=='transition' and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED' and event['worker_id']==ACTOR
assert (OUT/'actual-VERIFIED-append.exact.jsonl').read_bytes()==added
evidence=json.loads((OUT/'VERIFIED-evidence.full.json').read_bytes());assert event['evidence']==evidence
plraw=(E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes();pl=json.loads(plraw)
assert sha(plraw)=='f4bc0bedf3a46a4232f369a55a28ce88cc33122bd9b2a50419912cc381030773'
assert evidence['proved_local_evidence']==pl and (OUT/'PROVED_LOCAL-evidence.original.full.json').read_bytes()==plraw
plappend=(E/'actual-PROVED_LOCAL-append.exact.jsonl').read_bytes()
assert sha(plappend)=='a46e0b650bf2aa227cc9b4d2ee322ec06204d947199019ab4575dd76481a6262'
assert (OUT/'PROVED_LOCAL-append.original.exact.jsonl').read_bytes()==plappend
assert evidence['proved_local_exact_append_binding']['sha256']==sha(plappend)
transaction=json.loads((OUT/'actual-VERIFIED-transaction.receipt.json').read_bytes())
assert transaction['exit_code']==0 and transaction['normal_transition_API_attempts']==1
for name in ['stdout','stderr']:assert sha((OUT/('actual-VERIFIED-transaction.'+name)).read_bytes())==transaction[name+'_sha256']
frontier=json.loads((OUT/'post-VERIFIED-whole-frontier.receipt.json').read_bytes());assert frontier['exit_code']==0
for name in ['stdout','stderr']:assert sha((OUT/('post-VERIFIED-whole-frontier.'+name)).read_bytes())==frontier[name+'_sha256']
assert frontier['argv']==['/opt/anaconda3/bin/python','-B','tools/astis_frontier_cells.py','check']

states=_replay_advances([json.loads(x) for x in after.splitlines() if x.strip()]);foreign={k:v for k,v in states.items() if k!=ADV}
assert len(foreign)==303 and foreign==baseline['foreign_states']
discovery_raw=(ROOT/'runs/substantive_discoveries.jsonl').read_bytes()
assert discovery_raw==(LOCAL/'discoveries.original.local-only.jsonl').read_bytes()
discovery_states=_replay_discoveries([json.loads(x) for x in discovery_raw.splitlines() if x.strip()])
assert len(discovery_states)==43 and discovery_states==baseline['discovery_states']
C=ROOT/baseline['C'];oldraw=(LOCAL/'C.before.original.local-only.json').read_bytes();old=json.loads(oldraw);newraw=C.read_bytes();new=json.loads(newraw)
expected=json.loads(oldraw);expected['status']='independently_verified'
expected['evidence']['independent_verification']=str((E/'actual-VERIFIED-independent-decision.json').relative_to(ROOT));assert new==expected
expectedraw=oldraw.replace(b'"status": "proved_locally"',b'"status": "independently_verified"',1).replace(b'"independent_verification": ""',b'"independent_verification": '+json.dumps(expected['evidence']['independent_verification']).encode(),1)
assert newraw==expectedraw
older={}
for p in (ROOT/'research-wiki/frontier-cells').rglob('*'):
    if stat.S_ISREG(p.lstat().st_mode) and p!=C:older[str(p.relative_to(ROOT))]=sha(p.read_bytes())
assert len(older)==463 and older==baseline['older_frontier_files'] and 'research-wiki/frontier-cells/README.md' in older
tracked={}
for name,entry in baseline['tracked_files'].items():
    p=ROOT/name
    if p.is_symlink():tracked[name]={'type':'symlink','sha256':sha(os.readlink(p).encode())}
    elif p.is_file():tracked[name]={'type':'file','sha256':sha(p.read_bytes())}
    elif p.is_dir():tracked[name]={'type':'directory'}
    else:tracked[name]={'type':'missing'}
changed=sorted(k for k in tracked if tracked[k]!=baseline['tracked_files'][k])
allowed=sorted([baseline['C'],'runs/substantive_advances.jsonl']);assert changed==allowed
assert states[ADV]['state']=='VERIFIED' and states[ADV]['last_actor']==ACTOR
assert states[ADV]['owner_id']=='huanjian_gc_20261111_radial_fourth_matrix'
assert evidence['formalizer_API_pristine'] is False and evidence['pristine_chronology_certified'] is False
assert git('rev-parse','HEAD').decode().strip()==HEAD

prior_seal_hashes={
 'SOURCE_READING_SEAL.json':'920e93bff9d7929cf74b6d970d1afa19dbfb24c992efd943bc3de2e7288dd2d6',
 'type-only/TYPE_ONLY_SEAL.json':'e4de0841eed32fa0a440d97b7b5b26a10e4e596546d6e8e4226bfd48e0e81def',
 'code-only-review/CODE_ONLY_SEAL.json':'bee36251c109b374686cec519bcf80beb8ff9ac37e093157bbacf356b6afb3d7',
 'anti-anchored-review/ANTI_ANCHORED_REVIEW_SEAL.json':'b0161b7ee2648a4b4199ed0a41d562cd64780eb7ffde7454d219c12e7002e656'}
for name,h in prior_seal_hashes.items():
    p=BASE.parent/name;assert sha(p.read_bytes())==h
    for entry in json.loads(p.read_bytes())['artifacts']:assert sha((BASE.parent/entry['path']).read_bytes())==entry['sha256']

failure={'schema_version':1,'classification':'IMPLEMENTATION_FAILED_REPORTING_ONLY',
 'original_wrapper_actual_exit_code':1,'original_wrapper_tool_receipt':binding(OUT/'original-wrapper.actual-tool-receipt.json'),
 'normal_API_returned_successfully_before_reporting_failure':True,'normal_API_original_receipt':binding(OUT/'actual-VERIFIED-transaction.receipt.json'),
 'actual_normal_API_calls':1,'recovery_normal_API_calls':0,
 'failure_site':'execute_verified_transaction.py line148: tracked_changed asserted equal to [C] only.',
 'concrete_cause':'The reporting allowlist omitted the authorized runs/substantive_advances.jsonl append. The only changed existing tracked paths are exactly C and that ledger.',
 'recovery':'Separate check-only script recomputes every complete foreign/discovery state, ledger prefix,463 older hashes, exact two-field C delta and allowed tracked changes. It writes reports only; it does not rerun the transaction or mutate canonical control state.',
 'mathematics_or_evidence_refuted':False,'original_script_preserved':binding(OUT/'execution-sources/execute_verified_transaction.original.py')}
(OUT/'reporting-failure-and-recovery-diagnosis.json').write_bytes(enc(failure))
preservation={'schema_version':1,'kind':'hash-only preservation; full foreign/control snapshots remain local',
 'HEAD_before':HEAD,'HEAD_after':HEAD,'HEAD_unchanged':True,
 'advance_ledger':{'prefix_bytes':len(prefix),'prefix_sha256':sha(prefix),'exact_prefix_unchanged':True,'after_bytes':len(after),'after_sha256':sha(after),
  'one_exact_new_record':True,'append_sha256':sha(added),'advance':ADV,'from_state':'PROVED_LOCAL','to_state':'VERIFIED','actor':ACTOR},
 'foreign_FULL_replayed_advance_states':{'count':303,'complete_nested_objects_equal':True,'before_sha256':baseline['foreign_states_sha256'],'after_sha256':sha(canon(foreign))},
 'discovery_ledger':{'exact_bytes_unchanged':True,'before_sha256':baseline['discovery_ledger_sha256'],'after_sha256':sha(discovery_raw)},
 'all_discovery_FULL_states':{'count':43,'complete_nested_objects_equal':True,'before_sha256':baseline['discovery_states_sha256'],'after_sha256':sha(canon(discovery_states))},
 'older_frontier_regular_files':{'count':463,'README_included':True,'all_paths_and_hashes_equal':True,'before_inventory_sha256':baseline['older_frontier_files_sha256'],'after_inventory_sha256':sha(canon(older))},
 'C_only_allowed_fields_changed':{'path':baseline['C'],'before_sha256':sha(oldraw),'after_sha256':sha(newraw),
  'changed_fields':['status','evidence.independent_verification'],'no_other_field_changed':True,'exact_raw_bytes_equal_surgical_two_field_replacement':True},
 'tracked_tree':{'existing_tracked_paths_changed':changed,'exactly_authorized_C_and_advance_ledger':True,'all_other_existing_tracked_contents_unchanged':True},
 'proved_local_payload_unchanged_nested_under_proved_local_evidence':True,'proved_local_exact_append_binding_unchanged':True,
 'normal_transition_API_calls':1,'recovery_transition_API_calls':0,'other_ledger_mutation_API_calls':0,'event_replay_append_used':False,
 'actual_whole_frontier_after':binding(OUT/'post-VERIFIED-whole-frontier.receipt.json'),'actual_whole_frontier_exit_code':0,
 'original_reporting_wrapper_exit_code':1,'original_reporting_failure_preserved':True,'original_failure_does_not_change_successful_API_outcome':True,
 'all_four_prior_phase_seals_and_original_artifacts_unchanged':True,'full_local_snapshots_exported':False}
(OUT/'hash-only-preservation-report.json').write_bytes(enc(preservation))
outcome={'schema_version':1,'outcome':'VERIFIED','advance_id':ADV,'actor':ACTOR,'proof_owner':'huanjian_gc_20261111_radial_fourth_matrix',
 'normal_transition_API_calls':1,'recovery_transition_API_calls':0,'metadata_HEAD':HEAD,'native_mathematical_candidate':MATH,
 'actual_append':binding(OUT/'actual-VERIFIED-append.exact.jsonl'),'actual_transaction_receipt':binding(OUT/'actual-VERIFIED-transaction.receipt.json'),
 'independent_decision':binding(E/'actual-VERIFIED-independent-decision.json'),'VERIFIED_evidence':binding(OUT/'VERIFIED-evidence.full.json'),
 'C_status':'independently_verified','actual_whole_frontier_after':binding(OUT/'post-VERIFIED-whole-frontier.receipt.json'),'whole_frontier_exit_code':0,
 'hash_only_preservation_report':binding(OUT/'hash-only-preservation-report.json'),
 'original_reporting_wrapper_exit_code':1,'reporting_failure_diagnosis':binding(OUT/'reporting-failure-and-recovery-diagnosis.json'),
 'recovery_receipt_path':str((OUT/'recovery-check-only.receipt.json').relative_to(ROOT)),
 'formalizer_API_pristine':False,'pristine_chronology_certified':False,'truth_boundary':evidence['truth_boundary'],
 'no_further_canonical_state_mutation_by_this_reviewer':True}
(OUT/'actual-outcome.json').write_bytes(enc(outcome))
print(json.dumps({'outcome':'VERIFIED','normal_API_calls':1,'recovery_API_calls':0,'original_wrapper_exit_code':1,
 'foreign_FULL_states_preserved':303,'discovery_FULL_states_and_ledger_bytes_preserved':43,'older_regular_frontier_files_preserved':463,
 'only_authorized_C_and_ledger_changed':True,'C_only_two_fields_changed':True,'whole_frontier_exit_code':0,
 'append_sha256':sha(added),'preservation_report_sha256':sha((OUT/'hash-only-preservation-report.json').read_bytes()),
 'outcome_sha256':sha((OUT/'actual-outcome.json').read_bytes())},indent=2))
