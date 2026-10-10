from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');o=r/'exact-science-verification75'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
expected_run,expected_lease,expected_payload=sys.argv[1:]
lp=o/'lease.final.json';assert sha(lp.read_bytes())==expected_lease
l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert l['owned_count']==len(rows)+1 and l['status']=='CLOSED_LAST' and l['VERIFIED'] and l['all_sessions_closed'] and not l['postclose_owned_writes']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
assert sha(can(rows))==l['closure_logical_sha256']
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['whole_logical_run_sha256']==expected_run
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==run['checked_commit']==l['verified_commit']
assert run['actor']=='/root/exact_science63' and run['VERIFIED'] and run['parent']==subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()
for key in ['complete_named_RAW_payload','decision','inputs_manifest','shared_verified','transition']:check(run[key])
assert run['complete_named_RAW_payload']['RAW_sha256']==expected_payload
payload=load(run['complete_named_RAW_payload']['path']);inputs=load(run['inputs_manifest']['path']);assert inputs==payload['inputs'] and inputs['input_count']==len(inputs['inputs'])
for z in inputs['inputs']:check(z)
d=load(run['decision']['path']);t=load(run['transition']['path']);v=load(run['shared_verified']['path'])
assert payload['decision']==d and payload['transition']==t==v and d['accepted_exact_commit'] and d['fake_closure_hits']==0
assert t['transition_count']==1 and t['verifier_id']=='/root/exact_science63' and t['owner_id']!=t['verifier_id']
ledger=Path('runs/substantive_advances.jsonl').read_bytes();n=t['ledger_before']['RAW_bytes'];append=check(t['exact_append'])
assert len(ledger)==t['ledger_after']['RAW_bytes'] and sha(ledger)==t['ledger_after']['RAW_sha256'] and sha(ledger[:n])==t['ledger_before']['RAW_sha256']
assert ledger[n:]==append and len(append.splitlines())==1 and json.loads(append)==t['event'] and t['event']['to_state']=='VERIFIED' and t['event']['from_state']=='PROVED_LOCAL'
assert all(q['exit_code']==0 for q in payload['gates']['receipts'])
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'verify75.py'),'postclose'],stdout=s,stderr=e);code=p.wait()
assert code==0
record=dict(status='ACCEPTED_NONOWNER_EXACT_SCI75',actual_root_PID=os.getpid(),native_verified=True,verified_commit=head,native_files=l['owned_count'],finite_current_inputs=inputs['input_count'],native_whole_logical_run_sha256=h,native_complete_named=run['complete_named_RAW_payload'],native_lease=pin(lp),native_readonly_PID=p.pid,native_readonly_EXIT=code,unique_VERIFIED_transition_PID=t['actual_transition_PID'],unique_VERIFIED_append=pin(Path(t['exact_append']['path'])),fresh_direct_Lean_math75_PID18716_exact_RAW_reused=True,full_RAW_whitespace_PASS=False,authored_complement_PASS=True,aggregate=False,reader=False,main_live=False,PURIFIED=False,Goal_complete=False)
q=r/'root.exact-verification75.adoption.json';assert not q.exists();q.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 CLOSED native exactSCI VERIFIED adopted; serialized shared aggregate/current reader remain pending.')
