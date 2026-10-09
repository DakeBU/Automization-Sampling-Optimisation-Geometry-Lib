from pathlib import Path
import hashlib, json, os

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-ambient-adjoint66'
d = r / 'independent-repository-exposition66'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
lease = load(d / 'lease.final.json')
run = load(d / 'review-run.json')
decision = load(d / 'complete-RAW-decision.json')
assert sha((d / 'lease.final.json').read_bytes()) == 'cbb0d682e323d7dab981509572601223c35fe70d3b864908b2723d7762f8cbca'
assert lease['status'] == 'CLOSED_LAST' and lease['last_owned_write']
assert lease['owned_file_count'] == 179
assert sha(can({k: v for k, v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['whole_logical_run_sha256'] == '0d3d990aad2938cb126f705b70da8946a2f43f6d0db72679e0d3b3dc8e9fa488'
files = {p.relative_to(d).as_posix(): p for p in d.rglob('*') if p.is_file()}
assert set(files) == {x['name'] for x in lease['all_owned_except_this_final_lease']} | {'lease.final.json'}
assert len(files) == 179
for x in lease['all_owned_except_this_final_lease']:
    b = files[x['name']].read_bytes()
    assert len(b) == x['RAW_bytes'] and sha(b) == x['RAW_sha256'], x['name']
    # Match the native receipt recipe exactly, including its binary gzip entry.
    lf = b.replace(b'\r\n', b'\n')
    assert len(lf) == x['LF_bytes'] and sha(lf) == x['LF_sha256'], x['name']
assert files['lease.final.json'].stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in files.values())
for key in ['COMPLETE_RAW_DECISION', 'COMPLETE_RAW_REVIEW', 'SEPARATE_COMPLETE_RAW_INPUT', 'owned_manifest']:
    x = lease[key]
    assert sha(files[x['name']].read_bytes()) == x['RAW_sha256']
assert decision['exact_science_shared_aggregate_admission'] is True
assert decision['historical_rendered_statement_six_steps_branch_admission'] is True
assert decision['current_complete_repository_reader_gate_PASS'] is False
assert decision['current_graph_freshness_admission'] is False
assert decision['source_mathematical_repair'] is False
assert decision['checked_INT_commit'] == 'eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
for k in ['Goal_complete', 'PURIFIED', 'full_Exposition', 'main_or_live_verified', 'whole_paper_complete']:
    assert decision[k] is False
out = r / 'root.repository66.adoption.json'
assert not out.exists()
out.write_text(json.dumps(dict(
    status='SCOPED_REPOSITORY66_ADOPTED_CURRENT_GENERATED_GRAPH_FRESHNESS_WITHHELD',
    actual_read_only_adopter_pid=os.getpid(), native_owned_files=179,
    checked_INT_commit=decision['checked_INT_commit'],
    native_whole_logical_run_sha256=run['run_sha256'],
    native_final_lease_RAW_sha256=sha((d / 'lease.final.json').read_bytes()),
    native_named_decision_RAW_sha256=sha((d / 'complete-RAW-decision.json').read_bytes()),
    exact_science_shared_aggregate_admission=True,
    historical_rendered_statement_six_steps_branch_admission=True,
    current_complete_repository_reader_gate_PASS=False,
    current_graph_freshness_admission=False,
    separate_root_application_and_nonowner_readback_required=True,
    full_Exposition=False, PURIFIED=False, whole_paper_complete=False, Goal_complete=False
), ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS closed repository66:179 native files; exact science/shared aggregate/historical reader accepted; current graph freshness remains withheld.')
