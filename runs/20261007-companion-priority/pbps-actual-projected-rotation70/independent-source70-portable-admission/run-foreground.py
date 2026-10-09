import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,subprocess,os,datetime,hashlib
O=pathlib.Path(__file__).resolve().parent
label,script=sys.argv[1:3];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen([sys.executable,str(O/script),*sys.argv[3:]],cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONIOENCODING':'utf-8'})
out,err=p.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
r={'schema':'portable-admission70-actual-foreground-terminal-v1','actual_pid':p.pid,'exit_code':p.returncode,'start_utc':start,'end_utc':end,'foreground':True,'command_argv':[sys.executable,str(O/script),*sys.argv[3:]],'cwd':'E:/Samplinglib'}
for k,b in [('stdout',out),('stderr',err)]:
 n=label+'.'+k+'.exactraw.txt';assert not (O/n).exists();(O/n).write_bytes(b);r[k]={'name':n,'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest()}
(O/(label+'.terminal-receipt.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(r,ensure_ascii=False));print(out.decode('utf-8'),end='');print(err.decode('utf-8'),end='');sys.exit(p.returncode)
