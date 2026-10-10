from pathlib import Path
import hashlib, json, os

base = Path('runs/20261007-companion-priority')
o = base / 'pbps-harmonic-flow-sourcegraph73'
pre = base / 'pbps-harmonic-flow-preproof73'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def check(z):
    b = Path(z['path']).read_bytes()
    assert len(b) == z['bytes'] and sha(b) == z['raw_sha256'], z['path']
    assert sha(b.replace(b'\r\n', b'\n')) == z['lf_sha256'], z['path']
    return b

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), RAW_bytes=len(b), RAW_sha256=sha(b), LF_sha256=sha(b.replace(b'\r\n', b'\n')))

lease = load(o / 'lease.final.json')
assert sha((o / 'lease.final.json').read_bytes()) == 'c57ff545394a24d4d8696f0148a3b160cec7f3cbd319c89ab11e8b2cf854eed9'
assert lease['state'] == 'CLOSED_LAST' and lease['actor'] == '/root/exact_science63'
assert lease['owned_count_including_lease'] == 49 and lease['read_only_probe_actual_exit_code'] == 0
rows = lease['all_files_except_self']
assert len(rows) == 48 and sha(can(rows)) == lease['closure_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()} == {Path(z['path']).resolve() for z in rows} | {(o / 'lease.final.json').resolve()}
for z in rows:
    check(z)
    assert Path(z['path']).stat().st_mtime_ns <= (o / 'lease.final.json').stat().st_mtime_ns
run = load(o / 'run.json')
h = sha(can({k: v for k, v in run.items() if k != 'run_sha256'}))
assert h == run['run_sha256'] == lease['whole_logical_run_sha256'] == '9626870ef809bfa53db37ffc586cc693179897afb239c3a26a90bc674353ed5f'
payload = load(run['complete_named_payload']['path'])
assert sha(check(run['complete_named_payload'])) == '7081797c0fab9e65f956d4283ed7b5ce23a3fbdb1bcab623fd303baec77b55d0'
for name, x in payload['content'].items():
    assert x == load(o / name), name
for name, x in payload['actual_native_terminals'].items():
    assert x == load(o / name), name
for z in payload['exact_content_raw_pins']:
    check(z)
inputs = load(run['complete_input_manifest']['path'])
assert inputs['input_count'] == len(inputs['inputs']) == 38
for z in inputs['inputs']:
    check(z)
graph = load(o / 'source-proof-graph.json')
coverage = load(o / 'source.coverage.json')
assert graph['node_count'] == 23 and graph['edge_count'] == 35 and graph['source_gap_count'] == 7
assert graph['independent_topology_review_status'] == 'PENDING_DISTINCT_REVIEWER'
assert graph['topology_source_only'] and not graph['implementation_header_or_proof_used']
assert (coverage['region_count'], coverage['block_count'], coverage['semantic_item_count'], coverage['node_dispositions'], coverage['excluded_dispositions']) == (13, 51, 79, 24, 55)
primary = check(graph['source_primary'])
for z in coverage['blocks']:
    a = z['literal_source_anchor']
    b = primary[a['raw_byte_start_inclusive']:a['raw_byte_end_exclusive']]
    assert len(b) == a['bytes'] and sha(b) == a['literal_span_raw_sha256']
    assert z['subitems'] and all(s['disposition'] in ['NODE', 'EXCLUDED'] for s in z['subitems'])
assert load(pre / 'root.source-first73.adoption.json')['native_owned_files'] == 103
p = pre / 'root.sourcegraph73.extraction-adoption.json'
assert not p.exists()
record = dict(status='ACCEPTED_IMMUTABLE_INDEPENDENT_SOURCEGRAPH73_EXTRACTION_NOT_TOPOLOGY_APPROVAL', actual_root_PID=os.getpid(), native_owned_files=49, finite_inputs=38, native_whole_logical_run_sha256=h, native_lease=pin(o / 'lease.final.json'), complete_named_payload=pin(o / 'complete-named-stageA-source-review.payload.json'), source_graph=pin(o / 'source-proof-graph.json'), source_coverage=pin(o / 'source.coverage.json'), binder_audit=pin(o / 'binder-audit.json'), regions=13, blocks=51, semantic_items=79, NODE=24, EXCLUDED=55, graph_nodes=23, graph_edges=35, source_gaps=7, independent_topology_review_pending=True, header_sealed=False, proof_search=False, compiler_proof=False, SAU_claimed=False, Goal_complete=False)
p.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('PASS73 immutable CLOSED49/38 input extraction; distinct topology/header review still pending.')
