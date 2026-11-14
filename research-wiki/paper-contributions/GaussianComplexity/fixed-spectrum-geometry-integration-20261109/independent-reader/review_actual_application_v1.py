"""Bounded actual application readback only; no APIs/build/browser/source verdict."""
from pathlib import Path
import ast, datetime, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
B = R / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-integration-20261109'
O = S / 'actual-application-readback-review-v1'
C = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
HEAD = '62813df927fd3c156dd57099cc11613074d91bc0'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
OWNER = 'huanjian_gc_20261109_fixed_spectrum_geometry'
INTEGRATOR = OWNER + '_integration'
VERIFIER = '/root/source_reader_9a6d2f'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry'
CELL = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json'
AP = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
LP = 'runs/substantive_advances.jsonl'; DP = 'runs/substantive_discoveries.jsonl'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *args: subprocess.check_output(['git', *args], cwd=R)
def readpin(path, digest):
    raw = path.read_bytes(); assert sha(raw) == digest, path
    return raw
def readref(ref):
    p = (R / ref['path']).resolve(); assert p.is_relative_to(R)
    return readpin(p, ref['sha256'])
def source_digest():
    d = hashlib.sha256()
    for p in [R / 'AutoSamplingTheory.lean', *sorted((R / 'AutoSamplingTheory').rglob('*.lean')),
              R / 'Tests.lean', *sorted((R / 'Tests').rglob('*.lean')),
              R / 'lakefile.lean', R / 'lean-toolchain', R / 'lake-manifest.json']:
        if p.exists():
            d.update(p.relative_to(R).as_posix().encode()); d.update(b'\0'); d.update(p.read_bytes()); d.update(b'\0')
    return d.hexdigest()
assert not O.exists() and git('rev-parse', 'HEAD').decode().strip() == HEAD
receipt_path = R / '.astis/huanjian-resume-20261103/20261109T020413438561Z-geometry-sole-STAB-exact-six-payload-application-v3.receipt.json'
receipt_raw = receipt_path.read_bytes(); receipt = json.loads(receipt_raw)
assert receipt['exit_code'] == 0 and receipt['head_before'] == receipt['head_after'] == HEAD
assert receipt['command'] == ['/opt/anaconda3/bin/python', '-B', '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/apply_reviewed_shared_v3.py']
log_raw = readpin(Path(receipt['log']), 'ce1a863eaeaa2b87616061451c7e0eea807a336f4f900e77de1b59eb1069a518')
assert sha(log_raw) == receipt['log_sha256']
log = json.loads(log_raw)
assert log == {'state': 'STABILIZING', 'normal_API_calls': 1, 'exact_shared_payloads': 6,
    'additional_lossless_own_metadata_object': 1, 'baseline_files_checked': 125851,
    'actual_source_digest': '6905b946089555464e4eedadfad3644fb4df3ee5d49ffc8445c16bb7fd997108', 'sourceV_reissued': False}
