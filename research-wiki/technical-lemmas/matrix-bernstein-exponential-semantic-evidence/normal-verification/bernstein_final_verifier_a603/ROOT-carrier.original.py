"""Carry the independent actor's completed one V and projection; never call an API."""
from pathlib import Path
import hashlib, json, subprocess, tarfile
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
R = Path('.astis/semantic-neutral-20261114/bernstein_final_verifier_a603')
N = Path('.astis/semantic-neutral-20261114/bernstein_exp_native_72c4')
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
L = Path('runs/substantive_advances.jsonl')
HELD = '8de3e1ef9973258fafaf9ee793a215c4d7683d93'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
assert git('rev-parse', 'HEAD').decode().strip() == HELD
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(C), str(L)}
assert sha(C.read_bytes()) == 'df69ae75fc0300490cb847987cc68a47809c98c5facea2fa771c245dd88ed2b0'
ap = (R / 'actual-VERIFIED-append.exact.jsonl').read_bytes()
vb = (R / 'VERIFIED-evidence.full.json').read_bytes()
assert sha(ap) == 'e432f9cf6e526006ff2a11254d5b50f3d3c5b8e5cc77dc83459fb27e9bac75e5'
assert sha(vb) == '0bbecbd7bd8d28b70394a5bbd3bff301e1113b5a3ff559d71c3231e0f6543672'
assert L.read_bytes() == git('show', f'{HELD}:{L}') + ap
event, v = json.loads(ap), json.loads(vb)
assert event['advance_id'] == 'ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic'
assert event['to_state'] == 'VERIFIED' and event['evidence'] == v
assert str(v['verifier_id']).endswith('bernstein_final_verifier_a603')
pl = json.loads((E / 'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert len(pl) == 24
cell = json.loads(C.read_bytes())
assert cell['status'] == 'independently_verified'
assert cell['owner_id'] == 'huanjian_20261114_matrix_bernstein_exponential'
assert isinstance(cell['evidence']['independent_verification'], str)
assert cell['evidence']['independent_verification_details'] == v
for k, x in pl.items():
    assert v[k] == x and cell['evidence']['independent_verification_details'][k] == x
allowp = R / 'ROOT-CARRIER-ALLOWLIST.json'
assert sha(allowp.read_bytes()) == '29b0270d44d0363065a793d6ac74b6e1ddb1c63b45483afb526950d47b019a93'
allow = json.loads(allowp.read_bytes())
assert allow['normalV_calls_total'] == 1 and allow['cell_projection_API_calls'] == 0
assert allow['native_archive_inclusions_total'] == 1
dest = E / 'normal-verification/bernstein_final_verifier_a603'
assert not dest.exists()
for x in allow['files']:
    rel = Path(x['relative_destination'])
    assert not rel.is_absolute() and '..' not in rel.parts and '.private.' not in str(rel)
    p = R / rel
    assert p == Path(x['source']) and not p.is_symlink()
    b = p.read_bytes()
    assert len(b) == x['bytes'] and sha(b) == x['sha256']
    create(dest / rel, b)
create(dest / allowp.name, allowp.read_bytes())
archives = [
    ('verifier-chosen-originals.v1.tar.gz', 'e6e9646bc2e154cb614932e6c41e20e0c2915d981b188cae36e560f47d71929a', 18, 1),
    ('cell-projection-originals.supplement.v1.tar.gz', '85b8d13ad89cf78c8aae3205b7b1902ebb889d292b13229e23e0191fc508800f', 7, 0)]
for name, digest, count, native_count in archives:
    p = dest / name
    assert sha(p.read_bytes()) == digest
    with tarfile.open(p, 'r:gz') as tf:
        members = tf.getmembers()
        assert len(members) == count
        assert all(m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts for m in members)
        embedded = [m for m in members if Path(m.name).name == 'native-chosen-originals.v1.tar.gz']
        assert len(embedded) == native_count
        for m in embedded:
            assert sha(tf.extractfile(m).read()) == '217ca0fbd83c5b380dfe7bb4f92b50a407801bd15d8d7286b831424a14d5bdb0'
small_native = {
    'native-final-summary-carrier.v1.json': '02847ddf13ae89bc8877f8bf167b3310c61ae295ec24a54f98fc6f4c227337d9',
    'native-chosen-originals.manifest.v1.json': 'f2515c5985106ec2fb304dc05692c3d81ab0ad4eac4ffb202914c137e5ca58d7',
    'native-chosen-originals.ROOT-allowlist.v1.json': '3c7a6de0b12c92e34066a41baaaad5a9587df033c7abcf7b87f559df9b11ffb5',
    'metadata-gates-once/metadata-gates-summary.json': 'e96a0636afce6052ed07227d450612289b35da71fecd49ff45354538d7e7029b'}
for name, digest in small_native.items():
    p = N / name
    assert sha(p.read_bytes()) == digest
    create(E / 'final-native-summary' / name, p.read_bytes())
owner = W / 'original-owner-current-at-normal-PL.json'
o = json.loads(owner.read_bytes())
assert o['actual_fetch_exit'] == 0 and o['original_owner']['state'] == 'STABILIZING'
create(dest / owner.name, owner.read_bytes())
memory_path = E / 'local-cycle-memory.json'
memory = json.loads(memory_path.read_bytes())
memory['current_state'] = 'INDEPENDENT_VERIFIED_LOCAL_ONLY; one normalPL, one independent normalV, zero ROOT V calls'
memory['checked_metadata_commit'] = HELD
memory['actual_V_append_sha256'] = sha(ap)
memory['actual_V_payload_sha256'] = sha(vb)
memory['all_original_PL_fields_inline_unchanged'] = len(pl)
memory['cell_projection'] = 'Independent actor completed zero-API projection; exact fullV details and STRING current-scope summary.'
memory['native_archive'] = {'sha256': '217ca0fbd83c5b380dfe7bb4f92b50a407801bd15d8d7286b831424a14d5bdb0',
    'included_exactly_once_inside': str(dest / archives[0][0]), 'regular_native_originals': 777}
memory['latest_owner_observation'] = {'file': str(dest / owner.name), 'sha256': sha(owner.read_bytes()),
    'origin_main': o['origin_main'], 'original_owner_released': False}
memory['remaining_reader_limits'] = 'Isolated/unapplied overlay only. Initial fit-scale graph labels remain small; demonstrated existing UI wheel/pan is readable. Physical phone/touch and clipboard execution untested. Production/main/full-site/purification acceptance not granted.'
memory_path.write_bytes(dump(memory))
create(dest / 'ROOT-carrier.original.py', Path(__file__).read_bytes())
paths = [C, L, memory_path, *[p for p in sorted(dest.rglob('*')) if p.is_file()],
         *[p for p in sorted((E / 'final-native-summary').rglob('*')) if p.is_file()]]
spec = W / 'VERIFIED-carrier-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(C), str(L), str(memory_path)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Carry independent matrix exponential and Gaussian MGF verification with exact originals'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for p in paths:
    assert git('show', f'{commit}:{p}') == p.read_bytes()
out = {'verification_carrier_commit': commit, 'checked_metadata_commit': HELD,
       'actual_V_append_sha256': sha(ap), 'all_original_PL_fields_inline_unchanged': len(pl),
       'ROOT_V_calls': 0, 'normal_API_replay': False, 'exact_owned_files': len(paths),
       'private_guards_exported': False, 'integration_publication_purification_wholeGoal': 'HOLD'}
create(W / 'actual-VERIFIED-carrier-commit.json', dump(out))
print(json.dumps(out))
