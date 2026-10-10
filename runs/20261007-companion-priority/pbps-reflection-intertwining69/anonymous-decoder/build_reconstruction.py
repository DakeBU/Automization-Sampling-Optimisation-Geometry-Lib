import hashlib
import json
import os
import pathlib
import sys

ROOT = pathlib.Path('E:/Samplinglib/.astis/decoder-69/independent')
PACKET = pathlib.Path('E:/Samplinglib/.astis/decoder-69/packet0.json')
AGENT = '/root/anonymous_decoder69'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

def dump(path, obj):
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

def lf(data):
    return data.replace(b'\r\n', b'\n')

raw = PACKET.read_bytes()
packet = json.loads(raw.decode('utf-8-sig'))
payload_root = ROOT / 'inputs'
payload_root.mkdir(exist_ok=True)
packet_raw = payload_root / 'packet0.raw.json'
packet_lf = payload_root / 'packet0.lf.json'
packet_raw.write_bytes(raw)
packet_lf.write_bytes(lf(raw))
statement = packet['lean']['statement'].encode('utf-8')
(payload_root / 'lean-statement.raw.txt').write_bytes(statement)
(payload_root / 'lean-statement.lf.txt').write_bytes(lf(statement))
# Preserve the exact lexical JSON array from the packet, not a reserialized array.
raw_text = raw.decode('utf-8-sig')
key = '"approved_definition_context"'
key_start = raw_text.index(key)
array_start = raw_text.index('[', key_start + len(key))
parsed_context, consumed = json.JSONDecoder().raw_decode(raw_text[array_start:])
assert parsed_context == packet['lean']['approved_definition_context']
context = raw_text[array_start:array_start + consumed].encode('utf-8')
(payload_root / 'approved-definition-context.raw.json').write_bytes(context)
(payload_root / 'approved-definition-context.lf.json').write_bytes(lf(context))

named_path = ROOT / 'anonymous_reconstruction_69.json'
named = json.loads(named_path.read_text(encoding='utf-8'))
slots = ['objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'scopes', 'constant_dependencies']
assert all(isinstance(named[k], str) and named[k] for k in slots)
assert named['decoder'] == AGENT and named['source_text_visible'] is False
assert sha(statement) == packet['lean']['statement_sha256']
assert packet['non_disclosure']['source_text_included'] is False
assert packet['non_disclosure']['source_identity_included'] is False
assert packet['input_artifacts'] == ['lean-statement', 'approved-definition-context']

observed = {
    'packet0': {
        'representation': 'complete original on-disk UTF-8 JSON bytes, including trailing whitespace',
        'raw_path': 'inputs/packet0.raw.json', 'lf_path': 'inputs/packet0.lf.json',
        'raw_sha256': sha(raw), 'lf_sha256': sha(lf(raw)),
        'raw_bytes': len(raw), 'lf_bytes': len(lf(raw))
    },
    'lean-statement': {
        'representation': 'decoded lean.statement string encoded as UTF-8 without added newline or BOM',
        'raw_path': 'inputs/lean-statement.raw.txt', 'lf_path': 'inputs/lean-statement.lf.txt',
        'raw_sha256': sha(statement), 'lf_sha256': sha(lf(statement)),
        'raw_bytes': len(statement), 'lf_bytes': len(lf(statement))
    },
    'approved-definition-context': {
        'representation': 'exact lexical approved_definition_context JSON array slice from original UTF-8 packet',
        'raw_path': 'inputs/approved-definition-context.raw.json',
        'lf_path': 'inputs/approved-definition-context.lf.json',
        'raw_sha256': sha(context), 'lf_sha256': sha(lf(context)),
        'raw_bytes': len(context), 'lf_bytes': len(lf(context))
    }
}
checks = {
    'schema_version': 1,
    'check_kind': 'bounded-source-blind-reconstruction-consistency',
    'statement_hash_matches_packet': True,
    'source_text_and_identity_flags_false': True,
    'seven_semantic_slots_nonempty': True,
    'context_slice_matches_packet_values': True,
    'source_web_memory_registry_compiler_reads': [],
    'external_input_paths_read': [str(PACKET).replace('\\', '/')],
    'own_output_reads_permitted': True,
    'no_source_facing_verdict_or_delta': True,
    'compiled_flag_not_used_as_mathematical_evidence': True,
    'lf_recipe': 'CRLF to LF ONLY; isolated CR, all other bytes, and trailing whitespace are retained',
    'mathematical_claim_boundary': 'independent reconstruction only; no proof, source-fidelity acceptance, or independent Lean check'
}
dump(ROOT / 'negative-checks.json', checks)

terminal = {
    'schema_version': 1,
    'receipts': [
        {
            'phase': 'initial-authorized-input-inspection',
            'tool': 'exec_command', 'chunk_id': '9630ac', 'actual_tool_exit_code': 0,
            'pid': None, 'pid_observation': 'not emitted by the initial read-only shell',
            'only_file_read': str(PACKET).replace('\\', '/'),
            'output_preservation': 'complete input output preserved by inputs/packet0.raw.json; no source input'
        },
        {
            'phase': 'artifact-generation', 'foreground_python_pid': os.getpid(),
            'parent_foreground_shell_pid': int(sys.argv[1]),
            'real_exit_code': None, 'exit_record_status': 'to be filled from outer shell after process completion'
        }
    ]
}
dump(ROOT / 'terminal-receipts.json', terminal)
dump(ROOT / 'lease.json', {
    'schema_version': 1, 'owner': AGENT, 'status': 'OPEN',
    'owned_root': str(ROOT).replace('\\', '/'),
    'scope': 'standalone source-blind reconstruction outputs only; no parent lease or packet modification',
    'closure_rule': 'the last owned write will set status CLOSED_LAST; subsequent actions read-only'
})
dump(ROOT / 'build-state.json', {
    'schema_version': 1, 'decoder': AGENT,
    'decoder_packet_sha256': packet['packet_sha256'],
    'decoder_packet_sha256_kind': 'canonical value declared in original packet; not substituted by on-disk RAW hash',
    'lean_statement_sha256': sha(statement),
    'observed_input_artifacts': observed,
    'lf_recipe': checks['lf_recipe'],
    'named_reconstruction_path': named_path.name,
    'named_reconstruction_raw_sha256': sha(named_path.read_bytes()),
    'reconstructed_text_sha256': sha(named['text'].encode('utf-8')),
    'seven_semantic_slots': slots,
    'generator_pid': os.getpid(),
    'parent_shell_pid': int(sys.argv[1])
})
print(json.dumps({'phase': 'generated', 'foreground_python_pid': os.getpid(), 'parent_shell_pid': int(sys.argv[1]), 'status': 'completed-body'}, ensure_ascii=False))
