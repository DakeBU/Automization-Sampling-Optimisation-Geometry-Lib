"""Mechanical review of actual original-verifier V and exact own-cell projection; no source verdict/API."""
from pathlib import Path
import ast, datetime, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O = S / 'source-V-own-frontier-projection-review-v1'
N = R / '.astis/semantic-neutral-20261109/src_9a6d2f/normal-V-preparation'
X = N / 'execution'
C = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
OWNER = 'huanjian_gc_20261109_fixed_spectrum_geometry'
VERIFIER = '/root/source_reader_9a6d2f'
CELL = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json'
AP = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
LP = 'runs/substantive_advances.jsonl'
DP = 'runs/substantive_discoveries.jsonl'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args], cwd=R)
def check(path, expected):
    raw = path.read_bytes(); assert sha(raw) == expected, path
    return raw
assert not O.exists() and git('rev-parse', 'HEAD').decode().strip() == C
manifest_raw = check(X / 'execution-manifest.json', '4d56c5efebdb787bf9fd71d9213259b2d5ff7f1f7ff726e217b6554ca37fe07a')
manifest = json.loads(manifest_raw)
api_raw = check(X / 'normal-API-receipt.json', manifest['receipts']['normal_API_sha256'])
api = json.loads(api_raw)
assert sha(api_raw) == 'ad78897143370ce65966028264499bc10a97b975edfeca8f09cb9bd5142c7e2b'
assert api['returned_success'] is True and api['error'] is None
assert api['normal_API_calls_actual'] == manifest['normal_API_calls'] == 1
assert api['actor'] == manifest['actor'] == VERIFIER
assert api['normal_API'] == manifest['normal_API'] == 'tools.astis_advance.transition_advance'
check(N / 'normal_v_helper.py', '153aa271cd2e3a3115160f67560e469ae38097675fd87f00154e08b50cd64e73')
prep_raw = check(N / 'preparation-manifest.json', '85b4c63164f5eb25ed8de9d5a7b971d36d7f38be4d3547cc3d2d34bc71db39bd')
for row in json.loads(prep_raw)['files']:
    b = (N / row['path']).read_bytes(); assert len(b) == row['bytes'] and sha(b) == row['sha256'], row['path']
execution_payload = json.loads((X / 'execution-payload-manifest.json').read_bytes())
assert execution_payload['execution_manifest_sha256'] == sha(manifest_raw)
for row in execution_payload['files']:
    b = (X / row['path']).read_bytes(); assert len(b) == row['bytes'] and sha(b) == row['sha256'], row['path']
