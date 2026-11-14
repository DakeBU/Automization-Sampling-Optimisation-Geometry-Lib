"""Refresh compact packet memory, preserving all existing queues and provenance."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])


def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)


head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'e8a9d12e3a1014efc1445d781027b217d96ab567'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
assert advance.current_advances()['ASTIS-SA-20261112-GaussianComplexitySourceRowLaw']['state'] == 'VERIFIED'
owner_path = evidence / 'last-formal-main-original-owner-observation.after-VERIFIED.json'
owner_raw = (workspace / 'latest-original-owner-after-independent-V.json').read_bytes()
create(owner_path, owner_raw)
raw_freezes = [
    ('.astis/semantic-neutral-20261112/ri_sg_78c2/raw-freeze-v1/frozen-manifest.json',
     '2bdc92ca14e919b33ec81f8480e8782bf0fe16e94fca4442e2f1e15ad040b351'),
    ('.astis/semantic-neutral-20261112/ri_tc_24a6/raw-freeze.json',
     'dc5f3b9278a7fe8d3eac246c794f0832ca157f4d9cf3b9c52443c28444e70ee9'),
]
for name, digest in raw_freezes:
    assert sha(Path(name).read_bytes()) == digest
memory = {
    'continuity': 'Same unfinished user Goal; previous weighted-frame local-cycle memory retained unchanged.',
    'previous_packet_memory': 'research-wiki/paper-contributions/GaussianComplexity/weighted-cosine-frame-semantic-evidence/local-cycle-memory.json',
    'mathematical_native_candidate': 'd0654e9bbed44ab852fc44598560799949d8bd12',
    'source_review_metadata_commit': '1280fad54b993b3ba888731387daa823a5b30d0b',
    'original_PLOCAL_carrier': 'f0511696ceb9f7c797ded1f5cdfd9eccf4ec5083',
    'native_review_metadata_carrier': '2c57883183937fdef1578a2b33e4ea892af2c694',
    'original_independent_VERIFIED_carrier': head,
    'actual_VERIFIED_append_sha256': 'f665dec771c757f8d2dba21c5b5c0b746d42387789c1beb224aad31c26aa164c',
    'local_result': 'Every actual coordinate-row map is measurable with exact standard Gaussian marginal; complete private same-product consumer proves the simultaneous source cutoff probability>=999/1000.',
    'q_zero': 'Included: r=1 and d>=2. No tau/kappa or positive-query premise.',
    'actual_compiled_parent_map': json.loads((evidence / 'publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents'],
    'new_owned': {'handwritten': 2, 'generated_internal': 2, 'all4_reachable': True},
    'native_closure': {'modules': 5, 'owned_types_and_bodies': 18, 'standard_axioms_only': True,
                       'older_authored_RadonNikodym_outside_this_consumer_closure_retained': 8},
    'formalizer_API_pristine': False,
    'source_originals': 103, 'native_archive_members': 334,
    'normal_verification_originals': 121, 'normal_verification_evidence_files': 126,
    'normal_VERIFIED_API_calls': 1, 'normal_API_exit': 0, 'postcheck_exit': 0,
    'frontier_pre_and_post_exit': [0, 0], 'root_VERIFIED_calls': 0,
    'full_PLOCAL_preservation': 'All20 fields preserved inline and original raw bytes unchanged.',
    'failure_provenance': 'Producer hidden-coordinate measurability and final ENNReal argument failures retained. Unreachable generated not_le cache removed from consumer simp list, unchanged strict kernel probe. Native four verifier-only causes retained. Independent count precheck failed before zero-V outcome inspection and versioned correction; successful API was never replayed.',
    'foreign_full_states_preserved': 305, 'all_discovery_full_states_and_ledger_preserved': 43,
    'older_regular_frontier_files_and_README_preserved': 465,
    'independent_other_tracked_files_preserved': 129882,
    'conceptual_mirror': 'No new source-backed correspondence. Both existing identities remain in their original merged/validated states; exact Gaussian library reuse does not create a conceptual Lean implication.',
    'original_owner_observation': str(owner_path),
    'global_integration': 'Latest main67aea8c4d5947cb0f4724cd4312cc81200177e04 still retains the original SlcLsiWeightedRadialMGF STABILIZING owner and the StatOT stabilizer. User selected original-owner completion/release; no takeover/shared integration/stale plan applied.',
    'next_mathematical_packet': 'Full joint independence of original physical Gaussian rows, consumed by measurability and independence of the literal Ex107 truncated matrices.',
    'next_status': 'Final literal Props formed only, with explicit finite real-entry matrix carrier. Not sealed, admitted or proved; no target proof search. Raw notes/preliminary graph are explicitly unaccepted until exact seal and binder/definition audit.',
    'next_raw_freezes': [{'path': name, 'sha256': digest} for name, digest in raw_freezes],
    'next_formation_receipt': '.astis/huanjian-resume-20261103/20261112T074709253066Z-source-row-independence-final-literal-Prop-formation-v4.receipt.json',
    'next_boundary': 'Marginal laws do not imply row joint independence. Yi differ by deterministic t_i, so independence is not iid. Same canonical product experiment only; closed cutoff and Gaussian-first paired indices preserved.',
    'remaining': [
        'Original row joint-independence and ambient/matrix-expectation adapters',
        'Public aggregate canonicalization, centered variance and matrix concentration',
        'Both main lower bounds and exact matvec/TV/precision/worst-query-cap/expected-cost adapters',
        'Serialized current-main/root Tests/Registry/source-index/global graph/site integration',
        'Actual desktop/mobile/MathJax/clipboard/download/public delivery',
        'Post-merge purification, Exposition Seal and final whole-paper acceptance',
    ],
    'whole_goal': 'unfinished',
}
memory_path = evidence / 'local-cycle-memory.json'
create(memory_path, dump(memory))
readme_path = evidence / 'README.md'
create(readme_path, (
    '# Original Gaussian row marginals and the simultaneous cutoff\n\n'
    'The public theorem proves measurability and exact standard Gaussian pushforward for each coordinate row of the canonical independent-column experiment. Its complete private consumer materially uses that theorem and the existing canonical exponential-moment node to prove the simultaneous closed-cutoff probability at least999/1000 under the same product measure. The standing range and q=0 are preserved.\n\n'
    'Independent raw/type/topology, whole-module, source-blind decoding, anti-anchored source/exposition review, five fresh native compilations and bounded production static rendering passed. The sole normal independent VERIFIED event is carried at e8a9d12e3a1014efc1445d781027b217d96ab567. Mathematical/native compile credit remains d0654e9, separately from later metadata carriers. All20 original local-proof fields and raw payload bytes survive unchanged. Known prior API exposure and all failed attempts remain disclosed; no pristine chronology is asserted.\n\n'
    'Six exact source-ordered folds, full private145-line export and local static links passed. Actual desktop/mobile/MathJax, source-index/globalgraph, clipboard/download/public delivery, serialized integration and purification remain open. The latest formal main still has the unreleased original stabilization owner; no stale integration plan was applied.\n\n'
    'The next bounded target is full row joint independence and actual truncated-matrix independence. Marginals alone cannot establish it. New Props have only been formed; preliminary source notes await the exact Statement Seal and binder/definition audit before formal topology admission. Both main bounds and all remaining oracle/precision/TV/cap/cost obligations remain unfinished.\n'
).encode())
process_paths = []
for source in sorted(workspace.iterdir()):
    if source.is_file() and source.suffix == '.py':
        dest = evidence / 'root-local-process-originals' / source.name
        create(dest, source.read_bytes())
        process_paths.append(dest)
process_manifest = evidence / 'root-local-process-originals/manifest.json'
create(process_manifest, dump({'files': [{'path': str(path), 'bytes': path.stat().st_size,
                                         'sha256': sha(path.read_bytes())} for path in process_paths],
                               'scope': 'Own process scripts only. Complete foreign/control snapshots remain local and private.'}))
paths = [owner_path, memory_path, readme_path, process_manifest, *process_paths]
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(memory_path), str(readme_path)], check=True)
subprocess.run(['git', 'commit', '-m', 'Record verified original-row cycle and next independence boundary'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
assert not git('diff', 'HEAD', '--name-only')
print(json.dumps({'cycle_memory_commit': commit, 'original_VERIFIED_carrier': head,
                  'owner_observation': json.loads(owner_raw), 'whole_goal': 'unfinished'}))
