import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,base64
O=pathlib.Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
J=lambda n:json.loads((O/n).read_bytes())
lease=J('lease.final.json');manifest=J('owned-manifest.json');run=J('source.0.review-run.json')
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write']=='lease.final.json'
assert H((O/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256']
assert H(C(manifest['files']))==manifest['entries_canonical_sha256']==lease['entries_canonical_sha256']
assert H(C({k:v for k,v in run.items() if k!='run_sha256'}))==lease['whole_logical_run_sha256']==run['run_sha256']
assert len(manifest['files'])==manifest['file_count'] and len(lease['bindings'])==lease['bound_layer_count']
assert len([p for p in O.rglob('*') if p.is_file()])==lease['owned_count']==manifest['owned_count_including_manifest_and_final_lease']
for f in lease['bindings']:
 b=(O/f['path']).read_bytes();assert len(b)==f['RAW_bytes'] and H(b)==f['RAW_sha256']
 assert H(b.replace(b'\r\n',b'\n'))==f['LF_sha256']
assert (O/'lease.final.json').stat().st_mtime_ns>=max((O/f['path']).stat().st_mtime_ns for f in lease['bindings'])
for q in J('complete-exact-input-manifest.json')['inputs']:
 assert (O/q['LF_snapshot']).read_bytes()==(O/q['snapshot']).read_bytes().replace(b'\r\n',b'\n')
 if q['assert_original_still_current_at_finalization']:assert pathlib.Path(q['original_path']).read_bytes()==(O/q['snapshot']).read_bytes()
print(json.dumps({'actual_pid':os.getpid(),'read_only':True,'EXIT_if_completed':0,'owned_count':lease['owned_count'],'manifest_regular_files':manifest['file_count'],'bound_layers':lease['bound_layer_count'],'exact_inputs':74,'last_write_verified':True,'all_RAW_LF_hashes_valid':True,'whole_logical_run_sha256':run['run_sha256'],'lease_RAW_sha256':H((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':H((O/'owned-manifest.json').read_bytes()),'named_payload_RAW_sha256':H((O/'complete-named-review-decision-input-payload.json').read_bytes())},ensure_ascii=False))
