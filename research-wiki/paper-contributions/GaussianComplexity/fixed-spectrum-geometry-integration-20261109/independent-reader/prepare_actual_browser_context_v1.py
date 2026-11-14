"""REVIEW-ONLY builder: actual facts required; emits disabled candidate context, never browser/API execution."""
from pathlib import Path
import argparse, ast, hashlib, importlib.util, json, re, subprocess, sys
sys.dont_write_bytecode = True
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
CANDIDATE = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
DECL = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry'
OWNER = 'huanjian_gc_20261109_fixed_spectrum_geometry'
INTEGRATOR = OWNER + '_integration'
VERIFIER = '/root/source_reader_9a6d2f'
DECODER = '/root/decode_80a1c2'
READER = '/root/geometry_integration_reader'
BINDING = '69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
CHECKER_SHA = 'e579e632b218e028310130e068230db3be8d0cca4d0e01714ea0f4b49c46268c'
COMMON_SHA = '2be36d2794fa949989bbeee2db10606c68ff966ef1de27c2337b5b6a4c90ace0'
PROPOSAL_SHA = '6f9045472dc9f11da494942d065b093efab12c2cf385f6d83a379ad771a5e904'
AP = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
CP = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json'
README = 'research-wiki/paper-contributions/GaussianComplexity/README.md'
LP = 'runs/substantive_advances.jsonl'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)
def refbytes(ref):
    assert set(ref) == {'path', 'sha256'}
    q = (R / ref['path']).resolve()
    assert q.is_relative_to(R) and re.fullmatch('[0-9a-f]{64}', ref['sha256'])
    raw = q.read_bytes(); assert sha(raw) == ref['sha256'], ref['path']
    return raw
def diffpaths(x, y, path=''):
    if isinstance(x, dict) and isinstance(y, dict):
        out = []
        for k in sorted(x.keys() | y.keys()):
            q = path + '/' + k.replace('~', '~0').replace('/', '~1')
            out += diffpaths(x[k], y[k], q) if k in x and k in y else [q]
        return out
    return [] if x == y else [path]
def source_digest():
    digest = hashlib.sha256()
    paths = [R / 'AutoSamplingTheory.lean', *sorted((R / 'AutoSamplingTheory').rglob('*.lean')),
             R / 'Tests.lean', *sorted((R / 'Tests').rglob('*.lean')),
             R / 'lakefile.lean', R / 'lean-toolchain', R / 'lake-manifest.json']
    for p in paths:
        if p.exists():
            digest.update(p.relative_to(R).as_posix().encode()); digest.update(b'\0')
            digest.update(p.read_bytes()); digest.update(b'\0')
    return digest.hexdigest()
