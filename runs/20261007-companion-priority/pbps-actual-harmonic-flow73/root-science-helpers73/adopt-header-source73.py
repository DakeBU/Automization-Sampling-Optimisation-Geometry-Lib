from pathlib import Path
import hashlib, json, os

pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
own = pre / 'independent-header-source73'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

def check(z):
    b = Path(z['path']).read_bytes()
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], z['path']
    assert sha(b.replace(b'\r\n', b'\n')) == z['LF_sha256'], z['path']
    return b

lease_path = own / 'lease.final.json'
assert sha(lease_path.read_bytes()) == 'd29689c7071e0ff35cfcfec6e303d090763d24b1c8cd12f984cd6c3eea59872c'
lease = load(lease_path)
assert lease['status'] == 'CLOSED_LAST' and lease['actual_close_pid'] == 38144 and lease['exit_code'] == 0 and not lease['background']
members = lease['all_files_except_self']
assert lease['member_count_except_self'] == len(members) == 51 and lease['owned_file_count_including_self'] == 52
assert {p.resolve() for p in own.rglob('*') if p.is_file()} == {Path(z['path']).resolve() for z in members} | {lease_path.resolve()}
for z in members:
    b = Path(z['path']).read_bytes()
    assert len(b) == z['bytes'] and sha(b) == z['raw_sha256'] and sha(b.replace(b'\r\n', b'\n')) == z['lf_sha256']
    assert Path(z['path']).stat().st_mtime_ns <= lease_path.stat().st_mtime_ns
manifest = json.loads(check(lease['whole_owned_manifest']))
assert manifest['count'] == len(manifest['files']) == 50
assert manifest['files'] == [z for z in members if z['path'] != lease['whole_owned_manifest']['path']]
run = load(own / 'run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['whole_logical_run_sha256'] == '0ce9bfaeda1bf2a573d606ee3d3d8beff7cd7a17fce7f511545233c8dd26b7ca'
assert run['reviewer'] == '/root/independent_primary69' and run['no_proof_compile_VERIFIED_or_fullpaper_credit']
payload_path = own / 'complete-named-review-decision-input-payload.json'
assert sha(payload_path.read_bytes()) == '5fdba896df782a8eb0b1fca7a59bcf525da7951de474131b58a8e63dbebd35d4'
payload = load(payload_path)
assert payload['whole_logical_run_sha256'] == h and payload['named_payload_count'] == len(payload['named_payloads']) == 4
for z in payload['named_payloads']:
    assert z['complete_RAW_UTF8'].encode() == check(z['pin'])
inputs = json.loads(check(run['input_manifest']))
assert inputs['input_count'] == len(inputs['inputs']) == 29
for z in inputs['inputs']:
    check(z)
for z in run['terminal_receipts']:
    t = json.loads(check(z))
    assert t['actual_pid'] > 0 and t['exit_code'] == 0 and t['background'] is False
assert len(run['terminal_receipts']) == 5
decision = json.loads(check(run['decision']))
assert decision['verdict'] == 'ACCEPT_SOURCE_TOPOLOGY_AND_PROSPECTIVE_HEADER_SEAL_READY'
assert decision['blocking_header_repairs'] == []
check(decision['header'])
assert decision['header']['RAW_sha256'] == 'a8a7f0f891906e4635d8b77046ee59ddcc3b3cbaeb37f22e6eff00d26b88a27d'
assert decision['exposure']['73_expectations_frozen_before_header_or_hash'] and not decision['exposure']['other73_header_math_decision_or_full_payload_read']
assert not decision['independent_graph_repair']['my_proposal_self_approved']
assert decision['coverage'] == dict(source_regions=13, source_blocks=51, semantic_items=79, NODE=24, EXCLUDED=55, nodes=23, edges_original=35, edges_after_distinct_overlay=37, SOURCE_GAP=7, semantic_binders=20, SOURCE=4, STANDING=6, TYPING=10, EXCESS=0, conjuncts=9, six_private_public_caller_prefixes_exact_equal=True)
graph = json.loads(check(decision['source_topology']))
original = json.loads(check(graph['original_graph']))
assert graph['nodes'] == original['nodes'] and graph['edges'][:35] == original['edges']
assert len(graph['nodes']) == 23 and len(graph['edges']) == 37 and graph['source_gap_count'] == 7
assert {(z['producer'], z['consumer']) for z in graph['edges'][35:]} == {('SCALE', 'GROUP'), ('ENERGY', 'ENERGY-NONNEG')}
repair = json.loads(check(decision['independent_graph_repair']['decision']))
assert repair['accepted'] and repair['reviewer_distinct_from_overlay_author'] and not repair['original_graph_coverage_self_approved']
math_adoption = load(pre / 'root.header-math73.adoption.json')
assert math_adoption['no_mathematical_header_repair'] and math_adoption['exact_header']['RAW_sha256'] == decision['header']['RAW_sha256']
record = dict(status='ACCEPTED_INDEPENDENT_SOURCE_TOPOLOGY73_AND_PROSPECTIVE_HEADER_ONLY', actual_root_PID=os.getpid(), native_owned_files=52, finite_inputs=29, whole_logical_run_sha256=h, native_lease=pin(lease_path), complete_named_payload=pin(payload_path), decision=run['decision'], exact_header=decision['header'], source_graph=decision['source_topology'], coverage=decision['coverage'], independent_two_edge_repair=decision['independent_graph_repair']['decision'], source_blind=False, anti_anchored=True, header_sealed=False, proof=False, SAU_claimed=False, VERIFIED=False, Goal_complete=False)
out = pre / 'root.header-source73.adoption.json'
assert not out.exists()
out.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS73 independent source CLOSED52/29; exact prospective header accepted; original23/35 + distinct2 source edges; seven proof gaps remain.')
