from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
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
env=dict(os.environ);env['PYTHONUTF8']='1'
p=subprocess.run([sys.executable,str(O/'verify_readbacks.py')],cwd=R,env=env,capture_output=True,encoding='utf8')
assert p.returncode==0,(p.stdout,p.stderr)
put('foreground-readbacks.json',{'actual_command':'python '+(O/'verify_readbacks.py').relative_to(R).as_posix(),
 'actual_exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'stdout_sha256':sha(p.stdout.encode()),
 'result':json.loads(p.stdout),'completed_at':now(),'compiler_by_reviewer':'NOT_STARTED'})
payload=json.loads((O/'named-source-overlay.payload.json').read_bytes())
run={'schema_version':1,'actor':'/root/next_primary59','status':'CLOSED_EXACT_SYNTAX_OVERLAY_SOURCE_ACCEPTED',
 'completed_at':now(),'named_source_overlay_payload':payload,'named_source_overlay_payload_sha256':sha(canon(payload)),
 'output_files_before_run':[pin(p) for p in sorted(O.rglob('*')) if p.is_file()],
 'checks':{'review_author_foreground_exit_code':0,'readback_foreground_exit_code':p.returncode,
 'immutable_inputs':14,'headers':2,'identity_annotations':11,'complete_named_rfl_equalities':2,'EXCESS':0},
 'accepted_scope':'Exact proposed successor headers: definitionally equal explicit identity-operator types only, no source or assumption repair.',
 'compiler_by_reviewer':'NOT_STARTED_CLOSED','PROVED_VERIFIED_Gamma_fullpaper_admission':False,
 'old_evidence_untouched':True,'root_only_production_writer':True,
 'native_hash_rule':'SHA256 canonical UTF8 JSON of entire run excluding ONLY top-level run_sha256; named payload hash is separate.',
 'closure_order':'Actual foreground readbacks EXIT0 and native/payload hash readbacks before final CLOSEDLAST lease write.'}
run['run_sha256']=sha(canon(run));put('run.json',run)
v=json.loads((O/'run.json').read_bytes());h=v.pop('run_sha256');assert sha(canon(v))==h
assert sha(canon(v['named_source_overlay_payload']))==v['named_source_overlay_payload_sha256']
put('lease.json',{'schema_version':1,'actor':'/root/next_primary59','status':'CLOSEDLAST','closed_at':now(),
 'foreground_readbacks_exit_code':p.returncode,'compiler_by_reviewer':'NOT_STARTED_CLOSED',
 'native_run':pin(O/'run.json'),'run_sha256':h,
 'named_source_overlay_payload_sha256':v['named_source_overlay_payload_sha256'],
 'scope':'Exact independent syntax/API source overlay acceptance; no mathematical proof or source assumption repair.',
 'old_evidence_untouched':True})
print(json.dumps({'status':'CLOSEDLAST','run_sha256':h,
 'named_source_overlay_payload_sha256':v['named_source_overlay_payload_sha256'],
 'source_review_raw_sha256':pin(O/'source-overlay-review.json')['raw_sha256'],
 'readback_actual_exit_code':p.returncode,'verdict':'EXACT_SYNTAX_OVERLAY_ACCEPTED','compiler_by_reviewer':'NOT_STARTED_CLOSED'}))
