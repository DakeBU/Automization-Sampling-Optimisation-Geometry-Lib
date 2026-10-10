from pathlib import Path
import hashlib,json,os,sys,subprocess,datetime
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'lf_bytes':len(lf),'raw_sha256':sha(b),'lf_sha256':sha(lf)}
def put(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==v
assert not (O/'lease.json').exists()
put('negative-evidence.json',{'inspection_console':{'tool':'0cc5c4','actual_exit_code':1,'error':'gbk UnicodeEncodeError printing Unicode JSON; ASCII readback corrected EXIT0'},'first_review_parser':{'tool':'b06cff','actual_exit_code':1,'error':'FULL_PROP_MISMATCH caused by parser strip removing initial binder indentation','failed_script':pin(O/'review_exact.failed0.snapshot.py'),'correction':'Use rstrip; complete Prop check and whole independent reviewer then EXIT0','successful_author_tool':'c938cd','successful_author_pid':31704,'actual_author_exit_code':0},'mathematical_or_source_repair':False})
env=dict(os.environ);env['PYTHONUTF8']='1'
p=subprocess.run([sys.executable,str(O/'readback.py')],cwd=R,env=env,capture_output=True,encoding='utf8');assert p.returncode==0,(p.stdout,p.stderr)
readback=json.loads(p.stdout)
put('foreground-readback.receipt.json',{'actual_command':[sys.executable,str(O/'readback.py')],'actual_exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'stdout_sha256':sha(p.stdout.encode()),'result':readback,'completed_at':now(),'finalizer_foreground_pid':os.getpid()})
payload=json.loads((O/'named-kernel-overlay-source.payload.json').read_bytes());assert sha(canon(payload))==readback['named_kernel_overlay_source_payload_sha256']
reviewpin=pin(O/'source-overlay-review.json')
run={'schema_version':1,'actor':'/root/next_primary59','status':'EXACT_KERNEL_SYNTAX_OVERLAY_SOURCE_ACCEPTED_CLOSED','completed_at':now(),'named_kernel_overlay_source_payload':payload,'named_kernel_overlay_source_payload_sha256':sha(canon(payload)),'output_files_before_run':[pin(x) for x in sorted(O.rglob('*')) if x.is_file()],'actual_foreground_evidence':{'author_python_pid':31704,'author_tool':'c938cd','author_exit_code':0,'readback_python_pid':readback['actual_readback_pid'],'readback_exit_code':p.returncode,'finalizer_python_pid':os.getpid()},'bounded_counts':{'qualified_input_snapshots':33,'headers':2,'H0_expansions':25,'complete_named_rfl_equalities':2,'creator_compiler_records':8,'reviewer_compilers':0,'EXCESS':0},'source_or_theorem_assumption_changes':0,'source_graph_coverage_changes':0,'proof_completion_admitted':False,'production_old_audits_creator_unchanged':True,'run_hash_recipe':'canonical UTF8 JSON sort_keys ensure_ascii=False separators comma colon; entire run excluding ONLY top-level run_sha256','closure_order':'All actual foreground readbacks EXIT0 and run/payload exact native hash reads precede CLOSEDLAST lease; lease is final filesystem operation.'}
run['run_sha256']=sha(canon(run));put('run.json',run)
rb=json.loads((O/'run.json').read_bytes());h=rb.pop('run_sha256');assert h==sha(canon(rb));assert rb['named_kernel_overlay_source_payload_sha256']==sha(canon(rb['named_kernel_overlay_source_payload']))
runpin=pin(O/'run.json')
output={'status':'CLOSEDLAST','verdict':'ACCEPT_EXACT_V2_TO_V3_KERNEL_SYNTAX_OVERLAY','review_raw_sha256':reviewpin['raw_sha256'],'run_sha256':h,'named_kernel_overlay_source_payload_sha256':run['named_kernel_overlay_source_payload_sha256'],'readback_actual_exit_code':0,'readback_pid':readback['actual_readback_pid'],'finalizer_pid':os.getpid(),'EXCESS':0,'new_compilers':0}
closed={'schema_version':1,'actor':'/root/next_primary59','status':'CLOSEDLAST','closed_at':now(),'actual_foreground_author_exit_code':0,'actual_foreground_readback_exit_code':0,'actual_foreground_readback_pid':readback['actual_readback_pid'],'actual_finalizer_pid':os.getpid(),'native_run':runpin,'run_sha256':h,'named_kernel_overlay_source_payload_sha256':run['named_kernel_overlay_source_payload_sha256'],'review':reviewpin,'scope':'Independent exact v2 to v3 syntax/source equality acceptance only; no theorem proof completion, Gamma, publication or whole Goal credit.','compiler_by_reviewer':'NOT_STARTED_CLOSED','last_filesystem_operation':'This CLOSEDLAST lease write'}
assert not (O/'lease.json').exists()
# Deliberately no filesystem reads/writes after this final write.
(O/'lease.json').write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(output))
