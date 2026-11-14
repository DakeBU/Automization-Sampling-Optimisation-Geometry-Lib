from pathlib import Path
import datetime,hashlib,json,sys
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=ROOT/'.astis/semantic-neutral-20261110/src_a83e10'
RUN=BASE/'sourcev_execution_20261110';PUB=RUN/'public';PRIVATE=RUN/'private'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def digest(v):return hashlib.sha256(canon(v)).hexdigest()
def load(p):return json.loads(p.read_text())
def write(n,v):(PUB/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumSignalStrength'
front=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-signal-strength.json'
ledger=ROOT/'runs/substantive_advances.jsonl'
before=(PRIVATE/'ledger.before.raw.jsonl').read_bytes()
append=(PUB/'exact-one-appended-ledger-event.raw.jsonl').read_bytes()
assert ledger.read_bytes()==before+append
assert len(append.splitlines())==1
event=json.loads(append);evidence=load(PUB/'original-evidence.raw.json')
assert event['advance_id']==ADV and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert event['worker_id']=='/root/source_reader_a83e10' and event['evidence']==evidence
assert canon(evidence)==(PUB/'original-evidence.canonical.json').read_bytes()
contract=load(PUB/'all-original-keys-retention-contract.json')
assert contract['complete_original_evidence']==evidence and contract['original_keys']==list(evidence)
assert all(digest(evidence[k])==v for k,v in contract['original_value_canonical_hashes'].items())
assert 'post_integration' not in evidence
receipt=load(PUB/'normal-api-receipt.json');assert receipt['actual_API_calls']==1 and receipt['success']
assert front.read_bytes()==(PUB/'own-frontier.after.raw.json').read_bytes()
diff=load(PUB/'frontier-closeout.exact-two-field-diff.json')
assert [d['path'] for d in diff]==['/status','/evidence/independent_verification']
assert load(front)['status']=='independently_verified'
preserved=load(PUB/'preservation-and-scope.json')
assert preserved['foreign_SAU_states_unchanged'] and preserved['foreign_frontier_and_tracked_inventory_bytes_unchanged']
assert preserved['original_evidence_all_keys_and_nested_values_equal_appended']
assert load(PRIVATE/'protected.before.json')==load(PRIVATE/'protected.after.json')
foreignbefore=load(PRIVATE/'states.before.json');foreignafter=load(PRIVATE/'states.after-api.json')
assert {k:v for k,v in foreignbefore.items() if k!=ADV}=={k:v for k,v in foreignafter.items() if k!=ADV}
for filename,expected in [('phase1.freeze.json','f4b7e781a584005ade0a21cb0d1df46b1d154b9b94df33d2f83bced7ffe9f822'),
 ('phase2.freeze.json','951a69f26cb0f2e4f58a644a7e57f081c593d8b62da6093c0a88dfbc7e30e9e9'),
 ('phase3.freeze.json','70eb35cfe123ea3a4a7b6da8f5797824295461d634b116ca1a82e7e549a59c28')]:
    assert sha(BASE/filename)==expected
    assert all(sha(BASE/x['path'])==x['sha256'] for x in load(BASE/filename)['files'])
overlay=BASE/'locator_precision_overlay/freeze.json'
assert sha(overlay)=='78990a241f6a7e1f9f75b519304c77b8da59d43671720a1cdf1b9d3c23003267'
assert all(sha(overlay.parent/x['path'])==x['sha256'] for x in load(overlay)['files'])
privatefiles=[{'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(PRIVATE.iterdir()) if p.is_file()]
summary={
 'advance_id':ADV,'verifier':'/root/source_reader_a83e10','state':'VERIFIED',
 'normal_API':'tools.astis_advance.transition_advance','actual_API_calls':1,
 'normal_API_appended_events':1,'pre_call_ledger_is_exact_byte_prefix':True,
 'source_native_mathematical_checked_commit':'df64aaa6088b6ac88c35696acfed906031964d72',
 'accepted_evidence_carrier_commit':'cb761181b45a73fe884d9c7590a8710105a108e1',
 'fresh_gate_native_at_carrier_claim':False,
 'original_evidence':{'raw_file':'original-evidence.raw.json','raw_sha256':sha(PUB/'original-evidence.raw.json'),
   'canonical_file':'original-evidence.canonical.json','canonical_sha256':digest(evidence),
   'all_original_keys':list(evidence),'observed_key_count_not_a_fixed_contract':len(evidence),
   'complete_original_object_and_each_nested_value_in_contract':'all-original-keys-retention-contract.json',
   'retention_contract_sha256':sha(PUB/'all-original-keys-retention-contract.json'),
   'future_rule':'Preserve every original key and recursively every original value exactly. Only the original verifier may later add post_integration; no compact replacement or original-value overwrite.',
   'post_integration_added':False},
 'exact_appended_event':{'raw_file':'exact-one-appended-ledger-event.raw.jsonl','raw_sha256':sha(PUB/'exact-one-appended-ledger-event.raw.jsonl'),
   'canonical_file':'exact-one-appended-ledger-event.canonical.json','canonical_sha256':digest(event),
   'evidence_canonically_identical_to_original':True},
 'frontier_closeout':{'normal_API_auto_changed_frontier':False,'separately_executed_after_API_success':True,
   'from_status':'proved_locally','to_status':'independently_verified',
   'only_fields':['/status','/evidence/independent_verification'],
   'owner_preserved':'huanjian_gc_20261110_fixed_spectrum_signal_strength',
   'old_raw_sha256':sha(PUB/'own-frontier.before.raw.json'),'new_raw_sha256':sha(PUB/'own-frontier.after.raw.json'),
   'exact_field_diff_sha256':sha(PUB/'frontier-closeout.exact-two-field-diff.json'),
   'all_other_fields_values_and_unrelated_text_bytes_preserved':True},
 'preservation':{'foreign_SAU_states_unchanged':True,'foreign_frontier_bytes_unchanged':True,
   'protected_file_count':preserved['protected_file_count'],
   'actual_nonempty_family_counts':preserved['actual_nonempty_family_counts'],
   'runs_substantive_discoveries_unchanged':True,
   'private_foreign_raw_snapshots_and_path_inventories_included_in_public':False,
   'private_bundle_commitment':digest(privatefiles)},
 'prior_reviews_proposals_unchanged':True,
 'scope':'LOCAL selected actual-Gaussian norm/SNR plus PRIVATE diagonal-law zero-event verification only. No full tau/shifted/rotated detector/Ex26, algorithm/oracle/TV/cost/main bounds, STAB/global/Registry/import/site/browser/publication/purification/wholeGoal or post_integration release.',
 'new_runs':'One normal VERIFIED API with its built-in publication admission; no extra native/static/global/site/browser acceptance rerun.',
 'public_outputs':'Only own execution/evidence/frontier artifacts; foreign raw snapshots remain private.'}
write('execution-summary.json',summary)
payloads=[p for p in sorted(PUB.iterdir()) if p.is_file() and p.name not in ['payload-manifest.json','execution.freeze.json','execution.freeze.sha256','output-file-manifest.json']]
write('payload-manifest.json',{'scope':'Exact public-safe payload files; separate seal/outer manifest are listed in output-file-manifest.json.',
 'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in payloads]})
freeze={'schema':1,'kind':'one-normal-local-sourceV-plus-separate-own-frontier-closeout',
 'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'advance_id':ADV,'verifier':'/root/source_reader_a83e10','actual_API_calls':1,
 'payload_manifest_sha256':sha(PUB/'payload-manifest.json'),
 'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in payloads]+[{'path':'payload-manifest.json','bytes':(PUB/'payload-manifest.json').stat().st_size,'sha256':sha(PUB/'payload-manifest.json')}],
 'original_evidence_raw_sha256':summary['original_evidence']['raw_sha256'],
 'original_evidence_canonical_sha256':summary['original_evidence']['canonical_sha256'],
 'appended_event_raw_sha256':summary['exact_appended_event']['raw_sha256'],
 'appended_event_canonical_sha256':summary['exact_appended_event']['canonical_sha256'],
 'all_original_keys_and_nested_values_retention_contract_sha256':summary['original_evidence']['retention_contract_sha256'],
 'foreign_private_preservation_bundle_commitment':digest(privatefiles),
 'public_contains_foreign_raw_snapshots':False,'separate_frontier_field_change_count':2,
 'post_integration_release':False,'scope':summary['scope']}
write('execution.freeze.json',freeze)
freezehash=sha(PUB/'execution.freeze.json')
(PUB/'execution.freeze.sha256').write_text(freezehash+'  execution.freeze.json\n')
files=[p for p in sorted(PUB.iterdir()) if p.is_file() and p.name!='output-file-manifest.json']
write('output-file-manifest.json',{'scope':'These and only these public files are selected for exact byte carry; this outer manifest is separately hash-pinned by the return receipt. No private file is selected.',
 'execution_freeze_sha256':freezehash,'files':[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]})
for p in PUB.iterdir():
    if p.is_file():p.chmod(0o444)
for p in PRIVATE.iterdir():
    if p.is_file():p.chmod(0o400)
print(json.dumps({'public_directory':str(PUB),'output_manifest':str(PUB/'output-file-manifest.json'),
 'output_manifest_sha256':sha(PUB/'output-file-manifest.json'),
 'execution_freeze':str(PUB/'execution.freeze.json'),'execution_freeze_sha256':freezehash,
 'original_evidence_raw_sha256':freeze['original_evidence_raw_sha256'],
 'original_evidence_canonical_sha256':freeze['original_evidence_canonical_sha256'],
 'appended_event_raw_sha256':freeze['appended_event_raw_sha256'],
 'appended_event_canonical_sha256':freeze['appended_event_canonical_sha256'],
 'actual_API_calls':1,'frontier_closeout_fields':2,
 'all_original_keys':list(evidence),'public_payload_files_including_seals_excluding_outer_manifest':len(files)},indent=2))
