from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80/exact-commit-verification80'
C='ac7cabf30e17a322ec187b7eb13e1a9d4a57695d'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,v):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');cmd=[sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (O/'post-admission-frontier.stdout.log').open('xb') as out,(O/'post-admission-frontier.stderr.log').open('xb') as err:
 child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);code=child.wait()
save('post-admission-frontier.receipt.json',dict(command_argv=cmd,cwd=str(R),verified_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/'post-admission-frontier.stdout.log'),stderr=info(O/'post-admission-frontier.stderr.log')))
assert code==0
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C
v=json.loads((O/'verified.json').read_text(encoding='utf-8'));assert v['verified_commit']==C
cell=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-measurability.json'
cd=json.loads(cell.read_text(encoding='utf-8'));assert cd['status']=='independently_verified' and isinstance(cd['evidence']['independent_verification'],str)
files=sorted([p for p in O.iterdir() if p.is_file()],key=lambda p:p.name)
save('closed-manifest80.json',dict(status='CLOSED_VERIFIED_CHILD_ADMISSION',verified_commit=C,verifier_id='/root/exact_verify77',verified=info(O/'verified.json'),admission=info(O/'admission80.json'),post_admission_frontier=info(O/'post-admission-frontier.receipt.json'),cell=info(cell),artifacts=[info(p) for p in files],manifest_self_hash_omitted=True,existing_stabilizing_lane_untouched=True,stabilization=False,Goal_complete=False))
print(json.dumps({'verified':info(O/'verified.json'),'closed_manifest':info(O/'closed-manifest80.json'),'post_admission_frontier':info(O/'post-admission-frontier.receipt.json')},ensure_ascii=False))
