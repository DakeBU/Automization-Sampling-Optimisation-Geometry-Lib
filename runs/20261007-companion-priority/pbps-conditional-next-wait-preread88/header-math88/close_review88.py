"""Immutable prospective whole-header and distinct local-source review closure.
No production proof, canonical-state mutation, or external-source publication.
"""
import hashlib
import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone

R = pathlib.Path('E:/Samplinglib')
B = R / 'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88'
O = B / 'header-math88'
S = B / 'independent-source-first88'
ME = '/root/exact_verify77'
NOW = datetime.now(timezone.utc).isoformat()

def read(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))

def descriptor(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(),
            'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

def check(d):
    p = pathlib.Path(d['path'])
    if not p.is_absolute():
        p = R / p
    got = descriptor(p)
    assert got['raw_sha256'] == d['raw_sha256'], (str(p), got, d)
    assert got['bytes'] == d['bytes'], (str(p), got, d)
    return got

def write(name, value):
    p = O / name
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return descriptor(p)

head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R, text=True).strip()
assert head == '24210c17b36c608fec3c259f811430cc9fc148cf', head
freeze = read(O / 'input-freeze88.json')
math_inputs = [check(d) for d in freeze['actual_math_inputs']]
preservation = read(O / 'collaborator-preservation88.json')
assert preservation['count'] == 21
for d in preservation['RAWs']:
    check(d)
header = descriptor(B / 'header88.proposed.lean')
assert header['raw_sha256'] == '89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
assert (B / 'header88.proposed.lean').read_bytes() == (O / 'header88.exactraw.snapshot.lean').read_bytes()
txt = (B / 'header88.proposed.lean').read_text(encoding='utf-8')
assert not re.search(r'\b(?:axiom|sorry|admit)\b|Prop\s*:=\s*True|:=\s*trivial', txt)
assert txt.count('private def ') == 1 and '\ntheorem ' not in txt
assert '#check @actual_conditional_next_wait_survival_statement' in txt
receipt = read(O / 'whole-header-typecheck88.receipt.json')
assert receipt['exit_code'] == 0 and receipt['terminal_closed']
assert receipt['complete_named_private_Prop'] and receipt['proof_credit'] is False
for k in ['header', 'exact_snapshot', 'stdout', 'stderr', 'toolchain', 'lake_manifest']:
    check(receipt[k])
definitions = read(O / 'definition-readback88.json')
assert len(definitions['six_analytic_binders']) == 6
assert len(definitions['thirteen_literal_definitions']) == 13
assert len(definitions['exact_eleven_shared87_definitions']) == 11
assert definitions['binder_block_identical_to_parents75_76_87']

author_closed = read(S / 'closed-raw-manifest.source-first88.native.json')
author_checked = [check(d) for d in author_closed['inputs'] + author_closed['outputs']]
assert len(author_closed['inputs']) == 10 and len(author_closed['outputs']) == 9
primary = R / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw = primary.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
span_checks = []
for s in author_closed['exact_primary_spans']:
    b = raw[s['byte_start_zero_based']:s['byte_end_exclusive']]
    assert hashlib.sha256(b).hexdigest() == s['raw_span_sha256'], s['id']
    span_checks.append({'id': s['id'], 'raw_span_sha256': s['raw_span_sha256'], 'exact_bytes_match': True})
