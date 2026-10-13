from pathlib import Path
import hashlib, json, os

out=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
marker=out/'CLOSED_LAST.json'
before=marker.read_bytes(); seal=json.loads(before)
assert seal['state']=='CLOSED_LAST'
expected={x['path'] for x in seal['files']}
actual={p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()}
assert actual==expected|{'CLOSED_LAST.json'}
assert len(expected)==seal['file_count_before_marker']
for item in seal['files']:
    raw=(out/item['path']).read_bytes(); lf=raw.replace(b'\r\n',b'\n')
    assert len(raw)==item['RAW_bytes'] and sha(raw)==item['RAW_sha256']
    assert len(lf)==item['CRLF_to_LF_only_bytes'] and sha(lf)==item['CRLF_to_LF_only_sha256']
    assert raw.count(b'\r\n')==item['CRLF_count']
assert sha((out/seal['native_report_file']).read_bytes())==seal['native_report_RAW_sha256']
logical=(out/seal['logical_run_file']).read_bytes()
assert logical==(out/seal['named_RAW_payload']).read_bytes()
assert sha(logical)==seal['review_run_sha256']
assert sha((out/seal['source_only_freeze_file']).read_bytes())==seal['source_only_freeze_RAW_sha256']
for name,evidence in seal['actual_foreground_writer_receipts'].items():
    receipt=json.loads((out/evidence['receipt']).read_text(encoding='utf-8'))
    assert receipt.get('actual_foreground_PID',receipt.get('writer_pid'))==evidence['PID']
    assert receipt['exit_code']==evidence['EXIT']
    for stream in ['stdout','stderr']:
        assert sha((out/receipt[stream+'_file']).read_bytes())==receipt[stream+'_sha256']
report=json.loads((out/seal['native_report_file']).read_text(encoding='utf-8'))
assert report['state']==report['audit_fields']['state']==report['source_review']['state']=='accepted'
assert report['packet_sha256']==seal['packet_sha256']
assert report['publication_binding_sha256']==seal['publication_binding_sha256']
assert marker.read_bytes()==before
print(json.dumps({'status':'PASS_EXTERNAL_READ_ONLY_CLOSED_LAST_VALIDATION','validator_PID':os.getpid(),'marker_RAW_sha256':sha(before),'manifest_files':len(expected),'total_files_including_marker':len(actual),'every_RAW_and_CRLF_to_LF_only_hash':'MATCH','exact_file_membership':'MATCH','source_first_freeze_unchanged':True,'logical_named_RAW_identical':True,'packet_sha256':seal['packet_sha256'],'publication_binding_sha256':seal['publication_binding_sha256'],'review_run_sha256':seal['review_run_sha256'],'native_report_RAW_sha256':seal['native_report_RAW_sha256'],'filesystem_writes_performed':False},indent=2))
