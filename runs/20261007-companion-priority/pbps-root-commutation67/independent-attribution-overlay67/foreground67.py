import os,sys,json,hashlib,subprocess,datetime
from pathlib import Path
O=Path(__file__).resolve().parent
assert not (O/'lease.final.json').exists(),'CLOSED_LAST'
mode=sys.argv[1]
label={'finalize':'finalizer','readback':'readback','closevalidate':'closevalidate'}[mode]
stdout=O/('foreground-'+label+'.stdout.RAW.log');stderr=O/('foreground-'+label+'.stderr.RAW.log')
assert not stdout.exists() and not stderr.exists(),'No terminal overwrite'
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONIOENCODING']='utf-8'
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with stdout.open('wb') as fo,stderr.open('wb') as fe:
 child=subprocess.Popen([sys.executable,str(O/'native67.py'),mode],stdout=fo,stderr=fe,env=env,cwd=str(O));code=child.wait()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest(),'LF_bytes':len(l),'LF_sha256':hashlib.sha256(l).hexdigest()}
receipt={'schema':'overlay67-actual-foreground-process-receipt-v1','operation':mode,'actual_child_PID':child.pid,'actual_observer_PID':os.getpid(),'actual_EXIT':code,'command':[sys.executable,str(O/'native67.py'),mode],'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stdout':pin(stdout),'stderr':pin(stderr),'foreground_wait_completed':True}
(O/('foreground-'+label+'.receipt.json')).write_bytes((json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
print(json.dumps(receipt));print(stdout.read_text(encoding='utf-8'));print(stderr.read_text(encoding='utf-8'))
sys.exit(code)
