from pathlib import Path
import hashlib, json, os

root = Path.cwd(); r = root / 'runs/20261007-companion-priority/pbps-centered-root-preproof64'
d = r / 'independent-primary64'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
lease, final, reader, cap, seal, api, regions = [load(d / n) for n in [
    'owned-lease.json', 'terminal-finalizer.json', 'terminal-readback.json',
    'bounded-source-api-capsule.json', 'source-first-graph-seal.json',
    'bounded-current-api-pins.json', 'primary-regions-receipt.json']]
assert lease['state'] == 'CLOSED_LAST' and lease['owner'] == '/root/preproof_centered64'
assert lease['no_more_owned_writes_authorized'] is True and lease['last_write'] == 'owned-lease.json'
assert sha((d / 'owned-lease.json').read_bytes()) == '3cd186d0b9e123bc9563ad3e265da8171233bcd9f00737c5d70c88f8d1ff55d4'
for name, key in [('terminal-finalizer.json', 'terminal_finalizer_sha256'),
                  ('terminal-readback.json', 'terminal_readback_sha256'),
                  ('bounded-source-api-capsule.json', 'capsule_sha256'),
                  ('bounded-source-api-synthesis.md', 'synthesis_sha256')]:
    assert sha((d / name).read_bytes()) == lease[key]
assert final['status'] == 'PASS' and reader['observed_finalizer_status'] == 'PASS'
assert reader['source_graph_unchanged'] is True and reader['all_checks_count'] == 6
assert final['statement_sealed_or_theorem_review_granted'] is False
owned = []
for q in final['artifacts']:
    p = d / q['name']; b = p.read_bytes()
    assert sha(b) == q['raw_sha256'] and len(b) == q['bytes'], p
    owned.append(p.resolve())
assert len(owned) == 101
assert {p.resolve() for p in d.rglob('*') if p.is_file()} == set(owned) | {
    d / 'terminal-finalizer.json', d / 'terminal-readback.json', d / 'owned-lease.json'}
assert sha((d / 'source-proof-graph.json').read_bytes()) == seal['graph_sha256'] == cap['source_graph_sha256']
assert sha((d / 'source-coverage-inventory.json').read_bytes()) == seal['coverage_sha256'] == cap['source_coverage_sha256']
assert not seal['candidate_read'] and not seal['theorem_review'] and not seal['statement_sealed']
assert seal['source_regions'] == 10 and seal['coverage_items'] == 1086 and seal['missing_alttext_count'] == 0
assert api['read_current_after_primary_graph_seal'] is True and api['no_Lean_authored_or_compile_run'] is True
pins = []
for q in api['files']:
    p = Path(q['path']); b = p.read_bytes(); z = b.replace(b'\r\n', b'\n')
    assert len(b) == q['bytes'] and sha(b) == q['raw_sha256'] and sha(z) == q['lf_sha256'], p
    assert Path(q['raw_snapshot']).read_bytes() == b and Path(q['lf_snapshot']).read_bytes() == z
    pins.append(q)
assert len(pins) == 23
primary = Path(regions['source']).read_bytes()
assert sha(primary) == regions['source_raw_sha256'] == cap['primary_source_raw_sha256'] == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for q in regions['regions']:
    a, b = q['byte_range_zero_based_half_open']; raw = primary[a:b]
    assert raw == Path(q['raw_file']).read_bytes() and sha(raw) == q['raw_sha256']
    assert raw.replace(b'\r\n', b'\n') == Path(q['lf_file']).read_bytes()
    assert sha(Path(q['lf_file']).read_bytes()) == q['lf_sha256']
    assert sha(Path(q['readable_file']).read_bytes()) == q['readable_sha256']
    assert sha(Path(q['alttext_file']).read_bytes()) == q['alttext_sha256']
    assert q['missing_alttext_count'] == 0
assert len(regions['regions']) == 10
parent = load(root / 'runs/20261007-companion-priority/pbps-macro-root63/root.exact-verification63.adoption.json')
assert parent['native_verified'] and parent['verified_commit'] == '4d02622332d02d0bd6c977d3cee48fd535ebf203'
out = r / 'root.primary64.adoption.json'; assert not out.exists()
out.write_text(json.dumps(dict(
    status='INDEPENDENT_PRIMARY64_BOUNDED_SOURCE_API_PROPOSAL_ADOPTED_NO_STATEMENT_SEAL',
    actual_root_reader_pid=os.getpid(), native_closed_owned_files=len(owned)+3,
    source_regions=10, source_inventory_items=1086, current_API_pins=23,
    graph_sha256=seal['graph_sha256'], coverage_sha256=seal['coverage_sha256'],
    capsule_RAW_sha256=lease['capsule_sha256'], native_lease_RAW_sha256=sha((d / 'owned-lease.json').read_bytes()),
    parent63_native_verified_commit=parent['verified_commit'],
    native_whole_run_hash_not_supplied=True,
    native_terminal_process_PID_or_exit_receipt_not_supplied=True,
    native_self_recorded_terminal_checks_not_a_Lean_or_science_gate=True,
    root_actual_closed_readback=True, proof_search_started=False,
    Statement_Seal=False, SAU_claim=False, theorem_or_source_verdict=False),
    ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
print('PASS root actual readback of CLOSED primary64 proposal:104 owned files,10 literal source regions,1086-item native inventory,23 fixed/current pins. No TYPE/Statement Seal/proof/source admission; native process-receipt/hash limits explicit.')
