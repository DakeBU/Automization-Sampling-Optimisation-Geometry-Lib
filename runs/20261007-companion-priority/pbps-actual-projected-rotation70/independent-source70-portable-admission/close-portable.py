import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime
O=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('E:/Samplinglib')
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def put(n,x):assert not (O/n).exists();(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
receipt=json.loads((O/'prepare-portable.terminal-receipt.json').read_bytes());assert receipt['exit_code']==0
for q in json.loads((O/'original-native-RAW-pins.json').read_bytes())['pins']:
 p=ROOT/q['path'];assert H(p.read_bytes())==q['RAW_sha256'] and p.stat().st_mtime_ns==q['original_mtime_ns']
files=[]
for p in sorted(O.iterdir()):
 assert p.is_file();b=p.read_bytes();l=b.replace(b'\r\n',b'\n');files.append({'path':p.name,'RAW_bytes':len(b),'RAW_sha256':H(b),'LF_bytes':len(l),'LF_sha256':H(l)})
m={'schema':'portable70-complete-owned-finite-manifest-v1','file_count':len(files),'owned_count_including_manifest_and_lease':len(files)+2,'files':files,'entries_canonical_sha256':H(C(files)),'self_policy':'exclude only own manifest and future final lease','original_CLOSED319_unchanged':True}
put('owned-manifest.json',m);mb=(O/'owned-manifest.json').read_bytes()
lease={'schema':'portable70-CLOSED-LAST-v1','status':'CLOSED_LAST','owned_count':len(files)+2,'bound_layers':len(files)+1,'native_manifest_RAW_sha256':H(mb),'entries_canonical_sha256':m['entries_canonical_sha256'],'bindings':files+[{'path':'owned-manifest.json','RAW_bytes':len(mb),'RAW_sha256':H(mb),'LF_bytes':len(mb),'LF_sha256':H(mb)}],'last_owned_write':'lease.final.json','no_further_owned_writes':True,'seal_actual_python_PID':os.getpid(),'seal_EXIT_policy':'authoritative foreground terminal return must establish EXIT0 after this last write','completed_review_actual_PID':receipt['actual_pid'],'completed_review_actual_EXIT':0,'original_CLOSED319_unchanged':True,'no_new_math_source_verdict':True,'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
put('lease.final.json',lease)
print(json.dumps({'actual_pid':os.getpid(),'status':'CLOSED_LAST','owned_count':len(files)+2,'manifest_RAW_sha256':H(mb),'lease_RAW_sha256':H((O/'lease.final.json').read_bytes()),'proposed_admission_RAW_sha256':H((O/'portable-admission-fields.proposed.json').read_bytes()),'decision_RAW_sha256':H((O/'portability-only.decision.json').read_bytes())},ensure_ascii=False))