def build(facts, facts_ref):
    assert Path.cwd().resolve() == R
    assert facts['facts_kind'] == 'fixed-spectrum-geometry-actual-prebrowser-facts-v1'
    assert facts['supplied_by'] == '/root'
    assert facts['candidate_commit'] == CANDIDATE and facts['publication_binding_sha256'] == BINDING
    assert facts['proposal_report_sha256'] == PROPOSAL_SHA
    assert facts['integration_owner'] == INTEGRATOR and facts['source_verifier_to_preserve'] == VERIFIER
    assert facts['browser_checker_sha256'] == CHECKER_SHA and facts['browser_common_sha256'] == COMMON_SHA
    assert facts['planned_original_PNGs'] == 44 and facts['planned_native_geometry_rows'] == 12
    assert facts['planned_old_DensityAffinity_DOM_regressions'] == 2
    for key in ['accepted_immutable_core', 'source_V_first_carrying_commit']:
        assert re.fullmatch('[0-9a-f]{40}', facts[key]) and facts[key] != CANDIDATE
    core = facts['accepted_immutable_core']
    assert git('rev-parse', 'HEAD').decode().strip() == core
    assert not git('diff', 'HEAD', '--name-only').strip()
    for ancestor in [CANDIDATE, facts['source_V_first_carrying_commit']]:
        subprocess.check_call(['git', 'merge-base', '--is-ancestor', ancestor, core], cwd=R)
    checker_path = S / 'check_final_reader_v1.py'; common_path = S / 'geometry_browser_common_v1.py'
    checker_raw = checker_path.read_bytes(); common_raw = common_path.read_bytes()
    assert sha(checker_raw) == CHECKER_SHA and sha(common_raw) == COMMON_SHA
    # Parse the frozen checker only as data. Never import its top-level browser.
    pin_nodes = [n for n in ast.parse(checker_raw).body if isinstance(n, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id == 'PINS' for t in n.targets)]
    assert len(pin_nodes) == 1
    pins = ast.literal_eval(pin_nodes[0].value)
    for name, expected in pins.items():
        raw = (R / name).read_bytes()
        assert sha(raw) == expected and git('show', core + ':' + name) == raw, name
    for asset in ['information-architecture.css', 'underlying-lean-graph.js']:
        assert (R / '_site/assets' / asset).read_bytes() == (R / 'website/static' / asset).read_bytes()
    assert facts['actual_gate']['path'] == '.astis/site-lean-gate.json'
    assert facts['site_metadata']['path'] == '_site/data/build-metadata.json'
    assert source_digest() == facts['source_digest']
    audit_raw = refbytes(facts['accepted_source_audit']); audit = json.loads(audit_raw)
    assert facts['accepted_source_audit']['path'] == AP
    assert audit['state'] == 'accepted' and audit['lean']['declaration'] == DECL
    assert audit['lean']['formalizer'] == OWNER and audit['reconstruction']['decoder'] == DECODER
    assert audit['source_review']['reviewer'] == VERIFIER and audit['publication_binding_sha256'] == BINDING
    assert len({OWNER, INTEGRATOR, VERIFIER, DECODER, READER, '/root'}) == 6
    source_run = refbytes(facts['source_review_run'])
    assert sha(source_run) == audit['source_review']['review_run_sha256']
    vraw = refbytes(facts['source_V_append']); stabraw = refbytes(facts['STAB_append'])
    assert vraw.endswith(b'\n') and stabraw.endswith(b'\n')
    assert len(vraw.splitlines()) == len(stabraw.splitlines()) == 1
    V = json.loads(vraw); stab = json.loads(stabraw)
    assert V['event'] == stab['event'] == 'transition' and V['advance_id'] == stab['advance_id'] == ADV
    assert (V['from_state'], V['to_state']) == ('PROVED_LOCAL', 'VERIFIED')
    assert (stab['from_state'], stab['to_state']) == ('VERIFIED', 'STABILIZING')
    assert V['worker_id'] == V['evidence']['verifier_id'] == VERIFIER
    assert stab['worker_id'] == stab['evidence']['integration_owner'] == INTEGRATOR
    assert V['evidence']['verified_commit'] == stab['evidence']['verified_commit'] == CANDIDATE
    candidate_ledger = git('show', CANDIDATE + ':' + LP)
    assert (R / LP).read_bytes() == candidate_ledger + vraw + stabraw
    execution = json.loads(refbytes(facts['source_V_actual_execution_manifest']))
    assert execution['normal_API_calls'] == 1 and execution['actor'] == VERIFIER
    assert execution['exact_append_sha256'] == sha(vraw) and execution['verified_commit'] == CANDIDATE
    assert execution['publication_binding_sha256'] == BINDING
    assert execution['accepted_audit_sha256'] == sha(audit_raw) and execution['source_review_run_sha256'] == sha(source_run)
    application = json.loads(refbytes(facts['sole_STAB_application_receipt']))
    assert application['normal_API_calls'] == 1 and application['actor'] == INTEGRATOR
    assert application['normal_state'] == 'STABILIZING' and application['append_sha256'] == sha(stabraw)
    assert application['ledger_before_sha256'] == sha(candidate_ledger + vraw)
    assert application['ledger_after_sha256'] == sha(candidate_ledger + vraw + stabraw)
    assert application['source_digest'] == facts['source_digest']
    assert application['new_source_verdict_or_actual_core_gates_or_runtime_or_Goal_complete'] is False
    proposal_raw = (S / 'conditional-proposal-v1/proposal-report.json').read_bytes()
    assert sha(proposal_raw) == PROPOSAL_SHA
    proposal = json.loads(proposal_raw)
    assert len(application['exact_shared_payloads']) == 6 and application['exact_shared_payloads'] == proposal['shared_paths']
    # The README remains protected until actual browser/original-image acceptance.
    assert (R / README).read_bytes() == git('show', CANDIDATE + ':' + README) == git('show', core + ':' + README)
    cell_raw = refbytes(facts['own_frontier_current']); cell = json.loads(cell_raw)
    assert facts['own_frontier_current']['path'] == CP
    source_cell_raw = git('show', facts['source_V_first_carrying_commit'] + ':' + CP)
    old_cell_raw = git('show', CANDIDATE + ':' + CP)
    if source_cell_raw != old_cell_raw:
        projection = json.loads(refbytes(facts['source_V_own_frontier_projection_review']))
        assert projection['reviewer'] == READER and projection['verdict'] == 'ACCEPT_EXACT_MECHANICAL_SOURCE_V_PROJECTION'
        assert projection['candidate_commit'] == CANDIDATE and projection['source_V_append_sha256'] == sha(vraw)
        assert projection['before_sha256'] == sha(old_cell_raw) and projection['after_sha256'] == sha(source_cell_raw)
        assert projection['changed_json_paths'] == diffpaths(json.loads(old_cell_raw), json.loads(source_cell_raw))
        assert projection['new_mathematical_or_source_verdict'] is False
    else:
        assert facts['source_V_own_frontier_projection_review'] is None
    integration_projection = json.loads(refbytes(facts['own_frontier_projection_review']))
    assert integration_projection == application['additional_own_frontier_metadata']
    assert integration_projection['sourceV_before_sha256'] == sha(source_cell_raw)
    inverse = integration_projection['insertion_inverse']
    i = inverse['character_insertion_offset']; added = inverse['inserted_text']; text = cell_raw.decode()
    assert text[i:i + len(added)] == added
    assert (text[:i] + text[i + len(added):]).encode() == source_cell_raw
    assert integration_projection['application_changed_json_paths'] == ['/evidence/canonical_integration']
    assert diffpaths(json.loads(source_cell_raw), cell) == ['/evidence/canonical_integration']
    expected_metadata = {'state': 'SOLE_STAB_EXACT_SIX_PATHS_APPLIED_ACTUAL_CORE_GATES_PENDING', 'owner': INTEGRATOR,
        'source_V_first_carrying_commit': facts['source_V_first_carrying_commit'], 'source_verifier_preserved': VERIFIER,
        'proposal_report_sha256': PROPOSAL_SHA, 'new_public_producer': DECL, 'private_Test_Registry_node': False,
        'new_conceptual_transport': False, 'actual_STAB_append_sha256': sha(stabraw)}
    assert cell['evidence']['canonical_integration'] == expected_metadata
    # Frozen common supplies actual full-baseline/foreign-state/frontier/model,
    # accepted audit/run/V/soleSTAB, exact own projection and official8 gate checks.
    # Its authorized_context is read-only and does not inspect execution flags.
    spec = importlib.util.spec_from_file_location('geometry_common_readonly_for_context_builder', common_path)
    common = importlib.util.module_from_spec(spec); spec.loader.exec_module(common)
    keys = ['candidate_commit', 'publication_binding_sha256', 'accepted_immutable_core', 'source_V_first_carrying_commit',
        'source_verifier_to_preserve', 'integration_owner', 'candidate_source_digest', 'source_digest',
        'proposal_report_sha256', 'browser_checker_sha256', 'browser_common_sha256', 'source_V_append', 'STAB_append',
        'source_V_actual_execution_manifest', 'accepted_source_audit', 'source_review_run', 'own_frontier_current',
        'own_frontier_projection_review', 'actual_gate', 'site_metadata', 'actual_checks_before_browser']
    candidate = {key: facts[key] for key in keys}
    candidate.update({'authorization_kind': 'fixed-spectrum-geometry-final-browser-v1', 'authorized_by': None,
        'prepared_for': '/root', 'execute_browser_authorized': False, 'new_source_verdict': False,
        'parking_authorized': False, 'reviewed_UI_repair': None,
        'review_state': 'CANDIDATE_CONTEXT_ONLY_ROOT_REVIEW_AND_NEW_SCOPED_OS_APPROVAL_PENDING',
        'planned_original_PNGs': 44, 'planned_native_geometry_rows': 12,
        'planned_old_DensityAffinity_DOM_regressions': 2,
        'actual_facts': facts_ref, 'context_builder_sha256': sha(Path(__file__).read_bytes())})
    readback = common.authorized_context(candidate)
    assert readback['lifecycle_API_called'] is False and readback['new_source_verdict'] is False
    assert git('rev-parse', 'HEAD').decode().strip() == core and not git('diff', 'HEAD', '--name-only').strip()
    assert (R / LP).read_bytes() == candidate_ledger + vraw + stabraw
    assert sha(checker_path.read_bytes()) == CHECKER_SHA and sha(common_path.read_bytes()) == COMMON_SHA
    return candidate, {'state': 'ACTUAL_FACTS_VALIDATED_CANDIDATE_CONTEXT_ONLY', 'actual_core': core,
        'candidate_authorization_execution_flag': False, 'authorized_by': None,
        'actual_facts': facts_ref, 'read_only_common_context_checks': readback,
        'immutable_checker_pins_verified': pins, 'README_candidate_core_live_bytes_exact': True,
        'actual_read_only_source_digest': facts['source_digest'], 'planned_original_PNGs': 44,
        'planned_native_geometry_rows': 12, 'planned_old_DensityAffinity_DOM_regressions': 2,
        'no_sourceV_API_STAB_browser_OS_park_or_pixel_acceptance': True,
        'root_next_step': 'Review exact actual facts and this disabled candidate context. A separate explicit root authorization and a NEW scoped OS/browser approval are required before any execute flag is enabled. Script PASS is not original-image acceptance.'}
