"""Observe the actual fixed toolchain and every manifest package before the next normal intake and proof."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess

workspace = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
lean = Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
version = subprocess.check_output([str(lean), '--version']).decode().strip()
assert 'version 4.33.0,' in version and 'd8b18978322de05a8f3dba51ef03cf5461676c17' in version
assert sha(lean.read_bytes()) == '1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554'
manifest_raw = Path('lake-manifest.json').read_bytes()
assert sha(manifest_raw) == 'b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'
manifest = json.loads(manifest_raw)
packages = []
for item in manifest['packages']:
    path = Path('.lake/packages') / item['name']
    revision = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD']).decode().strip()
    status = subprocess.check_output(['git', '-C', str(path), 'status', '--porcelain=v1', '--untracked-files=all'])
    assert revision == item['rev'] and not status, item['name']
    packages.append({'name': item['name'], 'revision': revision, 'porcelain_empty': True})
assert len(packages) == 9
source = Path('.astis/huanjian-resume-20261103/2610.20492v1.html').read_bytes()
assert len(source) == 951991 and sha(source) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
record = {
    'observed_utc': datetime.now(timezone.utc).isoformat(),
    'HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'lean_version': version, 'lean_binary_sha256': sha(lean.read_bytes()),
    'lean_toolchain_sha256': sha(Path('lean-toolchain').read_bytes()),
    'manifest_sha256': sha(manifest_raw), 'packages': packages,
    'source_sha256': sha(source),
    'scope': 'Actual read-only environment check when resuming the same Gaussian Goal. Prior canonical reuse API exposure is recorded separately.',
    'formalizer_API_pristine': False,
}
raw = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode()
with (workspace / 'actual-environment-at-resume.json').open('xb') as out:
    out.write(raw)
print(json.dumps(record))
