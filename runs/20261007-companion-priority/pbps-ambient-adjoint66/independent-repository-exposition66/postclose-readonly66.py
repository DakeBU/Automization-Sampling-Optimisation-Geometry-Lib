import os,pathlib,json,hashlib
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
lease=json.loads((O/'lease.final.json').read_bytes());entries=lease['all_owned_except_this_final_lease']
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_permitted']
assert sha((O/'owned-manifest.json').read_bytes())==lease['owned_manifest']['RAW_sha256']
names={z['name'] for z in entries}|{'lease.final.json'};actual={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()};assert names==actual
last=(O/'lease.final.json').stat().st_mtime_ns
for z in entries:
 p=O/z['name'];b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'];assert p.stat().st_mtime_ns<=last
run=json.loads((O/'review-run.json').read_bytes());h=run.pop('run_sha256');assert sha(json.dumps(run,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==h==lease['whole_logical_run_sha256']
print(json.dumps({'schema':'repo66-external-readonly-postclose-observation-v1','actual_foreground_PID':os.getpid(),'status':'PASS','owned_file_count':len(actual),'zero_postclose_owned_writes':True,'lease_RAW_sha256':sha((O/'lease.final.json').read_bytes()),'whole_logical_run_sha256':h,'manifest_RAW_sha256':sha((O/'owned-manifest.json').read_bytes()),'full_Exposition':False,'PURIFIED':False,'current_graph_freshness_admission':False}))
