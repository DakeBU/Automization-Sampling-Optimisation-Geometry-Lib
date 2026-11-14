from pathlib import Path
import gzip, hashlib, json, re, subprocess, sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_publication as pub

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()

def put(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(data)

assert not (W/'first-mathematical-candidate-commit.json').exists()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == '75dcc0c9c7d9591384c6e0705e118b1ab440cd6c'
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
s = json.loads((W/'statement-seal-v1.json').read_bytes())
p = Path(s['producer']['planned_file'])
t = Path(s['actual_private_consumer']['planned_file'])
cap = json.loads((E/'local-proof-capsule.json').read_bytes())
assert cap['state'] == 'PROVED_LOCAL_NOT_SOURCE_VERIFIED'
assert cap['normal_PROVED_LOCAL_API_calls'] == 1
pub.check_advance([s['producer']['name']], reviewed=False)
for n in ['record_proved_local.py', 'package_local_evidence.py', 'check_isolated_static_reader.py',
          'export_requested_normalization_context.py', 'create_mathematical_candidate.py']:
    put(E/'root-local-process-scripts'/n, (W/n).read_bytes())
put(E/'minimal-requested-orthonormal-normalization-context.json', (W/'minimal-requested-orthonormal-normalization-context.json').read_bytes())
for stem in [
    '20261110T164109997981Z-cosine-gram-package-lossless-original-source-local-and-retired-attempt',
    '20261110T164841736327Z-cosine-gram-requested-minimal-orthonormal-normalization-context',
    '20261110T165007007580Z-cosine-gram-normal-PROVED-LOCAL-exact-types-and-foreign-preservation',
]:
    rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    x = json.loads(rp.read_bytes())
    raw = Path(x['log']).read_bytes()
    assert x['exit_code'] == 0 and sha(raw) == x['log_sha256']
    put(E/(stem+'.receipt.json'), rp.read_bytes())
    put(E/(stem+'.log.gz'), gzip.compress(raw, mtime=0))
extra = [p, t,
    Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json'),
    E.parent/'fixed-spectrum-cosine-gram-statement-seal.json',
    Path('website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json'),
    Path('website/content/publications/huanjian-fixed-spectrum-cosine-gram.json'),
    Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-cosine-gram.json'),
    Path('runs/substantive_advances.jsonl')]
paths = sorted(set(extra + [q for q in E.rglob('*') if q.is_file()]))
assert all(q.is_file() and not q.is_symlink() for q in paths)
raws = {str(q): q.read_bytes() for q in paths}
for n, raw in raws.items():
    assert not re.search(rb'wxid_|/Library/Containers/com\.tencent\.xinWeChat', raw), n
    assert 'PRIVATE' not in n and 'baseline.private' not in n, n
before = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
subprocess.run(['git', 'add', '-f', '--'] + list(raws), check=True)
staged = set(subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines())
assert staged == set(raws), staged ^ set(raws)
for n, raw in raws.items():
    assert subprocess.check_output(['git', 'show', ':'+n]) == raw, n
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'commit', '-m', 'Prove cosine-frame Gram identities with actual Gaussian mean consumer'], check=True)
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert subprocess.check_output(['git', 'rev-parse', commit+'^'], text=True).strip() == before
for n, raw in raws.items():
    assert subprocess.check_output(['git', 'show', commit+':'+n]) == raw, n
record = {
    'commit': commit, 'parent': before,
    'scope': 'Immutable local mathematical candidate only. Working-layer Lean checks predate this commit; independent fresh exact-candidate native/source/module/reader review and normal sourceV remain pending. No public history, global integration or Goal completion.',
    'source_sha256': sha(p.read_bytes()), 'Test_sha256': sha(t.read_bytes()),
    'publication_binding_sha256': cap['binding_sha256'],
    'files_exact_in_Git_tree': [{'path': n, 'sha256': sha(raw), 'bytes': len(raw)} for n, raw in raws.items()],
    'all_selected_ignored_logs_force_staged_and_tree_verified': True,
    'no_push_no_shared_aggregator_graph_site_or_Registry_write': True,
}
put(W/'first-mathematical-candidate-commit.json', dump(record))
print(json.dumps({'commit': commit, 'files_exact': len(raws), 'sourceV': False, 'public': False}))
