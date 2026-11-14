"""UNEXECUTED Geometry browser guards. Future actual records are required, never fabricated."""
import argparse, ast, gzip, hashlib, json, os, re, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
PROPOSAL_REPORT_SHA = '6f9045472dc9f11da494942d065b093efab12c2cf385f6d83a379ad771a5e904'
CANDIDATE = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
OWNER = 'huanjian_gc_20261109_fixed_spectrum_geometry'
ACTOR = '/root/geometry_integration_reader'
BINDING = '69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
AUDIT = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
FRONTIER = 'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json'
sha = lambda b: hashlib.sha256(b).hexdigest()
def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)
def parse_args(doc):
    p = argparse.ArgumentParser(description=doc)
    p.add_argument('--authorization-json', required=True)
    p.add_argument('--authorization-sha256', required=True)
    return p.parse_args()
def readref(ref):
    p = (R / ref['path']).resolve()
    assert p.is_relative_to(R)
    raw = p.read_bytes()
    assert re.fullmatch('[0-9a-f]{64}', ref['sha256']) and sha(raw) == ref['sha256']
    return raw
def load_authorization(args):
    ref = {'path': args.authorization_json, 'sha256': args.authorization_sha256}
    a = json.loads(readref(ref))
    assert a['authorized_by'] == '/root' and a['authorization_kind'] == 'fixed-spectrum-geometry-final-browser-v1'
    assert a['execute_browser_authorized'] is True and a['new_source_verdict'] is False and a['parking_authorized'] is False
    assert a['candidate_commit'] == CANDIDATE and a['publication_binding_sha256'] == BINDING
    assert a['browser_checker_sha256'] == sha((S / 'check_final_reader_v1.py').read_bytes())
    assert a['browser_common_sha256'] == sha(Path(__file__).read_bytes())
    assert re.fullmatch('[0-9a-f]{40}', a['accepted_immutable_core']) and a['accepted_immutable_core'] != CANDIDATE
    assert git('rev-parse', 'HEAD').decode().strip() == a['accepted_immutable_core']
    subprocess.check_call(['git', 'merge-base', '--is-ancestor', CANDIDATE, a['accepted_immutable_core']], cwd=R)
    assert re.fullmatch('[0-9a-f]{40}', a['source_V_first_carrying_commit'])
    subprocess.check_call(['git', 'merge-base', '--is-ancestor', a['source_V_first_carrying_commit'], a['accepted_immutable_core']], cwd=R)
    assert a['reviewed_UI_repair'] is None  # Current inherited native-camera JS stays exact.
    return a, ref
def replay(ledger, discoveries):
    tree = ast.parse((R / 'tools/astis_advance.py').read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'_replay_advances', '_replay_discoveries'}]
    assert len(functions) == 2
    scope = {'Iterable': list, 'Any': object, 'NO_PROGRESS_FREEZE_AT': 3}
    exec(compile(ast.Module(body=functions, type_ignores=[]), '<pure-read-only-replay>', 'exec'), scope)
    return (scope['_replay_advances']([json.loads(x) for x in ledger.splitlines() if x.strip()]),
            scope['_replay_discoveries']([json.loads(x) for x in discoveries.splitlines() if x.strip()]))
