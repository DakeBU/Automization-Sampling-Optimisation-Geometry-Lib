"""Freeze the compiled shared node and its actual, separately bound consumer.

No ledger transition, root verification, shared integration or Goal completion.
Complete foreign/control/index guards are read locally and never archived.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tarfile

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers

W = Path('.astis/huanjian-real-matrix-positive-integral-20261112')
W22 = Path('.astis/huanjian-gc-source-matrix-variance-20261112')
E = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
E22 = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
C22 = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
ledger = Path('runs/substantive_advances.jsonl')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
b = json.loads((W / 'candidate-boundary-v3.private.json').read_bytes())
assert head == b['head'] == '441d54ee96a6182374d2df3bf4d2fb096d5b7e14'
assert not git('diff', '--cached', '--name-only')
assert git('diff', 'HEAD', '--name-only').decode().splitlines() == [str(ledger)]
assert git('ls-files', '--stage').decode() == b['tracked_git_index']
assert ledger.read_bytes() == git('show', f'{head}:{ledger}') + (E22 / 'normal-EXPLORING-append.exact.jsonl').read_bytes() + (E / 'normal-EXPLORING-append.exact.jsonl').read_bytes()
states = advance._replay_advances([json.loads(x) for x in ledger.read_bytes().splitlines()])
assert states.pop('ASTIS-SA-20261112-RealMatrixPositiveIntegral')['state'] == 'EXPLORING'
assert states == b['all_foreign_states']
assert states['ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance']['state'] == 'EXPLORING'
discovery_guard = json.loads((W / 'preproof-discoveries.private.json').read_bytes())
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(discovery_raw) == discovery_guard['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()]) == discovery_guard['full_states']
for name, digest in b['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name
controls = json.loads((W / 'intake-controls.private.json').read_bytes())
for name, digest in controls.items():
    if name == str(C22):
        assert sha(Path(name).read_bytes()) == b['qualification']['only_authorized_active_consumer_cell_delta']['after_sha256']
    else:
        assert sha(Path(name).read_bytes()) == digest, name

concept = Path('.astis/semantic-neutral-20261112/mp_sg_52ad/conceptual-v1')
manifest = concept / 'freeze-manifest.json'
assert sha(manifest.read_bytes()) == 'a0f98f7f3085f263bb4a804ad07894044639cfad4e85099286fb5c4e89d82ec8'
concept_files = [manifest]
for item in json.loads(manifest.read_bytes())['files']:
    p = concept / item['path']
    assert p.is_relative_to(concept)
    raw = p.read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], str(p)
    concept_files.append(p)
for p in concept_files:
    create(E / 'conceptual-mirror-originals' / p.relative_to(concept), p.read_bytes())
judgment = json.loads((concept / 'RealMatrixPositiveIntegral.audit.json').read_bytes())
assert judgment['conceptual_mirror_audit']['status'] == 'none-found'
cell = json.loads(C.read_bytes())
cell['conceptual_mirror_audit'] = {
    'status': 'none-found', 'discovery_ids': [],
    'independent_reviewer': '/root/row_indep_source_graph_78c2',
    'evidence': str(E / 'conceptual-mirror-originals/RealMatrixPositiveIntegral.audit.json'),
    'boundary': 'Exact original bounded per-SAU conceptual judgment, not a compiler or new source acceptance; existing mirror identities/status preserved without revalidation.',
}
cell['graph_contribution']['functor_view'] = 'none-found'
cell['graph_contribution']['visual_review'] = 'Actual kernel-extracted S parents are empty; actual P has four canonical ASTIS parents including S. Source/Lean maps authored. Shared graph integration and visual acceptance await original stabilization owner release.'
boundary = 'Shared finite-real-matrix probability/integrability/AE-PSD background compiled and materially used in the actual original-experiment uncentered moment bound. Centered/weighted norm consumer remains unimplemented; final source/native acceptance, serialized integration, publication and purification remain open.'
cell['truth_boundary'] = boundary
cell['source_detail_audit']['fidelity_boundary'] = boundary
cell['learning_contract']['salvage'] = {
    'required': True, 'status': 'completed',
    'reason': 'The first implementation failed only because the standard Real StarOrderedRing instance import was absent. Adding its existing provider import compiled the unchanged statement and route. Original failed source/receipt retained.',
    'promoted_fragments': [cell['shared_floor_audit']['canonical_declaration']],
    'discarded_fragments': [],
}
cell['evidence']['independent_verification'] = ''
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())

draft = json.loads((E / 'coupled-publication-draft-record.json').read_bytes())
S, P = [Path(draft[k]['file']) for k in ('producer', 'actual_consumer')]
for key in ('producer', 'actual_consumer'):
    assert sha(Path(draft[key]['file']).read_bytes()) == draft[key]['file_sha256']
assert not Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean').exists()
seals = [Path('research-wiki/technical-lemmas/real-matrix-positive-integral-statement-seal.json'), Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')]
assert [sha(p.read_bytes()) for p in seals] == ['a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26', '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14']

originals = []
for w in (W22, W):
    review = json.loads((w / 'reviewed-preproof-inputs.json').read_bytes())
    for item in review['independent_originals']:
        p = Path(item['path'])
        raw = p.read_bytes()
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], str(p)
        originals.append(p)
    originals.extend(p for p in w.iterdir() if p.is_file() and not p.is_symlink() and '.private.' not in p.name)
originals += concept_files
for receipt_path in sorted(Path('.astis/huanjian-resume-20261103').glob('*.receipt.json')):
    if not any(label in receipt_path.name for label in ('-real-matrix-positive-integral-', '-source-matrix-variance-')):
        continue
    obj = json.loads(receipt_path.read_bytes())
    p = Path(obj['log']).resolve().relative_to(Path.cwd().resolve())
    assert sha(p.read_bytes()) == obj['log_sha256']
    originals.extend([receipt_path, p])
originals = sorted(set(originals))
for p in originals:
    assert p.is_file() and not p.is_symlink() and p.stat().st_size < 5_000_000
    assert '.private.' not in p.name
archive_path = E / 'preproof-source-types-topology-local-build.original-files.tar.gz'
with tarfile.open(archive_path, 'x:gz') as archive:
    for p in originals:
        archive.add(p, arcname=str(p), recursive=False)
with tarfile.open(archive_path, 'r:gz') as archive:
    for p in originals:
        assert archive.extractfile(str(p)).read() == p.read_bytes()
create(E / 'preproof-source-types-topology-local-build.original-manifest.json', dump({
    'files': {str(p): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in originals},
    'scope': 'Bounded own source/type/topology/conceptual and actual build originals. Full foreign/control/index snapshots stay private/local.',
}))
create(E / 'candidate-preservation-qualification.json', dump({
    'original_preproof_baseline_sha256': b['qualification']['original_sha256'],
    'postmath_boundary': b['qualification'],
    'foreign_full_states_preserved': len(states),
    'older_frontier_files_preserved_since_qualified_boundary': len(b['all_existing_frontier_hashes']),
    'discovery_states_and_raw_ledger_preserved': len(discovery_guard['full_states']),
    'foreign_controls_preserved': len(controls),
    'normal_root_VERIFIED_calls': 0, 'normal_local_proof_calls': 0,
    'R9_full_source_SAU_still_EXPLORING': True,
}))
files = [S, P, Path('Tests/RealMatrixPositiveIntegral.lean'), C, C22, *seals, ledger]
for slug in ('huanjian-real-matrix-positive-integral', 'huanjian-gaussian-source-matrix-variance'):
    files.extend(Path(root) / (slug + '.json') for root in ('website/content/declaration_lessons', 'website/content/publications', 'research-wiki/semantic-roundtrip/audits'))
files.extend(p for root in (E, E22) for p in sorted(root.rglob('*')) if p.is_file())
assert len(files) == len(set(files))
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
subprocess.run(['git', 'diff', '--cached', '--check', '--', *map(str, files[:14])], check=True)
subprocess.run(['git', 'commit', '-m', 'Prove shared real PSD integral positivity and actual Gaussian second moments'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for p in files:
    assert git('show', f'{commit}:{p}') == p.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record = {
    'mathematical_candidate': commit, 'parent': head,
    'producer': draft['producer'], 'actual_consumer': draft['actual_consumer'],
    'actual_build': draft['build'], 'actual_kernel': draft['kernel'],
    'original_archive_sha256': sha(archive_path.read_bytes()),
    'original_archive_files': len(originals), 'exact_carried_files': len(files),
    'foreign_full_states_preserved': len(states),
    'qualified_older_frontiers_preserved': len(b['all_existing_frontier_hashes']),
    'state': 'EXPLORING; compiled mathematics only, independent final semantic/native acceptance pending.',
    'root_VERIFIED_calls': 0,
}
create(W / 'actual-immutable-math-candidate.json', dump(record))
print(json.dumps(record))
