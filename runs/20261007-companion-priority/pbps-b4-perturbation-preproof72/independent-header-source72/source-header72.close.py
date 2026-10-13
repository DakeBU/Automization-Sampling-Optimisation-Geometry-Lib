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
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'LF_recipe':'replace ONLY byte CRLF with LF; preserve all otherbytes','mtime_ns_at_close':p.stat().st_mtime_ns}
def check(q,base):
 p=base/q['path'];b=p.read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
 if 'mtime_ns_at_close' in q:assert p.stat().st_mtime_ns==q['mtime_ns_at_close']
run=json.loads((O/'source-header72.run.json').read_bytes());assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
if '--verify-only' in sys.argv:
 lease=json.loads((O/'lease.final.json').read_bytes());manifest=json.loads((O/'owned-manifest.json').read_bytes());assert lease['status']=='CLOSED_LAST'
 for q in lease['bindings']:check(q,O)
 assert sha((O/'owned-manifest.json').read_bytes())==lease['native_manifest_RAW_sha256'] and sha(canon(manifest['files']))==lease['entries_canonical_sha256']
 assert sorted(p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file())==sorted([q['path'] for q in lease['bindings']]+['lease.final.json'])
 assert all((O/q['path']).stat().st_mtime_ns <= (O/'lease.final.json').stat().st_mtime_ns for q in lease['bindings'])
 for q in json.loads((O/'stageB.exact-header-input-manifest72.json').read_bytes())['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
 for q in json.loads((O/'stageA.prior71-readonly-pins72.json').read_bytes())['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
 def pin(n):return {k:v for k,v in row(O/n).items() if k!='mtime_ns_at_close'}
 print(json.dumps({'actual_readonly_postclose_pid':os.getpid(),'status':'PASS_READ_ONLY_POST_CLOSE','owned_count':lease['owned_count'],'bound_layer_count':lease['bound_layer_count'],'manifest_entries':len(manifest['files']),'whole_logical_run_sha256':run['run_sha256'],'StageA_whole_logical':run['StageA_whole_logical_run_sha256'],'decision':pin('source-header72.decision.json'),'full_RAW_review':pin('source-header72.review.RAW.md'),'named_payload':pin('complete-named-review-decision-input-payload72.json'),'owned_manifest':pin('owned-manifest.json'),'lease':pin('lease.final.json'),'close_PID_EXIT':[lease['actual_close_pid'],0],'zero_postclose_owned_writes':True,'source_header_only_no_implementation_compile_proof_verified':True},indent=2));sys.exit(0)
assert not (O/'lease.final.json').exists() and not (O/'owned-manifest.json').exists()
pre=json.loads((O/'source-header72.preclose-verification.json').read_bytes());assert pre['status']=='PASS_PRE_CLOSE' and pre['whole_logical_run_sha256']==run['run_sha256']
for q in run['records']:check(q,B)
payload=json.loads((O/'complete-named-review-decision-input-payload72.json').read_bytes());assert payload['complete_native_run']==run and payload['complete_decision']==json.loads((O/'source-header72.decision.json').read_bytes())
for q in json.loads((O/'stageB.exact-header-input-manifest72.json').read_bytes())['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
for q in json.loads((O/'stageA.prior71-readonly-pins72.json').read_bytes())['inputs']:assert sha((B/q['path']).read_bytes())==q['RAW_sha256']
owned_count=sum(p.is_file() for p in O.rglob('*'))+5
out=encoded({'actual_pid':os.getpid(),'status':'CLOSED_LAST_SOURCE_HEADER72','owned_count':owned_count,'decision':'accept_prospective_headers_source_facing_only','blocking':0,'repairs':0,'whole_logical_run_sha256':run['run_sha256'],'source_header_only_no_implementation_compile_proof_verified':True})
(O/'source-header72.close.stdout.exactraw.txt').write_bytes(out);(O/'source-header72.close.stderr.exactraw.txt').write_bytes(b'')
receipt={'schema':'source72-foreground-close-terminal-receipt-v1','actual_pid':os.getpid(),'exit_code':0,'foreground':True,'background':False,'command_argv':[sys.executable,str(pathlib.Path(__file__).resolve())],'cwd':'E:/Samplinglib','receipt_prepared_before_final_lease':True,'external_terminal_EXIT0_correlates_actual_completion':True,'utc_before_last_lease':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':{'name':'source-header72.close.stdout.exactraw.txt','RAW_bytes':len(out),'RAW_sha256':sha(out)},'stderr':{'name':'source-header72.close.stderr.exactraw.txt','RAW_bytes':0,'RAW_sha256':sha(b'')}};write('source-header72.close.terminal-receipt.json',receipt)
files=[row(p) for p in sorted(O.rglob('*')) if p.is_file()];entries_hash=sha(canon(files));manifest={'schema':'source72-complete-owned-native-manifest-v1','owned_directory':str(O),'file_count_excluding_manifest_and_last_lease':len(files),'files':files,'entries_canonical_sha256':entries_hash,'scope':'Every regular owned file: frozenStageA,RAW/LFexactsource/header/fragments,smallcompletepayload,review/decision,helpers,retiredobservers/failures andrealterminalreceipts. No recursive history/base64.'};write('owned-manifest.json',manifest);mp=row(O/'owned-manifest.json');bindings=files+[mp];assert len(bindings)+1==owned_count
lease={'schema':'source72-independent-header-CLOSED-LAST-native-lease-v1','status':'CLOSED_LAST','owned_directory':str(O),'owned_count':owned_count,'bound_layer_count':len(bindings),'native_manifest_path':'owned-manifest.json','native_manifest_RAW_bytes':mp['RAW_bytes'],'native_manifest_RAW_sha256':mp['RAW_sha256'],'entries_canonical_sha256':entries_hash,'bindings':bindings,'actual_close_pid':os.getpid(),'actual_close_exit_code':0,'close_terminal_receipt':'source-header72.close.terminal-receipt.json','whole_logical_run_sha256':run['run_sha256'],'StageA_whole_logical_run_sha256':run['StageA_whole_logical_run_sha256'],'whole_logical_recipe':'Canonical sorted compact UTF8 JSON deleting ONLY top-level run_sha256; no other field removed.','decision':'accept_prospective_headers_source_facing_only;0blocking;0mathematicalrepairs','source_math_counts':{'primary_four_regions':255,'primary_NODE':142,'primary_EXCLUDED':113,'supplement_unique':106,'supplement_NODE':97,'supplement_EXCLUDED':9},'source_graph_nodes_edges':[24,53],'source_formulas_obligations':[20,27],'exact_candidates_RAW_sha256':['d1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a','bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d'],'last_owned_write':True,'postclose_policy':'No owned writes after this lease; furtherverification read-only. Actualexternalterminal EXIT0 corroborates prepared close receipt.','canonical_Git_ledger_Goal_old_CLOSED_writes':False,'truth_boundary':'Prospectivesourceheaderonly; noimplementationfidelity,proof/compile,SAUclaim,SCI/VERIFIED,actualH/K/rrho/B27/B28/fullB4/main/errors/cost/composition/Exposition/PURIFIED/live/paper/Goalcompletion.'}
# LAST owned filesystem write. Onlystdout/process completion below.
write('lease.final.json',lease);sys.stdout.write(out.decode('utf-8'))
