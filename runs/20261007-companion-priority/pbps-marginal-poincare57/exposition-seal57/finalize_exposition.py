from pathlib import Path
import json, hashlib, datetime, subprocess, os

ROOT = Path('E:/Samplinglib')
B = ROOT / 'runs/20261007-companion-priority/pbps-marginal-poincare57'
OUT = B / 'exposition-seal57'
ACTOR = '/root/fresh_blind_decoder56'
SCI = 'e8a9044ba5a945eaa4b4aecd110b63494fe6c68e'
HEAD = 'f311e4296fb5295a2e56e3214d3bd2585f849dcf'
RECIPE = 'SHA256 UTF8 json.dumps(COMPLETE native object minus ONLY complete_object_sha256, ensure_ascii=False, sort_keys=True, separators=(comma,colon)); no newline. Raw/LF file receipts and named publication payload digest are separate.'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')

def read(path):
    with Path(path).open('rb') as stream:
        return stream.read()

def pin(path):
    path = Path(path)
    raw = read(path)
    lf = raw.replace(b'\r\n', b'\n')
    return {'path': str(path).replace('\\', '/'), 'bytes': len(raw), 'raw_sha256': sha(raw), 'lf_bytes': len(lf), 'lf_sha256': sha(lf)}

def write(name, obj):
    obj = dict(obj)
    assert 'complete_object_sha256' not in obj
    obj['complete_object_sha256'] = sha(canonical(obj))
    path = OUT / name
    raw = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf8')
    with path.open('wb') as stream:
        stream.write(raw)
    assert read(path) == raw
    back = json.loads(read(path))
    value = back.pop('complete_object_sha256')
    assert sha(canonical(back)) == value
    return pin(path)

assert not (OUT / 'lease.json').exists(), 'No mutation or reopening of a CLOSED seal.'
prep = {'schema_version': 1, 'artifact_kind': 'native-exposition57-preparation-process', 'process': 'prepare_exposition.py', 'actual_native_exec_chunk': '127669', 'actual_exit_code': 0, 'actual_pid': 52168, 'actual_stdout_counts': {'input_count': 66, 'checks': 12, 'images': 4, 'formula_steps': 6, 'node_bytes': 36636, 'graph_nodes': 15, 'graph_edges': 14}, 'execution': 'Synchronous foreground tools.exec_command returned exit_code0 with no session_id. Every context-manager file resource closed. No detached/background/compiler/browser process launched.', 'hash_recipe': RECIPE}
write('prepare.process.status.json', prep)
manifest = json.loads(read(OUT / 'input.manifest.json'))
inputs = manifest['inputs']
assert manifest['input_count'] == len(inputs) == 66
for entry in inputs:
    assert pin(entry['input']['path']) == entry['input']
    assert pin(entry['raw_snapshot']['path']) == entry['raw_snapshot']
    assert pin(entry['lf_snapshot']['path']) == entry['lf_snapshot']
    assert read(entry['raw_snapshot']['path']) == read(entry['input']['path'])
    assert read(entry['lf_snapshot']['path']) == read(entry['input']['path']).replace(b'\r\n', b'\n')
verification = json.loads(read(OUT / 'verification.json'))
assert len(verification['checks']) == 12 and all(check['exit_code'] == 0 for check in verification['checks'])
assert len(verification['images']) == 4 and verification['rendered']['proof_steps'] == 6
for name in ['companion_container', 'graph_container']:
    assert pin(verification['site'][name]['path']) == verification['site'][name]
head_process = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True)
assert head_process.returncode == 0 and head_process.stdout.decode().strip() == HEAD
for path in sorted(OUT.glob('*.json')):
    obj = json.loads(read(path))
    value = obj.pop('complete_object_sha256')
    assert sha(canonical(obj)) == value, str(path)