append = check(X / 'actual-V-append.raw.jsonl', '7cd55a70605e1db1c8198f5f7a2eec6dbcb62b562becf539a80a9e5c632a501c')
assert append.endswith(b'\n') and len(append.splitlines()) == 1
event = json.loads(append)
before_ledger = gzip.decompress((N / 'advance-ledger.before.raw.jsonl.gz').read_bytes())
after_ledger = (R / LP).read_bytes()
assert before_ledger == git('show', C + ':' + LP)
assert after_ledger == before_ledger + append == gzip.decompress((X / 'ledger.after-observed.raw.jsonl.gz').read_bytes())
assert sha(before_ledger) == manifest['before_ledger_sha256'] == api['before_ledger_sha256']
assert sha(after_ledger) == manifest['after_ledger_sha256'] == api['after_ledger_sha256'] == 'fc0ede4ba8ab651476231137e5077f23fdd8fc794a689571141811c3be5846f4'
assert sha(append) == manifest['exact_append_sha256'] == api['observed_append_sha256']
assert event['event'] == 'transition' and event['advance_id'] == ADV
assert (event['from_state'], event['to_state']) == ('PROVED_LOCAL', 'VERIFIED')
assert event['worker_id'] == event['evidence']['verifier_id'] == VERIFIER
assert event['evidence']['verified_commit'] == manifest['verified_commit'] == C
assert event['evidence'] == json.loads((N / 'planned-normal-api-evidence.json').read_bytes())
assert event['created_at'] == manifest['actual_V_append']['created_at_from_actual_API']
audit_raw = check(R / AP, 'a101634a005e20e54c8791cf340b871a3adf79807b75b607f422957392b0bc6c')
assert audit_raw == (N / 'accepted-audit.raw.json').read_bytes()
audit = json.loads(audit_raw)
assert audit['state'] == 'accepted' and audit['source_review']['reviewer'] == VERIFIER
assert audit['lean']['formalizer'] == OWNER and audit['reconstruction']['decoder'] == '/root/decode_80a1c2'
assert len({OWNER, VERIFIER, audit['reconstruction']['decoder'], '/root', '/root/geometry_integration_reader', OWNER + '_integration'}) == 6
run_path = R / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence/fresh-source-reader-9a6d2f/phase3/reviewer-run.json'
source_run_raw = check(run_path, '1e40574a0ace4e7477aff07046611e5bfe70d5747b98d07fd52681a3b0e7dadb')
assert sha(source_run_raw) == manifest['source_review_run_sha256'] == audit['source_review']['review_run_sha256']
assert json.loads(source_run_raw)['actor'] == VERIFIER
assert audit['publication_binding_sha256'] == manifest['publication_binding_sha256'] == event['evidence']['source_audit']['publication_binding_sha256']
assert sha(audit_raw) == manifest['accepted_audit_sha256'] == event['evidence']['source_audit']['accepted_audit_sha256']

old = check(N / 'own-cell.before.raw.json', '61b6d11ca37531af201bed9f4872b6024b3cf788ce2c7631b23078053e64a6e7')
new = check(N / 'own-cell.after.raw.json', 'b040beefc7779754ff075dbd8de3c553f35d217a8923b193ebeeddcfe5465174')
assert old == git('show', C + ':' + CELL) and new == (R / CELL).read_bytes()
projection_raw = check(N / 'own-cell-projection.json', '4b818345f3e2da7184ca2d51d187b46d5225e14398742917e9eaa17a89c5ce46')
projection = json.loads(projection_raw)
assert projection['before_sha256'] == sha(old) and projection['after_sha256'] == sha(new)
replacements = sorted(projection['raw_replacements'], key=lambda x: x['start_byte'])
assert len(replacements) == 3
forward = old; after_positions = []; shift = 0
for item in replacements:
    a, b = item['start_byte'], item['end_byte_exclusive']
    old_token = json.dumps(item['old_value'], ensure_ascii=False).encode()
    new_token = json.dumps(item['new_value'], ensure_ascii=False).encode()
    assert old[a:b] == old_token and sha(old_token) == item['old_json_utf8_sha256']
    assert sha(new_token) == item['new_json_utf8_sha256']
    after_positions.append((a + shift, old_token, new_token))
    shift += len(new_token) - len(old_token)
for item in reversed(replacements):
    a, b = item['start_byte'], item['end_byte_exclusive']
    forward = forward[:a] + json.dumps(item['new_value'], ensure_ascii=False).encode() + forward[b:]
assert forward == new
inverse = new
for a, old_token, new_token in reversed(after_positions):
    assert inverse[a:a + len(new_token)] == new_token
    inverse = inverse[:a] + old_token + inverse[a + len(new_token):]
