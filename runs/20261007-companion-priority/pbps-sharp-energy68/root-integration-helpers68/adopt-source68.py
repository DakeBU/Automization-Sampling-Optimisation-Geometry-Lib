from pathlib import Path
import hashlib, json, os, sys
root = Path.cwd()
sys.path.insert(0, 'tools')
import astis_publication as pub, astis_semantic_roundtrip as rt
r = root / 'runs/20261007-companion-priority/pbps-sharp-energy68'
d = r / 'independent-source68'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def check(b, row):
    assert len(b) == row['RAW_bytes'] and sha(b) == row['RAW_sha256']
    lf = b.replace(b'\r\n', b'\n')
    assert sha(lf) == row['LF_sha256']
    if 'LF_bytes' in row:
        assert len(lf) == row['LF_bytes']
def pin(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(root).as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b),
                LF_sha256=sha(b.replace(b'\r\n', b'\n')))
lease = load(d / 'lease.final.json')
assert sha((d / 'lease.final.json').read_bytes()) == 'e5962c11b38f64e3d782175c959e2c25c4b5e2bcad750eaf963cf4f547c89aeb'
assert lease['status'] == 'CLOSED_LAST' and lease['total_owned_file_count_including_manifest_and_final_lease'] == 363
assert lease['last_owned_write'].startswith('lease.final.json;') and lease['actual_closing_pid'] == 23300
for key in ['complete_named_RAW_review', 'complete_named_RAW_decision', 'complete_named_RAW_input_payload', 'owned_manifest']:
    check((d / lease[key]['path']).read_bytes(), lease[key])
manifest = load(d / 'owned-manifest.json')
rows = manifest['all_regular_owned_files_excluding_manifest_self_and_final_lease']
assert len(rows) == 361 and sha(can(rows)) == lease['owned_rows_canonical_sha256']
files = {p.relative_to(d).as_posix(): p for p in d.rglob('*') if p.is_file()}
assert len(files) == 363 and set(files) == {row['path'] for row in rows} | {'owned-manifest.json', 'lease.final.json'}
for row in rows:
    check(files[row['path']].read_bytes(), row)
