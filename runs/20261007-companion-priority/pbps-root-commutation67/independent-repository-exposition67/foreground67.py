from pathlib import Path
import sys,os,subprocess,json,datetime,hashlib
O=Path(__file__).resolve().parent
assert not (O/'lease.final.json').exists()
label,script=sys.argv[1:3]
assert Path(script).name==script and label.replace('-','').replace('_','').isalnum()
out=O/(label+'.stdout.RAW.log');err=O/(label+'.stderr.RAW.log')
cmd=[sys.executable,'-X','utf8',str(O/script),*sys.argv[3:]]
env=dict(os.environ);env['PYTHONIOENCODING']='utf-8';env['PYTHONDONTWRITEBYTECODE']='1'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with out.open('wb') as a,err.open('wb') as b:
 p=subprocess.Popen(cmd,cwd='E:/Samplinglib',stdout=a,stderr=b,env=env);pid=p.pid;rc=p.wait()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'name':p.name,'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest(),'LF_bytes':len(l),'LF_sha256':hashlib.sha256(l).hexdigest()}
j={'schema':'repository67-actually-observed-foreground-terminal-v1','label':label,'actual_wrapper_PID':os.getpid(),'actual_foreground_PID':pid,'actual_exit':rc,'command':cmd,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'terminal_closed':True,'stdout':pin(out),'stderr':pin(err)}
(O/(label+'.receipt.json')).write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(j));print(out.read_text(encoding='utf-8'));print(err.read_text(encoding='utf-8'));sys.exit(rc)
