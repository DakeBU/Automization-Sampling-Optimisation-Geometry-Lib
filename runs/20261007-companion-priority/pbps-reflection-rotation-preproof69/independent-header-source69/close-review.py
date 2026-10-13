import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf),LF_sha256=sha(lf))
assert not (out/'lease.final.json').exists() and not (out/'owned-manifest.json').exists()
receipt=json.loads((out/'foreground-close-validator.receipt.json').read_bytes());assert receipt['actual_exit']==0
run=json.loads((out/'review-run.json').read_bytes());v=run.pop('run_sha256');assert sha(canon(run))==v
regular=[pin(p) for p in sorted(out.iterdir()) if p.is_file()];total=len(regular)+2
manifest=dict(schema='header-source69-finite-owned-closure-v1',owner='/root/independent_primary69',owned_path=str(out),
 regular_file_count=len(regular),regular_file_entries=regular,closure_entries_canonical_sha256=sha(canon(regular)),
 total_owned_files_including_manifest_and_final_lease=total,all_owned_inputs_outputs_scripts_and_terminals=True,
 self_boundary='Manifest excludes itself and final lease; lease binds manifest; external readback binds lease bytes.',postclose_writes_permitted=False)
(out/'owned-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8')
finalizer=json.loads((out/'finalizer-process.json').read_bytes());read=json.loads((out/'readback-report.json').read_bytes());val=json.loads((out/'close-validation.json').read_bytes())
lease=dict(schema='header-source69-CLOSED_LAST-lease-v1',owner='/root/independent_primary69',owned_path=str(out),status='CLOSED_LAST',
 closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_owned_write=True,postclose_writes_permitted=False,
 owned_file_count=total,regular_file_count=len(regular),manifest_RAW_sha256=sha((out/'owned-manifest.json').read_bytes()),
 finite_owned_closure_sha256=manifest['closure_entries_canonical_sha256'],whole_logical_run_sha256=v,
 whole_logical_hash_deletes_ONLY_top_level_run_sha256=True,
 COMPLETE_RAW_REVIEW=pin(out/'review-run.json'),COMPLETE_NAMED_REVIEW=pin(out/'RAW-review-payload.json'),
 COMPLETE_RAW_DECISION=pin(out/'header-source-decision.json'),SEPARATE_COMPLETE_RAW_LF_INPUT=pin(out/'RAW-input-payload.json'),
 FINITE_COVERAGE=pin(out/'finite-coverage-manifest.json'),
 verdict='ADMIT_HEADER_ONLY_FOR_STATEMENT_SEAL_CONSIDERATION',candidate_expanded_RAW_sha256='391ccc5bbf0978aa342269eb96c2dc4c9c23ae7865e6d9152959fc4df26f468b',
 actual_source_reviewer_pid=51488,actual_source_reviewer_exit=0,actual_finalizer_pid=finalizer['actual_pid'],actual_finalizer_exit=0,
 actual_readback_pid=read['actual_pid'],actual_readback_exit=0,actual_close_validator_pid=val['actual_pid'],actual_close_validator_exit=0,
 actual_lease_writer_pid=os.getpid(),lease_writer_exit_observation='Actual foreground exit observed externally after this last owned write',
 postclose_observation='postclose-readonly.py external stdout only, never saved inside closed folder',
 source_math_count=419,expanded_header_lines=107,expanded_header_segments=10,metadata_fields=read['metadata_fields'],
 source_header_only=True,no_proof_or_compilation=True,Statement_Seal=False,SAU_claim=False,
 prior_CLOSED82_native_bytes_unchanged=True,no_68_reviews_decoders_or_bodies=True,no_canonical_Git_or_ledger_edits=True)
(out/'lease.final.json').write_text(json.dumps(lease,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(lease,sort_keys=True))
