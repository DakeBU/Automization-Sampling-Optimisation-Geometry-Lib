import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent;H=lambda b:hashlib.sha256(b).hexdigest();C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();J=lambda n:json.loads((O/n).read_bytes())
l=J('lease.final.json');m=J('owned-manifest.json');r=J('header-source71.run.json');assert l['status']=='CLOSED_LAST'
assert H((O/'owned-manifest.json').read_bytes())==l['native_manifest_RAW_sha256'] and H(C(m['files']))==l['entries_canonical_sha256']
assert len([p for p in O.iterdir() if p.is_file()])==l['owned_count']==m['owned_count_including_manifest_and_final_lease']
for x in l['bindings']:
 b=(O/x['path']).read_bytes();assert len(b)==x['RAW_bytes'] and H(b)==x['RAW_sha256'] and H(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
assert H(C({k:v for k,v in r.items() if k!='run_sha256'}))==r['run_sha256']==l['whole_logical_run_sha256']
assert (O/'lease.final.json').stat().st_mtime_ns>=max((O/x['path']).stat().st_mtime_ns for x in l['bindings'])
for x in J('complete-exact-input-manifest.json')['inputs']:
 p=pathlib.Path(x['original_path']);assert H(p.read_bytes())==x['RAW_sha256'] and p.stat().st_mtime_ns==x['original_mtime_ns']
print(json.dumps({'actual_pid':os.getpid(),'read_only':True,'EXIT_if_completed':0,'owned_count':l['owned_count'],'all_RAW_LF_hashes_and_original_input_mtimes_valid':True,'lease_last_verified':True,'whole_logical_run_sha256':r['run_sha256'],'lease_RAW_sha256':H((O/'lease.final.json').read_bytes())},ensure_ascii=False))
