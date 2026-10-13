from pathlib import Path
import hashlib, json, os

pre = Path('runs/20261007-companion-priority/pbps-harmonic-flow-preproof73')
o = pre / 'independent-header-math73'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def check(z):
    b = Path(z['path']).read_bytes()
    assert len(b) == z['RAW_bytes'] and sha(b) == z['RAW_sha256'], z['path']
    assert sha(b.replace(b'\r\n', b'\n')) == z['LF_sha256'], z['path']
    return b

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == '2aec2b262f447a7401fabb3108b109bf825bcef82dd258e87a2786a091a4d691'
assert lease['status'] == 'CLOSED_LAST' and lease['actor'] == '/root/exact_science63'
assert lease['file_count_including_lease'] == 90 and len(lease['files']) == 89
assert sha(can(lease['files'])) == lease['all_nonself_logical_manifest_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()} == {Path(z['path']).resolve() for z in lease['files']} | {(o / 'lease.final.json').resolve()}
for z in lease['files']:
    check(z)
    assert Path(z['path']).stat().st_mtime_ns <= (o / 'lease.final.json').stat().st_mtime_ns
run = load(o / 'run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['run_sha256'] == '079aa8fe5e122d1b4350b4a6bf98e742cf531800a09a708f455b233293ac9624'
assert run['status'] == 'ACCEPTED_PROSPECTIVE_HEADER_ONLY' and not run['proof_source_topology_and_VERIFIED_credit']
payload = load(run['complete_named_RAW_payload']['path'])
assert sha(check(run['complete_named_RAW_payload'])) == '36264fa99f62973048aae4f8f344d25c4f412153d63fc310f981c5d07880a9be'
decision = load(o / 'header.decision.json')
repair = load(o / 'repair-decision.json')
assert payload['frozen_header_decision'] == decision and payload['separate_two_edge_repair_decision'] == repair
assert payload['typecheck'] == run['fresh_typecheck']
assert decision['accepted_prospectively'] and decision['complete_nine_conjuncts'] and decision['same_six_original_callers']
assert decision['extra_public_premises'] == 0 and not decision['mathematical_repair_required']
assert decision['header_decision_frozen_before_any_distinct_overlay_review'] and not decision['source_topology_self_approval']
assert decision['fresh_typecheck_PID'] == 34940 and decision['fresh_typecheck_EXIT'] == 0
assert run['fresh_typecheck']['exit_code'] == 0 and run['fresh_typecheck']['terminal_closed']
assert not run['fresh_typecheck']['proof_search'] and not run['fresh_typecheck']['target_theorem_proved']
check(decision['exact_header'])
assert decision['exact_header']['RAW_sha256'] == 'a8a7f0f891906e4635d8b77046ee59ddcc3b3cbaeb37f22e6eff00d26b88a27d'
inputs = load(run['input_manifest']['path'])
assert inputs == payload['input_manifest'] and inputs['input_count'] == len(inputs['inputs']) == 27
for z in inputs['inputs']:
    b = check(z)
    if z.get('snapshot'):
        assert b == (o / z['snapshot']).read_bytes()
assert repair['accepted'] and repair['reviewer_distinct_from_overlay_author'] and repair['proposal_author'] == 'independent_primary69'
assert not repair['original_graph_coverage_self_approved'] and not repair['canonical_or_old_closed_graph_modified']
assert repair['no_new_formula_binder_Lean_provider_or_proof'] and repair['actual_review_PID'] == 47896
assert {(z['producer'], z['consumer']) for z in repair['two_edges']} == {('SCALE', 'GROUP'), ('ENERGY', 'ENERGY-NONNEG')}
assert all(z['accepted'] for z in repair['two_edges'])
check(repair['proposal'])
check(repair['header_math_decision_frozen_before_overlay'])
p = pre / 'root.header-math73.adoption.json'
assert not p.exists()
record = dict(status='ACCEPTED_PROSPECTIVE_HEADER_MATH73_AND_DISTINCT_TWO_EDGE_REPAIR_ONLY', actual_root_PID=os.getpid(), native_owned_files=90, finite_inputs=27, native_whole_logical_run_sha256=h, native_lease=pin(o / 'lease.final.json'), complete_named_payload=pin(o / 'complete-named-header-review.payload.json'), exact_header=pin(pre / 'header73.proposed.lean'), header_decision=pin(o / 'header.decision.json'), separate_two_edge_repair=pin(o / 'repair-decision.json'), no_mathematical_header_repair=True, source_topology_full_admission=False, header_sealed=False, proof_search=False, compiler_proof=False, SAU_claimed=False, VERIFIED=False, Goal_complete=False)
p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS73 prospective header math CLOSED90/27 and distinct two-edge repair only; whole source-topology/seal/proof admission pending.')
