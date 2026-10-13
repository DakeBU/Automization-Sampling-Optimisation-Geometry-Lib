import os
import sys
sys.dont_write_bytecode = True
from seal_common import *

assert len(sys.argv) == 3, 'Pass actual returned seal process chunk and actual pid after EXIT0.'
chunk, stage_a_pid = sys.argv[1], int(sys.argv[2])
assert chunk and stage_a_pid > 0
original_path = OUT / 'initial-source-lease.raw.snapshot.json'
lease_path = BASE / 'source.review.lease.json'
assert lease_path.read_bytes() == original_path.read_bytes()
original = load(original_path)
assert original['status'] == 'OPEN' and original['compiler_started'] is False
inputs = check_inputs()
readbacks = load(OUT / 'output.readbacks.json')
check_self(readbacks)
assert readbacks['all_match']
for receipt in readbacks['artifacts']:
    check_pin(receipt)
run = load(OUT / 'reviewer.source.run.json')
check_self(run, 'run_sha256')
complete = load(OUT / 'complete.json')
check_self(complete)
standard = load(OUT / 'result0.json')
assert standard['review_run_sha256'] == run['run_sha256']
assert standard['verdict'] == 'equivalent-after-elaboration' and len(standard['semantic_slots']) == 7 and not standard['repairs']
all_outputs = [pin(p) for p in files()]
for receipt in all_outputs:
    check_pin(receipt)
closed = dict(original)
for key in ['status', 'read_lease', 'write_lease', 'Python_lease']:
    closed[key] = 'CLOSED'
closed['compiler_lease'] = 'NOT_STARTED_CLOSED'
closed['compiler_started'] = False
closed.update({'native_schema': 'astis-independent-source-review-resource-lease-v1', 'trusted_actor': '/root/next_primary56', 'original_OPEN_exact_snapshot': pin(original_path), 'source_review_result': pin(OUT / 'result0.json'), 'reviewer_source_run': pin(OUT / 'reviewer.source.run.json'), 'reviewer_source_run_complete_minus_run_sha256': run['run_sha256'], 'publication_binding_sha256': run['publication_binding_sha256'], 'input_manifest': pin(OUT / 'input.manifest.json'), 'input_actual_readback_count': 614, 'math_freeze602_current_unchanged': True, 'output_readbacks': pin(OUT / 'output.readbacks.json'), 'actual_output_artifacts': all_outputs, 'output_actual_readback_count': len(all_outputs), 'actual_foreground_sealing_process': {'script': pin(OUT / 'seal_source_review.py'), 'native_exec_chunk': chunk, 'actual_exit_code': 0, 'actual_pid': stage_a_pid, 'returned_success_before_closure': True}, 'foreground_lease_closer': {'script': pin(OUT / 'close_source_lease.py'), 'actual_pid': os.getpid(), 'detached': False, 'last_write_rule': 'All verification and exact output readbacks completed before this final CLOSED write. Only readonly lease/self-hash/readback assertions and stdout follow. Actual tool exit is reported externally, not manufactured as a pre-exit receipt.'}, 'source_fidelity_verdict': standard['verdict'], 'strict_final_proof_body_blindness': False, 'decoder_source_text_blind': True, 'decoder_identity_blind': False, 'whole_math_verdict_read': False, 'retained_negatives': ['Original sourcegraph57 two missing prerequisite paths retained; distinct accepted consumer overlay preserved.', 'Historical56 post-CLOSED mutation/restoration and exposed provider/candidate-body chronology unchanged.', 'Original source-binding API negative retained.', 'Reviewer temporal decoder input check0ddcdc EXIT1 retained; historical OPEN snapshot explicitly resolves the time-bound receipt, corrected bf9443 EXIT0; no locator or source repair.'], 'no_automatic_admission': 'Scoped source-fidelity seal only. No VERIFIED/PURIFIED/wholepaper/Gamma/main/cost/composition admission.', 'hash_recipe': RECIPE, 'self_hash_field': 'content_self_sha256', 'final_filesystem_write': 'This root source.review.lease.json CLOSED is LAST; its own bytes excluded from own output manifest to avoid recursion.'})
closed = seal(closed)
# This is deliberately the final filesystem write of the entire review.
lease_path.write_bytes((json.dumps(closed, ensure_ascii=False, indent=2) + '\n').encode('utf8'))
actual_closed = load(lease_path)
assert actual_closed == closed
check_self(actual_closed)
assert all(actual_closed[k] == 'CLOSED' for k in ['status','read_lease','write_lease','Python_lease'])
assert actual_closed['compiler_lease'] == 'NOT_STARTED_CLOSED'
print(json.dumps({'status': 'CLOSED_LAST', 'pid': os.getpid(), 'root_lease': pin(lease_path), 'root_lease_complete_minus_content_self_sha256': closed['content_self_sha256'], 'native_run_complete_minus_run_sha256': run['run_sha256'], 'result': pin(OUT / 'result0.json'), 'inputs': 614, 'outputs': len(all_outputs), 'compiler': 'NOT_STARTED_CLOSED', 'verdict': standard['verdict'], 'whole_math_verdict_read': False}, ensure_ascii=False))
