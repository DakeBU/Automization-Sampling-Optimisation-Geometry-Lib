from pathlib import Path
import json, hashlib, subprocess, runpy, sys, dataclasses

root = Path.cwd()
r = root / 'runs/20261007-companion-priority/pbps-macroscopic-centered-range58'
load = lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode()
def write(p, x):
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
checks = []
seen = set()
def pin(x):
    key = (x['path'], x['raw_sha256'], x.get('lf_sha256'))
    if key in seen: return
    seen.add(key)
    b = Path(x['path']).read_bytes()
    assert sha(b) == x['raw_sha256'], x['path']
    if 'bytes' in x: assert len(b) == x['bytes'], x['path']
    if 'raw_bytes' in x: assert len(b) == x['raw_bytes'], x['path']
    lf = b.replace(b'\r\n', b'\n')
    if 'lf_sha256' in x: assert sha(lf) == x['lf_sha256'], x['path']
    if 'lf_bytes' in x: assert len(lf) == x['lf_bytes'], x['path']
    checks.append(x)
def walk(x):
    if isinstance(x, dict):
        if 'path' in x and 'raw_sha256' in x: pin(x)
        for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
def self_hash(x, key):
    assert sha(canonical({k:v for k,v in x.items() if k != key})) == x[key], key
science = '8c8847715c1d4c3033224b069d8dd694f2a4bd30'
integration = 'a7cafde7957a8562bcd697d89c56b14768914c66'
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == integration
verified = runpy.run_path(str(root/'.astis/pbps-marginal-gradient51/require-verification58.py'))['require_verified']()
assert verified['verified_commit'] == science
repo = r/'repository-seal58'
rr, rl, rc = [load(repo/f) for f in ['run.json','lease.json','receipt.json']]
assert rl['status'] == 'CLOSED' and rl['actual_worker_exit_code'] == 0
assert rc['actual_review_worker_exit_code'] == 0 and rc['source_math_repairs'] == 0
assert rc['checked_science_commit'] == science and rc['checked_integration_commit'] == integration
for x,k in [(rr,'run_sha256'),(rl,'lease_sha256'),(rc,'receipt_sha256')]: self_hash(x,k)
assert sha(canonical(rr['repository_binding_payload'])) == rr['repository_binding_payload_sha256'] == rc['repository_binding_payload_sha256']
for f in ['run.json','lease.json','receipt.json','inputs.json','input-index.json','outputs.final.json','readback.json']:
    walk(load(repo/f))
ri = load(repo/'input-index.json')
assert ri['count'] == len(ri['entries']) == len(rr['inputs']) == 3234
assert len({x['qualified_path'] for x in ri['entries']}) == 3234
expo = r/'exposition-seal58'
er, el, ec = [load(expo/f) for f in ['run.json','lease.json','exposition.seal.json']]
assert el['status'] == 'CLOSED' and el['seal_actual_exit_code'] == 0
assert el['resource']['validator_actual_exit_code'] == 0
self_hash(er,'run_sha256')
assert sha(canonical(er['exposition_seal_payload'])) == er['exposition_seal_payload_sha256'] == el['exposition_seal_payload_sha256']
assert ec['science_commit'] == science and ec['integration_commit'] == integration
assert ec['full_Exposition_Seal'] is False and ec['PURIFIED'] is False
assert not ec['blocking_reader_fidelity_deltas'] and ec['reader_delivery_blockers']
for f in ['run.json','lease.json','exposition.seal.json','input.manifest.json','output.manifest.json','validator.json','complete.json']:
    walk(load(expo/f))
ei = load(expo/'input.manifest.json')
assert ei['input_count'] == len(ei['inputs']) == 87
for x in ei['inputs']:
    assert x['actual_input']['raw_sha256'] == x['exactraw_snapshot']['raw_sha256']
    assert x['actual_input']['lf_sha256'] == x['crlf_to_lf_snapshot']['raw_sha256']
out = dict(status='STRICT_NATIVE_SEALS_ADOPTED_SCOPED_READER_DELIVERY_BLOCKED',science_commit=science,integration_commit=integration,
           exact_native_pin_checks=len(checks),repository_complete_run_sha256=rr['run_sha256'],repository_named_payload_sha256=rr['repository_binding_payload_sha256'],
           exposition_complete_run_sha256=er['run_sha256'],exposition_named_payload_sha256=er['exposition_seal_payload_sha256'],
           reader_delivery_blockers=ec['reader_delivery_blockers'],full_Exposition_Seal=False,PURIFIED=False,checked_pins=checks)
write(r/'root.seals58.adoption.json',out)
sys.path.insert(0,str(root/'tools'))
import astis_advance as adv
pending=load(root/'.astis/pbps-marginal-gradient51/pending-discovery-real-L2-CFC60.json')
keys={f.name for f in dataclasses.fields(adv.Discovery)}
discovery=adv.Discovery(**{k:v for k,v in pending.items() if k in keys})
discovery.validate()
adv.publish_discovery(discovery)
write(r/'post58.raw-discovery.json',dict(status='RAW_POST58_DEPENDENCY_CANDIDATE_NOT_VALIDATED_NOT_PART58_CLOSURE',discovery=discovery.as_event(),
   scope='Post58 downstream operator-root adapter observation. Historical58 conceptual audit and accepted mathematics unchanged. No graph admission/formal edge/certificate.',
   reader_delivery_blockers=ec['reader_delivery_blockers']))
print('58 seals adopted',len(checks),'unique actual raw/LF pins; scoped exposition accepted, full delivery blocked; raw candidate discovery published')
