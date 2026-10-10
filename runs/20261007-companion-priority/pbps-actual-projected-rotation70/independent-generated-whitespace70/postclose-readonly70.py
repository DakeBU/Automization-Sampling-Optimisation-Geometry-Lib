import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
lb=(O/'lease.final.json').read_bytes();l=json.loads(lb);assert l['status']=='CLOSED_LAST';mb=(O/'owned-manifest.json').read_bytes();assert sha(mb)==l['manifest_RAW_sha256'];m=json.loads(mb);assert sha(canon(m['entries']))==m['entries_canonical_sha256'];assert {p.name for p in O.iterdir() if p.is_file()}=={q['path'] for q in m['entries']}|{'owned-manifest.json','lease.final.json'}
for q in m['entries']:
 p=O/q['path'];b=p.read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256'] and p.stat().st_mtime_ns==q['mtime_ns_at_close']
assert (O/'lease.final.json').stat().st_mtime_ns>=max(p.stat().st_mtime_ns for p in O.iterdir() if p.name!='lease.final.json')
r=json.loads((O/'review.run.json').read_bytes());h=r.pop('run_sha256');assert sha(canon(r))==h==l['whole_logical_run_sha256']
inp=json.loads((O/'input-manifest.json').read_bytes())
for q in inp['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
for q in inp['other137_original_packet_inputs_checked_in_place_not_duplicated']:
 b=pathlib.Path(q['path']).read_bytes();assert sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
print(json.dumps({'read_only_postclose_PID':os.getpid(),'PASS':True,'owned_count':l['owned_count'],'zero_postclose_owned_writes':True,'whole_logical_run_sha256':h,'decision_RAW_sha256':l['decision_RAW_sha256'],'manifest_RAW_sha256':sha(mb),'named_payload':l['complete_named_payload'],'lease_RAW_sha256':sha(lb)}))
