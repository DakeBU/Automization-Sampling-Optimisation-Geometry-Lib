from pathlib import Path
import json, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact, put_new, sha
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
R = Path('.astis/huanjian-resume-20261103')
files = {}
for n in ['first-mathematical-candidate-commit.json', 'create_mathematical_candidate.py',
          'create_mathematical_candidate.attempt1.executed.py', 'create_mathematical_candidate_v2.py',
          'prepare_candidate_v2_diagnostic.py', 'snapshot_owner_after_candidate.py',
          'latest-main-owner-after-cosine-gram-candidate.json',
          'check_disabled_v3_static_cg.py', 'check_disabled_v3_static_cg.attempt1.executed.py',
          'check_disabled_v3_static_cg_v2.py', 'prepare_disabled_static_v2.py',
          'disabled-v3-static-missing-theme-diagnostic.json',
          'next-range-preseal-exposure-and-source-only-planning.json',
          'package_postcandidate_process_only.py']:
    p = W/n
    files[str(p)] = p.read_bytes()
for n in ['disabled-v3-cosine-gram-static', 'disabled-v3-cosine-gram-static-v2']:
    for p in (W/n).rglob('*'):
        if p.is_file() and not p.is_symlink():
            files[str(p)] = p.read_bytes()
for p in sorted(R.glob('*cosine-gram*.receipt.json')):
    if p.name < '20261110T165128':
        continue
    x = json.loads(p.read_bytes())
    log = Path(x['log'])
    raw = log.read_bytes()
    assert sha(raw) == x['log_sha256']
    files[str(p)] = p.read_bytes()
    files[str(log.relative_to(Path.cwd()))] = raw
record = archive_exact(files, E/'postcandidate-root-process-only.lossless-file-bytes.tar.gz')
record['scope'] = 'Exact root process provenance after mathematical candidate, including real failed candidate/privacy-self-match and static/theme-fixture attempts. Disabled prospective UI output is not independent acceptance or production delivery. Future range notes are disclosed preseal source-only planning, not new mathematics or admission. No independent verdict or private foreign baseline is authored/exported.'
put_new(E/'postcandidate-root-process-only.archive-manifest.json', (json.dumps(record, ensure_ascii=False, indent=2)+'\n').encode())
print(json.dumps({k: record[k] for k in ['archive', 'sha256', 'file_count', 'scope']}))
