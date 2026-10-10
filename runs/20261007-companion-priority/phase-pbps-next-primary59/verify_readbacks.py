from pathlib import Path
import hashlib, json, sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib'); O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda n:json.loads((O/n).read_bytes())
x=read('primary.anchors.json'); b=(R/x['primary']['path']).read_bytes()
assert sha(b)==x['primary']['raw_sha256']
for a in x['anchors']:
    z=b[a['primary_start_utf8_byte']:a['primary_end_utf8_byte_exclusive']]
    assert len(z)==a['slice_bytes'] and sha(z)==a['slice_raw_sha256']
assert len(x['anchors'])==17
c=read('source.contract.json'); assert not c['admission'] and not c['compiler_started']
assert c['chronology']['candidate59_supplied'] is False
p=read('next-edge.blueprint.json'); assert len(p['steps'])==p['step_count']==7
a=read('api.inventory.json'); d=read('api.precision-addendum.json')
assert len(a['declarations'])==16 and len(d['declarations'])==3
for v in a['declarations']+d['declarations']:
    f=R/v['file']['path']; raw=f.read_bytes()
    assert sha(raw)==v['file']['raw_sha256']
    lines=raw.decode().splitlines()
    assert '\n'.join(lines[v['start_line']-1:v['end_line']])==v['exact_source_span']
for h in a['local_headers']:
    f=R/h['public_header']['path']; z=f.read_bytes()
    assert sha(z)==h['public_header']['raw_sha256'] and b':= by' not in z
assert read('capsule.bounded.json')['actual_exit_code']==0
assert read('collection.process.json')['compiler_started'] is False
assert read('lease.open.json')['compiler']=='NOT_STARTED'
assert not (O/'lease.json').exists(), 'Lease must close only after this check has exited0.'
print(json.dumps({'status':'PASS','primary_anchors':17,'public_headers':4,
 'mathlib_spans':19,'blueprint_steps':7,'compiler':'NOT_STARTED',
 'payload_json_parse_and_exact_source_readbacks':True}))
