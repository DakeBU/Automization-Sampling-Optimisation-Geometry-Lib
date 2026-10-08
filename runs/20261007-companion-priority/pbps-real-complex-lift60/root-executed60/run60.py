from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
root=Path.cwd(); label,cmd=sys.argv[1],sys.argv[2:]
d=root/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60'/label
d.mkdir(exist_ok=False)
def pin(p):
 b=p.read_bytes(); return dict(path=p.relative_to(root).as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (d/'stdout.log').open('wb') as o,(d/'stderr.log').open('wb') as e:
 p=subprocess.Popen(cmd,cwd=root,env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8'),stdout=o,stderr=e); code=p.wait()
x=dict(command=cmd,head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_pid=p.pid,exit_code=code,terminal_closed=True,stdout=pin(d/'stdout.log'),stderr=pin(d/'stderr.log'),scope='Exact statement type elaboration or foreground next60 local check; not independent mathematical/source acceptance.')
(d/'receipt.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(label=label,pid=p.pid,exit_code=code)))
print((d/'stdout.log').read_text(encoding='utf-8',errors='replace')[-12000:])
print((d/'stderr.log').read_text(encoding='utf-8',errors='replace')[-2000:])
sys.exit(code)
