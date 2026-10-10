import os
import sys
sys.dont_write_bytecode = True
from seal_common import *

initial = (OUT / 'initial-source-lease.raw.snapshot.json').read_bytes()
assert (BASE / 'source.review.lease.json').read_bytes() == initial
assert load(BASE / 'source.review.lease.json')['status'] == 'OPEN'
inputs = check_inputs()
verification = load(OUT / 'input-verification.json')
check_self(verification)
assert verification['all_match'] and verification['math_freeze602_current_unchanged']
assert not verification['whole_math_verdict_read'] and not verification['compiler_started_by_reviewer']
for name in ['publication.binding.payload.json', 'semantic.result.template.json', 'source.review.json', 'verification.process.status.json']:
    check_self(load(OUT / name))
binding = load(OUT / 'publication.binding.payload.json')
assert binding['named_payload_sha256'] == sha(canonical(binding['payload']))
packet = load(BASE / 'source.0.reviewer-packet.json')
check_self(packet, 'packet_sha256')
assert packet['publication_binding_sha256'] == binding['named_payload_sha256']
assert pin(OUT / 'production.header.seal.normalized.lf.snapshot.lean')['bytes'] == 1244
assert pin(OUT / 'production.header.seal.normalized.lf.snapshot.lean')['raw_sha256'] == 'e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
write(OUT / 'author.process.status.json', seal({'schema_version': 1, 'artifact_kind': 'actual-native-foreground-process-receipt', 'script': pin(OUT / 'author_source_review.py'), 'actual_native_exec_chunk': 'f110b6', 'actual_exit_code': 0, 'compiler_started': False, 'authority': 'Returned native tools.exec_command result; no detached process.'}))
write(OUT / 'schema.validator.preflight.status.json', seal({'schema_version': 1, 'actual_native_exec_chunk': '6b5c7d', 'actual_exit_code': 1, 'diagnosis': 'Optional third-party jsonschema is absent. No installation and no claim of third-party schema validation. Native recursive validator below checks every keyword actually present in the emitted schema (type, required, properties, additionalProperties, $schema) and rejects unsupported keywords.', 'source_or_mathematical_blocker': False}))
preceding = [pin(p) for p in files()]
for receipt in preceding:
    check_pin(receipt)
write(OUT / 'manifest.json', seal({'schema_version': 1, 'artifact_kind': 'source-review-prerun-exact-output-manifest', 'reviewer': '/root/next_primary56', 'artifacts': preceding, 'count': len(preceding), 'exclusions': ['manifest.json itself and outputs authored later; final output.readbacks.json and root CLOSED lease close this DAG without a recursive hash.'], 'hash_recipe': RECIPE}))
run = seal({'schema_version': 1, 'native_schema': 'astis-independent-source-review-run-v1', 'run_id': 'pbps-marginal-poincare57-source-review57', 'trusted_actor': '/root/next_primary56', 'role': 'independent-own-primary-first-source-review', 'independent_from_formalizer': True, 'independent_from_decoder': True, 'reviewer_packet_sha256': packet['packet_sha256'], 'publication_binding_sha256': binding['named_payload_sha256'], 'actual_packet': pin(BASE / 'source.0.reviewer-packet.json'), 'actual_primary_contract': pin(ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary.contract.json'), 'actual_primary_closed_lease': pin(ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/lease.json'), 'input_manifest': pin(OUT / 'input.manifest.json'), 'actual_readback_input_count': 614, 'math_freeze602_current_unchanged': True, 'source_review': pin(OUT / 'source.review.json'), 'standard_result_template': pin(OUT / 'semantic.result.template.json'), 'preceding_output_manifest': pin(OUT / 'manifest.json'), 'process_records': [pin(OUT / 'verification.process.status.json'), pin(OUT / 'author.process.status.json')], 'semantic_slots_count': 7, 'nonblocking_source_deltas': 3, 'repairs_count': 0, 'verdict': 'equivalent-after-elaboration', 'decoder_source_text_blind': True, 'decoder_identity_blind': False, 'strict_final_proof_body_blindness': False, 'whole_math_verdict_read': False, 'compiler_started': False, 'compiler_resource_status': 'NOT_STARTED_CLOSED', 'chronology': 'Own source-only primary/precision/blueprint, independently sealed1244 statement, original606region topology negatives and distinct accepted7node7edge consumer overlay all precede actual57 candidate body. Final main/Test body exposed; no blinded rerun manufactured.', 'temporal_open_decoder_receipt': 'Explicit native initial_lease_snapshot/initial_lease_artifact/preservation maps to preserved exact OPEN739raw/712LF bytes; final live CLOSED path distinct. Initial mistaken current-path check and failed script retained. No locator or mathematical repair.', 'hash_recipe': RECIPE, 'hash_field': 'run_sha256', 'nonrecursive_recipe': 'Run hashes complete native object minus ONLY run_sha256; pins preceding template/report/manifest. Later standard result0 binds this run digest; run deliberately does not pin later result0.'}, 'run_sha256')
write(OUT / 'reviewer.source.run.json', run)
check_self(load(OUT / 'reviewer.source.run.json'), 'run_sha256')
standard = load(OUT / 'semantic.result.template.json')['standard_result_without_run_binding']
assert standard['review_run_sha256'] == ''
standard['review_run_sha256'] = run['run_sha256']
assert set(standard) == set(packet['output_contract'])
assert list(standard['semantic_slots']) == packet['review_contract']['semantic_slots']
assert standard['verdict'] in packet['review_contract']['verdicts']
assert all(v['relation'] in packet['review_contract']['slot_relations'] and all(v[k] for k in ['original','reconstructed','evidence']) for v in standard['semantic_slots'].values())
assert standard['reviewer'] == '/root/next_primary56' and standard['independent_from_formalizer'] and standard['independent_from_decoder']
def validate_native(value, schema, pointer=''):
    assert set(schema) <= {'$schema', 'type', 'required', 'properties', 'additionalProperties'}, (pointer, 'Unsupported schema keyword')
    expected = schema.get('type')
    types = {'object': dict, 'array': list, 'string': str, 'boolean': bool}
    if expected:
        assert type(value) is types[expected], (pointer, expected)
    if expected == 'object':
        assert set(schema.get('required', [])) <= set(value), (pointer, 'required')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            assert set(value) <= set(props), (pointer, 'additionalProperties')
        for key, child in props.items():
            if key in value:
                validate_native(value[key], child, pointer + '/' + key)
