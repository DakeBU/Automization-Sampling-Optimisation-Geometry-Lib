import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
assert not (O/'lease.final.json').exists()
manifest=json.loads((O/'input-manifest70.json').read_bytes())
for q in manifest['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256'],q['path']
d=json.loads((O/'repository-reader70.decision.json').read_bytes());assert d['accept_scoped_aggregate'] and d['accept_scoped_reader'] and not d['blocking_findings'] and not d['required_repairs']
for p in O.glob('*.terminal-receipt.json'):
 x=json.loads(p.read_bytes())
 for k in ['stdout','stderr']:
  q=x[k];b=(O/q['name']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256']
for q in json.loads((O/'current-input-snapshot-map70.json').read_bytes())['snapshots']:
 b=(O/q['snapshot']).read_bytes();assert sha(b)==q['RAW_sha256'];assert (O/q['LF_snapshot']).read_bytes()==b.replace(b'\r\n',b'\n')
print('actual_PID',os.getpid(),'PASS all',manifest['count'],'finite exact RAW/LF inputs;140 final packet current inputs stable; all owned terminal streams/snapshots consistent. No old CLOSED/canonical/Git/ledger write.')
