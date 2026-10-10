from pathlib import Path
import hashlib, json, os, sys
root = Path.cwd(); sys.path.insert(0, 'tools')
import astis_semantic_roundtrip as rt, astis_publication as pub
r = root / 'runs/20261007-companion-priority/pbps-root-commutation67'
n = root / '.astis/decoder-67'; d = n / 'independent'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
can = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def pin(p):
    b = p.read_bytes()
    return dict(path=p.resolve().as_posix(), raw_bytes=len(b), raw_sha256=sha(b), lf_sha256=sha(b.replace(b'\r\n', b'\n')))
def write(p, x):
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
run, lease, payload = [load(d / k) for k in ['final_run.json', 'lease.json', 'reconstruction_payload.json']]
assert lease['status'] == 'CLOSED_LAST' and lease['last_owned_write']
assert sha((d / 'lease.json').read_bytes()) == '16ff8832b9726738a10cd37527f7c633a31e854d6476b58f53c24d1a91021729'
assert (d / 'lease.json').stat().st_mtime_ns >= max(p.stat().st_mtime_ns for p in d.iterdir() if p.is_file())
assert sha(can({k: v for k, v in run.items() if k != 'run_sha256'})) == run['run_sha256'] == lease['run_sha256'] == '22bd980f4390e913eb6ac12ba2fb98f5cb5c25d2de6e5f10e3d45dac6a2e3589'
named = sha((d / 'reconstruction_payload.json').read_bytes())
assert named == lease['reconstruction_payload_raw_sha256'] == 'fc7e5dc6beb3a11bb63fa0bb0362a3ca1acf04c73b581ce71a1a97393774cb71'
assert run['reconstructions'] == payload['reconstructions'] and len(payload['reconstructions']) == 2
for x in [run, lease, payload]:
    for k in ['source_text_visible', 'source_identity_visible', 'compiler_started']:
        assert x[k] is False
initial = (n / 'initial-lease.raw.snapshot.json').read_bytes()
assert initial == (n / 'lease.json').read_bytes() == (d / 'input.lease.raw.json').read_bytes()
assert sha(initial) == lease['initial_lease_raw_sha256'] and load(n / 'lease.json')['status'] == 'OPEN'
for key, file in [('closure_manifest_raw_sha256', 'closure_manifest.json'), ('self_manifest_raw_sha256', 'self_manifest.json'), ('terminal_manifest_raw_sha256', 'terminal_manifest.json'), ('final_run_raw_sha256', 'final_run.json')]:
    assert sha((d / file).read_bytes()) == lease[key]
rows = load(d / 'closure_manifest.json')['artifacts']
assert {p.name for p in d.iterdir()} == {x['path'] for x in rows} | {'closure_manifest.json', 'lease.json'} and len(list(d.iterdir())) == 25
for x in rows:
    b = (d / x['path']).read_bytes()
    assert len(b) == x['bytes'] and sha(b) == x['raw_sha256'], x['path']
for x in load(d / 'input_pin_map.json')['entries']:
    b = (d / x['raw_path']).read_bytes(); lf = b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    assert sha(b) == x['raw_sha256'] and sha(lf) == x['lf_sha256'] and lf == (d / x['lf_path']).read_bytes()
