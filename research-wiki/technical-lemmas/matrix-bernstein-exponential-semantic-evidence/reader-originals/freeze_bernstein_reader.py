"""Commit exact authored reader candidate and blind inputs, without source verdicts."""
from pathlib import Path
import hashlib, json, subprocess
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
head = git('rev-parse', 'HEAD').decode().strip()
assert head == '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
names = ['author_bernstein_audits.py', 'author_bernstein_publication.py', 'attach_bernstein_decodes.py',
         'freeze_bernstein_reader.py', 'source_span_helpers.reused.original.py',
         'candidate-publication-context.v1.json', 'private-consumer-audit.draft.json',
         'private-consumer-audit.bound.v1.json', 'private-consumer-audit.reconstructed.v1.json',
         'private-consumer-registry.draft.json', 'private-consumer-registry.bound.v1.json',
         'private-consumer-registry.reconstructed.v1.json', 'P.reviewer-packet.v1.json', 'T.reviewer-packet.v1.json']
for name in names:
    create(E / 'reader-originals' / name, (W / name).read_bytes())
paths = [Path('website/content/declaration_lessons/huanjian-matrix-bernstein-exponential.json'),
         Path('website/content/publications/huanjian-matrix-bernstein-exponential.json'),
         Path('research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json')]
record = {'kind': 'IMMUTABLE_AUTHORED_READER_CANDIDATE; not independent source or browser acceptance',
          'actual_math_commit': head, 'public_lines': 148, 'private_lines': 240, 'folds': 7,
          'public_binding_sha256': 'a28ca8bfad0fac53ddd29b53f48f60d5ad0a6b4574db4ea8aadac09539902d29',
          'private_binding_sha256': '03bdf8e4b2367f941dd52209f62f154bd264fad0bc47ef11ee5d45b2d6289783',
          'source_fidelity': 'pending independent packet-bound seven-slot review',
          'browser': 'pending ROOT-primary actual desktop/mobile/adjacent source/download/graph checks',
          'integration': 'HOLD original shared owner; no shared CSS/aggregator/Registry/global source/graph writes',
          'metadata': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in paths]}
create(E / 'reader-candidate.json', dump(record))
tracked = set(git('ls-files', '-z').split(b'\0'))
paths += [p for p in sorted(E.rglob('*')) if p.is_file() and str(p).encode() not in tracked]
assert len(set(paths)) == len(paths)
spec = W / 'reader-candidate-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', *map(str, paths[:3])], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Author matrix exponential proof and scoped original Gaussian MGF reader candidate'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for p in paths:
    assert git('show', f'{commit}:{p}') == p.read_bytes()
out = {'reader_candidate_commit': commit, 'actual_math_commit': head, 'owned_files': len(paths),
       'normal_API_calls': 0, 'source_and_runtime_verdicts': 'pending'}
create(W / 'actual-reader-candidate-commit.json', dump(out))
print(json.dumps(out))
