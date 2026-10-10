from pathlib import Path
import datetime, hashlib, json, os

out=Path(__file__).resolve().parent
marker=out/'CLOSED_LAST.json'
assert not marker.exists()
def sha(b): return hashlib.sha256(b).hexdigest()
def get(n): return json.loads((out/n).read_text(encoding='utf-8'))
report=get('compiled-source-review76.json')
integrity=get('compiled-review-integrity76.json')
validator=get('validate_compiled_review76.foreground-exit.json')
assert integrity['status']=='PASS_NATIVE_COMPILED_SOURCE_REVIEW_INTEGRITY'
assert validator['writer_pid']==integrity['validator_PID']==23260 and validator['exit_code']==0
assert report['state']==report['audit_fields']['state']==report['source_review']['state']=='accepted'
assert sha((out/'compiled-source-review76.json').read_bytes())==integrity['report_RAW_sha256']
assert sha((out/'review-logical-run76.json').read_bytes())==integrity['review_run_sha256']
assert (out/'review-logical-run76.json').read_bytes()==(out/'review-logical-run76.raw.json').read_bytes()
manifest=[]
for path in sorted(out.rglob('*')):
    if path.is_file():
        assert not path.is_symlink()
        raw=path.read_bytes(); lf=raw.replace(b'\r\n',b'\n')
        manifest.append({'path':path.relative_to(out).as_posix(),'RAW_bytes':len(raw),'RAW_sha256':sha(raw),'CRLF_to_LF_only_bytes':len(lf),'CRLF_to_LF_only_sha256':sha(lf),'CRLF_count':raw.count(b'\r\n')})
assert 'CLOSED_LAST.json' not in {x['path'] for x in manifest}
sealed={'schema_version':1,'state':'CLOSED_LAST','reviewer':'/root/fresh_source76','closure_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'closing_writer_PID':os.getpid(),'closing_writer_exit_policy':'No self-asserted exit. The external foreground caller captures this process stdout/stderr and obtains the actual Popen.wait exit without writing into this directory.','immutable_policy':'Exclusive-create once; never overwrite. After this marker is written this reviewer performs zero writes to this directory, including logs, receipts and metadata. External validation is read-only.','manifest_scope':'Every existing file recursively in this owned directory, excluding only this self-referential CLOSED_LAST.json marker. The external read-only validator checks exact membership and all RAW/LF hashes.','file_count_before_marker':len(manifest),'files':manifest,'source_only_freeze_file':'source-only.freeze76.json','source_only_freeze_RAW_sha256':integrity['source_first_freeze_sha256'],'packet_sha256':report['packet_sha256'],'publication_binding_sha256':report['publication_binding_sha256'],'native_report_file':'compiled-source-review76.json','native_report_RAW_sha256':sha((out/'compiled-source-review76.json').read_bytes()),'logical_run_file':'review-logical-run76.json','named_RAW_payload':'review-logical-run76.raw.json','review_run_sha256':report['review_run_sha256'],'logical_RAW_payload_identical':True,'independent_source_topology':'compiled-source-topology76.json','source_coverage':'compiled-source-coverage76.json','canonical_projections':['canonical-cell-source-proof-coverage76.json','canonical-publication-source-proof-coverage76.json'],'full_native_evidence_preserved':True,'actual_foreground_writer_receipts':{'source_first_freeze':{'PID':31828,'EXIT':0,'receipt':'write_source_freeze76.foreground-exit.json'},'substantive_compiled_review':{'PID':46836,'EXIT':0,'receipt':'write_compiled_review76.foreground-exit.json'},'explicit_native_state_export':{'PID':3964,'EXIT':0,'receipt':'finalize_compiled_review76.foreground-exit.json'},'artifact_integrity_validator':{'PID':23260,'EXIT':0,'receipt':'validate_compiled_review76.foreground-exit.json'},'fresh_exact_Lean_and_axioms':{'PID':40920,'EXIT':0,'receipt':'direct-review76.foreground-exit.json'}},'preserved_nonzero_exits':integrity['preserved_nonzero_exits'],'accepted_state':report['state'],'semantic_verdict':report['verdict'],'accepted_scope':report['source_review']['scope'],'open_truth_boundary':report['source_review']['open_truth_boundary'],'no_canonical_or_ledger_writes':True,'no_PROVED_LOCAL_VERIFIED_Goal_or_whole_paper_credit':True}
data=(json.dumps(sealed,ensure_ascii=False,indent=2)+'\n').encode()
with marker.open('xb') as stream:
    stream.write(data)
    stream.flush()
    os.fsync(stream.fileno())
# This stdout is external native evidence. No filesystem operation after this point mutates the directory.
print(json.dumps({'status':'CLOSED_LAST_WRITTEN_ONCE','closing_writer_PID':os.getpid(),'marker_RAW_sha256':sha(data),'manifest_files':len(manifest),'native_report_RAW_sha256':sealed['native_report_RAW_sha256'],'review_run_sha256':sealed['review_run_sha256'],'packet_sha256':sealed['packet_sha256'],'publication_binding_sha256':sealed['publication_binding_sha256'],'zero_directory_writes_after_marker':True},indent=2))
