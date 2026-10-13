import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
lb=(out/'lease.final.json').read_bytes();lease=json.loads(lb);assert lease['status']=='CLOSED_LAST' and lease['postclose_writes_permitted'] is False
mb=(out/'owned-manifest.json').read_bytes();assert sha(mb)==lease['manifest_RAW_sha256'];m=json.loads(mb)
assert len(list(out.iterdir()))==lease['owned_file_count']
assert len(m['regular_file_entries'])==lease['regular_file_count']
assert sha(canon(m['regular_file_entries']))==lease['finite_owned_closure_sha256']
for x in m['regular_file_entries']:
 b=(out/x['name']).read_bytes();assert sha(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes'] and sha(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
run=json.loads((out/'review-run.json').read_bytes());v=run.pop('run_sha256');assert sha(canon(run))==v==lease['whole_logical_run_sha256']
old=out.parent/'independent-primary69';oldlb=(old/'lease.final.json').read_bytes()
assert sha(oldlb)=='2d168d568a260f2cc18fba260a5bd7c1ac45cb41602f6a359df3d16b387aec93'
oldlease=json.loads(oldlb);oldmb=(old/'owned-manifest.json').read_bytes();assert sha(oldmb)==oldlease['manifest_RAW_sha256']
assert len(list(old.iterdir()))==82
for x in json.loads(oldmb)['regular_file_entries']:
 b=(old/x['name']).read_bytes();assert sha(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
print(json.dumps(dict(schema='header-source69-external-postclose-readonly-v1',actual_reader_pid=os.getpid(),
 actual_lease_writer_pid=lease['actual_lease_writer_pid'],no_owned_write=True,owned_file_count=lease['owned_file_count'],
 regular_entries_verified=lease['regular_file_count'],lease_RAW_sha256=sha(lb),manifest_RAW_sha256=sha(mb),
 finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],whole_logical_run_sha256=v,
 verdict=lease['verdict'],prior_CLOSED82_verified_unchanged=True,all_hashes_verified=True,no_proof_or_compilation=True),sort_keys=True))
