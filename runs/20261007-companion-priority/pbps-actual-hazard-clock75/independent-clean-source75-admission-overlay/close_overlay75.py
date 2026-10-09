import copy
import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent
R75 = OWN.parent
GEN1 = R75 / 'independent-clean-source75'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(name, value):
    (OWN / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def pin(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'RAW_bytes': len(raw), 'RAW_sha256': sha(raw),
            'LF_sha256': sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n'))}


def main():
    assert not (OWN / 'CLOSED_LAST.json').exists()
    gen1_closed = read(GEN1 / 'CLOSED_LAST.json')
    assert sha((GEN1 / 'CLOSED_LAST.json').read_bytes()) == '2de491f96fcce996feb3a98cb4b5da2d1753c6a457188e7c715b314768bf4dd6'
    gen1_files_before = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for p in GEN1.rglob('*') if p.is_file()}
    for item in gen1_closed['complete_owned_prior_manifest']:
        actual = pin(ROOT / item['path'])
        assert actual == item
    gen1_run = read(GEN1 / 'source.0.run.json')
    without_hash = {k: v for k, v in gen1_run.items() if k != 'review_run_sha256'}
    assert sha(canonical(without_hash)) == gen1_closed['review_run_sha256']
    assert gen1_run['findings_full']['verdict'] == 'equivalent-after-elaboration'
    packet_path = R75 / 'source-review.clean.packet.json'
    freeze_path = R75 / 'source-review.clean.freeze75.json'
    packet = read(packet_path)
    assert packet['publication_binding_sha256'] == gen1_run['publication_binding_verification_full']['publication_binding_sha256']
    cell_path = ROOT / 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-hazard-clock.json'
    publication_path = ROOT / 'website/content/publications/pbps-actual-hazard-clock.json'
    cell = read(cell_path)
    publication = read(publication_path)['items'][0]
    clean_freeze = read(freeze_path)
    frozen_inputs = {item['path']: item for item in clean_freeze['inputs']}
    for path in [packet_path, cell_path, publication_path]:
        current = pin(path)
        frozen = frozen_inputs[current['path']]
        assert all(current[k] == frozen[k] for k in ['RAW_bytes', 'RAW_sha256', 'LF_sha256'])
    coverage = read(GEN1 / 'source-proof-coverage75.json')
    review = read(GEN1 / 'source.0.review.json')
    prior_admission = read(GEN1 / 'source.0.admission-fields.json')
    source_link = {'state': 'accepted', 'audit_id': 'ASTIS-RT-20261010-PBPSActualHazardClock',
                   'reviewer': '/root/independent_clean_source75',
                   'reviewer_packet_sha256': review['reviewer_packet_sha256'],
                   'review_run_sha256': review['review_run_sha256'],
                   'run_artifact': (GEN1 / 'source.0.run.json').relative_to(ROOT).as_posix(),
                   'review_artifact': (GEN1 / 'source.0.review.json').relative_to(ROOT).as_posix(),
                   'publication_binding_sha256': packet['publication_binding_sha256'],
                   'evidence': 'Unchanged generation1 independent source-only-first seven-slot and complete BODY review; this administrative overlay adds no mathematical decision or repair.'}
    node_statuses = [{'node': node['id'], 'status': node['independent_scope_disposition'],
                      'BODY_regions': node['reviewed_implementation_mapping']['BODY_regions'],
                      'qualification': node['independent_qualification']} for node in coverage['nodes']]
    def overlay(original):
        value = copy.deepcopy(original)
        report = value['coverage_report']
        assert report['nodes'] == 32 and report['edges'] == 67
        assert report['source_items'] == 137 and report['NODE'] == 77 and report['EXCLUDED'] == 60
        original_open = report['internal_bridges_OPEN']
        assert original_open == 13
        report.update({
            'status': 'independently accepted actual one-clock implementation coverage; future recursive and downstream process nodes remain open or excluded',
            'internal_bridges_OPEN': 0,
            'internal_bridges_REVIEWED_FOR_ONE_CLOCK_CONSUMER': 13,
            'preproof_internal_bridges_OPEN': original_open,
            'future_obligations_count_origin': 'The existing value32 is retained as frozen preproof inventory provenance; it is not a residual first-clock bridge count.',
            'implementation_report': (GEN1 / 'source-proof-coverage75.json').relative_to(ROOT).as_posix(),
            'implementation_map': (R75 / 'implementation-source-map75.json').relative_to(ROOT).as_posix(),
            'source_first_freeze': (GEN1 / 'source-only.freeze75.json').relative_to(ROOT).as_posix(),
            'source_review': source_link,
            'reviewed_node_statuses': node_statuses,
            'source_topology_or_classification_changed': False,
            'original_graph_and_inventory_retained': True,
            'all_137_source_items_independently_classified': True,
            'all_source_RAW_LF_ranges_verified': True,
            'current_module_lines_reviewed': 396, 'current_literal_lets_reviewed': 8,
            'current_source_callers_reviewed': 6, 'current_conclusion_groups_reviewed': 10,
            'current_BODY_steps_reviewed': 9,
            'remaining_open_source_nodes': coverage['remaining_open_source_nodes'],
            'retained_context_nodes': coverage['retained_context_nodes'],
            'excluded_downstream_node': 'N30',
            'N21_qualification': coverage['all_13_internal_bridge_consumer_obligations'][10]['qualification'],
            'N24_qualification': gen1_run['findings_full']['bridge_qualifications']['N24'],
            'historical_header_references': 'Existing complete_literal_and_header/header_projection references are retained only as historical provenance; their files were not opened or re-admitted by this reviewer.',
            'not_Lean_dependency_graph': True, 'whole_paper_coverage': False,
            'full_process_or_Goal_completion': False})
        # Find the consumer qualification by identity rather than relying on a list order.
        report['N21_qualification'] = next(x['qualification'] for x in coverage['all_13_internal_bridge_consumer_obligations'] if x['node'] == 'N21')
        value['coverage_status'] = 'Independent current one-clock implementation source review accepted:137items77NODE60EXCLUDED;32nodes67edges;13internal consumer bridges reviewed with explicit N21/N24 qualifications. N25-N29 remain open,N30 excluded; no full-process/paper/Goal credit.'
        value['source_review'] = source_link
        return value
    cell_overlay = overlay(cell['source_proof_coverage'])
    publication_overlay = overlay(publication['source_proof_coverage'])
    audit_fields = copy.deepcopy(prior_admission['audit_fields'])
    audit_fields['state'] = 'accepted'
    assert audit_fields['source_review']['review_run_sha256'] == gen1_closed['review_run_sha256']
    admission_overlay = {'schema': 'pbps75-independent-administrative-admission-overlay/v1',
                         'accepted': True,
                         'kind': 'unchanged-accepted-review-administration',
                         'reviewer': '/root/independent_clean_source75',
                         'cell_id': cell['cell_id'], 'publication_item_id': publication['id'],
                         'audit_id': 'ASTIS-RT-20261010-PBPSActualHazardClock',
                         'cell_source_proof_coverage': cell_overlay,
                         'publication_source_proof_coverage': publication_overlay,
                         'audit_state_overlay': {'state': 'accepted'},
                         'audit_fields': audit_fields,
                         'source_review_reused_unchanged': source_link,
                         'source_review_run_sha256': review['review_run_sha256'],
                         'publication_binding_sha256': packet['publication_binding_sha256'],
                         'generation1_CLOSED_RAW_sha256': pin(GEN1 / 'CLOSED_LAST.json')['RAW_sha256'],
                         'mathematical_or_source_repair': False,
                         'canonical_application_performed': False, 'VERIFIED_transition_performed': False}
    input_paths = [packet_path, freeze_path, cell_path, publication_path,
                   GEN1 / 'CLOSED_LAST.json', GEN1 / 'source-proof-coverage75.json']
    input_paths += [ROOT / x['path'] for x in gen1_closed['five_named_RAW_outputs']]
    inputs = []
    for n, path in enumerate(input_paths, 1):
        raw = path.read_bytes()
        target = OWN / 'inputs' / f'{n:02d}.{path.name}.RAW'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        inputs.append({**pin(path), 'snapshot': target.relative_to(ROOT).as_posix()})
    manifest = {'schema': 'pbps75-administrative-overlay-input-manifest/v1', 'inputs': inputs,
                'generation1_all_owned_files_unchanged': True,
                'generation1_prior_file_manifest': gen1_closed['complete_owned_prior_manifest'],
                'source_review_run_reused': gen1_closed['review_run_sha256'],
                'no_historical_review_or_exposed_sibling_read': True}
    decision = {'schema': 'pbps75-administrative-overlay-decision/v1',
                'accepted': True, 'administrative_only': True,
                'exact_unchanged_mathematical_verdict': review['verdict'],
                'source_review_run_sha256': review['review_run_sha256'],
                'publication_binding_sha256': packet['publication_binding_sha256'],
                'canonical_keys_authored': ['cell_source_proof_coverage', 'publication_source_proof_coverage', 'audit_state_overlay'],
                'source_node_classification_or_graph_change': False,
                'open_nodes_retained': ['N25', 'N26', 'N27', 'N28', 'N29'],
                'N30_remains_excluded': True, 'mathematical_repairs': [],
                'canonical_application_performed': False, 'VERIFIED_transition_performed': False}
    run = {'schema': 'pbps75-complete-native-administrative-overlay-run/v1',
           'reviewer': '/root/independent_clean_source75', 'actual_PID': os.getpid(),
           'authorization': 'Root explicitly authorized a new sibling independent-clean-source75-admission-overlay directory after generation1 closure; generation1 must remain byte-for-byte immutable.',
           'purpose': 'Supply exact independently authored canonical cell/publication coverage overlays and accepted audit state; reuse unchanged accepted source review, not a source/mathematical repair.',
           'native_hash_convention': 'SHA256 of compact sorted-key ensure_ascii=False UTF8 JSON of this complete overlay.0.run.json excluding only top-level administrative_run_sha256. It is a complete native artifact, not a whole platform transcript claim.',
           'generation1_CLOSED_complete_RAW_utf8': (GEN1 / 'CLOSED_LAST.json').read_text(encoding='utf-8'),
           'generation1_CLOSED_pin': pin(GEN1 / 'CLOSED_LAST.json'),
           'generation1_complete_five_RAW_pins': gen1_closed['five_named_RAW_outputs'],
           'generation1_source_run_hash': review['review_run_sha256'],
           'source_review_and_evidence_unchanged': True,
           'exact_cell_before': cell['source_proof_coverage'],
           'exact_publication_before': publication['source_proof_coverage'],
           'complete_admission_overlay': admission_overlay,
           'complete_input_manifest': manifest, 'complete_decision': decision,
           'root_application_owner': True, 'VERIFIED_transition_performed': False}
    run_hash = sha(canonical(run))
    run['administrative_run_sha256'] = run_hash
    admission_overlay['administrative_run_sha256'] = run_hash
    decision['administrative_run_sha256'] = run_hash
    outputs = {'overlay.0.run.json': run, 'admission-overlay75.json': admission_overlay,
               'overlay.0.input-manifest.json': manifest, 'overlay.0.decision.json': decision}
    # The run contains the complete unhashed overlay/decision by value, so avoid mutation aliasing.
    run['complete_admission_overlay'] = {k: v for k, v in admission_overlay.items() if k != 'administrative_run_sha256'}
    run['complete_decision'] = {k: v for k, v in decision.items() if k != 'administrative_run_sha256'}
    assert sha(canonical({k: v for k, v in run.items() if k != 'administrative_run_sha256'})) == run_hash
    for name, value in outputs.items():
        write(name, value)
    whole_paths = [ROOT / x['path'] for x in gen1_closed['five_named_RAW_outputs']] + [GEN1 / 'CLOSED_LAST.json']
    whole_paths += [OWN / name for name in outputs]
    whole = {'schema': 'pbps75-complete-generation1-plus-administrative-native-payload/v1',
             'native_hash_convention': 'SHA256 compact sorted-key ensure_ascii=False UTF8 JSON excluding only whole_logical_payload_sha256; all ten named payloads below preserve complete RAW UTF8 bytes.',
             'source_review_run_sha256': review['review_run_sha256'], 'administrative_run_sha256': run_hash,
             'complete_named_RAW_payloads': [{**pin(path), 'RAW_utf8': path.read_text(encoding='utf-8')} for path in whole_paths]}
    whole_hash = sha(canonical(whole))
    whole['whole_logical_payload_sha256'] = whole_hash
    write('whole-logical-payload75.json', whole)
    gen1_files_after = {p: (sha(p.read_bytes()), p.stat().st_mtime_ns) for p in GEN1.rglob('*') if p.is_file()}
    assert gen1_files_before == gen1_files_after
    owned = [pin(path) for path in sorted(OWN.rglob('*')) if path.is_file()]
    closed = {'schema': 'pbps75-independent-administrative-overlay-CLOSED-LAST/v1',
              'status': 'CLOSED_LAST', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'actual_PID': os.getpid(), 'actual_EXIT': 0, 'exclusive_last_writer': True,
              'actual_EXIT_basis': 'Immediate SystemExit(0) after last write, separately confirmed by foreground terminal receipt.',
              'generation1_CLOSED_RAW_sha256': pin(GEN1 / 'CLOSED_LAST.json')['RAW_sha256'],
              'generation1_immutable': True, 'source_review_run_sha256': review['review_run_sha256'],
              'administrative_run_sha256': run_hash, 'whole_logical_payload_sha256': whole_hash,
              'complete_owned_prior_file_count': len(owned), 'complete_owned_prior_manifest': owned,
              'postclose_policy': 'No further writes here; standalone read-only verifier prints its result without writing.',
              'canonical_application_performed': False, 'VERIFIED_transition_performed': False}
    write('CLOSED_LAST.json', closed)
    print(json.dumps({'status': 'CLOSED_LAST', 'actual_PID': os.getpid(), 'actual_EXIT': 0,
                      'source_review_run_sha256': review['review_run_sha256'],
                      'administrative_run_sha256': run_hash, 'whole_logical_payload_sha256': whole_hash,
                      'CLOSED_LAST_RAW_sha256': sha((OWN / 'CLOSED_LAST.json').read_bytes()),
                      'complete_owned_prior_file_count': len(owned)}, indent=2), flush=True)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
