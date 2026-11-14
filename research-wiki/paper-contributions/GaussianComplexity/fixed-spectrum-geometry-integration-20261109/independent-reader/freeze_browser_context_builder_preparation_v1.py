"""Freeze schema/static preparation; do not execute the actual-facts builder."""
from pathlib import Path
import ast, datetime, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O = S / 'actual-browser-context-builder-preparation-v1'
assert not O.exists()
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
p = S / 'prepare_actual_browser_context_v1.py'
raw = p.read_bytes(); tree = ast.parse(raw)
compile(raw, str(p), 'exec')
assert not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr in {'transition_advance', 'launch', 'goto', 'current_advances', 'current_discoveries'} for n in ast.walk(tree))
assert '"execute_browser_authorized": True' not in raw.decode() and "'execute_browser_authorized': True" not in raw.decode()
assert "'authorized_by': None" in raw.decode() and "'execute_browser_authorized': False" in raw.decode()
assert raw.decode().index('sys.dont_write_bytecode = True') < raw.decode().index('spec.loader.exec_module(common)')
ref = {'type': 'object', 'required': ['path', 'sha256'], 'properties': {
    'path': {'type': 'string', 'minLength': 1}, 'sha256': {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}}, 'additionalProperties': False}
digest = {'type': 'string', 'pattern': '^[0-9a-f]{64}$'}
commit = {'type': 'string', 'pattern': '^[0-9a-f]{40}$'}
roles = ['canonical_lean', 'publication', 'contributor', 'semantic', 'frontier', 'site_build', 'site_check', 'graph_check']
properties = {
    'facts_kind': {'const': 'fixed-spectrum-geometry-actual-prebrowser-facts-v1'}, 'supplied_by': {'const': '/root'},
    'candidate_commit': {'const': 'ab8b47caed9f781191f8408154cd355c7e7c104c'},
    'publication_binding_sha256': {'const': '69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'},
    'proposal_report_sha256': {'const': '6f9045472dc9f11da494942d065b093efab12c2cf385f6d83a379ad771a5e904'},
    'browser_checker_sha256': {'const': 'e579e632b218e028310130e068230db3be8d0cca4d0e01714ea0f4b49c46268c'},
    'browser_common_sha256': {'const': '2be36d2794fa949989bbeee2db10606c68ff966ef1de27c2337b5b6a4c90ace0'},
    'source_verifier_to_preserve': {'const': '/root/source_reader_9a6d2f'},
    'integration_owner': {'const': 'huanjian_gc_20261109_fixed_spectrum_geometry_integration'},
    'accepted_immutable_core': commit, 'source_V_first_carrying_commit': commit,
    'candidate_source_digest': digest, 'source_digest': digest,
    'planned_original_PNGs': {'const': 44}, 'planned_native_geometry_rows': {'const': 12},
    'planned_old_DensityAffinity_DOM_regressions': {'const': 2},
    'actual_checks_before_browser': {'type': 'object', 'required': roles,
        'properties': {role: {'$ref': '#/$defs/artifactReference'} for role in roles}, 'additionalProperties': False}}
for name in ['source_V_append', 'STAB_append', 'source_V_actual_execution_manifest', 'accepted_source_audit',
             'source_review_run', 'own_frontier_current', 'own_frontier_projection_review', 'actual_gate',
             'site_metadata', 'sole_STAB_application_receipt']:
    properties[name] = {'$ref': '#/$defs/artifactReference'}
properties['source_V_own_frontier_projection_review'] = {'anyOf': [{'$ref': '#/$defs/artifactReference'}, {'type': 'null'}]}
schema = {'$schema': 'https://json-schema.org/draft/2020-12/schema',
    'title': 'Actual Geometry prebrowser facts supplied later by root; no authorization',
    'description': 'All artifact references must identify real immutable local evidence that already exists. Schema patterns are types, not placeholder future hash values. The builder also validates bytes, semantic relationships, candidate/current Git, actual one-call sourceV/STAB, full protected baseline and all eight gates. It emits a disabled candidate only.',
    'type': 'object', 'required': list(properties), 'properties': properties, 'additionalProperties': False,
    '$defs': {'artifactReference': ref}}
