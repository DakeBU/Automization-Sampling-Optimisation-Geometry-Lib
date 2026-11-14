"""One guarded normal PL call after exact independent mathematics/source/reader closure."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as pub
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json')
SP = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-statement-seal.json')
L = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic'
OWNER = 'huanjian_20261114_matrix_bernstein_exponential'
MATH = '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff'
READER = '9a8b163f4753a1329dbc0435c1e7f810f729c349'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
spec = importlib.util.spec_from_file_location('bernstein_private_preservation_guard', W / 'preservation_guard.private.py')
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)
head = git('rev-parse', 'HEAD').decode().strip()
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
assert not (W / 'normal-PROVED_LOCAL-attempted.once.json').exists()
cfg = json.loads((W / 'normal-PL-inputs.json').read_bytes())
assert cfg['metadata_commit'] == head
frozen = {x['path']: x['sha256'] for x in cfg['frozen_inputs']}
assert len(frozen) == len(cfg['frozen_inputs'])
for p, h in frozen.items():
    assert sha(Path(p).read_bytes()) == h
def frozen_ref(ref):
    assert frozen.get(ref['path']) == ref['sha256'], 'mandatory evidence not frozen'
    data = Path(ref['path']).read_bytes()
    assert sha(data) == ref['sha256']
    return data
def frozen_json(ref):
    return json.loads(frozen_ref(ref))
before = L.read_bytes()
assert before == git('show', f'{head}:{L}')
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states[ADV]['state'] == 'EXPLORING' and states[ADV]['owner_id'] == OWNER
preserved_before = guard.check('EXPLORING')
assert sha(SP.read_bytes()) == 'c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'
seal = json.loads(SP.read_bytes())
math = json.loads((E / 'local-math-candidate.json').read_bytes())
for x in math['source_files']:
    p = Path(x['path'])
    assert sha(p.read_bytes()) == x['sha256'] and git('show', f'{MATH}:{p}') == p.read_bytes()
checks = [math['actual_final_build'], math['actual_final_proof_value_kernel']]
for x in checks:
    r = json.loads(Path(x['file']).read_bytes())
    assert r['exit_code'] == 0 and sha(Path(r['log']).read_bytes()) == r['log_sha256'] == x['log_sha256']
assert cfg['native_math']['sha256'] == 'b65ea8f10740af2fad395ef448c9d0e87f92dc5646a1b3a313e5efdda356bc69'
native = frozen_json(cfg['native_math'])
assert native['status'] == 'PASS_NATIVE_MATHEMATICS_ONLY' and native['pinned_mathematical_candidate'] == MATH
assert native['candidate_closure_module_count'] == len(native['modules']) == 12
assert all(m['raw_declarations'] == m['full_types_checked'] == m['full_values_checked'] for m in native['modules'])
assert sum(m['full_values_checked'] for m in native['modules']) == native['candidate_raw_emissions'] == 75
assert all(native['lossless_DAG_inverse_checks'][k] is True for k in [
    'every_exported_full_type_and_value_structurally_equal_after_file_JSON_decode',
    'every_decoded_full_type_and_value_kernel_checked',
    'all_constructor_fields_names_levels_binders_metadata_literals_preserved'])
assert len(native['literal_target_checks']) == 4
assert all(x.get('full_actual_proof_value_kernel_checked_against_literal', x.get('full_value_kernel_checked', False))
           for x in native['literal_target_checks'])
assert native['clean_packages']['count'] == 9
assert native['clean_packages']['root_ASTIS_artifacts_in_effective_LEAN_PATH'] is False
assert native['clean_packages']['all_effective_package_paths_owned'] is True
assert native['allowed_axioms'] == ['propext', 'Classical.choice', 'Quot.sound']
assert all(not x['findings'] for x in native['fake_closure_scan'])
assert cfg['native_actual_parents']['sha256'] == 'ce0c6fc6de645fec235b3b69a66a59baa58433d7c195a76f516f024ba2bef624'
parent_record = frozen_json(cfg['native_actual_parents'])
assert parent_record['pinned_candidate'] == MATH
assert parent_record['native_report_unchanged_sha256'] == sha(Path(cfg['native_math']['path']).read_bytes())
a = json.loads(A.read_bytes())
assert a['source_review']['state'] == 'accepted' and a['state'] in ['source-reviewed', 'accepted']
assert a['publication_binding_sha256'] == '039a91f41fb14176849c877a897f6d47ca6f50b60f2bef5e29407854f044610b'
name = a['lean']['declaration']
pub.check_advance([name], reviewed=True)
cell = json.loads(C.read_bytes())
assert cell['conceptual_mirror_audit']['status'] == 'none-found'
assert not frontiers.validate_cells(frontiers.load_cells())
reader = cfg['reader']
assert reader['actual_reader_candidate_commit'] == READER
browser_reports = {}
native_root = Path('.astis/semantic-neutral-20261114/bernstein_exp_native_72c4')
for label, expected_status, expected_exit in [('original', 'FAIL', 1), ('isolated_candidate', 'PASS', 0)]:
    refs = reader[label]
    report = frozen_json(refs['actual_checks'])
    receipt = frozen_json(refs['process_receipt'])
    contract = frozen_json(refs['contract'])
    assert refs['checker_exit'] == receipt['exit_code'] == expected_exit
    assert report['status'] == receipt['actual_checks']['status'] == expected_status
    assert report['browser_started'] is True and report['screenshots']
    assert report['reader_commit'] == contract['reader_commit'] == READER
    assert report['mathematical_candidate'] == contract['mathematical_candidate'] == MATH
    assert report['contract_sha256'] == receipt['contract_sha256'] == refs['contract']['sha256']
    assert report['wrapper_sha256'] == receipt['wrapper_sha256'] == refs['wrapper']['sha256']
    frozen_ref(refs['wrapper'])
    assert contract['wrapper_sha256'] == refs['wrapper']['sha256']
    assert receipt['actual_checks']['sha256'] == refs['actual_checks']['sha256']
    assert (native_root / receipt['actual_checks']['path']).resolve() == Path(refs['actual_checks']['path']).resolve()
    assert receipt['exception'] is None and receipt['actual_chrome']['runtime_browser_version']
    for stream in ['stdout', 'stderr']:
        s = receipt[stream]
        p = str(native_root / s['path'])
        data = frozen_ref({'path': p, 'sha256': s['sha256']})
        assert len(data) == s['bytes']
    for png in report['screenshots']:
        frozen_ref({'path': str(native_root / png['path']), 'sha256': png['sha256']})
    assert not report['production_changes_applied']
    if label == 'isolated_candidate':
        assert all(x['pass'] for x in report['checks'])
        assert not report['javascript_errors'] and not report['blocked_external_requests']
        names = {x['name'] for x in report['checks']}
        for viewport in ['desktop', 'mobile']:
            assert {viewport + suffix for suffix in [
                '-seven-proof-steps', '-all-seven-steps-initially-folded',
                '-exact-P148-in-first-four-folds', '-exact-T240-in-last-three-folds',
                '-private-T-source-and-download-adjacent', '-adjacent-private-T-download-exact',
                '-source-table-horizontally-reachable', '-graph-exact-public-focus',
                '-graph-formal-and-source-styles-separate']} <= names
            for target in ['P', 'T']:
                assert {viewport + '-' + target + suffix for suffix in [
                    '-complete-source-exact', '-module-download-exact',
                    '-anchor-below-mobile-header', '-full-source-glyph-horizontal-reach',
                    '-last-source-glyph-actually-visible-below-header']} <= names
    browser_reports[label] = report
review_ref = reader['independent_runtime_review']['artifact']
runtime_review = frozen_json(review_ref)
assert runtime_review['accepted_isolated_candidate'] is True
assert runtime_review['immutable_reader_commit'] == READER and runtime_review['mathematical_candidate'] == MATH
assert runtime_review['production_changes_applied'] is False
assert runtime_review['reviewer'] not in [OWNER, 'ROOT', '/root', 'bernstein_exp_native_72c4']
for label in ['original', 'isolated_candidate']:
    assert runtime_review['actual_report_refs'][label]['sha256'] == reader[label]['actual_checks']['sha256']
assert reader['independent_runtime_review']['accepted'] is runtime_review['accepted_isolated_candidate']
graph_refs = reader['graph_zoom_supplement']
graph_report = frozen_json(graph_refs['actual_checks'])
graph_receipt = frozen_json(graph_refs['process_receipt'])
graph_contract = frozen_json(graph_refs['contract'])
frozen_ref(graph_refs['wrapper'])
assert graph_report['schema'] == 'root-primary-graph-zoom-result-v1'
assert graph_report['scope'] == 'GRAPH_ONLY; no full P/T reader rerun; no data/CSS/layout mutation'
assert graph_report['status'] == graph_receipt['actual_checks']['status'] == 'PASS'
assert graph_receipt['exit_code'] == graph_refs['checker_exit'] == 0
assert graph_report['reader_commit'] == graph_contract['reader_commit'] == READER
assert graph_report['mathematical_candidate'] == graph_contract['mathematical_candidate'] == MATH
assert graph_report['browser_started'] is True
assert graph_report['wrapper_sha256'] == graph_receipt['wrapper_sha256'] == graph_refs['wrapper']['sha256']
assert graph_report['contract_sha256'] == graph_receipt['contract_sha256'] == graph_refs['contract']['sha256']
assert graph_receipt['actual_checks']['sha256'] == graph_refs['actual_checks']['sha256']
assert graph_receipt['exception'] is None
assert all(x['pass'] for x in graph_report['checks'])
graph_names = {x['name'] for x in graph_report['checks']}
for viewport in ['desktop', 'mobile']:
    assert {viewport + suffix for suffix in [
        '-real-wheel-increased-label-size', '-selected-public-node-readable-and-fully-visible',
        '-exact-public-focus-preserved', '-exact-one-hop-neighbors-present',
        '-adjacent-node-0-readable-and-fully-visible', '-adjacent-node-1-readable-and-fully-visible',
        '-formal-edge-actual-visible-style', '-overlay-edge-actual-visible-style',
        '-exact-reader-link', '-reader-link-actual-visible']} <= graph_names
for stream in ['stdout', 'stderr']:
    x = graph_receipt[stream]
    assert len(frozen_ref({'path': str(native_root / x['path']), 'sha256': x['sha256']})) == x['bytes']
for png in graph_report['screenshots']:
    frozen_ref({'path': str(native_root / png['path']), 'sha256': png['sha256']})
assert runtime_review['graph_zoom_supplement']['actual_checks']['sha256'] == graph_refs['actual_checks']['sha256']
assert runtime_review['graph_zoom_supplement']['process_receipt']['sha256'] == graph_refs['process_receipt']['sha256']
assert reader['production_shared_files_changed'] is False
assert reader['exact_full_source_folds'] == {'P_lines': 148, 'T_lines': 240, 'folds': 7}
boundary = cell['truth_boundary'] + ' Actual complete P/T source bodies compiled, independently rebuilt/kernel/source reviewed, with isolated actual desktop/mobile/source/download/graph reader accepted. Original production-rendered reader defect and isolated candidate overlay remain distinct; shared integration and purification remain held.'
result = {
    'result_kind': 'reusable-interface', 'theorem_delta': seal['producer']['signature'],
    'lean_files': [x['path'] for x in math['source_files']], 'lean_declarations': [name],
    'publication_declarations': [name], 'focused_checks': checks,
    'truth_boundary': boundary, 'mathematical_candidate': MATH,
    'executed_build_qualification': math['build_commit_qualification'],
    'source_review_metadata_commit': head, 'reader_metadata_commit': READER,
    'publication_binding_sha256': a['publication_binding_sha256'],
    'actual_compiled_parent_edges': math['canonical_P_parents'],
    'actual_material_consumer': {'name': math['kernel']['actual_private_name'],
        'file': math['source_files'][1]['path'], 'file_sha256': math['source_files'][1]['sha256'],
        'sealed_signature': seal['actual_private_consumer']['signature'],
        'actual_ASTIS_parents': math['private_T_parents'],
        'actual_proof_DAG_parent_witnesses': cfg['native_actual_parents'],
        'private_implementation_only': True, 'public_API_registry_credit': False,
        'scope': 'Authored original unconditional Gaussian normalized individual MGF comparison, all s>0 and each actual row, sole source hq, including q0. All normalization/regularity/centering/PSD/exp adapters proved internally.'},
    'independent_source_review': cell['evidence']['independent_source_review'],
    'independent_native_math': cfg['native_math'],
    'conceptual_mirror_audit': cell['conceptual_mirror_audit'],
    'owned_math': math['kernel'],
    'native_inventory_qualification': 'Twelve actual transitive ASTIS modules emit75 candidate declarations; every complete type AND value, plus16 auxiliary values, were kernel rechecked, with lossless structural ExprDAG inverse including metadata. These inventory counts are evidence accounting, not theorem closure or public-node counts.',
    'formalizer_API_pristine': False,
    'proof_iteration': math['iteration_qualification'] + ' Independent native harness and inverse-codec failures retained with actual changed successors. Metadata-only T locator54->57 separately reviewed; original reader defect and isolated rendering overlay retained.',
    'actual_reader_evidence': reader, 'preservation_before_API': preserved_before,
    'integration_notes': 'User chose original shared stabilization owner finish/release. No takeover/shared CSS/shared renderer/root imports/Registry/global source-index/graph/production site or clean-port write. No sum-tail/full Bernstein/C6/Lemma4.4/main lowerbounds or oracle/TV/precision/query-cap/cost/purification credit.'}
create(W / 'normal-PROVED_LOCAL-attempted.once.json', dump({'advance_id': ADV, 'head': head,
    'before_ledger_sha256': sha(before), 'normal_API_calls_requested': 1}))
advance.transition_advance(ADV, 'PROVED_LOCAL', worker_id=OWNER, evidence=result)
after = L.read_bytes()
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event['advance_id'] == ADV and event['to_state'] == 'PROVED_LOCAL' and event['evidence'] == result
cell['status'] = 'proved_locally'
cell.pop('reservation_only', None)
cell['truth_boundary'] = boundary
cell['evidence']['focused_checks'] = checks
cell['evidence']['normal_API_calls'] = 4
cell['evidence']['actual_PROVED_LOCAL_append_sha256'] = sha(append)
cell['evidence']['independent_native_math'] = cfg['native_math']
cell['evidence']['actual_canonical_parent_witnesses'] = cfg['native_actual_parents']
cell['evidence']['actual_reader_evidence'] = reader
cell['evidence']['local_math_candidate']['independent_native'] = 'PASS actual immutable0ff complete native closure and proof values'
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_P_T;LOCAL_COMPILED;INDEPENDENT_SOURCE_NATIVE_AND_ISOLATED_RUNTIME_READER_ACCEPTED;INTEGRATION_HELD'
cell['reader_contract']['status'] = reader['scope_boundary']
cell['graph_contribution']['visual_review'] = reader['graph_boundary']
cell['learning_contract']['failure_class'] = 'NONE'
cell['learning_contract']['salvage'] = {'required': True, 'status': 'completed',
    'reason': 'All actual proof/API/native harness/metadata/reader failures and originals retained; no source binder or definition changed. Every handwritten proof component is material; compiler-generated support is not an extra public node.',
    'promoted_fragments': [name], 'discarded_fragments': []}
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
preserved_after = guard.check('PROVED_LOCAL')
assert preserved_after == preserved_before
create(E / 'actual-PROVED_LOCAL-append.exact.jsonl', append)
create(E / 'actual-PROVED_LOCAL-evidence.full.json', dump(result))
create(E / 'normal-PROVED_LOCAL-preservation.json', dump(preserved_after))
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(C), str(L)}
print(json.dumps({'state': 'PROVED_LOCAL', 'actual_API_calls': 1, 'append_sha256': sha(append),
                  'full_original_payload_sha256': sha(dump(result)), 'preservation': preserved_after,
                  'ROOT_VERIFIED_calls': 0}))
