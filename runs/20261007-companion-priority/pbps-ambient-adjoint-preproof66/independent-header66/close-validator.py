import json,os,hashlib
from pathlib import Path
O=Path(__file__).parent
assert not (O/'lease.final.json').exists()
for n in ['terminal.finalizer.observed.json','terminal.readback.observed.json']:
 x=json.loads((O/n).read_bytes());assert x['actual_exit_code']==0 and x['actual_foreground_pid']>0
c=json.loads((O/'closure-index.json').read_bytes())
for k in ['COMPLETE_RAW_DECISIONS','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_INPUT']:
 x=c[k];assert hashlib.sha256((O/x['name']).read_bytes()).hexdigest()==x['RAW_sha256']
print(json.dumps(dict(status='CLOSE_VALIDATOR_PASS',actual_pid=os.getpid(),actual_finalizer_readback_EXIT0=True),sort_keys=True))
