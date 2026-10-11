"""Commit only the independently reviewed merge and its lossless evidence."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

r = Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args])

review = load(r / 'independent-review/merge-resolution-review104.native.json')
assert review['decision'] == 'ACCEPT_BOUNDED_UNCOMMITTED_MERGE_RESOLUTION'
assert git('rev-parse', 'HEAD').decode().strip() == review['checked_parents']['ours']
assert git('rev-parse', 'MERGE_HEAD').decode().strip() == review['checked_parents']['upstream']
assert git('write-tree').decode().strip() == review['checked_index_tree']
assert not git('diff', '--name-only', '--diff-filter=U').strip()
prior = load(r / 'premerge.json')
for x in prior['dirty_raw']:
    assert sha(Path(x['path']).read_bytes()) == x['raw_sha256'], x['path']
labels = ['tests', 'astis', 'canonical', 'publication', 'contributor', 'semantic',
          'frontier', 'process-memory', 'python-compile', 'site-build', 'site-check',
          'graph-after-site', 'site-regressions', 'harness', 'diff-check', 'curve-graph']
for label in labels:
    c = load(r / 'checks' / ('integration-' + label) / 'receipt.json')
    assert c['terminal_closed'] and c['exit_code'] == 0, label
reader = load(r / 'pbps-reader-after-merge.json')
assert reader['status'] == 'PASS_GENERATED_CONTENT_ONLY'
assert reader['exact_step_Lean_regions'] == 7 and reader['details_initially_folded'] == 13
staged_before = set(git('diff', '--cached', '--name-only').decode().splitlines())
assert staged_before == {x['path'] for x in review['staged_files']}
files = [p for p in r.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
prev = r.parent.parent / 'pbps-actual-phase-normalization103/integration103'
files += [prev / n for n in ['postpush-binding103.json', 'push103.stdout.log', 'push103.stderr.log']]
added, archives = [], []
for p in sorted(files):
    if p.suffix == '.pyc':
        continue
    name, raw = p.as_posix(), p.read_bytes()
    if p.suffix.lower() in {'.gz', '.png', '.jpg', '.pdf'}:
        git('-c', 'core.autocrlf=false', 'add', '-f', '--', name)
        added.append(name)
        continue
    opaque = p.suffix in {'.log', '.snapshot', '.exactraw', '.lean'} or 'parent-blobs' in p.parts or len(raw) > 200000
    normal = b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n', b'\n').split(b'\n')).rstrip(b'\n') + b'\n'
    if opaque or normal != raw:
        z = Path(str(p) + '.merge104.raw.gz')
        assert not z.exists() or gzip.decompress(z.read_bytes()) == raw
        if not z.exists():
            z.write_bytes(gzip.compress(raw, mtime=0))
        git('-c', 'core.autocrlf=false', 'add', '-f', '--', z.as_posix())
        added.append(z.as_posix())
        archives.append(dict(raw_path=name, raw_sha256=sha(raw), archive=z.as_posix(),
                             archive_raw_sha256=sha(z.read_bytes()), public_text_sha256=None if opaque else sha(normal)))
    if not opaque:
        blob = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'], input=normal).decode().strip()
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo', '100644', blob, name], check=True)
        added.append(name)
manifest = r / 'merge-storage-map.json'
assert not manifest.exists()
manifest.write_text(json.dumps(dict(archives=archives, checked_parents=review['checked_parents'],
    reviewed_production_index_tree=review['checked_index_tree'], added_evidence_only=added,
    prospective104_header_or_claim_included=False, PBPS_merged_to_main=False), indent=2) + '\n', encoding='utf8', newline='\n')
git('-c', 'core.autocrlf=false', 'add', '--', manifest.as_posix())
added.append(manifest.as_posix())
for x in review['staged_files']:
    assert sha(git('show', ':' + x['path'])) == x['index_sha256'], x['path']
for x in archives:
    assert sha(gzip.decompress(git('show', ':' + x['archive']))) == x['raw_sha256']
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == staged_before | set(added)
for args in [('diff', '--cached', '--check'), ('diff', '--check')]:
    q = subprocess.run(['git', *args], capture_output=True)
    assert q.returncode == 0, (q.stdout + q.stderr).decode(errors='replace')
git('commit', '-q', '-m', 'Merge reviewed curve extension while preserving PBPS normalization')
head = git('rev-parse', 'HEAD').decode().strip()
assert git('rev-list', '--parents', '-n', '1', head).decode().split()[1:] == [prior['head'], prior['upstream']]
for x in prior['dirty_raw']:
    assert sha(Path(x['path']).read_bytes()) == x['raw_sha256']
(r / 'merge-commit.json').write_text(json.dumps(dict(commit=head, parents=[prior['head'], prior['upstream']],
    gates=16, independent_merge_review=True, prior_dirty_RAW_preserved=True, PBPS_merged_to_main=False,
    prospective104_proved=False), indent=2) + '\n', encoding='utf8', newline='\n')
print('REVIEWED_MERGE_COMMIT', head)
