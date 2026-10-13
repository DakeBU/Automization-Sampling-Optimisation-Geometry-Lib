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
def rb(stage):
 env=dict(os.environ);env['PYTHONUTF8']='1';p=subprocess.run([sys.executable,str(O/'readback.py'),stage],cwd=R,env=env,capture_output=True,encoding='utf8');assert p.returncode==0,(p.stdout,p.stderr)
 return {'actual_command':[sys.executable,str(O/'readback.py'),stage],'actual_exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'stdout_sha256':sha(p.stdout.encode()),'result':json.loads(p.stdout),'completed_at':now()}
assert not (O/'lease.json').exists()
before=rb('pre');put('foreground-pre-readback.receipt.json',before)
payload=json.loads((O/'named-source-review.payload.json').read_bytes());ph=sha(canon(payload));assert ph==before['result']['named_source_review_payload_sha256']
run={'schema_version':1,'actor':'/root/next_primary59','status':'SCOPED_SOURCE_AND_EXPOSITION_REVIEW_SEALED','completed_at':now(),'named_source_review_payload':payload,'named_source_review_payload_sha256':ph,'output_pins_before_run':[pin(p) for p in sorted(O.rglob('*')) if p.is_file()],'actual_foreground_process_evidence':{'author_pid':51936,'author_tool':'d52645','author_actual_exit_code':0,'pre_readback_pid':before['result']['actual_readback_pid'],'pre_readback_actual_exit_code':before['actual_exit_code'],'finalizer_pid':os.getpid()},'source_order':'Frozen31-region primary read; own primary-boundary.before-packets authored; fresh packets; full current proof bodies; current authored reader/publication; exact publication binding recomputed.','decisions':{'verdicts':['equivalent-after-elaboration','equivalent-after-elaboration'],'EXCESS':0,'blocking_deltas':0,'repairs':0,'declarations':2,'canonical_slots_each':7,'reader_formula_proof_steps':10,'reviewer_compilers':0},'native_run_hash_recipe':'Canonical UTF8 JSON sort_keys ensure_ascii=False separators comma colon of ENTIRE run excluding ONLY top-level run_sha256.','review_output_rule':'Each source.i.review.json is exactly named_source_review_payload.reviews_before_native_run_binding[i] plus review_run_sha256 equal to this entire native run hash. Final exact output bytes checked by a new foreground child, then receipt/lease bind final raw/LF outputs; avoids circular self-hashing.','publication_truth_boundary':'Independent scoped source fidelity and authored exposition correspondence only; no self source-topology approval, compiler proof gate, VERIFIED, stabilization, purification/live-page/whole-paper/Gamma/Goal admission.','canonical_creator_and_prior_artifacts_untouched':True,'compiler_by_reviewer':'NOT_STARTED_CLOSED'}
run['run_sha256']=sha(canon(run));put('run.json',run);h=run['run_sha256']
for i,v in enumerate(payload['reviews_before_native_run_binding']):
 review=dict(v);review['review_run_sha256']=h;put(f'source.{i}.review.json',review)
after=rb('final');put('foreground-final-readback.receipt.json',after)
outputs=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
put('receipt.json',{'actor':'/root/next_primary59','status':'ACCEPT_SCOPED_SOURCE_AND_CURRENT_EXPOSITION','actual_author_pid':51936,'actual_author_exit_code':0,'actual_pre_readback_pid':before['result']['actual_readback_pid'],'actual_pre_readback_exit_code':0,'actual_final_readback_pid':after['result']['actual_readback_pid'],'actual_final_readback_exit_code':0,'actual_finalizer_pid':os.getpid(),'run_sha256':h,'named_source_review_payload_sha256':ph,'qualified_output_raw_LF_pins':outputs,'source_review_verdicts':['equivalent-after-elaboration','equivalent-after-elaboration'],'reviewer_compilers':0,'independent_root_adoption_required':True,'all_other_source_obligations_open':True})
reviewpins=[pin(O/f'source.{i}.review.json') for i in [0,1]]
result={'status':'CLOSEDLAST','review_run_sha256':h,'named_source_review_payload_sha256':ph,'source_review_raw_sha256':[x['raw_sha256'] for x in reviewpins],'verdicts':['equivalent-after-elaboration','equivalent-after-elaboration'],'EXCESS':0,'blocking':0,'repairs':0,'author_pid':51936,'pre_readback_pid':before['result']['actual_readback_pid'],'final_readback_pid':after['result']['actual_readback_pid'],'readback_actual_exit_codes':[0,0],'finalizer_pid':os.getpid(),'new_compilers':0}
closed={'actor':'/root/next_primary59','status':'CLOSEDLAST','closed_at':now(),'source_reviews':reviewpins,'run':pin(O/'run.json'),'run_sha256':h,'named_source_review_payload_sha256':ph,'receipt':pin(O/'receipt.json'),'actual_author_exit_code':0,'actual_pre_readback_exit_code':0,'actual_final_readback_exit_code':0,'actual_finalizer_pid':os.getpid(),'reviewer_compilers':'NOT_STARTED_CLOSED','no_VERIFIED_or_Gamma_or_wholepaper_admission':True,'last_filesystem_operation':'This CLOSEDLAST lease write; no reads or writes follow it in this process.'}
assert not (O/'lease.json').exists()
(O/'lease.json').write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result))
