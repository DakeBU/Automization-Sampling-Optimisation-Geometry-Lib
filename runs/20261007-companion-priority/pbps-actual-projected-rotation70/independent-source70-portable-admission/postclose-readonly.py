import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os
O=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('E:/Samplinglib');H=lambda b:hashlib.sha256(b).hexdigest()
l=json.loads((O/'lease.final.json').read_bytes());assert l['status']=='CLOSED_LAST'
assert len([p for p in O.iterdir() if p.is_file()])==l['owned_count']
for q in l['bindings']:
 b=(O/q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and H(b)==q['RAW_sha256'] and H(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
for q in json.loads((O/'original-native-RAW-pins.json').read_bytes())['pins']:
 p=ROOT/q['path'];assert H(p.read_bytes())==q['RAW_sha256'] and p.stat().st_mtime_ns==q['original_mtime_ns']
assert (O/'lease.final.json').stat().st_mtime_ns>=max((O/q['path']).stat().st_mtime_ns for q in l['bindings'])
print(json.dumps({'actual_pid':os.getpid(),'read_only':True,'EXIT_if_completed':0,'owned_count':l['owned_count'],'all_hashes_valid':True,'original_CLOSED319_hashes_and_mtimes_unchanged':True,'lease_last_verified':True,'lease_RAW_sha256':H((O/'lease.final.json').read_bytes())},ensure_ascii=False))