def authorized_context(a):
    proposal_raw = (S / 'conditional-proposal-v1/proposal-report.json').read_bytes()
    assert sha(proposal_raw) == PROPOSAL_REPORT_SHA == a['proposal_report_sha256']
    p = json.loads(proposal_raw)
    assert a['candidate_source_digest'] == p['candidate_source_digest']
    assert a['source_digest'] == p['predicted_source_digest_after_exact_proposed_Lean_payloads']
    for row in p['shared_paths']:
        raw = (R / row['path']).read_bytes()
        assert sha(raw) == row['planned_after_sha256']
        assert git('show', a['accepted_immutable_core'] + ':' + row['path']) == raw
    br = p['protected_baseline']; compressed = readref({'path': br['path'], 'sha256': br['gzip_sha256']})
    baseline_raw = gzip.decompress(compressed); assert sha(baseline_raw) == br['raw_sha256']
    baseline = json.loads(baseline_raw)
    # Three possible actual own metadata paths require evidence below. Nothing
    # else is exempted from lossless foreign/current-candidate preservation.
    ledger_name = 'runs/substantive_advances.jsonl'
    exceptions = {ledger_name, AUDIT, FRONTIER}
    checked = 0
    for name, row in baseline['protected_tracked'].items():
        if name in exceptions: continue
        q = R / name; raw = os.fsencode(os.readlink(q)) if q.is_symlink() else q.read_bytes()
        assert sha(raw) == row['sha256'], name
        checked += 1
    assert checked == len(baseline['protected_tracked']) - len(exceptions)
    before_ledger = git('show', CANDIDATE + ':' + ledger_name)
    assert sha(before_ledger) == baseline['all_tracked'][ledger_name]['sha256']
    now = (R / ledger_name).read_bytes(); assert now.startswith(before_ledger)
    tail = now[len(before_ledger):].splitlines(); assert len(tail) == 2
    V, stab = map(json.loads, tail)
    verifier = a['source_verifier_to_preserve']
    assert verifier not in [OWNER, ACTOR, '/root']
    assert V['advance_id'] == stab['advance_id'] == ADV
    assert V['worker_id'] == V['evidence']['verifier_id'] == verifier
    assert (V['from_state'], V['to_state']) == ('PROVED_LOCAL', 'VERIFIED')
    assert (stab['from_state'], stab['to_state']) == ('VERIFIED', 'STABILIZING')
    assert stab['worker_id'] == a['integration_owner'] and a['integration_owner'] not in [OWNER, ACTOR, verifier]
    assert V['evidence']['verified_commit'] == CANDIDATE
    assert all(V['evidence'][k] for k in ['gate', 'source_audit', 'fake_closure_scan'])
    append = readref(a['source_V_append'])
    assert append == tail[0] + b'\n' and now.count(append) == 1
    assert readref(a['STAB_append']) == tail[1] + b'\n'
    execution = json.loads(readref(a['source_V_actual_execution_manifest']))
    assert execution['normal_API_calls'] == 1 and execution['actor'] == verifier and execution['exact_append_sha256'] == sha(append)
    assert a['accepted_source_audit']['path'] == AUDIT
    audit_raw = readref(a['accepted_source_audit']); audit = json.loads(audit_raw)
    assert audit['state'] == 'accepted' and audit['publication_binding_sha256'] == BINDING
    assert audit['lean']['formalizer'] == OWNER and audit['source_review']['reviewer'] == verifier
    assert audit['reconstruction']['decoder'] not in [verifier, OWNER, ACTOR]
    assert sha(readref(a['source_review_run'])) == audit['source_review']['review_run_sha256']
    assert git('show', a['accepted_immutable_core'] + ':' + AUDIT) == audit_raw
    assert git('show', a['source_V_first_carrying_commit'] + ':' + AUDIT) == audit_raw
    assert append in git('show', a['source_V_first_carrying_commit'] + ':' + ledger_name)
    assert a['own_frontier_current']['path'] == FRONTIER
    frontier_raw = readref(a['own_frontier_current'])
    assert git('show', a['accepted_immutable_core'] + ':' + FRONTIER) == frontier_raw
    before_frontier_raw = git('show', CANDIDATE + ':' + FRONTIER)
    assert sha(before_frontier_raw) == baseline['all_frontier_raw_hashes'][FRONTIER]
    before_frontier = json.loads(before_frontier_raw); frontier = json.loads(frontier_raw)
    # An explicitly reviewed actual mechanical metadata projection is mandatory
    # if own frontier bytes change. This preparation creates no such projection.
    if frontier_raw != before_frontier_raw:
        projection = json.loads(readref(a['own_frontier_projection_review']))
        assert projection['authorized_by'] == '/root' and projection['scope'] == 'mechanical-own-cell-sourceV-STAB-evidence-only'
        assert projection['candidate_commit'] == CANDIDATE and projection['advance_id'] == ADV
        assert projection['before_sha256'] == sha(before_frontier_raw) and projection['after_sha256'] == sha(frontier_raw)
        assert projection['source_V_append_sha256'] == sha(append) and projection['STAB_append_sha256'] == sha(tail[1] + b'\n')
        assert projection['new_mathematical_or_source_verdict'] is False
        # Keep source math, parents, seals and coverage graph exact; only the
        # separately reviewed metadata paths may differ, never a whole subtree.
        def differences(x, y, path=''):
            if isinstance(x, dict) and isinstance(y, dict):
                out = []
                for k in sorted(x.keys() | y.keys()):
                    q = path + '/' + k.replace('~', '~0').replace('/', '~1')
                    out += differences(x[k], y[k], q) if k in x and k in y else [q]
                return out
            return [] if x == y else [path]
        changed = differences(before_frontier, frontier)
        assert changed == projection['changed_json_paths']
        permitted = {'/evidence/canonical_integration', '/evidence/execution_boundary', '/evidence/existing_source_V',
            '/evidence/independent_verification', '/evidence/source_phase_history', '/graph_contribution/visual_review',
            '/source_detail_audit/fidelity_boundary', '/source_detail_audit/gap',
            '/source_proof_coverage/independent_implementation_review', '/statement_seal/status', '/status'}
        assert set(changed) <= permitted
    else:
        assert a['own_frontier_projection_review'] is None
    for key in ['cell_id', 'advance_id', 'owner_id', 'target_statement', 'parents', 'source_anchor']:
        assert frontier[key] == before_frontier[key]
    discovery_raw = (R / 'runs/substantive_discoveries.jsonl').read_bytes()
    states, discoveries = replay(now, discovery_raw)
    assert states[ADV]['state'] == 'STABILIZING' and [k for k, v in states.items() if v['state'] == 'STABILIZING'] == [ADV]
    assert {k: v for k, v in states.items() if k != ADV} == baseline['foreign_SAU_states']
    assert discoveries == baseline['all_discovery_states']
    gate = json.loads(readref(a['actual_gate'])); meta = json.loads(readref(a['site_metadata']))
    assert gate['passed'] and meta['gate']['passed'] and meta['gate']['current']
    assert gate['commit'] == meta['git']['commit'] == a['accepted_immutable_core']
    assert gate['source_digest'] == meta['source_digest'] == a['source_digest']
    roles = {'canonical_lean', 'publication', 'contributor', 'semantic', 'frontier', 'site_build', 'site_check', 'graph_check'}
    assert set(a['actual_checks_before_browser']) == roles
    needles = {'publication': 'astis_publication.py', 'contributor': 'astis_contributor_contract.py',
        'semantic': 'astis_semantic_roundtrip.py', 'frontier': 'astis_frontier_cells.py',
        'site_build': 'build_site.py', 'site_check': 'check_site.py', 'graph_check': 'graph-check'}
    for role, ref in a['actual_checks_before_browser'].items():
        receipt = json.loads(readref(ref))
        assert receipt['exit_code'] == 0 and receipt['head_before'] == receipt['head_after'] == a['accepted_immutable_core']
        log = Path(receipt['log']).read_bytes(); assert sha(log) == receipt['log_sha256']
        if role == 'canonical_lean':
            assert log.decode().splitlines().count('ASTIS check passed') == 1
            assert receipt['command'][1:] in [['tools/astis.py', 'check'], ['website/scripts/lean_gate.py']]
        else:
            assert needles[role] in str(receipt['command'])
    return {'conditional_proposal_exact_applied': True, 'original_source_verifier': verifier,
        'unique_original_V_append_sha256': sha(append), 'sole_STAB': ADV,
        'foreign_tracked_raw_bytes_preserved': True, 'protected_raw_files_checked': checked,
        'all_foreign_states_frontiers_models_and_discovery_bytes_preserved': True,
        'own_frontier_successor': a['own_frontier_current'], 'source_V_first_carrying_commit': a['source_V_first_carrying_commit'],
        'lifecycle_API_called': False, 'new_source_verdict': False, 'all8_actual_receipts_exact_core_read': True}
