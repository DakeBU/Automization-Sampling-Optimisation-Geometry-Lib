from pathlib import Path
import hashlib,json,os,subprocess,sys
pre=Path('runs/20261007-companion-priority/pbps-recursive-preproof76');o=pre/'independent-math-header76'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'];return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='06db1672bd4d73b24c39c6b131254a950207b0377c1d34dea23f728518ef907d'
l=load(lp);assert l['status']=='CLOSED_LAST' and l['reviewer']=='/root/header_math72' and not l['full_target_proved'] and not l['VERIFIED']
rows=l['files'];assert len(rows)+1==l['owned_files']==71 and sha(can(rows))==l['closure_logical_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']=='41d66a32102d8381905cf64e7b8f74beca0b518711a50c034f33dc3d95c6f450'
assert run['status']=='ACCEPTED_V3_PROSPECTIVE_HEADER_ONLY' and not run['full_target_proved'] and not run['SAU'] and not run['source_review']
assert sha(check(run['complete_named_RAW_payload']))=='c6f01d01e5cfc79f7c3665c75b92c8e397bc6ebb999f8f8c213d282dec516e00'
check(run['original_header']);b=check(run['accepted_header']);assert b==(pre/'header76.v3.proposed.lean').read_bytes()
assert sha(b)=='996b8a89ffe84cfef8faf75551f962f2378db221841f5e1a38137eb81281d015'
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'readonly.stdout.log').open('wb') as s,(out/'readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'review76.py'),'readonly'],stdout=s,stderr=e);code=p.wait()
assert code==0
q=pre/'root.math-header76.adoption.json';assert not q.exists()
q.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_V3_MATH_HEADER_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_lease=pin(lp),native_complete_payload=run['complete_named_RAW_payload'],accepted_header=pin(pre/'header76.v3.proposed.lean'),native_typechecks=run['typechecks'],checked_parent=run['checked_parent'],current_parent=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),parent_qualification='Review began at INT74; exact source/parent/header inputs remain unchanged after the independent SCI75 proof commit. No future76 theorem is proved.',readonly_PID=p.pid,readonly_EXIT=code,source_header_review=False,Statement_Seal=False,SAU=False,VERIFIED=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 CLOSED71 prospective mathematical/header type review adopted; source header/seal/SAU/proof pending.')
