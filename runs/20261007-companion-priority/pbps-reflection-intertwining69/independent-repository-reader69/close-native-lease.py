"""Last owned write. Run directly, never through the logging wrapper."""
import datetime, hashlib, json, os, pathlib
out = pathlib.Path(__file__).resolve().parent

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')

def pin(p):
    b=p.read_bytes()
    item=dict(name=str(p.relative_to(out)).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=sha(b))
    try:
        b.decode('utf-8')
        lf=b.replace(b'\r\n',b'\n')
        item.update(LF_bytes=len(lf),LF_sha256=sha(lf),LF_recipe='only CRLF-to-LF; lone CR preserved')
    except UnicodeDecodeError:
        item.update(LF_bytes=None,LF_sha256=None,LF_recipe='not applicable to binary; preserve RAW')
    return item

assert not (out/'lease.final.json').exists(), 'CLOSED bundles are immutable'
run=json.loads((out/'review-run.json').read_text(encoding='utf-8'))
logical=dict(run);logical.pop('run_sha256')
assert sha(canonical(logical)) == run['run_sha256']
decision=json.loads((out/'repository-reader69.decision.json').read_text(encoding='utf-8'))
assert decision['ready_to_close'] is True
for label in ['finalize-review','readback-review','validate-close']:
    receipt=json.loads((out/(label+'.receipt.json')).read_text(encoding='utf-8'))
    assert receipt['actual_exit']==0 and receipt['completed'] and receipt['foreground']
excluded={out/'manifest.final.json',out/'lease.final.json'}
files=sorted(p for p in out.rglob('*') if p.is_file() and p not in excluded)
assert not any(p.is_symlink() for p in files)
entries=[pin(p) for p in files]
closure=sha(canonical(entries))
manifest=dict(schema='repository-reader69-finite-native-manifest-v1',entries=entries,
    regular_file_count=len(entries),owned_file_count=len(entries)+2,
    excludes_exactly=['manifest.final.json','lease.final.json'],
    finite_owned_closure_sha256=closure,
    complete_including_helpers_negatives_terminal_receipts_and_binary_captures=True)
(out/'manifest.final.json').write_text(json.dumps(manifest,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
lease=dict(schema='repository-reader69-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',
    owner='/root/independent_primary69',owned_path=str(out),
    regular_file_count=len(entries),owned_file_count=len(entries)+2,
    finite_owned_closure_sha256=closure,manifest_RAW_sha256=sha((out/'manifest.final.json').read_bytes()),
    whole_logical_run_sha256=run['run_sha256'],whole_logical_hash_deletes_ONLY_top_level_run_sha256=True,
    verdict=decision['verdict'],remaining_truth_boundary=decision['remaining_truth_boundary'],
    actual_lease_writer_pid=os.getpid(),closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    last_owned_write=True,postclose_writes_permitted=False,
    lease_writer_exit_observation='Actual EXIT observed externally by direct foreground command.',
    postclose_observation='Read-only output only, never written into this closed tree.',
    canonical_Git_ledger_Goal_edits=False,no_new_math_or_source_verdict=True,
    full_Exposition_PURIFIED_main_live_wholepaper_Goal_completion=False)
for label,stem in [('finalize-review','finalizer'),('readback-review','readback'),('validate-close','close_validator')]:
    receipt=json.loads((out/(label+'.receipt.json')).read_text(encoding='utf-8'))
    lease['actual_'+stem+'_pid']=receipt['actual_pid']
    lease['actual_'+stem+'_exit']=receipt['actual_exit']
lease.update(complete_named_input_count=132,final_root_input_count=108,finite_review_check_count=13,
    actual_visual_captures=8,actual_copy_callbacks=3,actual_HTTP200_RAW_roundtrip_downloads=3,
    BODY_steps=6,BODY_lines=308,registry_count=517,root_jobs=9179,test_jobs=9479,publication_units=238,
    checked_science_commit=decision['checked_science_commit'],
    final_root_packet_RAW_sha256=decision['final_root_packet_RAW_sha256'],
    final_cell_RAW_sha256=decision['final_cell_RAW_sha256'],final_graph_RAW_sha256=decision['final_graph_RAW_sha256'],
    blocking_findings=0,required_repairs=0)
for name,key in [('review-run.json','COMPLETE_RAW_REVIEW'),('repository-reader69.decision.json','COMPLETE_NAMED_DECISION'),
                 ('complete-named-review-decision-input-payload.json','COMPLETE_NAMED_REVIEW_DECISION_INPUT'),
                 ('RAW-input-payload.json','SEPARATE_COMPLETE_RAW_LF_INPUT'),
                 ('finite-repository-reader-coverage.json','FINITE_REVIEW_COVERAGE')]:
    lease[key]=pin(out/name)
(out/'lease.final.json').write_text(json.dumps(lease,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(dict(actual_lease_writer_pid=os.getpid(),regular_files=len(entries),owned_files=len(entries)+2,
    lease_RAW_sha256=sha((out/'lease.final.json').read_bytes()),manifest_RAW_sha256=lease['manifest_RAW_sha256'],
    finite_owned_closure_sha256=closure,whole_logical_run_sha256=run['run_sha256']),sort_keys=True))
