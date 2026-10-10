import hashlib,json,os,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
name='lease.json' if '--committed' in sys.argv else 'proposed-lease.closed.json'
closed=json.loads((OUT/name).read_text(encoding='utf-8'))
assert closed['status']=='CLOSED_LAST'
for n,h in closed['complete_owned_outputs'].items():assert sha((OUT/n).read_bytes())==h,(n,h)
all_files={str(p.relative_to(OUT)).replace('\\','/') for p in OUT.rglob('*') if p.is_file()}
expected=set(closed['complete_owned_outputs'])|set(closed['self_hash_exclusions'])
assert all_files==expected,(all_files-expected,expected-all_files)
assert sha((OUT/'output.manifest.json').read_bytes())==closed['output_manifest_RAW_sha256']
run=json.loads((OUT/'run.json').read_text(encoding='utf-8'))
b=json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
assert sha(b)==run['run_sha256']==closed['whole_run_sha256']
assert sha((OUT/'review.payload.json').read_bytes())==closed['named_complete_payload_RAW_sha256']
if '--committed' in sys.argv:
 assert (OUT/'lease.json').read_bytes()==(OUT/'proposed-lease.closed.json').read_bytes()
 assert (OUT/'lease.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in OUT.rglob('*') if p.is_file() and p.name!='lease.json')
print(json.dumps({'status':'ACTUAL_READ_ONLY_FOREGROUND_CLOSED_BINDING_PASS','actual_reader_pid':os.getpid(),'candidate_or_committed':name,'whole_run_sha256':closed['whole_run_sha256'],'named_complete_payload_RAW_sha256':closed['named_complete_payload_RAW_sha256'],'owned_output_count':len(expected),'all_owned_hashes_passed':True,'no_local_writes_performed':True,'last_write_verified':'--committed' in sys.argv},indent=2))
