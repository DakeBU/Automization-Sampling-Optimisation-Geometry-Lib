"""Read-only terminal probe. Never store its output in the closed tree."""
import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
lease=json.loads((out/'lease.final.json').read_text(encoding='utf-8'))
manifest=json.loads((out/'manifest.final.json').read_text(encoding='utf-8'))
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['postclose_writes_permitted']
assert sha((out/'manifest.final.json').read_bytes())==lease['manifest_RAW_sha256']
entries=manifest['entries']
assert sha(canonical(entries))==lease['finite_owned_closure_sha256']
seen=set()
for e in entries:
    p=out/e['name'];b=p.read_bytes();seen.add(p)
    assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'],e['name']
    if e['LF_sha256'] is not None:
        lf=b.replace(b'\r\n',b'\n')
        assert len(lf)==e['LF_bytes'] and sha(lf)==e['LF_sha256'],e['name']
actual={p for p in out.rglob('*') if p.is_file()}
assert actual==seen|{out/'manifest.final.json',out/'lease.final.json'}
assert len(actual)==lease['owned_file_count'] and len(entries)==lease['regular_file_count']
run=json.loads((out/'review-run.json').read_text(encoding='utf-8'));run_sha=run.pop('run_sha256')
assert sha(canonical(run))==run_sha==lease['whole_logical_run_sha256']
for key in ['COMPLETE_RAW_REVIEW','COMPLETE_NAMED_DECISION','COMPLETE_NAMED_REVIEW_DECISION_INPUT','SEPARATE_COMPLETE_RAW_LF_INPUT']:
    e=lease[key];b=(out/e['name']).read_bytes();assert sha(b)==e['RAW_sha256']
print(json.dumps(dict(schema='repository-reader69-readonly-postclose-v1',actual_pid=os.getpid(),
    all_native_bytes_verified=True,owned_files=len(actual),regular_files=len(entries),
    finite_owned_closure_sha256=lease['finite_owned_closure_sha256'],
    manifest_RAW_sha256=lease['manifest_RAW_sha256'],lease_RAW_sha256=sha((out/'lease.final.json').read_bytes()),
    whole_logical_run_sha256=run_sha,postclose_writes=0),sort_keys=True))
