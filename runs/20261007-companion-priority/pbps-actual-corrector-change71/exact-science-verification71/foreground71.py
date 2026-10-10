from pathlib import Path
import subprocess,sys,json,os,hashlib
from datetime import datetime,timezone
OWN=Path(__file__).resolve().parent
ROOT=Path('E:/Samplinglib')
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
label=sys.argv[1];assert not (OWN/'lease.final.json').exists();assert not (OWN/f'{label}.receipt.json').exists()
helper=OWN/'verify71.py';(OWN/f'{label}.executed-helper.RAW.py').write_bytes(helper.read_bytes())
start=datetime.now(timezone.utc).isoformat();out=OWN/f'{label}.stdout.log';err=OWN/f'{label}.stderr.log'
cmd=[PY,'-B','-X','utf8',str(helper),sys.argv[2] if len(sys.argv)>2 else label]
with out.open('wb') as fo,err.open('wb') as fe:
 p=subprocess.Popen(cmd,cwd=ROOT,stdout=fo,stderr=fe)
 print(json.dumps(dict(started=label,actual_foreground_PID=p.pid,runner_PID=os.getpid())),flush=True);ec=p.wait()
d=dict(label=label,command=cmd,actual_foreground_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),exit_code=ec,terminal_closed=True,stdout=pin(out),stderr=pin(err))
(OWN/f'{label}.receipt.json').write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
print(json.dumps(d),flush=True)
print(out.read_text(encoding='utf-8',errors='replace')[-6000:],flush=True)
if ec:print(err.read_text(encoding='utf-8',errors='replace')[-8000:],flush=True)
sys.exit(ec)