assert len(span_checks) == 9
chronology = [json.loads(s) for s in (S / 'chronology.native.jsonl').read_text(encoding='utf-8').splitlines()]
assert chronology[0]['candidate_read'] is False
assert chronology[-1]['event'] == 'SOURCE_FIRST88_FREEZE_COMPLETED'
assert chronology[-1]['candidate88_read'] is False
source_terminal = read(S / 'terminal-completion88.native.json')
assert source_terminal['status'] == 'SOURCE_FIRST_IMMUTABLE_FREEZE_CLOSED'
assert source_terminal['candidate88_exposure'] is False
own_reconstruction = read(O / 'primary-before-graph-reconstruction88.json')
assert own_reconstruction['candidate_seen_before_this_additional_topology_assignment'] is True
assert own_reconstruction['source_blind_or_primary_first_over_entire_task'] is False
assert own_reconstruction['author_graph_and_source_correspondence_verdict_not_yet_read'] is True
graph = read(S / 'source-proof-slice88.native.json')
coverage = read(S / 'source-coverage88.native.json')
assert len(graph['nodes']) == 9 and len(graph['edges']) == 10
assert len(coverage['in_scope']) == 6 and len(coverage['exclusions']) == 5
expected = {
    ('S87-I1', 'S87-I3'), ('S87-I2', 'S87-I3'),
    ('S87-I3', 'S88-P1'), ('S88-A1', 'S88-A2'),
    ('S87-I1', 'S88-P1'), ('S88-A1', 'S88-P2'),
    ('S88-P1', 'S88-P2'), ('S88-A2', 'S87-I4'),
    ('S88-P2', 'S87-I4'), ('S87-I4', 'S87-I5')}
assert {(e['source'], e['target']) for e in graph['edges']} == expected
assert all(e['consumer_use_site'] and e['justification'] for e in graph['edges'])
nodes = {n['id']: n for n in graph['nodes']}
assert nodes['S87-I4']['status'] == 'OPEN_TARGET88'
assert nodes['S87-I5']['status'] == 'OPEN_EXCLUDED_FROM88'
todo = set(nodes)
seen = set()
while todo:
    ready = {n for n in todo if all(e['source'] in seen for e in graph['edges'] if e['target'] == n)}
    assert ready, 'cyclic local source graph'
    seen |= ready
    todo -= ready

global_graph_path = R / 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/topology-repair-review86/source-proof-graph86.single-edge-proposed-successor.json'
global_inventory_path = R / 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json'
gg, gi = read(global_graph_path), read(global_inventory_path)
assert descriptor(global_graph_path)['raw_sha256'] == 'c7ed4b13d3471c42d2e516edfef3009345ce156e961685a0ad6f11344aa0f7d8'
assert descriptor(global_inventory_path)['raw_sha256'] == 'cd5f487c3091946ab0699c4c50203a1703ff8b6e0f44a67cfa86920c9a26db3f'
assert len(gg['nodes']) == 38 and len(gg['edges']) == 76
assert sum(e['dependency_edge'] for e in gg['edges']) == 73
assert len(gi['items']) == 47 and len(gi['atomic_dispositions']) == 72
assert len(gi['source_gaps']) == 3
j = {j['target']: j for j in gg['junctions']}
assert j['G86-10']['kind'] == 'OR_OF_SUFFICIENT_BACKGROUND_ROUTES'
assert all(r['kind'] == 'AND' for r in j['G86-10']['routes'])
assert j['G86-30']['kind'] == 'AND_FUTURE_OPEN'
integrity = write('source-input-integrity88.json', {
    'status': 'ALL_10_AUTHOR_INPUTS_9_OUTPUTS_AND_9_PRIMARY_SPANS_RAW_VALIDATED',
    'reviewer_id': ME, 'created_utc': NOW,
    'author_manifest': descriptor(S / 'closed-raw-manifest.source-first88.native.json'),
    'RAW_checked_descriptors': author_checked, 'exact_primary_spans': span_checks,
    'integrity_only_not_content_review': ['seal_source_first88.py', 'primary88.extracted.private.json'],
    'private_source_exclusion_preserved': author_closed['excluded_from_publication'],
    'no_extractor_private_script_rationale_or_candidate_acceptance_verdict_read': True,
    'author_primary_first_sequence': chronology,
    'own_sequence': 'Candidate first read 686f88; additional primary A1/A2 read 2bac64; own reconstruction frozen 156d25; author graph first read 3dca4c. This independent reviewer is not claimed source-blind or pre-candidate.',
    'unchanged_global_graph': descriptor(global_graph_path),
    'unchanged_global_inventory': descriptor(global_inventory_path),
    'counts': {'local_nodes':9, 'local_edges':10, 'local_NODE_groups':6, 'local_EXCLUDED_groups':5,
               'global_inventory_items':47,'global_atomic_dispositions':72,'global_nodes':38,
               'global_relations':76,'global_dependencies':73,'global_excluded_associations':3},
    'collaborator_21_RAW_rechecked': True})