helper_raw = readpin(R / receipt['command'][2], '33d3be0ef4cf9c9bc7ed756b8509e39f2b323ff5881a2adf5e8ae8909030b702')
app_raw = readpin(B / 'exact-shared-application-receipt.json', '2e7a16cb5c5702ba29275ed9a6b8d30f7b6763a4c9ebd8daf69bf88345b9d14e')
app = json.loads(app_raw)
auth_raw = readpin(B / 'root-sole-STAB-application-authorization-v3.json', '58febf15b75ba9127954f4dc117e24fa1bffbae56fa23012456e79f20730ec75')
auth = json.loads(auth_raw)
assert auth['application_helper_sha256'] == sha(helper_raw)
assert auth['authorized_by'] == '/root' and auth['exact_six_path_application_authorized'] is True
assert auth['own_frontier_single_object_projection_authorized'] is True and auth['new_source_verdict'] is False
assert json.loads(readref(auth['independent_successor_review']))['verdict'] == 'ACCEPT_EXACT_UNAPPLIED_SUCCESSOR'
assert auth['source_V_first_carrying_commit'] == HEAD and auth['source_verifier'] == VERIFIER
source_manifest_raw = readref(auth['source_V_actual_execution_manifest'])
source_manifest = json.loads(source_manifest_raw)
assert sha(source_manifest_raw) == '4d56c5efebdb787bf9fd71d9213259b2d5ff7f1f7ff726e217b6554ca37fe07a'
assert source_manifest['normal_API_calls'] == 1 and source_manifest['actor'] == VERIFIER
Vraw = readref(auth['actual_source_V_append'])
assert sha(Vraw) == '7cd55a70605e1db1c8198f5f7a2eec6dbcb62b562becf539a80a9e5c632a501c'
stab_raw = readpin(B / 'sole-STAB-append.exact.jsonl', '271a16a8c9b44294515b4cfe790b5560bbc544d415846db76adce9330420ab88')
assert Vraw.endswith(b'\n') and stab_raw.endswith(b'\n') and len(Vraw.splitlines()) == len(stab_raw.splitlines()) == 1
V = json.loads(Vraw); stab = json.loads(stab_raw)
candidate_ledger = git('show', C + ':' + LP)
before = gzip.decompress((B / 'before-STAB-ledger.raw.jsonl.gz').read_bytes())
after = gzip.decompress((B / 'after-STAB-ledger.raw.jsonl.gz').read_bytes())
assert before == candidate_ledger + Vraw == git('show', HEAD + ':' + LP)
assert after == before + stab_raw == (R / LP).read_bytes()
assert after.count(Vraw) == 1 and after.count(stab_raw) == 1
assert sha(before) == app['ledger_before_sha256'] == auth['ledger_before_STAB_sha256']
assert sha(after) == app['ledger_after_sha256'] == '5b58146368803e26104d11892b5d29cd6862bda63bb41268bdbc07be2b94190b'
assert git('show', HEAD + '^:' + LP) == candidate_ledger
assert V['worker_id'] == V['evidence']['verifier_id'] == VERIFIER
assert (V['from_state'], V['to_state']) == ('PROVED_LOCAL', 'VERIFIED')
assert stab['event'] == 'transition' and stab['advance_id'] == ADV
assert (stab['from_state'], stab['to_state']) == ('VERIFIED', 'STABILIZING')
assert stab['worker_id'] == stab['evidence']['integration_owner'] == INTEGRATOR
assert stab['evidence']['verifier_id'] == VERIFIER and stab['evidence']['verified_commit'] == C
assert stab['evidence']['source_V_first_carrying_commit'] == HEAD
assert stab['evidence']['lean_declarations'] == stab['evidence']['publication_declarations'] == [DECL]
assert app['normal_API_calls'] == 1 and app['actor'] == INTEGRATOR and app['append_sha256'] == sha(stab_raw)
audit_raw = readref(auth['accepted_source_audit']); assert audit_raw == (R / AP).read_bytes() == git('show', HEAD + ':' + AP)
audit = json.loads(audit_raw)
assert sha(audit_raw) == 'a101634a005e20e54c8791cf340b871a3adf79807b75b607f422957392b0bc6c'
assert audit['source_review']['reviewer'] == VERIFIER and audit['lean']['formalizer'] == OWNER
assert len({VERIFIER, OWNER, INTEGRATOR, '/root', '/root/geometry_integration_reader', audit['reconstruction']['decoder']}) == 6
assert sha(readref(auth['source_review_run'])) == audit['source_review']['review_run_sha256']
source_projection_review = json.loads(readref(auth['source_V_own_frontier_projection_review']))
assert source_projection_review['verdict'] == 'ACCEPT_EXACT_MECHANICAL_SOURCE_V_PROJECTION'

proposal_raw = readpin(S / 'conditional-proposal-v1/proposal-report.json', '6f9045472dc9f11da494942d065b093efab12c2cf385f6d83a379ad771a5e904')
proposal = json.loads(proposal_raw)
assert app['exact_shared_payloads'] == proposal['shared_paths'] and len(app['exact_shared_payloads']) == 6
payload_rows = []
for row in proposal['shared_paths']:
    ref = row['planned_after_archive']; z = readpin(R / ref['path'], ref['gzip_sha256']); raw = gzip.decompress(z)
    assert sha(raw) == ref['raw_sha256'] == row['planned_after_sha256'] and (R / row['path']).read_bytes() == raw
    payload_rows.append({'path': row['path'], 'actual_sha256': sha(raw), 'exact_conditional_archive': True})