report = json.loads(read(OUT / 'exposition.review.json'))
assert report['verdict'] == 'ACCEPT_SCOPED_DESKTOP_EXPOSITION_WITH_RETAINED_DEBT'
assert report['science_commit'] == SCI and report['integration_commit'] == HEAD
assert report['reviewer'] == ACTOR
preceding_outputs = [pin(path) for path in sorted(OUT.rglob('*')) if path.is_file()]
output_manifest = write('manifest.json', {'schema_version': 1, 'artifact_kind': 'native-exposition57-output-manifest', 'pins': preceding_outputs, 'preceding_output_count': len(preceding_outputs), 'self_hash_recipe': RECIPE, 'scope': 'Actual output snapshots, scripts, opened lease and prepared review/readbacks only. Later native run/complete/lease separately bind preceding artifacts. No recursive self-file byte pin.'})
run = write('reviewer.exposition.run.json', {'schema_version': 1, 'artifact_kind': 'native-independent-exposition-review-run', 'trusted_actor': ACTOR, 'scope': 'Independent scoped desktop ExpositionSeal57 only', 'science_commit': SCI, 'integration_commit': HEAD, 'verdict': report['verdict'], 'input_count': len(inputs), 'output_manifest': output_manifest, 'source_review_reused': pin(B / 'source-review57/result0.json'), 'source57_native_run_complete_minus_run_sha256': verification['source_run_complete_minus_run_sha256'], 'source57_named_publication_payload_sha256': verification['named_publication_binding_payload_sha256'], 'source57_publication_wrapper_complete_minus_content_self_sha256': verification['publication_binding_wrapper_complete_minus_content_self_sha256'], 'named_payload_is_not_native_run_hash': True, 'review': pin(OUT / 'exposition.review.json'), 'verification': pin(OUT / 'verification.json'), 'prepare_process': pin(OUT / 'prepare.process.status.json'), 'independent_viewed_images': 4, 'image_display_boundary': 'Four1440x1800 portable PNGs personally viewed through tool; display resized to1408x1760. No mobile/physical/live browser validation.', 'formula_steps': 6, 'all12_existing_gate_receipts_checked': True, 'counts': {'Registry': 498, 'root_jobs': 9160, 'Tests_jobs': 9449, 'focused_graph_nodes': 15, 'focused_graph_edges': 14}, 'independence': 'Reviewer did not create science57, source-review57 or root desktop visuals; full production/Test/source bodies now visible under separate exposition57 authorization. Original56 decoder source-text blindness remains historical.', 'no_new_compiler_or_browser': True, 'finalizer': {'script': pin(OUT / 'finalize_exposition.py'), 'pid': os.getpid(), 'mode': 'Synchronous foreground process; native tool return exit_code0 after final readbacks is authoritative.', 'no_spawned_or_detached_jobs': True, 'git_readonly_subprocess_exited': head_process.returncode}, 'native_hash_field': 'complete_object_sha256', 'native_hash_recipe': RECIPE, 'no_separately_named_run_payload': True})
native_run = json.loads(read(OUT / 'reviewer.exposition.run.json'))
run_complete_hash = native_run['complete_object_sha256']
complete = write('complete.json', {'schema_version': 1, 'artifact_kind': 'native-scoped-exposition57-completion', 'status': 'REVIEW_COMPLETE_PENDING_FINAL_LEASE_WRITE', 'science_commit': SCI, 'integration_commit': HEAD, 'run': run, 'run_COMPLETE_native_minus_complete_object_sha256': run_complete_hash, 'manifest': output_manifest, 'input_count': len(inputs), 'checked12_exit0': True, 'images4_independently_viewed': True, 'six_formula_steps_losslessly_bound': True, 'scoped_acceptance': True, 'full_reader_or_purified': False, 'final_lease_must_be_written_last': True, 'hash_recipe': RECIPE})
readbacks = []
for path in sorted(OUT.rglob('*')):
    if path.is_file():
        receipt = pin(path)
        assert pin(path) == receipt
        readbacks.append(receipt)
