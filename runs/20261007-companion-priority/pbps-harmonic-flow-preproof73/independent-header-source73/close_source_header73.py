from pathlib import Path
import copy, hashlib, json, os, sys, traceback

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73'
OWN = BASE / 'independent-header-source73'
GRAPH = ROOT / 'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
REPAIR = BASE / 'independent-header-math73'
LF_RECIPE = 'Replace CRLF byte pairs with LF only; preserve bare CR and every other byte'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load(p):
    return json.loads(p.read_bytes())

def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def write(name, value):
    p = OWN / name
    assert not p.exists(), 'Refuse to overwrite any previous artifact: ' + str(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def pin(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'RAW_bytes': len(b),
            'RAW_sha256': sha(b), 'LF_sha256': sha(b.replace(b'\r\n', b'\n')),
            'LF_recipe': LF_RECIPE}

def member(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'bytes': len(b),
            'raw_sha256': sha(b), 'lf_sha256': sha(b.replace(b'\r\n', b'\n'))}

def check_pin(r):
    p = ROOT / r['path']
    b = p.read_bytes()
    assert len(b) == r['RAW_bytes'] and sha(b) == r['RAW_sha256'], str(p)
    assert sha(b.replace(b'\r\n', b'\n')) == r['LF_sha256'], str(p)

try:
    assert not (OWN / 'lease.final.json').exists()
    stageA = load(OWN / 'StageA.finite-input-pins73.json')
    stageB = load(OWN / 'StageB.header-current-inputs73.manifest.json')
    for r in stageA['inputs'] + [stageA['primary_reference']] + stageB['inputs']:
        check_pin(r)
    frozen = {
        'StageA.source-expectations73.before-header.frozen.json': 'f029d006cc1c6109b8d54c39d88a1a0617ea3115495313090128a024181e2eb9',
        'StageA.topology-decision73.before-header.frozen.json': '970577a488f9ce0bdc1edcd34b74f296f35529e3d0e291fc15792302ac26e998',
        'StageA.independent-source79-classification73.frozen.json': '996dc78d8160c6961e624dff96e7284c3dddeea4747a3b5183936d890c568f48',
        'StageA.independent-binder20-review73.frozen.json': '161db48530cbbf00b61f4807eb3db155efabe1a54ff1c84e2f63ce73673da858',
        'sourcegraph-edge-overlay73/proposal.json': '7aa8520d3ee96ee04757f73ef606c5b677eb9819775bc738203469b6aa56f939'
    }
    for n, s in frozen.items():
        assert sha((OWN / n).read_bytes()) == s, n

    # This is the ONLY decoded decision from the distinct reviewer scope.
    repair_bytes = (REPAIR / 'repair-decision.json').read_bytes()
    assert len(repair_bytes) == 4491
    assert sha(repair_bytes) == '80b5002de1e2225886d772ae6a19e40320a1f7fca351192cd60ad26a6378c4a4'
    repair = json.loads(repair_bytes)
    assert repair['accepted'] and repair['reviewer_distinct_from_overlay_author']
    assert not repair['original_graph_coverage_self_approved']
    assert repair['proposal']['RAW_sha256'] == frozen['sourcegraph-edge-overlay73/proposal.json']
    assert repair['actual_review_PID'] == 47896
    # Opaque hash only: do not parse lease, header verdict or full reviewer payload.
    repair_lease = pin(REPAIR / 'lease.final.json')
    assert repair_lease['RAW_sha256'] == '2aec2b262f447a7401fabb3108b109bf825bcef82dd258e87a2786a091a4d691'
    d = OWN / 'repair-inputs'
    d.mkdir(exist_ok=False)
    (d / 'repair-decision.exactraw.snapshot.json').write_bytes(repair_bytes)
    (d / 'repair-decision.LF.snapshot.json').write_bytes(repair_bytes.replace(b'\r\n', b'\n'))
    repair_ref = {'decision': pin(REPAIR / 'repair-decision.json'), 'opaque_closed_lease': repair_lease,
                  'decoded_authorization': 'Narrow two-edge repair decision only',
                  'header_math_verdict_or_full_payload_decoded': False,
                  'reviewer': '/root/exact_science63', 'actual_review_PID': 47896, 'exit_code': 0,
                  'scope_member_count_reported_by_root': 90,
                  'member_count_independently_replayed_here': False,
                  'my_proposal_self_approved': False}
    write('distinct-two-edge-repair73.authority.json', repair_ref)

    proposal = load(OWN / 'sourcegraph-edge-overlay73/proposal.json')
    original = load(GRAPH / 'source-proof-graph.json')
    assert len(original['nodes']) == 23 and len(original['edges']) == 35
    assert len(proposal['add_only_edges']) == 2
    old_pairs = {(e['producer'], e['consumer']) for e in original['edges']}
    new_pairs = {(e['producer'], e['consumer']) for e in proposal['add_only_edges']}
    assert new_pairs == {('SCALE', 'GROUP'), ('ENERGY', 'ENERGY-NONNEG')}
    assert not old_pairs & new_pairs
    assert {(e['producer'], e['consumer']) for e in repair['two_edges']} == new_pairs
    nodes = {n['id'] for n in original['nodes']}
    edges = copy.deepcopy(original['edges']) + copy.deepcopy(proposal['add_only_edges'])
    assert len(nodes) == 23 and all(e['producer'] in nodes and e['consumer'] in nodes for e in edges)
    # Independently check acyclicity of this finite source-obligation projection.
    incoming = {n: 0 for n in nodes}
    adjacency = {n: [] for n in nodes}
    for e in edges:
        incoming[e['consumer']] += 1
        adjacency[e['producer']].append(e['consumer'])
    todo = sorted(n for n in nodes if incoming[n] == 0)
    order = []
    while todo:
        n = todo.pop(0)
        order.append(n)
        for v in adjacency[n]:
            incoming[v] -= 1
            if incoming[v] == 0:
                todo.append(v)
    assert len(order) == 23
    projection = {'schema': 'astis-independent-source-topology-projection73/v1',
                  'status': 'ACCEPTED_SOURCE_OBLIGATION_TOPOLOGY_WITH_DISTINCT_TWO_EDGE_REPAIR',
                  'original_graph': pin(GRAPH / 'source-proof-graph.json'),
                  'original_graph_unmodified': True, 'nodes': copy.deepcopy(original['nodes']),
                  'edges': edges, 'node_count': 23, 'edge_count': 37, 'original_edge_count': 35,
                  'exact_original_nodes_and_edges_retained': True, 'source_gap_count': 7,
                  'source_gap_node_ids': original['source_gap_node_ids'],
                  'source_coverage': pin(OWN / 'StageA.independent-source79-classification73.frozen.json'),
                  'source_regions': 13, 'source_blocks': 51, 'semantic_items': 79, 'NODE': 24, 'EXCLUDED': 55,
                  'binder_inventory': {'SOURCE': 4, 'STANDING': 6, 'TYPING': 10, 'EXCESS': 0},
                  'distinct_repair': repair_ref, 'finite_DAG_check': {'acyclic': True, 'order': order},
                  'layer': 'Source reconstructed proof obligations; never compiled Lean implication',
                  '73_proof_or_fullpaper_credit': False}
    write('source-proof-graph73.reviewed-projection.json', projection)

    primary = ROOT / stageA['primary_reference']['path']
    raw = primary.read_bytes()
    blocks = load(GRAPH / 'source.blocks.json')
    regions = []
    for region in blocks['regions']:
        a, b = region['raw_byte_start_inclusive'], region['raw_byte_end_exclusive']
        selected = raw[a:b]
        assert sha(selected) == region['whole_region_raw_sha256']
        rs = {'source_id': region['source_id'], 'RAW_start_inclusive': a, 'RAW_end_exclusive': b,
              'RAW_bytes': len(selected), 'RAW_sha256': sha(selected),
              'LF_sha256': sha(selected.replace(b'\r\n', b'\n')), 'blocks': []}
        for block in region['blocks']:
            aa, bb = block['raw_byte_start_inclusive'], block['raw_byte_end_exclusive']
            selected_block = raw[aa:bb]
            assert sha(selected_block) == block['literal_span_raw_sha256']
            rs['blocks'].append({'block_id': block['block_id'], 'RAW_start_inclusive': aa,
                                 'RAW_end_exclusive': bb, 'RAW_bytes': len(selected_block),
                                 'RAW_sha256': sha(selected_block),
                                 'LF_sha256': sha(selected_block.replace(b'\r\n', b'\n'))})
        regions.append(rs)
    assert len(regions) == 13 and sum(len(r['blocks']) for r in regions) == 51
    write('source13-region51-block.finite-RAW-LF-map73.json',
          {'primary': pin(primary), 'LF_recipe': LF_RECIPE, 'range_semantics': '[inclusive,exclusive)',
           'reference_not_duplicate_source_payload': True, 'regions': regions})

    # Whole-file hashes are provenance only; only these two exact call ranges were read mathematically.
    reuse = load(GRAPH / 'reuse.gradient-continuity.json')
    calls = []
    extra_inputs = []
    for c in reuse['actual_existing_consumers']:
        p = ROOT / c['path']
        b = p.read_bytes()
        assert sha(b) == c['whole_file_raw_sha256']
        selected = b[c['raw_byte_start_inclusive']:c['raw_byte_end_exclusive']]
        assert sha(selected) == c['literal_span_raw_sha256']
        calls.append({'path': c['path'], 'RAW_start_inclusive': c['raw_byte_start_inclusive'],
                      'RAW_end_exclusive': c['raw_byte_end_exclusive'], 'RAW_sha256': sha(selected),
                      'LF_sha256': sha(selected.replace(b'\r\n', b'\n')),
                      'whole_module_mathematical_review': False})
        extra_inputs.append(pin(p))
    inputs = stageA['inputs'] + [stageA['primary_reference']] + stageB['inputs'] + extra_inputs + [repair_ref['decision'], repair_lease]
    assert len(inputs) == len({r['path'] for r in inputs}) == 29
    write('source-header73.input-manifest.json',
          {'schema': 'astis-finite-source-header-inputs73/v1', 'input_count': len(inputs), 'inputs': inputs,
           'gradient_consumer_read_ranges': calls,
           'source_ranges': pin(OWN / 'source13-region51-block.finite-RAW-LF-map73.json'),
           'source_snapshot_policy': 'Reuse immutable exact fixed primary plus finite RAW range and LF recipe; no recursive prior packet copies',
           'new_candidate_snapshots': pin(OWN / 'StageB.header-current-inputs73.manifest.json'),
           'narrow_repair_snapshot': 'repair-inputs/repair-decision.exactraw.snapshot.json',
           'current_pins_rechecked_unchanged': True, 'LF_recipe': LF_RECIPE})

    semantic_checks = [
        {'slot': 'source_assumptions_and_callers', 'verdict': 'accept', 'reason': 'Same six source-standing callers; complete real C2/both Hessian bounds/eta positivity/non-strict cap; no ingredient premise'},
        {'slot': 'definitions_actual_inputs', 'verdict': 'accept', 'reason': 'Actual c=y-eta gradientVxRef; literal Phi; weighted SUM H with same center and eta'},
        {'slot': 'quantifiers_and_domains', 'verdict': 'accept', 'reason': 'All y,xRef,t,x,p jointly for continuity/Borel; arbitrary z packages x,p; all-real group/time/energy'},
        {'slot': 'conclusions_and_coefficients', 'verdict': 'accept', 'reason': 'All nine conjuncts; exact two ODE coefficients/signs/reference gradient, inverse laws and pi endpoint'},
        {'slot': 'source_omitted_bridges', 'verdict': 'accept_as_internal_obligations', 'reason': 'Seven source gaps visible; local Gradient producer found; no public supplied proof certificate'},
        {'slot': 'degenerate_and_endpoint_cases', 'verdict': 'accept', 'reason': 'Rank0/alphaeta1/zero energy retained, eta>0, no normal division or strict cap'},
        {'slot': 'truth_boundary_and_representation', 'verdict': 'accept_prospective_header_only', 'reason': 'Private literal is nonprovider; empty theorem proof; no stochastic/bounce/kernel/nonexplosion/invariance/full result credit'}
    ]
    decision = {
        'schema': 'astis-independent-source-topology-and-prospective-header73/v1',
        'reviewer': '/root/independent_primary69', 'verdict': 'ACCEPT_SOURCE_TOPOLOGY_AND_PROSPECTIVE_HEADER_SEAL_READY',
        'source_topology_admission': 'accept original23nodes35edges with separately reviewed add-only2edges; final23nodes37edges',
        'header_admission': 'accept exact prospective signature only; no mathematical/binder/formula repair required',
        'header': stageB['inputs'][0], 'before_header_expectations': pin(OWN / 'StageA.source-expectations73.before-header.frozen.json'),
        'before_header_historical_topology_decision': pin(OWN / 'StageA.topology-decision73.before-header.frozen.json'),
        'source_topology': pin(OWN / 'source-proof-graph73.reviewed-projection.json'),
        'coverage': {'source_regions': 13, 'source_blocks': 51, 'semantic_items': 79, 'NODE': 24, 'EXCLUDED': 55,
                     'nodes': 23, 'edges_original': 35, 'edges_after_distinct_overlay': 37, 'SOURCE_GAP': 7,
                     'semantic_binders': 20, 'SOURCE': 4, 'STANDING': 6, 'TYPING': 10, 'EXCESS': 0,
                     'conjuncts': 9, 'six_private_public_caller_prefixes_exact_equal': True},
        'semantic_checks': semantic_checks,
        'deltas': [
            {'id': '73-sourcegraph-scale-group', 'classification': 'source-ingredient-edge-completion',
             'producer': 'SCALE', 'consumer': 'GROUP', 'binder_or_formula_change': False, 'distinct_approval': repair_ref['decision']},
            {'id': '73-sourcegraph-energy-nonneg', 'classification': 'source-definition-edge-completion',
             'producer': 'ENERGY', 'consumer': 'ENERGY-NONNEG', 'binder_or_formula_change': False, 'distinct_approval': repair_ref['decision']},
            {'id': '73-header-attribution-comment', 'classification': 'attribution-only-representation',
             'noncomment_Lean_bytes_unchanged': True, 'mathematical_delta': False},
            {'id': '73-source-derived-internal-completions', 'classification': 'explicit-source-omitted-bridge-obligations',
             'items': ['all-real extension/group/two inverses', 'joint continuity and Borel adapter', 'exact energy nonnegativity', 'derivative/trigonometric/scale/norm cancellation'],
             'future_internal_production_required': True, 'new_public_premise': False}
        ],
        'blocking_header_repairs': [], 'independent_graph_repair': repair_ref,
        'existing_producer': pin(OWN / 'StageA.gradient-producer-independent-check73.frozen.json'),
        'typing_context': {'root_actual_PID': 50512, 'exit_code': 0, 'credit': 'private target Prop formation only; no proof'},
        'exposure': {'not_source_blind': True,
                     'prior': ['70/71 full source/implementation/publication', '72 prospective and whole implementation/source/publication', 'B27 bounded dependency diagnosis'],
                     '73_expectations_frozen_before_header_or_hash': True, '73_proof_BODY_read': False,
                     'other73_header_math_decision_or_full_payload_read': False, 'new72_review_verdict_read': False,
                     'distinct_repair_read_after_own_header_judgments': True},
        'remaining_open': ['73 implementation and proof of all nine clauses', 'internal omitted-source bridges',
                           'bounce/hazard/nonexplosion', 'stochastic Markov/stationarity/invariance',
                           'actual terminal H/kernel and H1/B2', 'actual B27/B28 and main/error/cost result',
                           'reader exposition/integration and independent theorem verification'],
        'credit': {'proof': False, 'implementation_source_fidelity': False, 'compile_of_theorem': False,
                  'SAU_claim_or_seal_written': False, 'SCI': False, 'VERIFIED': False,
                  'Exposition_Seal': False, 'PURIFIED': False, 'main_live': False, 'whole_paper': False, 'Goal': False},
        'canonical_Git_ledger_or_old_CLOSED_writes': False,
        'review': pin(OWN / 'source-header73.review.RAW.md'), 'input_manifest': pin(OWN / 'source-header73.input-manifest.json')
    }
    write('source-header73.decision.json', decision)
    write('StageB.final-observer-negatives73.json', {
        'events': [{'tool_chunk': 'f661d0', 'exit_code': 1, 'actual_pid': 'not reported; not invented',
                    'classification': 'PowerShell foreach pipeline parser observation error before file operations',
                    'correction_tool_chunk': '1d3493', 'correction_exit_code': 0,
                    'canonical_or_owned_mutation_by_failed_observation': False}],
        'StageA_negative_preserved': pin(OWN / 'StageA.observer-negatives73.json')})
    write('source-header73.close.terminal.json', {'actual_pid': os.getpid(), 'exit_code': 0, 'argv': sys.argv,
                                                'background': False, 'task': 'finite pins/source topology/header closure; no Lean compile'})
    run = {'schema': 'astis-source-header73-native-run/v1', 'reviewer': '/root/independent_primary69',
           'owned_scope': OWN.relative_to(ROOT).as_posix(), 'status': 'SOURCE_TOPOLOGY_AND_PROSPECTIVE_HEADER_REVIEW_COMPLETE',
           'decision': pin(OWN / 'source-header73.decision.json'), 'review': pin(OWN / 'source-header73.review.RAW.md'),
           'input_manifest': pin(OWN / 'source-header73.input-manifest.json'),
           'reviewed_source_topology': pin(OWN / 'source-proof-graph73.reviewed-projection.json'),
           'source_coverage79': pin(OWN / 'StageA.independent-source79-classification73.frozen.json'),
           'native_prior_reference_integrity': pin(OWN / 'StageA.native-reference-integrity73.json'),
           'terminal_receipts': [pin(OWN / n) for n in [
               'StageA.freeze-inputs.terminal.json', 'StageA.author-expectations.terminal.json',
               'StageA.edge-overlay-proposal.terminal.json', 'StageB.header-review.terminal.json',
               'source-header73.close.terminal.json']],
           'frozen_before_header_hashes': frozen, 'distinct_repair': repair_ref,
           'no_proof_compile_VERIFIED_or_fullpaper_credit': True,
           'whole_logical_hash_recipe': 'SHA256 canonical JSON UTF8 ensure_ascii=False sort_keys=True separators=(comma,colon); delete ONLY top-level run_sha256'}
    run['run_sha256'] = sha(canonical(run))
    write('run.json', run)
    named = []
    for n in ['source-header73.review.RAW.md', 'source-header73.decision.json', 'source-header73.input-manifest.json', 'run.json']:
        p = OWN / n
        named.append({'name': n, 'pin': pin(p), 'complete_RAW_UTF8': p.read_bytes().decode('utf-8')})
    write('complete-named-review-decision-input-payload.json', {
        'schema': 'astis-small-complete-named-source-header-payload73/v1', 'named_payloads': named,
        'named_payload_count': 4, 'whole_logical_run_sha256': run['run_sha256'],
        'all_other_owned_evidence': 'whole-owned.manifest.json and lease.final.json enumerate exact native files',
        'immutable_prior_packets': 'finite referenced pins only; no recursive historical payload or base64 copies'})
    files = sorted(p for p in OWN.rglob('*') if p.is_file())
    write('whole-owned.manifest.json', {'schema': 'astis-whole-owned-native-manifest73/v1',
                                       'scope': OWN.relative_to(ROOT).as_posix(), 'LF_recipe': LF_RECIPE,
                                       'excludes': ['whole-owned.manifest.json (self)', 'lease.final.json (last closure)'],
                                       'count': len(files), 'files': [member(p) for p in files]})
    files_with_manifest = sorted(p for p in OWN.rglob('*') if p.is_file())
    # LAST OWNED WRITE. Every later operation must be read-only.
    write('lease.final.json', {'schema': 'astis-closed-last-native-lease73/v1', 'status': 'CLOSED_LAST',
                               'owned_scope': OWN.relative_to(ROOT).as_posix(), 'actual_close_pid': os.getpid(),
                               'exit_code': 0, 'background': False, 'member_count_except_self': len(files_with_manifest),
                               'owned_file_count_including_self': len(files_with_manifest) + 1,
                               'whole_logical_run_sha256': run['run_sha256'],
                               'whole_owned_manifest': pin(OWN / 'whole-owned.manifest.json'),
                               'all_files_except_self': [member(p) for p in files_with_manifest],
                               'LF_recipe': LF_RECIPE, 'close_order': 'lease.final.json is final owned write; postclose read-only',
                               'source_topology_header_credit_only': True, 'canonical_or_old_CLOSED_written': False})
    print(json.dumps({'actual_pid': os.getpid(), 'exit_code': 0,
                      'owned_file_count': len(files_with_manifest) + 1,
                      'whole_logical_run_sha256': run['run_sha256'],
                      'decision': pin(OWN / 'source-header73.decision.json'),
                      'payload': pin(OWN / 'complete-named-review-decision-input-payload.json'),
                      'manifest': pin(OWN / 'whole-owned.manifest.json'), 'lease': pin(OWN / 'lease.final.json')},
                     ensure_ascii=False, indent=2))
except BaseException:
    traceback.print_exc()
    # Do not mutate any owned file on failure, especially after a possible closure.
    sys.exit(1)
