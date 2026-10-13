import hashlib
import json
import os
import pathlib
import sys

ROOT = pathlib.Path('E:/Samplinglib/.astis/decoder-69/independent')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def dump(path, obj):
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

state = json.loads((ROOT / 'build-state.json').read_text(encoding='utf-8'))
named_path = ROOT / state['named_reconstruction_path']
named = json.loads(named_path.read_text(encoding='utf-8'))
receipts = json.loads((ROOT / 'terminal-receipts.json').read_text(encoding='utf-8-sig'))
assert receipts['receipts'][1]['real_exit_code'] == 0
assert sha(named_path.read_bytes()) == state['named_reconstruction_raw_sha256']

run = {
    'schema_version': 1,
    'schema_name': 'complete-independent-source-blind-review-run',
    'decoder': named['decoder'],
    'source_text_visible': False,
    'input_artifacts': named['input_artifacts'],
    'decoder_packet_sha256': state['decoder_packet_sha256'],
    'decoder_packet_sha256_kind': state['decoder_packet_sha256_kind'],
    'lean_statement_sha256': state['lean_statement_sha256'],
    'observed_input_artifacts': state['observed_input_artifacts'],
    'lf_recipe': state['lf_recipe'],
    'reconstructed_theorem_text': named['text'],
    'reconstructed_text_sha256': state['reconstructed_text_sha256'],
    'seven_semantic_slots': {key: named[key] for key in state['seven_semantic_slots']},
    'named_reconstruction': {
        'path': named_path.name,
        'raw_sha256': state['named_reconstruction_raw_sha256'],
        'canonical_logical_sha256': sha(canonical(named)),
        'hash_kinds_are_distinct': True
    },
    'execution': {
        'generation_python_pid': state['generator_pid'],
        'generation_real_exit_code': receipts['receipts'][1]['real_exit_code'],
        'foreground_shell_pid': int(sys.argv[1]),
        'finalization_python_pid': os.getpid(),
        'terminal_receipts_path': 'terminal-receipts.json',
        'terminal_receipts_raw_hash_location': 'manifest.json',
        'closure_exit_observation': 'actual child exits recorded by foreground shell before lease closure; foreground shell exit and read-only postclose tool exit observed externally'
    },
    'logical_hash_recipe': 'Delete only the top-level run_sha256 field; json.dumps(sort_keys=True, ensure_ascii=False, separators=(comma,colon)); UTF-8 without BOM; SHA256. No nested field or other content is deleted.',
    'boundary': {
        'reconstruction_only': True,
        'source_facing_verdict': None,
        'source_facing_deltas': None,
        'compiler_run': False,
        'source_identity_guessed': False,
        'source_web_memory_registry_prior_review_access': False,
        'compiled_packet_flag_used_as_evidence': False
    },
    'output_envelope': {'path': 'decoded0.json', 'raw_hash_location': 'manifest.json', 'contains_run_sha256': True}
}
run_hash = sha(canonical(run))
run['run_sha256'] = run_hash
assert run_hash != state['named_reconstruction_raw_sha256']
dump(ROOT / 'review-run.json', run)

decoded = dict(named)
decoded.update({
    'schema_name': 'complete-source-blind-decoded-output',
    'decoder_packet_sha256': state['decoder_packet_sha256'],
    'lean_statement_sha256': state['lean_statement_sha256'],
    'observed_input_artifacts': state['observed_input_artifacts'],
    'lf_recipe': state['lf_recipe'],
    'reconstructed_theorem_text': named['text'],
    'reconstructed_text_sha256': state['reconstructed_text_sha256'],
    'decoder_run_sha256': run_hash,
    'named_reconstruction_raw_sha256': state['named_reconstruction_raw_sha256'],
    'named_reconstruction_path': named_path.name,
    'review_run_path': 'review-run.json',
    'mathematical_claim_boundary': 'independent complete reconstruction only; no source-fidelity acceptance or proof claim'
})
dump(ROOT / 'decoded0.json', decoded)
print(json.dumps({'phase': 'finalized-review-payloads', 'foreground_python_pid': os.getpid(), 'parent_shell_pid': int(sys.argv[1]), 'whole_logical_sha256': run_hash, 'named_raw_sha256': state['named_reconstruction_raw_sha256']}, ensure_ascii=False))
