from pathlib import Path
import hashlib, json, os, datetime

root = Path.cwd()
pre = root / 'runs/20261007-companion-priority/pbps-centered-root-preproof64'
n = pre / 'independent-header64'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def pin(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), bytes=len(b), raw_sha256=sha(b),
                lf_sha256=sha(b.replace(b'\r\n', b'\n')))
def write(p, x):
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
def inventory_check(entries, base):
    for e in entries:
        b = (base / e['name']).read_bytes()
        assert len(b) == e['bytes'] and sha(b) == e['raw_sha256'], e['name']

lease = load(n / 'owned-lease.json')
review = load(n / 'independent-header64.review.json')
digests = load(n / 'review-digests.json')
assert lease['state'] == lease['event'] == 'CLOSED_LAST'
assert sha((n / 'owned-lease.json').read_bytes()) == 'f92f0ba11d299898d3dc5dc21555e65da01b8dd028d33fa8a374d360cc4aff13'
logical = {k:v for k,v in review.items() if k != 'run_sha256'}
assert sha(canonical(logical)) == review['run_sha256'] == digests['run_sha256'] == 'b213a9fc385d4b548e7d3168ee73dbe3306088e5ba3ddc88bbe5141e6c264223'
assert sha((n / digests['named_payload']).read_bytes()) == digests['full_named_RAW_payload_sha256'] == 'a5ec0efd329fc07d5b406d965dc109bb90cf73730350ce40df4bb1d63b3352c0'
assert sha((n / 'independent-header64.review.md').read_bytes()) == digests['report_raw_sha256']
inventory_check(lease['owned_outputs'], n)
actual = {p.relative_to(n).as_posix() for p in n.rglob('*') if p.is_file()}
assert actual == {q['name'] for q in lease['owned_outputs']} | {'owned-lease.json'}
assert len(actual) == 60
assert sha(canonical(lease['owned_outputs'])) == lease['owned_outputs_logical_manifest_sha256']
for label, filename in [('finalizer','terminal-finalizer.json'),('readback','terminal-readback.json')]:
    evidence = load(n / filename); receipt = load(n / (label + '.process-receipt.json'))
    inventory_check(evidence['owned_manifest'], n)
    assert receipt['actual_exit_code'] == 0 and receipt['terminal_closed']
    assert receipt['actual_child_pid'] == evidence['actual_pid']
    for ext in ['stdout','stderr']:
        assert sha((n / (label+'.'+ext+'.txt')).read_bytes()) == receipt[ext+'_raw_sha256']
    assert sha((n / filename).read_bytes()) == lease['terminal_'+label+'_raw_sha256']
    assert lease['actual_foreground_processes'][label]['receipt_raw_sha256'] == sha((n / (label+'.process-receipt.json')).read_bytes())
exact = load(n / 'exact-header-input-pins.json')
for q in exact['files']:
    current = pin(q['path'])
    assert all(current[k] == q[k] for k in ['bytes','raw_sha256','lf_sha256'])
assert [q['raw_sha256'] for q in exact['files'][:2]] == [
    'e47db63e47e177698eda425514dfdb511ecce4742f6a091c24fca0ed2f3461ee',
    '28460b7230b6122deb9ef57020e82cf34cecfeb6cc908bf03eee2ef96b717f89']
support = load(n / 'bounded-diagnostic-support-inputs.json')
for q in support['fixed_support_inputs']:
    current = pin(q['path'])
    assert all(current[k] == q[k] for k in ['bytes','raw_sha256','lf_sha256'])
    assert sha((n / q['raw_snapshot']).read_bytes()) == q['raw_sha256']
    assert sha((n / q['lf_snapshot']).read_bytes()) == q['lf_sha256']
reread = load(n / 'primary-before-header-reread-receipt.json')
primary_dir = pre / 'independent-primary64'
inventory_check(reread['primary64_immutable_outputs'], primary_dir)
primary = Path(reread['primary_source']).read_bytes()
assert sha(primary) == reread['primary_source_raw_sha256']
for q in reread['regions']:
    a,b = q['byte_range_zero_based_half_open']
    assert sha(primary[a:b]) == q['raw_sha256']
