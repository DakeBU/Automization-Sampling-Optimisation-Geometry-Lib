"""Authorized recording only: two distinct artifacts; no transition/API/browser/shared write."""
from pathlib import Path
import ast, datetime, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
P = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109'
S = P / 'independent-reader'
O = S / 'local-acceptance-and-eligibility-v1'
B = R / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-integration-20261109'
C = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
CORE = 'b3581af0fc7e517e6cf5b883f4af064ddaa72aa2'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
OWNER = 'huanjian_gc_20261109_fixed_spectrum_geometry'
INTEGRATOR = OWNER + '_integration'
VERIFIER = '/root/source_reader_9a6d2f'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry'
BINDING = '69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
DIGEST = '6905b946089555464e4eedadfad3644fb4df3ee5d49ffc8445c16bb7fd997108'
AP = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
CP = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json'
LP = 'runs/substantive_advances.jsonl'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
canonical = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
git = lambda *args: subprocess.check_output(['git', *args], cwd=R)
refs = {}
def readpin(key, path, expected):
    raw = path.read_bytes(); assert sha(raw) == expected, path
    refs[key] = {'path': str(path.relative_to(R)), 'sha256': expected}
    return raw
def readref(key, ref):
    return readpin(key, R / ref['path'], ref['sha256'])
assert O.is_dir() and not (O / 'local-integration-acceptance-v1.json').exists()
grant_path = P / 'root-local-acceptance-and-normalpark-eligibility-authorization-v1.json'
grant_raw = readpin('recording_authorization', grant_path, '6b545b5e6dc2e6a6ee57168dc427250fdc74420dd8878a39d2fee909ae8eaaa9')
grant = json.loads(grant_raw)
assert grant['authorized_by'] == '/root' and grant['recording_actor'] == '/root/geometry_integration_reader'
assert grant['authorization_kind'] == 'record-actual-local-integration-acceptance-and-separate-normalpark-eligibility'
assert grant['record_local_acceptance'] is True and grant['record_separate_normalpark_eligibility'] is True
assert grant['API_or_park_execution_authorized'] is False and grant['new_source_verdict'] is False
assert grant['immutable_core'] == CORE and grant['source_digest'] == DIGEST and grant['publication_binding_sha256'] == BINDING
assert git('rev-parse', 'HEAD').decode().strip() == CORE
pixel_raw = readref('independent_actual44_pixel_acceptance', grant['independent_actual44_review']); pixel = json.loads(pixel_raw)
assert pixel['reviewer'] == '/root/geometry_integration_reader' and pixel['verdict'] == 'ACCEPT'
assert pixel['immutable_core'] == CORE and pixel['source_digest'] == DIGEST
assert pixel['independent_original_review']['actual_originals_individually_viewed'] == 44
assert not pixel['blocking_visual_defects'] and pixel['new_mathematical_or_source_verdict'] is False
root8_raw = readref('root_actual8_original_acceptance', grant['root_actual8_review']); root8 = json.loads(root8_raw)
assert root8['reviewer'] == '/root' and root8['core'] == CORE
assert root8['verdict'] == 'ACCEPT_REPRESENTATIVE8_ORIGINALS_SCOPED' and len(root8['actually_opened_originals']) == 8
browser_path = S / 'browser/live-20261109T023719009047Z/report.json'
browser_raw = readpin('actual_approved_browser44_report', browser_path, '303524312bf5933ed8746ea2730d73d53e21e1255cf86c25386e3d80461fb997')
browser = json.loads(browser_raw)
assert browser['head'] == CORE and browser['status'] == 'passed' and browser['source_digest'] == DIGEST
assert browser['UI_repair'] is None and browser['external_GitHub_HTML_checked'] is False
assert len(browser['screenshots']) == 44 and len(browser['native_selection_geometry']) == 12
image_hashes = {row['file']: row['sha256'] for row in browser['screenshots']}
assert all(image_hashes[row['file']] == row['sha256'] for row in root8['actually_opened_originals'])
browser_auth_raw = readref('actual_browser_execution_authorization', browser['authorization'])
browser_auth = json.loads(browser_auth_raw)
assert browser_auth['accepted_immutable_core'] == CORE and browser_auth['execute_browser_authorized'] is True
assert browser_auth['new_source_verdict'] is False and browser_auth['parking_authorized'] is False
gate_refs = {}
assert set(browser_auth['actual_checks_before_browser']) == {'canonical_lean','publication','contributor','semantic','frontier','site_build','site_check','graph_check'}
for role, ref in browser_auth['actual_checks_before_browser'].items():
    raw = readref('actual_gate_' + role, ref); row = json.loads(raw)
    assert row['exit_code'] == 0 and row['head_before'] == row['head_after'] == CORE
    assert sha(Path(row['log']).read_bytes()) == row['log_sha256']
    gate_refs[role] = {**ref, 'head': CORE, 'exit_code': 0, 'log_sha256': row['log_sha256']}