edge_reasons = {
    ('S87-I1', 'S87-I3'): 'Actual history descends from prefix sigma algebra; together with I2, not alone, it inherits unused-tail independence.',
    ('S87-I2', 'S87-I3'): 'Disjoint iid coordinate blocks AND actual prefix causality establish independence of the generated history and complete tail.',
    ('S87-I3', 'S88-P1'): 'Tail coordinate zero is raw w(n) with its original Exp1 law; measurable functions of history remain past functions.',
    ('S88-A1', 'S88-A2'): 'Continuous nondecreasing finite hazard with zero origin makes first closed >= crossing obey the strict survival equivalence, even flat hazard and infinity.',
    ('S87-I1', 'S88-P1'): 'Last record and history-duration are past-measurable. This redundant direct use does not create an alternative sufficient route.',
    ('S88-A1', 'S88-P2'): 'Joint Borel threshold/weight is necessary for parameter integration; fixed-state identities alone cannot be substituted at random state.',
    ('S88-P1', 'S88-P2'): 'Independent joint product law permits integration against the history distribution; no conditional-law hypothesis is smuggled in.',
    ('S88-A2', 'S87-I4'): 'Literal waiting-time event is converted using pointwise strict threshold equivalence; this AND-combines with the product integral calculation.',
    ('S88-P2', 'S87-I4'): 'Measurable nonnegative product integration gives the all-history-event unnormalized identity. No division by history-event mass.',
    ('S87-I4', 'S87-I5'): 'A history-dependent finite-horizon duration can later furnish a final no-event factor; densities, ordered iteration and full trajectory assembly remain OPEN.'}
topology = write('topology-review88.json', {
    'status': 'ACCEPTED_INDEPENDENT_SOURCE_SLICE_TOPOLOGY_AND_BOUNDED_COVERAGE_ONLY',
    'reviewer_id': ME, 'graph_creator_id': '/root/fresh_source87', 'created_utc': NOW,
    'primary': descriptor(primary), 'header':header,
    'graph':descriptor(S/'source-proof-slice88.native.json'),
    'coverage':descriptor(S/'source-coverage88.native.json'),
    'own_before_graph_reconstruction':descriptor(O/'primary-before-graph-reconstruction88.json'),
    'source_integrity':integrity,
    'independence': {'distinct_from_graph_creator':True, 'implementation88_BODY_seen':False,
                     'extractor_private_script_or_rationale_seen':False,
                     'source_header_acceptance_verdict_seen':False,
                     'own_candidate_exposure_before_additional_source_audit':True,
                     'own_primary_reread_and_reconstruction_before_author_graph_read':True},
    'source_reconstruction': 'Direct complete A1.SS1/A1.SS2 reread recovers actual iid clock construction, literal hazard crossing and stopped update, explicit joint Borel justification, and the omitted measurable random-history integration ingredient in A7 iteration. Source topology was not reconstructed from Lean proof bodies.',
    'nodes_checked': [{'id':n['id'],'classification':n['kind'],'status':n['status'],'accepted_within_bounded_scope':True} for n in graph['nodes']],
    'edges_checked': [{'source':a,'target':b,'direction_and_use_site_accepted':True,'reason':edge_reasons[(a,b)]} for a,b in sorted(expected)],
    'AND_OR_review': 'I1 AND I2 give I3; joint Borel hazard AND independent fresh input feed P2; crossing endpoint AND measurable-parameter integration feed I4. A2 may feed final event conversion without a separate edge into raw-threshold integration P2. Local route is conjunctive, not ten independent sufficient implications. Inherited G86-10 CDF/transport alternatives remain OR-of-AND, optional summability remains optional, all other global junctions unchanged.',
    'coverage_review': {'local_in_scope_groups':[{'anchor':i['anchor'],'disposition':i['disposition'],'accepted':True} for i in coverage['in_scope']],
                        'local_excluded_groups':[{'anchor':i['anchor'],'reason':i['reason'],'accepted':True} for i in coverage['exclusions']],
                        'inherited_global_coverage':'47 items/72 atomic dispositions are unchanged RAW reuse. Heuristic Ex12-17/p1.1-p1.6 remain excluded, outer operator/Gaussian averaging and A2 augmentation remain separate OPEN consumers. This local review does not recertify the entire global proof or close any global item.',
                        'conditional_source_attribution':'Conditional survival is an explicit ASTIS source-implicit probability bridge, not a printed standalone source theorem.'},
    'scope_and_gaps':'I4 is a prospective target only. I5, full G86-11, conditional finite densities, full A7, random-depth restart, physical-time memorylessness/Markov, reversal, invariance, all-L2/Jensen/density, Gaussian averaging and query costs remain OPEN/outside. Fixed finite depth needs no nonexplosion or uniform cap. No future/open edge receives proof credit.',
    'required_repairs':[], 'canonical_source_graph_edited':False, 'proof_or_VERIFIED_credit':False})

