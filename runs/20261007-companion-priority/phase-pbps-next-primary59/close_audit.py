from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),
 'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
 assert json.loads(p.read_bytes())==x
 return pin(p)
assert not (O/'lease.json').exists()
env=dict(os.environ);env['PYTHONUTF8']='1'
r=subprocess.run([sys.executable,str(O/'verify_readbacks.py')],cwd=R,env=env,
 capture_output=True,encoding='utf8')
assert r.returncode==0, (r.stdout,r.stderr)
readback={'command':'python runs/20261007-companion-priority/phase-pbps-next-primary59/verify_readbacks.py',
 'actual_exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
 'stdout_sha256':sha(r.stdout.encode()),'result':json.loads(r.stdout),'completed_at':now()}
manifest=json.loads((O/'input.manifest.json').read_bytes())
observations=[]
for p in manifest['inputs']:
 current=pin(R/p['path'])
 observations.append({'path':p['path'],'matches_observed_raw':current['raw_sha256']==p['raw_sha256'],
 'original_observation':p,'closure_observation':current,
 'interpretation':'Mutable control can drift under root sole stabilization; original observed bytes remain the audit input. Fixed primary/Mathlib drift is forbidden.'})
 if '/mathlib/' in p['path'] or 'primary-pbps.' in p['path']:
  assert current['raw_sha256']==p['raw_sha256']
put('output.readbacks.json',{'foreground_check':readback,'input_current_readbacks':observations,
 'headers_readback':'Exact saved public-header bytes and all19 Mathlib spans verified by actual foreground subprocess; no compiler called.'})
payload_files=[pin(p) for p in sorted(O.iterdir()) if p.is_file()]
payload={'payload_name':'primary59.actual-selfadjoint-centered-T-source-only-audit',
 'files':payload_files,'file_count':len(payload_files)}
run={'schema_version':1,'actor':'/root/next_primary59','status':'SOURCE_ONLY_AUDIT_CLOSED',
 'completed_at':now(),'science_status':'NO_SAU_NO_PROOF_NO_FORMAL_ADMISSION',
 'compiler':'NOT_STARTED_CLOSED','candidate59_supplied':False,'root_only_stabilization_unchanged':True,
 'checks':{'author_foreground_exit_code':0,'readback_foreground_exit_code':r.returncode,
 'anchors':17,'headers':4,'api_spans':19,'blueprint_steps':7},
 'named_payload':payload,'named_payload_sha256':sha(canon(payload)),
 'run_hash_convention':'SHA256 canonical UTF8 JSON of the whole run, excluding only top-level run_sha256. named_payload_sha256 hashes the distinct named_payload value and is not the run hash.',
 'memory_trace':{'citation':'MEMORY.md:553-554|note=[historical PBPS SPHMC boundary prompted current source verification]',
 'rollout_id':'01a08b25-37dc-7d43-90fa-9c251088dbf2','current_evidence_supersedes_memory':True},
 'failures_preserved':['author_audit.failed0.snapshot.py','primary.anchors.failed0.snapshot.json'],
 'lease_order':'All source/API/output readbacks actual EXIT0 before lease.json is written CLOSEDLAST; no post-closure file mutation by this actor.'}
run['run_sha256']=sha(canon(run))
put('reviewer.primary.run.json',run)
v=json.loads((O/'reviewer.primary.run.json').read_bytes());h=v.pop('run_sha256');assert sha(canon(v))==h
assert sha(canon(v['named_payload']))==v['named_payload_sha256']
# The final filesystem write/readback is the CLOSEDLAST lease, after all foreground checks EXIT0.
lease={'schema_version':1,'actor':'/root/next_primary59','status':'CLOSEDLAST',
 'closed_at':now(),'scope':'source-only audit','compiler':'NOT_STARTED_CLOSED',
 'foreground_readbacks_exit_code':r.returncode,'run':pin(O/'reviewer.primary.run.json'),
 'run_sha256':h,'admission':False,'no_postclosure_work':True}
put('lease.json',lease)
print(json.dumps({'status':'CLOSEDLAST','run_sha256':h,
 'named_payload_sha256':v['named_payload_sha256'],'payload_files':len(payload_files),
 'readbacks_exit_code':r.returncode,'compiler':'NOT_STARTED_CLOSED','candidate59':'NONE'}))
