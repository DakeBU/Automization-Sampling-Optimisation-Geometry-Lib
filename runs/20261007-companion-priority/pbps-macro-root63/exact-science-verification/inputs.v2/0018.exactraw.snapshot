import hashlib
import json
from pathlib import Path

OUT=Path('E:/Samplinglib/.astis/decoder-63/independent')
sha=lambda b:hashlib.sha256(b).hexdigest()
readback=json.loads((OUT/'terminal.readback.json').read_bytes())
assert readback['observed_finalizer_exit_code']==0
assert readback['all_receipt_bindings_passed']
bindings={p.name:sha(p.read_bytes()) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'}
closure={'status':'ALL_NATIVE_OUTPUTS_PINNED_BEFORE_CLOSED_LAST','owned_artifacts':bindings,
 'self_hash_exclusions':['closure.bindings.json','proposed-lease.closed.json','lease.json'],
 'self_hash_reason':'Closure pins all prior outputs; final lease pins closure and all prior outputs. Proposed lease and final lease must have identical bytes, excluding their own recursive hash.'}
(OUT/'closure.bindings.json').write_text(json.dumps(closure,indent=2)+'\n',encoding='utf-8')
bindings['closure.bindings.json']=sha((OUT/'closure.bindings.json').read_bytes())
receipt=json.loads((OUT/'native.receipt.json').read_bytes())
lease={'status':'CLOSED_LAST','allowed_inputs':['packet0.json'],
 'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,
 'parent_lease_open_raw_sha256':sha((OUT/'parent-lease.open.raw.json').read_bytes()),
 'statement_sha256':json.loads((OUT/'capture.json').read_bytes())['statement_raw_sha256'],
 'context_sha256':json.loads((OUT/'capture.json').read_bytes())['context_sha256'],
 'decoded_payload_raw_sha256':receipt['decoded_payload_raw_sha256'],
 'whole_logical_run_sha256':receipt['whole_logical_run_sha256'],
 'terminal_readback':readback,'owned_artifacts':bindings,
 'self_hash_exclusions':['proposed-lease.closed.json','lease.json'],
 'self_binding':'proposed-lease.closed.json and lease.json must have byte-for-byte equality after commit; this lease otherwise pins every owned output.',
 'terminal_requirement':'An actual read-only foreground CLOSED candidate binding check must finish successfully before commit_closure.py is invoked.'}
(OUT/'proposed-lease.closed.json').write_text(json.dumps(lease,indent=2)+'\n',encoding='utf-8')
print('CLOSED_CANDIDATE_PREPARED; native lease still OPEN; all outputs pinned')
