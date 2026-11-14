"""Refresh exact local-cycle memory; preserve every older queue and original outcome."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
verdict = json.loads((workspace / 'actual-original-VERIFIED-commit.json').read_bytes())
assert head == verdict['immutable_original_VERIFIED_carrier'] == '91c5dee8052b1fa4059443e563d0960aea79ff95'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
states = advance.current_advances()
own = states.pop('ASTIS-SA-20261112-GaussianComplexitySourceRowIndependence')
assert own['state'] == 'VERIFIED'
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
assert states == baseline['all_foreign_states'] and len(states) == 306
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
guard = json.loads((workspace / 'preproof-discoveries.private.json').read_bytes())
assert sha(discovery_raw) == guard['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()]) == guard['full_states']
owner_path = evidence / 'last-formal-main-original-owner-observation.json'
owner = json.loads(owner_path.read_bytes())
next_seal_path = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-statement-seal.json')
assert sha(next_seal_path.read_bytes()) == 'b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b'
memory = {
    'continuity': 'Same unfinished user Goal; all previous packet memories and complete evidence retained.',
    'previous_packet_memory': 'research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence/local-cycle-memory.json',
    'mathematical_native_candidate': '66e0bb9b748d68816a8443d60696656c9340222f',
    'source_review_metadata_commit': 'dac347c5a32c892aed3992b1bcc83141172e7c39',
    'original_PLOCAL_carrier': 'c79ea9c0960c4366cfb9ba94cd079d6a74cfd8cd',
    'native_review_metadata_carrier': 'e5a4eadca4a6208e54cc90b7cb351e664f922cd5',
    'original_independent_VERIFIED_carrier': head,
    'actual_VERIFIED_append_sha256': verdict['actual_VERIFIED_append_sha256'],
    'local_result': 'Full joint independence of actual Gaussian physical rows in the canonical independent-column experiment. Material private consumer proves measurability and full independence of the exact locally truncated Ex107 matrices on that identical probability space.',
    'q_zero': 'Included: r=1,d>=2; sole logical premise2q+1<d. No tau/kappa/Gram/moment/measurability/independence certificate.',
    'actual_compiled_parent_map': json.loads((evidence / 'publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents'],
    'new_owned': {'handwritten': 2, 'generated_internal': 0, 'all2_reachable': True},
    'native_closure': {'fresh_modules': 3, 'owned_types_and_bodies': 3, 'standard_axioms_only': True},
    'first_mathematical_implementation_build_and_strict_probe': 'Both passed on first actual attempt with exact sealed types; actual receipts/logs retained.',
    'formalizer_API_pristine': False,
    'source_originals': 59, 'native_listed_files': 460, 'native_archive_members': 461,
    'normal_verification_originals': 75, 'normal_verification_evidence_files': 77,
    'normal_VERIFIED_API_calls': 1, 'normal_API_exit': 0, 'postcheck_exit': 0,
    'frontier_pre_and_post_exit': [0, 0], 'root_VERIFIED_calls': 0,
    'full_PLOCAL_preservation': 'All20 fields preserved inline and exact original raw bytes unchanged.',
    'failure_provenance': 'Two preseal type-formation failures and failed exploratory unqualified Measure namespace lookups retained; no target implementation failure. Native isolated Python import setup failure retained. Independent verifier local-main/origin-main and archive/local-olean prechecks failed before API, then versioned corrections passed. Root original/copy-path custody guard failed before writes, then byte-exact v2 passed; successful V never replayed. Original scripts/streams remain unchanged.',
    'foreign_full_states_preserved': 306, 'all_discovery_full_states_and_ledger_preserved': 43,
    'older_regular_frontier_files_and_README_preserved': 466,
    'independent_other_tracked_files_preserved': 130148,
    'conceptual_mirror': 'No new source-backed mechanism correspondence. Existing symmetry/radial identities and original merged/validated statuses retained. Marginal laws or symmetry alone are not joint independence; canonical compiled row-law node reused once.',
    'reader': 'Six exact initially closed production static folds, full81-line private source at L11 and original blankT60 passed. Independent source/code/decoding accepted. Actual desktop/mobile/MathJax/global source-index/graph/clipboard/interactive download/public delivery remain open.',
    'original_owner_observation': str(owner_path), 'owner_observed_utc': owner['checked_utc'],
    'global_integration': 'Actual fetched origin/mainab87352ce7689d885b49dd854a39e77a7c1cae6c still retains original SlcLsiWeightedRadialMGF STABILIZING and StatOT stabilizer. This observation predates V; no release inference or takeover. Shared integration remains HOLD per user original-owner choice.',
    'next_mathematical_packet': 'Actual original-experiment Yi integrability and first moments; material private actual integrals of the unweighted and cos((2q+1)theta)-weighted finite sums equal aI and0.',
    'next_seal': str(next_seal_path), 'next_seal_sha256': sha(next_seal_path.read_bytes()),
    'next_status': 'Exact literal Props formed and sealed before target proof search. Independent raw/type/source-graph freezes exist; distinct topology challenge and fresh-source phases pending. No next target implementation or normal intake yet.',
    'next_chronology': 'Global seal precedes SG raw freeze; raw precedes that actor first type exposure; type verdict precedes graph. Original ambiguous raw-phase label retained with separate exact qualification, never rewritten.',
    'remaining': [
        'Actual matrix expectation and arbitrary ambient adapters, public aggregate canonicalization',
        'Centered variance, matrix Bernstein/concentration and full Lemma4.4',
        'Both main lower bounds and exact matvec/TV/precision/worst-query-cap/expected-cost adapters',
        'Serialized current-main/root Tests/Registry/source-index/globalgraph/site integration',
        'Actual desktop/mobile/MathJax/clipboard/download/public delivery',
        'Post-merge purification, Exposition Seal and final whole-paper acceptance',
    ],
    'whole_goal': 'unfinished',
}
memory_path = evidence / 'local-cycle-memory.json'
create(memory_path, dump(memory))
readme_path = evidence / 'README.md'
create(readme_path, (
    '# Actual Gaussian row independence and truncated matrix images\n\n'
    'The public theorem proves full joint independence of the literal physical rows of the original independent-column Gaussian experiment. The real private consumer proves both measurability and full independence of the exact closed-cutoff Ex107 matrix images under that same measure. The standing source range and q=0 are preserved; the same existing canonical row-law node is reused.\n\n'
    'Both actual sealed targets compiled on their first implementation attempt and passed the strict literal kernel applications. Independent raw/type/topology, whole-module, source-blind decoding and anti-anchored source review passed. The separate fresh native actor compiled all three ASTIS modules from empty ASTIS outputs and checked all owned types/bodies/axioms. Its six production static folds and full81-line private source export include original blankT60. Native compile credit is66e0bb9; the sole normal independent VERIFIED event is carried at91c5dee8, preserving all20 original PLOCAL fields and raw bytes.\n\n'
    'Prior API exposure and every rejected formation, namespace, native setup, verifier precheck and root custody check are retained with their actual scope. No successful ledger transition was replayed. Static rendering does not grant actual desktop/mobile/MathJax/source-index/globalgraph/copy/download delivery, serialized integration or purification. Original stabilization ownership is still unreleased at the last actual remote observation.\n\n'
    'Next: actual source-experiment truncated matrix means and both actual finite-sum expectations. Exact literal statements are sealed, with independent source type/topology work in progress; no new target proof is claimed. Both main lower bounds and remaining oracle/precision/TV/cap/cost obligations remain unfinished.\n'
).encode())
process_paths = []
for source in sorted(workspace.glob('*.py')):
    dest = evidence / 'root-local-process-originals' / source.name
    create(dest, source.read_bytes())
    process_paths.append(dest)
runner = Path('.astis/huanjian-resume-20261103')
labels = [
    'source-originals-attachment', 'normal-PROVED-LOCAL', 'carry-original-PROVED-LOCAL',
    'formal-main-owner-after-local-proof', 'native-originals-and-held-carrier',
    'final-contributor', 'final-reviewed-publication', 'final-semantic', 'final-frontier',
    'carry-sole-original-VERIFIED', 'carry-sole-original-VERIFIED-v2',
]
for label in labels:
    matches = list(runner.glob('*-source-row-independence-' + label + '.receipt.json'))
    assert len(matches) == 1
    receipt_path = matches[0]
    receipt_raw = receipt_path.read_bytes()
    receipt = json.loads(receipt_raw)
    log_path = Path(receipt['log'])
    assert sha(log_path.read_bytes()) == receipt['log_sha256']
    assert receipt['exit_code'] == (1 if label == 'carry-sole-original-VERIFIED' else 0)
    for source in (receipt_path, log_path):
        dest = evidence / 'root-local-process-originals/actual-runs' / source.name
        create(dest, source.read_bytes())
        process_paths.append(dest)
manifest_path = evidence / 'root-local-process-originals/manifest.json'
create(manifest_path, dump({'files': [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in process_paths],
                            'scope': 'Own process scripts and exact post-candidate command receipts/streams only. Complete foreign/control/private snapshots remain local.'}))
paths = [memory_path, readme_path, manifest_path, *process_paths]
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(memory_path), str(readme_path)], check=True)
subprocess.run(['git', 'commit', '-m', 'Record verified Gaussian row independence and next matrix-mean boundary'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
assert not git('diff', 'HEAD', '--name-only')
create(workspace / 'actual-cycle-memory-commit.json', dump({'cycle_memory_commit': commit, 'original_VERIFIED_carrier': head}))
print(json.dumps({'cycle_memory_commit': commit, 'original_VERIFIED_carrier': head, 'whole_goal': 'unfinished'}))
