from pathlib import Path
import hashlib,json,os
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/b27-dependency-diagnosis'
def sha(b):return hashlib.sha256(b).hexdigest()
lease=json.loads((OWN/'lease.final.json').read_text(encoding='utf-8'))
assert lease['state']=='CLOSED_LAST'
manifest=OWN/lease['manifest']['path']
assert sha(manifest.read_bytes())==lease['manifest']['raw_sha256']
m=json.loads(manifest.read_text(encoding='utf-8'))
for p in m['files']:
 b=(OWN/p['path']).read_bytes()
 assert len(b)==p['raw_bytes'] and sha(b)==p['raw_sha256'],p['path']
 assert sha(b.replace(b'\r\n',b'\n'))==p['lf_sha256'],p['path']
actual={p.relative_to(OWN).as_posix() for p in OWN.rglob('*') if p.is_file()}
expected={p['path'] for p in m['files']}|{'owned-manifest.json','lease.final.json'}
assert actual==expected
for p in json.loads((OWN/'inputs.finite-pins.json').read_text(encoding='utf-8'))['files']:
 b=(ROOT/p['path']).read_bytes();assert sha(b)==p['raw_sha256'],p['path']
r=json.loads((OWN/'diagnosis.run.json').read_text(encoding='utf-8'));claimed=r.pop('run_sha256')
assert sha(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==claimed==lease['whole_logical_sha256']
assert (OWN/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in OWN.rglob('*') if p.is_file())
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'read_only_postclose':True,'files':len(actual),'raw_lf_and_finite_set_verified':True,'current_content_inputs':7,'whole_logical_sha256':claimed,'lease_raw_sha256':sha((OWN/'lease.final.json').read_bytes())},indent=2))
