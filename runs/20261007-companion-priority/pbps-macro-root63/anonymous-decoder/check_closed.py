import hashlib
import json
import os
import sys
from pathlib import Path

OUT=Path('E:/Samplinglib/.astis/decoder-63/independent')
sha=lambda b:hashlib.sha256(b).hexdigest()
mode=sys.argv[1]
assert mode in ['candidate','committed']
raw=(OUT/('proposed-lease.closed.json' if mode=='candidate' else 'lease.json')).read_bytes()
lease=json.loads(raw)
assert lease['status']=='CLOSED_LAST'
assert lease['allowed_inputs']==['packet0.json']
for name,digest in lease['owned_artifacts'].items():
 assert sha((OUT/name).read_bytes())==digest,name
actual={p.name for p in OUT.iterdir() if p.is_file()}
assert actual==set(lease['owned_artifacts'])|{'lease.json','proposed-lease.closed.json'},actual
if mode=='candidate':
 assert json.loads((OUT/'lease.json').read_bytes())['status']=='OPEN'
else:
 assert raw==(OUT/'proposed-lease.closed.json').read_bytes()
print(json.dumps({'event':'READ_ONLY_CLOSED_BINDING_CHECK_PASSED','mode':mode,
 'reader_pid':os.getpid(),'closed_candidate_or_lease_sha256':sha(raw),
 'owned_output_count':len(actual),'all_output_bindings_passed':True},indent=2))
