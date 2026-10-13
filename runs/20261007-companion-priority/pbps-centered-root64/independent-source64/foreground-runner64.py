from pathlib import Path
import subprocess,sys,datetime,hashlib,json,os
ROOT=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
results=[]
for mode in ['finalizer','readback']:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();cmd=[sys.executable,str(ROOT/'native-finalizer64.py'),mode]
 child=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE);stdout,stderr=child.communicate();ended=datetime.datetime.now(datetime.timezone.utc).isoformat()
 logs={}
 for label,raw in [('stdout',stdout),('stderr',stderr)]:
  name=f'foreground-{mode}.{label}.log';(ROOT/name).write_bytes(raw);logs[label]={'relative_path':name,'raw_bytes':len(raw),'raw_sha256':sha(raw),'lf_sha256':sha(raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))}
 receipt={'schema':'source64-actual-foreground-terminal-receipt-v1','mode':mode,'command':cmd,'cwd':str(ROOT),'started_utc':started,'finished_utc':ended,'actual_foreground_pid':child.pid,'parent_foreground_pid':os.getpid(),'exit_code':child.returncode,'terminal_closed':True,**logs}
 (ROOT/f'foreground-{mode}.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');results.append(receipt)
 if child.returncode:
  print(stdout.decode('utf-8'));print(stderr.decode('utf-8'));sys.exit(child.returncode)
print(json.dumps({'actual_foreground_validation_runs':[{'mode':x['mode'],'pid':x['actual_foreground_pid'],'exit_code':x['exit_code'],'terminal_closed':x['terminal_closed']} for x in results]},indent=2))
