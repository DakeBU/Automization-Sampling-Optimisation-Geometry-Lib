import hashlib
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent
GEN1 = OWN.parent / 'independent-clean-source75'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def main():
    before = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for base in [OWN, GEN1] for p in base.rglob('*') if p.is_file()}
    closed = json.loads((OWN / 'CLOSED_LAST.json').read_text(encoding='utf-8'))
    assert closed['status'] == 'CLOSED_LAST' and closed['actual_EXIT'] == 0
    actual_files = {p.relative_to(ROOT).as_posix() for p in OWN.rglob('*') if p.is_file()}
    expected_files = {x['path'] for x in closed['complete_owned_prior_manifest']} | {(OWN / 'CLOSED_LAST.json').relative_to(ROOT).as_posix()}
    assert actual_files == expected_files
    for item in closed['complete_owned_prior_manifest']:
        raw = (ROOT / item['path']).read_bytes()
        assert len(raw) == item['RAW_bytes'] and sha(raw) == item['RAW_sha256']
        assert sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == item['LF_sha256']
    gen1_raw = (GEN1 / 'CLOSED_LAST.json').read_bytes()
    assert sha(gen1_raw) == closed['generation1_CLOSED_RAW_sha256'] == '2de491f96fcce996feb3a98cb4b5da2d1753c6a457188e7c715b314768bf4dd6'
    gen1 = json.loads(gen1_raw)
    for item in gen1['complete_owned_prior_manifest']:
        raw = (ROOT / item['path']).read_bytes()
        assert len(raw) == item['RAW_bytes'] and sha(raw) == item['RAW_sha256']
        assert sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == item['LF_sha256']
    run = json.loads((OWN / 'overlay.0.run.json').read_text(encoding='utf-8'))
    run_hash = run.pop('administrative_run_sha256')
    assert sha(canonical(run)) == run_hash == closed['administrative_run_sha256']
    whole = json.loads((OWN / 'whole-logical-payload75.json').read_text(encoding='utf-8'))
    whole_hash = whole.pop('whole_logical_payload_sha256')
    assert sha(canonical(whole)) == whole_hash == closed['whole_logical_payload_sha256']
    assert len(whole['complete_named_RAW_payloads']) == 10
    for item in whole['complete_named_RAW_payloads']:
        raw = (ROOT / item['path']).read_bytes()
        assert raw == item['RAW_utf8'].encode('utf-8') and sha(raw) == item['RAW_sha256']
    admission = json.loads((OWN / 'admission-overlay75.json').read_text(encoding='utf-8'))
    assert admission['audit_fields']['state'] == 'accepted'
    assert admission['audit_fields']['source_review']['review_run_sha256'] == gen1['review_run_sha256']
    for key in ['cell_source_proof_coverage', 'publication_source_proof_coverage']:
        value = admission[key]
        assert value['coverage_report']['internal_bridges_OPEN'] == 0
        assert value['coverage_report']['internal_bridges_REVIEWED_FOR_ONE_CLOCK_CONSUMER'] == 13
        assert value['coverage_report']['remaining_open_source_nodes'] == ['N25', 'N26', 'N27', 'N28', 'N29']
        assert len(value['coverage_report']['reviewed_node_statuses']) == 32
    after = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for base in [OWN, GEN1] for p in base.rglob('*') if p.is_file()}
    assert before == after
    print(json.dumps({'status': 'PASS_READONLY_POSTCLOSE', 'actual_verifier_PID': os.getpid(), 'actual_verifier_EXIT': 0,
                      'closed_writer_PID': closed['actual_PID'], 'closed_writer_EXIT': closed['actual_EXIT'],
                      'generation1_fully_unchanged': True, 'all_new_owned_RAW_LF_pins_verified': True,
                      'complete_original_five_RAW_and_new_four_RAW_plus_original_CLOSED_verified': True,
                      'source_review_run_sha256': gen1['review_run_sha256'],
                      'administrative_run_sha256': run_hash, 'whole_logical_payload_sha256': whole_hash,
                      'CLOSED_LAST_RAW_sha256': sha((OWN / 'CLOSED_LAST.json').read_bytes()),
                      'no_writes_or_mtime_changes': True}, indent=2))


if __name__ == '__main__':
    main()
