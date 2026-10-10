from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=r/'exact-science-label-recheck73'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='192fe75b7dc68bec850ec2189b56f02228d5a4c0e0d5250cfa2be52495272e99'
l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert len(rows)==77 and l['owned_count']==78 and l['status']=='CLOSED_LAST' and l['VERIFIED'] and l['all_sessions_closed'] and not l['postclose_owned_writes']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
assert sha(can(rows))==l['closure_logical_sha256']
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['whole_logical_run_sha256']=='507dd32fc6a863e416b503057505b1224237f9cf6082fbc884a4fd134e5e37ef'
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['checked_commit']==l['verified_commit']=='d7e00a7c0e8b0f37fcc2dbe99f6b646d3a7b1de6'
assert run['actor']=='/root/exact_science63' and run['VERIFIED'] and run['parent']==subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()
for key in ['complete_named_RAW_payload','decision','inputs_manifest','shared_verified','transition']:check(run[key])
assert run['complete_named_RAW_payload']['RAW_sha256']=='43f94fa93353a32ac3bd1463f497ea36c99ea7491464296863a787ceebfbbea4'
payload=load(run['complete_named_RAW_payload']['path']);inputs=load(run['inputs_manifest']['path']);assert inputs==payload['inputs'] and inputs['input_count']==len(inputs['inputs'])==40
for z in inputs['inputs']:check(z)
d=load(run['decision']['path']);t=load(run['transition']['path']);v=load(run['shared_verified']['path'])
assert payload['decision']==d and payload['transition']==t==v and d['accepted_exact_commit'] and not d['original_commit_VERIFIED'] and d['fake_closure_hits']==0
assert t['transition_count']==1 and t['verifier_id']=='/root/exact_science63' and t['owner_id']!=t['verifier_id'] and t['actual_transition_PID']==23996
ledger=Path('runs/substantive_advances.jsonl').read_bytes();n=t['ledger_before']['RAW_bytes'];append=check(t['exact_append'])
assert len(ledger)==t['ledger_after']['RAW_bytes'] and sha(ledger)==t['ledger_after']['RAW_sha256'] and sha(ledger[:n])==t['ledger_before']['RAW_sha256']
assert ledger[n:]==append and len(append.splitlines())==1 and json.loads(append)==t['event'] and t['event']['to_state']=='VERIFIED' and t['event']['from_state']=='PROVED_LOCAL'
assert all(q['exit_code']==0 for q in payload['gates']['receipts'])
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'recheck73.py'),'postclose'],stdout=s,stderr=e);code=p.wait()
assert code==0
record=dict(status='ACCEPTED_NONOWNER_EXACT_SCI73_LABEL_CHILD',actual_root_PID=os.getpid(),native_verified=True,verified_commit=head,native_files=78,finite_current_inputs=40,native_whole_logical_run_sha256=h,native_complete_named=run['complete_named_RAW_payload'],native_lease=pin(lp),native_readonly_PID=p.pid,native_readonly_EXIT=code,unique_VERIFIED_transition_PID=23996,unique_VERIFIED_append=pin(Path(t['exact_append']['path'])),old_failed_science_commit_VERIFIED=False,fresh_Lean_PID_36212_reused_exact_RAW=True,full_RAW_whitespace_PASS=False,authored_complement_PASS=True,aggregate=False,reader=False,main_live=False,PURIFIED=False,Goal_complete=False)
q=r/'root.exact-verification73.adoption.json';assert not q.exists();q.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS73 CLOSED78/40pins exact child VERIFIED adopted; old failedSCI remains unverified; shared aggregate/reader pending.')
