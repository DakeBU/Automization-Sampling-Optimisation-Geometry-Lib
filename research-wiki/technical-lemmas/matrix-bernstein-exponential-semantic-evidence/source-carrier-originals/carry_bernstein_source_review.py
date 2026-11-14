"""Carry independent source originals; no normal state transition or self-verification."""
from pathlib import Path
import hashlib, json, subprocess, tarfile, sys
sys.path.insert(0, 'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
S = Path('.astis/semantic-neutral-20261114/bernstein_exp_fresh_61a9')
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '9a8b163f4753a1329dbc0435c1e7f810f729c349'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
allowp = S / 'ROOT-carrier-allowlist.v1.json'
assert sha(allowp.read_bytes()) == '4c2e60385802f60a5cd66671051832d3a9a638f30ceadb7d6a73e4bc1c251bb8'
allow = json.loads(allowp.read_bytes())
dest = E / 'source-review/bernstein_exp_fresh_61a9'
assert not dest.exists()
selected = []
for row in allow['paths_relative_to_repository']:
    p = Path(row['path'])
    assert p.parent == S and '.private.' not in p.name
    b = p.read_bytes()
    assert len(b) == row['bytes'] and sha(b) == row['sha256']
    create(dest / p.name, b)
    selected.append(dest / p.name)
create(dest / allowp.name, allowp.read_bytes())
selected.append(dest / allowp.name)
manifest = json.loads((dest / 'chosen-originals.manifest.v1.json').read_bytes())
archive = dest / 'chosen-originals.v1.tar.gz'
assert sha(archive.read_bytes()) == manifest['archive']['sha256']
with tarfile.open(archive, 'r:gz') as tf:
    members = tf.getmembers()
    assert len(members) == manifest['archive_regular_file_count'] == 86
    assert len({m.name for m in members}) == len(members)
    expected = {x['member']: x for x in manifest['members']}
    assert set(expected) == {m.name for m in members}
    for m in members:
        assert m.isfile() and not m.name.startswith('/') and '..' not in Path(m.name).parts
        b = tf.extractfile(m).read()
        assert len(b) == expected[m.name]['bytes'] and sha(b) == expected[m.name]['sha256']
run = dest / 'source-reader-review.run.v2.json'
assert sha(run.read_bytes()) == 'c0d561fe1f9d150670e554fb6ba1fc7574b6f62e5533dbc4c442cf153b4dbe49'
public = json.loads(A.read_bytes())
private = json.loads((W / 'private-consumer-audit.reconstructed.v2.json').read_bytes())
for label, a, packet in [('P', public, W / 'P.reviewer-packet.v2.json'),
                         ('T', private, W / 'T.reviewer-packet.v2.json')]:
    op = dest / (label + '.audit-overlay.v2.json')
    o = json.loads(op.read_bytes())
    pkt = json.loads(packet.read_bytes())
    assert o['reviewer_packet_sha256'] == pkt['packet_sha256']
    assert o['review_run_sha256'] == sha(run.read_bytes())
    assert o['independent_from_formalizer'] and o['independent_from_decoder']
    assert set(o['semantic_slots']) == set(rt.SEMANTIC_SLOTS)
    assert not o['deltas'] and not o['repairs'] and o['verdict'] == 'equivalent-after-elaboration'
    for key in ['semantic_slots', 'deltas', 'verdict', 'repairs']:
        a[key] = o[key]
    a['source_review'] = {'state': 'accepted', 'reviewer': o['reviewer'],
        'independent_from_formalizer': o['independent_from_formalizer'],
        'independent_from_decoder': o['independent_from_decoder'],
        'reviewer_packet_sha256': o['reviewer_packet_sha256'],
        'evidence': o['review_evidence'], 'review_run_sha256': o['review_run_sha256'],
        'run_artifact': str(run)}
    a['state'] = 'source-reviewed'
    a['reader_commit'] = head
    a['actual_math_commit'] = '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff'
    a['independent_original_overlay'] = {'path': str(op), 'sha256': sha(op.read_bytes())}
public_path = A
public_path.write_bytes(dump(public))
create(E / 'private-consumer-audit.source-reviewed.v2.json', dump(private))
create(E / 'private-consumer-registry.source-reviewed.v2.json', dump({'schema_version': 1, 'audits': [private]}))
data = pub.inputs()
item = next(x for x in pub.load() if x['id'] == 'huanjian-matrix-bernstein-exponential')
assert pub.binding_digest(item, item['bindings'][0], data) == public['publication_binding_sha256'] == '039a91f41fb14176849c877a897f6d47ca6f50b60f2bef5e29407854f044610b'
cell = json.loads(C.read_bytes())
cell['evidence']['independent_source_review'] = {
    'reviewer': '/root/bernstein_exp_fresh_61a9', 'source_reader_commit': head,
    'P_decision': public['verdict'], 'private_T_decision': private['verdict'],
    'P_publication_binding_sha256': public['publication_binding_sha256'],
    'private_T_binding_sha256': private['publication_binding_sha256'],
    'review_run': str(run), 'review_run_sha256': sha(run.read_bytes()),
    'complete_code_first_judgment': str(dest / 'PT-whole-module-code-judgment.v1.json'),
    'complete_code_first_sha256': 'f67ac23fe192d56e50603d29f00b93cdd37de6dd22e20a33e2b216610b4371c1',
    'raw_and_whole_code_before_outcomes_and_reconstructions': True,
    'all_code_lines_exact_in_seven_folds': 388,
    'locator_correction': 'Only T source locator54->57; v1 originals retained, v2 independently rebound.',
    'runtime_reader': 'pending separate original/candidate ROOT-primary browser check and independent screenshot review',
    'archive': str(archive), 'archive_sha256': sha(archive.read_bytes())}
cell['conceptual_mirror_audit'] = {'status': 'none-found', 'discovery_ids': [],
    'evidence': str(E / 'conceptual-mirror-audit.authored-v1.json'),
    'independent_review': str(run), 'independent_run_sha256': sha(run.read_bytes()),
    'scope': 'Scoped scalar/CFC/PSD expectation mechanism audit; no new cross-domain transport and no formal edge inferred from similarity.'}
cell['evidence']['local_math_candidate']['independent_semantic'] = 'accepted exact P real component and private authored actual-Gaussian specialization'
cell['reservation_only'] = 'Normal ledger EXPLORING; independent complete source/semantic/static reader accepted. Actual browser and independent final state admission pending.'
C.write_bytes(dump(cell))
for p in [W / 'bounded-mirror-memory-readback.v1.json', W / 'original-owner-current-after-actual-mgf.json', Path(__file__)]:
    create(E / 'source-carrier-originals' / p.name, p.read_bytes())
paths = [A, C, E / 'private-consumer-audit.source-reviewed.v2.json', E / 'private-consumer-registry.source-reviewed.v2.json',
         *selected, *[p for p in sorted((E / 'source-carrier-originals').rglob('*')) if p.is_file()]]
spec = W / 'source-carrier-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(A), str(C)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Carry independent complete matrix exponential and Gaussian MGF source reviews'], check=True)
out = {'source_carrier_commit': git('rev-parse', 'HEAD').decode().strip(), 'normal_API_calls': 0,
       'independent_P_T_semantics': 'accepted', 'runtime_reader': 'pending', 'ROOT_V_calls': 0}
create(W / 'actual-independent-source-carrier-commit.json', dump(out))
print(json.dumps(out))
