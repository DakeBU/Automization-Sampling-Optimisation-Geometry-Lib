import os, subprocess
import review76 as r

lp=r.O/'lease.final.json';before=lp.read_bytes();lease=r.json.loads(before)
assert lease['status']=='CLOSED_LAST' and lease['actor']==r.ACTOR and lease['final_owned_write'] and lease['postclose_owned_writes_forbidden']
rows=lease['files'];assert len(rows)+1==lease['file_count_including_lease'] and r.sha(r.can(rows))==lease['closure_logical_sha256']
assert {path.resolve() for path in r.O.rglob('*') if path.is_file()}=={r.resolve(item['path']).resolve() for item in rows}|{lp.resolve()}
for item in rows:r.check(item);assert r.resolve(item['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
assert not any(path.is_file() for path in r.CACHE.rglob('*'))
run=r.load(r.O/'run.json');assert r.sha(r.can({key:value for key,value in run.items() if key!='run_sha256'}))==run['run_sha256']==lease['run_sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r.ROOT,text=True).strip()==run['checked_science_commit']==r.SCI
for key in ['decision','inputs_manifest','complete_named_RAW_payload','checks','named_review','owned_script','actual_execution_checker','actual_final_writer_script','independent_PNG_observations']:r.check(run[key])
decision=r.load(run['decision']['path']);im=r.load(run['inputs_manifest']['path']);payload=r.load(run['complete_named_RAW_payload']['path']);checks=r.load(run['checks']['path'])
assert im['inputs']==r.load(r.DIS)['inputs'] and im['input_count']==len(im['inputs'])==149
r.check(im['dispatch']);assert r.sha(r.DIS.read_bytes())==run['dispatch_RAW_sha256']=='54b29a35f4d68136e744724e6fafd567f33a54a56b33d13faf6f4ba6d7b9403d'
for item in im['inputs']:r.check(item)
assert payload['decision']==decision and payload['inputs']==im and payload['checks']==checks
assert payload['named_review_UTF8']==r.resolve(run['named_review']['path']).read_text(encoding='utf-8')
assert payload['full_exact_module_UTF8'].encode()==(r.ROOT/r.MOD).read_bytes()
for terminal in payload['full_own_foreground_terminal_RAW_payloads']:
    r.check(terminal['receipt_pin']);receipt=terminal['receipt']
    assert r.load(terminal['receipt_pin']['path'])==receipt
    assert terminal['stdout_exact_UTF8'].encode()==r.check(receipt['stdout']) and terminal['stderr_exact_UTF8'].encode()==r.check(receipt['stderr'])
assert decision['accepted_scoped_aggregate'] and decision['independent_of_formalizer_stabilizer'] and decision['blockers']==[]
assert decision['Registry']==525 and decision['publication_units']==246 and decision['copy_callbacks']==decision['RAW_downloads']==3
assert decision['formula_BODY_steps']==10 and decision['independently_viewed_PNGs']==13 and decision['current_gate_receipts']==18
for key in ['new_VERIFIED_transition','new_independent_mathematics_certification','new_source_fidelity_certification','self_validation_of_old_source_verdict','Goal_complete','PURIFIED','full_Exposition_Seal','main','live','whole_paper']:assert decision[key] is False
qualification=checks['result']['communication_qualification'];assert qualification['new_source_or_math_verdict'] is False and qualification['new_VERIFIED'] is False and qualification['self_validation_of_old_source_verdict'] is False
assert qualification['whole_logical_run_sha256']=='f0bcdae9864810e4271fcc74533099f78bfe86208d15017f21d38719f486c75a'
assert r.sha((r.SOURCE_REVIEW/'CLOSED_LAST.json').read_bytes())==r.SOURCE_LEASE_SHA
assert lp.read_bytes()==before
print(r.json.dumps(dict(status='PASS_EXTERNAL_READ_ONLY_SCOPED_READER76_CLOSURE',actor=r.ACTOR,actual_external_readonly_PID=os.getpid(),writer_PID=lease['writer_PID'],owned_files=lease['file_count_including_lease'],owned_runtime_files=0,current_inputs=149,every_owned_RAW_LF_pin_and_membership='MATCH',run_sha256=run['run_sha256'],run_RAW_sha256=r.sha((r.O/'run.json').read_bytes()),lease_RAW_sha256=r.sha(before),complete_named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'],closure_logical_sha256=lease['closure_logical_sha256'],communication_qualification_bound=True,source121_unchanged=True,no_owned_writes=True,new_VERIFIED_transition=False,blockers=[]),ensure_ascii=False,indent=2))
