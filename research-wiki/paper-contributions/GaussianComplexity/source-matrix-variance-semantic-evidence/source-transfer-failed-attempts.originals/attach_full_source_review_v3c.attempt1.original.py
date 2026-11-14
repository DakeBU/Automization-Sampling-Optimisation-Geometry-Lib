"""Carry complete independent originals; attach only current public P overlay."""
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
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-variance.json')
R = Path('.astis/semantic-neutral-20261112/mv_src_6e28')
OLD = R/'r9-full-consumer-source-review-v3a'
NEW = R/'incremental-reader-v3c'
LEDGER = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
MATH = 'e654e98642350a615c473bc8190fbc1d47fe52bd'
READER = '1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])
def create(p, raw):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as out:
        out.write(raw)
def checked(p, digest, size=None):
    assert p.is_file() and not p.is_symlink(), str(p)
    raw = p.read_bytes()
    assert sha(raw) == digest and (size is None or len(raw) == size), str(p)
    return raw

assert git('rev-parse', 'HEAD').decode().strip() == READER
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
b = json.loads((W/'continuation-after-shared-VERIFIED.private.json').read_bytes())
ledger_raw = LEDGER.read_bytes()
assert sha(ledger_raw) == b['ledger_sha256']
states = advance._replay_advances([json.loads(x) for x in ledger_raw.splitlines()])
assert states.pop(ADV)['state'] == 'EXPLORING' and states == b['all_foreign_states']
assert states['ASTIS-SA-20261112-RealMatrixPositiveIntegral']['state'] == 'VERIFIED'
for p, h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(discovery_raw) == json.loads((W/'continuation-discoveries.private.json').read_bytes())['ledger_sha256']

# Preflight all originals before any canonical metadata changes. Completed S is read-only.
plans = {}
def plan(source, dest, digest, size=None):
    assert not source.is_absolute() and '..' not in source.parts and source.is_relative_to(R)
    assert not dest.is_absolute() and '..' not in dest.parts
    raw = checked(source, digest, size)
    if dest.exists():
        assert not dest.is_symlink() and dest.read_bytes() == raw, str(dest)
    else:
        assert dest.is_relative_to(E), str(dest)
    if dest in plans:
        assert plans[dest] == raw
    plans[dest] = raw

manifest_records = []
for phase, digest, count in [
    (OLD, 'ba7533b3b3c03f5cd35097a22bb4782147307c2ca3f7262dcc9b11483ef2b005', 258),
    (NEW, '4bffe7a6bbbde331d808f7bce8d02bebf228f9ce98c51cc7c9ccabce2af3c241', 31),
]:
    mp = phase/'portable-custody-manifest.json'
    raw = checked(mp, digest)
    manifest = json.loads(raw)
    assert len(manifest['records']) == count
    for item in manifest['records']:
        plan(Path(item['source_path']), Path(item['destination_path']), item['sha256'], item['bytes'])
    destroot = E/'source-review/mv_src_6e28'/phase.name
    plan(mp, destroot/mp.name, digest)
    post = phase/'postseal-output-index.json'
    expected_post = ('fcf98f3ef1670098ab9e2131f5b141724d62e5e588a5126d28d4d4df39ebf680'
                     if phase == OLD else '5de45b4a3221ef5b93044ffa532ac1cdda339ea6079860e501f0847f0cf91181')
    postraw = checked(post, expected_post)
    for item in json.loads(postraw)['files']:
        source = Path(item['path'])
        assert source.is_relative_to(phase)
        plan(source, destroot/source.relative_to(phase), item['sha256'], item['bytes'])
    plan(post, destroot/post.name, expected_post)
    manifest_records.append({'manifest': str(destroot/mp.name), 'sha256': digest, 'records': count,
                             'postseal_index': str(destroot/post.name), 'postseal_sha256': expected_post})

overlayraw = checked(NEW/'P/canonical-audit-overlay.portable.json',
                     'c0e56991804459ffc63b1229455c8a846747dcee577a1bd6df87c6d42acdcd34')
