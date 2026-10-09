from pathlib import Path
import subprocess,sys,os,datetime,hashlib,json
ROOT=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
receipts=[]
for mode in ['finalizer','readback']:
 cmd=[sys.executable,str(ROOT/'native-finalizer64.py'),mode];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat();logs={}
 for k,raw in [('stdout',out),('stderr',err)]:
  name=f'foreground-{mode}.{k}.log';(ROOT/name).write_bytes(raw);logs[k]={'relative_path':name,'raw_bytes':len(raw),'raw_sha256':sha(raw)}
 receipt={'schema':'source64-auxiliary-overlay-foreground-receipt-v1','command':cmd,'actual_foreground_pid':p.pid,'runner_pid':os.getpid(),'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'terminal_closed':True,**logs};(ROOT/f'foreground-{mode}.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');receipts.append(receipt)
 if p.returncode:print(out.decode('utf-8'));print(err.decode('utf-8'));sys.exit(p.returncode)
print(json.dumps({'actual_foreground_runs':[{'pid':x['actual_foreground_pid'],'exit_code':x['exit_code'],'terminal_closed':x['terminal_closed']} for x in receipts],'runner_pid':os.getpid()},indent=2))