accessed = {n.slice.value for n in ast.walk(tree) if isinstance(n, ast.Subscript)
            and isinstance(n.value, ast.Name) and n.value.id == 'facts' and isinstance(n.slice, ast.Constant) and isinstance(n.slice.value, str)}
assert accessed <= set(properties), accessed - set(properties)
for old, expected in [('check_final_reader_v1.py', 'e579e632b218e028310130e068230db3be8d0cca4d0e01714ea0f4b49c46268c'),
                      ('geometry_browser_common_v1.py', '2be36d2794fa949989bbeee2db10606c68ff966ef1de27c2337b5b6a4c90ace0')]:
    assert sha((S / old).read_bytes()) == expected
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == 'ab8b47caed9f781191f8408154cd355c7e7c104c'
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=R)
O.mkdir()
(O / 'actual-browser-facts-v1.schema.json').write_bytes(dump(schema))
(O / 'builder.exact.raw.py.gz').write_bytes(gzip.compress(raw, mtime=0))
report = {'state': 'ACTUAL_BROWSER_CONTEXT_BUILDER_PREPARED_UNEXECUTED', 'preparer': '/root/geometry_integration_reader',
    'builder': str(p.relative_to(R)), 'builder_sha256': sha(raw),
    'input_schema': str((O / 'actual-browser-facts-v1.schema.json').relative_to(R)),
    'input_schema_sha256': sha((O / 'actual-browser-facts-v1.schema.json').read_bytes()),
    'future_values_invented': False, 'actual_facts_JSON_produced_now': False,
    'builder_executed_against_repository': False, 'fresh_entire_baseline_rescan_during_preparation': False,
    'checks_prepared_for_later_real_facts': ['Exact current-binding accepted audit, real source-review run, known distinct source reviewer/decoder/formalizer/root/reader/integrator',
        'Real sourceV manifest normal_API_calls1, actor, exact append, candidate, binding, accepted audit and source run hashes',
        'Exact candidate raw ledger plus sole actual V plus sole normal STAB, and actual one-call application receipt',
        'Separate sourceV own-cell review if needed, exact combined mechanical projection, inverse actual insertion and canonical metadata',
        'Current immutable core ancestry/source digest/current Git bytes, frozen code/Test/lesson/publication/parent/model/UI pins and current site assets',
        'All official8 real receipt/log hashes/head/exit checks and source-bound gate/site metadata via frozen common read-only guards',
        'Full original tracked baseline/foreign state/frontier/model/discovery preservation; README remains exact candidate/live/core before real browser acceptance'],
    'output_prepared_for_later': ['candidate-browser-authorization.DISABLED.json with authorized_by:null and execute_browser_authorized:false',
        'actual-context-validation-report.json with read-only validation scope', 'freeze.json with exact produced candidate/report hashes'],
    'mandatory_root_boundary': 'Root must inspect exact builder and the later actual facts/disabled output. This preparation and later context validation grant no root/browser/OS authorization. A separately created explicit authorization and NEW scoped OS approval are required before setting an execute flag.',
    'planned_browser_scope': {'original_PNGs': 44, 'native_geometry_rows': 12, 'old_DensityAffinity_DOM_regressions': 2,
        'desktop_mobile_widths': [1440, 390], 'pixel_acceptance': 'Actual originals require separate independent inspection; script PASS never certifies pixels.'},
    'frozen_checker_common_or_prior_reviews_modified': False,
    'no_sourceV_STAB_API_browser_OS_network_model_park_commit_or_shared_mutation': True,
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'preparation-report.json').write_bytes(dump(report))
(O / 'preparation-recorder.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': report['state'], 'report_sha256': sha((O / 'preparation-report.json').read_bytes()),
    'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
    'builder_actual_execution_or_browser_authorized': False}
(O / 'freeze.json').write_bytes(dump(freeze))
print(json.dumps({'builder_sha256': sha(raw), 'schema_sha256': report['input_schema_sha256'],
    'report_sha256': freeze['report_sha256'], 'freeze_sha256': sha((O / 'freeze.json').read_bytes()),
    'actual_builder_executed': False}, indent=2))