overlay = json.loads(overlayraw)
auditraw = A.read_bytes()
audit = json.loads(auditraw)
assert overlay['id'] == audit['id']
for key in ['source', 'lean', 'reconstruction', 'publication_binding_sha256', 'publication_context']:
    assert overlay[key] == audit[key], key
assert overlay['candidate_commit'] == overlay['actual_math_commit'] == MATH
assert overlay['reader_commit'] == READER
assert overlay['publication_binding_sha256'] == '00bdeee242bd0c09802bbe1d7497da5da80c58d77f4ddb54df8196b5db27f1cf'
assert overlay['state'] == 'source-reviewed' and overlay['source_review']['state'] == 'accepted'
assert overlay['verdict'] == 'equivalent-after-elaboration' and overlay['deltas'] == overlay['repairs'] == []
assert semantic.decoder_packet(overlay) == semantic.decoder_packet(audit)
assert semantic.semantic_reviewer_packet(audit)['packet_sha256'] == '30aa93cad3d15b6a74c63b92683e16d1da148a2bd96b1981982f95cdfccf5861'
review = overlay['source_review']
assert review['reviewer'] == '/root/mv_fresh_source_6e28' and review['evidence']
checked(NEW/'P/reviewer-run.json', review['review_run_sha256'])
t = json.loads(checked(NEW/'T/private-consumer-source-decision.portable.json',
                       'd34f8e65595df2d881e09db52b70480bc58d39498f5992698610bd5626ea28db'))
assert t['state'] == 'source-reviewed' and t['source_review']['state'] == 'accepted'
assert t['source_review']['reviewer_packet_sha256'] == 'bc05d582ce5fd1042403a3574972162b29bbc86d2eac20803678cb12637a4f11'
checked(NEW/'T/reviewer-run.json', t['source_review']['review_run_sha256'])
registry = copy.deepcopy(semantic.load_registry())
matches = [x for x in registry['audits'] if x['id'] == audit['id']]
assert len(matches) == 1
matches[0].update(overlay)
assert not semantic.validate_registry(registry)

new_originals = []
for dest, raw in plans.items():
    if not dest.exists():
        create(dest, raw)
        new_originals.append(dest)
create(E/'audit-before-independent-full-source-v3c.original.json', auditraw)
A.write_bytes(overlayraw)
publication.inputs.cache_clear()
publication.load.cache_clear()
publication.check_advance([audit['lean']['declaration']], reviewed=True)

