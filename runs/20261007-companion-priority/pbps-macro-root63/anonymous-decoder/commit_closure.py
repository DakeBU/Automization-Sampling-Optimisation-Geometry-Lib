import hashlib
import json
import os
import sys
from pathlib import Path

BASE=Path('E:/Samplinglib/.astis/decoder-63')
OUT=BASE/'independent'
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sys.argv[1:]==['--candidate-check-exit-code','0']
raw=(OUT/'proposed-lease.closed.json').read_bytes()
lease=json.loads(raw)
assert lease['status']=='CLOSED_LAST'
for name,digest in lease['owned_artifacts'].items():
 assert sha((OUT/name).read_bytes())==digest,name
assert json.loads((OUT/'lease.json').read_bytes())['status']=='OPEN'
assert (BASE/'lease.json').read_bytes()==(OUT/'parent-lease.open.raw.json').read_bytes()
(OUT/'lease.json').write_bytes(raw)
parent={'status':'CLOSED','allowed_inputs':['packet0.json'],
 'source_text_visible':False,'source_identity_visible':False,'compiler_started':False,
 'historical_open_snapshot':str(OUT/'parent-lease.open.raw.json'),
 'historical_open_raw_sha256':sha((OUT/'parent-lease.open.raw.json').read_bytes()),
 'independent_native_lease':str(OUT/'lease.json'),
 'independent_native_lease_raw_sha256':sha(raw),
 'independent_native_receipt':str(OUT/'native.receipt.json'),
 'independent_native_receipt_raw_sha256':sha((OUT/'native.receipt.json').read_bytes()),
 'decoded_payload_raw_sha256':lease['decoded_payload_raw_sha256'],
 'whole_logical_run_sha256':lease['whole_logical_run_sha256'],
 'closure_pid':os.getpid(),'candidate_check_observed_exit_code':0,
 'terminal_order':['finalizer returned exit 0','foreground reader reopened stdout and receipt','read-only CLOSED candidate binding check returned exit 0','independent native lease written CLOSED_LAST','parent lease closed after independent-native closure']}
(BASE/'lease.json').write_text(json.dumps(parent,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'event':'CLOSED_LAST_COMMITTED_THEN_PARENT_CLOSED','closure_pid':os.getpid(),
 'native_lease_raw_sha256':sha(raw),'parent_closed_lease_raw_sha256':sha((BASE/'lease.json').read_bytes()),
 'native_receipt_raw_sha256':sha((OUT/'native.receipt.json').read_bytes()),
 'decoded_payload_raw_sha256':lease['decoded_payload_raw_sha256'],
 'whole_logical_run_sha256':lease['whole_logical_run_sha256']},indent=2))
