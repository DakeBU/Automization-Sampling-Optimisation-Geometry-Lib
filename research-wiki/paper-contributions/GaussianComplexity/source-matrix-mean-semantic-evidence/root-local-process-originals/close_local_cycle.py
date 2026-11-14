"""Persist this bounded local result and its actual next boundary, preserving all older state."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-mean-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args])

def create(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(raw)

head = git('rev-parse', 'HEAD').decode().strip()
verdict = json.loads((workspace / 'actual-original-VERIFIED-commit.json').read_bytes())
assert head == verdict['immutable_original_VERIFIED_carrier'] == '13010966ab04fe4bc848ac6d9f06e89d684c83f1'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
states = advance.current_advances()
own = states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean')
assert own['state'] == 'VERIFIED'
baseline = json.loads((workspace / 'preproof-baseline.private.json').read_bytes())
assert states == baseline['all_foreign_states'] and len(states) == 307
for name, digest in baseline['all_existing_frontier_hashes'].items():
    assert sha(Path(name).read_bytes()) == digest
discovery_raw = Path('runs/substantive_discoveries.jsonl').read_bytes()
guard = json.loads((workspace / 'preproof-discoveries.private.json').read_bytes())
assert sha(discovery_raw) == guard['ledger_sha256']
assert advance._replay_discoveries([json.loads(x) for x in discovery_raw.splitlines()]) == guard['full_states']
next_seal = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
assert sha(next_seal.read_bytes()) == '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
memory = {
    'continuity': 'Same unfinished user Goal; all older queues, frontiers, complete payloads and packet memories retained.',
    'previous_packet_memory': 'research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence/local-cycle-memory.json',
    'mathematical_native_candidate': '5fb1440f771bdae77ad31f27b2275447fe3e89e5',
    'source_review_metadata_commit': '75d59375b9f87dfaea4de083249c0d93eef4942c',
    'original_PLOCAL_carrier': '121b50ab73aa362a148d2108ee607b76e82321d7',
    'native_review_metadata_carrier': '94116ada2dad7de1d31ca9c67189ee734a72ed16',
    'original_independent_VERIFIED_carrier': head,
    'actual_VERIFIED_append_sha256': verdict['actual_VERIFIED_append_sha256'],
    'local_result': 'Every literal actual closed-cutoff Ex107 Yi is Bochner integrable under the original independent-column product Gaussian law, with mean (a/d)(I tensor ti ti-transpose). Private consumer proves integrability of both actual finite sums and their actual expectations aI and0, including finite Bochner exchange.',
    'source_to_Lean_scope': 'Ex110 prints sums of expectations. The actual integrals of finite sums use an explicit internal integrability/exchange bridge. No independent-copy random variables or supplied formal means replace the original experiment.',
    'q_zero': 'Included; only premise2q+1<d. No row law, moment, integrability, independence, Gram, scalar-bias or ambient-transfer certificates.',
    'actual_compiled_parent_map': json.loads((evidence / 'publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents'],
    'new_owned': {'handwritten': 2, 'generated_internal': 1, 'all3_reachable': True},
    'native_closure': {'fresh_ASTIS_modules': 7, 'closed_full_types_and_bodies': 39, 'root_reachable': 32, 'older_generated_outside_root_closure_retained': 7, 'standard_axioms_only': True},
    'normal_verification': verdict,
    'source_originals': {'v1_files': 67, 'v2_files': 78, 'v1_unchanged': True, 'v2_qualification': 'Only evidence field schema compatibility; mathematical report and canonical packet hashes unchanged.'},
    'native_portable': {'payload_files': 440, 'archive_members': 441, 'own_receipts': 109, 'relevant_inputs': 50, 'tracked': 48, 'pinned_local': 2, 'large_local_dump_exported': False},
    'formalizer_API_pristine': False,
    'failure_provenance': 'Reservation metadata label mismatch retained; correction before intake. Post-admission API probe unknown names retained. P first0, T first1 (proof-local Matrix annotation), second1 (implicit smul_sum args), third0; sealed types unchanged. Strict first0. Source v1review_evidence/evidence schema mismatch preserved with independently authored v2 qualification. Native preparer/probe failures retained. Normal verifier API/pre/post all0 once. Root custody v1 assumed a prior packet metadata key and failed before writes; actual ledger readback confirmed one V, v2 checked the real verification_metadata_HEAD field and passed. No successful API replay.',
    'source_graph_routes': '13 preproof internal ports; CLM route selected and entrywise route unselected OR alternative, not a false AND or 13 separate proof credits. All required selected ports discharged by actual proof and independent source/native review.',
    'conceptual_mirror': 'No new cross-source mechanism correspondence. Canonical row, retained radial moment and cosine frame nodes reused, without second public lemma credit. Both older merged/validated conceptual records and exact statuses retained.',
    'reader': 'Six exact initially closed production static folds, full158-line private source at L17 including blankL157/endL158, and14 materialized local links/download targets passed bounded native static review. Actual desktop/mobile/MathJax/clipboard/runtime/download/globalsource-index/graph/public delivery remain open.',
    'original_owner_observation': str(evidence / 'last-formal-main-original-owner-observation.json'),
    'global_integration': 'Actual fetched origin/main4db0f863 at2026-11-12T13:07:23.963004Z still held SlcLsiWeightedRadialMGF and StatOT stabilizers. Local main a7cc differs. This observation predates normal V; no release inference or takeover. Wait for original owner per user choice.',
    'next_mathematical_packet': 'Actual original-experiment Yi squared integrability and uncentered PSD domination by C I; real private centered and cosine-weighted centered squared integrability and operator-norm variance bounds, C=2r(r+2)/d.',
    'next_seal': str(next_seal), 'next_seal_sha256': sha(next_seal.read_bytes()),
    'next_status': 'Literal Props formed0 and exact seal completed before new-target proof/API. Independent raw freezes preserved and post-seal binder/definition/type graph work requested. No next proof files, intake or new-target proof/API retrieval yet.',
    'next_source_locator': 'Z definitionp13; Ex113/114 and centered/cos² comparisons p14; entire Bernstein p15 excluded. Earlier p15 assignment wording retained as a corrected locator, not a mathematical source defect.',
    'remaining': ['Actual variance, bounded-summand radius and matrix Bernstein/concentration/full Lemma4.4', 'Arbitrary ambient and public aggregate canonicalization adapters', 'Both main lower bounds and exact matvec/TV/precision/worst-query-cap/expected-cost adapters', 'Serialized current-main/root Tests/Registry/source-index/globalgraphs/site integration', 'Actual desktop/mobile/MathJax/clipboard/download/public delivery', 'Post-merge purification, Exposition Seal and final whole-paper acceptance'],
    'whole_goal': 'unfinished',
}
memory_path = evidence / 'local-cycle-memory.json'
create(memory_path, dump(memory))
readme = evidence / 'README.md'
create(readme, (
    '# Actual Gaussian truncated matrix means\n\n'
    'The public theorem proves integrability and exact first moments of the literal Ex107 matrices under the original independent-column Gaussian experiment. The material private consumer proves both actual finite sums integrable and their Bochner expectations equal to aI and0. The standing source range includes q=0; canonical row-law, retained radial second moment and cosine Gram declarations are reused.\n\n'
    'The immutable mathematics is5fb1440f. Independent source-blind decoding, fresh source/type/whole-module review, seven-module fresh native builds and strict literal kernel applications passed. The sole normal independent VERIFIED append is carried at13010966; all20 PLOCAL fields and exact raw bytes remain intact, with307 foreign complete states,43 discovery complete states/ledger and467 older regular frontier files preserved. Root never invoked VERIFIED.\n\n'
    'All failed reservation/API/consumer/native/source-schema and root-custody attempts retain their original labels and streams. The source actor independently added a schema-compatible v2 overlay without changing its mathematical report. Static rendering is bounded evidence; actual desktop/mobile/MathJax, global graph/index, interactive copy/download and public delivery remain open. Original stabilization ownership is unreleased at the last actual remote observation; no takeover.\n\n'
    'Next is the exact original-experiment uncentered second-moment domination and both real centered variance operator-norm bounds. Its literal statements are sealed; independent source topology is pending, and no implementation or intake is claimed. Both main lower bounds, oracle/cost adapters, serialized integration, purification and whole-paper acceptance remain unfinished.\n'
).encode())
paths = [memory_path, readme]
for source in sorted(workspace.glob('*.py')):
    dest = evidence / 'root-local-process-originals' / source.name
    create(dest, source.read_bytes())
    paths.append(dest)
runner = Path('.astis/huanjian-resume-20261103')
labels = ['source-originals-attachment', 'normal-PROVED-LOCAL', 'carry-original-PROVED-LOCAL', 'formal-main-owner-after-math-candidate', 'native-originals-and-held-carrier', 'final-contributor', 'final-reviewed-publication', 'final-semantic', 'final-frontier', 'carry-sole-original-VERIFIED', 'carry-sole-original-VERIFIED-v2']
for label in labels:
    matches = list(runner.glob('*-source-matrix-mean-' + label + '.receipt.json'))
    assert len(matches) == 1
    receipt_path = matches[0]
    receipt = json.loads(receipt_path.read_bytes())
    log_path = Path(receipt['log'])
    assert sha(log_path.read_bytes()) == receipt['log_sha256']
    assert receipt['exit_code'] == (1 if label == 'carry-sole-original-VERIFIED' else 0)
    for source in [receipt_path, log_path]:
        dest = evidence / 'root-local-process-originals/actual-runs' / source.name
        create(dest, source.read_bytes())
        paths.append(dest)
manifest_path = evidence / 'root-local-process-originals/manifest.json'
create(manifest_path, dump({'files': [{'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in paths if p not in [memory_path, readme]], 'scope': 'Own process scripts and exact post-candidate command receipts/streams only; no full private foreign/control snapshots exported.'}))
paths.append(manifest_path)
subprocess.run(['git', 'add', '-f', '--', *map(str, paths)], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(memory_path), str(readme)], check=True)
subprocess.run(['git', 'commit', '-m', 'Record independently verified actual Gaussian means and next variance boundary'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
assert not git('diff', 'HEAD', '--name-only')
create(workspace / 'actual-cycle-memory-commit.json', dump({'cycle_memory_commit': commit, 'original_VERIFIED_carrier': head}))
print(json.dumps({'cycle_memory_commit': commit, 'original_VERIFIED_carrier': head, 'whole_goal': 'unfinished'}))
