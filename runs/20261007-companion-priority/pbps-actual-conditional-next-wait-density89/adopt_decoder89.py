from pathlib import Path
import hashlib, json, sys
R = Path('E:/Samplinglib')
r = Path(__file__).parent
d = R / 'runs/semantic-decoder-outputs/round89'
sys.path.insert(0, str(R / 'tools'))
import astis_semantic_roundtrip as rt
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
expected = {'reconstruction.json':'487e282c5bf604907f955f46876367800bd80dd41df1496f88f86caee89373a3', 'decoder-run.json':'e23422579f231a320534ef539e5b3a35064d5229892e1bf04c5c8184b7abaf41', 'manifest.json':'b17a4b4e161049b61647d2414f89d674b7aea6437895e8ecfcb53b6dd9901c58'}
for name, digest in expected.items():
    assert sha((d / name).read_bytes()) == digest, name
m = load(d / 'manifest.json')
n = load(d / 'reconstruction.json')
run = load(d / 'decoder-run.json')
packet = load(r / 'anonymous.decoder89.json')
for x in m['inputs'] + m['outputs']:
    b = Path(x['path']).read_bytes()
    assert len(b) == x['bytes'] and sha(b) == x['sha256'], x['path']
assert m['closed'] and m['input_set_closed'] and m['output_set_closed']
inp = run['input_reads'][0]
assert sha((r / 'anonymous.decoder89.json').read_bytes()) == inp['sha256'] == 'ebe974ffbf6cc0ed7d3fbab55dd1181689e798040c25164bc4263fd005af4b66'
assert packet['packet_sha256'] == rt.sha256_json({k:v for k,v in packet.items() if k != 'packet_sha256'})
assert not n['source_text_visible']
assert all(run['context_disclosure'][k] is False for k in ['source_text_visible','source_identity_visible','source_anchor_visible','declaration_identity_visible','proof_visible','source_review_visible','source_fidelity_verdict_visible'])
assert not run['context_disclosure']['extra_mathematical_inputs']
assert n['decoder_run_sha256'] == expected['decoder-run.json']
text = n['reconstructed_theorem_text']
assert sha(text.encode()) == n['reconstructed_text_sha256'] == m['reconstructed_text_utf8_sha256']
assert isinstance(n['semantic_uncertainties'], list) and len(n['semantic_uncertainties']) == 3
ap = R / 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json'
a = load(ap)
assert a['state'] == 'draft' and rt.decoder_packet(a) == packet
assert a['lean']['statement_sha256'] == m['statement_utf8_sha256']
snap = r / 'audit.before-decoder89.json'
assert not snap.exists()
snap.write_bytes(ap.read_bytes())
a.update(state='blind-reconstructed', reconstruction=dict(text=text, text_sha256=n['reconstructed_text_sha256'], decoder=n['decoder']['identity'], decoder_run_sha256=n['decoder_run_sha256'], decoder_packet_sha256=packet['packet_sha256'], source_text_visible=False, lean_statement_sha256=a['lean']['statement_sha256'], input_artifacts=packet['input_artifacts'], observed_input_artifacts=[dict(path=inp['path'],raw_sha256=inp['sha256'])], run_artifact=(d/'decoder-run.json').relative_to(R).as_posix(), native_named_payload_sha256=expected['reconstruction.json'], native_run_manifest_RAW_sha256=expected['manifest.json'], unresolved_semantics=[], native_semantic_uncertainties=n['semantic_uncertainties'], native_structured_payload=(d/'reconstruction.json').relative_to(R).as_posix(), run_hash_recipe='Exact native decoder-run.json bytes, neutral RAW input packet and independent native manifest. Embedded canonical packet hash independently checked; raw and canonical hashes intentionally differ. Native limitations retained verbatim, not source fidelity conclusions.'))
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
out = r/'root.decoder89.adoption.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='BLIND_RECONSTRUCTION_ADOPTED_ONLY',decoder=n['decoder']['identity'],native_manifest_RAW_sha256=expected['manifest.json'],packet_sha256=packet['packet_sha256'],canonical_sorted_json_complete_sha256=rt.sha256_json(packet),raw_packet_sha256=inp['sha256'],native_semantic_uncertainties_preserved=n['semantic_uncertainties'],classification='Native limitations concern approved hittingAfter semantics, no independent proof compile and raw/canonical metadata hash distinction. No unresolved theorem interpretation asserted; final source reviewer must assess all native text.',source_verdict=False,VERIFIED=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact native89 blind reconstruction adopted; no source-fidelity or VERIFIED credit.')
