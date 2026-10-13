from pathlib import Path
import hashlib,json,os,sys
sys.dont_write_bytecode=True
ROOT=Path('E:/Samplinglib');OUT=ROOT/'runs/20261007-companion-priority/pbps-recursive-path-preread76'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(o):return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def verify(p):
 b=(ROOT/p['path']).read_bytes();l=b.replace(b'\r\n',b'\n');assert len(b)==p['RAW_bytes'] and sha(b)==p['RAW_sha256'];assert len(l)==p['LF_bytes'] and sha(l)==p['LF_sha256']
lease=json.loads((OUT/'lease.final.json').read_bytes());assert lease['state']=='CLOSED_LAST'
files={p.relative_to(ROOT).as_posix():p for p in OUT.rglob('*') if p.is_file()}
expected={p['path'] for p in lease['all_owned_except_only_self']};assert set(files)==expected|{(OUT/'lease.final.json').relative_to(ROOT).as_posix()}
for p in lease['all_owned_except_only_self']:verify(p)
manifest=json.loads((OUT/'native.manifest.json').read_bytes());assert len(manifest['members'])==manifest['member_count']
for p in manifest['members']:verify(p)
inputs=json.loads((OUT/'inputs.manifest.json').read_bytes());pins=[inputs['primary'],inputs['primary_parser']]+inputs['source_slices']+inputs['API_fragments']+inputs['API_whole_sources_opaque_pins']+inputs['reused_native_finite_pins']
for p in pins:verify(p)
run=json.loads((OUT/'run.json').read_bytes());logical=dict(run);del logical['run_sha256'];assert sha(canon(logical))==run['run_sha256']==lease['run_whole_logical_sha256']
payload=json.loads((OUT/'complete-named-review-decision-input.payload.json').read_bytes());assert len(payload['names'])==10
for p in payload['names']:verify(p);assert p['RAW_utf8'].encode()==(ROOT/p['path']).read_bytes()
last=(OUT/'lease.final.json').stat().st_mtime_ns;assert all(p.stat().st_mtime_ns<=last for p in files.values())
print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'postclose_mode':'READ_ONLY_NO_OWNED_WRITES','all_owned_count':len(files),'lease_members':len(expected),'manifest_members':manifest['member_count'],'finite_input_entries_verified':len(pins),'named_complete_entries':len(payload['names']),'run_whole_logical_sha256':run['run_sha256'],'payload_RAW_sha256':sha((OUT/'complete-named-review-decision-input.payload.json').read_bytes()),'lease_RAW_sha256':sha((OUT/'lease.final.json').read_bytes()),'lease_last_owned_write_check':'PASS','all_RAW_LF_checks':'PASS'}))