cell = json.loads(C.read_bytes())
assert cell['status'] == 'claimed' and cell['owner_id'] == 'huanjian_gc_20261112_source_matrix_variance'
cell['evidence']['independent_source_review'] = {
    'reviewer': review['reviewer'], 'actual_math_commit': MATH, 'reader_commit': READER,
    'public_P_audit': str(A), 'public_P_original_overlay_sha256': sha(overlayraw),
    'public_P_reviewer_packet_sha256': review['reviewer_packet_sha256'],
    'public_P_run_sha256': review['review_run_sha256'],
    'private_T_decision': str(E/'source-review/mv_src_6e28/incremental-reader-v3c/T/private-consumer-source-decision.portable.json'),
    'private_T_original_decision_sha256': 'd34f8e65595df2d881e09db52b70480bc58d39498f5992698610bd5626ea28db',
    'private_T_run_sha256': t['source_review']['review_run_sha256'],
    'complete_original_custody': manifest_records,
    'v3a_blocker_and_v3b_accepted_originals_preserved': True,
    'private_T_public_API_or_registry_credit': False,
}
cell['evidence']['private_consumer_final_source']['review'] = 'Independent whole-code and seven-slot source review accepted; current v3c incremental context accepted. Native/kernel/browser verification is separate and pending.'
cell['evidence']['shared_background_dependency_pending'] = {
    **cell['evidence']['shared_background_dependency_pending'],
    'new_compiled_parent_claimed': True, 'pending': False,
    'independent_shared_state': 'VERIFIED',
    'canonical_declaration': 'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef',
    'completion_memory': 'research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/local-cycle-memory.json',
}
cell['reader_contract']['status'] = 'Independent whole-code, source, seven-slot reconstruction and current v3c context accepted: four full public-P folds and three full private-T folds. Real native/kernel/browser acceptance remains separate. Public binding is the uncentered P only; private T gives no public API/main-result credit.'
cell['source_proof_coverage'] = {
    'inventory': str(E/'preproof-source-admission.json'),
    'reviewed_nodes': 'Original independent source graph and distinct topology challenge; all105 source atoms and67 source units retained. Full P/T code and25 mapped spans reviewed independently.',
    'excluded_with_reason': 'Original50 NODE/55 EXCLUDED records retained, including p15 concentration excluded.',
    'source_gaps': 'No genuine source gap found by the independent roles. Internal proof obligations are discharged in selected code; unselected OR alternatives are retained, not claimed proved.',
    'alternative_routes': ['Selected tensor continuous-linear-map transport; entrywise alternative retained unselected.', 'Selected actual-Y integrability from the existing public actual-matrix-mean provider; direct alternative retained unselected.'],
    'exact_source_and_Lean_map': str(E/'source-lean-map.full-consumer-v3b.draft.json'),
}
cell['proof_digestion'] = {
    'existing_substrate': 'Actual row marginal law, radial fourth moment, weighted half-grid frame, actual truncated matrix means, canonical real PSD integral; real selfadjoint matrix order and real continuous functional calculus.',
    'bookkeeping': 'Literal Y square and cutoff majorant, actual Bochner integrability, tensor moment/frame aggregate; noncommutative centering with both fixed multiplication integrals; deterministic cosine-square order; two true L2 operator norm conclusions.',
    'new_reusable': 'No new shared lemma in this R9 unit; the shared PSD expectation node belongs to its independently VERIFIED shared unit.',
    'new_topology': 'Actual original-product-experiment variance composition. Private centered and weighted consumer is implementation mathematics, with canonical public placement and downstream main consumer still integration/purification debt.',
}
cell['purification'] = {
    'status': 'pending',
    'dead_code_audit': 'Own actual proof-value check covers2 authored roots plus5 emitted internal helpers, closed/reachable with standard axioms; independent native inventory remains pending.',
    'duplicate_semantics_audit': 'Reuse canonical shared PSD integral and existing row/moment/frame/mean nodes. Historical private copies remain immutable pending serialized canonicalization.',
    'canonicalization': 'Public P retained once; T stays private Test consumer, never entered into the public registry as a second API.',
    'compressed_spine_delta': 'Actual law -> literal moment majorant -> PSD expectation/frame upper -> true noncommutative centering -> cosine contraction -> real spectral/operator norm bound.',
    'reader_default_view': 'Compact uncentered public statement; seven formula/proof folds include the clearly labelled private centered/weighted consequence, with exact complete P/T code drill-down.',
}
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
record = {
    'kind': 'Byte-exact original independent R9 full-source and incremental-reader review attachment',
    'actual_math_commit': MATH, 'reader_commit': READER,
    'public_P_original_overlay_sha256': sha(overlayraw), 'original_custody': manifest_records,
    'all_original_destinations_verified': len(plans), 'new_original_destinations': len(new_originals),
    'private_T_public_registry_changes': 0, 'root_VERIFIED_calls': 0, 'normal_R9_PL_or_V_calls': 0,
    'actual_reviewed_publication_validation': 'passed',
    'native_browser_full_site_integration_purification_Goal_credit': False,
    'foreign_full_states_preserved': len(states), 'foreign_regular_frontier_hashes_preserved': len(b['all_existing_frontier_hashes']),
}
recordpath = E/'actual-independent-full-source-v3c-attachment.json'
create(recordpath, dump(record))
assert LEDGER.read_bytes() == ledger_raw and Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery_raw
for p, h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(A), str(C)}
paths = [*new_originals, E/'audit-before-independent-full-source-v3c.original.json', A, C, recordpath]
spec = W/'full-source-v3c-transfer-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file='+str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(A), str(C)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Attach independent actual matrix variance source and stable reader reviews'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for p in paths:
    assert git('show', f'{commit}:{p}') == p.read_bytes()
assert not git('diff', 'HEAD', '--name-only')
result = {**record, 'source_metadata_commit': commit, 'carried_changed_files': len(paths)}
create(W/'actual-independent-full-source-v3c-commit.json', dump(result))
print(json.dumps(result))
