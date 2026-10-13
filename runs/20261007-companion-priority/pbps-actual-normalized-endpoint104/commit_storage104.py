"""Deliver the independent bounded storage audit without changing its RAW bytes."""
from pathlib import Path
import gzip, hashlib, json, subprocess

r = Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
folder = r / 'integration-storage-review104'
out = r / 'integration104'
sha = lambda b: hashlib.sha256(b).hexdigest()
def git(*a):
    return subprocess.check_output(['git', *a])

head = json.loads((folder / 'storage-decision104.native.json').read_bytes())['checked_integration_commit']
assert git('rev-parse', 'HEAD').decode().strip() == head
assert not git('diff', '--cached', '--name-only').strip()
decision = json.loads((folder / 'storage-decision104.native.json').read_bytes())
assert decision['verdict'] == 'ACCEPT_IMMUTABLE_STORAGE_AND_GENERATED_READER_ONLY'
assert decision['checked_integration_commit'] == head
manifest = json.loads((folder / 'closed-RAW-manifest104.native.json').read_bytes())
assert manifest['checked_integration_commit'] == head
assert sha((folder / 'storage-decision104.native.json').read_bytes()) == manifest['decision']['raw_sha256']
rows, staged = [], []
for p in sorted(folder.rglob('*')):
    if not p.is_file() or '__pycache__' in p.parts or p.suffix == '.pyc':
        continue
    raw = p.read_bytes()
    name = p.as_posix()
    if p.suffix.lower() in {'.gz', '.png', '.jpg', '.jpeg', '.webp', '.pdf'}:
        git('-c', 'core.autocrlf=false', 'add', '-f', '--', name)
        staged.append(name)
        continue
    normalized = b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n', b'\n').split(b'\n')).rstrip(b'\n') + b'\n'
    opaque = p.suffix in {'.log', '.lean', '.html', '.snapshot'} or len(raw) > 200000
    if opaque or normalized != raw:
        archive = Path(str(p) + '.delivery104.raw.gz')
        assert not archive.exists() or gzip.decompress(archive.read_bytes()) == raw
        if not archive.exists():
            archive.write_bytes(gzip.compress(raw, mtime=0))
        git('-c', 'core.autocrlf=false', 'add', '-f', '--', archive.as_posix())
        staged.append(archive.as_posix())
        rows.append(dict(raw_path=name, raw_sha256=sha(raw), archive=archive.as_posix(), archive_raw_sha256=sha(archive.read_bytes()), public_text_raw_sha256=None if opaque else sha(normalized)))
    if not opaque:
        blob = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'], input=normalized).decode().strip()
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo', '100644', blob, name], check=True)
        staged.append(name)
path = out / 'storage-delivery-RAW104.json'
assert not path.exists()
path.write_text(json.dumps(dict(files=rows, reviewed_integration_commit=head, scope='Independent storage audit only; no mathematics or shared publication mutation.'), indent=2) + '\n', encoding='utf8', newline='\n')
for p in [path, Path(__file__).resolve().relative_to(Path.cwd().resolve())]:
    git('-c', 'core.autocrlf=false', 'add', '--', p.as_posix())
    staged.append(p.as_posix())
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) <= set(staged)
for row in rows:
    assert sha(gzip.decompress(git('show', ':' + row['archive']))) == row['raw_sha256']
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'diff', '--check'], check=True)
subprocess.run(['git', 'commit', '-q', '-m', 'Archive independent endpoint-pair reversal delivery audit'], check=True)
print('AUDIT104_COMMIT', git('rev-parse', 'HEAD').decode().strip())
