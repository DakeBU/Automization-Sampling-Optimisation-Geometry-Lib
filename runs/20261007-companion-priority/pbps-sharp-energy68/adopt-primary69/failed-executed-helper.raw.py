from pathlib import Path
import base64, hashlib, json, os
root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-reflection-rotation-preproof69'
d = r / 'independent-primary69'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def check(b, row):
    assert len(b) == row['RAW_bytes'] and sha(b) == row['RAW_sha256']
    lf = b.replace(b'\r\n', b'\n')
    assert sha(lf) == row['LF_sha256']
    if 'LF_bytes' in row:
        assert len(lf) == row['LF_bytes']
def pin(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))
lease = load(d / 'lease.final.json')
assert sha((d / 'lease.final.json').read_bytes()) == '2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93'
assert lease['status'] == 'CLOSED_LAST' and lease['last_owned_write'] and lease['owned_file_count'] == 82
assert all(lease[key] == 0 for key in ['actual_close_validator_exit', 'actual_finalizer_exit', 'actual_readback_exit'])
assert [lease[key] for key in ['actual_close_validator_pid', 'actual_finalizer_pid', 'actual_readback_pid', 'actual_lease_writer_pid']] == [25888, 51388, 17948, 26420]
manifest = load(d / 'owned-manifest.json')
assert sha((d / 'owned-manifest.json').read_bytes()) == lease['manifest_RAW_sha256'] == '1c2cb829368b83a04d59aad24859c5c724c381236347d6ae3b07a353173a68e9'
rows = manifest['regular_file_entries']
assert len(rows) == 80 and sha(can(rows)) == manifest['closure_entries_canonical_sha256'] == lease['finite_owned_closure_sha256']
files = {p.relative_to(d).as_posix(): p for p in d.rglob('*') if p.is_file()}
assert len(files) == 82 and set(files) == {row['name'] for row in rows} | {'owned-manifest.json', 'lease.final.json'}
for row in rows:
    check(files[row['name']].read_bytes(), row)
assert (d / 'lease.final.json').stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in files.values())
run = load(d / 'review-run.json')
assert sha(can({k:v for k,v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['whole_logical_run_sha256'] == 'd38706cf97501b4b372a40efd120dfc34f87939718531b7ea224dbbdd345d6b7'
for key in ['COMPLETE_NAMED_SOURCE_EXPECTATIONS', 'COMPLETE_RAW_REVIEW', 'FINITE_SOURCE_COVERAGE', 'SEPARATE_COMPLETE_RAW_LF_INPUT']:
    check((d / lease[key]['name']).read_bytes(), lease[key])
for name, field in [('RAW-input-payload.json', 'inputs'), ('primary-source-expectation-payload.json', 'complete_outputs')]:
    payload = load(d / name)
    assert len(payload[field]) == 13
    for row in payload[field]:
        b = base64.b64decode(row['complete_RAW_bytes_base64'])
        check(b, row)
        assert base64.b64decode(row['complete_LF_bytes_base64']) == b.replace(b'\r\n', b'\n')
        assert (d / row['name']).read_bytes() == b
        original = Path(row['source_path'].replace('\\', '/'))
        assert original.read_bytes() == b
coverage = load(d / 'finite-coverage-manifest.json')
assert coverage['count'] == 419 and len(coverage['entries']) == 419
assert coverage['missing'] == coverage['unclassified'] == 0
assert coverage['prior_six_region_count'] == 344 and coverage['new_B4_consumer_region_count'] == 75
assert sha(can(coverage['entries'])) == coverage['entries_canonical_sha256']
primary = (d / 'whole-primary.exact-RAW.html').read_bytes()
assert len(primary) == 1482128 and sha(primary) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert len({row['id'] for row in coverage['entries']}) == 419
for row in coverage['entries']:
    lo, hi = row['source_RAW_range_end_exclusive']
    assert sha(primary[lo:hi]) == row['RAW_sha256'] and row['source_role']
graph = load(d / 'source-proof-graph.json')
assert len(graph['nodes']) == 22 and len(graph['edges']) == 49
assert sha((d / 'source-proof-graph.json').read_bytes()) == '1b464d9452b722abbaa6e274872366d8771780f96bc263dfeeb86322c2e88b8c'
assert sha((d / 'source-expectations.json').read_bytes()) == 'c4580c95682580e8a3a0bc68585efa98c9c659e52c928a0a6dbfdbaa6dcc62cf'
assert not lease['candidate69_seen'] and not lease['header69_seen'] and not lease['canonical_or_Git_or_ledger_edits']
out = r / 'root.primary69.adoption.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_PRIMARY69_SOURCE_ONLY_ACCEPTED',
    actual_read_only_adopter_pid=os.getpid(), source_only=True, native_owned_files=82,
    native_whole_logical_run_sha256=run['run_sha256'], native_lease=pin(d / 'lease.final.json'),
    named_complete_expectations=pin(d / 'primary-source-expectation-payload.json'),
    named_complete_RAW_LF_inputs=pin(d / 'RAW-input-payload.json'),
    complete_RAW_review=pin(d / 'review-run.json'), source_items=419, primary_regions=7,
    source_graph_sha256=sha((d / 'source-proof-graph.json').read_bytes()),
    source_expectations_sha256=sha((d / 'source-expectations.json').read_bytes()),
    next_edge='SAME actual V0* D=-A0 V0*, on all h:kerP; D=R U inclusion',
    real_source_consumers=['B21 actual projected rotation', 'B4 shared error component B27'],
    source_before_candidate=True, mathematical_proof=False, source_candidate_acceptance=False,
    SAU_claim=False, Goal_complete=False), ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS69 read-only primary adoption CLOSED82;419 exact source math nodes,22 graph nodes/49 source-only edges; no candidate proof or SAU claim.')
