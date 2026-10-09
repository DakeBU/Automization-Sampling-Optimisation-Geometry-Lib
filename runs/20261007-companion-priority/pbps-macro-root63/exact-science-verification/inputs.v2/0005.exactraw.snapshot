import hashlib
import json
import os
import sys
from pathlib import Path

OUT=Path('E:/Samplinglib/.astis/decoder-63/independent')
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sys.argv[1:]==['--finalizer-exit-code','0']
stdout=(OUT/'finalizer.stdout.txt').read_bytes()
receipt_raw=(OUT/'native.receipt.json').read_bytes()
receipt=json.loads(receipt_raw)
run=json.loads((OUT/'native.run.json').read_bytes())
for name,digest in receipt['owned_artifacts'].items():
 assert sha((OUT/name).read_bytes())==digest,name
without_hash={k:v for k,v in run.items() if k!='run_sha256'}
logical=sha(json.dumps(without_hash,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
assert logical==run['run_sha256']==receipt['whole_logical_run_sha256']
assert 'FINALIZER_COMPLETED' in stdout.decode('utf-8')
readback={'event':'FOREGROUND_READER_REOPENED_FINALIZER_STDOUT_AND_RECEIPT',
 'reader_pid':os.getpid(),'finalizer_pid':receipt['finalizer_pid'],'observed_finalizer_exit_code':0,
 'native_receipt_raw_sha256':sha(receipt_raw),'finalizer_stdout_raw_sha256':sha(stdout),
 'whole_logical_run_sha256':logical,'all_receipt_bindings_passed':True,
 'native_lease_status':json.loads((OUT/'lease.json').read_bytes())['status']}
(OUT/'terminal.readback.json').write_text(json.dumps(readback,indent=2)+'\n',encoding='utf-8')
print('REOPENED_FINALIZER_STDOUT_BEGIN\n'+stdout.decode('utf-8')+'REOPENED_FINALIZER_STDOUT_END')
print('REOPENED_RECEIPT_BINDING_RESULT\n'+json.dumps(readback,indent=2))
print('READBACK_READER_COMPLETED')
