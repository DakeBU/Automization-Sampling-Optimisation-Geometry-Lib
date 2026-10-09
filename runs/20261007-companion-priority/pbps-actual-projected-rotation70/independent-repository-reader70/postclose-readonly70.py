import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
lb=(O/'lease.final.json').read_bytes();l=json.loads(lb);assert l['status']=='CLOSED_LAST' and l['no_further_owned_writes'];mb=(O/'owned-manifest.json').read_bytes();assert sha(mb)==l['manifest']['RAW_sha256'];m=json.loads(mb);assert sha(canon(m['entries']))==m['entries_canonical_sha256']
files={str(p.relative_to(O)).replace('\\','/') for p in O.rglob('*') if p.is_file()};assert files=={q['path'] for q in m['entries']}|{'owned-manifest.json','lease.final.json'};assert len(files)==l['owned_count']
for q in m['entries']:
 p=O/q['path'];b=p.read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and len(b.replace(b'\r\n',b'\n'))==q['LF_bytes'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256'];assert p.stat().st_mtime_ns==q['mtime_ns_at_close']
assert (O/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in O.rglob('*') if p.is_file() and p.name!='lease.final.json')
run=json.loads((O/'review.run.json').read_bytes());rh=run.pop('run_sha256');assert sha(canon(run))==rh==l['whole_logical_run_sha256']
inp=json.loads((O/'input-manifest70.json').read_bytes())
for q in inp['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
assert sha(lb)==sha((O/'lease.final.json').read_bytes())
print(json.dumps({'read_only_postclose_actual_PID':os.getpid(),'PASS':True,'owned_count':len(files),'finite_inputs':len(inp['inputs']),'final_packet_current_inputs':140,'last_owned_write':'lease.final.json','zero_owned_changes_after_close':True,'whole_logical_run_sha256':rh,'decision_RAW_sha256':l['decision_RAW_sha256'],'manifest_RAW_sha256':sha(mb),'named_payload':l['complete_named_payload'],'lease_RAW_sha256':sha(lb)},ensure_ascii=False))
