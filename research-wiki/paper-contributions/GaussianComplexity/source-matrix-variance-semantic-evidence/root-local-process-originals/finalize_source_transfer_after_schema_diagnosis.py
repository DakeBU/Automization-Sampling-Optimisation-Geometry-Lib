"""Finish interrupted byte transfer, explicitly preserving the existing S schema failure."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as publication
import astis_semantic_roundtrip as semantic
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
R = Path('.astis/semantic-neutral-20261112/mv_src_6e28')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-variance.json')
HEAD = '1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
MATH = 'e654e98642350a615c473bc8190fbc1d47fe52bd'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])
def create(p, raw):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as out:
        out.write(raw)
assert git('rev-parse','HEAD').decode().strip() == HEAD
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(A),str(C)}
b = json.loads((W/'continuation-after-shared-VERIFIED.private.json').read_bytes())
ledger = Path('runs/substantive_advances.jsonl').read_bytes()
assert sha(ledger) == b['ledger_sha256']
states = advance._replay_advances([json.loads(x) for x in ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance')['state'] == 'EXPLORING'
assert states == b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
discovery = Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(discovery) == json.loads((W/'continuation-discoveries.private.json').read_bytes())['ledger_sha256']

destinations = set()
custody = []
for phase,digest in [
    (R/'r9-full-consumer-source-review-v3a','ba7533b3b3c03f5cd35097a22bb4782147307c2ca3f7262dcc9b11483ef2b005'),
    (R/'incremental-reader-v3c','4bffe7a6bbbde331d808f7bce8d02bebf228f9ce98c51cc7c9ccabce2af3c241'),
]:
    root = E/'source-review/mv_src_6e28'/phase.name
    mp = phase/'portable-custody-manifest.json'
    assert sha(mp.read_bytes()) == digest
    manifest = json.loads(mp.read_bytes())
    records = list(manifest['records'])
    post = phase/'postseal-output-index.json'
    records += [{'source_path': x['path'], 'destination_path': str(root/Path(x['path']).relative_to(phase)),
                 'bytes': x['bytes'], 'sha256': x['sha256']} for x in json.loads(post.read_bytes())['files']]
    records += [{'source_path': str(p),'destination_path':str(root/p.name),
                 'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in [mp,post]]
    for item in records:
        p,d = Path(item['source_path']),Path(item['destination_path'])
        assert p.is_relative_to(R) and not p.is_symlink() and not d.is_symlink()
        raw = p.read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256'] and d.read_bytes() == raw, str(d)
        if d.is_relative_to(E): destinations.add(d)
    custody.append({'manifest':str(root/mp.name),'sha256':digest,'records':len(manifest['records']),
                    'postseal_index':str(root/post.name),'postseal_sha256':sha(post.read_bytes())})
overlay = R/'incremental-reader-v3c/P/canonical-audit-overlay.portable.json'
assert sha(overlay.read_bytes()) == 'c0e56991804459ffc63b1229455c8a846747dcee577a1bd6df87c6d42acdcd34'
assert A.read_bytes() == overlay.read_bytes()
prior = E/'audit-before-independent-full-source-v3c.original.json'
assert prior.read_bytes() == git('show',f'{HEAD}:{A}')
audit = json.loads(A.read_bytes())
assert not semantic.validate_registry(semantic.load_registry())
publication.check_advance([audit['lean']['declaration']],reviewed=True)
cells = frontiers.load_cells()
errors = frontiers.validate_cells(cells)
expected = ['research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json: status independently_verified requires independent_verification']
assert errors == expected, errors
baseline = copy.deepcopy(cells)
for c in baseline:
    if c['__path__'] == str(C):
        old = json.loads(git('show',f'{HEAD}:{C}'))
        c.clear(); c.update(old); c['__path__'] = str(C)
assert frontiers.validate_cells(baseline) == expected

failure_sources = [W/'attach_full_source_review_v3c.attempt1.original.py',
                   W/'attach_full_source_review_v3c.attempt2.original.py',
                   W/'source-attachment-attempt1-diagnosis.json',W/'source-attachment-attempt2-diagnosis.json']
for stem in ['20261112T174403813674Z-source-matrix-variance-attach-full-independent-v3c',
             '20261112T174429197586Z-source-matrix-variance-attach-full-independent-v3c-v2']:
    p = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    r = json.loads(p.read_bytes())
    assert r['exit_code'] == 1 and sha(Path(r['log']).read_bytes()) == r['log_sha256']
    failure_sources.extend([p,Path(r['log'])])
for p in failure_sources:
    dest = E/'source-transfer-failed-attempts.originals'/p.name
    create(dest,p.read_bytes()); destinations.add(dest)
record = {
    'actual_math_commit': MATH, 'reader_commit': HEAD,
    'public_P_complete_original_overlay_sha256':sha(A.read_bytes()),
    'current_source_review':'Independent current v3c source-reviewed / child accepted; two informational elaboration deltas preserved exactly, no repairs.',
    'complete_original_custody':custody,
    'actual_reviewed_publication_validation':'passed',
    'actual_frontier_validation':'failed: same single pre-existing committed S field schema error; no own R9 error',
    'unchanged_baseline_frontier_errors':errors,
    'required_next_action':'Original independent S verifier prepares metadata-only correction retaining its full evidence object and immutable normal V event, no V replay; then rerun final metadata gates.',
    'normal_R9_PL_or_V_calls':0,'root_VERIFIED_calls':0,
    'private_T_public_registry_changes':0,'full_site_integration_purification_Goal_credit':False,
    'foreign_full_states_preserved':len(states),'foreign_frontiers_unchanged':len(b['all_existing_frontier_hashes']),
}
rp = E/'actual-independent-full-source-v3c-attachment.json'
create(rp,dump(record))
destinations.update([prior,rp,A,C])
paths = []
for p in sorted(destinations):
    old = subprocess.run(['git','show',f'{HEAD}:{p}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if old.returncode or old.stdout != p.read_bytes(): paths.append(p)
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(A),str(C)}
assert Path('runs/substantive_advances.jsonl').read_bytes() == ledger
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery
for p,h in b['all_existing_frontier_hashes'].items(): assert sha(Path(p).read_bytes()) == h,p
spec = W/'full-source-v3c-finalized-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines()) == set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(A),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry original variance source reviews and diagnose existing evidence field schema'],check=True)
commit = git('rev-parse','HEAD').decode().strip()
for p in paths: assert git('show',f'{commit}:{p}') == p.read_bytes()
assert not git('diff','HEAD','--name-only')
result = {**record,'source_metadata_commit':commit,'carried_changed_files':len(paths)}
create(W/'actual-independent-full-source-v3c-commit.json',dump(result))
print(json.dumps(result))