app_review_path = S / 'actual-application-readback-review-v1/actual-application-readback-ACCEPT.json'
app_review_raw = readpin('independent_actual_application_readback', app_review_path, '130cff0d51188864acc51c110e72439cb478b5a1d6332ab357c4289b9a8e9e0a')
assert json.loads(app_review_raw)['verdict'] == 'ACCEPT_EXACT_ACTUAL_APPLICATION_READBACK_SCOPED'
application_auth = json.loads((B / 'root-sole-STAB-application-authorization-v3.json').read_bytes())
audit_raw = readref('original_accepted_source_audit', application_auth['accepted_source_audit'])
assert sha(audit_raw) == grant['accepted_source_audit_sha256'] == 'a101634a005e20e54c8791cf340b871a3adf79807b75b607f422957392b0bc6c'
audit = json.loads(audit_raw)
assert audit['source_review']['reviewer'] == grant['original_source_verifier'] == VERIFIER
assert audit['lean']['formalizer'] == OWNER and audit['publication_binding_sha256'] == BINDING
source_run_raw = readref('original_source_review_run', application_auth['source_review_run'])
assert sha(source_run_raw) == audit['source_review']['review_run_sha256']
source_V_execution = json.loads(readref('original_actual_source_V_execution_manifest', application_auth['source_V_actual_execution_manifest']))
assert source_V_execution['actor'] == VERIFIER and source_V_execution['normal_API_calls'] == 1
assert source_V_execution['verified_commit'] == C and source_V_execution['accepted_audit_sha256'] == sha(audit_raw)
first_V_commit = application_auth['source_V_first_carrying_commit']
assert first_V_commit == '62813df927fd3c156dd57099cc11613074d91bc0'
Vraw = readref('original_actual_V_append', application_auth['actual_source_V_append'])
stabraw = readpin('actual_sole_STAB_append', B / 'sole-STAB-append.exact.jsonl', '271a16a8c9b44294515b4cfe790b5560bbc544d415846db76adce9330420ab88')
assert sha(Vraw) == grant['original_V_append_sha256'] == '7cd55a70605e1db1c8198f5f7a2eec6dbcb62b562becf539a80a9e5c632a501c'
assert sha(stabraw) == grant['STAB_append_sha256']
V = json.loads(Vraw); stab = json.loads(stabraw)
assert V['worker_id'] == V['evidence']['verifier_id'] == VERIFIER and V['evidence']['verified_commit'] == C
assert (V['from_state'], V['to_state']) == ('PROVED_LOCAL', 'VERIFIED')
assert stab['worker_id'] == stab['evidence']['integration_owner'] == INTEGRATOR
assert (stab['from_state'], stab['to_state']) == ('VERIFIED', 'STABILIZING')
ledger_raw = (R / LP).read_bytes(); candidate_prefix = git('show', C + ':' + LP)
assert ledger_raw == candidate_prefix + Vraw + stabraw == git('show', CORE + ':' + LP)
assert sha(ledger_raw) == '5b58146368803e26104d11892b5d29cd6862bda63bb41268bdbc07be2b94190b'
assert ledger_raw.count(Vraw) == ledger_raw.count(stabraw) == 1
refs['current_ledger'] = {'path': LP, 'sha256': sha(ledger_raw)}
cell_raw = (R / CP).read_bytes(); assert cell_raw == git('show', CORE + ':' + CP)
refs['current_own_cell'] = {'path': CP, 'sha256': sha(cell_raw)}
assert audit_raw == git('show', CORE + ':' + AP)
tree = ast.parse((R / 'tools/astis_advance.py').read_text())
node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_replay_advances')
ns = {'Iterable': list, 'Any': object, 'NO_PROGRESS_FREEZE_AT': 3}
exec(compile(ast.Module(body=[node], type_ignores=[]), '<official-pure-replay-only>', 'exec'), ns)
states = ns['_replay_advances']([json.loads(row) for row in ledger_raw.splitlines()])
assert states[ADV]['state'] == 'STABILIZING' and states[ADV]['owner_id'] == OWNER
assert [k for k, v in states.items() if v['state'] == 'STABILIZING'] == [ADV]
for p, digest in browser['input_pins'].items(): assert sha((R / p).read_bytes()) == digest, p
history_path = B / 'actual-delivery-evidence-manifest.json'; history_raw = history_path.read_bytes()
assert sha(history_raw) == 'e309ab8d132972ea0a2672ab4659f9060aaa3a68a8f905b3e04706484b9f90e8'
history = json.loads(history_raw)
assert history['local_acceptance_or_normalpark_or_new_source_verdict'] is False
assert history['independent44pixel_acceptance'] == 'pending separate report; script PASS not pixels'
refs['historical_delivery_manifest_unchanged'] = {'path': str(history_path.relative_to(R)), 'sha256': sha(history_raw)}
pixel_limits = pixel['scope_limits_and_nonblocking_observations']
boundary = 'Selected actual C4 geometry plus real private fixed-input Borel reply consumer only. Author strict-grid/Hessian route, parent standalone source/audit debt, joint hidden-input/adaptive/private-seed/history/transcript/output laws, target-law/TV/finite precision, deterministic caps and explicit expected costs, moments/Krylov and both full main lower bounds remain separate. Remote owner release/delivery, postmerge purification/Exposition Seal and whole Goal remain open.'
time = datetime.datetime.now(datetime.timezone.utc).isoformat()
acceptance = {'schema_version': 1, 'recording_actor': '/root/geometry_integration_reader',
    'status': 'ACCEPTED_SCOPED_LOCAL_INTEGRATION', 'recorded_utc': time,
    'authorization': refs['recording_authorization'], 'immutable_core': CORE, 'candidate_commit': C,
    'source_V_first_carrying_commit': first_V_commit,
    'source_digest': DIGEST, 'publication_binding_sha256': BINDING,
    'declaration': DECL, 'advance_id': ADV, 'proof_owner': OWNER,
    'original_source_verifier': VERIFIER, 'original_V_append_sha256': sha(Vraw), 'STAB_append_sha256': sha(stabraw),
    'accepted_source_audit_sha256': sha(audit_raw), 'original_V_evidence_canonical_sha256': sha(canonical(V['evidence'])),
    'scope': 'Actual same-immutable-core local software and own-site desktop1440/mobile390 reader delivery accepted for the selected one-node result. This records the already separately accepted sourceV/application/gates/browser/original-image layers without issuing a new source verdict.',
    'actual_acceptance_evidence': {'independent_application_readback': refs['independent_actual_application_readback'],
        'official8_same_core_gates': gate_refs, 'approved_browser44_report': refs['actual_approved_browser44_report'],
        'independent_all44_original_pixel_acceptance': refs['independent_actual44_pixel_acceptance'],
        'root_representative8_original_acceptance': refs['root_actual8_original_acceptance']},
    'actual_reader_scope': {'original_PNGs': 44, 'desktop_originals': 22, 'mobile_originals': 22, 'native_geometry_rows': 12,
        'native_rows_with_originals': 8, 'extra_native_DOM_only_rows': 4, 'old_DensityAffinity_DOM_only_regressions': 2,
        'source_and_module_delivery': 'Own-site local HTTP/source/module/downloads only; GitHub syntax and external GitHub HTML branches both unexecuted.',
        'pixel_limits_preserved_verbatim': pixel_limits},
    'state_recorded': {'current_state': 'STABILIZING', 'current_integration_owner': INTEGRATOR,
        'proofowner_unchanged': True, 'candidate_prefix_plus_original_V_plus_one_STAB_exact': True,
        'original_V_evidence_fields_unchanged': True},
    'historical_record_boundary': {'record': refs['historical_delivery_manifest_unchanged'],
        'meaning': 'Retained exact EXECUTED/PENDING-at-creation history. This new acceptance is an additional layer; the old manifest and root8 pending-at-creation wording are not overwritten or retroactively upgraded.'},
    'truth_boundary': boundary, 'new_source_verdict': False, 'API_or_normalpark_execution_authorized': False,
    'remote_publication_purification_Seal_main_bounds_or_Goal_complete': False}
