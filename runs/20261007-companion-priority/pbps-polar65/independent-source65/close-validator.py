import json,hashlib,os
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
assert not (O/'lease.final.json').exists()
for n in ['terminal.finalizer.observed.json','terminal.readback.observed.json']:
 d=json.loads((O/n).read_bytes());assert d['actual_exit_code']==0 and d['actual_foreground_pid']>0
c=json.loads((O/'closure-index.json').read_bytes())
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 d=c[k];assert H((O/d['name']).read_bytes())==d['RAW_sha256']
print(json.dumps(dict(actual_pid=os.getpid(),status='CLOSE_VALIDATION_PASS',owned_files_before_closure=len(list(O.iterdir())),finalizer_and_readback_actual_EXIT0=True),sort_keys=True))