assert load(d / 'terminal_readback.json')['status'] == 'EXIT0'
assert load(d / 'terminal_readback.json')['readback_pid'] == 42628
assert load(d / 'finalizer_result.json')['status'] == 'EXIT0' and lease['close_pid'] == 28628
pub.inputs.cache_clear(); pub.load.cache_clear(); data = pub.inputs()
records = []
for i, (aid, slug) in enumerate([
    ('ASTIS-RT-20261009-RealL2PositiveSquareCommutation', 'real-l2-positive-square-commutation'),
    ('ASTIS-RT-20261009-PBPSActualRootInverseCommutation', 'pbps-actual-root-inverse-commutation')]):
    ap = root / 'research-wiki/semantic-roundtrip/audits' / f'{aid}.json'
    audit = load(ap); packet = load(n / f'packet{i}.json')
    assert audit['state'] == 'draft' and rt.decoder_packet(audit) == packet == load(r / f'anonymous.{i}.decoder.json')
    assert (n / f'packet{i}.json').read_bytes() == (d / f'input.packet{i}.raw.json').read_bytes()
    assert rt.sha256_json({k: v for k, v in packet.items() if k != 'packet_sha256'}) == packet['packet_sha256']
    item = next(x for x in pub.load() if x['id'] == slug)
    assert pub.binding_digest(item, item['bindings'][0], data) == audit['publication_binding_sha256']
    decoded = next(x for x in payload['reconstructions'] if x['packet_id'] == packet['packet_id'])
    assert sha(decoded['reconstructed_theorem_text'].encode()) == decoded['reconstructed_text_sha256']
    assert set(decoded['seven_slot_coverage']) == set(payload['semantic_slots']) and all(decoded['seven_slot_coverage'].values())
    assert all(decoded[k] for k in payload['semantic_slots'])
    records.append((i, ap, audit, packet, decoded))
dest = r / 'anonymous-decoder'; dest.mkdir(exist_ok=False); maps = []
for p in [*sorted(d.iterdir()), n / 'packet0.json', n / 'packet1.json', n / 'lease.json', n / 'initial-lease.raw.snapshot.json']:
    target = dest / ('parent-lease.open.json' if p == n / 'lease.json' else p.name)
    assert not target.exists(); target.write_bytes(p.read_bytes())
    maps.append(dict(original=pin(p), explicit_exact_raw_snapshot=pin(target)))
for i, ap, audit, packet, decoded in records:
    adapter = dest / f'decoded{i}.root-adapter.json'
    write(adapter, dict(native_payload=pin(dest / 'reconstruction_payload.json'), native_complete_payload=payload, selected_packet_id=packet['packet_id'], whole_logical_run_sha256=run['run_sha256'], native_named_payload_RAW_sha256=named, native_bytes_unchanged=True, actual_root_read_only_adopter_pid=os.getpid()))
    before = r / f'audit.{i}.before-decoder.exactraw.snapshot.json'
    assert not before.exists(); before.write_bytes(ap.read_bytes())
    audit.update(state='blind-reconstructed', reconstruction=dict(text=decoded['reconstructed_theorem_text'], text_sha256=decoded['reconstructed_text_sha256'], decoder='/root/anonymous_decoder64', decoder_run_sha256=run['run_sha256'], decoder_packet_sha256=packet['packet_sha256'], source_text_visible=False, lean_statement_sha256=audit['lean']['statement_sha256'], input_artifacts=['lean-statement', 'approved-definition-context'], observed_input_artifacts=[pin(dest / f'packet{i}.json')], run_artifact=adapter.relative_to(root).as_posix(), run_binding=(dest / 'lease.json').relative_to(root).as_posix(), native_named_payload_sha256=named, run_hash_recipe=run['run_hash_rule']))
    ap.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    write(r / f'source.{i}.reviewer-packet.json', rt.semantic_reviewer_packet(audit))
write(r / 'root.decoder67.adoption.json', dict(status='CLOSED_FRESH_ANONYMOUS_DECODER67_ADOPTED', actual_adopter_pid=os.getpid(), native_whole_run_sha256=run['run_sha256'], native_complete_named_RAW_sha256=named, native_owned_files=25, raw_snapshot_mappings=maps, original_draft_audit_snapshots=[pin(r / f'audit.{i}.before-decoder.exactraw.snapshot.json') for i in range(2)], source_text_visible=False, source_identity_visible=False, compiler_started=False, native_parent_lease_preserved_OPEN=True, source_verdict=False, VERIFIED_transition=False))
print('PASS closed blind decoder67:25 unchanged native files, both complete7-slot reconstructions, fresh source packets; source review pending.')
