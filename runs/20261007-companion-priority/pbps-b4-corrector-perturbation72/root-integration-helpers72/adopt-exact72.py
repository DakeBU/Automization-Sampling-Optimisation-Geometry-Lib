from pathlib import Path
import hashlib, json, os, subprocess, sys

root = Path.cwd()
sys.path.insert(0, str(root / 'tools'))
import astis_advance as adv
r = Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
o = r / 'exact-science-verification72'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def check(z):
    b = Path(z['path']).read_bytes()
    lf = b.replace(b'\r\n', b'\n')
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], z['path']
    assert sha(lf) == z['LF_sha256'], z['path']
    if 'LF_bytes' in z:
        assert len(lf) == z['LF_bytes']
    return b

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == '4c82de3555735746e086e14cfca86e9ad1190437c38b259295ccefe0d23c2eca'
assert lease['status'] == 'CLOSED_LAST' and lease['owner'] == '/root/header_math72' and lease['native_verified']
manifest = load(o / 'owned.manifest.json')
check(lease['manifest'])
assert manifest['entry_count'] == 161 and lease['owned_files'] == 163
assert sha(can(manifest['entries'])) == manifest['logical_entries_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()} == {Path(z['path']).resolve() for z in manifest['entries']} | {(o / 'owned.manifest.json').resolve(), (o / 'lease.final.json').resolve()}
for z in manifest['entries']:
    check(z)
    assert Path(z['path']).stat().st_mtime_ns <= (o / 'lease.final.json').stat().st_mtime_ns
q = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(o / 'verify72.py'), 'readonly'], capture_output=True, check=True)
readonly = json.loads(q.stdout.decode().splitlines()[-1])
assert readonly['status'] == 'PASS' and readonly['writer_terminated'] and readonly['unique_transition']
run = load(o / 'run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['run_sha256'] == '6764b360cf902b261b6bd5c86da1b2a767e3c88fd2444eba7012a0b8e744f11c'
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == run['checked_commit'] == lease['checked_commit'] == '18183c58eee62145b6059ded11c7be05a4cb82de'
assert run['reviewer'] == '/root/header_math72' and run['native_verified'] and run['no_more_owned_writes_after_final_lease']
assert run['parent'] == subprocess.check_output(['git', 'rev-parse', 'HEAD^'], text=True).strip() == '1e9d2feb727919ebaa17ee1a67b629a0b85b0ba9'
assert sha(check(run['complete_named'])) == '9e4faf63a2a6b8eb2286925fa7e0c9c25cb19d6478a59706f407dccc037382c5'
payload = load(run['complete_named']['path'])
assert payload['checked_commit'] == head and payload['reviewer'] == run['reviewer']
assert payload['inputs'] == run['inputs'] and payload['native_evidence_reuse'] == run['native_evidence']
assert payload['transition'] == run['unique_transition'] and payload['terminal_receipts'] == run['terminal_receipts']
assert payload['named_review'] == (o / 'complete-named-review.md').read_text(encoding='utf8')
assert len(payload['inputs']['records']) == 21
qualified = []
for z in payload['inputs']['records']:
    current = check(z['input'])
    git_bytes = subprocess.check_output(['git', 'show', head + ':' + z['input']['path']])
    assert git_bytes == check(z['git_blob']) and z['git_show_terminal_EXIT'] == 0
    if z['workspace_git_RAW_equal']:
        assert current == git_bytes
    else:
        assert z['allowed_nonRAW_equivalence'] and current.replace(b'\r\n', b'\n') == git_bytes.replace(b'\r\n', b'\n')
        qualified.append(z['input']['path'])
assert {(x['kind'], x['owned_files']) for x in payload['native_evidence_reuse']['records']} == {('math', 82), ('source', 258), ('strictblind', 5)}
for z in payload['native_evidence_reuse']['records']:
    assert z['unchanged']
    check(z['native_lease'])
for z in payload['fresh_compilers']['results']:
    assert z['terminal_EXIT'] == 0 and z['standard_axioms_only'] and z['fresh_source_elaboration'] and not z['cache_replay']
    check(z['owned_output_olean'])
    receipt = load(z['receipt']['path'])
    check(z['receipt'])
    assert receipt['terminal_EXIT'] == 0 and receipt['terminal_closed']
assert payload['focused']['status'] == 'PASS' and payload['focused']['fake_closure_hits'] == []
assert payload['metadata']['accepted_terminal_EXITs'] == [0] * 7 and not payload['metadata']['full_diff_whitespace_PASS_claimed']
labels = set(payload['metadata']['accepted_receipt_labels'])
assert len(labels) == 7
for receipt in payload['terminal_receipts']:
    if 'stdout' in receipt:
        check(receipt['stdout'])
        check(receipt['stderr'])
    else:
        assert receipt['label'].startswith('immutable-exception-')
        command = receipt['command']
        assert command[:2] == ['git', 'show'] and command[2].startswith(head + ':')
        b = subprocess.check_output(command)
        inline = receipt['stdout_inline_pin']
        assert len(b) == inline['RAW_bytes'] and sha(b) == inline['RAW_sha256']
        assert b == Path(command[2].split(':', 1)[1]).read_bytes()
        assert receipt['stderr_inline_pin'] == dict(RAW_bytes=0, RAW_sha256=sha(b''))
        assert receipt['terminal_EXIT'] == 0 and receipt['terminal_closed']
    if receipt['label'] in labels:
        assert receipt['terminal_EXIT'] == 0 and receipt['terminal_closed']
whitespace = payload['whitespace_exception_audit']
assert whitespace['substantive_count'] == 335 and len(whitespace['exact_frozen_exception_files']) == 13
assert whitespace['scoped_authored_terminal_EXIT'] == 0 and not whitespace['full_diff_whitespace_PASS_claimed']
transition = payload['transition']
ledger = Path('runs/substantive_advances.jsonl').read_bytes()
n = transition['before_bytes']
assert len(ledger) == transition['after_bytes'] and sha(ledger) == transition['after_RAW_sha256']
assert sha(ledger[:n]) == transition['before_RAW_sha256']
append = ledger[n:]
assert len(append.splitlines()) == transition['append_count'] == 1 and sha(append) == transition['appended_RAW_sha256']
event = json.loads(append)
assert event == transition['event'] and event['to_state'] == 'VERIFIED' and event['from_state'] == 'PROVED_LOCAL'
assert event['worker_id'] == '/root/header_math72' and event['worker_id'] != load(r / 'claim.json')['created_by']
assert adv.current_advances()[event['advance_id']]['state'] == 'VERIFIED'
check(run['verified_json'])
verified = load(r / 'verified.json')
assert verified == payload['verified'] and verified['verified_commit'] == head and verified['native_verified']
assert verified['actual_verifier_PID'] == transition['actual_verifier_PID'] == 21364
p = r / 'root.exact-verification72.adoption.json'
assert not p.exists()
record = dict(status='ACCEPTED_NONOWNER_EXACT_SCI72_TWO_CONNECTED_IDENTITIES', actual_root_PID=os.getpid(), native_verified=True, verified_commit=head, native_files=163, finite_Git_inputs=21, Git_CRLF_only_qualified_references=qualified, native_whole_logical_run_sha256=h, native_complete_named=pin(o / 'complete-named-review-decision-input-payload.json'), native_lease=pin(o / 'lease.final.json'), root_fresh_readonly_validator=readonly, root_readonly_terminal_EXIT=q.returncode, unique_VERIFIED_append_SHA256=sha(append), unique_VERIFIED_PID=21364, unique_VERIFIED_EXIT=0, full_whitespace_PASS=False, authored_whitespace_PASS=True, immutable_whitespace_findings=335, aggregate=False, reader=False, remoteCI=False, main_live=False, PURIFIED=False, Goal_complete=False)
p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS72 nonowner exact VERIFIED CLOSED163/21Git/freshLean2; unique21364 EXIT0 and scoped immutable whitespace evidence retained. Aggregate/reader pending.')