math_review = write('mathematical-review88.json', {
    'status':'ACCEPTED_PROSPECTIVE_WHOLE_HEADER_MATHEMATICS_AND_TYPE_ONLY',
    'reviewer_id':ME,'created_utc':NOW,'observed_head':head,'header':header,
    'complete_header_typecheck':descriptor(O/'whole-header-typecheck88.receipt.json'),
    'definition_readback':descriptor(O/'definition-readback88.json'),
    'binder_audit':'All six analytic binders exactly match actual75/76/87: positive alpha, alpha<=beta, C2 V, pointwise two-sided Hessian bound, positive eta, beta*eta<=1. Carrier inner-product/finite-dimensional/Borel instances are typing. No clock-law, independence, hazard regularity, kernel, cap, nonexplosion or integration provider premise is supplied.',
    'test_class_audit':'Measurable d and MeasurableSet A specify the admitted deterministic Borel duration functions and history events. They are not extra dynamics assumptions. d depends on the entire finite tagged history, including state/time, and cannot depend on the unused tail.',
    'literal_audit':'All eleven definitions shared with87 match, including all eight actual recursion definitions from76 and five hazard definitions from75. New liveSurvival and survivalWeight are total tagged extensions with False/0 after stop. Last Fin(n+1) index n matches record n; next tail coordinate0 matches raw w(n). P and clipping remain actual Exp1 product definitions.',
    'whole_four_conjunct_review':[
        'Joint event on the full abstract history times full raw tail is Borel: last-record evaluation, d, raw coordinate0 and clipping are measurable; live-sum branch and strict comparison with jointly measurable extended hitting time are Borel. No support restriction is needed.',
        'Weight is Borel by branchwise composition of jointly Borel finite Lambda with exp and ENNReal.ofReal. Hazard positivity gives 0<=Lambda, so every abstract-history weight is <=1, independently of history support.',
        'Actual parent87 gives the joint law of generated finite history and full unchanged unused raw tail. Parent75 supplies pointwise strict crossing equivalence and single-clock Exp1 survival. Integrating the joint Borel nonnegative event against the product law yields the restricted lintegral against map(history)P, with stop branch zero.',
        'The identity is unnormalized for every Borel A, with no positivity of P(history in A), no regular conditional law, no arbitrary correlated parameter, and no substitution of separately fixed-parameter AE identities at random parameters.'
    ],
    'parent_feasibility':[
        {'declaration':'ActualHazardClock.actual_integrated_hazard_clock_laws','internal_use':'Joint Lambda/tau Borel, Lambda finite/nonnegative/continuous/nondecreasing, exact tau<=u crossing and strict Exp1 survival. No parent conclusion added as public binder.'},
        {'declaration':'ActualFiniteHistoryTailLaw.actual_finite_history_tail_law','internal_use':'Actual history measurability, prefix causality and full tail joint product law. Actual finite-recursion producer76 and actual iid input laws are internal parents, not assumed provider evidence.'},
        {'generic_Mathlib':'measurableSet_lt; Measurable.lintegral_prod_right; lintegral_prod; lintegral_map','use':'Order-Borel event, measurable parameter integration and pushforward lintegral. SFinite/probability instances arise internally. No disintegration or uniform-parameter AE event is needed.'}],
    'counterexample_and_boundary_audit':[
        {'case':'n=0','finding':'History is the initial live record; tail starts at raw coordinate0. Formula reduces to fixed-state survival, with initial-history event of mass0 or1.'},
        {'case':'A null or empty','finding':'Both sides are zero by joint product/restricted lintegral. No division by P(A).'},
        {'case':'stopped last record','finding':'Left liveSurvival is False and right weight0, even if duration reads earlier records. No post-stop phase or waiting time is invented.'},
        {'case':'live current record with next wait infinity','finding':'All finite durations survive this clock; probability formula includes this mass. This case is distinct from an already stopped record.'},
        {'case':'duration0 and zero/negative raw threshold','finding':'At zero clipped threshold tau=0 and strict survival fails pointwise; Exp1 assigns these inputs zero mass. Live weight at duration0 is1, so the identity holds without excluding samples from total definitions.'},
        {'case':'flat or identically zero rate; bounded hazard','finding':'Closed >= first crossing retains strict survival equivalence. No inverse/strictly increasing hazard or finite waiting-time assumption. Infinity mass is allowed.'},
        {'case':'rank0 and zero reflection normal','finding':'Total Lean reflection and stopped recursion remain defined. Rank0 can yield identically zero hazard/infinite first wait; initial live and subsequent stopped cases remain consistent.'},
        {'case':'arbitrary finite history and unbounded d','finding':'All abstract records have actual finite-phase hazard laws; each d(h) is a finite NNReal. Weight<=1 avoids any moment bound on d or on supported histories.'},
        {'case':'endpoint and source guard','finding':'Source crossing uses >=; candidate uses u<tau, hence strict raw threshold exceedance. No replacement by >= survival, normalized finite law or elapsed physical-time residual clock.'}],
    'feasibility_verdict':'TRUE_AS_STATED_AND_FEASIBLE_FROM_EXISTING_INTERNAL_PARENTS_WITH_GENERIC_MEASURABLE_PRODUCT_INTEGRATION',
    'required_repairs':[], 'proof_implementation_attempted':False,
    'exclusions':['random event depth/stopping time','physical-time restart/memorylessness','conditional finite-event density','full path law/A7','temporal Markov or CK','global invariance/operators/query cost','uniform-in-parameters AE event'],
    'proof_or_VERIFIED_or_Goal_credit':False})

