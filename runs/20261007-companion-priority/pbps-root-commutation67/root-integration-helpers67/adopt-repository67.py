from pathlib import Path
import hashlib, json, os, subprocess

r = Path('runs/20261007-companion-priority/pbps-root-commutation67')
o = r / 'independent-repository-exposition67'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
lease = load(o / 'lease.final.json')
assert lease['status'] == 'CLOSED_LAST' and lease['last_owned_write']
assert lease['owner'] == '/root/independent_source64'
assert not lease['postclose_writes_permitted']
assert sha((o / 'lease.final.json').read_bytes()) == 'd095b9d0cddd86e14bc25e51c02bb060a13d012f43b41792f2796c6016da193a'
assert sha((o / 'owned-manifest.json').read_bytes()) == lease['owned_manifest']['RAW_sha256']
entries = lease['all_owned_except_this_final_lease']
actual = {p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}
assert actual == {z['name'] for z in entries} | {'lease.final.json'}
assert len(actual) == lease['owned_file_count'] == 299
last = (o / 'lease.final.json').stat().st_mtime_ns
for z in entries:
    p = o / z['name']; b = p.read_bytes(); lf = b.replace(b'\r\n', b'\n')
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], p
    assert len(lf) == z['LF_bytes'] and sha(lf) == z['LF_sha256'], p
    assert p.stat().st_mtime_ns <= last, p
run = load(o / 'review-run.json'); h = run.pop('run_sha256')
assert sha(json.dumps(run, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()) == h == lease['whole_logical_run_sha256']
for k in ['COMPLETE_RAW_REVIEW', 'COMPLETE_RAW_DECISION', 'SEPARATE_COMPLETE_RAW_INPUT']:
    z = lease[k]; assert sha((o / z['name']).read_bytes()) == z['RAW_sha256']
d = load(o / 'decision.json')
assert (o / 'decision.json').read_bytes() == (o / 'complete-RAW-decision.json').read_bytes()
assert d['status'] == 'ACCEPT_SCOPED_CURRENT_FINAL_ADMIN'
assert d['exact_SCI_commit'] == subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
for k in ['scoped_local_reader', 'serialized_shared_imports_Registry_Tests_aggregate', 'current_official_graph_freshness', 'current_full_graph_publication_validator', 'current_final_cell_binding']:
    assert d['acceptance'][k]
for k in ['full_Exposition', 'PURIFIED', 'main_merged', 'live', 'whole_Goal_complete']:
    assert not d['acceptance'][k]
for z in d['final_cells']:
    b = Path(z['path']).read_bytes(); assert len(b) == z['bytes'] and sha(b) == z['raw_sha256']
g = load(o / 'current-graph-and-publication-bindings.json')
assert g['full_publication_graph_validator_errors'] == []
assert g['current_recomputed_publication_inputs_sha256'] == d['current_graph_publication_inputs_sha256']
for k in ['current_graph', 'current_site_data']:
    z = g[k]; assert sha(Path(z['path']).read_bytes()) == z['RAW_sha256']
for z in d['current_publication_bindings']:
    q = z['canonical_audit']; assert sha(Path(q['path']).read_bytes()) == q['RAW_sha256']
dest = r / 'root.repository67.adoption.json'
assert not dest.exists()
payload = dict(schema='root-readonly-native-repository67-adoption-v1', actual_foreground_pid=os.getpid(),
    accepted_scoped_aggregate=True, accepted_current_graph=True, native_owned_file_count=299,
    exact_science_commit=d['exact_SCI_commit'], whole_logical_run_sha256=h,
    native_lease_RAW_sha256=sha((o / 'lease.final.json').read_bytes()),
    native_RAW_payloads={k: lease[k] for k in ['COMPLETE_RAW_REVIEW', 'COMPLETE_RAW_DECISION', 'SEPARATE_COMPLETE_RAW_INPUT']},
    final_cells=d['final_cells'], current_graph_publication_inputs_sha256=d['current_graph_publication_inputs_sha256'],
    native_decision=d['status'], independent_reviewer=d['reviewer'], zero_postclose_owned_writes=True,
    native_files_mutated=False, historical_INT66_freshness_withholding_unchanged=True,
    full_Exposition=False, PURIFIED=False, main_live=False, full_paper=False, whole_Goal_complete=False)
dest.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
print(json.dumps(dict(status='PASS_NATIVE_REPOSITORY67_ADOPTED', owned_files=299, accepted_scoped_aggregate=True, full_paper=False)))
