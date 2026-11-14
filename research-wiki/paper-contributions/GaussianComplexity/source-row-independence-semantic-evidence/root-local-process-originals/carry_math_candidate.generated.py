"""Carry only this compiled packet and bounded original evidence."""
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

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
evidence = paper / 'source-row-independence-semantic-evidence'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-independence.json')
ledger = Path('runs/substantive_advances.jsonl')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
head = git('rev-parse', 'HEAD').decode().strip()
assert head == baseline['head'] == '6ef180f7495ef79e1f70bac7909036fc6f7f73bc'
assert not git('diff', '--cached', '--name-only')
assert git('diff', 'HEAD', '--name-only').decode().splitlines() == [str(ledger)]
assert ledger.read_bytes() == git('show', f'{head}:{ledger}') + (evidence / 'normal-EXPLORING-append.exact.jsonl').read_bytes()
states = advance._replay_advances([json.loads(x) for x in ledger.read_bytes().splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence')['state'] == 'EXPLORING'
assert states == baseline['all_foreign_states']
discoveries = Path('runs/substantive_discoveries.jsonl').read_bytes()
discovery_guard = json.loads((workspace / 'preproof-discoveries.private.json').read_bytes())
assert sha(discoveries) == discovery_guard['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discoveries.splitlines()]) == discovery_guard['full_states']
for path, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == digest, path
controls = json.loads((workspace / 'intake-controls.private.json').read_bytes())
for path, digest in controls.items():
    assert sha(Path(path).read_bytes()) == digest, path


concept_root = Path('.astis/semantic-neutral-20261112/ri_tc_24a6/conceptual-v1')
concept_manifest = concept_root / 'freeze.json'
assert sha(concept_manifest.read_bytes()) == '9dfef374661ee32ade97303841ff4da3a2e1bfa85acf03d578d78c8408327a03'
frozen = json.loads(concept_manifest.read_bytes())
assert frozen['finding'] == 'none-found' and frozen['new_candidates'] == 0
concept_files = [concept_manifest]
for item in frozen['local_records']:
    path = Path(item['path'])
    raw = path.read_bytes()
    assert path.parent == concept_root
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    concept_files.append(path)
for path in concept_files:
    create(evidence / 'conceptual-mirror-originals' / path.name, path.read_bytes())
cell = json.loads(cell_path.read_bytes())
cell['conceptual_mirror_audit'] = {
    'status': 'none-found', 'discovery_ids': [],
    'scope': 'Bounded NEW correspondence only; existing symmetry identities remain unchanged.',
    'evidence': str(evidence / 'conceptual-mirror-originals/judgment.json'),
    'independent_reviewer': '/root/row_indep_topology_24a6',
    'existing_validated_mirrors': frozen['existing_records_preserved_without_revalidation'],
}
cell['graph_contribution']['functor_view'] = 'none-found'
cell['graph_contribution']['visual_review'] = 'Exact compiled parent extraction and source/Lean map available. Shared graph integration/visual acceptance await original stabilization owner release.'
cell['evidence']['independent_verification'] = ''
cell_path.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())

seal_path = paper / 'source-row-independence-statement-seal.json'
assert sha(seal_path.read_bytes()) == '88a55849ce9e13a9a04edff6aac13ce32d4370712b1b7a422fba0d570ff0b25e'
seal = json.loads(seal_path.read_bytes())
P, T = [Path(seal[k]['planned_file']) for k in ('producer', 'actual_private_consumer')]
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
assert sha(P.read_bytes()) == draft['producer_sha256']
assert sha(T.read_bytes()) == draft['private_consumer_sha256']

create(evidence / 'actual-local-mathematical-result.json', dump({
    'actual_compilation': draft['build'], 'actual_kernel': draft['kernel'],
    'literal_types_kernel_applied': True, 'raw_Expr_structural_equality': False,
    'owned_theorems': 2, 'handwritten_roots': 2, 'generated_reachable_internal': 0,
    'allowed_axioms_only': ['propext', 'Classical.choice', 'Quot.sound'],
    'canonical_actual_parent_edges': draft['actual_public_ASTIS_parents'],
    'formalizer_API_pristine': False, 'new_target_preseal_proof_attempts': 0,
    'normal_intake_receipt': '.astis/huanjian-resume-20261103/20261112T080727870702Z-source-row-independence-normal-intake.receipt.json',
    'actual_intake_readback_tool_chunk': 'f7be51',
    'status': 'Both unchanged sealed mathematical targets compiled on first implementation attempt. Independent final source/native acceptance and normal PROVED_LOCAL pending.',
}))
create(evidence / 'local-attempt-diagnoses.json', dump({
    'sealed_statements_changed': False,
    'preseal_formation_failures': 'Two preseal Matrix-alias/measurable-instance formation failures retained; explicit finite-entry function carrier formed v3. Source-implicit measurable-Y output added before firstseal; finalv4 formed. No targetproof or theorem existed in those probes.',
    'definition_semantics': 'Kernel independence wrappers expanded in meaningv2, with finite-product constructor excerpts. Exact source/kernel sigma-field meanings retain all finite-family events.',
    'proof_API_probe': 'The exploratory ProofAPI.lean exit1 was only three unqualified infinitePi name lookups. Their actual namespace is MeasureTheory.Measure. Production uses the qualified existing declarations; both actual targets then compiled first attempt.',
    'producer_implementation_failures': 0, 'consumer_implementation_failures': 0,
    'actual_strict_kernel_probe_failures': 0,
    'orchestration_note': 'An initial functions.exec parser error occurred before any tool action while composing the kernel-probe writer. No Lean/build receipt was generated by that failed tool-call parse. Corrected orchestration created the real unchanged strict probe, whose actual run exited0.',
    'salvage': 'All actual mathematical work is in the two compiled roots; no generated owned helper, duplicate marginal-law proof, wrapper premise, new source assumption or discarded proof fragment.',
}))

review = json.loads((workspace / 'reviewed-preproof-inputs.json').read_bytes())
originals = []
for item in review['independent_originals']:
    path = Path(item['path'])
    raw = path.read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
    originals.append(path)
originals += concept_files
originals += [p for p in workspace.iterdir()
              if p.is_file() and not p.is_symlink() and '.private.' not in p.name]
for receipt_path in sorted(Path('.astis/huanjian-resume-20261103').glob('*-source-row-independence-*.receipt.json')):
    obj = json.loads(receipt_path.read_bytes())
    log = Path(obj['log']).resolve().relative_to(Path.cwd().resolve())
    assert sha(log.read_bytes()) == obj['log_sha256']
    originals += [receipt_path, log]
originals = sorted(set(originals))
for p in originals:
    assert p.is_file() and not p.is_symlink() and p.stat().st_size < 5_000_000
    assert '.private.' not in p.name
archive_path = evidence / 'preproof-source-types-topology-local-build.original-files.tar.gz'
with tarfile.open(archive_path, 'x:gz') as archive:
    for path in originals:
        archive.add(path, arcname=str(path), recursive=False)
with tarfile.open(archive_path, 'r:gz') as archive:
    for path in originals:
        assert archive.extractfile(str(path)).read() == path.read_bytes()
create(evidence / 'preproof-source-types-topology-local-build.original-manifest.json', dump({
    'files': {str(path): {'bytes': path.stat().st_size, 'sha256': sha(path.read_bytes())} for path in originals},
    'scope': 'Bounded own source/type/topology/conceptual and actual build originals. Complete foreign preservation/control replays remain private and local.',
}))
slug = 'huanjian-gaussian-source-row-independence.json'
files = [P, T, cell_path, seal_path, ledger,
         Path('website/content/declaration_lessons') / slug,
         Path('website/content/publications') / slug,
         Path('research-wiki/semantic-roundtrip/audits') / slug,
         *sorted(p for p in evidence.rglob('*') if p.is_file())]
assert len(files) == len(set(files))
subprocess.run(['git', 'add', '-f', '--', *map(str, files)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, files))
authored = [P, T, cell_path, seal_path, *files[5:8]]
subprocess.run(['git', 'diff', '--cached', '--check', '--', *map(str, authored)], check=True)
subprocess.run(['git', 'commit', '-m', 'Prove original Gaussian row independence and actual truncated-matrix independence'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for path in files:
    assert git('show', f'{commit}:{path}') == path.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
record = {
    'mathematical_candidate': commit, 'parent': head,
    'producer_sha256': draft['producer_sha256'], 'private_consumer_sha256': draft['private_consumer_sha256'],
    'publication_binding_sha256': draft['publication_binding_sha256'],
    'source_lean_map_sha256': sha((evidence / 'source-lean-map.draft.json').read_bytes()),
    'archive_sha256': sha(archive_path.read_bytes()), 'original_archive_files': len(originals),
    'exact_carried_files': len(files), 'foreign_full_advance_states_preserved': len(states),
    'all_discovery_states_preserved': len(discovery_guard['full_states']),
    'older_frontier_regular_files_preserved': len(baseline['all_existing_frontier_hashes']),
    'foreign_controls_preserved': len(controls), 'formalizer_API_pristine': False,
    'state': 'EXPLORING. Exact bounded mathematics compiled; independent final semantic/native acceptance pending.',
}
create(workspace / 'actual-immutable-math-candidate.json', dump(record))
print(json.dumps(record))
