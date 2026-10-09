from pathlib import Path
import hashlib, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
OLD = ROOT / 'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-source73'
OWN = ROOT / 'runs/20261007-companion-priority/pbps-actual-harmonic-flow73/independent-source73'

def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_bytes())
def canonical(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
def pin(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'RAW_bytes': len(b), 'RAW_sha256': sha(b),
            'LF_sha256': sha(b.replace(b'\r\n', b'\n')), 'LF_recipe': 'CRLF byte pairs to LF only; preserve all other bytes'}
def write(n, x):
    p = OWN / n
    assert not p.exists()
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

assert not (OWN / 'lease.final.json').exists()
assert sha((OLD / 'lease.final.json').read_bytes()) == 'd29689c7071e0ff35cfcfec6e303d090763d24b1c8cd12f984cd6c3eea59872c'
lease = load(OLD / 'lease.final.json')
assert lease['status'] == 'CLOSED_LAST' and lease['owned_file_count_including_self'] == 52
for r in lease['all_files_except_self']:
    b = (ROOT / r['path']).read_bytes()
    assert len(b) == r['bytes'] and sha(b) == r['raw_sha256']
    assert sha(b.replace(b'\r\n', b'\n')) == r['lf_sha256']
run = load(OLD / 'run.json')
run_hash = run.pop('run_sha256')
assert sha(canonical(run)) == run_hash == '0ce9bfaeda1bf2a573d606ee3d3d8beff7cd7a17fce7f511545233c8dd26b7ca'
graph = load(OLD / 'source-proof-graph73.reviewed-projection.json')
expect = load(OLD / 'StageA.source-expectations73.before-header.frozen.json')
conjuncts = load(OLD / 'StageB.nine-conjuncts-source-review73.json')
assert len(graph['nodes']) == 23 and len(graph['edges']) == 37 and graph['source_gap_count'] == 7
assert graph['semantic_items'] == 79 and graph['NODE'] == 24 and graph['EXCLUDED'] == 55
assert conjuncts['conjunct_count'] == len(conjuncts['conjuncts']) == 9
assert len(expect['six_original_callers']) == 6
names = ['lease.final.json', 'whole-owned.manifest.json', 'run.json',
         'StageA.source-expectations73.before-header.frozen.json',
         'StageA.topology-decision73.before-header.frozen.json',
         'StageA.independent-source79-classification73.frozen.json',
         'StageA.independent-binder20-review73.frozen.json',
         'StageA.independent-node23-edge35-gap7-review73.frozen.json',
         'StageA.gradient-producer-independent-check73.frozen.json',
         'source-proof-graph73.reviewed-projection.json',
         'distinct-two-edge-repair73.authority.json',
         'StageB.actual-binder-definition-review73.json',
         'StageB.nine-conjuncts-source-review73.json',
         'source13-region51-block.finite-RAW-LF-map73.json',
         'source-header73.input-manifest.json', 'source-header73.decision.json',
         'source-header73.review.RAW.md']
write('preparation.source-contract-inputs73.json', {
    'input_count': len(names), 'inputs': [pin(OLD / n) for n in names],
    'old_native_members_opaque_hash_verified': 51, 'old_closed_native_written': False,
    'old_whole_logical_hash': run_hash, 'source_graph_rederived': False,
    'prior_source_header_credit_is_not_whole_implementation_credit': True})
plan = {
    'schema': 'astis-whole-source73-anti-anchored-preparation/v1',
    'status': 'READY_WAITING_EXPLICIT_FRESH_REVIEWER_PACKET',
    'reviewer': '/root/independent_primary69',
    'scope': OWN.relative_to(ROOT).as_posix(),
    'reuse': {'CLOSED52': pin(OLD / 'lease.final.json'),
             'expectations_frozen_before73_header_and_BODY': pin(OLD / 'StageA.source-expectations73.before-header.frozen.json'),
             'accepted_source_graph': pin(OLD / 'source-proof-graph73.reviewed-projection.json'),
             'source_items': 79, 'NODE': 24, 'EXCLUDED': 55, 'source_regions': 13, 'source_blocks': 51,
             'nodes': 23, 'edges': 37, 'internal_bridge_nodes': graph['source_gap_node_ids'],
             'semantic_binders': {'SOURCE': 4, 'STANDING': 6, 'TYPING': 10, 'EXCESS': 0}},
    'packet_gate': {'require': 'Root explicit fresh official anti-anchored reviewer packet ready message',
                   'before_gate': 'Read own immutable source contracts only; prepare scripts/schema only',
                   'current_production_Lean_read': False, 'current_new_lesson_or_publication_read': False,
                   'blind_decoder_result_read': False, 'fresh_math_verdict_read': False,
                   'source_verdict_issued': False},
    'bounded_review_order': [
        'Read and pin official packet/freeze first; validate permitted current input RAW and CRLF-only LF versions',
        'Read complete implementation including private literal, all public signatures and helper BODY; compare to frozen source independently',
        'Classify every exact module line and mathematical declaration; map each proof ingredient to source-obligation nodes/edges without changing graph layers',
        'Audit all six callers, expand all definitions/quantifiers; separately record retained source-standing assumptions versus assumptions actually used',
        'Check all nine conjuncts against exact source and full BODY; audit all seven internal bridges and local producer use',
        'Compare allowed blind reconstruction, canonical semantic slots/deltas, full publication context and all exact lesson formulas/BODY spans',
        'Freeze any concrete repair as an exact separately reviewable overlay; root alone applies canonical edits',
        'Close one small native whole-source bundle after final current packet is fixed; external read-only postclose only'],
    'nine_conclusions': [r['conjunct'] for r in conjuncts['conjuncts']],
    'invariants': {
        'center': expect['center'], 'literal_flow': expect['literal_flow'], 'ODE': expect['ODE'], 'energy': expect['energy'],
        'joint_domain': 'All y,xRef,t,x,p at fixed positive eta, same literal flow for continuity and Borel',
        'group_inverse': 'Same center, same eta, all real s,t; both inverse compositions',
        'pi': 'Phi_pi(x,p)=(2c-x,-p)',
        'degeneracies': 'rank0 and alpha*eta=1 retained; positive eta; zero energy; no Nontrivial/nonzero-normal premise',
        'private_literal': 'Complete proposition definition is nonprovider and must be exposed adjacent to public signature',
        'energy_norm': 'Weighted SUM of squared E component norms; never the product max norm',
        'source_hypothesis_vs_ingredient': 'All needed bridges produced internally; no producer becomes an extra public caller'},
    'finite_outputs_after_gate': {
        'whole_module_line_coverage': 'Every current exact line classified with declaration/source relationship and reason',
        'source79_coverage': 'Reuse frozen NODE24/EXCLUDED55; record precise current implementation relationship and retained exclusion reason',
        'source_topology_relationships': 'All23 nodes/all37 edges/all7 bridges checked against BODY or explicitly open; source graph is not Lean graph',
        'conclusions_and_binders': 'Nine conclusions, six callers, full private literal, all definitions, boundary cases and retained-versus-used assumptions',
        'lesson_coverage': 'Every declared formula/step and exact BODY span against full surrounding statement, assumptions and code',
        'semantic_roundtrip': 'Allowed canonical slot/delta schema inspected after packet gate; independently authored judgments and exact reasons',
        'admission_fields': 'Portable repository-relative evidence locators, exact final packet/binding pins, no self VERIFIED',
        'native_evidence': 'Complete named run/decision/review/input payload; finite RAW/LF versions and references; all-owned manifest; last CLOSED lease; actual PID/EXIT0'},
    'anti_anchoring_exposure': {
        'not_source_blind': True,
        'prior': ['70/71 full source and implementation/publication', '72 prospective and whole implementation/source/publication',
                  'bounded B27 dependency diagnosis', '73 independently source-first topology and prospective header review CLOSED52'],
        '73_current_implementation_BODY_never_read': True,
        'root_report_of_focused_compile_is_not_review_evidence_or_source_fidelity': True,
        'other73_header_math_verdict_never_read': True},
    'stochastic_exclusions': expect['future_exclusions'],
    'permissions': {'canonical_Lean_site_ledger_Git_writes': False, 'old_CLOSED_writes': False,
                    'new_compile_or_whole_site_graph_build': False, 'recursive_historical_payload_copy': False,
                    'VERIFIED_or_source_verdict_before_packet': False},
    'actual_preparation_PID': os.getpid(), 'background': False}
write('preparation.review-plan73.json', plan)
write('lease.open.json', {'status': 'OPEN_PREPARATION_ONLY_WAITING_FRESH_PACKET',
                         'owned_scope': OWN.relative_to(ROOT).as_posix(),
                         'production_BODY_or_publication_read': False, 'no_final_source_verdict': True})
write('preparation.terminal.json', {'actual_pid': os.getpid(), 'exit_code': 0, 'argv': sys.argv,
                                  'background': False, 'operation': 'Read own immutable source contracts and prepare bounded review only'})
print(json.dumps({'status': plan['status'], 'actual_pid': os.getpid(), 'exit_code': 0,
                  'source_input_count': len(names), 'old_CLOSED52_members_verified': 51,
                  'plan': pin(OWN / 'preparation.review-plan73.json'),
                  'source_inputs': pin(OWN / 'preparation.source-contract-inputs73.json'),
                  'current_BODY_or_lesson_read': False, 'source_verdict': False}, indent=2))