coverage = load(primary_dir / 'source-coverage-inventory.json')
assert coverage['unclassified_count'] == 0 and len(coverage['inventory']) == 1086
for q in coverage['inventory']:
    a,b = q['byte_range_zero_based_half_open']
    assert sha(primary[a:b]) == q['literal_sha256']
source_process = load(n / 'source-reread.process-receipt.json')
assert source_process['actual_exit_code'] == 0 and source_process['terminal']
for ext in ['stdout','stderr']:
    assert sha((n / ('source-reread.'+ext+'.txt')).read_bytes()) == source_process[ext+'_raw_sha256']
assert source_process['end_utc'] < min(q['first_exact_read_utc'] for q in exact['files'])
assert not reread['exact_header0_or_header1_received_or_read']
source_seal = load(n / 'pre-header-source-seal.json')
assert sha((n / 'pre-header-source-seal.json').read_bytes()) == exact['pre_header_source_seal_sha256']
assert sha((primary_dir / 'source-proof-graph.json').read_bytes()) == source_seal['source_graph_sha256']
assert sha((primary_dir / 'source-coverage-inventory.json').read_bytes()) == source_seal['source_coverage_sha256']
assert all(review['verdict'][h] == 'ACCEPT_FOR_ROOT_PREPROOF_STATEMENT_SEAL_CONSIDERATION' for h in ['header0','header1'])
assert not review['verdict']['blocking_semantic_deltas'] and not review['verdict']['mathematical_repair_overlay_required']
parent_path = root / 'runs/20261007-companion-priority/pbps-macro-root63/root.exact-verification63.adoption.json'
parent = load(parent_path)
assert parent['native_verified'] and parent['verified_commit'] == review['inspected_science_commit'] == '4d02622332d02d0bd6c977d3cee48fd535ebf203'
types = load(pre / 'root.named-types64.adoption.json')
assert types['status'] == 'TWO_FULL_NAMED64_TYPES_ELABORATED_NO_PROOF_NO_STATEMENT_SEAL'
adoption = dict(status='NATIVE_HEADER64_SOURCE_FIRST_REVIEW_ADOPTED', actual_root_reader_pid=os.getpid(),
    owned_native_files=60, immutable_primary_files=len(reread['primary64_immutable_outputs']),
    source_literal_inventory=1086, current_support_pins=len(support['fixed_support_inputs']),
    native_lease=pin(n / 'owned-lease.json'), native_review=pin(n / 'independent-header64.review.json'),
    named_full_RAW_payload=pin(n / digests['named_payload']), whole_logical_run_sha256=review['run_sha256'],
    native_actual_foreground_processes=lease['actual_foreground_processes'],
    primary_first_causality=True, mathematical_truth_granted=False, native_artifacts_rewritten=False)
write(pre / 'root.header64.adoption.json', adoption)
write(pre / 'root.statement-seal64.json', dict(status='STATEMENT64_SEALED_NOT_PROVED_NOT_CLAIMED',
    utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), actual_root_sealer_pid=os.getpid(),
    headers=[pin(pre / f'header{i}.lean') for i in range(2)],
    independent_review_adoption=pin(pre / 'root.header64.adoption.json'),
    whole_logical_run_sha256=review['run_sha256'], source_graph=pin(primary_dir / 'source-proof-graph.json'),
    source_coverage=pin(primary_dir / 'source-coverage-inventory.json'),
    named_type_adoption=pin(pre / 'root.named-types64.adoption.json'),
    verified_parent63_adoption=pin(parent_path), parent63_verified_commit=parent['verified_commit'],
    scope='Printed B15 order on the exact centered macro domain plus derived actual bounded inverse and its norm, a genuine B16 input. Full macro inverse, B16 polar, H1 and dynamics excluded.',
    internal_debt='Three canonical complex lifts; square-root monotonicity; actual C4 production assembly without Test imports; constant projection; centered restriction; derived unit/inverse/norm.',
    proof_search_started=False, theorem_admitted=False, Goal_complete=False))
print('PASS:60 CLOSED native outputs,104 primary outputs,1086 literal source items and source-first causality; exact headers64 Statement Sealed; no claim/proof/theorem admission.')