validate_native(standard, load(OUT / 'result.schema.json'))
write(OUT / 'result0.json', standard)
write(OUT / 'complete.json', seal({'schema_version': 1, 'artifact_kind': 'native-independent-scoped-source-review-complete', 'trusted_actor': '/root/next_primary56', 'source_fidelity_verdict': standard['verdict'], 'standard_semantic_slot_count': 7, 'deltas_count': 3, 'repairs_count': 0, 'reviewer_packet_sha256': packet['packet_sha256'], 'publication_binding_sha256': binding['named_payload_sha256'], 'native_run': pin(OUT / 'reviewer.source.run.json'), 'native_run_complete_minus_run_sha256': run['run_sha256'], 'standard_result': pin(OUT / 'result0.json'), 'result_schema': pin(OUT / 'result.schema.json'), 'input_manifest': pin(OUT / 'input.manifest.json'), 'preceding_output_manifest': pin(OUT / 'manifest.json'), 'actual_schema_validation': 'Native recursive validator checks every present schema keyword: type, required, properties, additionalProperties; unsupported keywords rejected. Actual standard10keys and7slots validated, native packet relation/verdict enums separately checked. Third-party jsonschema absent as preserved6b5c7d EXIT1 preflight; no external validation claim.', 'compiler': 'NOT_STARTED_CLOSED', 'whole_math_verdict_read': False, 'resource_closure_pending': 'Root original OPEN source.review.lease.json will be written CLOSED LAST by distinct readonly-after-lastwrite foreground closer after this actual EXIT0 is observed.', 'hash_recipe': RECIPE}))
outputs = [pin(p) for p in files()]
for receipt in outputs:
    check_pin(receipt)
write(OUT / 'output.readbacks.json', seal({'schema_version': 1, 'artifact_kind': 'actual-source-review-output-readbacks', 'reviewer': '/root/next_primary56', 'artifacts': outputs, 'count': len(outputs), 'all_match': True, 'self_exclusion': 'This readback object pins all preceding own outputs. Its own exact readback is included in final CLOSED root resource lease, never recursively in itself.', 'hash_recipe': RECIPE}))
check_self(load(OUT / 'output.readbacks.json'))
print(json.dumps({'status': 'SOURCE_REVIEW_SEALED_PENDING_ROOT_LEASE_LAST', 'pid': os.getpid(), 'inputs': 614, 'mathfreeze': 602, 'output_readbacks': len(outputs), 'result': pin(OUT / 'result0.json'), 'run': pin(OUT / 'reviewer.source.run.json'), 'native_run_sha256': run['run_sha256'], 'complete': pin(OUT / 'complete.json'), 'compiler': 'NOT_STARTED_CLOSED', 'whole_math_verdict_read': False}, ensure_ascii=False))
