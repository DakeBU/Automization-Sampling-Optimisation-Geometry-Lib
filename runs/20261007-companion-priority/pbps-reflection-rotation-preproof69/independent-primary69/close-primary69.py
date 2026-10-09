import datetime,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def pin(p):
 b=p.read_bytes();return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
assert not (out/'lease.final.json').exists() and not (out/'owned-manifest.json').exists()
r=json.loads((out/'foreground-close-validator.receipt.json').read_bytes());assert r['actual_exit']==0
run=json.loads((out/'review-run.json').read_bytes());v=run.pop('run_sha256');assert sha(canon(run))==v
regular=[pin(p) for p in sorted(out.iterdir()) if p.is_file()]
total=len(regular)+2
manifest=dict(schema='primary69-finite-owned-closure-manifest-v1',owner='/root/independent_primary69',owned_path=str(out),
 all_owned_bytes_including_inputs_scripts_outputs_terminals_and_negative_records=True,
 regular_file_count=len(regular),regular_file_entries=regular,
 closure_entries_canonical_sha256=sha(canon(regular)),total_owned_files_including_self_and_final_lease=total,
 self_boundary='This manifest excludes its own bytes and final lease to avoid self-reference; final lease binds this manifest; postclose external readback binds lease bytes.',postclose_writes_permitted=False)
(out/'owned-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8')
read=json.loads((out/'readback-report.json').read_bytes());val=json.loads((out/'close-validation.json').read_bytes())
finalizer=json.loads((out/'finalizer-process.json').read_bytes())
lease=dict(schema='primary69-CLOSED_LAST-owned-lease-v1',owner='/root/independent_primary69',owned_path=str(out),
 status='CLOSED_LAST',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 owned_file_count=total,regular_file_count=len(regular),manifest_RAW_sha256=sha((out/'owned-manifest.json').read_bytes()),
 finite_owned_closure_sha256=manifest['closure_entries_canonical_sha256'],
 whole_logical_run_sha256=v,whole_logical_hash_deletes_ONLY_top_level_run_sha256=True,
 COMPLETE_RAW_REVIEW=pin(out/'review-run.json'),COMPLETE_NAMED_SOURCE_EXPECTATIONS=pin(out/'primary-source-expectation-payload.json'),
 SEPARATE_COMPLETE_RAW_LF_INPUT=pin(out/'RAW-input-payload.json'),FINITE_SOURCE_COVERAGE=pin(out/'finite-coverage-manifest.json'),
 source_math_count=419,source_graph_nodes=22,source_graph_edges=read['source_graph_edges'],
 actual_finalizer_pid=finalizer['actual_pid'],actual_finalizer_exit=0,
 actual_readback_pid=read['actual_pid'],actual_readback_exit=0,actual_close_validator_pid=val['actual_pid'],actual_close_validator_exit=0,
 actual_lease_writer_pid=os.getpid(),lease_writer_exit_observation='External foreground shell tool observes actual EXIT after this final owned write',
 postclose_observation='External read-only postclose-readonly.py output; never saved inside closed folder',
 last_owned_write=True,postclose_writes_permitted=False,candidate69_seen=False,header69_seen=False,
 proof_or_mathematical_completion_claim=False,canonical_or_Git_or_ledger_edits=False)
(out/'lease.final.json').write_text(json.dumps(lease,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(lease,sort_keys=True))