accept_path = O / 'local-integration-acceptance-v1.json'; accept_path.write_bytes(dump(acceptance))
accept_ref = {'path': str(accept_path.relative_to(R)), 'sha256': sha(accept_path.read_bytes())}
eligibility = {'schema_version': 1, 'recording_actor': '/root/geometry_integration_reader',
    'status': 'ELIGIBLE_FOR_SEPARATE_EXACT_NORMALPARK_REVIEW_ONLY', 'recorded_utc': time,
    'authorization': refs['recording_authorization'], 'local_integration_acceptance': accept_ref,
    'immutable_core': CORE, 'candidate_commit': C, 'source_digest': DIGEST, 'publication_binding_sha256': BINDING,
    'source_V_first_carrying_commit': first_V_commit,
    'advance_id': ADV, 'declaration': DECL, 'proof_owner': OWNER,
    'current_state': 'STABILIZING', 'current_integration_owner': INTEGRATOR,
    'only_eligible_original_actor': VERIFIER,
    'eligible_transition_under_later_separate_grant': {'from_state': 'STABILIZING', 'to_state': 'VERIFIED', 'worker_id': VERIFIER,
        'meaning': 'Mechanical release back to the existing independently sourced V. It is not a new source review, a new theorem or a second original sourceV.'},
    'eligibility_is_API_or_execution_authorization': False, 'normal_API_calls_authorized_by_this_artifact': 0,
    'new_source_verdict': False, 'normalpark_executed': False,
    'must_preserve': {'original_source_verifier': VERIFIER, 'original_verified_commit': C,
        'original_V_append': refs['original_actual_V_append'], 'original_V_evidence_canonical_sha256': sha(canonical(V['evidence'])),
        'original_V_evidence_fields_exact': V['evidence'], 'original_V_audit': refs['original_accepted_source_audit'],
        'original_accepted_audit_raw_sha256': sha(audit_raw), 'sole_STAB_append': refs['actual_sole_STAB_append'],
        'all_old_raw_ledger_prefix_bytes': refs['current_ledger'], 'proof_owner': OWNER,
        'foreign_state_frontier_model_discovery_source_bytes': 'All original protected baselines remain; no broad own/foreign audit/model exception.'},
    'requires_before_any_normalpark_execution': ['Original source verifier prepares a bounded actual-facts helper with no state mutation during preparation.',
        'Independent exact helper/evidence/preservation review and real preflight only after these acceptance/eligibility artifacts exist.',
        'A separate concrete root execution grant bound to the exact reviewed helper, actual evidence hashes, original actor and one intended normal API event.',
        'At execution, original V evidence keys/values and raw prefix remain exact; any local acceptance evidence is a separate additional layer. No reissued source verdict, replacement verifier, manual append or foreign mutation.'],
    'accepted_reader_limits_preserved_verbatim': pixel_limits,
    'historical_delivery_manifest_not_rewritten': refs['historical_delivery_manifest_unchanged'],
    'truth_boundary': boundary, 'remote_owner_release_publication_purification_Seal_main_bounds_or_Goal_complete': False}