decision = write('decision88.json', {
    'status':'ACCEPTED_WHOLE_HEADER_MATHEMATICS_TYPE_AND_DISTINCT_SOURCE_TOPOLOGY_ONLY',
    'reviewer_id':ME,'created_utc':NOW,'observed_head':head,
    'header':header,'mathematical_review':math_review,'source_topology_review':topology,
    'complete_header_typecheck':descriptor(O/'whole-header-typecheck88.receipt.json'),
    'definition_readback':descriptor(O/'definition-readback88.json'),
    'source_integrity':integrity, 'required_repairs':[], 'blocking_findings':[],
    'failure_preservation':'Initial optional bs4 import failed; stdlib HTMLParser primary read succeeded. Original environment failure and exact successful native full-header stdout/stderr/receipt are retained. No header repair or mathematical failure was hidden.',
    'truth_boundary':'Preproof review only, not a Statement Seal, theorem proof, PROVED_LOCAL, VERIFIED, source roundtrip final acceptance, global graph closure, stabilization, main/reader/PURIFIED/full-paper/Goal completion.',
    'canonical_writes':[], 'collaborator_21_RAW_preserved':True})

all_inputs = {d['path']:d for d in math_inputs + author_checked}
extra_paths = [S/'closed-raw-manifest.source-first88.native.json', R/'docs/proof-digestion-protocol.md']
for p in extra_paths:
    d=descriptor(p);all_inputs[d['path']]=d