assert inverse == old
v3 = check(R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/apply_reviewed_shared_v3.py', '33d3be0ef4cf9c9bc7ed756b8509e39f2b323ff5881a2adf5e8ae8909030b702')
node = next(n for n in ast.parse(v3).body if isinstance(n, ast.FunctionDef) and n.name == 'differences')
ns = {}; exec(compile(ast.Module(body=[node], type_ignores=[]), '<V3-differences-only>', 'exec'), ns)
changed = ns['differences'](json.loads(old), json.loads(new))
assert changed == ['/evidence/independent_verification', '/statement_seal/status', '/status']
old_obj = json.loads(old); new_obj = json.loads(new)
assert old_obj['owner_id'] == new_obj['owner_id'] == OWNER
assert old_obj['advance_id'] == new_obj['advance_id'] == ADV
assert 'canonical_integration' not in new_obj['evidence']
for k in ['target_statement', 'source_anchor', 'parents', 'consumers', 'source_proof_coverage', 'shared_floor_audit', 'conceptual_mirror_audit', 'purification']:
    assert old_obj[k] == new_obj[k], k
assert new_obj['status'] == 'independently_verified'
assert 'STATIC_ONLY' in new_obj['statement_seal']['status']
for phrase in ['strict-grid/Hessian route', 'parent standalone audit debt', 'Static reader only', 'integration/remote delivery and purification/Exposition Seal remain separate']:
    assert phrase in new_obj['evidence']['independent_verification']

# Bounded independent state/raw frontier/model/readme checks. The full 4.8GB
# raw baseline scan was already actually performed at the source helper's
# mutation boundary; do not repeat that unchanged whole scan here.
baseline_raw = gzip.decompress((N / 'protected-baseline.json.raw.gz').read_bytes())
assert sha(baseline_raw) == '72d216e64de710b7c244db790af1fc899b1d90eb3064d5172ba3518272588b92'
baseline = json.loads(baseline_raw)
tree = ast.parse((R / 'tools/astis_advance.py').read_text())
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'_replay_advances', '_replay_discoveries'}]
scope = {'Iterable': list, 'Any': object, 'NO_PROGRESS_FREEZE_AT': 3}
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<official-pure-replay-only>', 'exec'), scope)
states = scope['_replay_advances']([json.loads(row) for row in after_ledger.splitlines()])
assert states[ADV]['state'] == 'VERIFIED' and states[ADV]['owner_id'] == OWNER
assert not any(s['state'] == 'STABILIZING' for s in states.values())
assert {k: v for k, v in states.items() if k != ADV} == baseline['foreign_SAU_states']
discovery_raw = (R / DP).read_bytes()
assert sha(discovery_raw) == manifest['discovery_ledger_sha256'] == baseline['all_tracked'][DP]['sha256']
assert scope['_replay_discoveries']([json.loads(row) for row in discovery_raw.splitlines()]) == baseline['all_discovery_states']
for p, digest in baseline['all_frontier_raw_hashes'].items():
    assert sha((R / p).read_bytes()) == (sha(new) if p == CELL else digest), p
for p, digest in baseline['all_models_before'].items(): assert sha((R / p).read_bytes()) == digest, p
readme = 'research-wiki/paper-contributions/GaussianComplexity/README.md'
assert sha((R / readme).read_bytes()) == baseline['all_tracked'][readme]['sha256']
configuration = json.loads((N / 'configuration.json').read_bytes())
for p, digest in configuration['proof_and_publication_pins'].items():
    if p not in [AP, LP]: assert sha((R / p).read_bytes()) == digest, p
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {AP, CELL, LP}
assert manifest['tracked_preservation']['tracked_files'] == len(baseline['all_tracked']) == 125851
assert manifest['tracked_preservation']['all_unallowed_raw_tracked_bytes_preserved'] is True
assert manifest['tracked_preservation']['allowed_overrides'] == {AP: sha(audit_raw), LP: sha(after_ledger), CELL: sha(new)}
assert manifest['proof_owner'] == OWNER and manifest['foreign_state_preservation']['proof_owner_preserved'] is True

O.mkdir()
inputs = [('execution-manifest.raw.json.gz', manifest_raw), ('normal-API-receipt.raw.json.gz', api_raw),
          ('actual-V-append.raw.jsonl.gz', append), ('own-cell.before.raw.json.gz', old),
          ('own-cell.after.raw.json.gz', new), ('original-projection.raw.json.gz', projection_raw),
          ('preparation-manifest.raw.json.gz', prep_raw)]
