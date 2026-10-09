from pathlib import Path
import subprocess,sys,json,os,hashlib
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;ROOT=Path('E:/Samplinglib');PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest(),LF_bytes=len(lf),LF_sha256=hashlib.sha256(lf).hexdigest())
label=sys.argv[1];assert not (O/'lease.final.json').exists();assert not (O/f'{label}.receipt.json').exists()
helper=O/'math72.py';(O/f'{label}.executed-helper.RAW.py').write_bytes(helper.read_bytes());start=datetime.now(timezone.utc).isoformat();out=O/f'{label}.stdout.log';err=O/f'{label}.stderr.log';cmd=[PY,'-B','-X','utf8',str(helper),sys.argv[2] if len(sys.argv)>2 else label]
with out.open('wb') as fo,err.open('wb') as fe:
 p=subprocess.Popen(cmd,cwd=ROOT,stdout=fo,stderr=fe);print(json.dumps(dict(started=label,actual_foreground_PID=p.pid,runner_PID=os.getpid())),flush=True);ec=p.wait()
d=dict(label=label,command=cmd,actual_foreground_PID=p.pid,actual_runner_PID=os.getpid(),started_utc=start,finished_utc=datetime.now(timezone.utc).isoformat(),exit_code=ec,terminal_closed=True,stdout=pin(out),stderr=pin(err));(O/f'{label}.receipt.json').write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n');print(json.dumps(d),flush=True);print(out.read_text(encoding='utf-8',errors='replace')[-4500:],flush=True)
if ec:print(err.read_text(encoding='utf-8',errors='replace')[-7000:],flush=True)
sys.exit(ec)
