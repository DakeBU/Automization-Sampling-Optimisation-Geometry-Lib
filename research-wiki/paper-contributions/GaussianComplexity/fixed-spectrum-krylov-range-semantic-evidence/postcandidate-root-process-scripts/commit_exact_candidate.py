from pathlib import Path
import hashlib, json, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
sha = lambda b: hashlib.sha256(b).hexdigest()
record = json.loads((W/'immutable-candidate-selected-files.private.json').read_bytes())
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == record['intended_base']
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
for name, row in record['files'].items():
    b = Path(name).read_bytes()
    assert sha(b) == row['sha256'] and len(b) == row['bytes'], name
subprocess.run(['git', 'add', '-f', '--', *record['files']], check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only', '-z']).decode().rstrip('\0').split('\0'))
assert staged == set(record['files']), (staged-set(record['files']), set(record['files'])-staged)
for name, row in record['files'].items():
    b = subprocess.check_output(['git', 'show', ':'+name])
    assert sha(b) == row['sha256'] and len(b) == row['bytes'], name
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'commit', '-m', 'feat(gaussian): prove actual cosine-feature Krylov range'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
parent = subprocess.check_output(['git', 'rev-parse', 'HEAD^'], text=True).strip()
assert parent == record['intended_base']
for name, row in record['files'].items():
    b = subprocess.check_output(['git', 'show', commit+':'+name])
    assert sha(b) == row['sha256'] and len(b) == row['bytes'], name
out = W/'actual-immutable-mathematical-candidate.json'
assert not out.exists()
out.write_text(json.dumps({'commit': commit, 'parent': parent, 'all125_selected_files_byte_exact_in_git': True, 'selected_files': len(record['files']), 'producer_sha256': record['files']['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean']['sha256'], 'private_Test_sha256': record['files']['Tests/GaussianComplexityFixedSpectrumKrylovRange.lean']['sha256'], 'PLOCAL_only_not_independently_verified_or_published': True, 'no_remote_or_global_mutation': True}, indent=2)+'\n')
print(out.read_text())
