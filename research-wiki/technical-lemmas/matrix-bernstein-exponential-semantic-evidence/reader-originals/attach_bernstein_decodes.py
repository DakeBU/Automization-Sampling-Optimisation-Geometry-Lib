"""Carry source-blind outputs verbatim; leave all source judgments to reviewer."""
from pathlib import Path
import hashlib, json
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
D = Path('.astis/semantic-neutral-20261114/anon_9b71')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
for p in sorted(D.rglob('*')):
    if p.is_file():
        assert not p.is_symlink() and '.private.' not in p.name
        create(E / 'decoder-originals/anon_9b71' / p.relative_to(D), p.read_bytes())
for label, dest in [('P', Path('research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json')),
                    ('T', W / 'private-consumer-audit.bound.v1.json')]:
    a = json.loads(dest.read_bytes())
    pkt = json.loads((D / ('input-' + label + '.json')).read_bytes())
    rp = D / 'output' / label / 'result.json'
    r = json.loads(rp.read_bytes())
    assert r['packet_sha256'] == pkt['packet_sha256']
    assert r['source_text_visible'] is False
    assert r['input_artifacts'] == ['lean-statement', 'approved-definition-context']
    assert sha(r['reconstructed_theorem_text'].encode()) == r['reconstructed_text_sha256']
    assert (D / 'output' / label / 'reconstruction.md').read_text() == r['reconstructed_theorem_text']
    reconstruction = {'text': r['reconstructed_theorem_text'], 'text_sha256': r['reconstructed_text_sha256'],
                      'decoder': r['decoder'], 'decoder_run_sha256': r['decoder_run_sha256'],
                      'decoder_packet_sha256': r['packet_sha256'], 'source_text_visible': False,
                      'lean_statement_sha256': a['lean']['statement_sha256'],
                      'input_artifacts': r['input_artifacts'],
                      'run_artifact': str(E / 'decoder-originals/anon_9b71/output' / label / 'result.json')}
    a['state'] = 'blind-reconstructed'
    a['reconstruction'] = reconstruction
    if label == 'P':
        dest.write_bytes(dump(a))
    else:
        create(W / 'private-consumer-audit.reconstructed.v1.json', dump(a))
        create(W / 'private-consumer-registry.reconstructed.v1.json', dump({'schema_version': 1, 'audits': [a]}))
print(json.dumps({'blind_decodes_attached': 2, 'new_source_verdicts': 0,
                  'canonical_packet_inputs': 'unchanged literal labels; physical custody separate'}))
