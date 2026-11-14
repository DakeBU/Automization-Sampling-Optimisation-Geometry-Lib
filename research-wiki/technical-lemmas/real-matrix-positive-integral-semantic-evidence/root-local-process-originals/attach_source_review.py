"""Carry complete original independent S and P-v2 source judgments, unmodified."""
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
E = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
E22 = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
phase = Path('.astis/semantic-neutral-20261112/mv_src_6e28/final-anti-anchored-phase')
ledger = Path('runs/substantive_advances.jsonl')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])
def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
assert head == '9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
before_ledger = ledger.read_bytes()
before_discoveries = Path('runs/substantive_discoveries.jsonl').read_bytes()
b = json.loads((W/'candidate-boundary-v3.private.json').read_bytes())
states = advance._replay_advances([json.loads(x) for x in before_ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-RealMatrixPositiveIntegral')['state'] == 'EXPLORING'
assert states == b['all_foreign_states']
for name, digest in b['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name

manifest_path = phase/'portable-custody-manifest.json'
manifest_raw = manifest_path.read_bytes()
assert sha(manifest_raw) == '01d51d9bc0ccab7ed6f82e50605882a10427179a7cce9a4ab07b30b41bd8f170'
manifest = json.loads(manifest_raw)
assert len(manifest['records']) == 140
assert sha((phase/'FINAL-ANTI-FROZEN.json').read_bytes()) == '73e2e3b62c9ac912b983a903b124def94fda3c64b59c72b4d15778647c3550ea'
files = []
dest_root = E/'source-review/mv_src_6e28/originals'
source_root = Path('.astis/semantic-neutral-20261112/mv_src_6e28')
for item in manifest['records']:
    p, dest = Path(item['source_path']), Path(item['destination_path'])
    assert not p.is_absolute() and '..' not in p.parts and p.is_relative_to(source_root)
    assert not dest.is_absolute() and '..' not in dest.parts and dest.is_relative_to(dest_root)
    assert p.is_file() and not p.is_symlink()
    raw = p.read_bytes()
    assert len(raw) == item['bytes'] and sha(raw) == item['sha256'], str(p)
    if dest.exists():
        assert dest.read_bytes() == raw and not dest.is_symlink()
    files.append((dest, raw))
assert len({str(p) for p,_ in files}) == len(files)

configs = [
    ('S', 'huanjian-real-matrix-positive-integral', E,
     'f8c75ec84e532ccebf2d4ca736d340f4e53c99452c334a96b8a0f5c5e1c86401',
     '5fa6bc71b0635cb54edb6a7ffac19435fe3ad5e875b65553dc2bd1614ad0e3a3',
     '33d30cf0a41a3246bfc864acbc6cde7537e2b7b7f5c734abb9eb7790b0a1ddc2',
     '607f16a85a561c33115e27455df0617022e8696c40a25569a77008c0b392f2a5'),
    ('P/v2', 'huanjian-gaussian-source-matrix-variance', E22,
     '49884675030b178d6c085df74a1b3be64297f8553c5ae40c41a623b7d16dc509',
     'acd49908a2a487fe6bbe0f26e3609bc0c3cb84b185cf0c681ee95d10385f91bd',
     'd2918c6a4b25cc8641a30dfd149a1f156b449a594493791ca1fa84bfd4074705',
     '0e719c90065882ba2db7012bbfcf86cb4af3dafaf3c44173828d676bae061cfa'),
]
updates, names, judgments = [], [], []
registry = copy.deepcopy(semantic.load_registry())
for label, slug, evidence, overlay_hash, packet_hash, run_hash, report_hash in configs:
    overlay_raw = (phase/label/'canonical-audit-overlay.portable.json').read_bytes()
    assert sha(overlay_raw) == overlay_hash
    overlay = json.loads(overlay_raw)
    assert overlay['state'] == 'source-reviewed' and overlay['source_review']['state'] == 'accepted'
    assert overlay['verdict'] == 'equivalent-after-elaboration'
    assert overlay['deltas'] == overlay['repairs'] == []
    assert overlay['source_review']['reviewer'] == '/root/mv_fresh_source_6e28'
    assert overlay['source_review']['reviewer_packet_sha256'] == packet_hash
    assert overlay['source_review']['review_run_sha256'] == run_hash
    assert overlay['source_review']['evidence']
    assert overlay['candidate_commit'] == head
    assert sha((phase/label/'reviewer-run.json').read_bytes()) == run_hash
    assert sha((phase/label/'review-report.md').read_bytes()) == report_hash
    audit_path = Path('research-wiki/semantic-roundtrip/audits')/(slug+'.json')
    old_raw = audit_path.read_bytes()
    audit = json.loads(old_raw)
    assert overlay['id'] == audit['id']
    assert overlay['publication_binding_sha256'] == audit['publication_binding_sha256']
    assert semantic.semantic_reviewer_packet(audit)['packet_sha256'] == packet_hash
    old_decoder = semantic.decoder_packet(audit)
    new = copy.deepcopy(audit)
    new.update(overlay)
    assert semantic.decoder_packet(new) == old_decoder
    matches = [a for a in registry['audits'] if a['id'] == audit['id']]
    assert len(matches) == 1
    matches[0].update(overlay)
    updates.append((audit_path, new, evidence, old_raw))
    names.append(audit['lean']['declaration'])
    judgments.append({'audit_id': audit['id'], 'report_sha256': report_hash,
        'run_sha256': run_hash, 'complete_original_overlay_sha256': overlay_hash,
        'publication_binding_sha256': audit['publication_binding_sha256'],
        'reviewer_packet_sha256': packet_hash, 'run_artifact': overlay['source_review']['run_artifact']})
for dest, raw in files:
    if not dest.exists():
        create(dest, raw)
self_dest = Path(manifest['manifest_self_destination'])
assert self_dest.is_relative_to(dest_root) and '..' not in self_dest.parts
create(self_dest, manifest_raw)
errors = semantic.validate_registry(registry)
assert not errors, errors
for audit_path, new, evidence, old_raw in updates:
    create(evidence/'audit-before-independent-source-review.original.json', old_raw)
    audit_path.write_bytes(dump(new))
publication.inputs.cache_clear()
publication.load.cache_clear()
publication.check_advance(names, reviewed=True)

cell = json.loads(C.read_bytes())
assert cell['status'] == 'claimed' and cell['evidence']['independent_verification'] == ''
cell['evidence']['independent_source_review'] = {
    'reviewer': '/root/mv_fresh_source_6e28', 'mathematical_candidate': head,
    'judgments': judgments, 'original_custody_manifest': str(self_dest),
    'original_custody_manifest_sha256': sha(manifest_raw),
    'terminal_seal_sha256': '73e2e3b62c9ac912b983a903b124def94fda3c64b59c72b4d15778647c3550ea',
}
cell['reader_contract']['status'] = 'Independent raw/type/whole-code/anti-anchored source and mathematical explanation accepted for S and actual uncentered P-v2. Three S and four P exact closed folds reproduce both modules. Native/browser validation separate; original-owner public site/source-index/graph integration and purification remain pending.'
cell['source_proof_coverage'] = {
    'inventory_archive': str(E/'preproof-source-types-topology-local-build.original-files.tar.gz'),
    'reviewed_nodes': 'Independent S source68atoms/50nodes/68edges and distinct topology challenge, then independent fresh raw/type/whole-module/two-anonymous-decoder anti-source review.',
    'excluded_with_reason': 'All68S atoms retain31NODE/37EXCLUDED. Generic authored background, upstream convex integral and actual primary-paper application remain separate. P follows its separately reviewed full R9 source graph; p15 is excluded.',
    'source_gaps': 'No genuine source gap claimed. Selected closed-convex applicability and actual uncentered residual are implemented; the direct Hermitian/quadratic alternative is unselected. Centered final module and wholeR9 are outside this packet.',
    'alternative_routes': ['closed-convex-set integral selected; direct Hermitian plus quadratic integration unselected'],
    'exact_source_and_Lean_maps': [str(E/'source-lean-map.draft.json'), str(E22/'source-lean-map.draft.json')],
}
cell['proof_digestion'] = {
    'existing_substrate': ['Convex.integral_mem', 'Matrix.posSemidef_iff_dotProduct_mulVec', 'Matrix.PosSemidef.smul', 'Matrix.PosSemidef.add'],
    'bookkeeping': ['PSD cone closed as Hermitian equalizer and all continuous quadratic halfspaces', 'Full finite real PSD convexity and exact L2Operator Bochner applicability', 'Actual P independently discharges residual integrability and PSD, ordinary square/tensor and finite expectation/frame identities'],
    'new_reusable': [names[0]],
    'new_topology': 'One canonical shared PSD expectation specialization is materially applied to the actual original-experiment P residual; conceptual analogy is not a Lean implication.',
}
cell['purification'] = {
    'status': 'pending', 'dead_code_audit': 'Own strict probe checks2 handwritten roots and2 emitted internal helpers closed/reachable with standard axioms. Independent native closure is separate.',
    'duplicate_semantics_audit': 'One public shared PSD integral node; older R4/R5 private applications remain immutable history with later canonicalization debt, not new generic copies.',
    'canonicalization': 'Shared probability finite-real PSD interface outside paper-specific route; concrete source conditions stay in actual caller.',
    'compressed_spine_delta': 'Full PSD cone geometry -> canonical convex expectation -> actual PSD residual expectation -> exact deterministic source frame upper bound.',
    'reader_default_view': 'Compact generic statement,3formula folds; separately bound actual uncentered source statement,4formula folds. Planned centered conclusions not awarded.',
}
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
record = {'kind': 'Byte-exact complete original independent source attachment',
    'mathematical_candidate': head, 'reviewer': '/root/mv_fresh_source_6e28',
    'judgments': judgments, 'portable_originals_copied': len(files),
    'original_manifest_sha256': sha(manifest_raw),
    'actual_core_schema_validation_errors': 0, 'actual_reviewed_publication_gate': 'passed',
    'code_Lean_source_decoder_lessons_bindings_unchanged': True,
    'root_PROVED_LOCAL_calls': 0, 'root_VERIFIED_calls': 0,
    'reader_and_full_R9_or_Goal_credit': False}
create(E/'actual-independent-source-review-attachment.json', dump(record))
assert ledger.read_bytes() == before_ledger
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == before_discoveries
for name, digest in b['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest, name
paths = [C, *[a for a,_,_,_ in updates]]
paths += [p for root in (E,E22) for p in sorted(root.rglob('*')) if p.is_file()]
changes = []
for p in paths:
    prior = subprocess.run(['git','show',f'{head}:{p}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if prior.returncode or prior.stdout != p.read_bytes():
        changes.append(p)
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(C), *[str(a) for a,_,_,_ in updates]}
subprocess.run(['git','add','-f','--',*map(str,changes)], check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines()) == set(map(str,changes))
subprocess.run(['git','diff','--cached','--check','--',str(C),*[str(a) for a,_,_,_ in updates]],check=True)
subprocess.run(['git','commit','-m','Attach independent shared PSD and actual uncentered Gaussian source reviews'],check=True)
commit = git('rev-parse','HEAD').decode().strip()
for p in changes:
    assert git('show',f'{commit}:{p}') == p.read_bytes()
assert not git('diff','HEAD','--name-only')
summary = {'mathematical_candidate':head, 'source_review_metadata_commit':commit,
    'byte_exact_source_originals':len(files), 'carried_changed_files':len(changes),
    'source_custody_sha256':sha(manifest_raw), 'root_VERIFIED_calls':0,
    'qualified_older_frontiers_preserved':len(b['all_existing_frontier_hashes'])}
create(W/'actual-independent-source-review-commit.json',dump(summary))
print(json.dumps(summary))
