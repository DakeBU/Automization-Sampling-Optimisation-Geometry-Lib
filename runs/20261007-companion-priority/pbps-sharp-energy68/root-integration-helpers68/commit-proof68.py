from pathlib import Path
import gzip, hashlib, json, os, re, subprocess, sys

root = Path.cwd()
r = Path('runs/20261007-companion-priority/pbps-sharp-energy68')
base = r.parent
parent = '38e5f34c6b2c82612459d54d6288a15e20d9deab'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == parent
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).strip()
assert (r / 'proved-local.json').is_file()
for folder in ['independent-math68', 'independent-source68']:
    assert load(r / folder / 'lease.final.json')['status'] == 'CLOSED_LAST'
for folder in ['anonymous-decoder', 'anonymous-consumer-decoder']:
    assert load(r / folder / 'lease.json')['status'] == 'CLOSED_LAST'
observer = Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
export = r / 'root-science-helpers68'
export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-sharp-energy68').glob('*.py'):
    (export / p.name).write_bytes(p.read_bytes())
(export / 'scope.json').write_text(json.dumps(dict(
    status='FROZEN_HELPER_SOURCES', active_observer_excluded=observer.as_posix(),
    scope='Root helper sources. Independent receipts provide execution evidence.'
), indent=2) + '\n', encoding='utf-8', newline='\n')
plan = load(r / 'publication-plan.json')
claim = load(r / 'claim.json')
paths = claim['proposed_files'] + [
    'research-wiki/frontier-cells/' + c + '.json' for c in plan['active_cells']
] + [
    'research-wiki/semantic-roundtrip/audits/' + a + '.json' for a in plan['audit_ids']
] + [
    'website/content/' + folder + '/' + slug + '.json'
    for folder in ['publications', 'declaration_lessons'] for slug in plan['slugs']
] + ['runs/substantive_advances.jsonl', 'runs/substantive_discoveries.jsonl']
folders = ['pbps-sharp-energy68', 'pbps-sharp-energy-preproof68']
for folder in folders:
    paths.extend(p.as_posix() for p in (base / folder).rglob('*')
                 if p.is_file() and not p.resolve().is_relative_to(observer))
late67 = subprocess.check_output([
    'git', 'ls-files', '--others', '--exclude-standard', '--',
    (base / 'pbps-root-commutation67').as_posix()
], text=True).splitlines()
paths = list(dict.fromkeys(paths + late67))
assert all(Path(p).is_file() and Path(p).stat().st_size < 100 * 1024 * 1024 for p in paths)
assert not any('pbps-reflection-rotation-preproof69' in p or
               'pbps-macro-root63/exact-science-verification/inputs/0446.exactraw.snapshot' in p or
               'pbps-real-defect-root61/next-macro-source62' in p or
               'pbps-centered-defect59/integration59/seal-' in p for p in paths)

def stage(items):
    subprocess.run(['git', '-c', 'core.autocrlf=false', 'add', '-f',
                    '--pathspec-from-file=-', '--pathspec-file-nul'],
                   input=('\0'.join(items) + '\0').encode(), check=True)

stage(paths)
full = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check'],
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
raw = full.stdout
findings = []
for line in raw.decode('utf-8').splitlines():
    match = re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$', line)
    if match:
        findings.append(dict(path=match[1], line=int(match[2]), kind=match[3]))
assert full.returncode in [0, 2] and (full.returncode == 0 or findings)
exceptions = list(dict.fromkeys(x['path'] for x in findings))
for path in exceptions:
    assert any(path.startswith((base / folder).as_posix() + '/')
               for folder in folders + ['pbps-root-commutation67']), ('Authored canonical whitespace', path)
    assert path in paths and not path.endswith(('proved-local.json', 'publication-plan.json', 'claim.json'))
authored = [p for p in paths if p not in set(exceptions)]
for start in range(0, len(authored), 64):
    subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check', '--']
                   + authored[start:start + 64], check=True)
diag = r / 'whitespace-diagnosis68'
diag.mkdir(exist_ok=False)
(diag / 'staged.raw-negative.log.gz').write_bytes(gzip.compress(raw, mtime=0))
(diag / 'diagnosis.json').write_text(json.dumps(dict(
    full_staged_exit=full.returncode, findings=findings, negative_RAW_sha256=sha(raw),
    immutable_native_exceptions=[dict(path=p, raw_sha256=sha(Path(p).read_bytes())) for p in exceptions],
    authored_complement_exit=0, active_observer_excluded=observer.as_posix(),
    scope='Preserve exact source/native/diagnostic bytes; finite immutable exceptions only. No full staged whitespace PASS.'
), indent=2) + '\n', encoding='utf-8', newline='\n')
paths.extend(p.as_posix() for p in diag.iterdir() if p.is_file())
stage(paths)
actual = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()
assert set(actual) <= set(paths)
for p in claim['proposed_files']:
    assert subprocess.check_output(['git', 'show', ':' + p]) == Path(p).read_bytes()
subprocess.run([sys.executable, '-X', 'utf8', 'tools/astis_publication.py', 'check', '--base', parent], check=True)
subprocess.run([sys.executable, '-X', 'utf8', 'tools/astis_contributor_contract.py', 'check', '--base', parent], check=True)
subprocess.run(['git', 'commit', '-q', '-m', 'Prove sharp PBPS corrector bound and actual modified energy equivalence'], check=True)
print('PASS68 science commit', subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
      'explicit paths', len(actual), 'immutable whitespace findings', len(findings))
