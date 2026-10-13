from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');o=r/'independent-repository-reader75'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
expected_run,expected_lease,expected_payload=sys.argv[1:]
lp=o/'lease.final.json';assert sha(lp.read_bytes())==expected_lease
l=load(lp);assert l['status']=='CLOSED_LAST' and l['actor']=='/root/header_math72' and l['postclose_owned_writes_forbidden'] and l['final_owned_write']
rows=l['files'];assert l['file_count_including_lease']==len(rows)+1 and sha(can(rows))==l['closure_logical_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']==expected_run
for key in ['complete_named_RAW_payload','decision','inputs_manifest']:check(run[key])
assert run['complete_named_RAW_payload']['RAW_sha256']==expected_payload
payload=load(run['complete_named_RAW_payload']['path']);d=load(run['decision']['path']);inputs=load(run['inputs_manifest']['path'])
assert payload['decision']==d and payload['inputs']==inputs and d['accepted_scoped_aggregate'] and not d['blockers'] and d['independent_of_formalizer_stabilizer']
assert d['actor']=='/root/header_math72' and not d['new_VERIFIED_transition'] and not d['new_independent_mathematics_certification']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head==d['checked_science_commit']==run['checked_science_commit']
dispatch=load(r/'final-reader-repository-packet75.json');assert inputs['input_count']==len(inputs['inputs'])==len(dispatch['inputs'])
check(inputs['dispatch'])
for z in inputs['inputs']:check(z)
assert d['copy_callbacks']==d['RAW_downloads']==4 and d['formula_BODY_steps']==9 and d['independently_viewed_PNGs']==12
assert d['Registry']==524 and d['publication_units']==245
assert all(not d[k] for k in ['Goal_complete','PURIFIED','full_Exposition_Seal','main','live','whole_paper'])
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'review75.py'),'postclose'],stdout=s,stderr=e);code=p.wait()
assert code==0
record=dict(status='ACCEPTED_INDEPENDENT_SCOPED_AGGREGATE_READER75_WITH_EXPOSITION_DEBT',actual_root_PID=os.getpid(),accepted_scoped_aggregate=True,checked_science_commit=head,native_actor=d['actor'],native_lease=pin(lp),native_run_sha256=h,complete_named_RAW_payload=run['complete_named_RAW_payload'],native_files=l['file_count_including_lease'],current_inputs=inputs['input_count'],readonly_PID=p.pid,readonly_EXIT=code,reader_debts=d['reader_debts'],new_math_verification=False,full_Exposition_Seal=False,PURIFIED=False,main=False,live=False,whole_paper=False,Goal_complete=False)
q=r/'root.repository75.adoption.json';assert not q.exists();q.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 independent scoped aggregate/current reader adopted; remaining exposition/PDMP/paper boundaries retained.')