source_cell = gzip.decompress((B / 'sourceV-own-frontier.before.raw.json.gz').read_bytes())
current_cell = (R / CELL).read_bytes()
assert source_cell == git('show', HEAD + ':' + CELL) and sha(source_cell) == 'b040beefc7779754ff075dbd8de3c553f35d217a8923b193ebeeddcfe5465174'
assert current_cell == gzip.decompress((B / 'own-frontier.after.raw.json.gz').read_bytes())
projection_raw = readpin(B / 'actual-own-frontier-projection.json', '48dc5f179c0e08752079b3337ad6156c2a16508fec00c49c7311a35287e869aa')
projection = json.loads(projection_raw); assert projection == app['additional_own_frontier_metadata']
assert projection['sourceV_before_sha256'] == sha(source_cell) and projection['after_sha256'] == sha(current_cell)
assert projection['source_V_append_sha256'] == sha(Vraw) and projection['STAB_append_sha256'] == sha(stab_raw)
assert projection['authorized_by'] == '/root' and projection['new_mathematical_or_source_verdict'] is False
functions = [n for n in ast.parse(helper_raw).body if isinstance(n, ast.FunctionDef) and n.name in {'differences', 'spans', 'append_integration'}]
scope = {'json': json}; exec(compile(ast.Module(body=functions, type_ignores=[]), '<accepted-V3-pure-functions-only>', 'exec'), scope)
metadata = json.loads(current_cell)['evidence']['canonical_integration']
assert metadata == {'state': 'SOLE_STAB_EXACT_SIX_PATHS_APPLIED_ACTUAL_CORE_GATES_PENDING', 'owner': INTEGRATOR,
    'source_V_first_carrying_commit': HEAD, 'source_verifier_preserved': VERIFIER, 'proposal_report_sha256': sha(proposal_raw),
    'new_public_producer': DECL, 'private_Test_Registry_node': False, 'new_conceptual_transport': False, 'actual_STAB_append_sha256': sha(stab_raw)}
expected_cell, inverse = scope['append_integration'](source_cell, metadata)
assert expected_cell == current_cell and inverse == projection['insertion_inverse']
i = inverse['character_insertion_offset']; added = inverse['inserted_text']; text = current_cell.decode()
assert text[i:i + len(added)] == added and (text[:i] + text[i + len(added):]).encode() == source_cell
assert scope['differences'](json.loads(source_cell), json.loads(current_cell)) == projection['application_changed_json_paths'] == ['/evidence/canonical_integration']
whole_paths = scope['differences'](json.loads(git('show', C + ':' + CELL)), json.loads(current_cell))
assert whole_paths == projection['changed_json_paths'] == ['/evidence/canonical_integration', '/evidence/independent_verification', '/statement_seal/status', '/status']

br = proposal['protected_baseline']; compressed = readpin(R / br['path'], br['gzip_sha256']); baseline_raw = gzip.decompress(compressed)
assert sha(baseline_raw) == br['raw_sha256']; baseline = json.loads(baseline_raw)
tree = ast.parse((R / 'tools/astis_advance.py').read_text())
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'_replay_advances', '_replay_discoveries'}]
ns = {'Iterable': list, 'Any': object, 'NO_PROGRESS_FREEZE_AT': 3}
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<official-pure-replay-only>', 'exec'), ns)
states = ns['_replay_advances']([json.loads(x) for x in after.splitlines()])
assert [k for k, v in states.items() if v['state'] == 'STABILIZING'] == [ADV] and states[ADV]['owner_id'] == OWNER
assert {k: v for k, v in states.items() if k != ADV} == baseline['foreign_SAU_states']
discovery_raw = (R / DP).read_bytes(); assert sha(discovery_raw) == baseline['all_tracked'][DP]['sha256']
assert ns['_replay_discoveries']([json.loads(x) for x in discovery_raw.splitlines()]) == baseline['all_discovery_states']
for p, digest in baseline['all_frontier_raw_hashes'].items():
    assert sha((R / p).read_bytes()) == (sha(current_cell) if p == CELL else digest), p
assert {str(p.relative_to(R)) for p in (R / 'research-wiki/frontier-cells').glob('*.json')} == set(baseline['all_frontier_raw_hashes'])
for p, digest in baseline['all_models_before'].items(): assert sha((R / p).read_bytes()) == digest, p
readme = 'research-wiki/paper-contributions/GaussianComplexity/README.md'
assert sha((R / readme).read_bytes()) == baseline['all_tracked'][readme]['sha256']
for p, digest in proposal['source_Test_lesson_publication_pins'].items():
    if p not in [AP, LP]: assert sha((R / p).read_bytes()) == digest, p
