"""Commit only SAU77 integration/evidence; preserve collaborator edits."""
from pathlib import Path
import gzip
import hashlib
import json
import subprocess

run = Path('runs/20261007-companion-priority/pbps-unit-exponential-product77')
note = json.loads((run / 'integration.notes.json').read_bytes())
assert note['status'] == 'LOCAL_SHARED_AGGREGATE_AND_GENERATED_READER_GATES_PASS_VISUAL_PENDING'
assert not subprocess.check_output(['git','diff','--cached','--name-only'], text=True).strip()
scope = json.loads((run / 'integration77/integration-scope.json').read_bytes())
paths = list(scope['owned']) + [
    'research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json',
    'runs/substantive_advances.jsonl', 'docs/module-graph.svg',
    'docs/assets/astis_lean_arsenal_module_graph.svg',
    'research-wiki/sampling-sde-library/lean-leaf-module-graph.md',
    'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json',
    'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.md',
]
old_archive = json.loads((run / 'resume-20261010/immutable-compiler-log-archive.json').read_bytes())
excluded = {old_archive['original_local_path']}
archives = []
for p in list(run.rglob('*')):
    if not p.is_file() or p.suffix in {'.pyc','.html'} or p.as_posix() in excluded:
        continue
    if p.suffix == '.log':
        raw = p.read_bytes()
        if len(raw) > 1000000 or any(line.endswith((b' ',b'\t')) for line in raw.splitlines()):
            gz = p.with_suffix(p.suffix + '.gz')
            assert not gz.exists()
            gz.write_bytes(gzip.compress(raw, mtime=0))
            assert gzip.decompress(gz.read_bytes()) == raw
            archives.append({'original_local_path': p.as_posix(), 'RAW_sha256': hashlib.sha256(raw).hexdigest(),
                             'archive': gz.as_posix(), 'archive_sha256': hashlib.sha256(gz.read_bytes()).hexdigest()})
            excluded.add(p.as_posix())
            paths.append(gz.as_posix())
            continue
    paths.append(p.as_posix())
archive_manifest = run / 'integration77/immutable-evidence-archives.json'
assert not archive_manifest.exists()
archive_manifest.write_text(json.dumps({'archives': archives,
    'recipe': 'gzip.decompress(archive) recovers exact original raw log. Local originals/receipts remain unchanged.',
    'reason': 'Preserve immutable compiler output while keeping staged whitespace clean and large logs compact.'}, indent=2) + '\n', encoding='utf8')
paths.append(archive_manifest.as_posix())
paths = list(dict.fromkeys(paths))
assert all(Path(p).exists() and p not in excluded for p in paths)
assert all(not p.startswith(('agent-briefs/','research-wiki/external-lean-libraries/','research-wiki/technical-lemmas/')) for p in paths)
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],
               input=('\0'.join(paths) + '\0').encode(), check=True)
check = subprocess.run(['git','-c','core.autocrlf=false','-c','core.whitespace=cr-at-eol','diff','--cached','--check'], capture_output=True)
print('Bounded staged paths:', len(paths), 'whitespace:', check.returncode)
if check.returncode:
    print(check.stdout.decode(errors='replace')[:12000])
    raise SystemExit(check.returncode)
subprocess.run(['git','commit','-m','Integrate verified exponential inputs with full local gates; retain visual debt'], check=True)
print(subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip())
