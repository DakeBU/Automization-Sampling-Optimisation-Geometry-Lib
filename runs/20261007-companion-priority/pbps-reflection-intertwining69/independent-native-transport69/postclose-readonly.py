import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
lease=json.loads((out/'lease.final.json').read_bytes());m=json.loads((out/'manifest.final.json').read_bytes())
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_permitted']
assert sha((out/'manifest.final.json').read_bytes())==lease['manifest_RAW_sha256']
assert sha(canonical(m['entries']))==lease['finite_owned_closure_sha256']
for e in m['entries']:
    b=(out/e['name']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
    lf=b.replace(b'\r\n',b'\n');assert len(lf)==e['LF_bytes'] and sha(lf)==e['LF_sha256']
assert {p.name for p in out.iterdir() if p.is_file()}=={e['name'] for e in m['entries']}|{'manifest.final.json','lease.final.json'}
r=json.loads((out/'review-run.json').read_bytes());h=r.pop('run_sha256');assert sha(canonical(r))==h==lease['whole_logical_run_sha256']
print(json.dumps(dict(actual_postclose_pid=os.getpid(),owned_file_count=lease['owned_file_count'],all_owned_RAW_LF_verified=True,
    postclose_writes=0,lease_RAW_sha256=sha((out/'lease.final.json').read_bytes()),whole_logical_run_sha256=h),sort_keys=True))