assert app['candidate_baseline_files_checked_before_and_after'] == len(baseline['all_tracked']) == 125851
assert app['foreign_states_preserved'] == len(baseline['foreign_SAU_states']) == 285
assert app['foreign_raw_frontiers_preserved'] == len(baseline['all_frontier_raw_hashes']) - 1 == 444
assert app['README_discovery_models_source_audit_preserved'] is True
actual_digest = source_digest()
assert actual_digest == app['source_digest'] == proposal['predicted_source_digest_after_exact_proposed_Lean_payloads'] == log['actual_source_digest']
assert git('rev-parse', 'HEAD').decode().strip() == HEAD
O.mkdir()
for name, raw in [('actual-application-receipt.raw.json.gz', app_raw), ('actual-logger-receipt.raw.json.gz', receipt_raw),
                  ('actual-logger-log.raw.gz', log_raw), ('actual-own-frontier-projection.raw.json.gz', projection_raw),
                  ('actual-STAB-append.raw.jsonl.gz', stab_raw), ('actual-root-authorization.raw.json.gz', auth_raw)]:
    (O / name).write_bytes(gzip.compress(raw, mtime=0))
record = {'reviewer': '/root/geometry_integration_reader', 'verdict': 'ACCEPT_EXACT_ACTUAL_APPLICATION_READBACK_SCOPED',
 'scope': 'Independent bounded metadata/application readback only; no new sourceV, formal runtime gate or pixel acceptance.',
 'candidate_commit': C, 'source_V_first_carrying_commit': HEAD, 'HEAD_during_review': HEAD,
 'actual_application_receipt_sha256': sha(app_raw), 'actual_logger_receipt_sha256': sha(receipt_raw), 'actual_logger_log_sha256': sha(log_raw),
 'actual_helper_sha256': sha(helper_raw), 'actual_root_authorization_sha256': sha(auth_raw),
 'original_source_V_append_sha256': sha(Vraw), 'actual_STAB_append_sha256': sha(stab_raw),
 'original_source_audit_sha256': sha(audit_raw), 'actual_own_frontier_projection_sha256': sha(projection_raw),
 'actual_own_frontier_after_sha256': sha(current_cell), 'actual_ledger_after_sha256': sha(after), 'actual_source_digest': actual_digest,
 'checks': {'actual_successful_normal_STAB_calls': 1, 'new_source_V_calls': 0, 'sole_STAB': ADV, 'proofowner_preserved': OWNER,
    'original_source_verifier_preserved': VERIFIER, 'original_V_raw_prefix_unique_and_exact': True,
    'six_payloads': payload_rows, 'private_Test_new_public_or_Registry_node': False,
    'sourceV_to_current_only_JSON_path': ['/evidence/canonical_integration'], 'whole_candidate_to_current_paths': whole_paths,
    'own_cell_forward_inverse_raw_bytes_exact': True, 'old_source_math_parent_coverage_tokens_preserved': True,
    'foreign_states_independently_replayed': 285, 'foreign_frontier_raw_hashes_independently_checked': 444,
    'all_discoveries_exact': len(baseline['all_discovery_states']), 'models_raw_hashes_independently_checked': len(baseline['all_models_before']),
    'README_and_all_critical_source_Test_lesson_publication_pins_exact': True,
    'full_raw_baseline_receipt': 'Executed acceptedV3 helper, exact successful logger/command/head and application receipt verify125851 candidate raw checks both before/after; bounded review does not repeat unchanged4.8GB scan.'},
 'new_mathematical_or_source_verdict': False, 'reviewer_API_or_shared_mutations': False,
 'pending': ['Immutable integration-core packaging', 'Actual same-head official8 Lean/publication/contributor/semantic/frontier/site/graph gates',
    'New scoped Chrome/OS approval', 'Actual44 original PNGs/12 native geometry rows and separate independent original-image acceptance',
    'Remote owner release/delivery and postmerge purification/Exposition Seal; both main lower bounds remain open'],
 'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'actual-application-readback-ACCEPT.json').write_bytes(dump(record))
(O / 'review-driver.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': record['verdict'], 'report_sha256': sha((O / 'actual-application-readback-ACCEPT.json').read_bytes()),
    'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
    'new_sourceV_runtime_browser_pixel_acceptance': False}
(O / 'freeze.json').write_bytes(dump(freeze))
assert (R / CELL).read_bytes() == current_cell and (R / LP).read_bytes() == after and (R / AP).read_bytes() == audit_raw
print(json.dumps({'report': str((O / 'actual-application-readback-ACCEPT.json').relative_to(R)), 'report_sha256': freeze['report_sha256'],
    'freeze_sha256': sha((O / 'freeze.json').read_bytes()), 'verdict': record['verdict'], 'new_source_verdict': False}, indent=2))
