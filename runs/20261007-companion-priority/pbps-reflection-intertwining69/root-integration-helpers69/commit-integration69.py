from pathlib import Path
import gzip, hashlib, json, os, re, subprocess

r = Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
assert subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip() == '2d286c283a6fb5dfc13180204bb0da54531a5c67'
assert load(r/'root.exact-verification69.adoption.json')['native_verified']
assert load(r/'visual.inspection.json')['viewed_by_root']
assert load(r/'root.repository69.adoption.json')['accepted_scoped_aggregate']
assert load(r/'root.native-transport69.adoption.json')['accepted_exact_transport']
assert not subprocess.check_output(['git','diff','--cached','--name-only'], text=True).strip()
for label in ['mandatory-astis-check-final','publication-final-admin','frontier-final-admin',
              'contributor-final-admin','semantic-final-admin','site-check-final',
              'graph-check-actual-final','reader-copy-download']:
    x = load(r/'integration69'/label/'receipt.json')
    assert x['terminal_closed'] and x['exit_code'] == 0, label
plan = load(r/'publication-plan.json')
shared = ['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean',
          'Tests/Basic.lean','docs/companion-papers-handoff.md',
          'website/content/samplewiki_companion_frontiers.json',
          'research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl',
          'runs/substantive_advances.jsonl','docs/module-graph.svg',
          'docs/assets/astis_lean_arsenal_module_graph.svg',
          'research-wiki/sampling-sde-library/lean-leaf-module-graph.md',
          'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json',
          'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining.md']
shared += ['research-wiki/frontier-cells/'+cid+'.json' for cid in plan['active_cells']]
changed = set(subprocess.check_output(['git','-c','core.autocrlf=false','diff','--name-only'], text=True).splitlines())
assert changed <= set(shared), changed-set(shared)
active = Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']).resolve()
assert active.is_relative_to((r/'integration69').resolve())
export = r/'root-integration-helpers69'; export.mkdir(exist_ok=False)
for p in Path('.astis/pbps-sharp-energy68').iterdir():
    if p.is_file() and p.suffix in ['.py','.mjs'] and not p.stem.endswith('70'):
        (export/p.name).write_bytes(p.read_bytes())
(export/'source-retention.json').write_text(json.dumps(dict(
    scope='Root integration helper sources retained; actual execution bound separately by receipts.',
    active_observer_excluded=active.as_posix()), indent=2)+'\n', encoding='utf-8', newline='\n')
future = {'adopt-and-seal-header70-native-ranges','adopt-and-seal-header70',
          'adopt-header-math70','retrieve-rotation70'}
paths = list(dict.fromkeys(shared + [p.as_posix() for p in r.rglob('*')
    if p.is_file() and not p.resolve().is_relative_to(active)
    and p.relative_to(r).parts[0] not in future]))
old = Path('runs/20261007-companion-priority/pbps-sharp-energy68')
late_paths = []
for folder in ['integration68/remote-int68-snapshot6','integration68/remote-int68-snapshot7']:
    late_paths += [p.as_posix() for p in (old/folder).rglob('*') if p.is_file()]
late_paths += [(old/p).as_posix() for p in ['remote-ci68.accepted.json',
    'integration68/pr315-body68-remote-accepted.md']]
paths += late_paths
paths = list(dict.fromkeys(paths))
transport = load(r/'integration69/native-transport69/manifest.json')
oversized = transport['original_path']
assert oversized == (r/'independent-repository-reader69/complete-named-review-decision-input-payload.json').as_posix()
assert sha(Path(oversized).read_bytes()) == transport['original_RAW_sha256']
assert oversized in paths
paths.remove(oversized)
assert all(Path(p).is_file() and Path(p).stat().st_size < 100*1024*1024 for p in paths)
assert not any('pbps-actual-projected-rotation-preproof70' in p or
    'pbps-macro-root63/exact-science-verification/inputs/0446.exactraw.snapshot' in p or
    Path(p).resolve().is_relative_to(active) for p in paths)
def stage(ps):
    subprocess.run(['git','-c','core.autocrlf=false','add','-f','--pathspec-from-file=-',
                    '--pathspec-file-nul'], input=('\0'.join(ps)+'\0').encode(), check=True)
stage(paths)
d = r/'integration69/staging-whitespace'; d.mkdir(exist_ok=False)
q = subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'], capture_output=True)
raw = q.stdout; hits = []
for line in raw.decode('utf-8').splitlines():
    m = re.match(r'^(.+?):([0-9]+): (trailing whitespace|new blank line at EOF|space before tab in indent).*$', line)
    if m: hits.append(dict(path=m[1], line=int(m[2]), kind=m[3]))
assert q.returncode in [0,2] and (q.returncode == 0 or hits)
bad = sorted({x['path'] for x in hits})
for p in bad: assert p.startswith(r.as_posix()+'/') or p in late_paths, p
authored = [p for p in paths if p not in set(bad)]
for start in range(0,len(authored),64):
    subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check','--']+
                   authored[start:start+64], check=True)
(d/'full-staged-immutable-negative.raw.gz').write_bytes(gzip.compress(raw, mtime=0))
(d/'diagnosis.json').write_text(json.dumps(dict(full_staged_exit=q.returncode,
    full_staged_called_PASS=q.returncode == 0,
    exact_immutable_raw_paths=[dict(path=p, raw_sha256=sha(Path(p).read_bytes())) for p in bad],
    findings=hits, negative_RAW_sha256=sha(raw), authored_complement_exit=0,
    no_folder_exclusion=True, active_observer_excluded=active.as_posix(),
    oversized_native_RAW_Git_object_excluded_exactly=oversized,
    exact_compressed_RAW_transport_manifest=(r/'integration69/native-transport69/manifest.json').as_posix(),
    future70_not_staged=True), ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
stage([p.as_posix() for p in d.iterdir() if p.is_file()])
actual = set(subprocess.check_output(['git','diff','--cached','--name-only'], text=True).splitlines())
assert actual <= set(paths) | {p.as_posix() for p in d.iterdir() if p.is_file()}
subprocess.run(['git','commit','-q','-m','Integrate independently verified PBPS full-micro reflection intertwining'], check=True)
print(json.dumps(dict(integration_commit=subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
    staged_files=len(actual), immutable_native_whitespace_findings=len(hits),
    authored_whitespace_PASS=True, full_staged_whitespace_PASS=q.returncode == 0,
    future70_not_staged=True, full_paper=False)))