for name, b in inputs: (O / name).write_bytes(gzip.compress(b, mtime=0))
record = {'reviewer': '/root/geometry_integration_reader', 'verdict': 'ACCEPT_EXACT_MECHANICAL_SOURCE_V_PROJECTION',
 'candidate_commit': C, 'source_V_append_sha256': sha(append), 'before_sha256': sha(old), 'after_sha256': sha(new),
 'changed_json_paths': changed, 'new_mathematical_or_source_verdict': False,
 'scope': 'Independent mechanical review only of the actual original-verifier one normal V and exact three-scalar own-cell projection. Source fidelity remains the original source actor9a6d2f judgment; no re-verification/renewed source verdict is issued.',
 'actual_evidence': {'execution_manifest_path': str((X / 'execution-manifest.json').relative_to(R)), 'execution_manifest_sha256': sha(manifest_raw),
    'normal_API_receipt_path': str((X / 'normal-API-receipt.json').relative_to(R)), 'normal_API_receipt_sha256': sha(api_raw),
    'normal_API_calls_actual': 1, 'actor': VERIFIER, 'event_time_from_actual_API': event['created_at'],
    'actual_ledger_sha256': sha(after_ledger), 'accepted_audit_sha256': sha(audit_raw), 'source_review_run_sha256': sha(source_run_raw)},
 'byte_projection': {'replacement_count': 3, 'exact_forward_reconstructs_current_after': True, 'exact_inverse_restores_candidate_before': True,
    'every_byte_outside_three_scalar_ranges_preserved': True, 'raw_CRLF_normalized': False,
    'old_source_math_seal_binders_parents_and_coverage_tokens_preserved': True,
    'status_meaning': 'Selected independently reviewed local geometry/static-reader sourceV only; integration/runtime/remote and source author alternate-route residuals remain explicit.'},
 'preservation_checks': {'candidate_old_ledger_prefix_exact': True, 'one_unique_normal_V_append': True,
    'proofowner_preserved': OWNER, 'foreign_states_exact': len(baseline['foreign_SAU_states']),
    'all_discoveries_exact': len(baseline['all_discovery_states']), 'foreign_frontier_raw_hashes_checked': len(baseline['all_frontier_raw_hashes']) - 1,
    'models_raw_hashes_checked': len(baseline['all_models_before']), 'README_and_all_critical_proof_publication_pins_exact': True,
    'current_changed_tracked_paths_exactly': [AP, CELL, LP],
    'source_helper_full_raw_preservation_receipt': 'Actual125851-file scan/allowed overrides verified from hash-pinned executed helper+manifest+normal API receipt; this bounded review did not repeat the unchanged4.8GB whole scan.'},
 'first_carrying_commit_created_or_checked': False, 'HEAD_during_review': C,
 'no_API_STAB_application_browser_OS_commit_or_shared_write_by_reviewer': True,
 'later_boundaries': 'Root first-carrying packaging and soleSTAB/exact application remain later. Immutable core official8 gates and actual44 originals/12 geometry rows/new scopedOS/independent pixels remain separate.',
 'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'mechanical-review-ACCEPT.json').write_bytes(dump(record))
(O / 'review-driver.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': record['verdict'], 'report_sha256': sha((O / 'mechanical-review-ACCEPT.json').read_bytes()),
    'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
    'new_source_verdict_or_API_authorization': False}
(O / 'freeze.json').write_bytes(dump(freeze))
assert (R / CELL).read_bytes() == new and (R / AP).read_bytes() == audit_raw and (R / LP).read_bytes() == after_ledger
print(json.dumps({'report': str((O / 'mechanical-review-ACCEPT.json').relative_to(R)), 'report_sha256': freeze['report_sha256'],
    'freeze_sha256': sha((O / 'freeze.json').read_bytes()), 'changed_json_paths': changed, 'verdict': record['verdict'],
    'new_source_verdict': False}, indent=2))