run = write('run-manifest88.json', {
    'schema':1,'reviewer_id':ME,'created_utc':NOW,'observed_head':head,
    'scope':'Independent complete prospective private Prop math/type review and distinct local source graph/coverage review. No proof search or production/state mutation.',
    'actual_read_or_integrity_checked_inputs':list(all_inputs.values()),
    'read_scope':freeze['parent_read_scope'],
    'mathlib_read_scope':'Only searched/read relevant measurable-product, map, order-Borel and independence APIs. No candidate implementation proof was authored.',
    'source_read_scope':'Complete primary A1.SS1/A1.SS2 independently reread, local author graph/coverage and inherited global inventory/node/junction/atomic-disposition summaries. Author seal script and private long source extract were hashed only, not consulted as rationale. No author source/header verdict read.',
    'chronology':'Earlier candidate exposure explicitly disclosed. Own complete primary reread and source reconstruction frozen before author graph read. Author source-only freeze is separately validated primary-first before candidate.',
    'terminal_typecheck':descriptor(O/'whole-header-typecheck88.receipt.json'),
    'native_environment_failure':descriptor(O/'primary-parser-environment-diagnosis88.json'),
    'mathematical_review':math_review,'topology_review':topology,'decision':decision,
    'all_reads_or_checks_terminal':True,'typecheck_exit_code':0,
    'kernel_axiom_or_dependency_proof_check':'NOT_APPLICABLE_NO_THEOREM_BODY_EXISTS; no theorem proof credit from type-only compile.',
    'no_proof_or_canonical_state_changes':True})

for d in all_inputs.values():
    check(d)
for d in preservation['RAWs']:
    check(d)
owned = [descriptor(p) for p in sorted(O.iterdir()) if p.is_file()]
closed = write('closed-RAW-manifest88.json', {
    'schema':1,'kind':'closed-noncircular-independent-header-math-and-source-topology88',
    'reviewer_id':ME,'created_utc':NOW,'observed_head':head,
    'frozen_current_inputs':list(all_inputs.values()),
    'owned_artifacts':owned,
    'recursive_author_manifest_RAW_validation':integrity,
    'author_private_source_artifacts_excluded_from_publication':author_closed['excluded_from_publication'],
    'content_review_vs_hash_only':'Author source extraction script and long private source extract are integrity-only checks; all source conclusions derive from own pinned primary reread and frozen reconstruction. Full 88 header is read and typechecked; no88 implementation exists.',
    'self_hash_omitted_to_avoid_cycle':True,
    'terminal_receipt_closed':True,'typecheck_exit_code':0,
    'preserved_collaborator_21_RAWs':descriptor(O/'collaborator-preservation88.json'),
    'no_canonical_state_or_proof_credit':True})
for d in owned:
    check(d)
print(json.dumps({'decision':decision,'closed_manifest':closed,
                  'topology':topology,'mathematics':math_review,
                  'run':run,'typecheck_receipt':descriptor(O/'whole-header-typecheck88.receipt.json'),
                  'inputs':len(all_inputs),'owned_outputs_before_closed_manifest':len(owned)},ensure_ascii=False))
