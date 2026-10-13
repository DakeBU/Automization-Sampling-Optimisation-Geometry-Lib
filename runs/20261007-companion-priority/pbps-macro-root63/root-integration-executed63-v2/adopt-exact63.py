from pathlib import Path
import hashlib, json, os, subprocess

root = Path.cwd(); r = root / 'runs/20261007-companion-priority/pbps-macro-root63'
d = r / 'exact-science-verification'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
seen = set()

def path(s):
    p = Path(str(s).replace('\\', '/'))
    return p if p.is_absolute() else root / p

def check(q, actual=None, span=False):
    p = path(actual or q['path']); b = p.read_bytes()
    if span:
        b = b''.join(b.splitlines(keepends=True)[q['start_line']-1:q['end_line']])
    assert sha(b) == q['raw_sha256'], (q['path'], p)
    z = b.replace(b'\r\n', b'\n')
    if 'lf_sha256' in q: assert sha(z) == q['lf_sha256'], p
    for k, v in [('bytes', len(b)), ('raw_bytes', len(b)), ('lf_bytes', len(z))]:
        if k in q: assert q[k] == v, (p, k)
    seen.add((str(path(q['path']).resolve()).lower(), q['raw_sha256'], q.get('start_line'), q.get('end_line')))

run, lease, receipt, decision, bindings, inputs, transition = [load(d / n) for n in [
    'run.json', 'lease.json', 'native.receipt.json', 'verification.decision.json',
    'bindings.result.json', 'input.manifest.json', 'transition.result.json']]
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == run['verified_commit'] == lease['verified_commit'] == '4d02622332d02d0bd6c977d3cee48fd535ebf203'
assert lease['status'] == 'CLOSED_LAST' and lease['verifier_id'] == '/root/exact_science63'
assert sha((d / 'lease.json').read_bytes()) == 'e999d5d8f77a2c3388a01782c2e402d40e7a5a1e454337c314500d2a90055544'
assert sha(can({k:v for k,v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['whole_run_sha256'] == '92df2c06469fbf6768955f8ae5b42ee0d2057ffbd7efc17c9d3b85e4a4130621'
assert sha((d / 'named-verification.payload.json').read_bytes()) == run['complete_named_RAW_payload_sha256'] == lease['distinct_complete_named_RAW_payload_sha256'] == 'd81da4c908301a984363da4d397f2a5dd53da6add285ba4bc4c058e3ff41b474'
assert decision['result'] == 'ACCEPTED_SCOPED_EXACT_SCIENCE63_WITH_EXPLICIT_INTEGRATION_METADATA_DEBT'
assert decision['required_scoped_gates_passed'] is True
assert receipt['full_repository_acceptance'] is False and lease['integration_metadata_debt']['frontier_check_exit_code'] == 1
assert lease['actual_foreground_candidate_readback']['exit_code'] == 0
assert lease['actual_foreground_candidate_readback']['status'] == 'FOREGROUND_TERMINAL_CLOSED'
assert lease['actual_foreground_candidate_readback']['actual_child_pid'] == 32304
assert lease['actual_final_closure_pid'] == 46240
for n, pid in [('finalizer.process.receipt.json', 14980), ('readback.process.receipt.json', 32304)]:
    q = load(d / n); assert q['exit_code'] == 0 and q['status'] == 'FOREGROUND_TERMINAL_CLOSED'
    assert q['actual_child_pid'] == pid
    check(q['stdout']); check(q['stderr'])
check(receipt['run_RAW']); check(receipt['named_payload']); check(receipt['independent_transition'])
outputs = lease['complete_owned_output_manifest_after_readback']
for q in outputs: check(q)
actual = {p.resolve() for p in d.rglob('*') if p.is_file()}
assert actual == {path(q['path']).resolve() for q in outputs} | {d / 'lease.json', d / 'proposed-lease.closed.json'}
assert (d / 'lease.json').read_bytes() == (d / 'proposed-lease.closed.json').read_bytes()
maps = {}
assert len(bindings['finite_explicit_history_maps']) == 60
for row in bindings['finite_explicit_history_maps']:
    q = row['original']; p = path(row['explicit_raw_snapshot']).resolve()
    check(q, p)
    maps.setdefault((str(path(q['path']).resolve()).lower(), q['raw_sha256']), set()).add(p)
assert bindings['qualified_pin_readbacks'] == 346 and not bindings['unresolved']
assert bindings['arbitrary_fallback_used'] is False
history = []
for row in bindings['checked_pins']:
    q = row['original']; effective = path(row['effective_exact_bytes']).resolve()
    key = (str(path(q['path']).resolve()).lower(), q['raw_sha256'])
    if row['historical_explicit_mapping']:
        assert key in maps and effective in maps[key], row
        history.append(dict(original=q, exact_snapshot=effective.as_posix()))
    else: assert effective == path(q['path']).resolve(), row
    assert row['mode'] in {'whole-file', 'literal-line-span'}
    check(q, effective, row['mode'] == 'literal-line-span')
assert len(inputs['input_artifacts']) == 1627 and inputs['frozen_before_own_compiler'] is True
before_ledger = d / 'ledger.before-own-VERIFIED.exactraw.snapshot'
after_ledger = d / 'ledger.after-own-VERIFIED.exactraw.snapshot'
for q in inputs['input_artifacts']:
    check(q, q['exact_raw_snapshot'])
    p = path(q['path'])
    if p.resolve() == (root / 'runs/substantive_advances.jsonl').resolve():
        check(q, before_ledger)
    else: check(q)
assert transition['append_count'] == 1 and transition['before_raw_prefix_preserved'] is True
assert transition['worker_id'] == '/root/exact_science63' and transition['state_after'] == 'VERIFIED'
assert transition['canonical_frontier_or_audit_mutated'] is False
assert after_ledger.read_bytes().startswith(before_ledger.read_bytes())
assert (root / 'runs/substantive_advances.jsonl').read_bytes() == after_ledger.read_bytes()
records = [json.loads(s) for s in after_ledger.read_text(encoding='utf-8').splitlines() if s.strip()]
accepted = [x for x in records if x.get('advance_id') == 'ASTIS-SA-20261009-PBPSUniqueMacroscopicDefectRoot' and x.get('to_state') == 'VERIFIED']
assert len(accepted) == 1 and accepted[0]['worker_id'] == '/root/exact_science63'
assert accepted[0]['evidence']['verified_commit'] == head
out = r / 'root.exact-verification63.adoption.json'; assert not out.exists()
out.write_text(json.dumps(dict(
    status='INDEPENDENT_EXACT_SCIENCE63_ACCEPTED_WITH_REPOSITORY_METADATA_DEBT',
    actual_adopter_pid=os.getpid(), native_verified=True, verified_commit=head,
    verifier='/root/exact_science63', native_whole_run_sha256=run['run_sha256'],
    distinct_native_complete_RAW_payload_sha256=run['complete_named_RAW_payload_sha256'],
    qualified_pin_readbacks=len(seen), native_owned_file_count=len(actual),
    finite_history_map_rows=60, unique_qualified_history_keys=len(maps), historical_resolutions=history,
    independent_ledger_transition=accepted[0], canonical_mutations_by_root=False,
    original_integration_metadata_debt=lease['integration_metadata_debt'],
    full_repository_acceptance=False, full_paper=False, integration_pending=True),
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
(r / 'verified.json').write_bytes((d / 'native.receipt.json').read_bytes())
print('PASS adopted independently CLOSED_LAST SCI63 VERIFIED;', len(seen), 'qualified readbacks;', len(actual), 'native owned files unchanged; repository metadata debt retained. Root made no VERIFIED transition.')
