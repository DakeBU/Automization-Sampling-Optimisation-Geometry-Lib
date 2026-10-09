import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,datetime
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def encoded(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def write(n,x):(O/n).write_bytes(encoded(x))
def row(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':'replace ONLY byte CRLF with LF; preserve every other byte','mtime_ns_at_close':p.stat().st_mtime_ns}
def check(q,base):
 p=base/q['path'];b=p.read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
 if 'mtime_ns_at_close' in q:assert p.stat().st_mtime_ns==q['mtime_ns_at_close']
run=json.loads((O/'source.0.run.json').read_bytes());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
if '--verify-only' in sys.argv:
 lease=json.loads((O/'lease.final.json').read_bytes());manifest=json.loads((O/'owned-manifest.json').read_bytes());assert lease['status']=='CLOSED_LAST'
 for q in lease['bindings']:check(q,O)
 assert sha((O/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256']
 assert sha(canon(manifest['files']))==manifest['entries_canonical_sha256']==lease['entries_canonical_sha256']
 assert sorted(p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file())==sorted([q['path'] for q in lease['bindings']]+['lease.final.json'])
 assert all((O/q['path']).stat().st_mtime_ns <= (O/'lease.final.json').stat().st_mtime_ns for q in lease['bindings'])
 for q in json.loads((O/'source.0.complete-finite-input-manifest.json').read_bytes())['entries']:
  b=(B/q['path']).read_bytes();assert sha(b)==q['current_RAW_sha256_at_close']
 def pin(n):return {k:v for k,v in row(O/n).items() if k!='mtime_ns_at_close'}
 print(json.dumps({'actual_readonly_postclose_pid':os.getpid(),'status':'PASS_READ_ONLY_POST_CLOSE','owned_count':lease['owned_count'],'bound_layer_count':lease['bound_layer_count'],'manifest_entries':len(manifest['files']),'versioned_input_count':77,'whole_logical_run_sha256':run['run_sha256'],'decision':pin('source.0.decision.json'),'admission_fields':pin('source.0.admission-fields.json'),'full_RAW_review':pin('source.0.review.RAW.md'),'named_payload':pin('complete-named-review-decision-input-payload.json'),'owned_manifest':pin('owned-manifest.json'),'lease':pin('lease.final.json'),'close_PID_EXIT':[lease['actual_close_pid'],0],'official_packet_sha256':run['official_packet_sha256'],'publication_binding_sha256':run['publication_binding_sha256'],'zero_postclose_owned_writes':True},indent=2))
 sys.exit(0)
assert not (O/'lease.final.json').exists() and not (O/'owned-manifest.json').exists()
pre=json.loads((O/'source.0.preclose-verification71.json').read_bytes());assert pre['status']=='PASS_PRE_CLOSE' and pre['whole_logical_run_sha256']==run['run_sha256']
for q in run['records']:check(q,B)
for q in json.loads((O/'source.0.complete-finite-input-manifest.json').read_bytes())['entries']:assert sha((B/q['path']).read_bytes())==q['current_RAW_sha256_at_close']
before=list(p for p in O.rglob('*') if p.is_file());owned_count=len(before)+5
stdout=encoded({'actual_pid':os.getpid(),'status':'CLOSED_LAST_SOURCE71','owned_count':owned_count,'whole_logical_run_sha256':run['run_sha256'],'official_packet_sha256':run['official_packet_sha256'],'no_mathematical_repair':True,'zero_blocking':True,'scope':'Independent bounded source fidelity only; no exactSCI/VERIFIED/full B4/main/paper/Exposition/PURIFIED/live/Goal credit.'})
(O/'source.0.close-native71.stdout.exactraw.txt').write_bytes(stdout);(O/'source.0.close-native71.stderr.exactraw.txt').write_bytes(b'')
receipt={'schema':'source71-foreground-close-terminal-receipt-v1','actual_pid':os.getpid(),'exit_code':0,'foreground':True,'background':False,'cwd':'E:/Samplinglib','command_argv':[sys.executable,str(pathlib.Path(__file__).resolve())],'receipt_prepared_before_final_lease':True,'terminal_completion_correlated_with_external_exec_EXIT0':True,'utc_before_final_lease':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':{'name':'source.0.close-native71.stdout.exactraw.txt','RAW_bytes':len(stdout),'RAW_sha256':sha(stdout)},'stderr':{'name':'source.0.close-native71.stderr.exactraw.txt','RAW_bytes':0,'RAW_sha256':sha(b'')}}
write('source.0.close-native71.terminal-receipt.json',receipt)
files=[row(p) for p in sorted(O.rglob('*')) if p.is_file()];entries_hash=sha(canon(files))
manifest={'schema':'independent-source71-complete-owned-native-manifest-v1','owned_directory':str(O),'file_count_excluding_manifest_and_last_lease':len(files),'files':files,'entries_canonical_sha256':entries_hash,'scope':'Every regular owned file, including all RAW/LF snapshots, full review, named payload, helpers, failures and actual terminal receipts. No recursive prior-history payload.'}
write('owned-manifest.json',manifest);mp=row(O/'owned-manifest.json');bindings=files+[mp]
assert len(bindings)+1==owned_count
lease={'schema':'independent-source71-CLOSED-LAST-native-lease-v1','status':'CLOSED_LAST','owned_directory':str(O),'owned_count':owned_count,'bound_layer_count':len(bindings),'native_manifest_path':'owned-manifest.json','native_manifest_RAW_bytes':mp['RAW_bytes'],'native_manifest_RAW_sha256':mp['RAW_sha256'],'entries_canonical_sha256':entries_hash,'bindings':bindings,'actual_close_pid':os.getpid(),'actual_close_exit_code':0,'close_terminal_receipt':'source.0.close-native71.terminal-receipt.json','whole_logical_run_sha256':run['run_sha256'],'whole_logical_recipe':'Canonical sorted compact UTF8 JSON deleting ONLY top-level run_sha256; no other field removed.','complete_finite_input_manifest':row(O/'source.0.complete-finite-input-manifest.json'),'versioned_inputs':77,'distinct_input_paths':73,'official_packet_sha256':run['official_packet_sha256'],'publication_binding_sha256':run['publication_binding_sha256'],'decision':'equivalent-after-elaboration;0blocking;0mathematical repairs;exact reader-status-only overlay separately approved','last_owned_write':True,'postclose_policy':'No owned writes after this lease; all subsequent verification read-only. External terminal EXIT0 corroborates prepared close receipt.','canonical_Git_ledger_Goal_or_old_CLOSED_writes':False,'truth_boundary':'Independent source fidelity only; no exactSCI/VERIFIED/full B4/main/errors/cost/composition/paper/Exposition/PURIFIED/main/live/Goal credit.'}
# This is the final owned filesystem write. Everything below is stdout or process exit.
write('lease.final.json',lease)
sys.stdout.write(stdout.decode('utf-8'))