elig_path = O / 'normalpark-eligibility-v1.json'; elig_path.write_bytes(dump(eligibility))
elig_ref = {'path': str(elig_path.relative_to(R)), 'sha256': sha(elig_path.read_bytes())}
manifest = {'state': 'TWO_SEPARATE_AUTHORIZED_RECORDS_FROZEN_NO_API_EXECUTION', 'recording_actor': '/root/geometry_integration_reader',
    'immutable_core': CORE, 'source_digest': DIGEST, 'publication_binding_sha256': BINDING,
    'local_integration_acceptance': accept_ref, 'separate_normalpark_eligibility': elig_ref, 'evidence_refs': refs,
    'actual8gate_receipts_read_existing_not_rerun': True, 'actual44pixels_not_repeated': True,
    'unchanged4_8GB_whole_baseline_not_rescanned': True, 'current_sourceV_STAB_cell_audit_code_pins_checked': True,
    'API_calls_by_this_recording': 0, 'normalpark_execution_authorized': False, 'new_source_verdict': False,
    'shared_or_historical_files_written': False}
(O / 'evidence-manifest.json').write_bytes(dump(manifest))
(O / 'root-recording-authorization.raw.json.gz').write_bytes(gzip.compress(grant_raw, mtime=0))
freeze = {'state': manifest['state'], 'local_integration_acceptance_sha256': accept_ref['sha256'],
    'normalpark_eligibility_sha256': elig_ref['sha256'], 'evidence_manifest_sha256': sha((O / 'evidence-manifest.json').read_bytes()),
    'files': [{'path': str(p.relative_to(R)), 'sha256': sha(p.read_bytes())} for p in sorted(O.iterdir()) if p.is_file()],
    'normalpark_or_API_executed': False}
(O / 'freeze.json').write_bytes(dump(freeze))
assert (R / LP).read_bytes() == ledger_raw and (R / CP).read_bytes() == cell_raw and (R / AP).read_bytes() == audit_raw
assert history_path.read_bytes() == history_raw and git('rev-parse', 'HEAD').decode().strip() == CORE
print(json.dumps({'local_integration_acceptance': accept_ref, 'normalpark_eligibility': elig_ref,
    'evidence_manifest_sha256': freeze['evidence_manifest_sha256'], 'freeze_sha256': sha((O / 'freeze.json').read_bytes()),
    'API_or_park_executed_or_authorized': False}, indent=2))
