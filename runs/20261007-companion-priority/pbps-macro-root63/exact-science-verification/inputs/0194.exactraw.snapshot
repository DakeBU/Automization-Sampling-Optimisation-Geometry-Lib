import hashlib, json, os, sys
from pathlib import Path

OUT = Path('E:/Samplinglib/.astis/decoder-60/independent')
def canonical(v): return json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
def sha(v): return hashlib.sha256(v).hexdigest()
def load(name): return json.loads((OUT / name).read_bytes())
checks = []
manifest = load('input-manifest.json')
for entry in manifest['inputs']:
    path = OUT / 'initial-lease.json' if entry['path'].endswith('lease.json') else Path(entry['path'])
    raw = path.read_bytes()
    assert sha(raw) == entry['raw_sha256']
    assert sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == entry['lf_sha256']
    obj = json.loads(raw)
    assert sha(canonical(obj)) == entry['canonical_json_sha256']
    if 'canonical_decoder_packet_sha256' in entry:
        assert sha(canonical({k:v for k,v in obj.items() if k != 'packet_sha256'})) == entry['canonical_decoder_packet_sha256']
        assert sha(obj['lean']['statement'].encode('utf-8')) == entry['statement_sha256']
    checks.append({'input': entry['path'], 'byte_and_canonical_hashes': 'PASS'})
payload = load('decoder-payload.json')
assert sha(canonical(payload['payload'])) == payload['payload_sha256']
for n in ['decoded0.json', 'decoded1.json']:
    obj = load(n)
    assert sha(obj['reconstructed_theorem_text'].encode('utf-8')) == obj['reconstructed_text_sha256']
    assert obj['decoder_run_sha256'] == payload['payload_sha256']
    assert obj['decoder'] == '/root/anonymous_decoder60'
    assert obj['source_text_visible'] is False and obj['source_identity_visible'] is False
    assert all(obj[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'])
    checks.append({'output': n, 'reconstruction_and_seven_slots': 'PASS', 'raw_sha256': sha((OUT/n).read_bytes()), 'reconstructed_text_sha256':obj['reconstructed_text_sha256']})
if '--final' in sys.argv:
    run = load('run.json')
    assert sha(canonical({k:v for k,v in run.items() if k != 'run_sha256'})) == run['run_sha256']
    for output in run['outputs']:
        assert sha((OUT/output['filename']).read_bytes()) == output['raw_sha256']
    checks.append({'output': 'run.json', 'native_whole_run_hash': 'PASS', 'run_sha256': run['run_sha256']})
print(json.dumps({'pid':os.getpid(), 'status':'PASS', 'checks':checks}, ensure_ascii=False))
