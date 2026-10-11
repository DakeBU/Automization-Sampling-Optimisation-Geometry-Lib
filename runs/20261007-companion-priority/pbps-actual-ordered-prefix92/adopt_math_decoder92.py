from pathlib import Path
import hashlib, json, sys

ROOT = Path('E:/Samplinglib')
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tools'))
import astis_semantic_roundtrip as rt

sha = lambda b: hashlib.sha256(b).hexdigest()
read = lambda p: json.loads(p.read_bytes())
def write_new(p, data):
    assert not p.exists(), p
    p.write_bytes((json.dumps(data, ensure_ascii=False, indent=2)+'\n').encode())

math_dir = RUN / 'independent-math92'
math_manifest = math_dir / 'closed-RAW92.native.json'
assert sha(math_manifest.read_bytes()) == '460d9eaf73dfc1ba1d193ecd2d747557f0d0fc421c80d1ad56a638000c98fd09'
m = read(math_manifest)
for x in m['inputs'] + m['outputs']:
    b = Path(x['path']).read_bytes()
    assert sha(b) == x['raw_sha256'] and len(b) == x['bytes'], x['path']
math_result = read(math_dir / 'production-math-review92.native.json')
assert math_result['decision'] == 'ACCEPT_FROZEN_PRODUCTION_MATHEMATICS_AND_KERNEL'

out = ROOT / 'runs/semantic-roundtrip/anonymous92/decoder'
closed = out / 'closed-RAW.native.json'
assert sha(closed.read_bytes()) == 'f33d4de61c881fee245788a22b745c6bd2721d2f29c3dbd771c9e5aaed8e3051'
d = read(closed)
for name, h in d['output_hashes'].items():
    assert sha((out/name).read_bytes()) == h
n = read(out/'decoder-result.native.json')
assert not n['source_text_visible'] and not d['source_text_visible']
assert n['run_manifest'] == d['run_manifest']
assert rt.sha256_json(n['run_manifest']) == n['decoder_run_sha256'] == d['decoder_run_sha256']
packet_path = ROOT/'runs/semantic-roundtrip/anonymous92/input.json'
packet = read(packet_path)
assert sha(packet_path.read_bytes()) == n['input_raw_sha256'] == d['input_raw_sha256']
assert packet['packet_sha256'] == rt.sha256_json({k:v for k,v in packet.items() if k != 'packet_sha256'}) == n['packet_sha256']
text = (out/'reconstruction.md').read_bytes().decode()
assert sha(text.encode()) == n['reconstructed_text_sha256']
ap = ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json'
a = read(ap)
assert a['state'] == 'draft' and rt.decoder_packet(a) == packet
write_new(RUN/'audit.before-adoption92.json', a)
a['lean']['statement_representation'].update(
    kernel_header_and_literal_expansion_checked=True,
    independent_kernel_evidence=(math_dir/'production-math-review92.native.json').relative_to(ROOT).as_posix())
a.update(state='blind-reconstructed', reconstruction=dict(
    text=text, text_sha256=n['reconstructed_text_sha256'], decoder='/root/blind_decoder92',
    decoder_run_sha256=n['decoder_run_sha256'], decoder_packet_sha256=packet['packet_sha256'],
    source_text_visible=False, lean_statement_sha256=a['lean']['statement_sha256'],
    input_artifacts=packet['input_artifacts'],
    observed_input_artifacts=[dict(path=packet_path.relative_to(ROOT).as_posix(),raw_sha256=n['input_raw_sha256'])],
    run_artifact=(out/'decoder-result.native.json').relative_to(ROOT).as_posix(),
    native_named_payload_sha256=d['output_hashes']['decoder-result.native.json'],
    native_run_manifest_RAW_sha256=sha(closed.read_bytes()),
    native_structured_payload=(out/'decoder-result.native.json').relative_to(ROOT).as_posix(),
    native_semantic_slots={k:n[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']},
    run_hash_recipe='Canonical SHA256 of the embedded run_manifest object in decoder-result.native.json: sorted-key compact JSON, ensure_ascii=False, UTF8, no trailing newline. This is not the raw artifact hash. Full native reconstruction retained, including scope and limitations.'))
assert rt.decoder_packet(a) == packet
review = rt.semantic_reviewer_packet(a)
ap.write_bytes((json.dumps(a,ensure_ascii=False,indent=2)+'\n').encode())
write_new(RUN/'root.math92.adoption.json',dict(status='INDEPENDENT_MATH_KERNEL_ONLY',
    native_manifest_raw_sha256=sha(math_manifest.read_bytes()), inputs_and_outputs_rehashed=len(m['inputs'])+len(m['outputs']),
    source_verdict=False, exact_commit_verified=False, VERIFIED=False))
write_new(RUN/'root.decoder92.adoption.json',dict(status='BLIND_RECONSTRUCTION_ONLY',
    native_manifest_raw_sha256=sha(closed.read_bytes()), canonical_packet_sha256=packet['packet_sha256'],
    embedded_run_manifest_canonical_sha256=n['decoder_run_sha256'], source_verdict=False, VERIFIED=False))
write_new(RUN/'anti-anchored.review92.json',review)
print(json.dumps(dict(status='adopted math and blind reconstruction only',review_packet=review.get('packet_sha256'),review_raw=sha((RUN/'anti-anchored.review92.json').read_bytes()))))
