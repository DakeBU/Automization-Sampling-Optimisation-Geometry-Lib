import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent
R75 = OWN.parent
BASE = ROOT / 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def sha(value):
    return hashlib.sha256(value).hexdigest()


def read(name):
    return json.loads((OWN / name).read_text(encoding='utf-8'))


def write(name, value):
    (OWN / name).write_bytes((json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))


def pin(path):
    raw = path.read_bytes()
    return {'path': path.relative_to(ROOT).as_posix(), 'RAW_bytes': len(raw), 'RAW_sha256': sha(raw),
            'LF_sha256': sha(raw.replace(b'\r\n', b'\n').replace(b'\r', b'\n'))}


def main():
    assert not (OWN / 'CLOSED_LAST.json').exists(), 'already closed; do not mutate'
    findings = read('independent-findings75.json')
    packet = json.loads((R75 / 'source-review.clean.packet.json').read_text(encoding='utf-8'))
    mechanical = read('mechanical-verification75.json')
    assert mechanical['terminal']['actual_EXIT'] == 0
    assert findings['accepted'] and not findings['blocking_deltas']
    for item in mechanical['inputs']:
        current = pin(ROOT / item['path'])
        assert all(current[k] == item[k] for k in ['RAW_bytes', 'RAW_sha256', 'LF_sha256']), item['path']
    generic_paths = [
        '.agents/skills/astis-semantic-roundtrip/SKILL.md', 'docs/theorem-publication-protocol.md',
        'tools/astis_publication.py', 'tools/astis_semantic_roundtrip.py', 'tools/astis_semantic_roundtrip_core.py',
        '.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean',
        '.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean',
        '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean']
    generic_receipts = []
    for n, name in enumerate(generic_paths, 1):
        path = ROOT / name
        target = OWN / 'generic-inputs' / f'{n:02d}.{path.name}.RAW'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
        generic_receipts.append({**pin(path), 'snapshot': target.relative_to(ROOT).as_posix(),
                                 'read_scope': 'Only the skill/protocol text or bounded API regions actually named in the native read register were semantically inspected; full file snapshot pins the substrate.'})
    graph = json.loads((BASE / 'source-proof-graph75.json').read_text(encoding='utf-8'))
    inventory = json.loads((BASE / 'source-coverage-inventory75.json').read_text(encoding='utf-8'))
    imap = json.loads((R75 / 'implementation-source-map75.json').read_text(encoding='utf-8'))
    mapped = {n['source_node']: n for n in imap['nodes']}
    context = {'N05', 'N32'}
    opened = {'N25', 'N26', 'N27', 'N28', 'N29'}
    nodes = []
    for node in graph['nodes']:
        ident = node['id']
        scope = ('OPEN-FUTURE-CONSUMER' if ident in opened else 'EXCLUDED-DOWNSTREAM-CONTEXT' if ident == 'N30'
                 else 'RETAINED-CONTEXT-NO-THEOREM-CREDIT' if ident in context else 'ACCEPTED-BOUNDED-ONE-CLOCK-INGREDIENT')
        nodes.append({**node, 'independent_scope_disposition': scope,
                      'reviewed_implementation_mapping': mapped[ident],
                      'independent_qualification': findings['bridge_qualifications'].get(ident, ''),
                      'source_topology_not_Lean_implication': True})
    items = [{**item, 'independent_review': 'Accepted exact source-range classification within this bounded selected universe; implementation coverage follows its named node dispositions, not automatic theorem completion.'} for item in inventory['items']]
    coverage = {'schema': 'pbps75-fresh-independent-source-proof-coverage/v1',
                'reviewer': '/root/independent_clean_source75',
                'status': 'ACCEPTED_BOUNDED_IMPLEMENTATION_SOURCE_COVERAGE',
                'publication_binding_sha256': packet['publication_binding_sha256'],
                'source_first_freeze': pin(OWN / 'source-only.freeze75.json'),
                'node_count': 32, 'edge_count': 67, 'item_count': 137, 'NODE': 77, 'EXCLUDED': 60,
                'internal_bridge_count': 13, 'selected_formula_count': 23,
                'source_graph_preserved': True, 'source_classifications_preserved': True,
                'source_topology_or_classification_changed': False,
                'all_source_RAW_LF_ranges_verified': True,
                'not_Lean_dependency_graph': True, 'whole_paper_coverage': False,
                'nodes': nodes, 'edges': graph['edges'], 'items': items,
                'all_13_internal_bridge_consumer_obligations': [
                    {'node': ident, 'accepted_for_current_consumer': True,
                     'qualification': findings['bridge_qualifications'].get(ident, 'Discharged by the independently inspected exact BODY regions in this node mapping.')} for ident in imap['source_gap_ids']],
                'remaining_open_source_nodes': sorted(opened), 'excluded_downstream_node': 'N30',
                'retained_context_nodes': sorted(context), 'truth_boundary': findings['truth_boundary']}
    write('source-proof-coverage75.json', coverage)
    input_manifest = {'schema': 'pbps75-fresh-independent-complete-input-manifest/v1',
                      'source_only_before_implementation': True,
                      'source_only_inputs': read('source-only-input-manifest75.json'),
                      'source_only_freeze': read('source-only.freeze75.json'),
                      'clean_finite_inputs': mechanical['inputs'], 'generic_API_inputs': generic_receipts,
                      'clean_authorization': 'Root authorized ONLY clean packet/freeze and finite listed inputs after source-only freeze; no original packet/freeze, before-clean snapshot, metadata-overlay, exposed sibling or historical preproof reviewer decision read.',
                      'no_global_session_store_search': True, 'no_canonical_or_Git_mutation': True,
                      'owned_writes': OWN.relative_to(ROOT).as_posix()}
    run = {'schema': 'pbps75-fresh-independent-native-source-review-run/v1',
           'reviewer': '/root/independent_clean_source75', 'formalizer': packet['roles']['formalizer'],
           'blind_decoder': packet['roles']['blind_decoder'],
           'independent_from_formalizer': True, 'independent_from_decoder': True,
           'native_hash_convention': 'SHA256 of compact sorted-key ensure_ascii=False UTF-8 JSON of this complete source.0.run.json logical object, excluding only top-level review_run_sha256. This is the full native review artifact, not a whole platform transcript claim.',
           'phase_order': ['primary+permitted-source-baseline', 'own-source-only-expectations-and-freeze',
                           'root-clean-packet-authorization', 'full-current-code+decoder+source+formula-review',
                           'independent-focused-Lean+axiom-check', 'independent-publication-binding-recomputation',
                           'seven-slot+ten-group+nine-BODY+32-node+137-item-verdict', 'exclusive-close', 'standalone-read-only-verification'],
           'source_first_expectations': read('source-only.expectations75.json'),
           'source_first_freeze': read('source-only.freeze75.json'),
           'source_only_verification': read('source-only-input-manifest75.json'),
           'source_only_primary_extract_utf8': (OWN / 'source-only-primary-extract75.txt').read_text(encoding='utf-8'),
           'clean_official_packet_full': packet,
           'input_manifest_full': input_manifest,
           'mechanical_verification_full': mechanical,
           'publication_binding_verification_full': read('publication-binding-verification75.json'),
           'findings_full': findings, 'source_proof_coverage_full': coverage,
           'compiler_stdout_full': (OWN / 'focused-lean75.stdout.RAW.txt').read_text(encoding='utf-8'),
           'compiler_stderr_full': (OWN / 'focused-lean75.stderr.RAW.txt').read_text(encoding='utf-8'),
           'substantive_read_register': [
               'Exact primary source six bounded regions; all 137 classifications, 23 literal formulas, 32 source nodes, 67 source edges and all 13 internal bridge obligations.',
               'Permitted stageA provenance only; its sibling expectations, review payloads, decisions, header/source reviews and admissions were not opened.',
               'Whole current ActualHazardClock module, all private definitions/helpers, eight lets, six callers, ten conclusion groups, all nine exact authored BODY slices and current source-map nodes.',
               'ActualHarmonicFlow and ActualBounceRate exact producer statements and needed internal continuity/energy/Lipschitz projections; source-backed proof ingredients stay internal.',
               'Full clean source/reconstruction packet; decoder reconstruction, native run and closure pins from finite input manifest. No decoder was created or prompted by this reviewer.',
               'Pinned Lean toolchain and lake manifest; Mathlib hittingAfter definition65-81, expMeasure/probability definitions93-100 and CDF165-174, continuous parametric primitive494-509.',
               'Generic semantic/publication hash and admission API definitions; exact current binding recomputed from listed files without whole registry scan.',
               'Finite current frontier-cell/audit key shape and source_proof_coverage/proof_digestion only. No historical referenced header review file was followed.'
           ],
           'nonmathematical_terminal_recoveries': [
               {'kind': 'PowerShell-parser', 'event': 'foreach pipeline syntax rejected before reading; corrected to collect items first.'},
               {'kind': 'stdout-encoding', 'event': 'GBK could not emit a source proof-end symbol; subsequent source extraction used Python -X utf8.'},
               {'kind': 'optional-parser-availability', 'event': 'bs4 absent; no install performed; dependency-free HTMLParser used.'},
               {'kind': 'Python-version-API', 'event': 'write_text newline argument unsupported; replaced by explicit UTF8 write_bytes before successful source freeze.'},
               {'kind': 'JSON-key-lookup', 'event': 'Lesson list is steps rather than proof_steps; corrected inspection; no mathematical/canonical edit.'}
           ],
           'actual_close_writer_PID': os.getpid(), 'expected_foreground_close_EXIT': 0,
           'source_review_admission_only': True, 'VERIFIED_transition_performed': False,
           'full_platform_transcript_hash_claimed': False}
    run_hash = sha(canonical(run))
    run['review_run_sha256'] = run_hash
    review_evidence = 'Fresh source-only freeze before clean packet; all seven semantic slots, complete 396-line module/private helpers, six callers/eight lets/ten groups/nine exact BODY formula steps and preserved 32-node/67-edge/137-item/13-bridge source coverage independently compared. Exact whole-module focused Lean PID43360 EXIT0 and standard axioms; exact current publication binding recomputed. Accepted only bounded one-clock prerequisites; future process obligations remain open. Native complete run hash convention is stated in source.0.run.json.'
    audit_fields = {'semantic_slots': findings['semantic_slots'], 'deltas': [],
                    'verdict': findings['verdict'],
                    'source_review': {'state': 'accepted', 'reviewer': '/root/independent_clean_source75',
                                      'independent_from_formalizer': True, 'independent_from_decoder': True,
                                      'reviewer_packet_sha256': packet['packet_sha256'],
                                      'review_run_sha256': run_hash,
                                      'run_artifact': (OWN / 'source.0.run.json').relative_to(ROOT).as_posix(),
                                      'evidence': review_evidence},
                    'publication_binding_sha256': packet['publication_binding_sha256']}
    review = {'schema_version': 1, 'semantic_slots': findings['semantic_slots'], 'deltas': [],
              'verdict': findings['verdict'], 'repairs': [], 'reviewer': '/root/independent_clean_source75',
              'independent_from_formalizer': True, 'independent_from_decoder': True,
              'review_evidence': review_evidence, 'review_run_sha256': run_hash,
              'reviewer_packet_sha256': packet['packet_sha256'],
              'publication_binding_sha256': packet['publication_binding_sha256'],
              'findings_full': findings, 'source_proof_coverage': (OWN / 'source-proof-coverage75.json').relative_to(ROOT).as_posix()}
    summary_coverage = {k: v for k, v in coverage.items() if k not in ['nodes', 'edges', 'items', 'all_13_internal_bridge_consumer_obligations']}
    summary_coverage['coverage_report'] = (OWN / 'source-proof-coverage75.json').relative_to(ROOT).as_posix()
    decision = {'schema': 'pbps75-clean-independent-source-decision/v1', 'accepted': True,
                'verdict': findings['verdict'], 'blocking_deltas': [], 'repairs': [],
                'reviewer': '/root/independent_clean_source75', 'review_run_sha256': run_hash,
                'reviewer_packet_sha256': packet['packet_sha256'],
                'publication_binding_sha256': packet['publication_binding_sha256'],
                'source_first': True, 'scope': findings['truth_boundary'],
                'nonblocking_observations': findings['nonblocking_observations'],
                'source_proof_coverage': summary_coverage,
                'canonical_admission_owner': 'root only; not applied by reviewer', 'VERIFIED': False}
    admission = {'schema': 'pbps75-clean-independent-source-admission-fields/v1',
                 'audit_id': 'ASTIS-RT-20261010-PBPSActualHazardClock', 'accepted': True,
                 'audit_fields': audit_fields, 'source_proof_coverage': summary_coverage,
                 'reviewer_packet_sha256': packet['packet_sha256'], 'review_run_sha256': run_hash,
                 'publication_binding_sha256': packet['publication_binding_sha256'],
                 'mathematical_repairs': [], 'canonical_application_performed': False,
                 'VERIFIED_transition_performed': False, 'scope': findings['truth_boundary']}
    outputs = {'source.0.run.json': run, 'source.0.decision.json': decision,
               'source.0.review.json': review, 'source.0.input-manifest.json': input_manifest,
               'source.0.admission-fields.json': admission}
    for name, payload in outputs.items():
        write(name, payload)
    whole = {'schema': 'pbps75-five-complete-named-RAW-logical-payload/v1',
             'native_hash_convention': 'Whole logical payload hash is SHA256 of compact sorted-key ensure_ascii=False UTF8 JSON excluding only top-level whole_logical_payload_sha256; each payload preserves the complete exact named RAW UTF8 bytes.',
             'review_run_sha256': run_hash,
             'complete_named_RAW_payloads': [{**pin(OWN / name), 'RAW_utf8': (OWN / name).read_text(encoding='utf-8')} for name in outputs]}
    whole['whole_logical_payload_sha256'] = sha(canonical(whole))
    write('whole-logical-payload75.json', whole)
    manifest = [pin(path) for path in sorted(OWN.rglob('*')) if path.is_file()]
    closed = {'schema': 'pbps75-clean-independent-CLOSED-LAST/v1',
              'status': 'CLOSED_LAST', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
              'actor': '/root/independent_clean_source75', 'actual_PID': os.getpid(),
              'actual_EXIT': 0, 'actual_EXIT_basis': 'Writer calls SystemExit(0) immediately after this last write; foreground terminal receipt independently confirms the actual exit.',
              'exclusive_last_writer': True, 'owned_directory': OWN.relative_to(ROOT).as_posix(),
              'review_run_sha256': run_hash, 'whole_logical_payload_sha256': whole['whole_logical_payload_sha256'],
              'five_named_RAW_outputs': [pin(OWN / name) for name in outputs],
              'complete_owned_prior_file_count': len(manifest), 'complete_owned_prior_manifest': manifest,
              'self_manifest_rule': 'CLOSED_LAST binds every prior owned file; this last file cannot self-hash. Its RAW hash is independently reported by the standalone readonly verifier and foreground receipt.',
              'postclose_policy': 'No further writes inside owned directory. Standalone read_only_verify75.py reads and prints only.',
              'no_canonical_or_Git_edit': True, 'VERIFIED_transition_performed': False}
    write('CLOSED_LAST.json', closed)
    print(json.dumps({'status': 'CLOSED_LAST', 'actual_PID': os.getpid(), 'actual_EXIT': 0,
                      'review_run_sha256': run_hash, 'whole_logical_payload_sha256': whole['whole_logical_payload_sha256'],
                      'CLOSED_LAST_RAW_sha256': sha((OWN / 'CLOSED_LAST.json').read_bytes()),
                      'complete_owned_prior_file_count': len(manifest)}, indent=2), flush=True)
    raise SystemExit(0)


if __name__ == '__main__':
    main()
