from pathlib import Path
import hashlib, json, os

base = Path('runs/20261007-companion-priority')
o = base / 'pbps-half-turn-construction-preread73'
out = base / 'pbps-harmonic-flow-preproof73'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def check(z):
    b = Path(z['path']).read_bytes()
    assert len(b) == z['bytes'] and sha(b) == z['raw_sha256'], z['path']
    assert sha(b.replace(b'\r\n', b'\n')) == z['lf_sha256'], z['path']
    return b

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == 'a588ba76302da36dd92a15a3d565d230594778158cd3ccd67c3b946e247481d2'
assert lease['state'] == 'CLOSED_LAST' and lease['actor'] == '/root/exact_science63'
assert lease['owned_count_including_lease'] == 103 and lease['actual_readonly_probe_exit_code'] == 0
rows = lease['all_files_except_self']
assert len(rows) == 102 and sha(can(rows)) == lease['closure_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()} == {Path(z['path']).resolve() for z in rows} | {(o / 'lease.final.json').resolve()}
for z in rows:
    check(z)
    assert Path(z['path']).stat().st_mtime_ns <= (o / 'lease.final.json').stat().st_mtime_ns
run = load(o / 'run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['whole_logical_run_sha256'] == 'f46a22d66aac350c901b2beb467500c39e8d10f2e98eb795bbaf0cd80fafc508'
assert run['status'] == 'READY_SOURCE_FIRST_CONTRACT_ONLY' and run['source_first_no_73_header_read']
assert not run['canonical_git_ledger_goal_writes'] and not run['new_compilation_or_proof_credit']
payload = load(run['complete_named_payload']['path'])
assert sha(check(run['complete_named_payload'])) == 'a570bcda2ac931d472ff2a7b2fc4f809c677f5a66ddb31d8a3ac469a94fe706c'
for name, x in payload['content'].items():
    assert x == load(o / name), name
for name, x in payload['native_execution'].items():
    assert x == load(o / name), name
for z in payload['exact_content_raw_pins']:
    check(z)
inputs = load(o / 'inputs.manifest.json')
assert inputs['input_count'] == len(inputs['inputs']) == 21
for z in inputs['inputs']:
    check(z)
source = load(o / 'source.regions.json')
primary = check(source['primary'])
for z in source['regions'] + source['formulas'] + load(o / 'construction.formula-spans.json')['formulas']:
    b = primary[z['raw_byte_start_inclusive']:z['raw_byte_end_exclusive']]
    assert len(b) == z['bytes'] and sha(b) == z['literal_span_raw_sha256']
    if 'snapshot' in z:
        assert b == (o / z['snapshot']).read_bytes()
assert not out.exists()
out.mkdir()
record = dict(status='ACCEPTED_IMMUTABLE_SOURCE_FIRST_PLANNING73_ONLY', actual_root_PID=os.getpid(), native_owned_files=103, finite_inputs=21, native_whole_logical_run_sha256=h, native_lease=pin(o / 'lease.final.json'), complete_named_payload=pin(o / 'complete-named-source-first-review.payload.json'), selected_contract=pin(o / 'selected-contract.json'), source_expectations=pin(o / 'source-expectations.json'), source_regions=13, block_formulas=19, supplementary_paired_formulas=4, full_SourceProofGraph_present=False, independent_source_topology_admission_pending=True, header_sealed=False, proof_search=False, compiler=False, SAU_claimed=False, VERIFIED=False, full_paper=False, Goal_complete=False)
(out / 'root.source-first73.adoption.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS73 source-first CLOSED103/21 finite inputs and exact source intervals; planning only, graph/statement seal/proof pending.')