for entry in inputs:
    assert pin(entry['input']['path']) == entry['input']
closed = write('lease.json', {'schema_version': 1, 'artifact_kind': 'native-exposition57-resource-lease', 'trusted_actor': ACTOR, 'status': 'CLOSED', 'read': 'CLOSED', 'write': 'CLOSED', 'Python': 'CLOSED', 'compiler': 'NOT_STARTED_CLOSED', 'browser': 'NOT_STARTED_BY_REVIEWER_CLOSED', 'opened_lease': pin(OUT / 'lease.open.json'), 'closed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope': 'Own exposition-seal57 only. No canonical/Lean/site/ledger mutation, newcompiler, browser or background job. Historical56 decoder untouched.', 'actual_preparation_exit_code': 0, 'actual_preparation_exec_chunk': '127669', 'finalizer_pid': os.getpid(), 'finalizer_exit_evidence': 'Enclosing synchronous native tools.exec_command result following LAST write/readback supplies actual process exit. This finalizer has no outstanding file handles, children or asynchronous work; Python lifetime closes on normal return. CLOSED record is effective upon that observed exit0.', 'actual_read_resources': {'external_content_inputs': [entry['input'] for entry in inputs], 'own_preceding_artifacts_and_scripts': readbacks, 'git_reads': 'Science/integration blob snapshots in verification; finalizer readonly git rev-parse exited0.', 'prior_tool_reads': 'Bounded source/context filenames and file contents disclosed in input.manifest preparation_disclosure; four actual tool image views.'}, 'actual_write_resources': {'sole_write_root': str(OUT).replace('\\', '/'), 'output_readbacks_before_last_write': readbacks, 'last_output': 'lease.json', 'helper_scripts': [pin(OUT / 'prepare_exposition.py'), pin(OUT / 'finalize_exposition.py')], 'no_other_writes': True}, 'output_readback_count': len(readbacks), 'input_count': len(inputs), 'run': run, 'run_COMPLETE_native_minus_complete_object_sha256': run_complete_hash, 'complete': complete, 'self_hash_recipe': RECIPE, 'path_schema': 'Every actual locator is a native JSON string, not a PowerShell object.', 'closure_order': 'This CLOSED lease is the LAST filesystem write. Only native readback verification and stdout follow. Its raw/LF/bytes receipts are external stdout to avoid circular self-byte hashing.'})
# No filesystem mutation follows the final CLOSED lease write.
check = json.loads(read(OUT / 'lease.json'))
closure_complete_hash = check.pop('complete_object_sha256')
assert sha(canonical(check)) == closure_complete_hash
assert pin(OUT / 'lease.json') == closed
for entry in check['actual_read_resources']['external_content_inputs']:
    assert isinstance(entry['path'], str)
print(json.dumps({'status': 'CLOSED', 'scope_verdict': report['verdict'], 'science_commit': SCI, 'integration_commit': HEAD, 'actual_pid': os.getpid(), 'lease': closed, 'review': pin(OUT / 'exposition.review.json'), 'run': pin(OUT / 'reviewer.exposition.run.json'), 'input_count': len(inputs), 'output_readback_count': len(readbacks), 'counts': {'existing_gates_PASS': 12, 'screenshots_actually_viewed': 4, 'proof_formula_steps': 6, 'formula_containers': 8, 'initially_closed_details': 11, 'graph_nodes': 15, 'graph_edges': 14, 'Registry': 498, 'root_jobs': 9160, 'Tests_jobs': 9449}, 'complete_native_self_hashes': {'review': report['complete_object_sha256'], 'run': run_complete_hash, 'lease': closure_complete_hash}, 'compiler': 'NOT_STARTED_CLOSED', 'browser': 'NOT_STARTED_BY_REVIEWER_CLOSED', 'no_math_or_whole_goal_admission': True, 'foreground_normal_exit_requires_enclosing_tool_receipt': True}, ensure_ascii=False))
