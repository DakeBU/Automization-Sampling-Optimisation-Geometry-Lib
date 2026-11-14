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
evidence = paper / 'source-matrix-mean-semantic-evidence'
cell_path = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-mean.json')
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
assert head == baseline['head'] == '90f3fe822621cba10350450798fae107b9c92335'
assert not git('diff', '--cached', '--name-only')
assert git('diff', 'HEAD', '--name-only').decode().splitlines() == [str(ledger)]
assert ledger.read_bytes() == git('show', f'{head}:{ledger}') + (evidence / 'normal-EXPLORING-append.exact.jsonl').read_bytes()
states = advance._replay_advances([json.loads(x) for x in ledger.read_bytes().splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean')['state'] == 'EXPLORING'
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


concept_root = Path('.astis/semantic-neutral-20261112/mm_tc_7f32/conceptual-v1')
concept_manifest = concept_root / 'freeze.json'
expected_concept = json.loads((workspace / 'expected-conceptual-original.json').read_bytes())
assert sha(concept_manifest.read_bytes()) == expected_concept['freeze_sha256']
frozen = json.loads(concept_manifest.read_bytes())
assert frozen['finding'] == 'none-found' and frozen['new_candidates'] == []
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

seal_path = paper / 'source-matrix-mean-statement-seal.json'
assert sha(seal_path.read_bytes()) == 'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b'
seal = json.loads(seal_path.read_bytes())
P, T = [Path(seal[k]['planned_file']) for k in ('producer', 'actual_private_consumer')]
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
assert sha(P.read_bytes()) == draft['producer_sha256']
assert sha(T.read_bytes()) == draft['private_consumer_sha256']

create(evidence / 'actual-local-mathematical-result.json', dump({
    'actual_compilation': draft['build'], 'actual_kernel': draft['kernel'],
    'literal_types_kernel_applied': True, 'raw_Expr_structural_equality': False,
    'owned_theorems': 3, 'handwritten_roots': 2, 'generated_reachable_internal': 1,
    'allowed_axioms_only': ['propext', 'Classical.choice', 'Quot.sound'],
    'canonical_actual_parent_edges': draft['actual_public_ASTIS_parents'],
    'formalizer_API_pristine': False, 'new_target_preseal_proof_attempts': 0,
    'normal_intake_receipt': '.astis/huanjian-resume-20261103/20261112T124409793898Z-source-matrix-mean-normal-intake.receipt.json',
    'actual_intake_readback_tool_chunk': '6d2689',
    'status': 'Unchanged sealed producer compiled first attempt; actual sum consumer compiled after two diagnosed proof-local elaboration/API fixes. Original strict kernel probe passed first attempt. Independent final source/native acceptance and normal PROVED_LOCAL pending.',
}))
create(evidence / 'local-attempt-diagnoses.json', dump({
    'sealed_statements_changed': False, 'formalizer_API_pristine': False,
    'preseal_formation_failures': 0,
    'preseal_definition_lookup_exposure': 'Overbroad definition-location lookup exposed adjacent standard theorem headers/proof fragments. Exact exposure and original tool chunk ids are retained from the first seal; no pristine API chronology asserted.',
    'reservation_description_failure': 'New unadmitted C description omitted literal Samplinglib/Mathlib labels required by the schema. Original C and exit1 retained; versioned v2 adds the actual library provenance labels only. Ledger unchanged before normal intake.',
    'post_admission_proof_API_lookup': 'ProofAPI exit1: Integrable.finset_sum and Matrix kronecker_sum/sum_kronecker names were unavailable. Actual integrable_finsetSum and linear-map sum rules were then inspected; rejected probe unchanged.',
    'producer_implementation_failures': 0,
    'consumer_implementation_failures': 2,
    'consumer_attempt1': 'Bare function annotation for proof-local t made field notation resolve to Function.transpose and omitted matrix multiplication. Version2 exposes definitionally equal Matrix annotation only, unchanged sealed statement.',
    'consumer_attempt2': 'Finset.smul_sum has implicit arguments; applying three positional placeholders failed. Version3 uses the same lemma by type inference, unchanged route and statements.',
    'consumer_first_failure_detailed_record': str(workspace / 'consumer-firstbuild-diagnosis.json'),
    'actual_strict_kernel_probe_failures': 0,
    'salvage': 'Actual first-moment producer and real two-sum consumer retained. Two handwritten roots and one emitted internal proof helper are all kernel-inspected, closed/reachable with standard axioms. No discarded mathematical fragment, extra source hypothesis, duplicate public radial/marginal lemma or assumption wrapper.',
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
for receipt_path in sorted(Path('.astis/huanjian-resume-20261103').glob('*-source-matrix-mean-*.receipt.json')):
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
slug = 'huanjian-gaussian-source-matrix-mean.json'
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
subprocess.run(['git', 'commit', '-m', 'Prove actual Gaussian truncated matrix means and both finite-sum expectations'], check=True)
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
