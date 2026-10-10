from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys

BASE = Path(__file__).resolve().parent
PRIMARY = BASE.parent / 'independent-primary64'
PYTHON = Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n): return json.loads((BASE / n).read_text(encoding='utf-8'))
def write(n, v): (BASE / n).write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p): return {'name': p.relative_to(BASE).as_posix(), 'bytes': p.stat().st_size, 'raw_sha256': sha(p)}
def inventory(excluded): return [pin(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p.relative_to(BASE).as_posix() not in excluded]
def check_manifest(entries):
    for e in entries:
        p = BASE / e['name']
        assert p.is_file() and p.stat().st_size == e['bytes'] and sha(p) == e['raw_sha256'], ('owned drift', e['name'])

def check_inputs():
    review = load('independent-header64.review.json')
    digests = load('review-digests.json')
    logical = dict(review)
    logical.pop('run_sha256')
    computed = hashlib.sha256(json.dumps(logical, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    assert computed == review['run_sha256'] == digests['run_sha256']
    assert sha(BASE / digests['named_payload']) == digests['full_named_RAW_payload_sha256']
    assert sha(BASE / 'independent-header64.review.md') == digests['report_raw_sha256']
    check_manifest(review['process_and_hash_contract']['owned_outputs_base_manifest'])
    exact = load('exact-header-input-pins.json')
    for p in exact['files']:
        live = Path(p['path']); raw = live.read_bytes()
        assert len(raw) == p['bytes'] and hashlib.sha256(raw).hexdigest() == p['raw_sha256']
        assert hashlib.sha256(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')).hexdigest() == p['lf_sha256']
    support = load('bounded-diagnostic-support-inputs.json')
    for p in support['fixed_support_inputs']:
        live = Path(p['path']); raw = live.read_bytes()
        assert len(raw) == p['bytes'] and hashlib.sha256(raw).hexdigest() == p['raw_sha256'], ('support drift', p['path'])
        assert sha(BASE / p['raw_snapshot']) == p['raw_sha256']
        assert sha(BASE / p['lf_snapshot']) == p['lf_sha256']
    reread = load('primary-before-header-reread-receipt.json')
    for p in reread['primary64_immutable_outputs']:
        f = PRIMARY / p['name']
        assert f.stat().st_size == p['bytes'] and sha(f) == p['raw_sha256'], ('primary drift', p['name'])
    raw = Path(reread['primary_source']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == reread['primary_source_raw_sha256']
    for region in reread['regions']:
        a, b = region['byte_range_zero_based_half_open']
        assert hashlib.sha256(raw[a:b]).hexdigest() == region['raw_sha256']
    coverage = json.loads((PRIMARY / 'source-coverage-inventory.json').read_text(encoding='utf-8'))
    assert coverage['unclassified_count'] == 0 and len(coverage['inventory']) == 1086
    for e in coverage['inventory']:
        a, b = e['byte_range_zero_based_half_open']
        assert hashlib.sha256(raw[a:b]).hexdigest() == e['literal_sha256']
    s = load('source-reread.process-receipt.json')
    assert s['actual_exit_code'] == 0 and s['terminal'] is True
    assert sha(BASE / 'source-reread.stdout.txt') == s['stdout_raw_sha256']
    assert sha(BASE / 'source-reread.stderr.txt') == s['stderr_raw_sha256']
    assert sha(BASE / 'primary-before-header-reread-receipt.json') == s['source_before_header_receipt_raw_sha256']
    seal = load('pre-header-source-seal.json')
    assert exact['pre_header_source_seal_sha256'] == sha(BASE / 'pre-header-source-seal.json')
    assert reread['exact_header0_or_header1_received_or_read'] is False
    assert s['end_utc'] < min(x['first_exact_read_utc'] for x in exact['files'])
    assert seal['actual_preread_process_receipt_sha256'] == sha(BASE / 'source-reread.process-receipt.json')
    assert sha(PRIMARY / 'source-proof-graph.json') == seal['source_graph_sha256'] == reread['graph_sha256']
    assert sha(PRIMARY / 'source-coverage-inventory.json') == seal['source_coverage_sha256'] == reread['coverage_sha256']
    return {'run_sha256': computed, 'full_named_RAW_payload_sha256': digests['full_named_RAW_payload_sha256'],
        'exact_header0_raw_sha256': exact['files'][0]['raw_sha256'], 'exact_header1_raw_sha256': exact['files'][1]['raw_sha256'],
        'primary_files_unchanged': len(reread['primary64_immutable_outputs']), 'coverage_items_checked': 1086,
        'source_first_causality_checked': True, 'fixed_support_inputs_unchanged': len(support['fixed_support_inputs'])}

def finalize():
    checked = check_inputs()
    excluded = {'owned-lease.json', 'terminal-finalizer.json', 'terminal-readback.json',
        'finalizer.stdout.txt', 'finalizer.stderr.txt', 'finalizer.process-receipt.json',
        'readback.stdout.txt', 'readback.stderr.txt', 'readback.process-receipt.json'}
    write('terminal-finalizer.json', {'schema': 1, 'event': 'ACTUAL_FOREGROUND_FINALIZER_CHECK_COMPLETE',
        'actual_pid': os.getpid(), 'utc': now(), 'checks': checked,
        'owned_manifest': inventory(excluded), 'own_future_process_and_closure_layer_exclusions': sorted(excluded),
        'pycache_count': len(list(BASE.rglob('*.pyc'))), 'proof_or_compiler_run': False,
        'native_exit_evidence_location': 'finalizer.process-receipt.json, written by foreground parent after child exit'})
    print(json.dumps({'event': 'FINALIZER_PASS', 'actual_pid': os.getpid(), **checked, 'finalizer_raw_sha256': sha(BASE / 'terminal-finalizer.json')}))

def readback():
    checked = check_inputs()
    f = load('terminal-finalizer.json')
    check_manifest(f['owned_manifest'])
    process = load('finalizer.process-receipt.json')
    assert process['actual_exit_code'] == 0 and process['terminal_closed'] is True
    assert process['actual_child_pid'] == f['actual_pid']
    assert sha(BASE / 'finalizer.stdout.txt') == process['stdout_raw_sha256']
    assert sha(BASE / 'finalizer.stderr.txt') == process['stderr_raw_sha256']
    excluded = {'owned-lease.json', 'terminal-readback.json', 'readback.stdout.txt', 'readback.stderr.txt', 'readback.process-receipt.json'}
    write('terminal-readback.json', {'schema': 1, 'event': 'ACTUAL_FOREGROUND_READBACK_CHECK_COMPLETE',
        'actual_pid': os.getpid(), 'utc': now(), 'checks': checked,
        'finalizer_raw_sha256': sha(BASE / 'terminal-finalizer.json'),
        'finalizer_process_receipt_raw_sha256': sha(BASE / 'finalizer.process-receipt.json'),
        'actual_finalizer_pid': process['actual_child_pid'], 'actual_finalizer_exit': process['actual_exit_code'],
        'owned_manifest': inventory(excluded), 'own_future_process_and_closure_layer_exclusions': sorted(excluded),
        'pycache_count': len(list(BASE.rglob('*.pyc'))), 'proof_or_compiler_run': False,
        'native_exit_evidence_location': 'readback.process-receipt.json, written by foreground parent after child exit'})
    print(json.dumps({'event': 'READBACK_PASS', 'actual_pid': os.getpid(), **checked, 'readback_raw_sha256': sha(BASE / 'terminal-readback.json')}))

def run(which):
    assert which in ['finalizer', 'readback']
    action = 'finalize' if which == 'finalizer' else 'readback'
    pre = inventory({'owned-lease.json', which + '.stdout.txt', which + '.stderr.txt', which + '.process-receipt.json'})
    started = now()
    process = subprocess.Popen([str(PYTHON), '-X', 'utf8', str(Path(__file__).resolve()), action], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    ended = now()
    (BASE / (which + '.stdout.txt')).write_bytes(stdout)
    (BASE / (which + '.stderr.txt')).write_bytes(stderr)
    receipt = {'schema': 1, 'event': 'ACTUAL_FOREGROUND_CHILD_TERMINATED', 'action': action,
        'actual_parent_pid': os.getpid(), 'actual_child_pid': process.pid, 'actual_exit_code': process.returncode,
        'terminal_closed': process.poll() is not None, 'started_utc': started, 'ended_utc': ended,
        'stdout_raw_sha256': hashlib.sha256(stdout).hexdigest(), 'stderr_raw_sha256': hashlib.sha256(stderr).hexdigest(),
        'pre_input_pins': pre, 'pre_input_pin_scope': 'Exact owned files present before foreground child launch except open lease and this process output/receipt self-layer.',
        'proof_or_compiler_run': False}
    write(which + '.process-receipt.json', receipt)
    print(stdout.decode('utf-8'), end='')
    if stderr: print(stderr.decode('utf-8'), file=sys.stderr, end='')
    print(json.dumps({'event': 'NATIVE_PROCESS_RECEIPT', 'action': action, 'actual_parent_pid': os.getpid(),
        'actual_child_pid': process.pid, 'actual_exit_code': process.returncode, 'terminal_closed': process.poll() is not None,
        'process_receipt_raw_sha256': sha(BASE / (which + '.process-receipt.json'))}))
    sys.exit(process.returncode)

def close():
    checked = check_inputs()
    f, r = load('terminal-finalizer.json'), load('terminal-readback.json')
    check_manifest(f['owned_manifest']); check_manifest(r['owned_manifest'])
    processes = {}
    for which, evidence in [('finalizer', f), ('readback', r)]:
        process = load(which + '.process-receipt.json')
        assert process['actual_exit_code'] == 0 and process['terminal_closed'] is True
        assert process['actual_child_pid'] == evidence['actual_pid']
        assert sha(BASE / (which + '.stdout.txt')) == process['stdout_raw_sha256']
        assert sha(BASE / (which + '.stderr.txt')) == process['stderr_raw_sha256']
        processes[which] = {'actual_parent_pid': process['actual_parent_pid'], 'actual_child_pid': process['actual_child_pid'],
            'actual_exit_code': process['actual_exit_code'], 'terminal_closed': process['terminal_closed'],
            'receipt_raw_sha256': sha(BASE / (which + '.process-receipt.json'))}
    all_outputs = inventory({'owned-lease.json'})
    manifest_sha = hashlib.sha256(json.dumps(all_outputs, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()
    lease = {'schema': 1, 'event': 'CLOSED_LAST', 'state': 'CLOSED_LAST', 'owned_prefix': str(BASE),
        'actual_closer_pid': os.getpid(), 'closed_utc': now(), 'checks': checked, 'actual_foreground_processes': processes,
        'terminal_finalizer_raw_sha256': sha(BASE / 'terminal-finalizer.json'),
        'terminal_readback_raw_sha256': sha(BASE / 'terminal-readback.json'),
        'owned_outputs': all_outputs, 'owned_output_count_excluding_lease': len(all_outputs),
        'owned_outputs_logical_manifest_sha256': manifest_sha,
        'explicit_self_layer_exclusions': [{'name': 'owned-lease.json', 'reason': 'Cannot bind its own literal raw digest; native post-close read-only terminal reports and checks the full literal lease bytes.'}],
        'pycache_policy': 'All files recursively included; no pycache exclusion.', 'pycache_files': [p.relative_to(BASE).as_posix() for p in sorted(BASE.rglob('*.pyc'))],
        'write_order_contract': 'This CLOSED_LAST lease is the last owned write; subsequent terminal readback is read-only.',
        'theorem_or_science_or_Goal_admission': False, 'Statement_Seal_granted': False}
    write('owned-lease.json', lease)
    print(json.dumps({'event': 'CLOSED_LAST', 'actual_closer_pid': os.getpid(), 'lease_raw_sha256': sha(BASE / 'owned-lease.json'),
        'owned_outputs_plus_lease': len(all_outputs) + 1, 'actual_processes': processes, **checked}))

def postclose():
    lease = load('owned-lease.json')
    assert lease['state'] == lease['event'] == 'CLOSED_LAST'
    check_manifest(lease['owned_outputs'])
    names = {e['name'] for e in lease['owned_outputs']} | {'owned-lease.json'}
    actual = {p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()}
    assert actual == names, ('unbound output', sorted(actual ^ names))
    checked = check_inputs()
    print(json.dumps({'event': 'READ_ONLY_NATIVE_POST_CLOSE_PASS', 'actual_pid': os.getpid(),
        'lease_raw_sha256': sha(BASE / 'owned-lease.json'), 'closed_actual_closer_pid': lease['actual_closer_pid'],
        'owned_outputs_plus_lease': len(actual), 'all_owned_outputs_bound': True, 'writes': 0, **checked}))

action = sys.argv[1]
if action == 'finalize': finalize()
elif action == 'readback': readback()
elif action == 'run': run(sys.argv[2])
elif action == 'close': close()
elif action == 'postclose': postclose()
else: raise ValueError(action)