def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--actual-facts-json', required=True)
    p.add_argument('--actual-facts-sha256', required=True)
    p.add_argument('--output-dir', required=True)
    args = p.parse_args()
    facts_ref = {'path': args.actual_facts_json, 'sha256': args.actual_facts_sha256}
    facts = json.loads(refbytes(facts_ref))
    output = (R / args.output_dir).resolve()
    assert output.is_relative_to(S) and output != S and not output.exists()
    # No output is created until every actual input and all eight real gates pass.
    candidate, report = build(facts, facts_ref)
    output.mkdir(parents=True)
    (output / 'candidate-browser-authorization.DISABLED.json').write_bytes(dump(candidate))
    (output / 'actual-context-validation-report.json').write_bytes(dump(report))
    manifest = {'state': report['state'], 'execute_browser_authorized': False,
        'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(output.iterdir()) if q.is_file()]}
    (output / 'freeze.json').write_bytes(dump(manifest))
    print(json.dumps({'state': report['state'], 'output': str(output.relative_to(R)),
        'candidate_context_sha256': sha((output / 'candidate-browser-authorization.DISABLED.json').read_bytes()),
        'freeze_sha256': sha((output / 'freeze.json').read_bytes()), 'execute_browser_authorized': False}, indent=2))
if __name__ == '__main__':
    main()
