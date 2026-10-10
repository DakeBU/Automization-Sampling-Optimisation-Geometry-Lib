import hashlib
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def main():
    before = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for p in OWN.rglob('*') if p.is_file()}
    closed = json.loads((OWN / 'CLOSED_LAST.json').read_text(encoding='utf-8'))
    assert closed['status'] == 'CLOSED_LAST' and closed['actual_EXIT'] == 0
    files = {p.relative_to(ROOT).as_posix() for p in before}
    prior = {x['path'] for x in closed['complete_owned_prior_manifest']}
    assert files == prior | {(OWN / 'CLOSED_LAST.json').relative_to(ROOT).as_posix()}
    for item in closed['complete_owned_prior_manifest']:
        raw = (ROOT / item['path']).read_bytes()
        assert len(raw) == item['RAW_bytes']
        assert sha(raw) == item['RAW_sha256']
        assert sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == item['LF_sha256']
    run = json.loads((OWN / 'source.0.run.json').read_text(encoding='utf-8'))
    run_hash = run.pop('review_run_sha256')
    assert sha(canonical(run)) == run_hash == closed['review_run_sha256']
    whole = json.loads((OWN / 'whole-logical-payload75.json').read_text(encoding='utf-8'))
    whole_hash = whole.pop('whole_logical_payload_sha256')
    assert sha(canonical(whole)) == whole_hash == closed['whole_logical_payload_sha256']
    assert len(whole['complete_named_RAW_payloads']) == 5
    for item in whole['complete_named_RAW_payloads']:
        raw = (ROOT / item['path']).read_bytes()
        assert raw == item['RAW_utf8'].encode('utf-8')
        assert sha(raw) == item['RAW_sha256'] and len(raw) == item['RAW_bytes']
    review = json.loads((OWN / 'source.0.review.json').read_text(encoding='utf-8'))
    admission = json.loads((OWN / 'source.0.admission-fields.json').read_text(encoding='utf-8'))
    assert review['verdict'] == 'equivalent-after-elaboration'
    assert review['review_run_sha256'] == run_hash == admission['audit_fields']['source_review']['review_run_sha256']
    assert len(review['semantic_slots']) == 7 and not review['deltas'] and not review['repairs']
    assert admission['publication_binding_sha256'] == run['clean_official_packet_full']['publication_binding_sha256']
    assert run['mechanical_verification_full']['terminal']['actual_EXIT'] == 0
    after = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for p in OWN.rglob('*') if p.is_file()}
    assert before == after, 'readonly verifier observed a postclose mutation'
    print(json.dumps({'status': 'PASS_READONLY_POSTCLOSE', 'actual_verifier_PID': os.getpid(), 'actual_verifier_EXIT': 0,
                      'closed_writer_PID': closed['actual_PID'], 'closed_writer_EXIT': closed['actual_EXIT'],
                      'complete_owned_prior_file_count': len(prior), 'all_owned_files_RAW_LF_verified': True,
                      'five_complete_RAW_payloads_verified': True, 'native_complete_run_hash_verified': True,
                      'review_run_sha256': run_hash, 'whole_logical_payload_sha256': whole_hash,
                      'CLOSED_LAST_RAW_sha256': sha((OWN / 'CLOSED_LAST.json').read_bytes()),
                      'no_writes_or_mtime_changes': True}, indent=2))


if __name__ == '__main__':
    main()
