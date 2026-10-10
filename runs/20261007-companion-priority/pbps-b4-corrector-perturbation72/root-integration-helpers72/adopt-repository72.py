from pathlib import Path
import hashlib, json, os, subprocess, sys

r = Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
o = r / 'independent-repository-reader72'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
canon = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def check(z):
    b = Path(z['path']).read_bytes()
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], z['path']
    assert sha(b.replace(b'\r\n', b'\n')) == z['LF_sha256'], z['path']
    return b

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))

expected_run, expected_lease, expected_payload = sys.argv[1:]
lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == expected_lease
assert lease['status'] == 'CLOSED_LAST' and lease['actor'] == '/root/exact_science63'
assert lease['postclose_owned_writes_forbidden'] and lease['final_owned_write']
assert lease['file_count_including_lease'] == len(lease['files']) + 1
assert sha(canon(lease['files'])) == lease['closure_logical_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()} == (
    {Path(z['path']).resolve() for z in lease['files']} | {(o / 'lease.final.json').resolve()})
for z in lease['files']:
    check(z)
    assert Path(z['path']).stat().st_mtime_ns <= (o / 'lease.final.json').stat().st_mtime_ns
run = load(o / 'run.json')
h = sha(canon({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['run_sha256'] == expected_run
assert sha(check(run['complete_named_RAW_payload'])) == expected_payload
check(run['decision'])
check(run['inputs_manifest'])
payload = load(run['complete_named_RAW_payload']['path'])
decision = load(o / 'decision.json')
assert payload['decision'] == decision and decision['accepted_scoped_aggregate']
assert decision['actor'] == '/root/exact_science63' and decision['independent_of_formalizer_stabilizer']
assert not decision['new_independent_mathematics_certification']
assert not decision['new_VERIFIED_transition'] and not decision['blockers']
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert head == decision['checked_science_commit'] == run['checked_science_commit']
inputs = load(o / 'inputs.manifest.json')
assert inputs == payload['inputs'] and inputs['input_count'] == len(inputs['inputs']) == 145
check(inputs['dispatch'])
for z in inputs['inputs']:
    check(z)
assert len(payload['gates']['receipts']) == 21
finals = [x for x in payload['gates']['receipts'] if 'after-admin-recovery' in x['label']]
assert len(finals) == 8 and all(x['exit_code'] == 0 and x['terminal_closed'] for x in finals)
assert decision['RAW_downloads'] == decision['copy_callbacks'] == 5
assert decision['formula_BODY_steps'] == [6, 4] and decision['independently_viewed_PNGs'] == 13
assert decision['Registry'] == 521 and decision['publication_units'] == 242
assert decision['root_jobs'] == 9183 and decision['Tests_jobs'] == 9483
assert not any(decision[k] for k in ['Goal_complete', 'PURIFIED', 'full_Exposition_Seal', 'main', 'live', 'whole_paper'])
out = Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out / 'native-readonly.stdout.log').open('wb') as s, (out / 'native-readonly.stderr.log').open('wb') as e:
    p = subprocess.Popen([sys.executable, '-B', '-X', 'utf8', str(o / 'review72.py'), 'postclose'], stdout=s, stderr=e)
    code = p.wait()
assert code == 0
readonly = json.loads((out / 'native-readonly.stdout.log').read_text(encoding='utf8').splitlines()[-1])
assert readonly['status'] == 'READONLY_POSTCLOSE_PASS' and not readonly['owned_writes']
record = dict(status='ACCEPTED_INDEPENDENT_SCOPED_AGGREGATE_READER72_WITH_EXPOSITION_DEBT',
    actual_root_PID=os.getpid(), accepted_scoped_aggregate=True, checked_science_commit=head,
    native_actor=decision['actor'], native_lease=pin(o / 'lease.final.json'),
    native_run_sha256=h, complete_named_RAW_payload=run['complete_named_RAW_payload'],
    native_files=lease['file_count_including_lease'], current_inputs=145,
    readonly_PID=p.pid, readonly_EXIT=code, readonly=readonly,
    readonly_stdout=pin(out / 'native-readonly.stdout.log'), readonly_stderr=pin(out / 'native-readonly.stderr.log'),
    reader_debts=decision['reader_debts'], new_math_verification=False,
    full_Exposition_Seal=False, PURIFIED=False, main=False, live=False, whole_paper=False, Goal_complete=False)
dest = r / 'root.repository72.adoption.json'
assert not dest.exists()
dest.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS72 independent scoped aggregate/reader adopted;145 exact inputs,8 final gates,5 copy/downloads; exposition debt retained.')
