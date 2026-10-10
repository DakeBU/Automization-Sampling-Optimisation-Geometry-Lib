import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
lease_bytes=(out/'lease.final.json').read_bytes();lease=json.loads(lease_bytes)
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and lease['postclose_writes_permitted'] is False
mb=(out/'owned-manifest.json').read_bytes();assert sha(mb)==lease['manifest_RAW_sha256']
m=json.loads(mb);rows=m['regular_file_entries'];assert sha(canon(rows))==lease['finite_owned_closure_sha256']
files=list(out.iterdir());assert len(files)==lease['owned_file_count'] and all(p.is_file() for p in files)
assert len(rows)==lease['regular_file_count']
for x in rows:
 b=(out/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
r=json.loads((out/'review-run.json').read_bytes());v=r.pop('run_sha256');assert v==lease['whole_logical_run_sha256']==sha(canon(r))
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_NAMED_SOURCE_EXPECTATIONS','SEPARATE_COMPLETE_RAW_LF_INPUT','FINITE_SOURCE_COVERAGE']:
 x=lease[k];b=(out/x['name']).read_bytes();assert sha(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
print(json.dumps(dict(schema='primary69-external-postclose-readonly-result-v1',actual_postclose_reader_pid=os.getpid(),
 closed=True,no_owned_write=True,owned_file_count=len(files),regular_entries_verified=len(rows),
 lease_RAW_sha256=sha(lease_bytes),manifest_RAW_sha256=sha(mb),finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],
 whole_logical_run_sha256=v,source_math_count=lease['source_math_count'],all_hashes_verified=True,
 actual_lease_writer_pid=lease['actual_lease_writer_pid'],source_only=True,completion_claim=False),sort_keys=True))
