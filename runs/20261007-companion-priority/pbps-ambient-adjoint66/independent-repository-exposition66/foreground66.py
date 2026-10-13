import sys,os,pathlib,subprocess,json,datetime,hashlib
O=pathlib.Path(__file__).resolve().parent;label,script=sys.argv[1:3]
out=O/(label+'.stdout.RAW.log');err=O/(label+'.stderr.RAW.log');cmd=['C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe','-X','utf8',str(O/script)];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with out.open('wb') as a,err.open('wb') as b:
 p=subprocess.Popen(cmd,cwd='E:/Samplinglib',stdout=a,stderr=b);pid=p.pid;rc=p.wait()
def pin(p):
 b=p.read_bytes();return {'name':p.name,'RAW_bytes':len(b),'RAW_sha256':hashlib.sha256(b).hexdigest(),'LF_sha256':hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest()}
j={'schema':'repo66-actually-observed-foreground-terminal-v1','label':label,'actual_wrapper_PID':os.getpid(),'actual_foreground_PID':pid,'actual_exit':rc,'command':cmd,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'terminal_closed':True,'stdout':pin(out),'stderr':pin(err)}
(O/(label+'.receipt.json')).write_bytes(json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2).encode()+b'\n');print(json.dumps(j));print(out.read_text(encoding='utf-8'));print(err.read_text(encoding='utf-8'));sys.exit(rc)
