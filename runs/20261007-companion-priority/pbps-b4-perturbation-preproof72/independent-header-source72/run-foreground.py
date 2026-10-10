import sys
sys.dont_write_bytecode=True
import json,os,pathlib,subprocess,hashlib,datetime
sys.stdout.reconfigure(encoding='utf-8')
O=pathlib.Path(__file__).resolve().parent
label,script=sys.argv[1:3];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.Popen([sys.executable,str(O/script),*sys.argv[3:]],cwd='E:/Samplinglib',stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONIOENCODING':'utf-8','PYTHONDONTWRITEBYTECODE':'1'})
out,err=p.communicate();end=datetime.datetime.now(datetime.timezone.utc).isoformat()
for suffix,data in [('stdout',out),('stderr',err)]:(O/(label+'.'+suffix+'.exactraw.txt')).write_bytes(data)
receipt={'schema':'independent-header-source72-foreground-terminal-v1','label':label,'actual_pid':p.pid,'exit_code':p.returncode,'foreground':True,'background':False,'start_utc':start,'end_utc':end,'command_argv':[sys.executable,str(O/script),*sys.argv[3:]],'cwd':'E:/Samplinglib','stdout':{'name':label+'.stdout.exactraw.txt','RAW_bytes':len(out),'RAW_sha256':hashlib.sha256(out).hexdigest()},'stderr':{'name':label+'.stderr.exactraw.txt','RAW_bytes':len(err),'RAW_sha256':hashlib.sha256(err).hexdigest()}}
(O/(label+'.terminal-receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(receipt,ensure_ascii=True));print(out.decode('utf-8',errors='replace'),end='');print(err.decode('utf-8',errors='replace'),end='');sys.exit(p.returncode)