assert (d / 'lease.final.json').stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in files.values())
run = load(d / 'review-run.json')
assert sha(can({k:v for k,v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['whole_logical_run_sha256'] == 'e987d89be0647776605af9fdd96c49ce309355540bf927823ae1fda9f7d534ce'
assert run['decisions_count'] == 3 and run['semantic_slot_count'] == 21
payload = load(d / 'complete-RAW-input-payload.json')
assert payload['entry_count'] == len(payload['entries']) == 146
for row in payload['entries']:
    original, raw, lf = root / row['source_path'], d / row['raw_snapshot'], d / row['lf_snapshot']
    b = original.read_bytes()
    check(b, row)
    assert raw.read_bytes() == b and lf.read_bytes() == b.replace(b'\r\n', b'\n')
    if row['original_header_path']:
        assert (root / row['original_header_path']).read_bytes() == b
coverage = load(d / 'source-coverage-and-stage-order.audit.json')
assert coverage['item_count'] == 344 and coverage['missing_items'] == 0 and len(coverage['six_regions']) == 6
assert not coverage['whole_paper_coverage_claim'] and not coverage['prior67_final_verdict_read']
assert coverage['source_expectations']['RAW_sha256'] == 'ced1c679be92f94e8fa0edd8ed06935c5ef5dace0596f0e8b547a6d019afa997'
body = load(d / 'eleven-literal-BODY-spans.readback.json')
assert len(body['steps']) == 11
for item in body['steps']:
    region = item['region']
    module = (root / region['path']).read_bytes()
    assert sha(module) == region['source_raw_sha256']
    lesson = load(root / 'website/content/declaration_lessons' / (item['lesson'] + '.json'))['units'][0]
    step = lesson['steps'][item['step'] - 1]
    code = step['lean'].encode()
    assert sha(code) == region['exact_code_raw_sha256'] and len(code) == item['raw_code_bytes']
    assert module.count(code) == 1
    start = module.index(code)
    assert module[:start].count(b'\n') + 1 == region['start_line']
    assert code.endswith(b'\n')
    assert module[:start + len(code)].count(b'\n') == region['end_line']
    public_start = module.index(b'\ntheorem ')
    proof_start = module.index(b':= by', public_start)
    assert proof_start < start < module.rindex(b'\nend')
    assert item['exact_BODY_code'] and item['before_module_end_and_after_public_proof_start']
pub.inputs.cache_clear()
pub.load.cache_clear()
data, plan = pub.inputs(), load(r / 'publication-plan.json')
bindings = []
for i, key in enumerate(['0', '1', 'consumer']):
    decision = load(d / f'source.{key}.decision.json')
    packet = load(r / f'source.{key}.reviewer-packet.json')
    audit = load(root / 'research-wiki/semantic-roundtrip/audits' / (plan['audit_ids'][i] + '.json')) if i < 2 else load(r / 'consumer.semantic-audit68.blind.json')
    assert rt.semantic_reviewer_packet(audit) == packet
    assert packet['packet_sha256'] == decision['reviewer_packet_sha256']
    assert sha((r / f'source.{key}.reviewer-packet.json').read_bytes()) == decision['reviewer_packet_RAW_sha256']
    assert decision['verdict'] == 'equivalent-after-elaboration' and not decision['repairs'] and not decision['blocking_deltas']
    assert decision['independent_from_formalizer'] and decision['independent_from_decoder']
    assert set(decision['semantic_slots']) == set(rt.SEMANTIC_SLOTS)
    assert all(slot['evidence'] and slot['relation'] != 'not-audited' for slot in decision['semantic_slots'].values())
    assert len(decision['deltas']) == 5 and all(delta['blocking'] is False for delta in decision['deltas'])
    assert decision['review_run_sha256'] == run['run_sha256']
    if i < 2:
        item = next(item for item in pub.load() if item['id'] == plan['slugs'][i])
        assert pub.binding_digest(item, item['bindings'][0], data) == audit['publication_binding_sha256'] == decision['publication_binding_sha256']
        assert pub.digest(pub.review_context(item, item['bindings'][0], data)) == decision['candidate_context_canonical_sha256']
    else:
        assert sha(can(audit['publication_context'])) == audit['publication_binding_sha256'] == decision['publication_binding_sha256'] == decision['candidate_context_canonical_sha256']
    assert not decision['full_Exposition_Seal'] and not decision['PURIFIED'] and not decision['VERIFIED_transition_claim']
    bindings.append(dict(key=key, packet_sha256=packet['packet_sha256'],
        publication_binding_sha256=decision['publication_binding_sha256'],
        publication_context_sha256=decision['candidate_context_canonical_sha256'],
        native_decision=pin(d / f'source.{key}.decision.json')))
terminals = lease['actual_terminal_receipts']
for name, pid in [('validation68.v3.terminal.json',20500), ('author68.v2.terminal.json',43732), ('final-native-readback68.terminal.json',14120)]:
    assert terminals[name]['actual_child_pid'] == pid and terminals[name]['actual_exit_code'] == 0
assert terminals['validation68.v2.terminal.json']['actual_exit_code'] == 1
out = r / 'root.source68.adoption.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_SOURCE68_ACCEPTED_SELECTED_BOUNDARIES',
    actual_read_only_adopter_pid=os.getpid(), native_owned_files=363,
    native_whole_logical_run_sha256=run['run_sha256'],
    native_complete_RAW_review_sha256=lease['complete_named_RAW_review']['RAW_sha256'],
    native_complete_RAW_decision_sha256=lease['complete_named_RAW_decision']['RAW_sha256'],
    separate_complete_RAW_input_sha256=lease['complete_named_RAW_input_payload']['RAW_sha256'],
    native_lease=pin(d / 'lease.final.json'), finite_current_input_entries=146,
    source_items=344, source_regions=6, literal_BODY_steps=11, semantic_slots=21,
    decisions=bindings, negative_v2_validation_preserved=True,
    closing_pid_external_EXIT0=23300, postclose_read_only_pid_external_EXIT0=33448,
    source_mathematical_repair=False, canonical_schema_adapter_pending=True,
    full_Exposition=False, PURIFIED=False, VERIFIED=False, Goal_complete=False),
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS source68 CLOSED363:146 exact current RAW/LF inputs,344 source nodes,11 BODY steps,3 packets and21 slots; no mathematical repair or full-Exposition claim.')
